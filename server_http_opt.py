# -*- coding: utf-8 -*-
from memory_profiler_helper import DEBUG_CURREN_MEM
DEBUG_CURREN_MEM("server_http_opt.py 刚开始")
from requests import post, get
# 服务器证书已过期，所有请求 verify=False，屏蔽告警刷屏
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass
DEBUG_CURREN_MEM("server_http_opt.py 加载requests")
import json
from datetime import datetime
import platform
import wmi
import os
import copy
import winreg
DEBUG_CURREN_MEM("server_http_opt.py 加载json、datetime、os")
from error_code import *
DEBUG_CURREN_MEM("server_http_opt.py 加载error_code")
from app_info import * 
DEBUG_CURREN_MEM("server_http_opt.py 加载app_info")

TIME_OUT = 8
URL_OF_REPORT_CLIENT = "{}://{}:{}/cyj/reportclient".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
URL_OF_GET_CONFIG = "{}://{}:{}/cyj/config".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
# 上报日志
URL_OF_LOG = "{}://{}:{}/cyj/log".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
TIME_OUT_OF_LOG = 1.6
# 上传图片
URL_OF_UPLOAD = "{}://{}:{}/cyj/upload".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
TIME_OUT_OF_UPLOAD = 3
# 登录信息
URL_OF_LOGIN = "{}://{}:{}/cyj/login".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
TIME_OUT_OF_LOGIN = 1.6
# 付款信息
URL_OF_PAYMENT = "{}://{}:{}/cyj/payment".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
TIME_OUT_OF_PAYMENT = 1.6
# 订单信息
URL_OF_TRADE = "{}://{}:{}/cyj/trade".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
TIME_OUT_OF_TRADE = 1.6
# 授权信息
URL_OF_LICENCE = "{}://{}:{}/cyj/licence".format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT)
TIME_OUT_OF_LICENCE = 1.6

# 全局变量
g_str_mac_for_server = ""
g_client_name = ""
g_b_Inited = False
g_get_screen_func = None

def http_is_Inited():
    global g_b_Inited
    
    return g_b_Inited
    
def get_current_time():
    now = datetime.now()
    time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    return time_str

# 获取操作系统类型
g_os_version  = ""
def get_os_version():
    os_name = platform.system()  # 获取操作系统名称
    os_version = platform.version()  # 获取操作系统的详细版本信息
    os_release = platform.release()  # 获取操作系统的版本号（如10）
    os_version = "{}_{}_{}".format(os_name, os_release, os_version)
    return os_version

# 获取CPU类型
g_cpu_version = ""
def get_cpu_version():
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        return cpu.Name

# 获取系统的版本
g_edition = ""
def get_windows_edition():
    try:
        # 打开注册表路径
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        # 读取 EditionID
        edition, _ = winreg.QueryValueEx(key, "EditionID")
        winreg.CloseKey(key)
        return edition
    except Exception as e:
        return str(e)
    return ""
# test
"""
edition = get_windows_edition()
print("Windows Edition:", edition)
if edition.upper() == "ENTERPRISE":
    print("这是 Windows 10 企业版")
elif edition.upper() == "PROFESSIONAL":
    print("这是 Windows 10 专业版")
else:
    print("未识别版本：", edition)
"""
    
# 报告客户端信息
def http_report_client_info(str_mac, client_name, config_json_data):
    global g_str_mac_for_server
    global g_client_name
    global g_os_version
    global g_cpu_version
    global g_edition
    
    try:
        print(f"Mac地址: {str_mac}")
        g_edition = get_windows_edition()
        print(f"操作系统版本: {g_edition}") 
        g_os_version = get_os_version()
        print(f"操作系统类型: {g_os_version}")
        g_os_version = g_os_version + "_" + g_edition
        g_cpu_version = get_cpu_version()
        print(f"CPU类型: {g_cpu_version}")

        # 把 FRIEND_INFO_LIST 从config_json_data里去掉，不然数据太多了
        config_json_data_copy = copy.deepcopy(config_json_data)
        if "FRIEND_INFO_LIST" in config_json_data_copy:
            del config_json_data_copy["FRIEND_INFO_LIST"]
        if "username_of_can_deposit_list" in config_json_data_copy:
            del config_json_data_copy["username_of_can_deposit_list"]
            
            
        data = {'str_mac': str_mac, 'os_version':g_os_version, 'cpu_version':g_cpu_version, 'client_name':client_name, 'time_str':get_current_time(), 'local_config_data':config_json_data_copy}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        # chenyj debug
        # print("上报的数据是:【{}】".format(json_data))
        response = post(URL_OF_REPORT_CLIENT, data=json_data, headers=headers, timeout=TIME_OUT, verify=False)
        response_json = json.loads(response.text, strict = False)
        iRet = response_json["code"]
        if iRet != 0:
            print("!!!!!1报告客户端信息失败:{}".format(response_json))
            return APP_RET_CODE_SERVER_ERRE 
    except Exception as e:
        print("!!!!2报告客户端信息失败\n{}".format(e))
        return APP_RET_CODE_NET_ERROR
        
    g_str_mac_for_server = str_mac
    g_client_name = client_name   
    # chenyj debug
    print("http报告客户端信息成功")
    
    return APP_RET_CODE_SUCESS

