# -*- coding: utf-8 -*-
import requests
import base64
import os
from log_helper import print_my
from PIL import Image
from app_info import * 
from time_helper import TIME_BEGIN, TIME_END
from error_code import *
    
############################################百度OCR#########################################
# client_id 为官网获取的AK， client_secret 为官网获取的SK
#g_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=9M92Xoucd01BO6MxtyALGoNS&client_secret=OEKte7F4z9jNyDkmKkduEIA80iKNaE5o'
#g_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ajM4fgiUqkwZqdtRaSxmb2h1&client_secret=OJthZ8tKFtofYDQwXXF7ythteyai0aoJ'
#g_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=UnRRXasUXt06F3YLcH9AmmIN&client_secret=OJthZ8tKFtofYDQwXXF7ythteyai0aoJ'
g_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=A9LcTOdLDiMGPPMJIhnNPWZx&client_secret=urjBP9eZYAAX425fxs4wRMDftCWv1CTb'
g_request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
###########################################阿里OCR###########################################
# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_ocr20191230
# pip install aliyun-python-sdk-core
# pip install aliyun-python-viapi-utils
# pip install viapi-utils
# pip install oss2

import os
from alibabacloud_ocr20191230.client import Client
from alibabacloud_ocr20191230.models import RecognizeCharacterRequest
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
import json 
from viapi.fileutils import FileUtils

#AccessKey ID
access_key_id = "YOUR_ALIYUN_ACCESS_KEY_ID"

#AccessKey Secret
access_key_secret = "YOUR_ALIYUN_ACCESS_KEY_SECRET"

config = Config(
  # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html
  # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html
  # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
  access_key_id=access_key_id,
  access_key_secret=access_key_secret,
  # 访问的域名
  endpoint='ocr.cn-shanghai.aliyuncs.com',
  # 访问的域名对应的region
  region_id='cn-shanghai'
)
#############################################################################################

g_access_token = None
 

os.environ["REQUESTS_CA_BUNDLE"] = "cacert.pem"
def get_access_token():
    global g_access_token
    global g_host
    try:
        print("====>get_access_token")
        #print(requests)
        #tt = requests.get("http://wwww.baidu.com")
        #print("23333")
        response = requests.get(g_host)
        print("<====get_access_token")
    except Exception as e: 
        print("!!!!!get_access_token, 出现异常\n Exception: {}==={}".format(e, g_host))
        print_my("!!!!!OCR组件初始化失败")
        return None
    if response:
        #print(response.json())
        pass
    access_token = response.json()["access_token"]
    g_access_token = access_token
    return access_token
 
# In[2]:
#get_access_token()

# encoding:utf-8
# 获取图片OCR的结果 
def get_ocr_result_from_baidu(img_path):
    global c, g_request_url
    
    if g_access_token == None:
        get_access_token()
    # 二进制方式打开图片文件
    #f = open('C:/Users/chenyujing/Documents/雷电模拟器/Pictures/Screenshots/Screenshot_2022-07-27-15-00-37.png', 'rb')
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = g_access_token
    request_url = g_request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(request_url, data=params, headers=headers)
    except Exception as e:
        print("!!!!!get_ocr_result_from_baidu, 出现异常，\n Exception: {}".format(e))
        return None
    if response:
        #print (response.json())
        try:
            json_return = response.json()
        except Exception as e:
            print("!!!!!get_ocr_result_from_baidu, 出现异常，response:{}. \n Exception: {}".format(response, e))
            return None
        return json_return
    return None




# In[4]:


#img_path = "C:/Users/chenyujing/Desktop/AI爬虫/示例图片/Screenshot_20220725-221046.png"
#img_path = "./评论.png"
#json_result = get_ocr_result(img_path)
#json_result


# In[5]:

# encoding:utf-8
# 获取图片OCR的结果 
def get_ocr_result_from_alibaba(img_path):
    
    # 二进制方式打开图片文件
    #f = open('C:/Users/chenyujing/Documents/雷电模拟器/Pictures/Screenshots/Screenshot_2022-07-27-15-00-37.png', 'rb')
     
    file_utils = FileUtils(access_key_id, access_key_secret)
    oss_url = file_utils.get_oss_url(img_path, "png", True)
    print(oss_url)

    recognize_character_request = RecognizeCharacterRequest(
            image_url=oss_url,
            min_height=10,
            output_probability=True
        )
    runtime = RuntimeOptions()
    try:
        # 初始化Client
        client = Client(config)
        response = client.recognize_character_with_options(recognize_character_request, runtime)
        # 获取整体结果
        print(response.body)
 
        json_return = {}
        words_result = []
        for result in response.body.data.results:
            print(result.text)
            print(result.probability)
            print(result.text_rectangles)
            location = {"top":result.text_rectangles.top, "left":result.text_rectangles.left, "width":result.text_rectangles.width, "height":result.text_rectangles.height}   
            word_result = {"words":result.text, "location":location}
            words_result.append(word_result)
            
        json_return["words_result"] = words_result
        return json_return
    except Exception as error:
        # tips: 可通过error.__dict__查看属性名称
        print("!!!!!get_ocr_result_from_alibaba, 出现异常，\n Exception: {}".format(error))
        return None
    return None

def is_Chinese_chr(ch):
    if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def is_Chinese_str(str):
    for ch in str:
        if True == is_Chinese_chr(ch):
            return True
    return False


# In[7]:

def get_ocr_result(img_path):
    # chenyj 在这里决定是使用百度还是使用阿里的OCR引擎 
    return get_ocr_result_from_baidu(img_path)
    #return get_ocr_result_from_alibaba(img_path)

# 带缩小操作后获取图片OCR的结果 
def get_ocr_result_with_small(img_path):
    # 先对图片等比例缩放
    MAX_HEIGHT = 960
    float_ratio = 1.0
    img_path_of_real_ocr = img_path
    TEMP_IMG_NAME_FOR_OCR = SCREENSHOT_SAVE_DIR + "/temp_small_for_ocr.png"
    
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
    json_return = get_ocr_result(img_path_of_real_ocr)

    if json_return is None:
        raise Exception("!!!!百度OCR接口调用失败.原因未知")
        TIME_END()
        return APP_RET_CODE_OCR_ERROR, json_return
    if "words_result" not in json_return:
        raise Exception("!!!!百度OCR接口调用失败.{}".format(json_return))
        return APP_RET_CODE_OCR_ERROR, json_return
        
    # 对坐标还原    
    for result in json_return["words_result"]:
        result["location"]["left"] = int(float(result["location"]["left"])/float_ratio)
        result["location"]["top"] = int(float(result["location"]["top"])/float_ratio)
        result["location"]["width"] = int(float(result["location"]["width"])/float_ratio)
        result["location"]["height"] = int(float(result["location"]["height"])/float_ratio)
        # 对ocr效果进行调整 
        # chenyj test 
        if len(result["words"]) >= 2 and (result["words"][-1] in ['l', 'j', '1']):
            result["words"] = result["words"][:-1] + 'i'
        result["words"] = result["words"].replace("（", "(")
    
    TIME_END()
    return APP_RET_CODE_SUCESS, json_return 

