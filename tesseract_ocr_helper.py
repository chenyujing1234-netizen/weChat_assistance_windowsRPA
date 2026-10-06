# -*- coding: utf-8 -*-
import os
from cv2 import imread
import cv2
from threading import Lock
import traceback
import pytesseract
# pip install line_profiler -i https://pypi.tuna.tsinghua.edu.cn/simple
from app_info import * 
from error_code import *
from log_helper import print_my
from time_helper import TIME_BEGIN, TIME_END
from server_http_opt import upload_snape
import test_baidu_ocr

TESSDATA_DIR_PATH = TESSERACT_DIR + "\\tessdata"
TESSERACT_EXE_PATH = TESSERACT_DIR + "\\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = TESSDATA_DIR_PATH
# 配置Tesseract的安装路径（如果需要的话）
pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH

#tesseract_lan = pytesseract.get_languages(config="")
#print_my("!!!!tesseract支持的语言:{}".format(tesseract_lan))

g_lock_for_tesseract = Lock()
def tesseract_get_ocr_result(img_path):
    iRet = APP_RET_CODE_UNKNOW
    text_return = ""
    
    #TIME_BEGIN()
    g_lock_for_tesseract.acquire()
    try:
        img = imread(img_path)
        '''
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 二值化
        ret,binary = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
        # 保存二值化后的图像
        cv2.imwrite('binary_image.png', binary)
        """
        # 使用pytesseract进行文字框识别
        boxes = pytesseract.image_to_boxes(img, lang='chi_sim+eng')  # 支持中文和英文
        # 遍历识别结果，绘制矩形框
        for box in boxes.splitlines():
            box = box.split(' ')
            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv2.rectangle(img, (x, img.shape[0] - y), (x + w, img.shape[0] - h), (0, 0, 255), 2)
        # 保存或显示结果
        cv2.imwrite('output_image.jpg', img)
        """
        '''

        text_return = pytesseract.image_to_string(img, config='--psm 6', lang='chi_sim')
        text_return = text_return.replace(" ", "")
        # chenyj debug
        #print("!!!!!!tesseract识别文本:\n【\n{}\n】".format(text_return))
        iRet = APP_RET_CODE_SUCESS
        
        # 检查Tesseract OCR结果是否不理想，如果是则使用百度OCR
        img_height, img_width = img.shape[:2]
        if len(text_return) < 40 and img_width > 500 and img_height > 500:
            print("Tesseract OCR结果不理想，尝试使用百度OCR")
            try:
                # 调用百度OCR
                baidu_ocr_result = test_baidu_ocr.get_ocr_result(img_path)
                if baidu_ocr_result and "words_result" in baidu_ocr_result:
                    # 提取百度OCR的文本结果
                    baidu_text = ""
                    for result in baidu_ocr_result["words_result"]:
                        if "words" in result:
                            baidu_text += result["words"]
                    # 如果百度OCR返回了有效结果，则使用它
                    if baidu_text:
                        text_return = baidu_text
                        print("百度OCR识别成功，结果长度: {}".format(len(text_return)))
            except Exception as e:
                print_my("百度OCR调用异常: {}".format(e))
    except TypeError  as e:
        #print("!!!!!托管器还没准备好，导致tesseract失败")
        iRet = APP_RET_CODE_NO_READY
    except Exception as e:
        print_my("!!!!!tesseract_get_ocr_result, 异常:\n{}".format(e))
        upload_snape(img_path)
        traceback.print_exc()  # 打印详细的堆栈信息
        iRet = APP_RET_CODE_UNKNOW
    finally:
        g_lock_for_tesseract.release()
    
    #TIME_END()
    return iRet, text_return 
"""
#mg_path = SCREENSHOT_SAVE_DIR + "/" + "example" + ".png"
#img_path = SCREENSHOT_SAVE_DIR + "/" + "sao_ma_deng_lu" + ".jpg"
#img_path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_table_name" + ".png"
#img_path = SCREENSHOT_SAVE_DIR + "/" + "test3" + ".png"
#img_path = SCREENSHOT_SAVE_DIR + "/" + "test4" + ".png"
img_path = "C:\\Users\\admin\\Desktop\\4.png"
iRet, text_return = tesseract_get_ocr_result(img_path)
if iRet == APP_RET_CODE_SUCESS:
    print("OCR的结果:{}".format(text_return))
"""