# 获取配置
def http_get_config():
    global g_str_mac_for_server
    global g_client_name
    global g_b_Inited
    
    config_return = {}
    
    if len(g_str_mac_for_server) == 0 or len(g_client_name) == 0:
        return False
        
    try:
        data = {'str_mac': g_str_mac_for_server, 'client_name':g_client_name, 'time_str':get_current_time()}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = get(URL_OF_GET_CONFIG, data=json_data, headers=headers, timeout=TIME_OUT, verify=False)
        response_json = json.loads(response.text, strict = False)
        if response_json["code"] != 0:
            print("!!!!!获取配置失败:{}".format(response_json))
            return False, config_return 
        if "body" in response_json:
            config_return = json.loads(response_json["body"])
    except Exception as e:
        print("!!!!获取配置失败\n{}".format(e))
        return False, config_return
        
    g_b_Inited = True
    print("http获取配置成功:【{}】".format(config_return))
    
    return True, config_return

# http初始化
def http_init(str_mac, client_name, config_json_data, get_screen_func):
    global g_get_screen_func
    
    config_return = {}
    
    iRet = http_report_client_info(str_mac, client_name, config_json_data)
    if iRet != 0:
        return iRet, config_return
    
    iRet, config_return = http_get_config()
    if False == iRet:
        return -1, config_return
    
    g_get_screen_func = get_screen_func
    return 0, config_return
    
# 上报日志
g_text_of_log = ""
def http_report_log(text):
    global g_text_of_log
    
    # 入参检查
    if g_b_Inited == False:
        return APP_RET_CODE_NO_READY 
    if len(text) <= 0:
        return APP_RET_CODE_UNVALID_PARAM

    # 防止重复上报
    if g_text_of_log == text:
        return APP_RET_CODE_SUCESS
    g_text_of_log = text 
    
    # 上报日志服务器
    try:
        data = {'str_mac': g_str_mac_for_server, 'client_name':g_client_name, 'time_str':get_current_time(), 'log_text': text}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = post(URL_OF_LOG, data=json_data, headers=headers, timeout=TIME_OUT_OF_LOG, verify=False)
        response_json = json.loads(response.text, strict = False)
        if response_json["code"] != 0:
            print("!!!!!1服务器日志服务访问失败:{}".format(response_json))
            return APP_RET_CODE_SERVER_ERRE 
    except Exception as e:
        print("!!!!2服务器日志服务访问失败\n{}".format(e))
        # chenyj 服务器访问失败也认为正常
        #return APP_RET_CODE_NET_ERROR
        return APP_RET_CODE_SUCESS
    return APP_RET_CODE_SUCESS
   
# 上传文件        
def http_upload_file(path, path_save):
    if False == os.path.exists(path):
        print("要上传的文件{}不存在".format(path))
        return False
        
    with open(path, 'rb') as f:
        try:
            #files = {'file': (os.path.basename(path), f)}
            files = {'file': (path_save, f)}
            # 发送POST请求上传文件
            response = post(URL_OF_UPLOAD, files=files, verify=False)
            response_json = json.loads(response.text, strict = False)
            if response_json["code"] != 0:
                print("!!!!!上传文件失败:{}".format(response_json))
                return False 
        except Exception as e:
            print("!!!!上传文件失败\n{}".format(e))
            return False
    # chenyj debug
    print("文件【{}】up sucess".format(path))
    return True
"""
str_mac = "04:ed:33:14:24:41"
http_upload_file("./screenshot_img/before.PNG", "./{}/{}/before.PNG".format(CLIENT_NAME, str_mac))    
"""   

# 上传当前雷电模拟器的截图
def upload_snape(upload_img_path = ""):
    global g_get_screen_func
    
    if g_get_screen_func is None:
        print("!!!!upload_snape, 函数还没准备好")
        http_report_log("!!!!upload_snape, 函数还没准备好")
        return APP_RET_CODE_NO_READY
    if len(upload_img_path) == 0:
        upload_img_path = SCREENSHOT_SAVE_DIR + "/" + "screen" + ".png"
        iRet = g_get_screen_func(upload_img_path)
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!!upload_snape, 托管器还没准备好")
            http_report_log("!!!!upload_snape, 托管器还没准备好")
            return iRet
    file_name = os.path.basename(upload_img_path)    
    http_upload_file(upload_img_path, "./{}/{}/{}".format(CLIENT_NAME, g_str_mac_for_server, file_name)) 
    return APP_RET_CODE_SUCESS

