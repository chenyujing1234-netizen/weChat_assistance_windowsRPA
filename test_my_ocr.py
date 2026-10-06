# -*- coding: utf-8 -*-
import requests
import os
from threading import Lock
from log_helper import print_my
from PIL import Image
from app_info import * 
from time_helper import TIME_BEGIN, TIME_END
from error_code import *

# 创建锁对象
g_lock_for_my_ocr = Lock()

def get_ocr_result_with_small_my(img_path):
    """
    请求服务端进行OCR识别，并返回识别结果
    
    参数:
        img_path: 图片的完整路径
    
    返回:
        iRet: 错误码，成功返回APP_RET_CODE_SUCESS，失败返回相应的错误码
        text_return: 识别出的文本内容
    """
    iRet = APP_RET_CODE_UNKNOW
    text_return = ""
    
    # 检查图片文件是否存在
    if not os.path.exists(img_path):
        print_my(f"MY OCR 错误：图片文件不存在 - {img_path}")
        return APP_RET_CODE_OCR_ERROR, text_return
    
    # 先对图片等比例缩放（与test_baidu_ocr.py保持一致）
    MAX_HEIGHT = 960
    float_ratio = 1.0
    img_path_of_real_ocr = img_path
    TEMP_IMG_NAME_FOR_OCR = SCREENSHOT_SAVE_DIR + "/temp_small_for_ocr.png"
    
    try:
        # 获取锁
        g_lock_for_my_ocr.acquire()
        TIME_BEGIN()
        with Image.open(img_path) as img:
            # 获取图片分辨率
            width, height = img.size
            if height > MAX_HEIGHT:
                height_new = MAX_HEIGHT
                float_ratio = height_new/height
                width_new = int(width*float_ratio)
                img_new = img.resize((width_new, height_new))
                img_new.save(TEMP_IMG_NAME_FOR_OCR)
                img_path_of_real_ocr = TEMP_IMG_NAME_FOR_OCR
    except Exception as e:
        print_my(f"MY OCR 图片处理异常: {e}")
        # 即使图片处理失败，也尝试直接使用原图
        img_path_of_real_ocr = img_path
        g_lock_for_my_ocr.release()
        return APP_RET_CODE_OCR_ERROR, text_return

    # 发送POST请求到OCR服务端
    ocr_url = "http://114.55.254.123/v1/ocr/upload"
    ocr_headers = {"X-API-Key": "35013bf90d5d49a3797d808f48967a78e4ed5bd1be1bd19c"}
    try:
        #print_my(f"正在请求OCR服务端: {ocr_url}")
        with open(img_path_of_real_ocr, 'rb') as f:
            files = {'file': (os.path.basename(img_path_of_real_ocr), f)}
            response = requests.post(ocr_url, headers=ocr_headers, files=files, timeout=30)

        # 检查响应状态
        if response.status_code == 200:
            # 解析JSON响应
            json_result = response.json()

            # 新OCR服务格式: {"success":true, "text":"全文", "lines":[{"text":..., "score":...}]}
            if json_result.get("success") == True:
                if "text" in json_result and json_result["text"]:
                    text_return = json_result["text"]
                elif "lines" in json_result and json_result["lines"]:
                    # text字段缺失时用分行结果拼接
                    text_return = "\n".join(line["text"] for line in json_result["lines"] if "text" in line)
                else:
                    # 图片上没有识别到任何文本，返回成功但文本为空
                    text_return = ""
                #print_my(f"OCR识别成功，识别文本长度: {len(text_return)}")
                iRet = APP_RET_CODE_SUCESS
            else:
                print_my(f"MY OCR服务返回失败: {json_result}")
                iRet = APP_RET_CODE_OCR_ERROR
        else:
            print_my(f"MY OCR服务请求失败，状态码: {response.status_code}")
            print_my(f"响应内容: {response.text}")
            iRet = APP_RET_CODE_OCR_ERROR
    
    except requests.exceptions.RequestException as e:
        print_my(f"MY OCR服务请求异常: {e}")
        iRet = APP_RET_CODE_OCR_ERROR
    except ValueError as e:
        print_my(f"MY OCR JSON解析异常: {e}")
        iRet = APP_RET_CODE_OCR_ERROR
    except Exception as e:
        print_my(f"MY OCR处理异常: {e}")
        iRet = APP_RET_CODE_OCR_ERROR
    finally:
        # 释放锁
        g_lock_for_my_ocr.release()
        # 清理临时文件
        if img_path_of_real_ocr != img_path and os.path.exists(img_path_of_real_ocr):
            try:
                os.remove(img_path_of_real_ocr)
            except:
                pass
        
        TIME_END()
    
    return iRet, text_return

"""
img_path = "C:\\Users\\admin\\Desktop\\test.jpg"
iRet, text_return = get_ocr_result_with_small_my(img_path)
print(f"OCR识别结果: {text_return}")
"""