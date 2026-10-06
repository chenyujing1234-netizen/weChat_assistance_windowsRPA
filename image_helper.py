# -*- coding: utf-8 -*-

import os
import hashlib
from PIL import Image
import time
import traceback
from cv2 import imread, absdiff, cvtColor, inRange, countNonZero, COLOR_BGR2HSV, imdecode
import numpy as np
from app_info import * 
from log_helper import print_my
from error_code import *
from server_http_opt import upload_snape

g_get_screen_func = None
##############################################################################
# 获得图片的md5值
def get_md5_of_image(image_path):
    # 创建一个md5对象
    md5 = hashlib.md5()
    
    # 打开图片文件并读取内容
    with open(image_path, 'rb') as file:
        while True:
            chunk = file.read(4096)  # 每次读取4096字节
            if not chunk:
                break
            md5.update(chunk)  # 更新md5对象
    
    # 获取最终的md5值
    return md5.hexdigest()
    
def pixel_equal(image1, image2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片像素点
    piex1 = image1.load()[x, y]
    piex2 = image2.load()[x, y]
    threshold = 10
    # 比较每个像素点的RGB值是否在阈值范围内，若两张图片的RGB值都在某一阈值内，则我们认为它的像素点是一样的
    #print(piex1[0], piex1[1], piex1[2])
    if abs(piex1[0] - piex2[0]) < threshold and abs(piex1[1]- piex2[1]) < threshold and abs(piex1[2] - piex2[2]) < threshold:
        return True
    else:
        return False

def compare(image1, image2):
    """
    进行比较
    :param image1:图片1
    :param image2: 图片2
    :return:
    """
    left = 0		# 坐标起始位置
    right_num = 0	# 记录相同像素点个数
    false_num = 0	# 记录不同像素点个数
    all_num = 0		# 记录所有像素点个数
    for i in range(left, image1.size[0]):
        for j in range(image1.size[1]):
            if pixel_equal(image1, image2, i, j):
                right_num += 1
            else:
                false_num += 1
            all_num += 1
    same_rate = right_num / all_num		# 相同像素点比例
    nosame_rate = false_num / all_num	# 不同像素点比例
    #print_my("same_rate: ", same_rate)
    #print_my("nosame_rate: ", nosame_rate)
    
    return same_rate

def compare_with_cv2(img_befor_cut_path, img_after_cut_path):
    # 读取两张图片
    image1 = imread(img_befor_cut_path)
    image2 = imread(img_after_cut_path)
    
    # 计算两张图片之间的差异
    difference = absdiff(image1, image2)
    # 设置一个阈值，用于判断像素点是否相似
    threshold = 50
    # 计算相似的像素点数量
    similar_pixels = np.sum(difference[:,:,0] < threshold) + np.sum(difference[:,:,1] < threshold) + np.sum(difference[:,:,2] < threshold)
    total_pixels = image1.shape[0] * image1.shape[1] * 3
    # 计算相似像素点的比例
    similarity_ratio = similar_pixels / total_pixels
    #print("相似像素点的比例为: {}".format(similarity_ratio))
    return similarity_ratio
    
def has_img_change(img_befor_cut_path, img_after_cut_path, need_rate = 0.93, b_debug = True):
    global g_img_count
    
    #  像素相似比例比较 
    try:
        """
        image_before = Image.open(img_befor_cut_path)
        image_after = Image.open(img_after_cut_path)
        same_rate = compare(image_before, image_after)
        """
        same_rate = compare_with_cv2(img_befor_cut_path, img_after_cut_path)
    except Exception as e:
        print("!!!!!has_img_change出现异常\n{}".format(e))
        if "where arrays have the same size and the same number of" in str(e): 
            #return APP_RET_CODE_FORMAT_ERROR, False
            time.sleep(2)
            return APP_RET_CODE_SUCESS, True
        
        upload_snape(img_befor_cut_path)
        upload_snape(img_after_cut_path)
        traceback.print_exc()  # 打印详细的堆栈信息
        return APP_RET_CODE_UNKNOW, False
        
    # 比较方式二：md5比较 
    #md5_before = md5(open(img_befor_cut_path, "rb").read())
    #md5_after = md5(open(img_after_cut_path, "rb").read())
    #if md5_before.hexdigest() != md5_after.hexdigest():
    if same_rate > need_rate:
        # chenyj debug
        if b_debug == True:
            print("   图片没有改变，same_rate:{}".format(same_rate))
        return APP_RET_CODE_SUCESS, False
    # chenyj debug
    print("   图片发生了改变，same_rate:{}".format(same_rate))     
    return APP_RET_CODE_SUCESS, True
#has_img_change("C://Users//admin//Desktop//6666.jpg", "C://Users//admin//Desktop//6666.jpg")
    
def image_init(get_screen_func):
    global g_get_screen_func
    g_get_screen_func = get_screen_func
    return 0

g_img_path_for_check_begin = SCREENSHOT_SAVE_DIR + "/" + "image_for_check_begin" + ".png" 
g_img_path_for_check_end = SCREENSHOT_SAVE_DIR + "/" + "image_for_check_end" + ".png" 
# 检查图片是否有变化开始（暂不支持并行） 
def image_check_begin():
    global g_get_screen_func
    
    if g_get_screen_func == None:
        print_my("image_check_begin, 还没有初始化")
        return 2
    
    g_get_screen_func(g_img_path_for_check_begin)
      
    return 0

def wait_image_change(input_event, need_rate = 0.990):
    TRY_COUNT_MAX = 10
    i_try_count = 0
    iRet = APP_RET_CODE_UNKNOW
    while i_try_count < TRY_COUNT_MAX:
        i_try_count += 1
        if True == input_event.wait(0.5):
            print("wait_image_change, 被要求退出1")
            return -1  
        iRet, bChange = image_check_end(need_rate)
        if iRet == 0 and bChange == True:
            if True == input_event.wait(0.5):
                print("wait_image_change, 被要求退出2")
                return -1  
            return APP_RET_CODE_SUCESS
        if iRet == APP_RET_CODE_UNKNOW and bChange == False:
            break
        
    if iRet == APP_RET_CODE_FORMAT_ERROR:
        return APP_RET_CODE_SUCESS
    
    return APP_RET_CODE_UNKNOW
    
# 检查图片是否有变化结束（暂不支持并行）
def image_check_end(need_rate = 0.95):
    global g_get_screen_func

    bChange = False 
    if g_get_screen_func == None:
        print_my("image_check_begin, 还没有初始化")
        return 2, bChange
        
    g_get_screen_func(g_img_path_for_check_end)
    
    iRet, bChange = has_img_change(g_img_path_for_check_begin, g_img_path_for_check_end, need_rate)
    
    return iRet, bChange
    
def image_is_white(image):
    # 将图像转换为HSV颜色空间
    hsv = cvtColor(image, COLOR_BGR2HSV)
    # 定义白色在HSV中的范围
    lower_white = np.array([0, 0, 255])
    upper_white = np.array([0, 0, 255])
    # 创建掩码
    mask = inRange(hsv, lower_white, upper_white)
    # 计算白色区域的像素数量
    white_count = countNonZero(mask)
    # 如果白色区域占主导，则认为背景是白色
    #print("  白色占{:.2f}%".format(white_count/image.size))
    return white_count > image.size * 0.15

def image_is_gray(image):
    # 将图像转换为HSV颜色空间
    hsv = cvtColor(image, COLOR_BGR2HSV)
    # 定义灰色的HSV阈值范围
    #lower_gray = np.array([0, 50, 0])
    #upper_gray = np.array([180, 70, 255])
    lower_gray = np.array([0, 0, 225])
    upper_gray = np.array([0, 0, 225])
    # 创建掩码
    mask = inRange(hsv, lower_gray, upper_gray)
    # 计算灰色区域的像素数量
    gray_count = countNonZero(mask)
    # 如果白色区域占主导，则认为背景是灰色
    #print("  灰色占{:.2f}%".format(gray_count/image.size))
    return gray_count > image.size * 0.15

def image_is_blue(image):
    # 将图像转换为HSV颜色空间
    hsv = cvtColor(image, COLOR_BGR2HSV)
    # 定义蓝色的HSV范围
    # 50, 142, 236
    lower_blue = np.array([49, 141, 235])
    upper_blue = np.array([51, 143, 237])
    # 创建掩码
    mask = inRange(hsv, lower_blue, upper_blue)
    # 计算蓝色区域的像素数量
    blue_count = countNonZero(mask)
    # 如果蓝色区域占主导，则认为背景是蓝色
    #print("  蓝色占{:.2f}%".format(blue_count/image.size))
    return blue_count > image.size * 0.15
 
def image_is_black(image):
    # 将图像转换为HSV颜色空间
    hsv = cvtColor(image, COLOR_BGR2HSV)
    # 定义黑色在HSV中的范围
    lower_black = np.array([0, 0, 15])
    upper_black = np.array([0, 0, 68])
    # 创建掩码
    mask = inRange(hsv, lower_black, upper_black)
    # 计算黑色区域的像素数量
    black_count = countNonZero(mask)
    # 如果白色区域占主导，则认为背景是黑色
    #print("  黑色占{:.2f}%".format(black_count/image.size))
    #return black_count > image.size * 0.15
    return black_count > image.size * 0.01
    
# 判断一张图片中的红色像素所在的区域占整张图的比例
def calculate_red_area_ratio(image_path):
    #image = imread(image_path)
    image = imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
     
    # 将图像转换为HSV颜色空间
    hsv = cvtColor(image, COLOR_BGR2HSV)
    # 定义红色在HSV中的范围
    lower_red = np.array([0, 172, 225])
    upper_red = np.array([0, 172, 250])
    # 创建掩码
    mask = inRange(hsv, lower_red, upper_red)
    # 计算红色区域的像素数量
    red_count = countNonZero(mask)
    
    red_area_ratio = red_count / image.size
    # chenyj debug
    print(f"红色像素区域占整张图片的比例: {red_area_ratio:.2%}")

    return red_area_ratio


# 判断一张图片中的绿色像素所在的区域占整张图的比例
def calculate_green_area_ratio(image_path, log_text = ""):
    #image = imread(image_path)
    image = imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
     
    # 将图像转换为HSV颜色空间
    hsv = cvtColor(image, COLOR_BGR2HSV)
    # 定义绿色在HSV中的范围
    lower_green = np.array([74, 245, 183])
    upper_green = np.array([74, 246, 193])
    # 创建掩码
    mask = inRange(hsv, lower_green, upper_green)
    # 计算绿色区域的像素数量
    green_count = countNonZero(mask)
    
    green_area_ratio = green_count / image.size
    # chenyj debug
    print(f"[{log_text}]绿色像素区域占整张图片的比例: {green_area_ratio:.2%}")

    return green_area_ratio