# 上报登录状态
def http_report_login_status(bind_phone = ""):
    global g_b_Inited
    # 入参检查
    if g_b_Inited == False:
        return APP_RET_CODE_NO_READY 
    
    # 上报服务器
    try:
        data = {'str_mac': g_str_mac_for_server, 'client_name':g_client_name, 'time_str':get_current_time(), 'bind_phone': bind_phone}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = post(URL_OF_LOGIN, data=json_data, headers=headers, timeout=TIME_OUT_OF_LOGIN, verify=False)
        response_json = json.loads(response.text, strict = False)
        if response_json["code"] != 0:
            print("!!!!!1上报登录状态失败:{}".format(response_json))
            return APP_RET_CODE_SERVER_ERRE 
    except Exception as e:
        print("!!!!2上报登录状态失败\n{}".format(e))
        # chenyj 服务器访问失败也认为正常
        #return APP_RET_CODE_NET_ERROR
        return APP_RET_CODE_SUCESS
    return APP_RET_CODE_SUCESS

# 获取购买记录
def http_get_payment(phone=""):
    global g_b_Inited

    payments_return = []
    # 入参检查
    if g_b_Inited == False:
        return APP_RET_CODE_NO_READY, payments_return
    if len(phone) <= 0:
        return APP_RET_CODE_UNVALID_PARAM, payments_return
        
    try:
        data = {'str_mac': g_str_mac_for_server, 'phone': phone}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = get(URL_OF_PAYMENT, data=json_data, headers=headers, timeout=TIME_OUT_OF_PAYMENT, verify=False) 
        response_json = json.loads(response.text, strict = False)
        print(f"==============={response_json}===================")
        if response_json["code"] != 0:
            print("!!!!!获取购买记录失败:{}".format(response_json))
            return False, payments_return
        if "body" in response_json:
            payments_return = json.loads(response_json["body"])
    except Exception as e:
        print("!!!!获取购买记录失败\n{}".format(e))
        return False, payments_return
        
    print("http获取购买记录成功:【{}】".format(payments_return))
    
    return True, payments_return

# 获取订单信息
def http_get_trade(phone="", str_subject = "", str_total_amount = ""):
    global g_b_Inited

    trade_return = {}
    # 入参检查
    if g_b_Inited == False:
        return APP_RET_CODE_NO_READY, trade_return
    if len(phone) <= 0 or len(str_subject) <= 0 or len(str_total_amount) <= 0:
        return APP_RET_CODE_UNVALID_PARAM, trade_return
        
    try:
        data = {'str_mac': g_str_mac_for_server, 'phone': phone, 'str_subject': str_subject, 'str_total_amount': str_total_amount}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = get(URL_OF_TRADE, data=json_data, headers=headers, timeout=TIME_OUT_OF_TRADE, verify=False)
        response_json = json.loads(response.text, strict = False)
        print(f"==============={response_json}===================")
        if response_json["code"] != 0:
            print("!!!!!获取订单信息失败:{}".format(response_json))
            return False, trade_return
        if "body" in response_json:
            trade_return = json.loads(response_json["body"])
    except Exception as e:
        print("!!!!获取订单信息失败\n{}".format(e))
        return False, trade_return
        
    print("http获取订单信息成功:【{}】".format(trade_return))
    
    return True, trade_return
# chenyj test
"""
g_str_mac_for_server = "345345346546757657"
g_b_Inited = True
http_get_trade("15280006510", "10天会员", "0.01")
"""

# 获取授权信息
def http_get_licence(phone=""):
    global g_b_Inited

    licences_return = []
    # 入参检查
    if g_b_Inited == False:
        return APP_RET_CODE_NO_READY, payments_licences_returneturn
    if len(phone) <= 0:
        return APP_RET_CODE_UNVALID_PARAM, licences_return
        
    try:
        data = {'str_mac': g_str_mac_for_server, 'phone': phone}
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = get(URL_OF_LICENCE, data=json_data, headers=headers, timeout=TIME_OUT_OF_PAYMENT, verify=False) 
        response_json = json.loads(response.text, strict = False)
        print(f"==============={response_json}===================")
        if response_json["code"] != 0:
            print("!!!!!获取授权记录失败:{}".format(response_json))
            return False, licences_return
        if "body" in response_json:
            licences_return = json.loads(response_json["body"])
    except Exception as e:
        print("!!!!获取授权记录失败\n{}".format(e))
        return False, licences_return
        
    print("http获取授权记录成功:【{}】".format(licences_return))
    
    return True, licences_return
# chenyj test
"""
g_str_mac_for_server = "345345346546757657"
g_b_Inited = True
http_get_licence("15280006510")
"""