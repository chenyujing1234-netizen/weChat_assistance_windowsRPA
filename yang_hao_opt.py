# -*- coding: utf-8 -*-

import subprocess
import time
import pyautogui
import win32gui
import win32con
from random import randint
import threading
import sys
import os
import test_baidu_ocr  
from PIL import Image
from enum import Enum
import shutil 
from threading import Event
import re
import traceback
from datetime import datetime, timedelta  
from dateutil import parser 
import dateutil.relativedelta  
import json
import copy
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
from cv2 import imread
from log_helper import print_my
from app_info import *
from server_http_opt import *
from image_helper import image_init, image_check_begin, image_check_end, wait_image_change, image_is_white, image_is_gray, image_is_blue, image_is_black, calculate_red_area_ratio, calculate_green_area_ratio, has_img_change
from error_code import *
from agent_helper import agent_get_result
from llm_helper import llm_get_result_for_local_rag, llm_get_result_for_local_rag_for_chat, llm_get_result_from_kimi
from coze_helper import llm_get_result_for_coze_for_chat, BOT_ID_OF_IMAGE_GEN_AGENT, API_TOKEN_OF_IMAGE_GEN_AGENT, COZE_FRON_STR
from character_helper import llm_get_result_from_character
from test_my_ocr import get_ocr_result_with_small_my
from time_helper import TIME_BEGIN, TIME_END
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    from yang_hao_opt_helper_of_windows import *
# 导入坐标配置模块
from location_config import g_location_config

# 使用配置文件中的屏幕尺寸
if g_location_config:
    W_SCREEN = g_location_config.W_SCREEN
    H_SCREEN = g_location_config.H_SCREEN

g_w_screen = W_SCREEN
g_h_screen = H_SCREEN
W_SCREEN_heng = H_SCREEN
H_SCREEN_heng = W_SCREEN

# 从配置文件读取好友列表坐标
if g_location_config:
    FRIEND_CHAT_LIST_LT_X = g_location_config.FRIEND_CHAT_LIST_LT_X
    FRIEND_CHAT_LIST_LT_Y = g_location_config.FRIEND_CHAT_LIST_LT_Y
    
g_friend_chat_list_x = FRIEND_CHAT_LIST_LT_X
g_friend_chat_list_y = FRIEND_CHAT_LIST_LT_Y

# 从配置文件读取聊天窗口坐标
if g_location_config:
    CHAT_LT_X = g_location_config.CHAT_LT_X
    CHAT_LT_Y = g_location_config.CHAT_LT_Y
        
    g_chat_x = CHAT_LT_X
    g_chat_y = CHAT_LT_Y
    
CHAT_HALF_X = 335
g_chat_half_x = CHAT_HALF_X
CHAT_TIME_LT_X = 293
CHAT_TIME_RB_X = 375
g_chat_time_lt_x = CHAT_TIME_LT_X
g_chat_time_rb_x = CHAT_TIME_RB_X

# 从配置文件读取聊天行高相关配置
if g_location_config:
    CHAT_LINE_HEIGHT = g_location_config.CHAT_LINE_HEIGHT
    CHAT_LINE_HEIGHT_INTER = g_location_config.CHAT_LINE_HEIGHT_INTER
    CHAT_MIN_Y_FOR_OCR = g_location_config.CHAT_MIN_Y_FOR_OCR
    CHAT_MAX_Y_FOR_OCR = g_location_config.CHAT_MAX_Y_FOR_OCR

    g_chat_line_height = CHAT_LINE_HEIGHT
    g_chat_line_height_inter = CHAT_LINE_HEIGHT_INTER
g_chat_min_y_for_ocr = CHAT_MIN_Y_FOR_OCR
g_chat_max_y_for_ocr = CHAT_MAX_Y_FOR_OCR

CHAT_LINE_WIDTH_INTER = 15
g_chat_line_width_inter = CHAT_LINE_WIDTH_INTER

# 从配置文件读取聊天文本边界相关配置
if g_location_config:
    CHAT_LT_X_SHOULD_MIN = g_location_config.CHAT_LT_X_SHOULD_MIN
    CHAT_LT_X_SHOULD_MIN_INTER = g_location_config.CHAT_LT_X_SHOULD_MIN_INTER
    CHAT_RB_X_SHOULD_MIN = g_location_config.CHAT_RB_X_SHOULD_MIN
    CHAT_RB_X_SHOULD_MIN_INTER = g_location_config.CHAT_RB_X_SHOULD_MIN_INTER

    g_chat_lt_x_should_min = CHAT_LT_X_SHOULD_MIN
    g_chat_lt_x_should_min_inter = CHAT_LT_X_SHOULD_MIN_INTER
    g_chat_rb_x_should_min = CHAT_RB_X_SHOULD_MIN
    g_chat_rb_x_should_min_inter = CHAT_RB_X_SHOULD_MIN_INTER

# 群聊天时发送username应该的lt_x
SENDER_LT_X_SHOULD_MIN = 90
g_sender_lt_x_should_min = SENDER_LT_X_SHOULD_MIN
SENDER_LT_X_SHOULD_MIN_INTER = 5
g_sender_lt_x_should_min_inter = SENDER_LT_X_SHOULD_MIN_INTER

# 从配置文件读取好友资料页昵称坐标
if g_location_config:
    g_rb_x_of_nickname_of_new_friend_information_page = g_location_config.NICKNAME_RB_X
    g_rb_y_of_nickname_of_new_friend_information_page = g_location_config.NICKNAME_RB_Y
    
# 从配置文件读取权限申请页面取消按钮位置
if g_location_config:
    QUXIAN_CANCEL_LT_X = g_location_config.QUXIAN_CANCEL_LT_X
    QUXIAN_CANCEL_LT_Y = g_location_config.QUXIAN_CANCEL_LT_Y


g_quxian_cancel_x = QUXIAN_CANCEL_LT_X
g_quxian_cancel_y = QUXIAN_CANCEL_LT_Y
# “权限申请保持后台页面”取消按钮位置 
g_quxian_kee_back_cancel_x = 418
g_quxian_kee_back_cancel_y = 1117
# “账号在其他设备上登录”取消按钮位置
g_has_login_in_other_cancel_x = 962
g_has_login_in_other_cancel_y = 708
# ”提示：由于对方的隐私设置"页面确定按钮位置
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    g_msg_because_privacy_x = 536
    g_msg_because_privacy_y = 1099
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    g_msg_because_privacy_x = 546
    g_msg_because_privacy_y = 1381
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    g_msg_because_privacy_x = 546
    g_msg_because_privacy_y = 1381
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    g_msg_because_privacy_x = 546
    g_msg_because_privacy_y = 1381
    
# ”小程序入口提示"页面关闭按钮位置
g_msg_small_program_x = 413
g_msg_small_program_y = 1198

# “登录设备选择页”取消按钮位置
DEVICE_TYPE_CANCEL_LT_X = 416
DEVICE_TYPE_CANCEL_LT_Y = 591
g_device_type_cancel_x = DEVICE_TYPE_CANCEL_LT_X
g_device_type_cancel_y = DEVICE_TYPE_CANCEL_LT_Y
g_device_type_cancel_x_2 = 335
g_device_type_cancel_y_2 = 589
# “登录注册页”取消按钮位置
LOGIN_REG_CANCEL_LT_X = 284
LOGIN_REG_CANCEL_LT_Y = 1795
g_login_reg_cancel_x = LOGIN_REG_CANCEL_LT_X
g_login_reg_cancel_y = LOGIN_REG_CANCEL_LT_Y
# “进入微信页”取消按钮位置
ENTER_WECHAT_LT_X = 513
ENTER_WECHAT_LT_Y = 496
g_enter_wechat_cancel_x = ENTER_WECHAT_LT_X
g_enter_wechat_cancel_y = ENTER_WECHAT_LT_Y
# “微信可设置字体大小页”取消按钮位置
SETTING_FONT_CANCEL_LT_X = 421
SETTING_FONT_CANCEL_LT_Y = 1074
g_setting_font_cancel_x = SETTING_FONT_CANCEL_LT_X
g_setting_font_cancel_y = SETTING_FONT_CANCEL_LT_Y
# “本次登录已失效页”取消按钮位置
LOGIN_LOSS_CANCEL_LT_X = 961
LOGIN_LOSS_CANCEL_LT_Y = 649
g_login_loss_cancel_x = LOGIN_LOSS_CANCEL_LT_X
g_login_loss_cancel_y = LOGIN_LOSS_CANCEL_LT_Y
LOGIN_LOSS_CANCEL_LT_X_2 = 538
LOGIN_LOSS_CANCEL_LT_Y_2 = 1063
g_login_loss_cancel_x_2 = LOGIN_LOSS_CANCEL_LT_X_2
g_login_loss_cancel_y_2 = LOGIN_LOSS_CANCEL_LT_Y_2
# “切换验证方式页”取消按钮位置
CHANGE_LOGIN_CANCEL_LT_X = 972
CHANGE_LOGIN_CANCEL_LT_Y = 878
g_change_login_cancel_x = CHANGE_LOGIN_CANCEL_LT_X
g_change_login_cancel_y = CHANGE_LOGIN_CANCEL_LT_Y
g_change_login_cancel_x_2 = 963
g_change_login_cancel_y_2 = 878
# “切换验证方式作为平板页” “作为平板”按钮位置
g_change_login_pad_x = 535
g_change_login_pad_y = 774
# “允许微信录音吗页”取消按钮位置
#    横屏
CAN_AUDIO_CANCEL_LT_X_heng = 979
CAN_AUDIO_CANCEL_LT_Y_heng = 646
g_can_audio_cancel_x_heng = CAN_AUDIO_CANCEL_LT_X_heng
g_can_audio_cancel_y_heng = CAN_AUDIO_CANCEL_LT_Y_heng
CAN_AUDIO_CANCEL_LT_X_heng_2 = 1047
CAN_AUDIO_CANCEL_LT_Y_heng_2 = 608
g_can_audio_cancel_x_heng_2 = CAN_AUDIO_CANCEL_LT_X_heng_2
g_can_audio_cancel_y_heng_2 = CAN_AUDIO_CANCEL_LT_Y_heng_2
#    竖屏
CAN_AUDIO_CANCEL_LT_X = 558
CAN_AUDIO_CANCEL_LT_Y = 1066
g_can_audio_cancel_x = CAN_AUDIO_CANCEL_LT_X
g_can_audio_cancel_y = CAN_AUDIO_CANCEL_LT_Y
g_can_audio_cancel_x_2 = 627
g_can_audio_cancel_y_2 = 1028
# “允许微信拍摄照片和录制视频页”取消按钮位置
#    横屏
CAN_IMAGE_CANCEL_LT_X_heng = 1105
CAN_IMAGE_CANCEL_LT_Y_heng = 607
g_can_image_cancel_x_heng = CAN_IMAGE_CANCEL_LT_X_heng
g_can_image_cancel_y_heng = CAN_IMAGE_CANCEL_LT_Y_heng
#    竖屏
CAN_IMAGE_CANCEL_LT_X = 558
CAN_IMAGE_CANCEL_LT_Y = 1066
g_can_image_cancel_x = CAN_IMAGE_CANCEL_LT_X
g_can_image_cancel_y = CAN_IMAGE_CANCEL_LT_Y
CAN_IMAGE_CANCEL_LT_X_2 = 688
CAN_IMAGE_CANCEL_LT_Y_2 = 1026
g_can_image_cancel_x_2 = CAN_IMAGE_CANCEL_LT_X_2
g_can_image_cancel_y_2 = CAN_IMAGE_CANCEL_LT_Y_2
# “当前账号已经在其他设备登录页”取消按钮位置
#HAS_LOGIN_CANCEL_LT_X = 963
#HAS_LOGIN_CANCEL_LT_Y = 668
HAS_LOGIN_CANCEL_LT_X = 540
HAS_LOGIN_CANCEL_LT_Y = 1100
g_has_login_cancel_x = HAS_LOGIN_CANCEL_LT_X
g_has_login_cancel_y = HAS_LOGIN_CANCEL_LT_Y
# “当前账号已经在其他设备登录页”确定按钮位置
HAS_LOGIN_CONFIRM_LT_X = 544
HAS_LOGIN_CONFIRM_LT_Y = 1133
HAS_LOGIN_CONFIRM_LT_X_2 = 955
HAS_LOGIN_CONFIRM_LT_Y_2 = 710
g_has_login_confirm_x = HAS_LOGIN_CONFIRM_LT_X
g_has_login_confirm_y = HAS_LOGIN_CONFIRM_LT_Y
g_has_login_confirm_x_2 = HAS_LOGIN_CONFIRM_LT_X_2
g_has_login_confirm_y_2 = HAS_LOGIN_CONFIRM_LT_Y_2
# “登录过期请重新登录页”确定按钮位置
RE_LOGIN_CANCEL_LT_X = 538
RE_LOGIN_CANCEL_LT_Y = 1072
g_re_login_cancel_x = RE_LOGIN_CANCEL_LT_X
g_re_login_cancel_y = RE_LOGIN_CANCEL_LT_Y
# “为了你的安全请重新登录页”确定按钮位置
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    SAFE_RE_LOGIN_CANCEL_LT_X = 538
    SAFE_RE_LOGIN_CANCEL_LT_Y = 1049
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    SAFE_RE_LOGIN_CANCEL_LT_X = 538
    SAFE_RE_LOGIN_CANCEL_LT_Y = 1049
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    SAFE_RE_LOGIN_CANCEL_LT_X = 358
    SAFE_RE_LOGIN_CANCEL_LT_Y = 700
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    SAFE_RE_LOGIN_CANCEL_LT_X = 538
    SAFE_RE_LOGIN_CANCEL_LT_Y = 1049

g_safe_re_login_cancel_x = SAFE_RE_LOGIN_CANCEL_LT_X
g_safe_re_login_cancel_y = SAFE_RE_LOGIN_CANCEL_LT_Y
# “密码登录页”取消按钮位置
SECRET_LOGIN_CANCEL_LT_X = 554
SECRET_LOGIN_CANCEL_LT_Y = 778
g_secret_login_cancel_x = SECRET_LOGIN_CANCEL_LT_X
g_secret_login_cancel_y = SECRET_LOGIN_CANCEL_LT_Y
g_secret_login_cancel_x_2 = 554
g_secret_login_cancel_y_2 = 725
# “登录出现错误,请你重新登录页面”确定按钮位置
ERROR_LOGIN_CANCEL_LT_X = 541
ERROR_LOGIN_CANCEL_LT_Y = 1052
g_error_login_cancel_x = ERROR_LOGIN_CANCEL_LT_X
g_error_login_cancel_y = ERROR_LOGIN_CANCEL_LT_Y
# “微信屦次停止运行页面”确定按钮位置
ERROR_STOP_CANCEL_LT_X = 330
ERROR_STOP_CANCEL_LT_Y = 1069
g_error_stop_cancel_x = ERROR_STOP_CANCEL_LT_X
g_error_stop_cancel_y = ERROR_STOP_CANCEL_LT_Y
g_error_stop_cancel_x_2 = 661
g_error_stop_cancel_y_2 = 651
# “微信没有响应页面”确定按钮位置
ERROR_NO_RESPONSE_CANCEL_LT_X = 656
ERROR_NO_RESPONSE_CANCEL_LT_Y = 569
g_error_no_response_cancel_x = ERROR_NO_RESPONSE_CANCEL_LT_X
g_error_no_response_cancel_y = ERROR_NO_RESPONSE_CANCEL_LT_Y
ERROR_NO_RESPONSE_CANCEL_LT_X_2 = 297
ERROR_NO_RESPONSE_CANCEL_LT_Y_2 = 980
g_error_no_response_cancel_x_2 = ERROR_NO_RESPONSE_CANCEL_LT_X_2
g_error_no_response_cancel_y_2 = ERROR_NO_RESPONSE_CANCEL_LT_Y_2
# “系统界面没有响应”关闭按钮
g_system_ui_no_response_cancel_x = 328
g_system_ui_no_response_cancel_y = 984
g_system_ui_no_response_cancel_x_2 = 658
g_system_ui_no_response_cancel_y_2 = 561
# “初始使用朋友圈发送文本提醒页面”确定按钮位置
ERROR_NO_RESPONSE_CIRCLE_TEXT_I_KNOW_X = 534
ERROR_NO_RESPONSE_CIRCLE_TEXT_I_KNOW_Y = 1820
g_circle_text_i_know_x = ERROR_NO_RESPONSE_CIRCLE_TEXT_I_KNOW_X
g_circle_text_i_know_y = ERROR_NO_RESPONSE_CIRCLE_TEXT_I_KNOW_Y
# “微信申请访问照片权限页面”确定按钮位置
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    WEI_XIN_APPLY_VISIT_AMBLE_X = 938
    WEI_XIN_APPLY_VISIT_AMBLE_Y = 1049
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    WEI_XIN_APPLY_VISIT_AMBLE_X = 535
    WEI_XIN_APPLY_VISIT_AMBLE_Y = 1975 
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    WEI_XIN_APPLY_VISIT_AMBLE_X = 535
    WEI_XIN_APPLY_VISIT_AMBLE_Y = 1975 
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    WEI_XIN_APPLY_VISIT_AMBLE_X = 535
    WEI_XIN_APPLY_VISIT_AMBLE_Y = 1975 
    
g_wei_xin_apply_visit_amble_x = WEI_XIN_APPLY_VISIT_AMBLE_X
g_wei_xin_apply_visit_amble_y = WEI_XIN_APPLY_VISIT_AMBLE_Y 
# “保留此次编辑”确定按钮位置
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    KEEP_EDIT_X = 938  # 还未确定
    KEEP_EDIT_Y = 1049 # 还未确定
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    KEEP_EDIT_X = 318
    KEEP_EDIT_Y = 1306 
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    KEEP_EDIT_X = 318
    KEEP_EDIT_Y = 1306 
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    KEEP_EDIT_X = 318
    KEEP_EDIT_Y = 1306 

g_keep_edit_x = KEEP_EDIT_X
g_keep_edit_y = KEEP_EDIT_Y 
# “麦克风权限未开启”我知道了按钮位置
MIC_AUTHORITY_NO_OPEN_X = 414
MIC_AUTHORITY_NO_OPEN_Y = 1113
g_mic_authority_no_open_x = MIC_AUTHORITY_NO_OPEN_X
g_mic_authority_no_open_y = MIC_AUTHORITY_NO_OPEN_Y 
# “你已退出微信”确定按钮位置
g_you_has_logout_wechat_x = 960
g_you_has_logout_wechat_y = 627
g_you_has_logout_wechat_x_2 = 538
g_you_has_logout_wechat_y_2 = 1044

# 消息内容向下滚动到底的最大次数
MAX_SLIDE_DOWN_COUNT = 12
# 消息内容向上滚动到顶的最大次数
MAX_SLIDE_UP_COUNT = 1

# 通讯录向上滚动到底的最大次数
MAX_SLIDE_DOWN_COUNT_FRIENDBOOK = 60
# 通讯录向上滚动到顶的最大次数(约每页20个好友)
#MAX_SLIDE_UP_COUNT_FRIENDBOOK = 60 # 对应最多1200个好友
#MAX_SLIDE_UP_COUNT_FRIENDBOOK = 480 # 对应最多8000个好友
MAX_SLIDE_UP_COUNT_FRIENDBOOK = 600 # 对应最多8000个好友
MAX_SLIDE_DOWN_COUNT_FRIENDBOOK = 600 # 对应最多8000个好友
# 标签页标签的最多个数
MAX_LOOP_COUNT_OF_TAG = 16

PACKAGE_NAME = 'com.tencent.mm'
MAIN_ACTIVAT_NAME = '.ui.LauncherUI'

# 判断是否是业务内容的关键字
BUSINESS_MESSAGE_LIST = ["忙线未接听", "忙线未接听", "已取消", "已在其它设备接听", "已取消", "转文字", "对方已拒绝", "撤回了一条消息", "通话中断", "置顶了一条消息", "未应答", "通话时长", "对方无应答", "我通过了你的朋友验证请求", "微信电脑版"]
# 触发发现新消息的红色像素占监控区域的比例
#NEW_MSG_RATIO = 0.25
NEW_MSG_RATIO = 0.05

# 触发发现新加好友的红色像素占监控区域的比例
NEW_PASS_RATIO = 0.05

# 判断通讯录是否是业务内容的关键字
BUSINESS_FRIENDBOOK_LIST = ["微信团队", "文件传输助手", "1个朋友", "新的朋友", "仅聊天的朋友", "群聊", "标签", "公众号", "我的企业及企业联系人", "及企业联系人", "企业微信联系人", "星标朋友", "搜索", "叟索"]
#

g_object_info_of_can_deposit_dict = {}
g_monitor_object_info_dict = {}  
g_message_dict = {}

g_Event_test = Event()  
g_Event_test.clear()
g_i_chat_count = 0
g_i_crop_count = 0
g_i_friendbook_count = 0
g_table = None
###############################测试##########################
# 修改分辨率
#cmd='"./LDPlayer9/adb.exe" "shell" "wm size 720x1280"'
#subprocess.run(cmd) 
#time.sleep(1)

DEVICE_CMD = ""
g_process_creationflags = subprocess.CREATE_NO_WINDOW
# 获得雷电设备
def adb_is_lei_dian_device_ready(table):
    global DEVICE_CMD
    global g_table
    
    device_name_list = []
    
    g_table = table
    # 先发一次截屏
    path = SCREENSHOT_SAVE_DIR + "/" + "example" + ".png"
    adb_get_screen(path)

    temp_path = "./adb_device.txt"
    with open(temp_path,"wb") as out:
        cmd = LEI_DIAN_DIR + "/adb.exe devices"
        subprocess.run(cmd, stdout = out, creationflags=g_process_creationflags)
        time.sleep(0.1)
        
    with open(temp_path, "r") as f:
        lines = f.readlines()
        #print_my(lines)
        #if len(lines) <= 2:
        #    return False
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if "offline" in line or "no devices" in line or "devices attached" in line:
                continue
            # 本地模拟器
            if "device" in line and "emulator-" in line :
                if len(line.split("\t")) < 2:
                    continue
                device_name = line.split("\t")[0]
                device_name = device_name.strip()
                device_name_list.append(device_name)
            # 无影云手机
            elif "device" in line and ":" in line:
                if len(line.split("\t")) < 2:
                    continue
                device_name = line.split("\t")[0]
                device_name = device_name.strip()
                device_name_list.append(device_name)
    
    if len(device_name_list) > 0:
        print_my(f"####找到模拟器设备共有{len(device_name_list)}个，分别是:{device_name_list}")
        device_name_selected = device_name_list[0]
        DEVICE_CMD = "-s {}".format(device_name_selected)
        print_my("####选中的模拟器设备是: {}".format(DEVICE_CMD))
        return True
    else:
        print_my("####没有找到模拟器设备")
        DEVICE_CMD = ""
    return False
    
    #List of devices attached
    #emulator-5554	device
    #120.26.204.112:100      unauthorized    # 无影云手机(未授权)
    #120.26.204.112:100      device    # 无影云手机(已授权)
#adb_is_lei_dian_device_ready(None)

# 判断本地的微信应用程序是否准备好
def is_windows_wechat_ready(table):
    global g_table

    g_table = table
    
    # 1. 判断微信应用程序是否安装 
    if False == is_wechat_installed():
        print("!!!!!is_windows_wechat_ready, 微信程序还未安装")
        return APP_RET_CODE_WECHAT_NO_INSTALL
    return APP_RET_CODE_SUCESS

def adb_start_server():
    """启动一次 adb server（若已启动则什么都不做）"""
    cmd = "{}/adb.exe start-server".format(LEI_DIAN_DIR)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    return
#adb_start_server()

def restart_adb_server():
    cmd = "{}/adb.exe kill-server".format(LEI_DIAN_DIR)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    cmd = "{}/adb.exe start-server".format(LEI_DIAN_DIR)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
#restart_adb_server()

# 匹配无线远程调试的手机（要求手机端停留在匹配的弹出界面）
# adb.exe pair 192.168.4.33:41471
def adb_pair_remote_phone(ip_str, port_str, pairing_code):
    iRet = APP_RET_CODE_UNKNOW
    
    print(f"开始匹配远程手机:{ip_str}:{port_str} 匹配码:{pairing_code}")
    cmd = LEI_DIAN_DIR + "/adb.exe pair {}:{}".format(ip_str, port_str)
    try:
        # 1. 引入常量
        CREATE_NO_WINDOW = 0x08000000
        # 2. 构造 startupinfo
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        # 启动子进程
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # 自动处理字符串而不是字节
            encoding="utf-8",        # 关键：显式用 UTF-8
            errors="replace",        # 解码失败时用占位符，不抛异常
            bufsize=1,   # 行缓冲
            creationflags=CREATE_NO_WINDOW,   # 关键
            startupinfo=startupinfo           # 可选，但保险
        )
        
        # 读取直到看到提示符
        prompt = "Enter pairing code:"
        output = ""
        while prompt not in output:
            char = proc.stdout.read(1)
            if not char:
                break
            output += char
            print(char, end="")  # 实时回显
        print(f"匹配时第一步输出:{output}")
        # 输入配对码
        print(f"输入配对码:{pairing_code}")
        proc.stdin.write(pairing_code + "\n")
        proc.stdin.flush()

        # 读取剩余输出
        # 3. 继续按行读剩余输出
        for line in iter(proc.stdout.readline, ""):
            print(f"匹配时第二步输出:{line}")
            if "Failed" in line:
                print(f"匹配失败")
            elif "Successfully paired" in line:
                print("恭喜，匹配成功")
                iRet = APP_RET_CODE_SUCESS
        # 等待进程结束
        proc.wait()
    except Exception as e:
        print(f"匹配出现异常.{e}")
    
    return iRet
#adb_pair_remote_phone("192.168.210.161", "37615", "416961")

# 连接无线远程调试的手机 
# adb.exe connect 192.168.210.161:35153
def adb_connect_remote_phone(table, ip_str, port_str):
    global g_table
    
    iRet = APP_RET_CODE_UNKNOW
    
    g_table = table
    print(f"开始连接远程手机:{ip_str}:{port_str}")
    cmd = LEI_DIAN_DIR + "/adb.exe connect {}:{}".format(ip_str, port_str)
    try:
        # 1. 引入常量
        CREATE_NO_WINDOW = 0x08000000
        # 2. 构造 startupinfo
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        # 启动子进程
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=CREATE_NO_WINDOW,   # 关键
            startupinfo=startupinfo           # 可选，但保险
        )
        # 读取直到看到提示符
        prompt = "connected to"
        output = ""
        while prompt not in output:
            char = proc.stdout.read(1)
            if not char:
                break
            output += char
        print(f"连接时输出:{output}")
        if prompt in output and "cannot connect to" not in output:
            print("恭喜，连接成功")
            iRet = APP_RET_CODE_SUCESS
        # 等待进程结束
        proc.wait()
    except Exception as e:
        print(f"连接出现异常.{e}")

    return iRet
#adb_connect_remote_phone("192.168.210.161", "37073")

# 判断手机远程调式是否连通、是否点亮、是否解锁
def adb_is_remote_phone_ready(table):
    global g_table
    
    g_table = table
    if adb_get_phone_size() == False:
        return APP_RET_CODE_PHONE_NO_CONNECT
    iRet = is_screen_light()
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    iRet = is_screen_unlock()
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    return APP_RET_CODE_SUCESS

# 判断手机是否点亮
def is_screen_light():
    temp_path = "./adb_device_policy.txt"
    try:
        with open(temp_path,"wb") as out:
            cmd= LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell dumpsys window policy"
            subprocess.run(cmd, stdout = out, creationflags=g_process_creationflags)
            time.sleep(0.1)
        with open(temp_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "screenState=SCREEN_STATE_ON" in line:
                    #print_my("屏幕已点亮")
                    return APP_RET_CODE_SUCESS
    except Exception as e:
        print(f"is_screen_light异常:{e}")
        return APP_RET_CODE_PHONE_NO_CONNECT
    print("屏幕没有点亮")
    return APP_RET_CODE_PHONE_NO_LIGHT                       
# 使用示例
"""
if len(g_device_id_set) >= 1:
    device_serial = g_device_id_set[0]  # 替换为你的设备序列号
    is_screen_light = is_screen_light(device_serial)
    if is_screen_light == True:
        print_my("屏幕已点亮")
"""
 
# 判断手机是否锁定
def is_screen_unlock():
    temp_path = "./adb_device_policy.txt"
    try:
        with open(temp_path,"wb") as out:
            cmd= LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell dumpsys window policy"
            subprocess.run(cmd, stdout = out, creationflags=g_process_creationflags)
            time.sleep(0.1)
        with open(temp_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "showing=false" in line:
                    #print_my("屏幕已解锁")
                    return APP_RET_CODE_SUCESS   
    except Exception as e:
        print(f"is_screen_unlock异常:{e}")
        return APP_RET_CODE_PHONE_NO_CONNECT
    print("屏幕已锁定")
    return APP_RET_CODE_PHONE_NO_UNLOCK      

#截取模拟器中手机屏幕图，并保存到电脑指定文件夹中
g_lock_of_adb = threading.Lock()
def adb_get_screen(path, draw_bbox = None):
    global g_table
    
    iRet = APP_RET_CODE_SUCESS
    g_lock_of_adb.acquire()
    try:
        if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
            cmd= LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell screencap -p"
            temp_png = SCREENSHOT_SAVE_DIR + "/tmp.png"
            with open(temp_png, "wb") as out:
                subprocess.run(cmd,stdout=out, creationflags=g_process_creationflags)
            time.sleep(0.5)
            #adb 命令有时直接截图保存到电脑出错的解决办法-加下面一段即可
            with open(temp_png, "rb") as f:
                bys = f.read()
                bys_ = bys.replace(b"\r\n",b"\n")  # 二进制流中的"\r\n" 替换为"\n"

            with open(path, "wb") as f:
                f.write(bys_)
            if len(bys_) == 0:
                iRet = APP_RET_CODE_UNKNOW
        else:
            iRet = windows_get_screen(path)
    except Exception as e:
        print("adb_get_screen,发生异常:\n{}".format(e))
        iRet = APP_RET_CODE_UNKNOW
    finally:
        if iRet == APP_RET_CODE_SUCESS:
            if g_table is not None and g_b_Draw_snap == True:
                update_screen_img_info = {}
                update_screen_img_info["image_path"] = path
                if draw_bbox is None:
                    update_screen_img_info["draw_box"] = ""
                else:
                    update_screen_img_info["draw_box"] = draw_bbox
                update_screen_img_info_str = json.dumps(update_screen_img_info)
                g_table.signal_of_table.emit("update_screen_img_info_" + update_screen_img_info_str)
        g_lock_of_adb.release()
    
    return iRet
"""
path = SCREENSHOT_SAVE_DIR + "/" + "example_first" + ".png"
adb_get_screen(path)
time.sleep(1)
"""
 
#截取电脑屏幕中全屏图，并保存到电脑指定文件夹中
def adb_get_whole_screen(path, draw_bbox = None):
    global g_table
    
    iRet = APP_RET_CODE_SUCESS
    g_lock_of_adb.acquire()
    try:
        if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
            pass
        else:
            iRet = capture_screenshot_of_whole_screen(path)
    except Exception as e:
        print("adb_get_screen,发生异常:\n{}".format(e))
        iRet = APP_RET_CODE_UNKNOW
    finally:
        if iRet == APP_RET_CODE_SUCESS:
            if g_table is not None and g_b_Draw_snap == True:
                update_screen_img_info = {}
                update_screen_img_info["image_path"] = path
                if draw_bbox is None:
                    update_screen_img_info["draw_box"] = ""
                else:
                    update_screen_img_info["draw_box"] = draw_bbox
                update_screen_img_info_str = json.dumps(update_screen_img_info)
                g_table.signal_of_table.emit("update_screen_img_info_" + update_screen_img_info_str)
        g_lock_of_adb.release()
    
    return iRet
"""
path = SCREENSHOT_SAVE_DIR + "/" + "screen" + ".png"
adb_get_whole_screen(path)
time.sleep(1)
"""

# 将电脑端的图片传到手机端
def adb_send_image_to_phone(img_path):
    # adb push "C:\path\to\image.jpg" "/sdcard/DCIM/Camera/image.jpg"
    dst_img_path = "/sdcard/Pictures/4.png"
    cmd= "{}/adb.exe {} push \"{}\" \"{}\"".format(LEI_DIAN_DIR, DEVICE_CMD, img_path, dst_img_path)
    print("动作:【将电脑端的图片{}传到手机端】".format(img_path))
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    time.sleep(2) 
    return 
#img_path = "C:\\Users\\admin\\Desktop\\4.png"
#adb_send_image_to_phone(img_path)
 
#{
#"except_name":"正在载入数据页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LODING_DATA, "include_str_list":["正在载入", "微信", "数", "据"]
#},
EXCEPT_BOX_INFO_DICT_LIST = [
                        {
                            "except_name":"权限申请页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_AUTHORITY, "include_str_list":["权限申请", "取消", "去设置"]
                        },
                        {
                            "except_name":"权限申请保持后台页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_AUTHORITY_KEEY_BACK, "include_str_list":["权限申请", "在手机系统设置中", "允许微信保持后"]
                        },
                        {
                            "except_name":"权限申请保持后台页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_AUTHORITY_KEEY_BACK, "include_str_list":["允许微信保持后", "否则可能无法及时收到微信", "消息通知"]
                        },
                        {
                            "except_name":"权限申请保持后台页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_AUTHORITY_KEEY_BACK, "include_str_list":["权限申请", "在手机系统设置中", "消息通知", "取消"]
                        },
                        {
                           "except_name":"二维码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, "include_str_list":["请使用微信", "二维码登录"]
                        },
                        {
                           "except_name":"二维码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, "include_str_list":["二维码已过期", "二维码登录"]
                        },
                        {
                           "except_name":"二维码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, "include_str_list":["仅传输文件", "扫码登录"]
                        },
                        {
                           "except_name":"二维码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, "include_str_list":["团限招", "扫码登录"]
                        },
                        {
                           "except_name":"进入微信页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT, "include_str_list":["微信", "切换账号", "仅传输文件"]
                        },
                        {
                           "except_name":"进入微信页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT, "include_str_list":["信", "切", "账号", "仅传输文件"]
                        },
                        {
                           "except_name":"进入微信页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT, "include_str_list":["微信", "仅传输文件"], "max_character_count": 50
                        },
                        {
                           "except_name":"进入微信页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT, "include_str_list":["信", "切", "账", "仅传输文件"], "max_character_count": 50
                        },
                        {
                           "except_name":"进入微信页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT, "include_str_list":["信", "切", "号", "仅传输文件"], "max_character_count": 50
                        },
                        {
                           "except_name":"需在手机上完成登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_NEED_PHONE_LOGION, "include_str_list":["微信", "需在手机上完成登录", "取消"]
                        },
                        {
                           "except_name":"登录注册页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LOGION_REG, "include_str_list":["语言"], "exclude_str_list":["微信", "通讯录", "通话", "分钟", "前", "小时", "全文", "消息", "更换", "视频"]
                        },
                        {
                           "except_name":"登录注册页面", "except_code":
                           APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LOGION_REG, "include_str_list":["登录", "注册"]
                        },
                        {
                           "except_name":"使用设备类型设置页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_USE_DEVICE_TYPE, "include_str_list":["同时在手机和平板上使用", "仅在平板上使用"]
                        },
                        {
                           "except_name":"使用设备类型设置页面2", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_USE_DEVICE_TYPE2, "include_str_list":["作为平板使用", "作为手机使用"]
                        },
                        {
                           "except_name":"使用设备类型设置仅平板页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_USE_DEVICE_TYPE_ONLY_PAD, "include_str_list":["仅在平板上使用"], "exclude_str_list": ["同时", "手机和平板上"]
                        },
                        {
                           "except_name":"托管器主页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LEI_DIAN_MAIN, "include_str_list":["系统应用", "微信", "搜索游戏"], "exclude_str_list":["系统界面没有响应", "微信屡次停止运行"]
                        },
                        {
                           "except_name":"托管器主页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LEI_DIAN_MAIN, "include_str_list":["系统应用", "微信", "传奇"], "exclude_str_list":["系统界面没有响应", "微信屡次停止运行"]
                        },
                        {
                           "except_name":"托管器主页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LEI_DIAN_MAIN, "include_str_list":["系统应用", "微信", "全民江湖"], "exclude_str_list":["系统界面没有响应", "微信屡次停止运行"]
                        },
                        {
                           "except_name":"托管器主页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LEI_DIAN_MAIN, "include_str_list":["系统应用", "微信", "最强祖师"], "exclude_str_list":["系统界面没有响应", "微信屡次停止运行"]
                        },
                        {
                           "except_name":"等待手机上确认页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_WAIT_CONFIRM, "include_str_list":["二维码登录", "扫码成功", "请在手机上轻触确认登录"]
                        },
                        {
                           "except_name":"正在载入数据页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LODING_DATA, "include_str_list":["正在载入"]
                        },
                        {
                           "except_name":"微信可设置字体大小页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SETTING_FONT, "include_str_list":["微信可设置字体大小", "暂不设置", "前往设置"]
                        },
                        {
                           "except_name":"本次登录已失效页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LOGIN_LOSS, "include_str_list":["你的微信登录环境存在异常", "本次登录已失效"]
                        },
                        {
                           "except_name":"切换验证方式页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD, "include_str_list":["切换验证方式", "平板和手机同时登录", "找回密码"]
                        },
                        {
                           "except_name":"切换验证方式页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD, "include_str_list":["切换验证方式", "作为平板登录", "找回密码"]
                        },
                        {
                           "except_name":"登录方式(平板)", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD_PAD, "include_str_list":["请填写微信密码", "作为平板登录", "找回密码"]
                        },
                        {
                           "except_name":"登录方式(平板)", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD_PAD, "include_str_list":["用短信验证码", "作为平板登录", "找回密码"]
                        },
                        {
                           "except_name":"切换验证方式(不期待的)页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD_UNEXPECT, "include_str_list":["切换验证方式", "用声音锁登录", "找回密码"], "exclude_str_list":["平板"]
                        },
                        {
                           "except_name":"允许微信录音吗页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CAN_LU_YIN, "include_str_list":["允许微信录音"]
                        },
                        {
                           "except_name":"允许微信拍摄照片页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CAN_IMAGE, "include_str_list":["允许微信拍摄照片"]
                        },
                        {
                           "except_name":"微信屡次停止运行页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_STOP_RUN, "include_str_list":["微信屡次停止运行"]
                        },
                        {
                           "except_name":"微信没有响应页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_NO_RESPONSE, "include_str_list":["微信没有响应"]
                        },
                        {
                           "except_name":"系统界面没有响应页面", "except_code":APP_RET_CODE_SYSTEM_UI_NO_RESPONSE, "include_str_list":["系统界面没有响应", "关闭应用"]
                        },
                        {
                           "except_name":"系统界面没有响应页面", "except_code":APP_RET_CODE_SYSTEM_UI_NO_RESPONSE, "include_str_list":["系统界面没有响应", "等待"]
                        },
                        {
                           "except_name":"系统界面没有响应页面", "except_code":APP_RET_CODE_SYSTEM_UI_NO_RESPONSE, "include_str_list":["系统", "响应", "关闭应用", "等待"]
                        },
                        {
                           "except_name":"当前账号已经在其他设备登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_HAS_LOGIN_IN_OTHER, "include_str_list":["当前账号于", "设备上登录", "客户端"]
                        },
                        {
                           "except_name":"当前账号已经在其他设备登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_HAS_LOGIN_IN_OTHER_2, "include_str_list":["当前账号于", "设备上登录", "请及时改密"]
                        },
                        {
                           "except_name":"登录过期请重新登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_RE_LOGIN, "include_str_list":["登录过期", "重新登录", "确定"]
                        },
                        {
                           "except_name":"为了你的安全请重新登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SAFE_RE_LOGIN, "include_str_list":["为了你的账号安全", "请重新登录", "确定"]
                        },
                        {
                           "except_name":"密码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN, "include_str_list":["平板和手机同时登录", "密码", "短信验证"]
                        },
                        {
                           "except_name":"密码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN, "include_str_list":["平板和手机同时登录", "密码", "请填写微信密码"]
                        },
                        {
                           "except_name":"密码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN, "include_str_list":["平板和手机同时登录", "找回密码", "紧急冻结"]
                        },
                        {
                           "except_name":"密码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN, "include_str_list":["密码", "用短信验证码登录", "冻结", "回密码"]
                        },
                        {
                           "except_name":"密码登录页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN, "include_str_list":["密码", "冻结", "回密码", "更多选项"]
                        },
                        {
                           "except_name":"登录出现错误页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ERROR_LOGIN_RE, "include_str_list":["登录出现错误", "请你重新登录"]
                        },
                        {
                           "except_name":"初始使用朋友圈发送文本提醒页面", "except_code":APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ERROR_SEND_CIRCLE_TEXT_REMIND, "include_str_list":["长按拍照按钮发文字", "请勿过于依赖此方法"]
                        },
                        {
                           "except_name":"微信申请访问照片权限", "except_code":APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE, "include_str_list":["允许", "微信", "访问您设备上的照片"]
                        },
                        {
                           "except_name":"微信申请访问照片权限", "except_code":APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE, "include_str_list":["微信", "访问您设备上的照片", "媒体内容和文件"]
                        },
                        {
                           "except_name":"微信申请访问照片权限", "except_code":APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE, "include_str_list":["允许", "访问您设备上的照片", "媒体内容和文件"]
                        },
                        {
                           "except_name":"微信申请访问照片权限", "except_code":APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE, "include_str_list":["允许", "微信",  "媒体内容和文件"]
                        },
                        {
                           "except_name":"微信申请访问照片权限", "except_code":APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE, "include_str_list":["允许", "微信",  "照片及文件"]
                        },
                        {
                           "except_name":"微信申请访问照片权限", "except_code":APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE, "include_str_list":["允许", "读写设备上", "照片及文件"]
                        },
                        {
                           "except_name":"保留此次编辑", "except_code":APP_RET_CODE_MSG_KEEP_EDIT, "include_str_list":["保留此次编辑", "不保留", "保留"]
                        },
                        {
                           "except_name":"麦克风权限未开启", "except_code":APP_RET_CODE_MIC_AUTHORITY_NO_OPEN, "include_str_list":["麦克风权限未开启"]
                        },
                        {
                           "except_name":"麦克风权限未开启", "except_code":APP_RET_CODE_MIC_AUTHORITY_NO_OPEN, "include_str_list":["麦克风", "我知道了", "前往设置"]
                        },
                        {
                           "except_name":"你已退出微信", "except_code":APP_RET_CODE_YOU_HAS_LOGOUT_WECHAT, "include_str_list":["你已退出微信", "确定"]
                        },
                        {
                           "except_name":"账号在其他设备上登录", "except_code":APP_RET_CODE_HAS_LOGIN_IN_OTHER, "include_str_list":["当前账号", "登录", "若不是本人", "况可前往"]
                        },
                        {
                           "except_name":"提示：由于对方的隐私设置", "except_code":APP_RET_CODE_MSG_BECAUSE_PRIVACY, "include_str_list":["提示", "由于对方的隐私设置"]
                        },
                        {
                           "except_name":"提示：由于对方的隐私设置", "except_code":APP_RET_CODE_MSG_BECAUSE_PRIVACY, "include_str_list":["提示", "你无法通过群", "将其添加至", "确定"]
                        },
                        {
                           "except_name":"提示：由于对方的隐私设置", "except_code":APP_RET_CODE_MSG_BECAUSE_PRIVACY, "include_str_list":["由于对方的隐私设置", "将其添加至", "确定"]
                        },
                        {
                           "except_name":"小程序入口提示", "except_code":APP_RET_CODE_MSG_SMALL_PROGRAM, "include_str_list":["小程序", "小程序入口已开启", "你可以在发现"]
                        },
                        {
                           "except_name":"小程序入口提示", "except_code":APP_RET_CODE_MSG_SMALL_PROGRAM, "include_str_list":["小程序入口已开启", "你可以在发现", "查看和使用曾经用过的小程序服务"]
                        },
                        {
                           "except_name":"小程序入口提示", "except_code":APP_RET_CODE_MSG_SMALL_PROGRAM, "include_str_list":["你可以在发现", "查看和使用曾经用过的小程序服务", "关闭", "去看看"]
                        },
                        {
                           "except_name":"小程序入口提示", "except_code":APP_RET_CODE_MSG_SMALL_PROGRAM, "include_str_list":["小程序", "查看和使用曾经用过的小程序服务", "关闭", "去看看"]
                        },
                        {
                           "except_name":"小程序入口提示", "except_code":APP_RET_CODE_MSG_SMALL_PROGRAM, "include_str_list":["小程序", "小程序入口已开启", "你可以在发现", "关闭", "去看看"]
                        }                                          
                                 
                        
                            ]
                        
# 异常弹窗处理
def do_exception_proc(i_except_code, input_event):
    except_name = ""
    for except_box_info_dict in EXCEPT_BOX_INFO_DICT_LIST:
        except_name_ = except_box_info_dict["except_name"]
        except_code_ = except_box_info_dict["except_code"]
        if except_code_ == i_except_code:
            except_name = except_name_
            break 
            
    if i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_AUTHORITY:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_quxian_cancel_x, g_quxian_cancel_y)
        if True == input_event.wait(1):
            print("do_exception_proc, 被要求退出1")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_USE_DEVICE_TYPE:   
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_device_type_cancel_x, g_device_type_cancel_y)
        if True == input_event.wait(1):
            print("do_exception_proc, 被要求退出2")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_USE_DEVICE_TYPE2:   
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_device_type_cancel_x_2, g_device_type_cancel_y_2)
        if True == input_event.wait(1):
            print("do_exception_proc, 被要求退出3")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_USE_DEVICE_TYPE_ONLY_PAD:   
        # chenyj debug
        #print_my("奇怪，你进入【{}】页面，最大可能是你设置你的微信为仅允许平板登录了，请你在手机上重新设置下吧".format(except_name))
        print_my("奇怪，你进入【{}】页面，请联系客服".format(except_name))
        return APP_RET_CODE_SUCESS 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LOGION_REG:   
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_login_reg_cancel_x, g_login_reg_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出4")
            return APP_RET_CODE_ZHU_DONG_EXIT  
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["登录", "进入微信"])
        """
        adb_click(g_enter_wechat_cancel_x, g_enter_wechat_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出5")
            return APP_RET_CODE_ZHU_DONG_EXIT  
        """
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LEI_DIAN_MAIN:
        # 
        open_wechat_app_and_set_top()
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出6")
            return APP_RET_CODE_ZHU_DONG_EXIT  
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SETTING_FONT:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_setting_font_cancel_x, g_setting_font_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出7")
            return APP_RET_CODE_ZHU_DONG_EXIT  
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LOGIN_LOSS:
        # chenyj debug
        print("动作:【点击[{}]移除双按钮】".format(except_name))
        adb_click(g_login_loss_cancel_x, g_login_loss_cancel_y)
        adb_click(g_login_loss_cancel_x_2, g_login_loss_cancel_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出8")
            return APP_RET_CODE_ZHU_DONG_EXIT   
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD:
        # chenyj debug
        print("动作:【点击[{}]移除双按钮】".format(except_name))
        adb_click(g_change_login_cancel_x, g_change_login_cancel_y)
        adb_click(g_change_login_cancel_x_2, g_change_login_cancel_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出9")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD_PAD:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_change_login_pad_x, g_change_login_pad_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出10")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CHANGE_LOGIN_METHOD_UNEXPECT:
        # chenyj debug
        print_my("奇怪，你怎么会进入【{}】页面，我也无能为力，联系下客服吧".format(except_name))
        return APP_RET_CODE_SUCESS 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CAN_LU_YIN:
        if g_w_screen > g_h_screen:
            # chenyj debug
            print("动作:【点击[{}]移除双按钮.宽屏】".format(except_name))
            adb_click(g_can_audio_cancel_x_heng, g_can_audio_cancel_y_heng)
            adb_click(g_can_audio_cancel_x_heng_2, g_can_audio_cancel_y_heng_2)
            
        else:
            # chenyj debug
            print("动作:【点击[{}]移除双按钮.竖屏】".format(except_name))
            adb_click(g_can_audio_cancel_x, g_can_audio_cancel_y)
            adb_click(g_can_audio_cancel_x_2, g_can_audio_cancel_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 11")
            return APP_RET_CODE_ZHU_DONG_EXIT  
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_CAN_IMAGE:
        if g_w_screen > g_h_screen:
            # chenyj debug
            print("动作:【点击[{}]移除按钮.宽屏】".format(except_name))
            adb_click(g_can_image_cancel_x_heng, g_can_image_cancel_y_heng)
        else:
            # chenyj debug
            print("动作:【点击[{}]双移除按钮.竖屏】".format(except_name))
            adb_click(g_can_image_cancel_x, g_can_image_cancel_y)
            adb_click(g_can_image_cancel_x_2, g_can_image_cancel_y_2)
            
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出12")
            return APP_RET_CODE_ZHU_DONG_EXIT  
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_HAS_LOGIN_IN_OTHER:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_has_login_cancel_x, g_has_login_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出13")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_HAS_LOGIN_IN_OTHER_2:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_has_login_confirm_x, g_has_login_confirm_y)
        adb_click(g_has_login_confirm_x_2, g_has_login_confirm_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出14")
            return APP_RET_CODE_ZHU_DONG_EXIT                  
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_RE_LOGIN:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_re_login_cancel_x, g_re_login_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出15")
            return APP_RET_CODE_ZHU_DONG_EXIT   
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SAFE_RE_LOGIN:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_safe_re_login_cancel_x, g_safe_re_login_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出16")
            return APP_RET_CODE_ZHU_DONG_EXIT   
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN:
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            # chenyj debug
            print("动作:【点击[{}]移除双按钮】".format(except_name))
            adb_click(g_secret_login_cancel_x, g_secret_login_cancel_y)
            adb_click(g_secret_login_cancel_x_2, g_secret_login_cancel_y_2)
            if True == input_event.wait(1):
                print_my("do_exception_proc, 被要求退出17")
                return APP_RET_CODE_ZHU_DONG_EXIT              
        else:
            pass
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ERROR_LOGIN_RE:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_error_login_cancel_x, g_error_login_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出18")
            return APP_RET_CODE_ZHU_DONG_EXIT   
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_STOP_RUN:
        # chenyj debug
        print("动作:【点击[{}]移除双按钮】".format(except_name))
        adb_click(g_error_stop_cancel_x, g_error_stop_cancel_y)
        adb_click(g_error_stop_cancel_x_2, g_error_stop_cancel_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出19")
            return APP_RET_CODE_ZHU_DONG_EXIT                 
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_NO_RESPONSE:
        # chenyj debug
        print("动作:【点击[{}]移除双按钮】".format(except_name))
        adb_click(g_error_no_response_cancel_x, g_error_no_response_cancel_y)
        adb_click(g_error_no_response_cancel_x_2, g_error_no_response_cancel_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出20")
            return APP_RET_CODE_ZHU_DONG_EXIT    
    elif i_except_code == APP_RET_CODE_SYSTEM_UI_NO_RESPONSE:
        # chenyj debug
        print("动作:【点击[{}]移除双按钮】".format(except_name))
        adb_click(g_system_ui_no_response_cancel_x, g_system_ui_no_response_cancel_y)
        adb_click(g_system_ui_no_response_cancel_x_2, g_system_ui_no_response_cancel_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出21")
            return APP_RET_CODE_ZHU_DONG_EXIT    
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ERROR_SEND_CIRCLE_TEXT_REMIND:
        # chenyj debug
        print("动作:【点击[{}]我知道按钮】".format(except_name))
        adb_click(g_circle_text_i_know_x, g_circle_text_i_know_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出22")
            return APP_RET_CODE_ZHU_DONG_EXIT
    elif i_except_code == APP_RET_CODE_WEI_XIN_APPLY_VISIT_AMBLE:
        # chenyj debug
        print("动作:【点击[{}]允许按钮】".format(except_name))
        adb_click(g_wei_xin_apply_visit_amble_x, g_wei_xin_apply_visit_amble_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出23")
            return APP_RET_CODE_ZHU_DONG_EXIT
    elif i_except_code == APP_RET_CODE_MSG_KEEP_EDIT:
        # chenyj debug
        print("动作:【点击[{}]允许按钮】".format(except_name))
        adb_click(g_keep_edit_x, g_keep_edit_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出24")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_MIC_AUTHORITY_NO_OPEN:
        # chenyj debug
        print("动作:【点击[{}]我知道了按钮】".format(except_name))
        adb_click(g_mic_authority_no_open_x, g_mic_authority_no_open_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出25")
            return APP_RET_CODE_ZHU_DONG_EXIT
    elif i_except_code == APP_RET_CODE_YOU_HAS_LOGOUT_WECHAT:
        # chenyj debug
        print("动作:【点击[{}]确定双按钮】".format(except_name))
        adb_click(g_you_has_logout_wechat_x, g_you_has_logout_wechat_y)
        adb_click(g_you_has_logout_wechat_x_2, g_you_has_logout_wechat_y_2)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出26")
            return APP_RET_CODE_ZHU_DONG_EXIT
    elif i_except_code == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_AUTHORITY_KEEY_BACK:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_quxian_kee_back_cancel_x, g_quxian_kee_back_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出27")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_HAS_LOGIN_IN_OTHER:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        print_my("!!!!你的账号已经在其他设备上登录了，请重新登录")
        adb_click(g_has_login_in_other_cancel_x, g_has_login_in_other_cancel_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出28")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_MSG_BECAUSE_PRIVACY:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_msg_because_privacy_x, g_msg_because_privacy_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出29")
            return APP_RET_CODE_ZHU_DONG_EXIT 
    elif i_except_code == APP_RET_CODE_MSG_SMALL_PROGRAM:
        # chenyj debug
        print("动作:【点击[{}]移除按钮】".format(except_name))
        adb_click(g_msg_small_program_x, g_msg_small_program_y)
        if True == input_event.wait(1):
            print_my("do_exception_proc, 被要求退出30")
            return APP_RET_CODE_ZHU_DONG_EXIT     
    return APP_RET_CODE_SUCESS
    
# 异常弹窗口检查
def do_exception_check(text_of_screen):
    for except_box_info_dict in EXCEPT_BOX_INFO_DICT_LIST:
        except_name = except_box_info_dict["except_name"]
        include_str_list = except_box_info_dict["include_str_list"]
        exclude_str_list = []
        if "exclude_str_list" in except_box_info_dict:
            exclude_str_list = except_box_info_dict["exclude_str_list"]
        except_code = except_box_info_dict["except_code"]
        b_hitted = True
        for include_str in include_str_list:
            if include_str not in text_of_screen:
                b_hitted = False
                break
        for exclude_str in exclude_str_list:
            if exclude_str in text_of_screen:
                b_hitted = False
                break
        if b_hitted == True:
            # chenyj debug
            print("!!!!!检测到非业务界面[{}], because:【{}】".format(except_name, text_of_screen))
            return except_code
        
    return APP_RET_CODE_SUCESS
    
#截取模拟器中手机屏幕图，并进行异常检测，然后保存到电脑指定文件夹中
g_lock_for_adb_get_screen_with_exception = threading.Lock()
def adb_get_screen_with_exception_check_and_proc(input_event):  
    g_lock_for_adb_get_screen_with_exception.acquire()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_check_exception" + ".png"
    if True == os.path.exists(path):
        os.remove(path)
    adb_get_screen(path)
    
    # 顺便检测下分辨率的变化
    if False == adb_get_phone_size(path):
        g_lock_for_adb_get_screen_with_exception.release()
        return APP_RET_CODE_NO_READY
        
    # chenyj test
    #path = SCREENSHOT_SAVE_DIR + "/" + "test" + ".png"
    if True == input_event.wait(0.1):
        print_my("adb_get_screen_with_exception_check_and_proc, 被要求退出1")
        g_lock_for_adb_get_screen_with_exception.release()
        return APP_RET_CODE_ZHU_DONG_EXIT 
    iRet, text_return = get_ocr_result_with_small_my(path)
    # 如果是因为设备没有准备好导致截图失败，那么先认为没有异常
    if iRet == APP_RET_CODE_NO_READY:
        iRet = APP_RET_CODE_SUCESS
    if iRet != APP_RET_CODE_SUCESS:
        g_lock_for_adb_get_screen_with_exception.release()
        return iRet
    
    # 检查是否异常
    #print(f"异常检测时，获得的文本是:{text_return}")
    iRet = do_exception_check(text_return)
    if iRet != APP_RET_CODE_SUCESS:
        # 开发模式：保存异常截图
        if g_b_Develop_Mode and path is not None:
            try:
                # 创建page_img文件夹（如果不存在）
                page_img_dir = os.path.join(SCREENSHOT_SAVE_DIR, "page_img")
                if not os.path.exists(page_img_dir):
                    os.makedirs(page_img_dir)
                
                # 获取错误码名称
                error_code_name = get_error_code_name(iRet)
                # 生成带时间戳和错误码名称的文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                saved_filename = f"Except_{error_code_name}_{timestamp}.png"
                saved_path = os.path.join(page_img_dir, saved_filename)
                
                # 复制原图片
                shutil.copy(path, saved_path)
                print_my(f"[开发模式-Exception] 保存异常截图：{error_code_name} -> page_img/{saved_filename}")
            except Exception as e:
                print_my(f"[开发模式-Exception] 保存异常截图失败：{e}")
        
        g_lock_for_adb_get_screen_with_exception.release()
        return iRet
        
    g_lock_for_adb_get_screen_with_exception.release()    
    return APP_RET_CODE_SUCESS
    
# image_helper初始化 
image_init(adb_get_screen)

g_lock_for_adb_get_phone_size = threading.Lock()
def adb_get_phone_size(screen_path = ""):
    global g_w_screen
    global g_h_screen

    g_lock_for_adb_get_phone_size.acquire()
    """
    方式一：直接获得手机分辨率（问题：因为使用平板模式，获得的分辨率是1920x1080,但实际是1080*1020
    temp_path = "./phone_size.txt"
    SIZE_KEY = "Physical size: "
    
    with open(temp_path,"wb", creationflags=g_process_creationflags) as out:
        cmd = f"./LDPlayer9/adb.exe {DEVICE_CMD} shell wm size"
        subprocess.run(cmd, stdout = out, creationflags=g_process_creationflags)
        time.sleep(0.1)
    with open(temp_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        print_my(lines)
        for line in lines:
            line = line.strip()
            # Physical size: 1080x2400
            
            if SIZE_KEY in line:
                line = line.replace(SIZE_KEY, "")
                temp_list = line.split("x")
                assert len(temp_list) == 2
                g_w_screen = int(temp_list[0])
                g_h_screen = int(temp_list[1])
                print_my("动作:【获得手机的分辨率为:{}x{}】".format(g_w_screen, g_h_screen))
                return True 
    print_my("动作:【!!!!!!获得托管器分辨率失败】")
    """
    # 方式二：通过截到的图片的在大小
    if len(screen_path) == 0:
        screen_path = SCREENSHOT_SAVE_DIR + "/" + "example_for_size" + ".png"
        adb_get_screen(screen_path)
    # 打开图片文件
    try:
        with Image.open(screen_path) as img:
            # 获取图片分辨率
            width, height = img.size
            #if width > height:
            #    return False
            
            if g_w_screen == width and g_h_screen == height:
                g_lock_for_adb_get_phone_size.release()
                return True 
                
            g_w_screen = width
            g_h_screen = height
            
            g_friend_chat_list_x = int(FRIEND_CHAT_LIST_LT_X/W_SCREEN*g_w_screen)
            g_friend_chat_list_y = int(FRIEND_CHAT_LIST_LT_Y/H_SCREEN*g_h_screen)
            g_chat_x = int(CHAT_LT_X/W_SCREEN*g_w_screen)
            g_chat_y = int(CHAT_LT_Y/H_SCREEN*g_h_screen)
            g_chat_half_x = int(CHAT_HALF_X/W_SCREEN*g_w_screen)
            g_chat_time_lt_x = int(CHAT_TIME_LT_X/W_SCREEN*g_w_screen)
            g_chat_time_rb_x = int(CHAT_TIME_RB_X/W_SCREEN*g_w_screen)
            g_chat_line_height = int(CHAT_LINE_HEIGHT/H_SCREEN*g_h_screen)
            g_chat_line_height_inter = int(CHAT_LINE_HEIGHT_INTER/H_SCREEN*g_h_screen)
            g_chat_line_width_inter = int(CHAT_LINE_WIDTH_INTER/W_SCREEN*g_w_screen)
            g_chat_min_y_for_ocr = int(CHAT_MIN_Y_FOR_OCR/H_SCREEN*g_h_screen) 
            g_chat_max_y_for_ocr = int(CHAT_MAX_Y_FOR_OCR/H_SCREEN*g_h_screen) 
            g_chat_lt_x_should_min = int(CHAT_LT_X_SHOULD_MIN/W_SCREEN*g_w_screen) 
            g_chat_lt_x_should_min_inter = int(CHAT_LT_X_SHOULD_MIN_INTER/W_SCREEN*g_w_screen) 
            g_chat_rb_x_should_min = int(CHAT_RB_X_SHOULD_MIN/W_SCREEN*g_w_screen) 
            g_chat_rb_x_should_min_inter = int(CHAT_RB_X_SHOULD_MIN_INTER/W_SCREEN*g_w_screen) 
            g_sender_lt_x_should_min = int(SENDER_LT_X_SHOULD_MIN/W_SCREEN*g_w_screen) 
            g_sender_lt_x_should_min_inter = int(SENDER_LT_X_SHOULD_MIN_INTER/W_SCREEN*g_w_screen) 
            g_quxian_cancel_x = int(QUXIAN_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_quxian_cancel_y = int(QUXIAN_CANCEL_LT_Y/H_SCREEN*g_h_screen) 
            g_device_type_cancel_x = int(DEVICE_TYPE_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_device_type_cancel_y = int(DEVICE_TYPE_CANCEL_LT_Y/H_SCREEN*g_h_screen) 
            g_login_reg_cancel_x = int(LOGIN_REG_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_login_reg_cancel_y = int(LOGIN_REG_CANCEL_LT_Y/H_SCREEN*g_h_screen)    
            g_setting_font_cancel_x = int(SETTING_FONT_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_setting_font_cancel_y = int(SETTING_FONT_CANCEL_LT_Y/H_SCREEN*g_h_screen) 
            g_login_loss_cancel_x = int(LOGIN_LOSS_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_login_loss_cancel_y = int(LOGIN_LOSS_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_change_login_cancel_x = int(CHANGE_LOGIN_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_change_login_cancel_y = int(CHANGE_LOGIN_CANCEL_LT_Y/H_SCREEN*g_h_screen) 
            g_can_audio_cancel_x_heng = int(CAN_AUDIO_CANCEL_LT_X_heng/W_SCREEN_heng*g_w_screen) 
            g_can_audio_cancel_y_heng = int(CAN_AUDIO_CANCEL_LT_Y_heng/H_SCREEN_heng*g_h_screen)
            g_can_audio_cancel_x_heng_2 = int(CAN_AUDIO_CANCEL_LT_X_heng_2/W_SCREEN_heng*g_w_screen) 
            g_can_audio_cancel_y_heng_2 = int(CAN_AUDIO_CANCEL_LT_Y_heng_2/H_SCREEN_heng*g_h_screen)
            g_can_audio_cancel_x = int(CAN_AUDIO_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_can_audio_cancel_y = int(CAN_AUDIO_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_can_image_cancel_x_heng = int(CAN_IMAGE_CANCEL_LT_X_heng/W_SCREEN_heng*g_w_screen) 
            g_can_image_cancel_y_heng = int(CAN_IMAGE_CANCEL_LT_Y_heng/H_SCREEN_heng*g_h_screen)
            g_can_image_cancel_x = int(CAN_IMAGE_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_can_image_cancel_y = int(CAN_IMAGE_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_has_login_cancel_x = int(HAS_LOGIN_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_has_login_cancel_y = int(HAS_LOGIN_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_has_login_confirm_x = int(HAS_LOGIN_CONFIRM_LT_X/W_SCREEN*g_w_screen) 
            g_has_login_confirm_y = int(HAS_LOGIN_CONFIRM_LT_Y/H_SCREEN*g_h_screen) 
            g_has_login_confirm_x_2 = int(HAS_LOGIN_CONFIRM_LT_X_2/W_SCREEN*g_w_screen) 
            g_has_login_confirm_y_2 = int(HAS_LOGIN_CONFIRM_LT_Y_2/H_SCREEN*g_h_screen) 
            g_re_login_cancel_x = int(RE_LOGIN_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_re_login_cancel_y = int(RE_LOGIN_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_secret_login_cancel_x = int(SECRET_LOGIN_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_secret_login_cancel_y = int(SECRET_LOGIN_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_error_login_cancel_x = int(ERROR_LOGIN_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_error_login_cancel_y = int(ERROR_LOGIN_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_error_stop_cancel_x = int(ERROR_STOP_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_error_stop_cancel_y = int(ERROR_STOP_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_error_no_response_cancel_x = int(ERROR_NO_RESPONSE_CANCEL_LT_X/W_SCREEN*g_w_screen) 
            g_error_no_response_cancel_y = int(ERROR_NO_RESPONSE_CANCEL_LT_Y/H_SCREEN*g_h_screen)
            g_circle_text_i_know_x = int(ERROR_NO_RESPONSE_CIRCLE_TEXT_I_KNOW_X/W_SCREEN*g_w_screen) 
            g_circle_text_i_know_y = int(ERROR_NO_RESPONSE_CIRCLE_TEXT_I_KNOW_Y/H_SCREEN*g_h_screen)
            g_wei_xin_apply_visit_amble_x = int(WEI_XIN_APPLY_VISIT_AMBLE_X/W_SCREEN*g_w_screen) 
            g_wei_xin_apply_visit_amble_y = int(WEI_XIN_APPLY_VISIT_AMBLE_Y/H_SCREEN*g_h_screen)

            # chenyj debug
            if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
                print("动作:【获得微信的宽高为:{}x{}】".format(g_w_screen, g_h_screen))
            else:
                print("动作:【获得托管器的分辨率为:{}x{}】".format(g_w_screen, g_h_screen))
            g_lock_for_adb_get_phone_size.release()
            return True 
    except Exception as e:
        # chenyj debug
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
            print("动作:【获得微信宽高失败】\n{}".format(e))
        else:
            print("动作:【获得托管器分辨率失败】\n{}".format(e))
    g_lock_for_adb_get_phone_size.release()
    return False
#adb_get_phone_size() 

def get_screen_of_friend_chat_list(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v2.png"  
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (g_friend_chat_list_x, g_friend_chat_list_y, int(1075/W_SCREEN*g_w_screen), int(1833/H_SCREEN*g_h_screen))    
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (g_friend_chat_list_x, g_friend_chat_list_y, int(1075/W_SCREEN*g_w_screen), int(2132))    
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (g_friend_chat_list_x, g_friend_chat_list_y, int(590/W_SCREEN*g_w_screen), int(1103))    
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (g_friend_chat_list_x, g_friend_chat_list_y, int(399), int(984))  
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet 
    img = Image.open(temp_png)
    #print_my(bbox)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list" + ".png"
#get_screen_of_friend_chat_list(path)

def get_screen_of_new_friend_list(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v12.png"     
    
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (g_rb_x_of_nickname_of_new_friend_information_page, g_rb_y_of_nickname_of_new_friend_information_page, int(1054), int(1900))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (g_rb_x_of_nickname_of_new_friend_information_page, g_rb_y_of_nickname_of_new_friend_information_page, int(1055), int(2300))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (g_rb_x_of_nickname_of_new_friend_information_page, g_rb_y_of_nickname_of_new_friend_information_page, int(1055), int(2300))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (g_rb_x_of_nickname_of_new_friend_information_page+G_X_PIAN_YI, g_rb_y_of_nickname_of_new_friend_information_page+G_Y_PIAN_YI, int(399+G_X_PIAN_YI), int(986+G_Y_PIAN_YI))
    #print_my(bbox) 
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet 
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_new_friend_list" + ".png"
#get_screen_of_new_friend_list(path)

# 获取朋友聊天页面的关键长条
def get_screen_of_first_item_of_friend_chat_list(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v3.png"    
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        #bbox = (int(21/W_SCREEN*g_w_screen), int(121/H_SCREEN*g_h_screen), int(311/W_SCREEN*g_w_screen), int(212/H_SCREEN*g_h_screen))
        #bbox = (int(113/W_SCREEN*g_w_screen), int(133/H_SCREEN*g_h_screen), int(307/W_SCREEN*g_w_screen), int(164/H_SCREEN*g_h_screen))
        bbox = (int(113/W_SCREEN*g_w_screen), int(133/H_SCREEN*g_h_screen), int(307/W_SCREEN*g_w_screen), int(1762/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(195), int(246), int(500), int(2138))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(127), int(129), int(400), int(1099))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (int(171), int(122), int(347), int(983))
    #print_my(bbox)  
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet 
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "first_item_of_friend_chat_list" + ".png"
#get_screen_of_first_item_of_friend_chat_list(path)

# 截取table_name的截图
def get_screen_of_table_name(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v4.png"       
    # chenyj debug
    #print("get_screen_of_table_name， g_w_screen:{} g_h_screen:{}".format(g_w_screen, g_h_screen))
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (int(254), int(113), int(850), int(174))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(134/W_SCREEN*g_w_screen), int(52/H_SCREEN*g_h_screen), int(950/W_SCREEN*g_w_screen), int(100/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(134/W_SCREEN*g_w_screen), int(52/H_SCREEN*g_h_screen), int(950/W_SCREEN*g_w_screen), int(100/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (int(421+G_X_PIAN_YI), int(41+G_Y_PIAN_YI), int(866+G_X_PIAN_YI), int(85+G_Y_PIAN_YI))
    #print_my(bbox)
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_table_name" + ".png"
#get_screen_of_table_name(path)

# 截取聊天页面发送条的截图
def get_screen_of_send_btn(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v5.png"       
    # chenyj debug
    #print_my("g_w_screen:{} g_h_screen:{}".format(g_w_screen, g_h_screen))
    bbox = (int(0/W_SCREEN*g_w_screen), int(1840/H_SCREEN*g_h_screen), int(1080/W_SCREEN*g_w_screen), int(1920/H_SCREEN*g_h_screen))
    #print_my(bbox)
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)  
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_send_btn" + ".png"
#get_screen_of_send_btn(path)

# 截取“最近”页面底部的截图
def get_screen_of_recent_bottom(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v6.png"     
    # chenyj debug
    #print_my("g_w_screen:{} g_h_screen:{}".format(g_w_screen, g_h_screen))
    bbox = (int(8/W_SCREEN*g_w_screen), int(1814/H_SCREEN*g_h_screen), int(1080/W_SCREEN*g_w_screen), int(1920/H_SCREEN*g_h_screen))
    #print_my(bbox)
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_rectent_bottom" + ".png"
#get_screen_of_recent_bottom(path)

def get_screen_of_chat(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v7.png" 
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (g_chat_x, g_chat_y, int(992/W_SCREEN*g_w_screen), int(1829/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (g_chat_x, g_chat_y, int(1034), int(2132))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (g_chat_x, g_chat_y, int(1034), int(2132))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (g_chat_x, g_chat_y, int(1044+G_X_PIAN_YI), int(761+G_Y_PIAN_YI))
    #print_my(bbox)     
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_chat" + ".png"
#get_screen_of_chat(path)

def get_screen_of_friendbook(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v8.png"       
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (96, 117, int(687/W_SCREEN*g_w_screen), int(1831/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (175, 211, int(959), int(2138))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (175, 211, int(959), int(2138))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (198+G_X_PIAN_YI, 155+G_Y_PIAN_YI, int(404+G_X_PIAN_YI), int(986+G_Y_PIAN_YI))
    #print_my(bbox)
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friendbook" + ".png"
#get_screen_of_friendbook(path)

def get_screen_of_taginfo(i_tag_loop_count, path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v19.png"   
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        i_left = int(21)
        i_top = int(222+i_tag_loop_count*126)
        bbox = (i_left, i_top, int(370 + i_left), int((39+i_top)/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        i_left = int(32)
        i_top = int(395+i_tag_loop_count*226)
        bbox = (i_left, i_top, int(500 + i_left), int(57+i_top))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        i_left = int(32)
        i_top = int(395+i_tag_loop_count*226)
        bbox = (i_left, i_top, int(500 + i_left), int(57+i_top))
    #print_my(bbox)   
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS, i_left, i_top
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_taginfo" + ".png"
#get_screen_of_taginfo(1, path)

# adb找开微信应用
def adb_open_dou_yin_app():
    #找到抖音应用的包名和activity
    cmd= "{}/adb.exe {} shell am start -n {}/{}".format(LEI_DIAN_DIR, DEVICE_CMD, PACKAGE_NAME, MAIN_ACTIVAT_NAME)
    print_my("动作:【启动微信app】")
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    time.sleep(2) 
    return True
#adb_open_dou_yin_app()
#time.sleep(10)

# 打开微信应用并置顶
def open_wechat_app_and_set_top():
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        # 1.先确保已经运行
        iRet = is_windows_wechat_running_and_top()
        if iRet == APP_RET_CODE_SUCESS:
            return True
        
        if iRet == APP_RET_CODE_WECHAT_NO_RUNNING:
            iRet = start_wechat()
            if iRet != APP_RET_CODE_SUCESS:
                return False
            # 启动后等待2秒
            time.sleep(2)
            iRet = is_windows_wechat_running_and_top()
        # 2.确保是在屏幕内
        if iRet == APP_RET_CODE_WECHAT_NO_IN_SCREEN:
            print("open_wechat_app_and_set_top，微信没在屏幕内，要怎么处理呢...")
            pass 
        # 3.微信还原
        iRet = restore_wechat_normal()
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!!!open_wechat_app_and_set_top还原微信失败")
            iRet = restore_wechat_normal_by_process()
            if iRet != APP_RET_CODE_SUCESS:
                print("!!!!!open_wechat_app_and_set_to通过进程还原微信失败")
                return False
        # 4.将微信移动到当前显示器正中央
        iRet = move_wechat_to_center()
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!!!open_wechat_app_and_set_top将微信移动到当前显示器正中央失败")
            return False
        
        # 5.确保置顶
        iRet = set_wechat_top()
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!!!open_wechat_app_and_set_top设置微信置顶失败")
            return False
        #print("open_wechat_app_and_set_top， 设置微信置项及可见成功")
        return True
    else:
        return adb_open_dou_yin_app()
    
# 强制退出微信应用
def adb_stop_dou_yin_app():
    #找到抖音应用的包名和activity
    cmd= LEI_DIAN_DIR + "/adb.exe {} shell am force-stop {}".format(DEVICE_CMD, PACKAGE_NAME)
    print_my("动作:【强制停止微信app】")
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    time.sleep(2) 
#adb_stop_dou_yin_app()
#time.sleep(10)

# 重启微信
def restart_wechat(input_event):
    print(f"准备强制重启微信")
    pids = kill_wechat(False)
    if pids:
        print("已杀掉微信进程：", pids)
    if True == input_event.wait(0.1):
        print_my("restart_wechat, 被要求退出")
        return -1
    open_wechat_app_and_set_top()
    return APP_RET_CODE_SUCESS


# adb判断当前微信是不是在前台展示了
def adb_is_dou_yin_running():
    temp_path = "./activity_info.txt"
    try:
        with open(temp_path,"wb") as out:
            cmd = LEI_DIAN_DIR +  f"/adb.exe {DEVICE_CMD} shell dumpsys activity activities"
            subprocess.run(cmd, stdout = out, creationflags=g_process_creationflags)
            time.sleep(0.1)
        with open(temp_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            i_index = -1
            for i, line in enumerate(lines):
                if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
                    if "Running activities" in line:
                        i_index = i + 1
                        continue
                    if i == i_index:
                        if PACKAGE_NAME in line:
                            #print_my("微信在前台运行, Activate是：{}".format(line))
                            # chenyj debug
                            print("微信在前台运行")
                            return True
                        else:
                            print_my("!!!!微信不在前台运行")
                            return False 
                    # 无影云手机 
                    if "mCurrentFocus=Window" in line and PACKAGE_NAME in line:
                        print("微信在前台运行")
                        return True
                else:
                    if ("WindowStateAnimator" in line or "mResumedActivity" in line) and PACKAGE_NAME in line:    
                        print("微信在前台运行")
                        return True
    except Exception as e:
        print("判断当前微信是不是在前台展示了失败\n{}".format(e))
    print("微信不在前台运行")
    return False
#adb_is_dou_yin_running()

# 判断当前微信是不是在前台展示了
def is_weChat_running():
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        iRet = is_windows_wechat_running_and_top()
        if iRet == APP_RET_CODE_SUCESS:
            return True
        else:
            return False
    else:
        return adb_is_dou_yin_running()
        
# 回手机主界面
def adb_click_home():               
    cmd= LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell input keyevent 3"
    print_my("动作:【回到手机主屏幕】")
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    time.sleep(2)   
#adb_click_home()

# 返回
def adb_click_back():
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        # 注意：不能用 pyautogui.press('esc')！
        # start_block_inputs 的键盘钩子把"注入的ESC"识别为停止程序的信号
        # （见windows_helper.py的stop_block_inputs与low_level_keyboard_proc），
        # 模拟ESC会直接触发stopBtnFun导致程序自动停止。
        # 改用PostMessage直接向微信窗口投递ESC，不经过系统输入队列，不会被钩子拦截。
        print("动作:【发送ESC返回命令(PostMessage)】")
        if g_wechat_info.hwd != -1 and win32gui.IsWindow(g_wechat_info.hwd):
            VK_ESCAPE = 0x1B
            win32gui.PostMessage(g_wechat_info.hwd, win32con.WM_KEYDOWN, VK_ESCAPE, 0)
            win32gui.PostMessage(g_wechat_info.hwd, win32con.WM_KEYUP, VK_ESCAPE, 0)
        else:
            print("!!!!adb_click_back, 微信窗口句柄无效")
        time.sleep(0.5)
        return
    cmd = LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell input keyevent 4"
    print("动作:【发送系统返回命令】")
    subprocess.run(cmd, creationflags=g_process_creationflags)
    time.sleep(0.5)
#adb_click_back()



def adb_click(x, y):
    global g_table
    
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        iRet = windows_click(x, y)
        if iRet != APP_RET_CODE_SUCESS:
            return iRet
    else:
        cmd = "{}/adb.exe {} shell input tap {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, int(x), int(y))
        subprocess.run(cmd, creationflags=g_process_creationflags) 
        #print("动作:【按坐标:({}, {})】".format(x, y))
    # 画出点击位置
    if g_table is not None and g_b_Draw_snap == True:
        update_click_screen_info = {}
        update_click_screen_info["x0"] = int(x)
        update_click_screen_info["y0"] = int(y)
        update_click_screen_info_str = json.dumps(update_click_screen_info)
        g_table.signal_of_table.emit("update_click_screen_info_" + update_click_screen_info_str)

    time.sleep(0.3)
    return APP_RET_CODE_SUCESS

def adb_click_back_of_chat():
    # chenyj debug
    print("动作:【点击聊天页面的返回按钮】")
    adb_click(int(47/W_SCREEN*g_w_screen), int(80/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_back_of_chat()

# 点击“消息列表”table按钮 
def adb_click_message_list_table_btn():
    print("动作:【点击消息列表Table按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(135/W_SCREEN*g_w_screen), int(1870/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(138), int(2216))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
        adb_click(int(85), int(1155))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:# OK
        adb_click(int(46+G_X_PIAN_YI), int(146+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS

# 点击“通讯录”table按钮    
def adb_click_friendbook_table_btn():
    print("动作:【点击通讯录Table按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(404/W_SCREEN*g_w_screen), int(1874/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(400), int(2216))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
        adb_click(int(272), int(1155))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:# OK
        adb_click(int(45+G_X_PIAN_YI), int(220+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS

# 点击“通讯录管理”table按钮    
def adb_click_friendbook_manage_btn():
    print("动作:【点击通讯录管理按钮】")
    adb_click(int(269+G_X_PIAN_YI), int(133+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS

# 点击"发现"table按钮    
def adb_click_discover_table_btn():
    print("动作:【点击发现Table按钮】")
    if g_location_config:
        adb_click(g_location_config.BTN_NAV_DISCOVER_X, g_location_config.BTN_NAV_DISCOVER_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(672/W_SCREEN*g_w_screen), int(1870/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(672), int(2216))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
            adb_click(int(450), int(1155))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:# OK
            adb_click(int(48), int(361))
    return APP_RET_CODE_SUCESS

# 点击"我的"table按钮    
def adb_click_me_table_btn():
    print("动作:【点击我的Table按钮】")
    if g_location_config:
        adb_click(g_location_config.BTN_NAV_ME_X, g_location_config.BTN_NAV_ME_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(948/W_SCREEN*g_w_screen), int(1877/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(944), int(2216))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
            adb_click(int(633), int(1155))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
            adb_click(int(44+G_X_PIAN_YI), int(935+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS

# 点击发现table页中的"朋友圈"按钮 
def adb_click_friend_circle_of_discord():
    print("动作:【点击朋友圈按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_FRIEND_CIRCLE_X, g_location_config.BTN_FRIEND_CIRCLE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(132/W_SCREEN*g_w_screen), int(165/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(426), int(285))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(426), int(285))
    return APP_RET_CODE_SUCESS

# 点击文字发送模式中"谁可以看"按钮
def adb_click_who_can_see_of_text_mode():
    print("动作:【点击文字发送模式中\"谁可以看\"按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_WHO_CAN_SEE_TEXT_X, g_location_config.BTN_WHO_CAN_SEE_TEXT_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(607/W_SCREEN*g_w_screen), int(635/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(298), int(1107))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(298), int(1107))
    return APP_RET_CODE_SUCESS

# 点击图片发送模式中"谁可以看"按钮
def adb_click_who_can_see_of_img_mode():
    print("动作:【点击图片发送模式中\"谁可以看\"按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_WHO_CAN_SEE_IMG_X, g_location_config.BTN_WHO_CAN_SEE_IMG_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(607/W_SCREEN*g_w_screen), int(848/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(319), int(1413)) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(319), int(1413)) 
    return APP_RET_CODE_SUCESS

# 点击设置页面的关闭按钮
def adb_click_close_setting_btn():
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_CLOSE_SETTING_X, g_location_config.BTN_CLOSE_SETTING_Y)
    else:
        adb_click(int(790), int(25))
    return  APP_RET_CODE_SUCESS
     
# 点击添加到通讯录页面的关闭按钮
def adb_click_close_add_to_friendbook_btn():
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_CLOSE_ADD_TO_FRIENDBOOK_X, g_location_config.BTN_CLOSE_ADD_TO_FRIENDBOOK_Y)
    else:
        adb_click(int(444), int(9))
    return  APP_RET_CODE_SUCESS

# 点击添加到通讯录页面(好友不存在）的关闭按钮
def adb_click_close_add_to_friendbook_when_no_exist_btn():
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_CLOSE_ADD_TO_FRIENDBOOK_NO_EXIST_X, g_location_config.BTN_CLOSE_ADD_TO_FRIENDBOOK_NO_EXIST_Y)
    else:
        adb_click(int(1008), int(11))
    return  APP_RET_CODE_SUCESS

# 点击添加为好友页面的取消按钮
def adb_click_close_apply_add_btn(input_event):
    adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["取消"])
    return  APP_RET_CODE_SUCESS

# 点击"部分可见"按钮 
def adb_click_part_can_see():
    print("动作:【点击部分可见按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_PART_CAN_SEE_X, g_location_config.BTN_PART_CAN_SEE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(121/W_SCREEN*g_w_screen), int(430/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(200), int(755))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(200), int(755))
    return APP_RET_CODE_SUCESS

# 点击"选择朋友"按钮 
def adb_click_select_friend():
    print("动作:【点击选择朋友按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SELECT_FRIEND_X, g_location_config.BTN_SELECT_FRIEND_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(133/W_SCREEN*g_w_screen), int(638/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(243), int(1144))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(243), int(1144))
    return APP_RET_CODE_SUCESS

# 点击聊天页的消息编辑框  
def adb_click_chat_edit_for_send_btn(b_debug = False):
    # chenyj debug
    print("动作:【点击消息编辑框】")
    if b_debug == True:
        print("动作:【准备回复消息】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.EDIT_CHAT_FOR_SEND_X, g_location_config.EDIT_CHAT_FOR_SEND_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(146/W_SCREEN*g_w_screen), int(1870/H_SCREEN*g_h_screen)) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(172), int(2222))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(172), int(2222))    
    return 

# 点击添加好友，输入好友账号的编辑框   
def adb_click_edit_of_add_friend():
    # chenyj debug
    print("动作:【点击添加好友编辑框】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.EDIT_ADD_FRIEND_X, g_location_config.EDIT_ADD_FRIEND_Y)
        time.sleep(0.2)
        adb_click(g_location_config.EDIT_ADD_FRIEND_X, g_location_config.EDIT_ADD_FRIEND_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(505/W_SCREEN*g_w_screen), int(147/H_SCREEN*g_h_screen))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(418), int(269))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(319), int(175))
    return 
#adb_click_edit_of_add_friend()
 
# 点击设置备注和标签页面的备注编辑框   
def adb_click_edit_of_setting_remark():
    # chenyj debug
    print("动作:【点击设置备注和标签页面的备注编辑框】")
    adb_click(int(49/W_SCREEN*g_w_screen), int(362/H_SCREEN*g_h_screen))     
    return 

# 点击申请添加好友页面的备注编辑框   
def adb_click_remark_edit_of_apply_add():
    # chenyj debug
    print("动作:【点击申请添加好友页面的备注编辑框】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.EDIT_REMARK_APPLY_ADD_X, g_location_config.EDIT_REMARK_APPLY_ADD_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(76/W_SCREEN*g_w_screen), int(491/H_SCREEN*g_h_screen))   
            adb_click(int(76/W_SCREEN*g_w_screen), int(529/H_SCREEN*g_h_screen))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(131), int(859))   
            adb_click(int(131), int(859)) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(85), int(552))   
            adb_click(int(85), int(552)) 
    return    
#adb_click_remark_edit_of_apply_add()

# 点击通过朋友验证页面的备注编辑框   
def adb_click_remark_edit_of_pass_new_frient():
    # chenyj debug
    print("动作:【点击通过朋友验证页面的备注编辑框】")
    adb_click(int(60/W_SCREEN*g_w_screen), int(231/H_SCREEN*g_h_screen))     
    return  

# 点击发送朋友圈的方案的编辑框   
def adb_click_edit_of_wenAn_of_send_circle():
    # chenyj debug
    print("动作:【点击发送朋友圈的方案的编辑框】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.EDIT_WENAN_SEND_CIRCLE_X, g_location_config.EDIT_WENAN_SEND_CIRCLE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(153/W_SCREEN*g_w_screen), int(175/H_SCREEN*g_h_screen))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(207), int(293))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(207), int(293))
    return 

# 点击搜索可见好友栏的编辑框 
def adb_click_edit_of_search_can_see():
    # chenyj debug
    print("动作:【点击搜索可见好友栏的编辑框】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.EDIT_SEARCH_CAN_SEE_X, g_location_config.EDIT_SEARCH_CAN_SEE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(541/W_SCREEN*g_w_screen), int(162/H_SCREEN*g_h_screen))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(591), int(276))  
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(591), int(276))  
    return 

# 点击选择朋友页面的选择按钮
def adb_click_select_of_select_friend_page():
    # chenyj debug
    print("动作:【点击选择朋友页面的选择按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SELECT_OF_SELECT_FRIEND_PAGE_X, g_location_config.BTN_SELECT_OF_SELECT_FRIEND_PAGE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(998/W_SCREEN*g_w_screen), int(77/H_SCREEN*g_h_screen))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(965), int(144)) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(965), int(144)) 
    return 

# 点击"保存为标签"页面的忽略按钮 
def adb_click_ingor_of_save_label_page():
    # chenyj debug
    print("动作:【点击\"保存为标签\"页面的忽略按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_IGNORE_SAVE_LABEL_X, g_location_config.BTN_IGNORE_SAVE_LABEL_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(418/W_SCREEN*g_w_screen), int(1048/H_SCREEN*g_h_screen))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(326), int(1303))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(326), int(1303))
    return 

# 点击"谁可以看"页面的完成按钮 
def adb_click_finish_of_who_can_see_page():
    # chenyj debug
    print("动作:【点击\"谁可以看\"页面的完成按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_FINISH_WHO_CAN_SEE_X, g_location_config.BTN_FINISH_WHO_CAN_SEE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(997/W_SCREEN*g_w_screen), int(76/H_SCREEN*g_h_screen))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(964), int(141))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(964), int(141))
    return 

# 点击"拍照记录生活"页面的我知道按钮 
def adb_click_i_know_of_circle_photo_record_page():
    # chenyj debug
    print("动作:【点击\"拍照记录生活\"页面的我知道按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_I_KNOW_CIRCLE_PHOTO_X, g_location_config.BTN_I_KNOW_CIRCLE_PHOTO_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(545/W_SCREEN*g_w_screen), int(1176/H_SCREEN*g_h_screen))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(545), int(1376))  
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(545), int(1376))  
    return 
    
# 点击选择搜索到的用户 
def adb_click_select_friend_of_searched():
    # chenyj debug
    print("动作:【点击选择搜索到的用户】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SELECT_FRIEND_SEARCHED_X, g_location_config.BTN_SELECT_FRIEND_SEARCHED_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(225/W_SCREEN*g_w_screen), int(283/H_SCREEN*g_h_screen))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(337), int(499))  
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(337), int(499))  
    return 
    
# 点击聊天页的加号按钮  
def adb_click_chat_add_btn(b_debug = False):
    # chenyj debug
    print("动作:【点击加号按钮】")
    if b_debug == True:
        print("动作:【点击加号按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_CHAT_ADD_X, g_location_config.BTN_CHAT_ADD_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(1040/W_SCREEN*g_w_screen), int(1875/H_SCREEN*g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(1016), int(2200))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(1016), int(2200))     
    return 

# 点击聊天页的相册按钮  
def adb_click_chat_album_btn(b_debug = True):
    # chenyj debug
    print("动作:【点击相册按钮】")
    if b_debug == True:
        print("动作:【点击相册按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_CHAT_ALBUM_X, g_location_config.BTN_CHAT_ALBUM_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(154/W_SCREEN*g_w_screen), int(1644/H_SCREEN*g_h_screen)) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(166), int(1808))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(166), int(1808))    
    return 

# 带检查地点击聊天页的相册按钮 
def adb_click_chat_album_btn_with_check(input_event, b_debug = False):
    image_check_begin()
    adb_click_chat_album_btn(b_debug)
    #time.sleep(0.5)
    # 在电脑慢的时间这里要设置大一些
    time.sleep(2)
    iRet = wait_image_change(input_event, 0.99)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    return APP_RET_CODE_SUCESS
    
# 选中相册的第一张图片按钮  
def adb_click_album_first_img_btn(b_debug = False):
    # chenyj debug
    print("动作:【点击相册的第一张图片按钮】")
    if b_debug == True:
        print("动作:【点击相册的第一张图片按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_ALBUM_FIRST_IMG_X, g_location_config.BTN_ALBUM_FIRST_IMG_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(242/W_SCREEN*g_w_screen), int(142/H_SCREEN*g_h_screen))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(216), int(253))  
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(216), int(253))  
    return 

# 点击发送图片按钮  
def adb_click_send_img_btn(b_debug = True):
    # chenyj debug
    #print("动作:【点击发送图片按钮】")
    if b_debug == True:
        print("动作:【点击发送图片按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SEND_IMG_X, g_location_config.BTN_SEND_IMG_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(1010/W_SCREEN*g_w_screen), int(1877/H_SCREEN*g_h_screen))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(929), int(2215))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(929), int(2215))     
    return 

# adb点击发送按钮 
def adb_click_send_btn(b_debug = True):
    # chenyj debug
    print("动作:【点击发送】")
    if b_debug == True:
        print_my("动作:【回复消息】完成")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SEND_X, g_location_config.BTN_SEND_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(1043/W_SCREEN*g_w_screen), int(1876/H_SCREEN*g_h_screen))     
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(972), int(2166)) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(972), int(2166)) 
    return 

# adb点击发送朋友圈的发送按钮 
def adb_click_send_btn_of_send_circle(b_debug = True):
    # chenyj debug
    print("动作:【点击发送朋友圈的发送按钮】")
    if b_debug == True:
        print_my("动作:【回复消息】完成")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SEND_CIRCLE_X, g_location_config.BTN_SEND_CIRCLE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(1008/W_SCREEN*g_w_screen), int(77/H_SCREEN*g_h_screen))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(970), int(141))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(970), int(141))   
    return 

# adb点击发送朋友圈编辑的退出确认按钮 
def adb_click_exit_btn_of_send_circle_edit():
    # chenyj debug
    print("动作:【点击发送朋友圈编辑的退出确认按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_EXIT_SEND_CIRCLE_EDIT_X, g_location_config.BTN_EXIT_SEND_CIRCLE_EDIT_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(665/W_SCREEN*g_w_screen), int(1047/H_SCREEN*g_h_screen))  
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(757), int(1304))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(757), int(1304))    
    return 
    
# 带检查地点击聊天页面左上角的返回按钮 
def adb_click_back_of_chat_with_check(input_event):
    image_check_begin()
    adb_click_back_of_chat()
    #time.sleep(0.5)
    # 在电脑慢的时间这里要设置大一些
    time.sleep(2)
    iRet = wait_image_change(input_event, 0.991)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("adb_click_back_of_chat_with_check, 被要求退出2")
        else:
            print_my("!!!!, adb_click_back_of_chat_with_check失败({})".format(iRet))
        return iRet
    return APP_RET_CODE_SUCESS

def adb_click_back_with_check(input_event, i_count = 1, need_rate = 0.991):
    for i in range(i_count):
        image_check_begin()
        adb_click_back()
        iRet = wait_image_change(input_event, need_rate)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("adb_click_back_with_check, 被要求退出2")
            else:
                print_my("####adb_click_back_with_check失败({})".format(iRet))
            return iRet
    return APP_RET_CODE_SUCESS
 
# 长按某个坐标点
def adb_longpress(x, y):
    drag_bot_x_random_number = x
    drag_bot_y_random_number = y
    drag_top_x_random_number = x 
    drag_top_y_random_number = y
    cmd = "{}/adb.exe {} shell input swipe {} {} {} {} 800".format(LEI_DIAN_DIR, DEVICE_CMD, drag_bot_x_random_number, drag_bot_y_random_number, drag_top_x_random_number, drag_top_y_random_number)
    #print_my(cmd)
    subprocess.run(cmd, creationflags=g_process_creationflags)     
    #print("动作:【长按坐标:({}, {})】".format(x, y))
    time.sleep(0.1)
#adb_longpress(30, 30)

# 长按右上角发送朋友圈按钮
def adb_longpress_send_circle_btn():
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        drag_bot_x_random_number = g_location_config.BTN_LONGPRESS_SEND_CIRCLE_BOT_X
        drag_bot_y_random_number = g_location_config.BTN_LONGPRESS_SEND_CIRCLE_BOT_Y
        drag_top_x_random_number = g_location_config.BTN_LONGPRESS_SEND_CIRCLE_TOP_X
        drag_top_y_random_number = g_location_config.BTN_LONGPRESS_SEND_CIRCLE_TOP_Y
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            drag_bot_x_random_number = 1014
            drag_bot_y_random_number = 65
            drag_top_x_random_number = 1033
            drag_top_y_random_number = 82
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            drag_bot_x_random_number = 983
            drag_bot_y_random_number = 129
            drag_top_x_random_number = 1026
            drag_top_y_random_number = 159
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            drag_bot_x_random_number = 983
            drag_bot_y_random_number = 129
            drag_top_x_random_number = 1026
            drag_top_y_random_number = 159
        else:
            drag_bot_x_random_number = 983
            drag_bot_y_random_number = 129
            drag_top_x_random_number = 1026
            drag_top_y_random_number = 159
    
    cmd = "{}/adb.exe {} shell input swipe {} {} {} {} 800".format(LEI_DIAN_DIR, DEVICE_CMD, drag_bot_x_random_number, drag_bot_y_random_number, drag_top_x_random_number, drag_top_y_random_number)
    #print_my(cmd)
    subprocess.run(cmd, creationflags=g_process_creationflags)     
    print("动作:【长按右上角发送朋友圈按钮】")
    time.sleep(0.1)
#adb_longpress_send_circle_btn()
 
 
def windows_longpress_send_circle_btn():
    return windows_longpress(107, 33)
    
# 点击右上角发送朋友圈按钮
def adb_click_send_circle_btn():
    # chenyj debug
    print("动作:【点击右上角发送朋友圈按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SEND_CIRCLE_TOP_RIGHT_X, g_location_config.BTN_SEND_CIRCLE_TOP_RIGHT_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(1023/W_SCREEN*g_w_screen), int(80/H_SCREEN*g_h_screen))   
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(1000), int(135))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(1000), int(135))    
    return 

# 点击朋友圈页的从相册选择按钮
def adb_click_select_from_album_btn_of_circle():
    # chenyj debug
    print("动作:【点击朋友圈页的从相册选择按钮】")
    if g_location_config and g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(g_location_config.BTN_SELECT_FROM_ALBUM_CIRCLE_X, g_location_config.BTN_SELECT_FROM_ALBUM_CIRCLE_Y)
    else:
        # 兜底逻辑
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click(int(538/W_SCREEN*g_w_screen), int(1779/H_SCREEN*g_h_screen))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click(int(532), int(2048))    
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click(int(532), int(2048))    
    return 

# 向下滑动聊天列表栏
def adb_slide_friend_chat_list_down():
    drag_bot_x_random_number = randint(10, g_w_screen)
    drag_bot_y_random_number = randint(int(1487/1920 * g_h_screen), int(1625/1920 * g_h_screen))
    drag_top_x_random_number = randint(10, g_w_screen)
    drag_top_y_random_number = randint(int(773/1920 * g_h_screen), int(885/1920 * g_h_screen))
    cmd = "{}/adb.exe {} shell input swipe {} {} {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, drag_bot_x_random_number, drag_bot_y_random_number, drag_top_x_random_number, drag_top_y_random_number)
    #print_my(cmd)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    print_my("动作:【向下滑动聊天列表1屏】")
    time.sleep(0.1)
#path = SCREENSHOT_SAVE_DIR + "/" + "example_friend_chat_list_down" + ".png"
#adb_get_screen(path)
#adb_slide_friend_chat_list_down()

# 向上滑动聊天列表栏
def adb_slide_friend_chat_list_up():
    drag_bot_x_random_number = randint(10, g_w_screen)
    drag_bot_y_random_number = randint(int(1487/1920 * g_h_screen), int(1625/1920 * g_h_screen))
    drag_top_x_random_number = randint(10, g_w_screen)
    drag_top_y_random_number = randint(int(773/1920 * g_h_screen), int(885/1920 * g_h_screen))
    cmd = "{}/adb.exe {} shell input swipe {} {} {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, drag_top_x_random_number, drag_top_y_random_number, drag_bot_x_random_number, drag_bot_y_random_number)
    #print_my(cmd)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    print_my("动作:【向上滑动聊天列表1屏】")
    time.sleep(0.1)
#path = SCREENSHOT_SAVE_DIR + "/" + "example_friend_chat_list_up" + ".png"
#adb_get_screen(path)
#adb_slide_friend_chat_list_up()

def find_username_location(dst_username, json_return = ""):
    global g_i_crop_count
    
    x_of_lt = -1
    y_of_lt = -1
    x_of_middle = -1
    y_of_middle = -1
    
    b_is_groud, dst_username = username_standard(dst_username)
    
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list" + ".png"
    if len(json_return) == 0:
        get_screen_of_friend_chat_list(path)
        try:
            _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
        except Exception as e:
            print_my("!!!!!find_username_location， ocr_return_has_location, 出现异常\n Exception: {}".format(e))
            return x_of_lt, y_of_lt, x_of_middle, y_of_middle
        if json_return is None: 
            print_my("!!!!!find_username_location， find_username_location, ocr_return_has_location失败")
            return x_of_lt, y_of_lt, x_of_middle, y_of_middle
    # 在好友列表中找到指定的好友
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        
        """
        try:
            img = Image.open(path)
            bbox = (x, y, x + width, y + height)
            cropped_img = img.crop(bbox)
            g_i_crop_count += 1
            #crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_{}.png".format(g_i_crop_count)
            crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp.png"
            cropped_img.save(crop_path)
            crop_mage = imread(crop_path)
            # chenyj debug
            #print("content:{}".format(content))
            if True == image_is_black(crop_mage):
                pass
        except Exception as e: 
            print("!!!!出现异常:{}".format(e))
            continue 
        """
        # chenyj 
        # fix bug:消息列表中有好友"陈毓靖美亚柏科"，如果客服机器人设置的好友是"陈毓靖"，这里会命中
        #     但到了enter_chat_ui 里判断是不是在聊天对象里，却是采用严格判断的，所以这里也用严格判断        
        #if dst_username in result["words"]:
        _, username_of_ocr = username_standard(result["words"])
        if dst_username == username_of_ocr:
            x_of_lt = result["location"]["left"]
            y_of_lt = result["location"]["top"]
            x_of_middle = result["location"]["left"] + int(result["location"]["width"]/2)
            y_of_middle = result["location"]["top"] + int(result["location"]["height"]/2)
 
            # 加上偏移 
            x_of_lt = g_friend_chat_list_x + x_of_lt
            y_of_lt = g_friend_chat_list_y + y_of_lt
            x_of_middle = g_friend_chat_list_x + x_of_middle    
            y_of_middle = g_friend_chat_list_y + y_of_middle 
            break
    if x_of_middle != -1 and y_of_middle != -1:
        # chenyj debug
        #print_my("在好友列表中，用户【{}】的坐标是:x_of_middle:{} y_of_middle:{}".format(dst_username, x_of_middle, y_of_middle))
        pass
    else:
        pass 
        
    return x_of_lt, y_of_lt, x_of_middle, y_of_middle

import re

# 预编译正则，速度更快
_TIME_TAIL_RE = re.compile(
    r'(?:昨天|今天|明天|前天|后天|周一|周二|周三|周四|周五|周六|周日)?\s*[0-2]?\d[：:][0-5]\d$'
)

def strip_right_time(text: str) -> str:
    """
    去掉字符串右侧的时间串（含中文前缀）
    示例：
        '文件传输助手昨天20：07' -> '文件传输助手'
        '52CV-语义实例.19：29'   -> '52CV-语义实例.'
    """
    return _TIME_TAIL_RE.sub('', text)
 
# 对文本进行统一规整处理
def text_standard(text):
    text = strip_right_time(text)
    text = text.replace("（", "(").replace("）", ")").replace("①", "1").replace("②", "2").replace("③", "3").replace("④", "4").replace("⑤", "5").replace("⑥", "6").replace("⑦", "7").replace("⑧", "8").replace("⑨", "9").replace("⑩", "10").replace("o", "0").replace("O", "0")
    text = text.replace(".…", "").replace("...", "").replace("，", "")
    
    return text  

def username_standard(text):  
    b_is_groud = False 
    
    if len(text) == 0:
        return b_is_groud, text
    text = text_standard(text)
    if text.endswith("A"):
        text = text[:-1]
    if text.endswith("日"):
        text = text[:-1]
    if text.endswith("&"):
        text = text[:-1]
        
    # 判断是否是群聊消息
    pattern = r'\(\d+\)$'
    search_result = re.search(pattern, text)
    if search_result:
        b_is_groud = True
        text = text.replace(search_result.group(), "")
        
    text = clean_string(text)
    
    return b_is_groud, text 
    
# 通过标题判断是否在聊天页面 
def is_in_chat_page_by_title():
    b_is_in_chat = False
    user_name_of_chat = ""
    
    TIME_BEGIN()
    
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_table_name" + ".png"
    get_screen_of_table_name(path)
    try:
        # chenyj test 
        #iRet, text_return = tesseract_get_ocr_result(img_path)
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!get_page_type， get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        traceback.print_exc()  # 打印详细的堆栈信息
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        TIME_END()
        return APP_RET_CODE_OCR_ERROR, b_is_in_chat, user_name_of_chat
    if json_return is None: 
        print_my("!!!!!get_page_type, get_ocr_result_with_small 失败")
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        TIME_END()
        return APP_RET_CODE_OCR_ERROR, b_is_in_chat, user_name_of_chat
    # chenyj debug
    #print(json_return["words_result"])
    # chenyj test  
    if len(json_return["words_result"]) == 2:
        json_return["words_result"] = [json_return["words_result"][0]]
    if len(json_return["words_result"]) != 1:   
        return APP_RET_CODE_SUCESS, b_is_in_chat, user_name_of_chat
    for result in json_return["words_result"]:
        content = result["words"]
        b_is_in_chat = True
        user_name_of_chat = content
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        # chenyj debug
        print("当前是在聊天页,对象:【{}】".format(user_name_of_chat))
        break
    TIME_END()
    return APP_RET_CODE_SUCESS, b_is_in_chat, user_name_of_chat
#iRet, b_is_in_chat, user_name_of_chat = is_in_chat_page_by_title()

def get_page_type_by_title():
    type_return = PageType.Unknow
    b_is_groud = False
    user_name_of_chat = ""
    
    TIME_BEGIN()
    
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_table_name" + ".png"
    get_screen_of_table_name(path)
    try:
        # chenyj test 
        #iRet, text_return = tesseract_get_ocr_result(img_path)
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!get_page_type， get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        traceback.print_exc()  # 打印详细的堆栈信息
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        TIME_END()
        return APP_RET_CODE_OCR_ERROR, type_return, b_is_groud, user_name_of_chat
    if json_return is None: 
        print_my("!!!!!get_page_type, get_ocr_result_with_small 失败")
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        TIME_END()
        return APP_RET_CODE_OCR_ERROR, type_return, b_is_groud, user_name_of_chat
    # chenyj debug
    #print(json_return["words_result"])
    
    if len(json_return["words_result"]) == 0:
        print("get_page_type, 没有识别到任何文字")
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        TIME_END()
        return APP_RET_CODE_SUCESS, type_return, b_is_groud, user_name_of_chat
    # chenyj test  
    if len(json_return["words_result"]) == 2:
        json_return["words_result"] = [json_return["words_result"][0]]
        
    if len(json_return["words_result"]) != 1:
        print("当前可能是在\"我的\"页")
        path_full = SCREENSHOT_SAVE_DIR + "/" + "example_for_page_type" + ".png"
        iRet = adb_get_screen(path_full)
        if iRet != APP_RET_CODE_SUCESS:
            TIME_END()
            return iRet, type_return, b_is_groud, user_name_of_chat
        try:
            _, json_return_full = test_baidu_ocr.get_ocr_result_with_small(path_full)
        except Exception as e:
            print_my("!!!!!2get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
            b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
            TIME_END()
            return APP_RET_CODE_OCR_ERROR, type_return, b_is_groud, user_name_of_chat
        if json_return_full is None: 
            print_my("!!!!!2get_page_type, get_ocr_result_with_small 失败")
            b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
            TIME_END()
            return APP_RET_CODE_OCR_ERROR, type_return, b_is_groud, user_name_of_chat
        # chenyj debug
        #print_my(json_return_full["words_result"])        
        b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
        TIME_END()
        return APP_RET_CODE_SUCESS, type_return, b_is_groud, user_name_of_chat
        
    for result in json_return["words_result"]:
        content = result["words"]
        if ("微信" in content and ("(" in content or "（" in content) and (")" in content or "）" in content)) or "微信" == content:
            # chenyj debug
            print("当前是在消息列表页")
            type_return = PageType.Message_List
            break
        elif "通讯录" == content:
            # chenyj debug
            print("当前是在通讯录页")
            type_return = PageType.FriendBook
            break
        elif "发现" == content:
            # chenyj debug
            print("当前是在发现页")
            type_return = PageType.Discover
            break
        elif "全部收藏" == content:
            # chenyj debug
            print("当前是在收藏页")
            type_return = PageType.Collect
            break
        else:
            type_return = PageType.Chat
            user_name_of_chat = content
            b_is_groud, user_name_of_chat = username_standard(user_name_of_chat)
            # chenyj debug
            print("当前是在聊天页,对象:【{}】".format(user_name_of_chat))
            break
    TIME_END()
    return APP_RET_CODE_SUCESS, type_return, b_is_groud, user_name_of_chat
#iRet, type_page, b_is_groud, user_name_of_chat = get_page_type_by_title()

PAGE_INFO_DICT_LIST = [
                        {
                            "page_name":"我的页面", "page_type_code":PageType.Me, "include_str_list":["视频号直播", "聊天文件", "聊天记录管理"]
                        },
                        {
                            "page_name":"我的页面", "page_type_code":PageType.Me, "include_str_list":["加载历史聊天记录", "锁定", "意见反", "设置"]
                        },
                        {
                            "page_name":"我的页面", "page_type_code":PageType.Me, "include_str_list":["视频号直播", "锁定", "意见反", "设置"]
                        },
                        {
                            "page_name":"我的页面", "page_type_code":PageType.Me, "include_str_list":["视频号直播", "聊天记录管理", "加载历史聊天记录"]
                        },
                        {
                            "page_name":"我的页面", "page_type_code":PageType.Me, "include_str_list":["视频号直播", "聊天记录管理", "意见反", "设置"]
                        },
                        {
                            "page_name":"我的页面", "page_type_code":PageType.Me, "include_str_list":["聊天文件", "加载历史聊天记录", "锁定", "设置"]
                        },
                        {
                            "page_name":"设置页面", "page_type_code":PageType.Setting, "include_str_list":["账号与存", "自动登录", "快捷键", "通知"]
                        },
                        {
                            "page_name":"设置页面", "page_type_code":PageType.Setting, "include_str_list":["账号与存", "保留聊天记录", "自动下载"]
                        },
                        {
                            "page_name":"设置页面", "page_type_code":PageType.Setting, "include_str_list":["保留聊天记录", "空间", "管理", "关于微信", "存储位置", "天记录"]
                        },
                        {
                            "page_name":"设置页面", "page_type_code":PageType.Setting, "include_str_list":["账号与存", "自动登录", "关于微信", "存储位置", "天记录"]
                        },
                        {
                            "page_name":"设置页面", "page_type_code":PageType.Setting, "include_str_list":["自动登录", "通知", "空间", "管理", "存储位置", "天记录"]
                        },
                        {
                            "page_name":"设置页面", "page_type_code":PageType.Setting, "include_str_list":["号与存", "退出登录", "通用", "自动登录", "暂仅支持在手机上开启"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["新消息通知", "通知开关", "接收新消息通知", "接收语音和视频通话"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["通知开关", "接收新消息通知", "接收语音和视频通话", "通知显示消息详情"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["接收新消息通知", "接收语音和视频通话", "通知显示消息详情"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["接收语音和视频通话", "通知显示消息详情", "声音与震动", "消息提示音"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["接收新消息通知", "通知显示消息详情", "声音与震动", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["通知显示消息详情", "声音与震动", "消息提示音", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["新消息通知", "通知显示消息详情", "声音与震动", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["新消息通知", "接收新消息", "接收语音和视频通话", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["新消息通知", "通知开关", "接收语音和视频通话", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["消息通知", "语音和视频通话通知", "通知显示内容"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["消息通知", "通知显示内容", "消息提示音", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["消息通知", "语音和视频通话通知", "来电铃声"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["消息通知", "语音和视频通话通知", "提示音", "来电"]
                        },
                        {
                            "page_name":"新消息通知页面", "page_type_code":PageType.Setting_New_message_notice, "include_str_list":["消息通知", "语音和视频通话通知", "声音与震动", "来电"]
                        },
                        {
                            "page_name":"收藏页面", "page_type_code":PageType.Collect, "include_str_list":["搜索收藏", "新建笔记", "全部收藏"]
                        },
                        {
                            "page_name":"收藏页面", "page_type_code":PageType.Collect, "include_str_list":["最近使用", "链接", "图片与视频"]
                        },
                        {
                            "page_name":"收藏页面", "page_type_code":PageType.Collect, "include_str_list":["搜索收藏", "全部收藏", "最近使用"]
                        },
                        {
                            "page_name":"收藏页面", "page_type_code":PageType.Collect, "include_str_list":["全部收藏", "最近使用", "链接", "图片与视频"]
                        },
                        {
                            "page_name":"收藏页面", "page_type_code":PageType.Collect, "include_str_list":["链接", "图片与视频", "笔记", "文件", "音乐与音频", "聊天记录", "语音", "位置"]
                        },
                        {
                            "page_name":"收藏页面", "page_type_code":PageType.Collect, "include_str_list":["全部收藏", "最近使用", "链接", "图片与视频", "音乐与音频", "聊天记录", "语音", "位置"]
                        },
                        {
                            "page_name":"标签页面", "page_type_code":PageType.Tag, "include_str_list":["通讯录标签", "新建", "未设置标签的朋友"]
                        },                
                        {
                            "page_name":"标签页面", "page_type_code":PageType.Tag, "include_str_list":["新建", "编辑", "未设置标签的朋友"]
                        },  
                        {
                            "page_name":"标签页面", "page_type_code":PageType.Tag, "include_str_list":["通讯录标签", "新建", "编辑"]
                        }, 
                        {
                            "page_name":"标签为空页面", "page_type_code":PageType.Tag_Empty, "include_str_list":["通讯录标签", "新建标签"]
                        }, 
                        {
                            "page_name":"添加朋友页", "page_type_code":PageType.Add_Frient, "include_str_list":["添加朋友", "雷达加朋友"]
                        },
                        {
                            "page_name":"添加朋友页", "page_type_code":PageType.Add_Frient, "include_str_list":["添加朋友", "加身边的朋友"]
                        },
                        {
                            "page_name":"添加朋友页", "page_type_code":PageType.Add_Frient, "include_str_list":["手机联系人", "企业微信联系人"]
                        },
                        {
                            "page_name":"添加朋友页", "page_type_code":PageType.Add_Frient, "include_str_list":["雷达加朋友", "加身边的朋友"]
                        },
                        {
                            "page_name":"从相册选择页", "page_type_code":PageType.Select_From_Album, "include_str_list":["拍摄", "照片或视频"]
                        },
                        {
                            "page_name":"从相册选择页", "page_type_code":PageType.Select_From_Album, "include_str_list":["拍摄", "从相册选择"]
                        },
                        {
                            "page_name":"从相册选择页", "page_type_code":PageType.Select_From_Album, "include_str_list":["照片或视频", "从相册选择"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["搜索", "取消", "搜索指定内容"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["搜索", "取消", "朋友圈", "视频号"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["搜索指定内容", "朋友圈", "公众号", "视频号"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "最常使用", "聊天记录", ]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "收藏", "搜索网络结果"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["聊天记录", "收藏", "搜索网络结果"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "联系人", "搜索网络结果"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "搜索"], "max_character_count": 70
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":[("文件传输助手",4)]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["文件传输助手", "取消", "最常使用"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["文件传输助手", "最常使用", "搜索网络结果"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["文件传输助手", "取消",  "搜索网络结果"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["搜索", "最近在搜",  "页面设置"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "最近在搜",  "页面设置"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "索",  "页面设置"]
                        },
                        {
                            "page_name":"搜索页", "page_type_code":PageType.Search, "include_str_list":["取消", "群聊",  "搜索"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["聊天信息", "群聊名称", "群二维码", "群公告"]
                        },
                       {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["聊天信息", "群聊名称", "群二维码", "备注"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["群聊名称", "群二维码", "群公告", "备注"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["群二维码", "群公告", "备注", "查找聊天记录"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["群公告", "备注", "查找聊天记录", "消息免打扰"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["查找聊天记录", "消息免打扰", "置顶聊天", "保存到通讯录"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["群二维码", "保存到通讯录", "我在群里的昵称", "显示群成员"]
                        },
                        {
                            "page_name":"群信息页", "page_type_code":PageType.GroupInfo, "include_str_list":["聊天信息", "群公告", "查找聊天记录", "显示群成员"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天成员", "(", ")"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天成员", "(", "）"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天成员", "（", ")"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天成员", "（", "）"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天成员", "搜索"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天信息", "（", "）"], "exclude_str_list":["群二维码", "群公告", "群聊名称", "备注"]
                        },
                        {
                            "page_name":"群成员页", "page_type_code":PageType.GroupMember, "include_str_list":["聊天信息", "(", ")"], "exclude_str_list":["群二维码", "群公告", "群聊名称", "备注"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":[("发现", 2), "通讯录", "我"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":["扫一扫", "发现", "通讯录", "我"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":["听一听", "发现", "通讯录", "我"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":["小程序", "发现", "通讯录", "我"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":["扫一扫", "听一听", "小程序", "发现"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":["发", "视频号", "扫一扫", "附近", "微信"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":[ "视频号", "扫一扫", "附近", "微信", "通", "发现"]
                        },
                        {
                            "page_name":"发现页面", "page_type_code":PageType.Discover, "include_str_list":["视频号", "直播", "附近", "微信", "发现"]
                        },
                        {
                            "page_name":"消息列表页", "page_type_code":PageType.Message_List, "include_str_list":["微信(", "通讯录", "发现XXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "我", ")"], "exclude_str_list":["正在载入"]
                        },
                        {
                            "page_name":"通讯录管理页", "page_type_code":PageType.FriendBook_Manage, "include_str_list":["通讯录管理", "搜索", "呢称", "备注", "标签"]
                        },
                        {
                            "page_name":"通讯录管理页", "page_type_code":PageType.FriendBook_Manage, "include_str_list":["呢称", "备注", "标签", "朋友权限", "全部"]
                        },
                        {
                            "page_name":"通讯录管理页", "page_type_code":PageType.FriendBook_Manage, "include_str_list":[ "备注", "标签", "朋友权限", "全部", "最近群聊"]
                        },
                        {
                            "page_name":"通讯录管理页", "page_type_code":PageType.FriendBook_Manage, "include_str_list":["标签", "朋友权限", "全部", "标签", "最近群聊"]
                        },
                        {
                            "page_name":"通讯录管理页", "page_type_code":PageType.FriendBook_Manage, "include_str_list":["通讯录管理", "全部", "标签", "最近群聊"]
                        },
                        {
                            "page_name":"通讯录管理页", "page_type_code":PageType.FriendBook_Manage, "include_str_list":["通讯录管理", "呢称", "备注", "标签", "朋友权限"]
                        },
                        {
                            "page_name":"添加到通讯录页", "page_type_code":PageType.Add_to_FriendBook, "include_str_list":["添加朋友", "添加到通讯录"]
                        },
                        {
                            "page_name":"添加到通讯录页", "page_type_code":PageType.Add_to_FriendBook, "include_str_list":["添加朋友", "搜索", "视频号"]
                        },
                        {
                            "page_name":"添加到通讯录页", "page_type_code":PageType.Add_to_FriendBook, "include_str_list":["搜索", "视频号", "添加到通讯录"]
                        },
                        {
                            "page_name":"添加到通讯录页", "page_type_code":PageType.Add_to_FriendBook, "include_str_list":["添加朋友", "视频号", "等待验证"]
                        },
                        {
                            "page_name":"添加到通讯录页(文件传输助手)", "page_type_code":PageType.Add_to_FriendBook_FILE_CHANGE, "include_str_list":["添加到通讯录", "文件传输助手"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(文件传输助手)", "page_type_code":PageType.Add_to_FriendBook_FILE_CHANGE, "include_str_list":["文件传输助手", "功能介绍", "登录电脑版"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(文件传输助手)", "page_type_code":PageType.Add_to_FriendBook_FILE_CHANGE, "include_str_list":["添加到通讯录", "功能介绍", "登录电脑版"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["添加到通讯录", "设置备注", "添加标签与描述", "标签"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["标签", "描述", "设置朋友权限", "聊天", "朋友圈", "微信运动", "仅聊天", "不"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["添加到通讯录", "添加标签与描述", "标签", "描述", "聊天", "朋友圈", "微信运动", "仅聊天"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["设置备注", "添加标签与描述", "标签", "描述", "设置朋友权限", "朋友圈", "微信运动", "不"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["添加到通讯录", "设置备注", "描述", "设置朋友权限", "聊天", "朋友圈", "仅聊天", "不"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["添加到通讯录", "设置备注", "朋友圈", "微信运动", "仅聊天", "不"]
                        }, 
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["设置备注", "标签", "描述", "设置朋友权限", "聊天", "朋友圈", "不"]
                        },
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["设置备注", "标签", "描述", "设置朋友权限", "聊天", "朋友", "运动", "不"]
                        },
                        {
                            "page_name":"添加到通讯录页(对方主动请求)", "page_type_code":PageType.Add_to_FriendBook_OTHER_ZHU_DONG, "include_str_list":["设置备注", "标签", "描述", "聊天", "状态", "运动", "不"]
                        },      
                        {
                            "page_name":"新的朋友页", "page_type_code":PageType.New_Friend_Of_FriendBook, "include_str_list":["录管理", "搜索", "等待验证"]
                        },     
                        {
                            "page_name":"新的朋友页", "page_type_code":PageType.New_Friend_Of_FriendBook, "include_str_list":["新的朋友", "等待验证", "已添加"]
                        },     
                        {
                            "page_name":"新的朋友页", "page_type_code":PageType.New_Friend_Of_FriendBook, "include_str_list":["通讯录管理", "已添加", "已过期"]
                        }, 
                        {
                            "page_name":"通讯录页面", "page_type_code":PageType.FriendBook, "include_str_list":["录管理", "新的朋友", "群聊", "公众号"]
                        },
                        {
                            "page_name":"通讯录页面", "page_type_code":PageType.FriendBook, "include_str_list":["录管理", "新的朋友", "服务号"]
                        },
                        {
                            "page_name":"通讯录页面", "page_type_code":PageType.FriendBook, "include_str_list":["服务号", "企业微信联系人", "我的企业", "联系人"]
                        },
                        {
                            "page_name":"通讯录页面", "page_type_code":PageType.FriendBook, "include_str_list":["录管理", "群聊", "服务号", "我的企业"]
                        },
                        {
                            "page_name":"通讯录页面", "page_type_code":PageType.FriendBook, "include_str_list":["新的朋友", "公众号", "企业微信联系人", "联系人"]
                        },
                        {
                            "page_name":"通讯录页面", "page_type_code":PageType.FriendBook, "include_str_list":["群聊", "公众号", "服务号", "联系人"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["昵称", "微信号", "地区", "备注", "朋友圈"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["个性签名", "来源", "发消息", "语音聊天", "视频聊天"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["昵称", "地区",  "朋友圈", "来源", "语音聊天"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["微信号", "备注", "个性签名", "发消息", "视频聊天"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["地区", "备注", "来源", "发消息"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["昵称", "微信号", "朋友圈", "个性签名", "来源"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["微信号", "地区", "备注", "朋友圈", "个性签名"]
                        },
                        {
                            "page_name":"好友资料页", "page_type_code":PageType.Friend_Information, "include_str_list":["昵称", "微信号", "备注", "来源", "聊天"]
                        },
                        {
                            "page_name":"设置备注和标签", "page_type_code":PageType.Setting_Remark, "include_str_list":["设置备注和标签", "备注", "标签"]
                        }, 
                        {
                            "page_name":"设置备注和标签", "page_type_code":PageType.Setting_Remark, "include_str_list":["备注", "标签", "描述", "添加图片"]
                        },
                        {
                            "page_name":"设置备注和标签", "page_type_code":PageType.Setting_Remark, "include_str_list":["设置备注和标签", "备注", "描述", "添加图片"]
                        },
                        {
                            "page_name":"搜索到个人微信页", "page_type_code":PageType.Friend_Person_Exist, "include_str_list":["个人", "取消", "搜一搜", "小程序", "公众号"]
                        },
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "搜索无法找到该用户"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["搜索无法找到该用户", "请检查你填写的账号是否正确"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "请检查你填写的账号是否正确"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "账号", "异常"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "被搜", "状态"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "账号", "无法"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "状态", "无法", "显示"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["添加朋友", "被搜", "显示"]
                        }, 
                        {
                            "page_name":"该用户不存在", "page_type_code":PageType.Friend_No_Exist, "include_str_list":["账号", "状态", "异常"]
                        }, 
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["提醒谁看", "取消"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["提醒谁看", "公开"], "exclude_str_list":["私", "不给谁", "谁看"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["提醒", "看", "开", "取消"], "exclude_str_list":["私", "不给谁", "谁看"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["看", "公开", "取消"], "exclude_str_list":["私", "不给谁", "谁看"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["提醒", "看", "公", "取消"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["谁", "看", "公开", "取消"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["谁", "看", "一", "取消"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["提醒谁看", "发表", "取消"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["取消", "这一刻的想法"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈发表页", "page_type_code":PageType.Circle_Send, "include_str_list":["谁可以看", "发表", "取消"], "exclude_str_list":["私密", "不给谁"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["不给谁看", "公开", "私密"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["谁可以看", "公开", "私密", "谁可以看", "不给谁看"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["公开", "谁", "看", "不", "谁看"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":[("谁", 2), ("看", 2), "不"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["谁可以看", "公开", "确定", "取消"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["公开", "私密",  "谁可以看", "确定", "取消"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["谁可以看", "公开", "私密", "仅自己可见", "谁可以看", "不给谁看"]
                        },
                        {
                            "page_name":"朋友圈谁可以看页", "page_type_code":PageType.Circle_Who_Can_See, "include_str_list":["所有朋友可见", "私密", "谁可以看", "不给谁看", "取消"]
                        },
                        {
                            "page_name":"朋友圈选择朋友页", "page_type_code":PageType.Circle_Select_Frient, "include_str_list":["标签", "朋友"]
                        },
                        {
                            "page_name":"朋友圈选择朋友页", "page_type_code":PageType.Circle_Select_Frient, "include_str_list":["标签", "服友"]
                        },
                        {
                            "page_name":"朋友圈选择朋友页", "page_type_code":PageType.Circle_Select_Frient, "include_str_list":["标签", "股友"]
                        },
                        {
                            "page_name":"朋友圈选择朋友页", "page_type_code":PageType.Circle_Select_Frient, "include_str_list":["标签", "谁可以看"]
                        },
                        {
                            "page_name":"朋友圈选择朋友页", "page_type_code":PageType.Circle_Select_Frient, "include_str_list":["从群导入", "从标签导入"]
                        },
                        {
                            "page_name":"朋友圈拍照记录生活页", "page_type_code":PageType.Circle_Photo_Record, "include_str_list":["拍照", "记录生活", "你拍的照片", "你的朋友可以看到并且"]
                        },
                        {
                            "page_name":"朋友圈拍照记录生活页", "page_type_code":PageType.Circle_Photo_Record, "include_str_list":["你拍的照片", "你的朋友可以看到并且", "每个人只能看到自己朋友的评论", "我知道了"]
                        },
                        {
                            "page_name":"朋友圈拍照记录生活页", "page_type_code":PageType.Circle_Photo_Record, "include_str_list":["拍照", "记录生活", "每个人只能看到自己朋友的评论", "我知道了"]
                        },
                        {
                            "page_name":"朋友圈拍照记录生活页", "page_type_code":PageType.Circle_Photo_Record, "include_str_list":["拍照", "你拍的照片", "你的朋友可以看到并且", "我知道了"]
                        },
                        {
                            "page_name":"朋友圈拍照记录生活页", "page_type_code":PageType.Circle_Photo_Record, "include_str_list":["拍照,记录生活"]
                        },
                        {
                            "page_name":"朋友圈拍照记录生活页", "page_type_code":PageType.Circle_Photo_Record, "include_str_list":["拍照，记录生活"]
                        },
                        {
                            "page_name":"图片和视频页", "page_type_code":PageType.Img_And_Video, "include_str_list":["图片和视频", "预览"], "exclude_str_list":["通讯录", "发现", "我", "访问您设备上的", "媒体内容和文件"]
                        },
                        {
                            "page_name":"图片和视频页", "page_type_code":PageType.Img_And_Video, "include_str_list":["图片和视频", "完成"], "exclude_str_list":["通讯录", "发现", "我", "访问您设备上的", "媒体内容和文件"]
                        },
                        {
                            "page_name":"图片和视频页", "page_type_code":PageType.Img_And_Video, "include_str_list":["预览", "完成"], "exclude_str_list":["通讯录", "发现", "我", "访问您设备上的", "媒体内容和文件"]
                        },
                        {
                            "page_name":"图片和视频页", "page_type_code":PageType.Img_And_Video, "include_str_list":["预览", "原图"], "exclude_str_list":["通讯录", "发现", "我", "访问您设备上的", "媒体内容和文件"]
                        },
                        {
                            "page_name":"朋友圈页", "page_type_code":PageType.Circle, "include_str_list":["XXXXXXXXXXXXXXXXXXXXXXXXxXXXXXXXXXXXx"]
                        },
                        {
                            "page_name":"订阅号页", "page_type_code":PageType.Subscription, "include_str_list":["订阅号消息"], "exclude_str_list":["微信", "通讯录", "发现"]
                        },
                        {
                            # 注意: Windows微信的消息列表页,会话列表里天然有"服务通知"条目(前面有换行),
                            # 会被"\n服务通知"误判为服务通知页→误发ESC→微信主窗口响应ESC后消失→
                            # 截图全白→连续Unknow→触发"卡住"逻辑杀微信重启(死循环)。
                            # 消息列表页有"搜索"框,而真正的服务通知聊天页顶部只有标题无搜索框,以此区分。
                            "page_name":"服务通知页", "page_type_code":PageType.ServerNotice, "include_str_list":["\n<服务通知"], "exclude_str_list":["搜索"]
                        },
                        {
                            "page_name":"服务通知页", "page_type_code":PageType.ServerNotice, "include_str_list":["\n服务通知"], "exclude_str_list":["搜索"]
                        },
                        {
                            "page_name":"卡包页", "page_type_code":PageType.CardCag, "include_str_list":["\n<卡包\n"]
                        },
                        {
                            "page_name":"卡包页", "page_type_code":PageType.CardCag, "include_str_list":["\n卡包\n"]
                        },
                        {
                            "page_name":"卡包页", "page_type_code":PageType.CardCag, "include_str_list":["\n<卡包区\n"]
                        },
                        {
                            "page_name":"卡包页", "page_type_code":PageType.CardCag, "include_str_list":["\n卡包区\n"]
                        },
                        {
                            "page_name":"申请添加朋友", "page_type_code":PageType.ApplyAddFriend, "include_str_list":["申请添加朋友", "添加朋友申请", "设为常用申请语"]
                        },
                        {
                            "page_name":"申请添加朋友", "page_type_code":PageType.ApplyAddFriend, "include_str_list":["备注", "标签", "朋友权限", "聊天", "朋友圈", "微信运动"]
                        },
                        {
                            "page_name":"申请添加朋友", "page_type_code":PageType.ApplyAddFriend, "include_str_list":["申请添加朋友",  "设为常用申请语", "标签", "朋友权限"]
                        },
                        {
                            "page_name":"申请添加朋友", "page_type_code":PageType.ApplyAddFriend, "include_str_list":["添加朋友申请", "备注", "朋友权限", "朋友圈"]
                        },
                        {
                            "page_name":"公众号页", "page_type_code":PageType.OfficalAccount, "include_str_list":["\n<公众号"]
                        },
                        {
                            "page_name":"聊天信息页", "page_type_code":PageType.ChatInfo, "include_str_list":["聊天信息", "查找聊天记录", "置顶聊天", "聊天背景"]
                        },
                        {
                            "page_name":"聊天信息页", "page_type_code":PageType.ChatInfo, "include_str_list":["聊天信息", "查找聊天记录", "置顶聊天", "清空聊天记录"]
                        },
                        {
                            "page_name":"聊天信息页", "page_type_code":PageType.ChatInfo, "include_str_list":["查找聊天记录", "置顶聊天", "聊天背景", "清空聊天记录"]
                        }
                        
                      ]
# 页面类型检查
def do_page_type_check(text_of_screen):
    text_of_screen = text_of_screen.replace("（", "(").replace("）", ")")
    text_of_screen = text_of_screen.replace("", "")
    # 去除掉最上面的标题栏中的时间串 
    line_list_of_text = text_of_screen.split("\n")
    if len(line_list_of_text) > 1:
        first_line = line_list_of_text[0]
        has_colon_or_digit = any(ch in first_line for ch in ':0123456789')
        if has_colon_or_digit == True:
            line_list_of_text = line_list_of_text[1:]
            text_of_screen = "\n".join(line_list_of_text)
    
    # 先判断是不是异常的页面，如果是直接返回 
    except_code = do_exception_check(text_of_screen)  
    if except_code != APP_RET_CODE_SUCESS:
        return PageType.Except
    #         
    for page_info_dict in PAGE_INFO_DICT_LIST:
        page_name = page_info_dict["page_name"]
        include_str_list = page_info_dict["include_str_list"]
        max_character_count = -1
        if "max_character_count" in page_info_dict:
            max_character_count = page_info_dict["max_character_count"]
        exclude_str_list = []
        if "exclude_str_list" in page_info_dict:
            exclude_str_list = page_info_dict["exclude_str_list"]
        page_type_code = page_info_dict["page_type_code"]
        b_hitted = True
        # 判断字符数
        if max_character_count != -1:
            if len(text_of_screen) > max_character_count:
                continue 
        # 判断包含关键词        
        for item in include_str_list:
            if isinstance(item, str):
                include_str = item
                if include_str not in text_of_screen:
                    b_hitted = False
                    break
            elif isinstance(item, tuple):
                include_str = item[0]
                item_one = item[1]
                if isinstance(item_one, int):
                    include_count = item_one
                    count = text_of_screen.count(include_str)
                    if count < include_count:
                        b_hitted = False
                        break
                elif isinstance(item_one, str):
                    if item_one == "front":
                        index = text_of_screen.find(include_str)
                        if index == -1 or index > 20:
                            b_hitted = False
                            break
                    elif item_one == "back":
                        index = text_of_screen.rfind(include_str)
                        if index == -1 or index > 20:
                            b_hitted = False
                            break
        for exclude_str in exclude_str_list:
            if exclude_str in text_of_screen:
                b_hitted = False
                break
        if b_hitted == True:
            # chenyj debug
            print("{}".format(page_info_dict))

            if page_type_code == PageType.Chat:
                print("####检测到处于[{}]页面.文本:【{}】".format(page_name, text_of_screen))
            else:
                print("检测到处于[{}]页面".format(page_name))
            return page_type_code
    
    return PageType.Unknow
#text_of_screen = "6:16O雳分自\n<公众号Q三\n@贵阳网\n——Ml力\n′_ZL:dieiYY′\n公、,nP,“沥3\n\n“医宏t\nPo”1\n江=os1【失r助\n\n“aea.a\n\n孙-一\nEa\n\n胡忠雄出席贵阳贵安融入服务全国统一大市场建设座谈会\n\n@贵阳网\n\n贵阳公积金缴存基数调整!\n\n@SNsmien\n"
#do_page_type_check(text_of_screen)

# 判断现在是什么table页
def get_table_type(input_event):
    path = SCREENSHOT_SAVE_DIR + "/" + "img_of_tab" + ".png"
    #55 161 66 171 (x上加17，y加17 )
    bbox_tab_msg = (38+G_X_PIAN_YI, 144+G_Y_PIAN_YI, 49+G_X_PIAN_YI, 155+G_Y_PIAN_YI)
    bbox_tab_friend_book = (40+G_X_PIAN_YI, 225+G_Y_PIAN_YI, 48+G_X_PIAN_YI, 228+G_Y_PIAN_YI)
    bbox_tab_collect = (36+G_X_PIAN_YI, 29+G_Y_PIAN_YI, 55+G_X_PIAN_YI, 297+G_Y_PIAN_YI)
    iRet = adb_get_screen(path, bbox_tab_msg)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, False 

    if True == input_event.wait(0.1):
        print_my("get_table_page_type, 被要求退出1")
        return -1, False 
    
    # 判断是否是消息列表tab
    path_of_img_tab_msg = SCREENSHOT_SAVE_DIR + "/" + "img_of_tab_msg.png"
    img = Image.open(path)
    #print_my(bbox)
    cropped_img = img.crop(bbox_tab_msg)
    cropped_img.save(path_of_img_tab_msg) 
    if True == input_event.wait(0.1):
        print_my("get_table_page_type, 被要求退出2")
        return -1, False 
    ratio = calculate_green_area_ratio(path_of_img_tab_msg, "消息列表页")
    if ratio > 0.3:
        return APP_RET_CODE_SUCESS, PageType.Message_List

    # 判断是否是通讯录列表tab
    path_of_img_tab_friend_book = SCREENSHOT_SAVE_DIR + "/" + "img_of_tab_friend_book.png"
    img = Image.open(path)
    #print_my(bbox)
    cropped_img = img.crop(bbox_tab_friend_book)
    cropped_img.save(path_of_img_tab_friend_book) 
    if True == input_event.wait(0.1):
        print_my("get_table_page_type, 被要求退出3")
        return -1, False 
    ratio = calculate_green_area_ratio(path_of_img_tab_friend_book, "通讯录页")
    if ratio > 0.3:
        return APP_RET_CODE_SUCESS, PageType.FriendBook
    
    # 判断是否是收藏tab
    path_of_img_tab_collect = SCREENSHOT_SAVE_DIR + "/" + "img_of_tab_collect.png"
    img = Image.open(path)
    #print_my(bbox)
    cropped_img = img.crop(bbox_tab_collect)
    cropped_img.save(path_of_img_tab_collect) 
    if True == input_event.wait(0.1):
        print_my("get_table_page_type, 被要求退出4")
        return -1, False 
    ratio = calculate_green_area_ratio(path_of_img_tab_collect, "收藏页")
    if ratio > 0.3:
        return APP_RET_CODE_SUCESS, PageType.Collect
    
    return APP_RET_CODE_SUCESS, PageType.Unknow

# 获取错误码的名称
def get_error_code_name(error_code):
    """
    根据错误码值获取对应的常量名称
    :param error_code: 错误码值（整数）
    :return: 错误码名称（字符串），如果找不到则返回 "UNKNOWN_ERROR_CODE_{值}"
    """
    import error_code as ec
    # 遍历error_code模块的所有属性
    for name in dir(ec):
        if name.startswith('APP_RET_CODE_') or name.startswith('RET_'):
            try:
                value = getattr(ec, name)
                if isinstance(value, int) and value == error_code:
                    return name
            except:
                continue
    return f"UNKNOWN_ERROR_CODE_{error_code}"

# 开发模式：保存页面截图的辅助函数
def save_page_screenshot_in_dev_mode(path, page_type, log_prefix=""):
    """
    在开发模式下保存页面截图
    :param path: 截图文件路径
    :param page_type: 页面类型（PageType枚举）
    :param log_prefix: 日志前缀，用于区分不同的判断路径
    """
    if not g_b_Develop_Mode or path is None or page_type == PageType.Unknow or page_type == PageType.Except:
        return
    
    try:
        # 创建page_img文件夹（如果不存在）
        page_img_dir = os.path.join(SCREENSHOT_SAVE_DIR, "page_img")
        if not os.path.exists(page_img_dir):
            os.makedirs(page_img_dir)
        
        # 获取页面类型名称
        page_type_name = page_type.name
        # 生成带时间戳的文件名（避免覆盖）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_filename = f"page_{page_type_name}_{timestamp}.png"
        saved_path = os.path.join(page_img_dir, saved_filename)
        
        # 复制原图片
        shutil.copy(path, saved_path)
        
        # 输出日志
        prefix = f"[开发模式{log_prefix}]" if log_prefix else "[开发模式]"
        print_my(f"{prefix} 保存页面截图：{page_type_name} -> page_img/{saved_filename}")
    except Exception as e:
        prefix = f"[开发模式{log_prefix}]" if log_prefix else "[开发模式]"
        print_my(f"{prefix} 保存页面截图失败：{e}")
    
# 使用tesseract判断当前页面的类型
def get_page_type_by_tesseract(input_event):
    global g_table
    text_return = ""
    page_type_return = PageType.Unknow
    path = None  # 初始化path变量

    # 1.通过Windows判断
    iRet, page_type_return = get_page_type_by_windows(input_event, g_table.rightPanelWin)
    if iRet == APP_RET_CODE_SUCESS:
        if page_type_return == PageType.Circle:
            # 再用文字检查一遍
            path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_get_page_type_by_tesseract" + ".png"
            if True == os.path.exists(path):
                os.remove(path)
            iRet = adb_get_screen(path)
            if iRet != APP_RET_CODE_SUCESS:
                # 截图失败（如微信窗口暂未找到），视为设备未就绪，避免OCR报"图片文件不存在"
                return APP_RET_CODE_NO_READY, page_type_return, text_return

            # chenyj test
            #path = SCREENSHOT_SAVE_DIR + "/" + "test" + ".png"
            if True == input_event.wait(0.1):
                print("get_page_type_by_tesseract, 被要求退出1")
                return APP_RET_CODE_ZHU_DONG_EXIT, page_type_return, text_return
            iRet, text_return = get_ocr_result_with_small_my(path)
            # 如果是因为设备没有准备好导致截图失败，那么先认为没有异常
            if iRet == APP_RET_CODE_NO_READY:
                return APP_RET_CODE_SUCESS, page_type_return, text_return
            if iRet != APP_RET_CODE_SUCESS:
                return iRet, page_type_return, text_return    
            # 检查是否异常
            page_type_return_ = do_page_type_check(text_return)
            if page_type_return_ == PageType.Circle_Send:
                page_type_return = PageType.Circle_Send
        
        # 开发模式：保存页面截图
        save_page_screenshot_in_dev_mode(path, page_type_return, "-Tesseract-Win")
        
        return iRet, page_type_return, text_return

    # 2.通过文字判断
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_get_page_type_by_tesseract" + ".png"
    if True == os.path.exists(path):
        os.remove(path)
    iRet = adb_get_screen(path)
    if iRet != APP_RET_CODE_SUCESS:
        # 截图失败（如微信窗口暂未找到），视为设备未就绪，避免OCR报"图片文件不存在"
        return APP_RET_CODE_NO_READY, page_type_return, text_return

    # chenyj test
    #path = SCREENSHOT_SAVE_DIR + "/" + "test" + ".png"
    if True == input_event.wait(0.1):
        print("get_page_type_by_tesseract, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, page_type_return, text_return
    iRet, text_return = get_ocr_result_with_small_my(path)
    # 如果是因为设备没有准备好导致截图失败，那么先认为没有异常
    if iRet == APP_RET_CODE_NO_READY:
        return APP_RET_CODE_SUCESS, page_type_return, text_return
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, page_type_return, text_return    
    # 检查是否异常
    page_type_return = do_page_type_check(text_return)
    
    # 3.使用table颜色判断
    if page_type_return == PageType.Unknow:
        iRet, tab_type = get_table_type(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            return iRet, page_type_return, text_return
        if tab_type == PageType.Message_List:
            iRet, type_page, b_is_groud, user_name_of_chat = get_page_type_by_title()
            if iRet == APP_RET_CODE_SUCESS:
                if type_page == PageType.Chat or len(user_name_of_chat) == 0:
                    # 开发模式：保存Chat页面截图
                    save_page_screenshot_in_dev_mode(path, PageType.Chat, "-Tesseract-Table")
                    return iRet, PageType.Chat, text_return
            # 开发模式：保存Message_List页面截图
            save_page_screenshot_in_dev_mode(path, PageType.Message_List, "-Tesseract-Table")
            return iRet, PageType.Message_List, text_return
        elif tab_type == PageType.FriendBook:
            # 开发模式：保存FriendBook页面截图
            save_page_screenshot_in_dev_mode(path, PageType.FriendBook, "-Tesseract-Table")
            return iRet, PageType.FriendBook, text_return
        elif tab_type == PageType.Collect:
            # 开发模式：保存Collect页面截图
            save_page_screenshot_in_dev_mode(path, PageType.Collect, "-Tesseract-Table")
            return iRet, PageType.Collect, text_return
    if page_type_return == PageType.Unknow:
        print_my("####检测到处于[{}]页面.文本:【{}】".format("未知", text_return))
    else:
        # 开发模式：保存页面截图
        save_page_screenshot_in_dev_mode(path, page_type_return, "-Tesseract")
        
    return APP_RET_CODE_SUCESS, page_type_return, text_return
#iRet, page_type_return, text_return = get_page_type_by_tesseract(g_Event_test)

# 使用OCR判断当前页面的类型
def get_page_type_by_ocr(input_event):
    text_return = ""
    page_type_return = PageType.Unknow
    
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_get_page_type_by_ocr" + ".png"
    if True == os.path.exists(path):
        os.remove(path)
    adb_get_screen(path)
    
    # chenyj test
    #path = SCREENSHOT_SAVE_DIR + "/" + "test" + ".png"
    if True == input_event.wait(0.1):
        print("get_page_type_by_ocr, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, page_type_return, text_return
    
    text_return = ""
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        for result in json_return["words_result"]:
            content = result["words"]
            text_return += content
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!get_page_type_by_ocr get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, page_type_return, text_return
    if json_return is None: 
        print_my("!!!!!get_page_type_by_ocr, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR, page_type_return, text_return

    # 检查是否异常
    page_type_return = do_page_type_check(text_return)
    if page_type_return == PageType.Unknow:
        print_my("####检测到处于[{}]页面.文本:【{}】".format("未知", text_return))
    else:
        # 开发模式：保存页面截图
        save_page_screenshot_in_dev_mode(path, page_type_return, "-OCR")
 
    return APP_RET_CODE_SUCESS, page_type_return, text_return
#iRet, page_type_return, text_return = get_page_type_by_ocr(g_Event_test)

# 判断是否在某个页面
def is_in_page(input_event, page_type_expect_list = [PageType.Unknow], i_check_count = 2):
    i_count = 0
    page_type_return = PageType.Unknow
    text_return = ""

    while i_count < i_check_count:
        i_count += 1
        if i_count < 2:
            iRet, page_type_return, text_return = get_page_type_by_tesseract(input_event)
        else:
            iRet, page_type_return, text_return = get_page_type_by_ocr(input_event)
            
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                return APP_RET_CODE_ZHU_DONG_EXIT, page_type_return
            continue
        if page_type_return in page_type_expect_list:
            return APP_RET_CODE_SUCESS, page_type_return
        
        if True == input_event.wait(1):
            print_my("is_in_page, 被要求退出")
            return APP_RET_CODE_ZHU_DONG_EXIT, page_type_return
        
        continue    
    if page_type_return in page_type_expect_list:
        return APP_RET_CODE_SUCESS, page_type_return
    print(f"【\n{text_return}\n】")    
    return APP_RET_CODE_UNKNOW, page_type_return

# 确保是在消息列表页面    
def ensure_in_message_list_page(input_event, page_type_now = PageType.Unknow):
    text_return = ""
    
    # 粗略判断
    if page_type_now == PageType.Unknow:
        iRet, page_type_return, text_return = get_page_type_by_tesseract(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            return iRet
        if page_type_return in [PageType.Message_List, PageType.Chat]:
            print("粗略判断，当前是在消息列表页或聊天页")
            return APP_RET_CODE_HAS_IN_EXPECT_PAGE
    else:
        page_type_return = page_type_now
        
    # 复位到消息列表页
    if page_type_return == PageType.Chat:
        adb_click_back_with_check(input_event, 1) 
    elif page_type_return in [PageType.FriendBook, PageType.New_Friend_Of_FriendBook, PageType.Friend_Information, PageType.Discover, PageType.Collect, PageType.Me]:
        adb_click_message_list_table_btn() 
    elif page_type_return == PageType.Friend_No_Exist:
        adb_click_close_add_to_friendbook_when_no_exist_btn()
    elif page_type_return == PageType.Friend_Person_Exist:
        adb_click_back_with_check(input_event, 2)
    elif page_type_return == PageType.Img_And_Video:
        adb_click_back_with_check(input_event, 2)
    elif page_type_return == PageType.Add_to_FriendBook:
        adb_click_close_add_to_friendbook_btn()
    elif page_type_return == PageType.Tag:
        adb_click_back_with_check(input_event, 1, 0.994)
        adb_click_message_list_table_btn() 
    elif page_type_return == PageType.Tag_Empty:
        adb_click_back_with_check(input_event, 1, 0.994)
        adb_click_message_list_table_btn() 
    elif page_type_return == PageType.Circle:
        adb_click_close_circle_btn()
        adb_click_message_list_table_btn()
    elif page_type_return == PageType.Circle_Send:
        adb_click_close_circle_send_btn()   
        adb_click_close_circle_btn() 
        adb_click_message_list_table_btn()
    elif page_type_return == PageType.Circle_Who_Can_See:
        adb_click_close_who_can_see_btn()   
        adb_click_close_circle_btn() 
        adb_click_message_list_table_btn()
    elif page_type_return == PageType.Circle_Select_Frient:
        adb_click_close_select_who_can_see_btn()
        adb_click_close_who_can_see_btn()   
        adb_click_close_circle_btn() 
        adb_click_message_list_table_btn()
    elif page_type_return == PageType.Circle_Photo_Record:
        adb_click_back_with_check(input_event, 2)
        adb_click_message_list_table_btn()
    elif page_type_return == PageType.Add_Frient:
        adb_click_back_with_check(input_event, 1) 
        adb_click_message_list_table_btn()
    elif page_type_return == PageType.Search:
        adb_click_back_with_check(input_event, 1, 0.995)
    elif page_type_return == PageType.Add_to_FriendBook_OTHER_ZHU_DONG:
        adb_click_back_with_check(input_event, 2, 0.995)
        adb_click_message_list_table_btn() 
    elif page_type_return == PageType.Setting:
        adb_click_close_setting_btn()
    elif page_type_return == PageType.Setting_New_message_notice:
        adb_click_back_with_check(input_event, 2) 
        ensure_in_message_list_page(input_event)
    elif page_type_return == PageType.Setting_Remark:
        adb_click_back_with_check(input_event, 4) 
    elif page_type_return == PageType.Subscription:
        adb_click_back_with_check(input_event, 1) 
    elif page_type_return == PageType.GroupInfo:
        adb_click_back_with_check(input_event, 2)
        adb_click_back_with_check(input_event, 1, 0.995)
    elif page_type_return == PageType.GroupMember:
        adb_click_back_with_check(input_event, 3)
        adb_click_back_with_check(input_event, 1, 0.995)
    elif page_type_return == PageType.ServerNotice:
        adb_click_back_with_check(input_event, 1)
    elif page_type_return == PageType.CardCag:
        adb_click_back_with_check(input_event, 1)
        adb_click_message_list_table_btn() 
    elif page_type_return == PageType.ApplyAddFriend:
        adb_click_close_apply_add_btn(input_event)
        time.sleep(1.5)
        adb_click_close_add_to_friendbook_btn()
        ensure_in_message_list_page(input_event)
    elif page_type_return == PageType.OfficalAccount:
        adb_click_back_with_check(input_event, 1)
    elif page_type_return == PageType.ChatInfo:
        adb_click_back_with_check(input_event, 2)
    else:
        print_my("####未知的页面类型.【{}】".format(text_return))
        return APP_RET_CODE_UNKNOW
    """
    elif page_type_return in [PageType.TaskCenter_List, PageType.TaskCenter_First]:
        adb_click_back_with_check(input_event, 1)
    else:
        adb_click_back_with_check(input_event, 1)
    """
    return APP_RET_CODE_SUCESS
#ensure_in_message_list_page(g_Event_test)

def enter_message_list_page():
    iRet, type_page, b_is_groud, user_name_of_chat = get_page_type_by_title()
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    if type_page in [PageType.Message_List, PageType.Chat, PageType.FriendBook, PageType.Friend_Information, PageType.Discover, PageType.Me]:
        adb_click_message_list_table_btn()
    elif type_page == PageType.Chat:
    
        i_return = adb_click_back_of_chat_with_check(g_Event_test)
        if i_return != 0:
            return i_return
            
        adb_click_message_list_table_btn()
    time.sleep(1)
    return APP_RET_CODE_SUCESS
#enter_message_list_page()

# 判断是不是“最近"页
def is_recent_page():   
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_rectent_bottom" + ".png"
    get_screen_of_recent_bottom(path)
    try:
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!is_recent_page,get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        return type_return, user_name_of_chat
    if json_return is None: 
        print_my("!!!!!is_recent_page, get_ocr_result_with_small 失败")
        return type_return, user_name_of_chat
    # chenyj debug
    #print_my(json_return["words_result"])
    for result in json_return["words_result"]:
        content = result["words"]
        if ("微信" in content and ("(" in content or "（" in content) and (")" in content or "）" in content)) or "微信" == content:
            return True  
    return False

# adb点击微信按钮(用于返回消息列表页) 
def adb_click_back_wei_xin_btn():
    print("动作:【点击微信按钮】(用于返回消息列表页) ")
    adb_click(int(507/W_SCREEN*g_w_screen), int(1858/H_SCREEN*g_h_screen))
    time.sleep(1.0)     
    return 
#if is_recent_page() == True:
#    adb_click_back_wei_xin_btn()
 
def adb_click_back_wei_xin_btn_with_check():
    image_check_begin()
    adb_click_back_wei_xin_btn()
    time.sleep(0.5)
    iRet, bChange = image_check_end()
    if iRet == 0 and bChange == False:
        return APP_RET_CODE_APP_KA_ZHU
    return APP_RET_CODE_SUCESS
    
# 进入消息列表页的第一页
def enter_message_first(input_event):
    TIME_BEGIN()
    # 先回到消息列表页
    iRet = enter_message_list_page()
    if iRet != APP_RET_CODE_SUCESS:
        TIME_END()
        return iRet
        
    TRY_COUNT_MAX = 6
    i_try_count = 0
    while i_try_count < TRY_COUNT_MAX:
        i_try_count += 1
        adb_slide_friend_chat_list_up()
        if True == input_event.wait(0.5):
            print_my("enter_message_first, 被要求退出")
            TIME_END()
            return APP_RET_CODE_ZHU_DONG_EXIT 
        # 判断现在是不是“最近”页
        if is_recent_page() == True:
            # chenyj debug
            print("当前是在\"最近\"页")
            i_return = adb_click_back_wei_xin_btn_with_check()
            if i_return != 0:
                TIME_END()
                return i_return
            if True == input_event.wait(1):
                print_my("enter_message_first, 被要求退出2")
                TIME_END()
                return APP_RET_CODE_ZHU_DONG_EXIT 
            TIME_END()
            return APP_RET_CODE_SUCESS
    TIME_END()
    return APP_RET_CODE_UNKNOW 
#enter_message_first(g_Event_test)          

# 获得第一页中所有用户的昵称
def get_username_list_of_first_page(input_event, b_in_need_check_is_firstpage = True):
    global g_i_crop_count
    global g_object_info_of_can_deposit_dict
    # chenyj debug
    print("===>get_username_list_of_first_page") 
    username_list = []
    
    # 先把上一次的对象信息清除掉
    g_object_info_of_can_deposit_dict.clear()
    
    # 进入会话列表页的第一页
    if b_in_need_check_is_firstpage == True:
        iRet = enter_message_first(input_event)
        if iRet < 0:
            return iRet, username_list
        if iRet == 1:
            print_my("!!!!无找进入消息列表第1页")
            return 2, username_list
    
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list" + ".png"
    get_screen_of_friend_chat_list(path)
    try:
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!get_username_list_of_first_page， get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, username_list
    if json_return is None: 
        print_my("!!!!!get_username_list_of_first_page, get_ocr_result_with_small失败")
        return APP_RET_CODE_OCR_ERROR, username_list
    # 在好友列表中找到指定的好友
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        
        try:
            img = Image.open(path)
            bbox = (x, y, x + width, y + height)
            cropped_img = img.crop(bbox)
            g_i_crop_count += 1
            # chenyj test
            #crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_{}.png".format(g_i_crop_count)
            crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp.png"
            cropped_img.save(crop_path)
            crop_mage = imread(crop_path)
            # chenyj debug
            #print("g_i_crop_count:{}, content:{}".format(g_i_crop_count, content))
        except Exception as e:
            print("!!!!get_username_list_of_first_page, 出现异常:{}".format(e))
            continue 
        if True == image_is_black(crop_mage):
            _, content = username_standard(content)
            username_list.append(content)
                    
            # 顺便把新消息区域也记录下来
            x_of_lt = result["location"]["left"]
            y_of_lt = result["location"]["top"]
            x_of_middle = result["location"]["left"] + int(result["location"]["width"]/2)
            y_of_middle = result["location"]["top"] + int(result["location"]["height"]/2)
 
            # 加上偏移 
            x_of_lt = g_friend_chat_list_x + x_of_lt
            y_of_lt = g_friend_chat_list_y + y_of_lt
            x_of_middle = g_friend_chat_list_x + x_of_middle    
            y_of_middle = g_friend_chat_list_y + y_of_middle
            
            
            lt_x_of_new_msg = x_of_lt-int(15/W_SCREEN*g_w_screen) 
            lt_y_of_new_msg = y_of_lt-int(15/H_SCREEN*g_h_screen) 
            rb_x_of_new_msg = lt_x_of_new_msg + int(18/W_SCREEN*g_w_screen) 
            rb_y_of_new_msg = lt_y_of_new_msg + int(18/H_SCREEN*g_h_screen)
            rect_of_new_msg = [lt_x_of_new_msg, lt_y_of_new_msg, rb_x_of_new_msg, rb_y_of_new_msg]
            g_object_info_of_can_deposit_dict[content] = {}
            g_object_info_of_can_deposit_dict[content]["rect_of_new_msg"] = rect_of_new_msg
    # chenyj debug    
    print("<===get_username_list_of_first_page, 昵称列表:{}".format(username_list))     
    
    return RET_SUCESS, username_list
#get_username_list_of_first_page(g_Event_test, False)

# 获得某用户的新消息通知区域
def get_monitor_rect_of_new_msg(input_event, username_list, b_in_need_check_is_firstpage = True, b_need_clear = True):
    global g_monitor_object_info_dict
    global g_object_info_of_can_deposit_dict
    # chenyj debug
    print("===>get_monitor_rect_of_new_msg, 昵称:{}".format(username_list)) 
    # 先把上一次的对象信息清除掉
    if b_need_clear == True:
        g_monitor_object_info_dict.clear()
    
    # 进入会话列表页的第一页
    if b_in_need_check_is_firstpage == True:
        iRet = enter_message_first(input_event)
        if iRet < 0:
            return iRet, ""
        if iRet == 1:
            print_my("!!!!无找进入消息列表第1页")
            return 2, ""
     
    # 获得截图的文本
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list" + ".png"
    get_screen_of_friend_chat_list(path)
    try:
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!get_monitor_rect_of_new_msg， ocr_return_has_location, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, ""
    if json_return is None: 
        print_my("!!!!!get_monitor_rect_of_new_msg, ocr_return_has_location失败")
        return APP_RET_CODE_OCR_ERROR, ""
            
    for dst_username in username_list:
        _, dst_username = username_standard(dst_username)
 
        #  如果历史中可以找到就使用历史的
        if dst_username in g_object_info_of_can_deposit_dict:
            if dst_username not in g_monitor_object_info_dict:
                g_monitor_object_info_dict[dst_username] = {}
            g_monitor_object_info_dict[dst_username]["rect_of_new_msg"] = g_object_info_of_can_deposit_dict[dst_username]["rect_of_new_msg"]
            # chenyj debug
            print("get_monitor_rect_of_new_msg, [{}]直接使用历史的区域".format(dst_username))
        else: 
            x_of_lt, y_of_lt, x_of_middle, y_of_middle = find_username_location(dst_username, json_return)
            if x_of_middle == -1 or y_of_middle == -1:
                if dst_username in g_monitor_object_info_dict:
                    del g_monitor_object_info_dict[dst_username]
                    print(f"<===get_monitor_rect_of_new_msg,     !!!!找不到此用户[{dst_username}]啊,把它从列表里去掉")
                continue
                #print_my(f"    !!!!找不到此用户[{dst_username}]啊")
                #return APP_RET_CODE_NO_FOUND, dst_username

            print("   微信用户[{}]的新消息区域锚定成功 {}*{}".format(dst_username, x_of_lt, y_of_lt))
            
            #lt_x_of_new_msg = x_of_lt-int(30/W_SCREEN*g_w_screen) 
            lt_x_of_new_msg = int(77/W_SCREEN*g_w_screen) 
            lt_y_of_new_msg = y_of_lt-int(15/H_SCREEN*g_h_screen) 
            rb_x_of_new_msg = lt_x_of_new_msg + int(27/W_SCREEN*g_w_screen) 
            rb_y_of_new_msg = lt_y_of_new_msg + int(27/H_SCREEN*g_h_screen)
            rect_of_new_msg = [lt_x_of_new_msg, lt_y_of_new_msg, rb_x_of_new_msg, rb_y_of_new_msg]
            if dst_username not in g_monitor_object_info_dict:
                g_monitor_object_info_dict[dst_username] = {}
            g_monitor_object_info_dict[dst_username]["rect_of_new_msg"] = rect_of_new_msg
    # chenyj debug    
    print("<===get_monitor_rect_of_new_msg, 获得新消息区域成功。昵称列表:{}".format(username_list))     
    
    return RET_SUCESS, ""
#get_monitor_rect_of_new_msg(g_Event_test, ["忠宁爸爸"])

# 获得锚定成功的用户列表
def get_mao_ding_username_list():
    username_list_mao_ding = []
    for username in g_monitor_object_info_dict:
        username_list_mao_ding.append(username)
    return username_list_mao_ding
    
# 判断某用户是否有新消息 
def check_has_new_msg(input_event, dst_username):
    global g_monitor_object_info_dict
    
    _, dst_username = username_standard(dst_username) 
    if dst_username not in g_monitor_object_info_dict:
        #print_my("!!!!无法找到此用户[{}]的新消息区域啊".format(dst_username))
        #upload_snape()
        #return APP_RET_CODE_NO_FOUND, False
        return APP_RET_CODE_SUCESS, False
        
      
    #path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list" + ".png"
    #get_screen_of_friend_chat_list(path)
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_check_has_new_msg" + ".png"
    rect_of_new_msg = g_monitor_object_info_dict[dst_username]["rect_of_new_msg"]  
    bbox = (rect_of_new_msg[0], rect_of_new_msg[1], rect_of_new_msg[2], rect_of_new_msg[3])
    iRet = adb_get_screen(path, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, False 

    if True == input_event.wait(0.1):
        print_my("check_has_new_msg, 被要求退出1")
        return -1, False 
    
    path_of_img_new_msg = SCREENSHOT_SAVE_DIR + "/" + "img_of_new_msg_{}".format(dst_username) + ".png"
    img = Image.open(path)
    #print_my(bbox)
    cropped_img = img.crop(bbox)
    cropped_img.save(path_of_img_new_msg) 
    
    if True == input_event.wait(0.1):
        print_my("check_has_new_msg, 被要求退出2")
        return -1, False 
        
    #path_of_img_new_msg = SCREENSHOT_SAVE_DIR + "/" + "img_of_new_msg_有消息" + ".png"
    ratio = calculate_red_area_ratio(path_of_img_new_msg)
    if ratio > NEW_MSG_RATIO:
        return 0, True
    return 0, False
"""
username = "忠宁爸爸"
_, bHas = check_has_new_msg(g_Event_test, username)
if bHas == True:
    print_my("用户【{}】有新消息".format(username))
else:
    print_my("用户【{}】没有新消息".format(username))
"""
    
# 判断是否有加好友请求 
def check_has_new_pass(input_event):
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_check_has_pass" + ".png"
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (47, 198, 71, 215)
    else:
        bbox = (415, 1843, 442, 1868)
    
    iRet = adb_get_screen(path, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, False 

    if True == input_event.wait(0.1):
        print_my("check_has_new_pass, 被要求退出1")
        return APP_RET_CODE_APP_KA_ZHU, False 
    
    path_of_img_new_pass = SCREENSHOT_SAVE_DIR + "/" + "img_of_new_pass_mointor" + ".png"
    img = Image.open(path)  
    #print_my(bbox)
    cropped_img = img.crop(bbox)
    cropped_img.save(path_of_img_new_pass) 
    
    if True == input_event.wait(0.1):
        print_my("check_has_new_pass, 被要求退出2")
        return APP_RET_CODE_APP_KA_ZHU, False 
        
    ratio = calculate_red_area_ratio(path_of_img_new_pass)
    if ratio > NEW_PASS_RATIO:
        return APP_RET_CODE_SUCESS, True
    return APP_RET_CODE_SUCESS, False
"""
_, bHas = check_has_new_pass(g_Event_test)
if bHas == True:
    print("有新加友请求")
else:
    print("没有新加友请求")
"""

# 进入某个用户的聊天页面
def enter_chat_ui(input_event, dst_username):
    global g_monitor_object_info_dict
    
    b_is_groud = False 
    
    TIME_BEGIN()
    _, dst_username = username_standard(dst_username)
    # 判断不是已经在这个聊天页面了 
    iRet, type_return, b_is_groud, user_name_of_chat = get_page_type_by_title()
    if iRet == APP_RET_CODE_SUCESS and type_return == PageType.Chat and user_name_of_chat == dst_username:
        print(f"!!!当前已经是在【{dst_username}】的聊天页面了")
        return APP_RET_CODE_SUCESS, b_is_groud
    # chenyj debug
    print("===>enter_chat_ui, 对方昵称:{}".format(dst_username))
    
    #### 模式一:全列表找
    """
    # 先回到消息列表页
    enter_message_list_page()
    if is_weChat_running() == False:
        print_my("微信应用退出了")
        return APP_RET_CODE_APP_EXIT
            
    # 先把列表滚到底部 
    adb_slide_friend_chat_list_down()
    if True == input_event.wait(0.5):
        print_my("enter_chat_ui, 被要求退出")
        return -1 
    if is_weChat_running() == False:
        print_my("微信应用退出了")
        return APP_RET_CODE_APP_EXIT
        
    adb_slide_friend_chat_list_down()
    if True == input_event.wait(0.5):
        print_my("enter_chat_ui, 被要求退出")
        return -1 
    if is_weChat_running() == False:
        print_my("微信应用退出了")
        return APP_RET_CODE_APP_EXIT
        
    adb_slide_friend_chat_list_down()
    if True == input_event.wait(0.5):
        print_my("enter_chat_ui, 被要求退出")
        return -1 
    adb_slide_friend_chat_list_down()
    if True == input_event.wait(0.5):
        print_my("enter_chat_ui, 被要求退出")
        return -1 
    if is_weChat_running() == False:
        print_my("微信应用退出了")
        return APP_RET_CODE_APP_EXIT      
    
    # 找到此用户在聊天列表中的哪个位置 
    x1 = -1
    y1 = -1
    MAX_COUNT = 6
    i_gun_count = 0
    while i_gun_count < MAX_COUNT:
        i_gun_count += 1
        _, _, x1, y1 = find_username_location(dst_username)
        if x1 == -1 or y1 == -1:
            adb_slide_friend_chat_list_up()
            if True == input_event.wait(0.5):
                print_my("enter_chat_ui, 被要求退出")
                return -1 
            continue
        break
    """
    ### 模式二：只找第一页,然后每次都OCR
    """
    _, _, x1, y1 = find_username_location(dst_username)
    if x1 == -1 or y1 == -1:
        iRet = enter_message_first(input_event)
        if iRet < 0:
            TIME_END()
            return iRet, b_is_groud
        if iRet == 1:
            print_my("无找进入消息列表第1页")
            TIME_END()
            return 2, b_is_groud
        
    _, _, x1, y1 = find_username_location(dst_username)
    if x1 == -1 or y1 == -1:
        print_my(f"    找不到此用户[{dst_username}]啊")
        TIME_END()
        return APP_RET_CODE_NO_FOUND, b_is_groud

    print_my("   找到的了微信用户[{}]".format(dst_username))
    """
    ### 模式三：复用初始化时的新消息位置 
    if dst_username not in g_monitor_object_info_dict:
        print("    !!!!enter_chat_ui，找不到此用户[{}]啊，{}".format(dst_username, g_monitor_object_info_dict))
        TIME_END()
        return APP_RET_CODE_NO_FOUND, b_is_groud
    rect_of_new_msg = g_monitor_object_info_dict[dst_username]["rect_of_new_msg"]  
    x1 = rect_of_new_msg[0]
    y1 = rect_of_new_msg[3]
        
    # 点击进入此用户的聊天界面 
    # chenyj debug
    print("动作:【点击此用户】")
    adb_click(x1, y1)
    
    # 等待进入聊天界面
    i_try_count = 0
    while i_try_count < TRY_COUNT_MAX_FOR_CHAT:
        i_try_count += 1
        if True == input_event.wait(1.5):
        #if True == input_event.wait(0.5):
            print_my("enter_chat_ui, 被要求退出1")
            TIME_END()
            ensure_in_message_list_page(input_event)
            return -1, b_is_groud

        # 策略1：再检查一遍，确保进入此聊天界面了
        #"""
        iRet, type_return, b_is_groud, user_name_of_chat = get_page_type_by_title()
        if iRet != APP_RET_CODE_SUCESS:
            TIME_END()
            ensure_in_message_list_page(input_event)
            return iRet, b_is_groud
        if type_return == PageType.Chat and not (dst_username == user_name_of_chat or user_name_of_chat[:-1] in dst_username): 
            # chenyj debug
            print("!!!!进入非期待的聊天页面.期待:[{}]，却是:[{}]".format(dst_username, user_name_of_chat))
            ensure_in_message_list_page(input_event)
            return APP_RET_CODE_UNEXPECT_CHAT_PAGE, b_is_groud
        if (type_return == PageType.Chat and (dst_username == user_name_of_chat or user_name_of_chat[:-1] in dst_username)):
            break
        #"""
        # 策略2：直接认为成功了
        """
        if "b_is_groud" not in g_monitor_object_info_dict[dst_username]:
            iRet, type_return, b_is_groud, user_name_of_chat = get_page_type_by_title()
            if iRet != APP_RET_CODE_SUCESS:
                TIME_END()
                return iRet, b_is_groud
            if type_return == PageType.Chat and not (dst_username == user_name_of_chat or user_name_of_chat[:-1] in dst_username):
                return APP_RET_CODE_UNEXPECT_CHAT_PAGE, b_is_groud
            if (type_return == PageType.Chat and (dst_username == user_name_of_chat or user_name_of_chat[:-1] in dst_username)):
                g_monitor_object_info_dict[dst_username]["b_is_groud"] = b_is_groud
                break
        else:
            b_is_groud = g_monitor_object_info_dict[dst_username]["b_is_groud"]
            break
        """
            
        if i_try_count >= TRY_COUNT_MAX_FOR_CHAT:
            # chenyj debug
            print("!!!!确认没有进入【{}】的聊天界面".format(dst_username))
            upload_snape()
            TIME_END()
            ensure_in_message_list_page(input_event)
            return 3, b_is_groud
            
        # chenyj debug
        print("还没进入聊天页面，请稍等...")
        continue
    # chenyj debug
    print("<===enter_chat_ui, 对方昵称:{}".format(dst_username))  
    TIME_END()
    return 0, b_is_groud 
#enter_chat_ui(g_Event_test, "文件传输")

def chunk_string(s, chunk_size=30):
    return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]
    
def adb_install_adb_keyboard():
    cmd = LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} install {LEI_DIAN_DIR}/ADBKeyBoard.apk"
    subprocess.run(cmd, creationflags=g_process_creationflags)
    time.sleep(0.03)
#adb_install_adb_keyboard()

# 设置adb输入法
def adb_set_adb_ime():
    cmd = LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell ime enable com.android.adbkeyboard/.AdbIME"
    subprocess.run(cmd, creationflags=g_process_creationflags)
    time.sleep(0.03)
    cmd = LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell ime set com.android.adbkeyboard/.AdbIME"
    subprocess.run(cmd, creationflags=g_process_creationflags)
    time.sleep(0.2)
    print("动作:【设置adb输入法】")
#adb_set_adb_ime()

# 取消设置adb输入法
def adb_unset_adb_ime():
    cmd = LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell ime reset"
    subprocess.run(cmd, creationflags=g_process_creationflags)
    time.sleep(0.03)
    print("动作:【取消设置adb输入法】")
    
def adb_paste_text(text, b_debug = False):
    TIME_BEGIN()   
    # 将长文件拆开多次
    # 因为： 
    # 在Android系统中，属性名称的长度不能超过31个字符，属性值的长度不能超过91个字符。
    # 如果超出这个长度，就可能无法成功设置属性。
    chunks = chunk_string(text)
    # chenyj debug
    print("切分为:")
    for i, chunk in enumerate(chunks):
        print("【{}】{}".format(i, chunk))
    print("\n")

    #adb_set_adb_ime()
    for chunk in chunks:
        # 为粘贴成功，对里面的空格及tab键处理
        #chunk = chunk.replace("   ", "\t")
        #chunk = chunk.replace(" ", "\ ")
        #chunk = chunk.replace("\n", "\\n")
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            cmd = "{}/adb.exe {} shell setprop call.input \"'{}'\"".format(LEI_DIAN_DIR, DEVICE_CMD, chunk)
            subprocess.run(cmd, creationflags=g_process_creationflags) 
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
            windows_paste_text(chunk)
        else:
            # 使能输入中文
            # https://github.com/senzhk/ADBKeyBoard
            # adb install ADBKeyBoard.apk   (把 ADBKeyBoard.apk放在和adb.exe同一目录下)
            # adb shell ime enable com.android.adbkeyboard/.AdbIME
            # adb shell ime set com.android.adbkeyboard/.AdbIME   
            # 恢复手机里默认的输入法 
            # adb shell ime reset
            #cmd = "{}/adb.exe {} shell service call clipboard 2 i32 1 i32 0 s16 '{}'".format(LEI_DIAN_DIR, DEVICE_CMD, chunk) # 英文也不行
            #cmd = "{}/adb.exe {} shell input text \"'{}'\"".format(LEI_DIAN_DIR, DEVICE_CMD, chunk)  # 英文可以
            #cmd = "{}/adb.exe {} shell setprop call.input \"'{}'\"".format(LEI_DIAN_DIR, DEVICE_CMD, chunk) # 英文也不行
            cmd = "{}/adb.exe {} shell am broadcast -a ADB_INPUT_TEXT --es msg \"'{}'\"".format(LEI_DIAN_DIR, DEVICE_CMD, chunk)
            subprocess.run(cmd, creationflags=g_process_creationflags) 
        #subprocess.run(cmd) 
        #time.sleep(0.1) 
    # chenyj debug
    print("动作:【粘贴文本:{}】".format(text))
    #adb_unset_adb_ime()
    #if b_debug == True:
    #    print("动作:【准备回复的消息:{}】".format(text))
    TIME_END()
    return 
#adb_paste_text("我是顶替城 有浊")

# Ctrl+Z组合键
def adb_click_ctrl_z(str_will_del):
    if len(str_will_del) <= 0:
        return
    for _ in range(len(str_will_del)):
        cmd = LEI_DIAN_DIR + f"/adb.exe {DEVICE_CMD} shell input keyevent KEYCODE_DEL"
        subprocess.run(cmd, creationflags=g_process_creationflags)
        time.sleep(0.03)
    print("动作:【发送Ctrl+Z效果】")
# 测试
#str1 = "123456789"
#adb_paste_text(str1)
#adb_click_ctrl_z(str1)
  
# 判断当前页面是不是“发送”准备好
def is_send_ready():
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_send_btn" + ".png"
    get_screen_of_send_btn(path)
    try:
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!is_send_ready,get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        return False
    if json_return is None: 
        print_my("!!!!!is_send_ready, get_ocr_result_with_small 失败")
        return False
    # chenyj debug
    #print_my(json_return["words_result"])
    for result in json_return["words_result"]:
        content = result["words"]
        if "发送" in content:
            return True  
    return False

def send_webChat_message_with_agent(input_event, dst_username, agent_name, llm_name, coze_agent_info_list, message_all_list_now, message_all_list_new, str_mac, start_time_of_msg, b_in_need_check_is_chat = True):
    global g_b_Debug
    
    i_return = APP_RET_CODE_UNKNOW
    msg_send = ""
    
    # 找到最近的对方回复的内容 
    for i, message in enumerate(message_all_list_new):
        # chenyj test
        if message[0] == "me":
            break
        if len(msg_send) == 0:
            msg_send = message[2]
        else:
            msg_send = message[2] + "\n" + msg_send
    # 如果没找到,则采用旧的消息中的第一条
    if len(msg_send) == 0:
        if len(message_all_list_now) >= 1:
            message = message_all_list_now[0]
            if message[0] != "me":
                msg_send = message[2]
                
    if len(msg_send) == 0:
        # chenyj debug
        print("!!!!发现没有收到新消息")
        for i, message in enumerate(message_all_list_new):
            print("   [{}]:{} {}".format(i, message[0], message[2]))
            
        return APP_RET_CODE_UNVALID_PARAM, msg_send
    
    histroy = []
    for i, message in enumerate(message_all_list_now):
        # chenyj debug 
        #print("send_webChat_message_with_agent, message_all_list_now【{}th】{}".format(i, message))
        if message[0] == "me":
            role = "assistant"
        else:
            role = "user"
        message_item = {"role":role, "content":message[2]}
        #histroy.insert(0, message_item)
        histroy.append(message_item)
        if len(histroy) >= MAX_HISTORY_COUNT:
            break
    # chenyj debug
    """
    print_my("send_webChat_message_with_agent 会话:")
    for i, history_ in enumerate(histroy):
        print_my("  [{}] {}".format(i, history_))
    """
    
    i_try_count = 0
    while i_try_count < AGENT_TRY_COUNT_MAX:
        if agent_name == "电商客服自定义本地话术库":
            i_return, msg_receive = llm_get_result_for_local_rag(dst_username, histroy, msg_send, str_mac)
        elif agent_name == "闲聊专家自定义本地话术库":
            if llm_name in LLM_MODEL_NAME_TYPE_DICT:
                i_return, msg_receive = llm_get_result_for_local_rag_for_chat(dst_username, histroy, msg_send, str_mac) 
            else:
                # 调用Coze智能体
                coze_agent_sel = {}
                for coze_agent_info in coze_agent_info_list:
                    if COZE_FRON_STR + coze_agent_info["agent_name"] == llm_name:
                        coze_agent_sel = coze_agent_info
                        break
                if len(coze_agent_sel) == 0:
                    print_my(f"!!!!你原先设置的LLM或智能体【{llm_name}】找不到了")
                    return i_return, msg_send
                ##
                # 调用cozet智能体 
                i_return, msg_receive = llm_get_result_for_coze_for_chat(dst_username, histroy, msg_send, str_mac, coze_agent_sel["bot_id"], coze_agent_sel["api_token"])
        elif agent_name == "销冠自定义本地话术库":
            i_return, msg_receive = llm_get_result_for_local_rag_for_chat(dst_username, histroy, msg_send, str_mac)  
        elif agent_name == "KimiChat大模型":
            i_return, msg_receive = llm_get_result_from_kimi(dst_username, histroy, msg_send, str_mac)
        elif agent_name == "角色:女大学生闲聊":
            i_return, msg_receive = llm_get_result_from_character(dst_username, histroy, msg_send, str_mac)
        elif agent_name == "Coze图片生成智能体":
            i_return, msg_receive = llm_get_result_for_coze_for_chat(dst_username, histroy, msg_send, str_mac, BOT_ID_OF_IMAGE_GEN_AGENT, API_TOKEN_OF_IMAGE_GEN_AGENT)
            result_json = json.loads(msg_receive)
            msg_receive = result_json["photo"]
        else:
            i_return, msg_receive = agent_get_result(dst_username, agent_name, histroy, msg_send, str_mac)
        if APP_RET_CODE_SUCESS == i_return:
            break
        if True == input_event.wait(4):
            print_my("send_webChat_message_with_agent, 被要求退出")
            return APP_RET_CODE_ZHU_DONG_EXIT, msg_send 
        i_try_count += 1
    if i_try_count >= AGENT_TRY_COUNT_MAX:
        return i_return, msg_send            
    
    if agent_name in ["电商客服自定义本地话术库", "闲聊专家自定义本地话术库", "销冠自定义本地话术库"] and ("回答不了" in msg_receive and len(msg_receive) < 10):
        print_my("自定义知识库无法回答这个问题[{}]".format(msg_send))
        return APP_RET_CODE_NO_ANSWER_IN_KNOWLEDAGE, msg_send
        
    # chenyj debug
    #print("Agent返回的文本是:{}".format(msg_receive))
    if g_b_Debug == True:
        time_taken = time.time() - start_time_of_msg
        msg_receive = msg_receive + "【{:.1f}秒】".format(time_taken)
    i_return = send_webChat_message(input_event, dst_username, msg_receive, b_in_need_check_is_chat)
    if 0 != i_return:
        return i_return, msg_send
        
    return RET_SUCESS, msg_send



def find_image_path(s):
    # 正则表达式匹配Windows上的绝对路径或相对路径
    #pattern = r'([a-zA-Z]:\\[^:\n]*?\.(jpg|jpeg|png|gif|bmp|tiff)|\.\\[^:\n]*?\.(jpg|JPG|jpeg|JPEG|png|PNG|gif|GIF|bmp|BMP|tiff))'
    pattern = r'([a-zA-Z]:\\[^:\n]*?\.(jpg|jpeg|png|gif|bmp|tiff|JPG|JPEG|PNG|GIF|BMP|TIFF)|\.\\[^:\n]*?\.(jpg|jpeg|png|gif|bmp|tiff|JPG|JPEG|PNG|GIF|BMP|TIFF))'
     
    # 搜索字符串中的路径
    match = re.search(pattern, s)
    
    # 如果找到匹配的路径，返回该路径
    if match:
        return match.group(0)
    
    # 如果没有找到，返回None
    return None
# 测试
"""
#s = "这是一个包含图片路径的字符串：C:\\images\\photo.jpg 和 .\\images\\icon.png"
s = "C:\\Users\\admin\\Desktop\\weChat_assistance\\distxxx\\wechatAiAssistantV1.0-2024-10-09\\英语课程.JPG"
path = find_image_path(s)
if path:
    print(f"找到图片路径: {path}")
else:
    print("没有找到图片路径")
"""
    
def send_webChat_message(input_event, dst_username, content, b_in_need_check_is_chat = True):
    i_send_img_count = 0
    
    TIME_BEGIN()
    
    # 如果发送的内容中有图片路径，那么先把图片通过adb传到手机里
    img_path = find_image_path(content)
    if img_path:
        print(f"send_webChat_message, 找到图片路径: {img_path}")
        # 判断图片是否存在 
        if os.path.isfile(img_path) == True: 
            print_my("此次回答是图片回答模式")
            adb_send_image_to_phone(img_path)
            i_send_img_count = 1  
        else:
            print("!!!图片不存在啊")
    # chenyj debug
    if i_send_img_count == 0:
        print("此次回答是文本回答模式")

    b_is_groud, dst_username = username_standard(dst_username)
    # 先确保是在此用户的聊天页面
    if b_in_need_check_is_chat == True:
        iRet, type_return, b_is_groud, user_name_of_chat = get_page_type_by_title()
        if iRet != APP_RET_CODE_SUCESS:
            TIME_END()
            return iRet
        if not (type_return == PageType.Chat and dst_username == user_name_of_chat):
            iRet, b_is_groud = enter_chat_ui(input_event, dst_username)
            if iRet < 0:
                TIME_END()
                return iRet 
            elif iRet == 1: # 找不到此用户
                TIME_END()
                return 0
    """
    if is_weChat_running() == False:
        print_my("!!!!微信应用退出了")
        TIME_END()
        return APP_RET_CODE_APP_EXIT
    """
    # 模式1：发送文本
    if i_send_img_count == 0:
        TRY_COUNT_MAX = 2
        i_try_count = 0
        b_send_ready = False
        while i_try_count < TRY_COUNT_MAX:
            i_try_count += 1
            # 点击编辑框 
            adb_click_chat_edit_for_send_btn()
            if True == input_event.wait(0.3):
                print_my("send_webChat_message, 被要求退出1")
                TIME_END()
                return -1   
            """
            if is_weChat_running() == False:
                print_my("微信应用退出了")
                TIME_END()
                return APP_RET_CODE_APP_EXIT
            """
            # 粘贴文本    
            adb_paste_text(content)
            if True == input_event.wait(0.1):
                print_my("send_webChat_message, 被要求退出2")
                TIME_END()
                return -1  
            # 判断“发送”按钮是否出现
            if b_in_need_check_is_chat == True:
                if is_send_ready() == True:
                    b_send_ready = True
                    break
                else:
                    # chenyj debug
                    print("发送按钮还没出现,继续等待...")
            else: 
                b_send_ready = True
                break
          
        if b_send_ready == False:
            TIME_END()
            return APP_RET_CODE_NO_READY
        # 发送文本
        adb_click_send_btn()
    # 模式2：发送图片
    else:
        # 点击加号按钮 
        adb_click_chat_add_btn()
        if True == input_event.wait(0.3):
            print_my("send_webChat_message, 被要求退出3")
            TIME_END()
            return -1  
        
        # 点击相册按钮
        iRet = adb_click_chat_album_btn_with_check(input_event)
        if iRet == APP_RET_CODE_APP_KA_ZHU:
            print_my("send_webChat_message, 点击相册卡时无效，有异常页面，等待6秒")
            if True == input_event.wait(8):
                print_my("send_webChat_message, 被要求退出4")
                TIME_END()
                return -1  
            # 点击相册按钮
            adb_click_chat_album_btn()

        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Img_And_Video], 5)
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_circle_with_check, 当前不是在图片和视频页页面,但我忽略")
            
        # 选中第一张图片按钮
        adb_click_album_first_img_btn()
        if True == input_event.wait(1):
            print_my("send_webChat_message, 被要求退出5")
            TIME_END()
            return -1  
        # 点击发送图片按钮
        adb_click_send_img_btn()
                
    """
    if is_weChat_running() == False:
        print_my("!!!!微信应用退出了")
        TIME_END()
        return APP_RET_CODE_APP_EXIT
    """
    TIME_END()
    return RET_SUCESS
#content = "哈哈，看来你的优惠券群又有新福利了！不过，我可得提醒你，别光顾着抢券，也得注意一下身体哦，毕竟身体才是革命的本钱嘛！而且，说不定你抢到的券，最后会因为太忙而没时间用呢！"
#content = "哈哈，看来你的优惠券群又有新福利了！不过，我可得提醒你，别光顾着抢券，也得注意一下身体哦，"
#content = "哈哈，看来你的优惠券群又有新福利了！不过，我可得提醒你，别光顾着抢券"
#send_webChat_message(g_Event_test, USERNAME_FOR_NOTICE, content)    

# 正则匹配时间串
def match_time_string(time_str):
    # 正则表达式匹配格式1：7月27日 晚上21:18
    pattern1 = r'\d{1,2}月\d{1,2}日 (\D+)(\d{1,2}):\d{2}'
    pattern1_1 = r'\d{1,2}月\d{1,2}日(\D+)(\d{1,2}):\d{2}'
    pattern1_2 = r'\d{1,2}月\d{1,2}日(\D+)(\d{1,2})：\d{2}'
    # 正则表达式匹配格式2：昨天 下午5:29
    pattern2 = r'昨天 (\D+)(\d{1,2}):\d{2}'
    pattern2_1 = r'昨天(\D+)(\d{1,2}):\d{2}'
    pattern2_2 = r'昨天(\D+)(\d{1,2})：\d{2}'
    # 正则表达式匹配格式3：21:18
    pattern3 = r'^(\d{1,2}):\d{2}$'
    pattern3_1 = r'^(\d{1,2})：\d{2}$'
    # 正则表达式匹配格式4：晚上21:18
    pattern4 = r'(\D+)(\d{1,2}):\d{2}'
    pattern4_1 = r'(\D+)(\d{1,2})：\d{2}'

    # 检查匹配格式1
    if re.match(pattern1, time_str):
        return True
    elif re.match(pattern1_1, time_str):
        return True
    elif re.match(pattern1_2, time_str):
        return True
    # 检查匹配格式2
    elif re.match(pattern2, time_str):
        return True
    elif re.match(pattern2_1, time_str):
        return True
    elif re.match(pattern2_2, time_str):
        return True
    # 检查匹配格式3
    elif re.match(pattern3, time_str):
        return True
    elif re.match(pattern3_1, time_str):
        return True
    # 检查匹配格式4
    elif re.match(pattern4, time_str):
        return True
    elif re.match(pattern4_1, time_str):
        return True
    else:
        return False
    return False
 
def add_space(s):
    # 定义一个正则表达式，匹配“上午”、“下午”或“晚上”这三个词，且它们前面没有空格
    pattern = r'(上午|下午|晚上)'
    
    # 使用re.sub函数进行替换，将匹配到的词前面添加一个空格
    result = re.sub(pattern, r' \1', s)
    
    return result

def parse_and_standardize_time(time_str):  
    time_str_orig = time_str
    # 处理含有"今天"、"昨天"的时间字符串  
    today = datetime.now()  
    if "今天" in time_str:  
        date_part = today.strftime("%Y-%m-%d")  
        date_part = date_part + " "
        time_str = time_str.replace("今天", date_part)  
    elif "昨天" in time_str:  
        date_part = (today - timedelta(days=1)).strftime("%Y-%m-%d")  
        date_part = date_part + " "
        time_str = time_str.replace("昨天", date_part)  
    # 处理含有"周X"的时间字符串
    today = datetime.now()
    days_of_week = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}
    for week_day in days_of_week:
        if week_day in time_str:
            week_day_num = days_of_week[week_day]
            # 计算周五的日期
            date = today - timedelta(days=(today.weekday() - week_day_num) % 7)
            date_part = date.strftime("%Y-%m-%d")  
            date_part = date_part + " "
            time_str = time_str.replace(week_day, date_part)
            break
    #if "上午" in time_str:
    #    time_str = time_str.replace("上午", "AM")
    #elif "下午" in time_str:
    #    time_str = time_str.replace("下午", "PM")
        
    #time_str = time_str + ":00"
    # 尝试使用 dateutil.parser 解析时间  
    try:  
        dt = parser.parse(time_str, fuzzy=True)  
    except Exception as e:  
        print_my(f"!!!!无法解析时间串 '{time_str}': {e}")  
        # eg
        #!!!!无法解析时间串 '2024-09-16 00:94': minute must be in 0..59: 2024-09-16 00:94
        return None, time_str
 
    hour = dt.hour
    if "下午" in time_str or "晚上" in time_str:
        if hour < 12:
            dt = dt.replace(hour=hour + 12)  # 将时间改为下午3点
    # 将时间转换为 ISO 8601 格式  
    str_time = dt.strftime("%Y-%m-%dT%H:%M:%S") 
    # chenyj debug 
    #print_my("{} ==> {}".format(time_str_orig, str_time))
    
    return dt, str_time

# 判断聊天的内容是否属于业务内容 
def is_content_business(content):
    for str_business in BUSINESS_MESSAGE_LIST:
        if str_business in content:
            return True 
    # 把可能是语音业务文本去掉
    if len(content) <= 3:
        content = content.replace("\"", "").replace("(", "").replace(")", "")
        if content.isdigit():
            return True
    return False 
    
# 定义一个函数来处理时间字符串
def insert_colon_in_time(time_str):
    # 正则表达式匹配可能的小时和分钟
    match = re.search(r'(\D+)(\d{1,2})(\d{2})(?!\d)', time_str)
    
    if match:
        # 匹配到小时和分钟，插入冒号
        prefix = match.group(1)  # 前缀，如"昨天中午"、"上午"等
        hour = match.group(2)    # 小时部分
        minute = match.group(3)  # 分钟部分
        # 如果小时部分只有一个数字，需要在前面补0
        corrected_time_str = f"{prefix}{('0' if len(hour) == 1 else '')}{hour}:{minute}"
        return corrected_time_str
    else:
        # 如果没有匹配到，返回原始字符串
        return time_str

# 判断消息是不是引用文本
def is_msg_yin_yonged(img):
    if True == image_is_gray(img):
        return True 
 
# 判断消息是不是正式文本
def is_msg_text_content(img):
    if True == image_is_blue(img):
        return True 
    if True == image_is_white(img):
        return True 
    return False
    
# 结构化图片中的单群聊内容
def struct_single_chat_message(dst_username = "", b_is_groud =  False): 
    global g_i_chat_count
    global g_i_crop_count
    
    TIME_BEGIN()
    message_list = []
    message_no_time_list = []
    time_info_list = []
   
    _, dst_username = username_standard(dst_username)
    g_i_chat_count += 1
    if len(dst_username) == 0:
        iRet, type_page, b_is_groud, dst_username = get_page_type_by_title()
        if iRet != APP_RET_CODE_SUCESS:
            TIME_END()
            return iRet
        if len(dst_username) == 0:
            print_my("!!!!无法获得聊天对象")
            TIME_END()
            return message_list, message_no_time_list, time_info_list
    # chenyj debug
    # 是否是群聊消息
    if b_is_groud == True:  
        # chenyj debug
        #print("【{}】是群聊".format(dst_username))
        pass
    else:
        # chenyj debug
        #print("【{}】是单聊".format(dst_username))
        pass
    #     
    #path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_chat_{}".format(g_i_chat_count) + ".png"
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_chat_3" + ".png"
    get_screen_of_chat(path)
    
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        #_, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!struct_chat_message,get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        TIME_END()
        return message_list, message_no_time_list, time_info_list
    if json_return is None: 
        print_my("!!!!!struct_chat_message, get_ocr_result_with_small 失败")
        TIME_END()
        return message_list, message_no_time_list, time_info_list
    # chenyj debug
    #print(json_return["words_result"])

    # 找出里面的时间
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        # 去掉被截断的文本
        if y <= g_chat_min_y_for_ocr or y >= g_chat_max_y_for_ocr:
            continue
        if x < g_chat_time_lt_x or x > g_chat_time_rb_x:
            continue 
        if True == is_content_business(content):
            continue    
        # 7月27日 晚上21:18
        # 7月27日 上午7:18
        # 昨天 下午5:29
        # 21:18
        # 中午12:53
        ############ 异常 ##########
        # 下午133
        #昨天中午1253
        #昨天中午1256
        # chenyj debug
        #print("\"{}\"可能是时间".format(content))
        # 对一些异常的时间格式进行规范化后，找回来一些 
        if abs((x + int(width/2)) - g_chat_half_x) < 20:
            if False == match_time_string(content):
                #print_my("!!!!!这是一个格式不规范的时间:{}".format(content))
                # 对时间规整
                content = content.replace("周-", "周一")
                content = insert_colon_in_time(content)
                #print_my("  ==>规整后是:{}".format(content))
        if True == match_time_string(content):
            str_time = content
            # chenyj debug
            #print("找到了时间串:{}".format(str_time))
            # 把时间格式标准化
            str_time = str_time.replace("：", ":")
            str_time = add_space(str_time)
            # chenyj debug
            #print("  ==>规整为1:{}".format(str_time))
            dt, str_time = parse_and_standardize_time(str_time)
            if dt is None:
                print("!!!!!这是一个格式不规范的时间:{}".format(str_time))
                continue
            # chenyj debug
            #print("  ==>规整为2:{}".format(str_time))
            time_info_list.append([dt, str_time, y])
        
    # 对时间按y降序排序
    time_info_list = sorted(time_info_list, key=lambda x: x[2], reverse=True)
    # chenyj debug 
    """
    print_my("得到的时间列表是:")
    for time_info in time_info_list:
        print_my(" {}".format(time_info))
    """
    
    # 对OCR得到的文本进行类别标记
    # 去掉里面暂时处理不了的类型：引用文本
    TIME_BEGIN("对OCR得到的文本进行类别标记")
    words_results_new = []
    img = Image.open(path)
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        
        bbox = (x, y, x + width, y + height)
        try:
            cropped_img = img.crop(bbox)
            g_i_crop_count += 1
            #crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_{}.png".format(g_i_crop_count)
            crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp.png"
            cropped_img.save(crop_path)
            crop_mage = imread(crop_path)
        except Exception as e:
            print("!!!!struct_single_chat_message, 出现异常:{}".format(e))
            continue 
            
        if True == is_msg_yin_yonged(crop_mage):
            # chenyj debug
            print("背景颜色判断这是引用文本:{}".format(content))
            continue
        if False == is_msg_text_content(crop_mage):
            # chenyj debug
            print("背景颜色判断不是消息文本:{}".format(content))
            continue
        words_results_new.append(result)
    json_return["words_result"]= words_results_new
    TIME_END("对OCR得到的文本进行类别标记")
    # 对上下行的OCR聊天内容进行合并
    delete_result_list = []
    for result in json_return["words_result"]:
        content = result["words"]
        # chenyj debug
        #print_my("{}".format(content))
        lt_x = result["location"]["left"]
        lt_y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        rb_x = lt_x + width
        # 跳过发送者的名称 
        if lt_x < g_chat_half_x:
            if abs(lt_x - g_sender_lt_x_should_min) <= g_sender_lt_x_should_min_inter:
                # chenyj debug
                #print_my("0群聊发送者:[{}]".format(content))
                continue
                        
        # height <= g_chat_line_height and 
        #if (lt_x < g_chat_time_lt_x or lt_x > g_chat_time_rb_x):
        if True:
            for result_ in json_return["words_result"]:
                content_ = result_["words"]
                lt_x_ = result_["location"]["left"]
                lt_y_ = result_["location"]["top"]
                width_ = result_["location"]["width"]
                height_ = result_["location"]["height"]
                rb_x_ = lt_x_ + width_
                rb_y_ = lt_y_ + height_
                # 去掉被截断的文本
                if lt_y_ <= g_chat_min_y_for_ocr or lt_y_ >= g_chat_max_y_for_ocr:
                    print("0跳过可能被截断的文本.[{}]".format(content_))
                    continue
            
                if lt_x_ == lt_x and lt_y_ == lt_y:
                    continue
                if lt_y > lt_y_:
                    continue
                # 跳过发送者的名称 
                if lt_x_ < g_chat_half_x:
                    if abs(lt_x_ - g_sender_lt_x_should_min) <= g_sender_lt_x_should_min_inter:
                        # chenyj debug
                        #print_my("1群聊发送者:[{}]".format(content))
                        continue
                # and (lt_x_ < g_chat_time_lt_x or lt_x_ > g_chat_time_rb_x)
                if height_ <= g_chat_line_height:
                    if ((lt_y_ - (lt_y + height)) < g_chat_line_height_inter) and (abs(lt_x - lt_x_) < g_chat_line_width_inter):
                        # chenyj debug
                        #print_my("  {} 【({}, {})  <==> ({}, {})】".format(content_, lt_x, lt_y, lt_x_, lt_y_))
                        result["words"] = content + content_
                        result["location"]["left"] = lt_x if lt_x <= lt_x_ else lt_x_
                        rb_x_new = rb_x if rb_x >= rb_x_ else rb_x_
                        result["location"]["width"] = rb_x_new - result["location"]["left"]
                        result["location"]["height"] = rb_y_ - lt_y
                        
                        content = result["words"]
                        lt_x = result["location"]["left"]
                        lt_y = result["location"]["top"]
                        width = result["location"]["width"]
                        height = result["location"]["height"]
                        rb_x = lt_x + width
        
                        delete_result_list.append(result_)
    words_results_new = []
    for result in json_return["words_result"]:
        content = result["words"]
        lt_x = result["location"]["left"]
        lt_y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        b_delete = False
        for result_delete in delete_result_list:
            lt_x_delete = result_delete["location"]["left"]
            lt_y_delete = result_delete["location"]["top"]
            if lt_x == lt_x_delete and lt_y == lt_y_delete:
                b_delete = True
                break 
        if b_delete == False:
            words_results_new.append(result)
    json_return["words_result"]= words_results_new
    
    # 对所有聊天内容结构化
    y_of_time_last = g_h_screen
    for time_info in time_info_list:
        dt_of_time = time_info[0]
        str_time = time_info[1]
        y_of_time = time_info[2]
        sender_name = ""
        for result in json_return["words_result"]:
            content = result["words"]
            lt_x = result["location"]["left"]
            lt_y = result["location"]["top"]
            width = result["location"]["width"]
            rb_x = lt_x + width
            if True == is_content_business(content):
                print("跳过可能属于业务内容的文本.[{}]".format(content))
                continue
            # 去掉可能被截断的文本
            if lt_y <= g_chat_min_y_for_ocr or lt_y >= g_chat_max_y_for_ocr:
                print("1跳过可能被截断的文本.[{}]".format(content))
                continue
            if lt_y > y_of_time and lt_y < y_of_time_last:
                if lt_x < g_chat_half_x:
                    # 找到发送者的名称 
                    if abs(lt_x - g_sender_lt_x_should_min) <= g_sender_lt_x_should_min_inter:
                        # chenyj debug
                        print_my("2群聊发送者:[{}]".format(content))
                        sender_name = content
                        continue
                    # 找到可能是音频文字或图片的文字
                    if abs(lt_x - g_chat_lt_x_should_min) > g_chat_lt_x_should_min_inter:
                        print("1虽然得到OCR的结果:[{}],但可能是音频文字或图片文字".format(content))
                        continue
                    # chenyj debug
                    #print_my("lt_x:{}, 1 content:{}".format(lt_x, content))
                    #message = [dst_username, dt_of_time, str_time, content, lt_y]
                    if b_is_groud == True:
                        if len(sender_name) > 0:
                            message = [sender_name, str_time, content, lt_y]
                        else:
                            #assert False, "这条消息找不到发送者:{}".format(content)
                            print_my("!!!!!这条消息找不到发送者:{}".format(content))
                            continue
                    else:
                        message = [dst_username, str_time, content, lt_y]
                else:
                    if abs(rb_x - g_chat_rb_x_should_min) > g_chat_rb_x_should_min_inter:
                        print("2虽然得到OCR的结果:[{}],但可能是音频文字或图片文字".format(content))
                        continue
                    # chenyj debug
                    #print_my("rb_x:{}, 2 content:{}".format(rb_x, content))
                    #message = ["me", dt_of_time, str_time, content, lt_y]
                    message = ["me", str_time, content, lt_y]                 
                
                message_list.append(message)
                sender_name = ""
        y_of_time_last = y_of_time
    # 对消息按y降序排序
    message_list = sorted(message_list, key=lambda x: x[3], reverse=True)    
    # chenyj debug 
    """
    print_my("得到的有发送时间的消息列表是:")
    for i, message in enumerate(message_list):
        print_my(" 【{}】{}".format(i+1, message))   
    """
    
    # 找到不确定时间的消息
    y_of_time_min = g_h_screen
    if len(time_info_list) != 0:
        y_of_time_min = time_info_list[-1][2]
    sender_name = ""
    for result in json_return["words_result"]:
        content = result["words"]
        lt_x = result["location"]["left"]
        lt_y = result["location"]["top"]
        width = result["location"]["width"]
        rb_x = lt_x + width 
        if True == is_content_business(content):
            print("2跳过可能属于业务内容的文本.[{}]".format(content))
            continue
        # 去掉被截断的文本
        if lt_y <= g_chat_min_y_for_ocr or lt_y >= g_chat_max_y_for_ocr:
            print("2跳过可能被截断的文本.[{}]".format(content))
            continue
        if lt_y < y_of_time_min:
            if lt_x < g_chat_half_x:
                # 找到发送者的名称 
                if abs(lt_x - g_sender_lt_x_should_min) <= g_sender_lt_x_should_min_inter:
                    # chenyj debug
                    print_my("3群聊发送者:[{}]".format(content))
                    sender_name = content
                    continue
                if abs(lt_x - g_chat_lt_x_should_min) > g_chat_lt_x_should_min_inter:
                    print("3虽然得到OCR的结果:[{}],但可能是音频文字或图片文字".format(content))
                    continue
                # chenyj debug
                #print_my("lt_x:{}, 3 content:{}".format(lt_x, content))
                
                if b_is_groud == True:
                    if len(sender_name) > 0:
                        message = [sender_name, "", content, lt_y]
                    else:
                        #assert False, "这条消息找不到发送者:{}".format(content)
                        print_my("!!!!!这条消息找不到发送者:{}".format(content))
                        continue
                else:
                    message = [dst_username, "", content, lt_y]
            else:
                if abs(rb_x - g_chat_rb_x_should_min) > g_chat_rb_x_should_min_inter:
                    print("4虽然得到OCR的结果:[{}],但可能是音频文字或图片文字".format(content))
                    continue
                # chenyj debug
                #print_my("rb_x:{}, 4 content:{}".format(rb_x, content))
                message = ["me", "", content, lt_y]
            message_no_time_list.append(message)
            sender_name = ""
    # 对消息按y降序排序
    message_no_time_list = sorted(message_no_time_list, key=lambda x: x[3], reverse=True)    
    # chenyj debug
    """
    print_my("得到的无发送时间的消息列表是:")
    for i, message in enumerate(message_no_time_list):
        print_my(" 【{}】{}".format(i+1, message))  
    """
    TIME_END()
    return message_list, message_no_time_list, time_info_list    
#message_list, message_no_time_list, time_info_list = struct_single_chat_message()
  
# 向上滑动聊天内容
def adb_slide_chat_content_up(input_event):
    drag_bot_x_random_number = randint(100, g_w_screen)
    drag_bot_y_random_number = randint(int(1714/1920 * g_h_screen), int(1825/1920 * g_h_screen))
    drag_top_x_random_number = randint(100, g_w_screen)
    drag_top_y_random_number = randint(int(150/1920 * g_h_screen), int(250/1920 * g_h_screen))
    i_time_ms = 2000
    cmd = "{}/adb.exe {} shell input swipe {} {} {} {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, drag_top_x_random_number, drag_top_y_random_number, drag_bot_x_random_number, drag_bot_y_random_number, i_time_ms)
    #print_my(cmd)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    # chenyj debug
    print("动作:【向上滑动聊天内容1屏】")
    print_my("读取新消息中...")
    if True == input_event.wait(0.5):
        print_my("adb_slide_chat_content_up, 被要求退出")
        return -1 
    return 0
#path = SCREENSHOT_SAVE_DIR + "/" + "example_chat_slide_up" + ".png"
#adb_get_screen(path)
#adb_slide_chat_content_up(g_Event_test)

def adb_slide_chat_content_up_with_check(input_event):
    image_check_begin()
    iRet = adb_slide_chat_content_up(input_event)
    if iRet != 0:
        return iRet
    time.sleep(0.5)
    iRet, bChange = image_check_end()
    if iRet == 0 and bChange == False:
        return APP_RET_CODE_APP_KA_ZHU
    return APP_RET_CODE_SUCESS
    
# 向下滑动聊天内容
def adb_slide_chat_content_down(input_event):
    drag_bot_x_random_number = randint(100, g_w_screen)
    drag_bot_y_random_number = randint(int(1714/1920 * g_h_screen), int(1825/1920 * g_h_screen))
    drag_top_x_random_number = randint(100, g_w_screen)
    drag_top_y_random_number = randint(int(150/1920 * g_h_screen), int(250/1920 * g_h_screen))
    i_time_ms = 1000
    cmd = "{}/adb.exe {} shell input swipe {} {} {} {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, drag_bot_x_random_number, drag_bot_y_random_number, drag_top_x_random_number, drag_top_y_random_number, i_time_ms)
    #print_my(cmd)
    subprocess.run(cmd, creationflags=g_process_creationflags) 
    print_my("动作:【向下滑动聊天内容1屏】")
    if True == input_event.wait(1):
        print_my("adb_slide_chat_content_down, 被要求退出")
        return -1 
    return 0
#path = SCREENSHOT_SAVE_DIR + "/" + "example_chat_slide_down" + ".png"
#adb_get_screen(path)
#adb_slide_chat_content_down(g_Event_test)

def adb_slide_chat_content_down_with_check(input_event):
    image_check_begin()
    iRet = adb_slide_chat_content_down(input_event)
    if iRet != 0:
        return iRet
    time.sleep(0.5)
    iRet, bChange = image_check_end()
    if iRet == 0 and bChange == False:
        return APP_RET_CODE_APP_KA_ZHU
    return APP_RET_CODE_SUCESS

# 向上滑动通讯录
def adb_slide_friendbook_content_up(input_event):
    if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            drag_bot_x_random_number = randint(100, g_w_screen)
            drag_bot_y_random_number = randint(int(1830/1920 * g_h_screen), int(1832/1920 * g_h_screen))
            drag_top_x_random_number = randint(100, g_w_screen)
            drag_top_y_random_number = randint(int(120/1920 * g_h_screen), int(122/1920 * g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            drag_bot_x_random_number = randint(100, g_w_screen)
            drag_bot_y_random_number = randint(int(2120), int(2130))
            drag_top_x_random_number = randint(100, g_w_screen)
            drag_top_y_random_number = randint(int(220), int(250))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            drag_bot_x_random_number = randint(100, g_w_screen)
            drag_bot_y_random_number = randint(int(2120), int(2130))
            drag_top_x_random_number = randint(100, g_w_screen)
            drag_top_y_random_number = randint(int(220), int(250))
        
        i_time_ms = 2000
        cmd = "{}/adb.exe {} shell input swipe {} {} {} {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, drag_top_x_random_number, drag_top_y_random_number, drag_bot_x_random_number, drag_bot_y_random_number, i_time_ms)
        #print_my(cmd)
        subprocess.run(cmd, creationflags=g_process_creationflags) 
        # chenyj debug
        #print_my("动作:【向上滑动通讯录1屏】")
        print_my("读取新通讯录中...")
        if True == input_event.wait(0.5):
            print_my("adb_slide_friendbook_content_up, 被要求退出")
            return -1 
    else:
        return windows_slide_friendbook_up(input_event)
        
    return 0
#path = SCREENSHOT_SAVE_DIR + "/" + "example_chat_slide_up" + ".png"
#adb_get_screen(path)
#adb_slide_friendbook_content_up(g_Event_test)

def adb_slide_friendbook_up_with_check(input_event):
    image_check_begin()
    iRet = adb_slide_friendbook_content_up(input_event)
    if iRet != 0:
        return iRet
    time.sleep(0.5)
    iRet, bChange = image_check_end()
    if iRet == 0 and bChange == False:
        return APP_RET_CODE_APP_KA_ZHU
    return APP_RET_CODE_SUCESS

# 向下滑动通讯录
def adb_slide_friendbook_down(input_event):
    if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            drag_bot_x_random_number = randint(100, g_w_screen)
            drag_bot_y_random_number = randint(int(1700/1920 * g_h_screen), int(1702/1920 * g_h_screen))
            drag_top_x_random_number = randint(100, g_w_screen)
            drag_top_y_random_number = randint(int(160/1920 * g_h_screen), int(162/1920 * g_h_screen))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            drag_bot_x_random_number = randint(100, g_w_screen)
            drag_bot_y_random_number = randint(int(2120), int(2130))
            drag_top_x_random_number = randint(100, g_w_screen)
            drag_top_y_random_number = randint(int(220), int(250))
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            drag_bot_x_random_number = randint(100, g_w_screen)
            drag_bot_y_random_number = randint(int(2120), int(2130))
            drag_top_x_random_number = randint(100, g_w_screen)
            drag_top_y_random_number = randint(int(220), int(250))
        
        i_time_ms = 2000
        cmd = "{}/adb.exe {} shell input swipe {} {} {} {} {}".format(LEI_DIAN_DIR, DEVICE_CMD, drag_bot_x_random_number, drag_bot_y_random_number, drag_top_x_random_number, drag_top_y_random_number, i_time_ms)
        #print_my(cmd)
        subprocess.run(cmd, creationflags=g_process_creationflags) 
        print("动作:【向下滑动通讯录1屏】")
        if True == input_event.wait(1):
            print_my("adb_slide_friendbook_down, 被要求退出")
            return -1 
    else:
        return windows_slide_friendbook_down(input_event)
    return 0
#path = SCREENSHOT_SAVE_DIR + "/" + "example_chat_slide_down" + ".png"
#adb_get_screen(path)
#adb_slide_friendbook_down(g_Event_test)

def adb_slide_friendbook_down_with_check(input_event):
    image_check_begin()
    iRet = adb_slide_friendbook_down(input_event)
    if iRet != 0:
        return iRet
    time.sleep(0.5)
    iRet, bChange = image_check_end(0.98)
    if iRet == 0 and bChange == False:
        return APP_RET_CODE_APP_KA_ZHU
    return APP_RET_CODE_SUCESS
 
# 把聊天消息保存到文件中
def save_message(dst_username, message_all_list):
    b_is_groud, dst_username = username_standard(dst_username)
    path = MESSAGE_SESSION_DIR + "/" + dst_username + ".json"
    # 按时间排序
    message_all_list = sorted(message_all_list, key=lambda x: x[1], reverse=True) 
    with open(path, 'w', encoding='utf-8') as file:
        for i, message in enumerate(message_all_list):
            message_json = json.dumps(message, ensure_ascii=False)
            file.write(message_json)
            if i < len(message_all_list) - 1:
                file.write("\n")
    # chenyj debug
    print_my("将新消息保存到文件:【{}】".format(path))
    return True 
#message_all_list_test = [(11, "22", 33, "44"), (55, "66", 77, "88")]
#save_message("test", message_all_list_test)

# 读取某个聊天对象的聊天内容 
def read_message(dst_username):
    message_all_list = []
    
    b_is_groud, dst_username = username_standard(dst_username)
    path = MESSAGE_SESSION_DIR + "/" + dst_username + ".json"
    # 判断文件是否存在 
    if False == os.path.exists(path):
        print_my("!!!!!【{}】的聊天文件不存在".format(dst_username))
        return False, message_all_list 
        
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            message = json.loads(line)
            message_all_list.append(message)
    # 按时间排序
    message_all_list = sorted(message_all_list, key=lambda x: x[1], reverse=True)  
    # chenyj debug
    print("从本地聊天文件{}中读取到托管对象【{}】{}条聊天内容".format(path, dst_username, len(message_all_list)))   
    #for i, message in enumerate(message_all_list):
    #    print_my(" 【{}】{}".format(i+1, message))  
        
    return True, message_all_list
# chenyj test
'''
dst_username = "任小玲"
bRet, message_all_list = read_message(dst_username)
if bRet == True:
    g_message_dict[dst_username] = message_all_list
    # chenyj debug
    """
    print_my("从聊天对象【{}】的聊天文件中读取到{}条聊天内容:".format(dst_username, len(message_all_list)))
    for message in message_all_list:
        print_my("  {}".format(message))
    """
    pass
'''

# 读取所有离线消息
def read_all_message():
    global g_message_dict
    
    filename_list = []
    for filename in os.listdir(MESSAGE_SESSION_DIR):
        if filename.endswith(".json"):
            username = filename.replace(".json", "")
            bRet, message_all_list = read_message(username)
            if bRet == True:
                g_message_dict[username] = message_all_list
            
# 业务初始化
def auto_opt_init():
    read_all_message()
    return True

def add_message(message_all_list, message, message_all_list_orig):
    time_str = message[1]
    content = message[2]
    parsed_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
    year = parsed_time.year
    month = parsed_time.month
    day = parsed_time.day
    hour = parsed_time.hour
    minute = parsed_time.minute
    second = parsed_time.second
    
    # 检查在历史中是否有同年、月、日、时、分的消息,但不同秒与content的消息 
    b_same_minute_in_history = False 
    for message_ in message_all_list_orig:
        time_str_ = message_[1]
        content_ = message_[2]
        parsed_time_ = datetime.strptime(time_str_, "%Y-%m-%dT%H:%M:%S")
        year_ = parsed_time_.year
        month_ = parsed_time_.month
        day_ = parsed_time_.day
        hour_ = parsed_time_.hour
        minute_ = parsed_time_.minute
        second_ = parsed_time_.second 
        if year_ == year and month_ == month and day_ == day and hour_ == hour and minute_ == minute and second_ != second and content_ != content:
            b_same_minute_in_history = True 
            break 
    
    b_has_same_minute = False
    second_min = 30
    for message_ in message_all_list:
        time_str_ = message_[1]
        parsed_time_ = datetime.strptime(time_str_, "%Y-%m-%dT%H:%M:%S")
        year_ = parsed_time_.year
        month_ = parsed_time_.month
        day_ = parsed_time_.day
        hour_ = parsed_time_.hour
        minute_ = parsed_time_.minute
        second_ = parsed_time_.second
        
        if year_ == year and month_ == month and day_ == day and hour_ == hour and minute_ == minute:
            b_has_same_minute = True
            if second_ < second_min:
                second_min = second_
            continue 
    if b_has_same_minute == True: 
        if b_same_minute_in_history == False:
            second_new = second_min - 1
        else: 
            second_new = second_min + 1
    else: 
        second_new = 30
    if second_new < 0:
        second_new = 0
    if second_new > 59:
        second_new = 59 
    dt = datetime(year, month, day, hour, minute, second_new)
    time_str_new = dt.strftime("%Y-%m-%dT%H:%M:%S")
    message[1] = time_str_new
    message_all_list.append(message)
    return True

def is_exist_in_message_list(message_all_list_in, message_in):
    bExist = False   
    
    time_str = message_in[1]
    parsed_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
    year = parsed_time.year
    month = parsed_time.month
    day = parsed_time.day
    hour = parsed_time.hour
    minute = parsed_time.minute
    second = parsed_time.second
    
    for message_ in message_all_list_in:
        time_str_ = message_[1]
        parsed_time_ = datetime.strptime(time_str_, "%Y-%m-%dT%H:%M:%S")
        year_ = parsed_time_.year
        month_ = parsed_time_.month
        day_ = parsed_time_.day
        hour_ = parsed_time_.hour
        minute_ = parsed_time_.minute
        second_ = parsed_time_.second
        if message_in[0] == message_[0] and message_in[2] == message_[2]:
            if year == year_ and month == month_ and day_ == day and hour == hour_ and minute == minute_:
                bExist = True
                break
    return bExist


    
# 获得某个用户/群的聊天消息内容
def get_weChat_chat_content(input_event, dst_username, b_in_need_check_is_chat = True): 
    global g_message_dict
    global g_monitor_object_info_dict
    
    time_list = []
    i_gun_up_count = 0
    message_no_time_list_last = []
    message_all_list_orig = []
    message_all_list_now = []
    message_all_list_new = []
    
    TIME_BEGIN()
    _, dst_username = username_standard(dst_username)
    # chenyj debug
    print("===>get_weChat_chat_content")
    print_my("读取新消息")
    # 先确保是在此用户的聊天页面
    if b_in_need_check_is_chat == True:
        iRet, type_return, b_is_groud, user_name_of_chat = get_page_type_by_title()
        if iRet != APP_RET_CODE_SUCESS:
            TIME_END()
            return iRet, message_all_list_now, message_all_list_new
            
        if not (type_return == PageType.Chat and dst_username == user_name_of_chat):
            iRet, b_is_groud = enter_chat_ui(input_event, dst_username)
            if iRet != 0:
                TIME_END()
                return iRet, message_all_list_now, message_all_list_new
        else:
            # 滚动到聊天最底部
            i_gun_down_count = 0
            while i_gun_down_count < MAX_SLIDE_DOWN_COUNT:
                i_gun_down_count += 1
                iRet = adb_slide_chat_content_down_with_check(input_event)
                if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                    print_my("get_weChat_chat_content, 被要求退出")
                    TIME_END()
                    return APP_RET_CODE_ZHU_DONG_EXIT, message_all_list_now, message_all_list_new
                elif iRet == APP_RET_CODE_APP_KA_ZHU:
                    # chenyj dbug
                    print("get_weChat_chat_content, 滚动了消息的底部")
                    break
    else:
        iRet, b_is_groud = enter_chat_ui(input_event, dst_username)
        if iRet != 0:
            TIME_END()
            return iRet, message_all_list_now, message_all_list_new
        if "b_is_groud" not in g_monitor_object_info_dict[dst_username]:
            # chenyj debug
            print("之前没有存此用户[{}]的b_is_groud,现在去获得".format(dst_username))
            iRet, type_return, b_is_groud, user_name_of_chat = get_page_type_by_title()
            if iRet != APP_RET_CODE_SUCESS:
                TIME_END()
                return iRet, message_all_list_now, message_all_list_new
            # chenyj debug 
            print("type_return:{}, dst_username:{}, user_name_of_chat:{}".format(type_return, dst_username,  user_name_of_chat))
            if (type_return == PageType.Chat and dst_username == user_name_of_chat):
                g_monitor_object_info_dict[dst_username]["b_is_groud"] = b_is_groud
        else:
            b_is_groud = g_monitor_object_info_dict[dst_username]["b_is_groud"]
            
    if dst_username in g_message_dict:
        # chenyj debug 
        print("此用户【{}】之前存在{}条消息".format(dst_username, len(g_message_dict[dst_username])))
        message_all_list_orig = copy.deepcopy(g_message_dict[dst_username])
        message_all_list_now = copy.deepcopy(g_message_dict[dst_username])
    
    b_should_break = False 
    max_slide_up_COUNT_now = MAX_SLIDE_UP_COUNT
    time_info_list_all = []
    while i_gun_up_count < max_slide_up_COUNT_now:
        i_gun_up_count += 1
        message_list, message_no_time_list, time_info_list = struct_single_chat_message(dst_username, b_is_groud)
        # chenyj debug  
        print("=====第{}屏消息====".format(i_gun_up_count))
        print("有时间的消息:")
        for i, message in enumerate(message_list):
            print(" 【{}】{}".format(i+1, message))
        print("没有时间的消息:")
        for i, message in enumerate(message_no_time_list):
            print(" 【{}】{}".format(i+1, message))
            
        time_info_list_all.extend(time_info_list)
        if i_gun_up_count == max_slide_up_COUNT_now and len(time_info_list_all) == 0 and max_slide_up_COUNT_now < 12:
            max_slide_up_COUNT_now += 1
        
        TIME_BEGIN("第{}屏消息的后处理".format(i_gun_up_count))
        # 捞回上一截屏中没有发送时间的消息
        if len(time_info_list) > 0 and len(message_no_time_list_last) > 0:
            time_info = time_info_list[0]
            #dt_of_time = time_info[0]
            str_time = time_info[1]
            y_of_time = time_info[2]
            for message_no_time in message_no_time_list_last:
                #message_add_time = (message_no_time[0], dt_of_time, str_time, message_no_time[2])
                message_add_time = [message_no_time[0], str_time, message_no_time[2]]
                # 要加消息排重
                bExist = is_exist_in_message_list(message_all_list_now, message_add_time)
                """
                bExist = False
                for message_ in message_all_list_now:
                    if message_add_time[0] == message_[0] and message_add_time[1] == message_[1] and message_add_time[2] == message_[2]:
                        bExist = True
                        break
                """
                if bExist == False:
                    add_message(message_all_list_now, message_add_time, message_all_list_orig)
                    #message_all_list_now.append(message_add_time)   
                # 增加是否要停止的判断
                bExist = is_exist_in_message_list(message_all_list_orig, message_add_time)
                if bExist == True:
                    #print_my("^-^发现了旧的消息:【{}】".format(message_add_time))
                    b_should_break = True
                """
                for message_ in message_all_list_orig:
                    if message_add_time[0] == message_[0] and message_add_time[1] == message_[1] and message_add_time[2] == message_[2]:
                        b_should_break = True
                        break
                """
            # chenyj debug
            #print("捞回【{}】条消息的时间".format(len(message_no_time_list_last)))     
            message_no_time_list_last = message_no_time_list
        else:
            message_no_time_list_last.extend(message_no_time_list)
        # 要加消息排重
        for message in message_list:
            bExist = is_exist_in_message_list(message_all_list_now, message)
            """
            bExist = False
            for message_ in message_all_list_now:
                if message[0] == message_[0] and message[1] == message_[1] and message[2] == message_[2]:
                    bExist = True
                    break
            """
            if bExist == False:
                add_message(message_all_list_now, message, message_all_list_orig)
                #message_all_list_now.append(message)
            # 增加是否要停止的判断
            bExist = is_exist_in_message_list(message_all_list_orig, message)
            if bExist == True:
                # chenyj debug
                print("^-^发现了旧的消息:【{}】".format(message))
                b_should_break = True
            """
            for message_ in message_all_list_orig:
                if message[0] == message_[0] and message[1] == message_[1] and message[2] == message_[2]:
                    b_should_break = True
                    break
            """
        TIME_END("第{}屏消息的后处理".format(i_gun_up_count))
        # 如果发现是旧的消息就不再上一刷了
        if b_should_break == True:
            # chenyj debug
            print("^-^发现了旧的消息，不再向上刷了")
            break
        if i_gun_up_count == max_slide_up_COUNT_now:
            # chenyj debug
            print("达到滑动最大次数，不再向上刷了")
            break
        # 向上滚动一屏
        iRet = adb_slide_chat_content_up_with_check(input_event)
        if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
            print_my("get_weChat_chat_content, 被要求退出")
            TIME_END()
            return APP_RET_CODE_ZHU_DONG_EXIT, message_all_list_now, message_all_list_new
        elif iRet == APP_RET_CODE_APP_KA_ZHU:
            # chenyj debug
            print("get_weChat_chat_content, 滚动了消息的顶部")
            break    
            
        if True == input_event.wait(0.1):
            print_my("get_weChat_chat_content, 被要求退出")
            TIME_END()
            return APP_RET_CODE_ZHU_DONG_EXIT, message_all_list_now, message_all_list_new 
        """
        if is_weChat_running() == False:
            print_my("!!!!微信应用退出了")
            TIME_END()
            return APP_RET_CODE_APP_EXIT, message_all_list_now, message_all_list_new
        """
        continue
    TIME_BEGIN("总体消息的后处理")    
    for i, message in enumerate(message_all_list_now):
        bExist = is_exist_in_message_list(message_all_list_orig, message)
        if bExist == False:
            message_all_list_new.append(message)
    # chenyj debug 
    """
    print_my("得到来自【{}】的【{}】条新消息:".format(dst_username, len(message_all_list_new)))
    for i, message in enumerate(message_all_list_new):
        print_my(" 【{}】{}".format(i+1, message))   
        
    """
    
    print_my("新消息读取成功")
    # 按时间排序
    message_all_list_now = sorted(message_all_list_now, key=lambda x: x[1], reverse=True) 
    # 保存到文件中
    save_message(dst_username, message_all_list_now)
    g_message_dict[dst_username] = message_all_list_now
    TIME_END("总体消息的后处理")  
    # chenyj debug
    print("<===get_weChat_chat_content 共【{}】页，共{}条新消息".format(i_gun_up_count, len(message_all_list_new)))
    
    TIME_END()    
    return RET_SUCESS, message_all_list_now, message_all_list_new
#get_weChat_chat_content(g_Event_test, "任小玲")
 
# 点击消息列表页的添加好友加号按钮
def adb_click_add_btn():
    # chenyj debug
    print("动作:【点击添加按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(1022/W_SCREEN*g_w_screen), int(75/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(1006), int(140))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(671), int(78))
    return APP_RET_CODE_SUCESS
#adb_click_add_btn()

# 点击添加到通讯录页的添加朋友按钮
def adb_click_add_friend_btn():
    # chenyj debug
    print("动作:【点击添加好友按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(949/W_SCREEN*g_w_screen), int(256/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(823), int(456))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(565), int(285))
    return APP_RET_CODE_SUCESS
#adb_click_add_friend_btn()


# 点击消息列表页的搜索按钮
def adb_click_search_btn():
    # chenyj debug
    print("动作:【点击搜索按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(964/W_SCREEN*g_w_screen), int(75/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(893), int(141))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(893), int(141))
    return APP_RET_CODE_SUCESS
#adb_click_search_btn()

# 点击搜索页中的“文件传输助手”按钮
def adb_click_search_item_btn(i_pos_y = -1):
    # chenyj debug
    print("动作:【点击搜索页的指定Item项】")
    if i_pos_y == -1:
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            i_pos_y = 228
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            i_pos_y = 399
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            i_pos_y = 399
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(180/W_SCREEN*g_w_screen), int(i_pos_y/H_SCREEN*g_h_screen))
    else:
        adb_click(int(256), int(i_pos_y/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_search_item_btn()
 
# 点击添加好友搜索页搜索item按钮
def adb_click_search_item_btn_for_add_friend():
    # chenyj debug
    print("动作:【点击添加好友页的搜索item】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(217/W_SCREEN*g_w_screen), int(166/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(362), int(294))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(247), int(179))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(int(379+G_X_PIAN_YI), int(163+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS
#adb_click_search_item_btn_for_add_friend()

# 点击搜索到个人信息页搜索item按钮
def adb_click_search_item_btn_for_searched_person_page():
    # chenyj debug
    print("动作:【点击搜索到个人信息页搜索item按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(120/W_SCREEN*g_w_screen), int(221/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(220), int(391))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(220), int(391))
    return APP_RET_CODE_SUCESS
#adb_click_search_item_btn_for_searched_person_page()

# 点击通讯录页面的新的朋友item按钮
def adb_click_new_friend_item_btn_for_auto_pass():
    # chenyj debug
    print("动作:【点击通讯录页面的新的朋友item按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(456/W_SCREEN*g_w_screen), int(160/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(271), int(287))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(271), int(287))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(int(178+G_X_PIAN_YI), int(185+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS
#adb_click_new_friend_item_btn_for_auto_pass()

# 点击添加到通讯录按钮
def adb_click_add_to_friendbook_btn():
    # chenyj debug
    print("动作:【点击添加到通讯录双按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(544/W_SCREEN*g_w_screen), int(616/H_SCREEN*g_h_screen))
        adb_click(int(544/W_SCREEN*g_w_screen), int(526/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(43), int(1068))
        adb_click(int(43), int(948))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(369), int(654))
        adb_click(int(369), int(554))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        adb_click(int(250+G_X_PIAN_YI), int(379+G_Y_PIAN_YI))
    return APP_RET_CODE_SUCESS
#adb_click_add_to_friendbook_btn()

# 点击设置备注和标签按钮
def adb_click_set_remark_btn():
    # chenyj debug
    print("动作:【点击设置备注和标签按钮】")
    adb_click(int(109/W_SCREEN*g_w_screen), int(332/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_set_remark_btn()

# 点击设置备注和标签页面的保存按钮 
def adb_click_save_btn_of_setting_remark():
    # chenyj debug
    print("动作:【点击设置备注和标签页面的保存按钮】")
    adb_click(int(1011/W_SCREEN*g_w_screen), int(78/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_save_btn_of_setting_remark()

 
# 点击添加到通讯录(文件传输助手)页的添加到通讯录按钮
def adb_click_add_to_friendbook_of_file_trange_btn():
    # chenyj debug
    print("动作:【点击添加到通讯录(文件传输助手)页的添加到通讯录按钮】")
    adb_click(int(540/W_SCREEN*g_w_screen), int(483/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_add_to_friendbook_of_file_trange_btn()

# 点击添加好友的“发送”按钮
def adb_click_send_btn_for_add_friend():
    # chenyj debug
    print("动作:【点击添加好友的“发送”按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(538/W_SCREEN*g_w_screen), int(1806/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(538), int(2104))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(362), int(1080))
    return APP_RET_CODE_SUCESS
#adb_click_send_btn_for_add_friend()


# 按给出的文本找到按钮，且发现还没完成，就点击按钮
def adb_click_btn_by_ocr_if_no_finish_with_check(input_event, btn_text_list = [], x_click_pian_yi = 0, y_click_pian_yi = 0):

    if len(btn_text_list) <= 0:
        return APP_RET_CODE_UNVALID_PARAM
        
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_adb_click_btn_by_ocr" + ".png"
    if True == os.path.exists(path):
        os.remove(path)
    adb_get_screen(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("adb_click_btn_by_ocr_if_no_finish_with_check, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT
        
    try:
        iRet, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!adb_click_btn_by_ocr_if_no_finish_with_check， get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR
    if json_return is None or iRet != APP_RET_CODE_SUCESS: 
        print_my("!!!!!adb_click_btn_by_ocr_if_no_finish_with_check, get_ocr_result_with_small 失败")
        return APP_RET_CODE_OCR_ERROR
     
    # 执行动作
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        
        # 命中
        b_ming_zhong = False 
        for btn_text in btn_text_list:
            if btn_text in content: 
                b_ming_zhong = True 
                print("找到了[{}]按钮的位置:{}".format(btn_text, result))
                break 
        #if btn_text in content:
            #print("找到了[{}]按钮的位置:{}".format(btn_text, result))
        if b_ming_zhong == True:
            # 判断是否已经完成
            for result_ in json_return["words_result"]:
                content_ = result_["words"]
                x_ = result_["location"]["left"]
                y_ = result_["location"]["top"]
                width_ = result_["location"]["width"]
                height_ = result_["location"]["height"]
                if y_ > y and y_ < y + 80 and content_ == "已完成":
                    print("发现此按钮对应是已完成的")
                    return APP_RET_CODE_HAS_FINISH    
            x_click = int(x + int(width/2)) + x_click_pian_yi
            y_click = int(y + int(height/2)) + y_click_pian_yi
            #print("动作:【点击按钮({}, {})】".format(x_click, y_click))
            # chenyj 这里加入判断像素是否变化的开始
            image_check_begin()
            adb_click(x_click, y_click)
            iRet = wait_image_change(input_event, 0.998)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("adb_click_btn_by_ocr_if_no_finish_with_check, 被要求退出2")
                return iRet
    
            return APP_RET_CODE_SUCESS
         
    return APP_RET_CODE_UNKNOW

# 截取搜索页的群聊的截图  
def get_screen_of_qun_liao_of_search_page(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v17.png"   
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        y_pian_cha = 138 
        bbox = (int(20/W_SCREEN*g_w_screen), int(y_pian_cha/H_SCREEN*g_h_screen), int(440/W_SCREEN*g_w_screen), int(465/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        y_pian_cha = 242 
        bbox = (int(38/W_SCREEN*g_w_screen), int(y_pian_cha/H_SCREEN*g_h_screen), int(888/W_SCREEN*g_w_screen), int(700/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        y_pian_cha = 242 
        bbox = (int(38/W_SCREEN*g_w_screen), int(y_pian_cha/H_SCREEN*g_h_screen), int(888/W_SCREEN*g_w_screen), int(700/H_SCREEN*g_h_screen))
    
    #print_my(bbox)
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, y_pian_cha
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS, y_pian_cha
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_has_searched_group" + ".png"
#get_screen_of_qun_liao_of_search_page(path)

# 判断搜索页中是否有搜索到群 
def has_searched_group_of_search_page(input_event):
    i_pos_y = -1
    
    TIME_BEGIN()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_has_searched_group" + ".png"
    _, y_pian_cha = get_screen_of_qun_liao_of_search_page(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("has_searched_group_of_search_page, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, i_pos_y
        
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!has_searched_group_of_search_page get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, i_pos_y
    if json_return is None: 
        print_my("!!!!!has_searched_group_of_search_page, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR, i_pos_y

    #if len(json_return["words_result"]) == 2:
    #    json_return["words_result"] = [json_return["words_result"][0]]
    #if len(json_return["words_result"]) != 1:   
    #    return APP_RET_CODE_FRIEND_NO_FOUND, i_pos_y
    #print(json_return)
    b_exist = False
    all_content = ""
    for result in json_return["words_result"]:
        content = result["words"]
        all_content += content
    for result in json_return["words_result"]:
        content = result["words"]
        if "创建新的群聊":
            continue
        if "群聊" in content or "最常使用" in content:
            b_creat_new_group = False
            for result_ in json_return["words_result"]:
                content_ = result_["words"]
                interal_y = result_["location"]["top"] - result["location"]["top"]
                if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
                    interal_y_max = 90
                elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
                    interal_y_max = 110
                elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
                    interal_y_max = 110
                if "创建新的群聊" in content_ and (interal_y > 10 and interal_y < interal_y_max):
                    b_creat_new_group = True
                    break
            if b_creat_new_group == True:
                continue
            else:
                b_exist = True
                continue
        if b_exist == True:
            i_pos_y = int(result["location"]["top"] + y_pian_cha)
            break
        #break
    if b_exist == True:
        return RET_SUCESS, i_pos_y
    
    TIME_END()
    
    return APP_RET_CODE_FRIEND_NO_FOUND, i_pos_y
# 测试
#iRet, i_pos_y = has_searched_group_of_search_page(g_Event_test)
#print("是否已经搜索到群:{}, i_pos_y:{}".format("是" if iRet == RET_SUCESS else "否", i_pos_y))

# 截取搜索页的群聊的截图  
def get_screen_of_members_of_chat_info_page(path):
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        y_pian_cha = 191 
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        y_pian_cha = 237
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        y_pian_cha = 237
         
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v18.png"  
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (int(0/W_SCREEN*g_w_screen), int(y_pian_cha/H_SCREEN*g_h_screen), int(g_w_screen/W_SCREEN*g_w_screen), int(g_h_screen/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(0/W_SCREEN*g_w_screen), int(y_pian_cha/H_SCREEN*g_h_screen), int(g_w_screen/W_SCREEN*g_w_screen), int(g_h_screen/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(0/W_SCREEN*g_w_screen), int(y_pian_cha/H_SCREEN*g_h_screen), int(g_w_screen/W_SCREEN*g_w_screen), int(g_h_screen/H_SCREEN*g_h_screen))

    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, y_pian_cha
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS, y_pian_cha
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_group_member" + ".png"
#get_screen_of_members_of_chat_info_page(path)

# 点击聊天页中的“聊天信息”按钮
def adb_click_chat_info_btn_of_chat_page():
    # chenyj debug
    print("动作:【点击聊天页中的“聊天信息”按钮】")
    adb_click(int(1023/W_SCREEN*g_w_screen), int(77/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_chat_info_btn_of_chat_page()

# 获得页面中的所有的群成员的信息 
def get_members_info_of_chat_info_page(input_event):
    json_return = {}
    
    TIME_BEGIN()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_group_member" + ".png"
    _, y_pian_cha = get_screen_of_members_of_chat_info_page(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("get_members_info_of_chat_info_page, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, json_return
        
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!get_members_info_of_chat_info_page get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, json_return
    if json_return is None: 
        print_my("!!!!!get_members_info_of_chat_info_page, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR, json_return

    #print(json_return)
    # 对y坐标进行调整
    for result in json_return["words_result"]:
        content = result["words"]
        result["location"]["top"] = result["location"]["top"] + y_pian_cha
       
    TIME_END()
    
    return RET_SUCESS, json_return
    
    #return APP_RET_CODE_FRIEND_NO_FOUND, i_pos_y
# 测试
#iRet, json_return = get_members_info_of_chat_info_page(g_Event_test)

# 按策略添加群里的好友
def add_friends_in_group_with_check(input_event, groupname, username_has_add_list, remark_prefix, b_debug = True):
    username_new_add_list = []
    
    # 点击搜索按钮
    image_check_begin()
    adb_click_search_btn()
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_friends_in_group_with_check, 被要求退出1")
        else:
            print_my("!!!!, 找群{}失败({})".format(groupname, iRet))
        ensure_in_message_list_page(input_event)
        return iRet, username_new_add_list
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Search])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!!add_friends_in_group_with_check,当前不是在搜索页")
        return iRet, username_new_add_list
    
    # 粘贴文本    
    # chenyj test
    groupname_of_before_emoji = clean_string(groupname)
    # 使之能模糊匹配
    groupname_of_before_emoji = insert_star_except_between_digits(groupname_of_before_emoji)
    #username_of_before_emoji = "*".join(username_of_before_emoji)
    groupname_of_before_emoji = "*" + groupname_of_before_emoji
    if groupname_of_before_emoji == "*":
        # chenyj test 临时处理
        if "?" == groupname:
            groupname = "？"
        groupname_of_before_emoji = groupname
    image_check_begin()
    adb_paste_text(groupname_of_before_emoji, b_debug)
    #adb_paste_text(username, b_debug)
    #if True == input_event.wait(0.9):
    #    print_my("add_friends_in_group_with_check, 被要求退出2")
    #    ensure_in_message_list_page(input_event, PageType.Search)
    #    return -1 
    iRet = wait_image_change(input_event, 0.997)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_friends_in_group_with_check, 被要求退出2")
        else:
            print_my("!!!!, 找群{}失败({})".format(groupname, iRet))
        ensure_in_message_list_page(input_event, PageType.Search)
        return iRet, username_new_add_list
    
    # 判断搜索页中是否有搜索到群 
    iRet, i_pos_y = has_searched_group_of_search_page(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_friends_in_group_with_check, 被要求退出3")
        else:
            print_my("!!!无法搜索到群{}:{}".format(iRet, groupname))
            upload_snape()
        adb_click_back()
        _ = ensure_in_message_list_page(input_event, PageType.Search)
        return iRet, username_new_add_list
    
    # 选中
    image_check_begin()
    adb_click_search_item_btn(i_pos_y)
    iRet = wait_image_change(input_event, 0.998)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_friends_in_group_with_check, 被要求退出4")
        ensure_in_message_list_page(input_event, PageType.Chat)
        ensure_in_message_list_page(input_event, PageType.Search)
        return iRet, username_new_add_list

    # 点击聊天信息页
    image_check_begin()
    adb_click_chat_info_btn_of_chat_page()
    iRet = wait_image_change(input_event, 0.998)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_friends_in_group_with_check, 被要求退出5")
        ensure_in_message_list_page(input_event, PageType.GroupInfo)
        return iRet, username_new_add_list
    
    # 点击“查看更多群成员”按钮
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["更多群成员"])
    if iRet != APP_RET_CODE_SUCESS:
        if iRet != -1:
            iRet = APP_RET_CODE_GROUP_HAS_RELEASE
        ensure_in_message_list_page(input_event)
        return iRet, username_new_add_list
    
    # 获得OCR结果,然后循环加好友
    iRet, json_return = get_members_info_of_chat_info_page(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        ensure_in_message_list_page(input_event)
        return iRet, username_new_add_list
    
    remark_prefix = get_remark_prefix_str(remark_prefix)
    for i, result in enumerate(json_return["words_result"]):
        username = result["words"]
        
        if username in username_has_add_list:
            print("此好友已经添加过了:{}".format(username))
            continue
        if len(username_new_add_list) >= MAX_ADD_FRIEND_COUNT:
            print("达到此次加群好友的个数({}/{})，我将结束此将群加友循环".format(len(username_new_add_list), MAX_ADD_FRIEND_COUNT))
            adb_click_back_with_check(input_event, 2)
            ensure_in_message_list_page(input_event)
            return APP_RET_CODE_NO_FINISH, username_new_add_list
        
        username_new_add_list.append(username)
        
        # 跑过前面3个（很有可能是群主）
        if i <= 7 and len(username_has_add_list) == 0:
            print("跳过群好友:{}".format(username))
            continue
        
        b_in_GroupMember_page = False
        for j in range(3):
            iRet, _ = is_in_page(input_event, [PageType.GroupMember], 3)
            if iRet == RET_SUCESS:
                b_in_GroupMember_page = True
                break
            adb_click_back_with_check(input_event, 1) 
        if b_in_GroupMember_page == False:
            print("一直无法回到群成员页，我将结束此将群加友循环")
            ensure_in_message_list_page(input_event)
            return APP_RET_CODE_NO_FINISH, username_new_add_list

        
        print("准备要加的好友是:{}. {}/{}".format(username, i, len(json_return["words_result"])))
        
        # 点击成员
        image_check_begin()
        adb_click(result["location"]["left"], result["location"]["top"])
        iRet = wait_image_change(input_event, 0.998)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("add_friends_in_group_with_check, 被要求退出6")
            ensure_in_message_list_page(input_event, PageType.GroupInfo)
            return iRet, username_new_add_list

        #
        # 点击添加到通讯录按钮 
        iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["添加到通讯录"])
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("add_friends_in_group_with_check, 被要求退出7")
                adb_click_back_with_check(input_event, 4)
                ensure_in_message_list_page(input_event)
                return -1, username_new_add_list
            else:
                print_my("!!!!, 加群好友{}失败({})".format(username, iRet))
            #adb_click_back_with_check(input_event, 3)
            #return iRet 
            continue
        #
        #
        # 点击申请添加好友页面的备注编辑框 
        image_check_begin()
        adb_click_remark_edit_of_apply_add()
        if True == input_event.wait(0.3):
            print_my("add_friends_in_group_with_check, 被要求退出8")
            adb_click_back_with_check(input_event, 4)
            ensure_in_message_list_page(input_event)
            return -1, username_new_add_list
        
        iRet = wait_image_change(input_event, 0.99995)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("add_friends_in_group_with_check, 被要求退出9")
                adb_click_back_with_check(input_event, 4)
                ensure_in_message_list_page(input_event)
                return -1, username_new_add_list        
            else:
                print_my("!!!!, 加群好友{}失败({})".format(username, iRet))
            #ensure_in_message_list_page(input_event)
            #return iRet
            continue
        #
        # 粘贴备注
        adb_paste_text(remark_prefix, b_debug)
        if True == input_event.wait(0.5):
            print_my("add_friends_in_group_with_check, 被要求退出10")
            adb_click_back_with_check(input_event, 4)
            ensure_in_message_list_page(input_event)
            return -1, username_new_add_list
        #     
        time.sleep(0.7)
        
        # 点击发送按钮
        image_check_begin()
        adb_click_send_btn_for_add_friend()
        iRet = wait_image_change(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("add_friends_in_group_with_check, 被要求退出11")
                adb_click_back_with_check(input_event, 4)
                ensure_in_message_list_page(input_event)
                return -1, username_new_add_list 
            else:
                print_my("!!!!, 加群好友{}失败({})".format(username, iRet))
            #adb_click_back_with_check(input_event, 3)
            continue 

        # 因为有一闪的过程，所以这里等待一下
        time.sleep(0.9)     
        print_my("【加群好友】成功发送[{}]".format(username))
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            adb_click_back_with_check(input_event, 1)
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            adb_click_back_with_check(input_event, 3)
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            adb_click_back_with_check(input_event, 3)
        continue
        
    ensure_in_message_list_page(input_event)
    
    return APP_RET_CODE_SUCESS, username_new_add_list
#
#iRet, username_new_add_list = add_friends_in_group_with_check(g_Event_test, "鲸跃资源-前端后端对接", [], "【字符】：随机加的")

# 添加好友(windows)
def add_new_frient_with_check_windows(input_event, username, remark_prefix, b_debug = True):
    remark_prefix = get_remark_prefix_str(remark_prefix, username)
               
    # 点击编辑框 
    image_check_begin()
    adb_click_edit_of_add_friend()
    if True == input_event.wait(0.3):
        print_my("add_new_frient_with_check_windows, 被要求退出1")
        TIME_END()
        return -1  
    iRet = wait_image_change(input_event, 0.9994)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check_windows, 被要求退出2")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        return iRet
        
    # 粘贴文本  
    time.sleep(0.5)
    adb_paste_text(username, b_debug)
    if True == input_event.wait(0.5):
        print_my("add_new_frient_with_check_windows, 被要求退出3")
        return -1  
    #     
    time.sleep(1)
    
    # 点击搜索item
    """
    image_check_begin()
    adb_click_search_item_btn_for_add_friend()
    iRet = wait_image_change(input_event, 0.996)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check_windows, 被要求退出4")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        return iRet 
    """
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["网络查找手机"])
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check_windows, 被要求退出4")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        return iRet 
    #     
    time.sleep(2)
    #
    # 确保是在"添加到通讯录"页
    i_count = 0
    while i_count < WAIT_ENTER_ADD_FRIEND_PAGE_CONT_MAX:
        i_count += 1
        #iRet, page_type_return, _ = get_page_type_by_tesseract(input_event)
        iRet, page_type_return, _ = get_page_type_by_ocr(input_event)
        if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
            print_my("add_new_frient_with_check_windows, 被要求退出5")
            adb_click_back_with_check(input_event, 2)
            return iRet
        if iRet != APP_RET_CODE_SUCESS:
            adb_click_back_with_check(input_event, 2)
            return iRet
        
        if page_type_return == PageType.Friend_No_Exist:
            i_return = APP_RET_CODE_CANNOT_ADD
            print_my("!!!!账号[{}]不存在".format(username))
            adb_click_close_add_to_friendbook_when_no_exist_btn()
            return i_return
        elif page_type_return == PageType.Friend_Information:
            i_return = APP_RET_CODE_CANNOT_ADD
            print_my("!!!!账号[{}]已添加过".format(username))
            adb_click_back_with_check(input_event, 3)
            return i_return
        elif page_type_return == PageType.Friend_Person_Exist:
            print("!!!!好友[{}]搜索到了，但在个人信息搜索到页面，还要再点击一次".format(username))
            # 点击搜索item
            image_check_begin()
            adb_click_search_item_btn_for_searched_person_page()
            iRet = wait_image_change(input_event, 0.996)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("add_new_frient_with_check_windows, 被要求退出6")
                else:
                    print_my("!!!!, 444 加好友{}失败({})".format(username, iRet))
                adb_click_back_with_check(input_event, 3)
                return iRet 
        
        if page_type_return == PageType.Add_to_FriendBook:
            break 
        
        if True == input_event.wait(1):
            print_my("add_new_frient_with_check_windows, 被要求退出7")
            return -1     
            
        continue 
    if i_count >= WAIT_ENTER_ADD_FRIEND_PAGE_CONT_MAX:
        i_return = APP_RET_CODE_UNKNOW
        print_my("!!!!添加好友[{}]失败".format(username))
        #adb_click_back_with_check(input_event, 2)
        ensure_in_message_list_page(input_event)
        return i_return
    #
    #
    # 点击添加到通讯录按钮 
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["添加到通讯录"])
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check_windows, 被要求退出8")

        else:
            print_my("!!!!, 加群好友{}失败({})".format(username, iRet))
        adb_click_close_add_to_friendbook_btn()
        ensure_in_message_list_page(input_event)
        return iRet
    time.sleep(2)
    #
    #
    # 点击申请添加好友页面的备注编辑框 
    image_check_begin()
    adb_click_remark_edit_of_apply_add()
    if True == input_event.wait(0.3):
        print_my("add_new_frient_with_check_windows, 被要求退出9")
        adb_click_close_apply_add_btn(input_event)
        time.sleep(1.5)
        adb_click_close_add_to_friendbook_btn()
        ensure_in_message_list_page(input_event)
        return -1
    
    iRet = wait_image_change(input_event, 0.99995)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check_windows, 被要求退出10")     
        else:
            print_my("!!!!, 加群好友{}失败({})".format(username, iRet))
        adb_click_close_apply_add_btn(input_event)
        time.sleep(1.5)
        adb_click_close_add_to_friendbook_btn()
        ensure_in_message_list_page(input_event)
        return iRet
    #
    # 粘贴备注
    adb_paste_text(remark_prefix, b_debug)
    if True == input_event.wait(0.5):
        print_my("add_new_frient_with_check_windows, 被要求退出11")
        adb_click_close_apply_add_btn(input_event)
        time.sleep(1.5)
        adb_click_close_add_to_friendbook_btn()
        ensure_in_message_list_page(input_event)
        return -1
    #     
    time.sleep(0.7)
    
    # 点击发送按钮
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["确定"])
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check_windows, 被要求退出8")
        else:
            print_my("!!!!, 加群好友{}失败({})".format(username, iRet))
        adb_click_close_apply_add_btn(input_event)
        time.sleep(1.5)
        adb_click_close_add_to_friendbook_btn()
        ensure_in_message_list_page(input_event)
        return iRet
    time.sleep(1.5)
    
    adb_click_close_add_to_friendbook_btn()
    time.sleep(0.5)
    ensure_in_message_list_page(input_event)
    return iRet
    
# 添加好友
def add_new_frient_with_check(input_event, username, remark_prefix, b_debug = True):
    remark_prefix = get_remark_prefix_str(remark_prefix, username)
    
    # 点击添加好友按钮
    image_check_begin()
    adb_click_add_btn()
    if True == input_event.wait(0.5):
        print_my(", 被要求退出1")
        return -1 
    adb_click_add_friend_btn()
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出2")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        ensure_in_message_list_page(input_event)
        return iRet
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Add_Frient])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!!add_new_frient_with_check,当前不是在添加朋友页")
        return iRet
            
    # 点击编辑框 
    image_check_begin()
    adb_click_edit_of_add_friend()
    if True == input_event.wait(0.3):
        print_my("add_new_frient_with_check, 被要求退出3")
        TIME_END()
        adb_click_back_with_check(input_event, 2)
        return -1  
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出4")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        ensure_in_message_list_page(input_event)
        return iRet
        
    # 粘贴文本  
    adb_paste_text(username, b_debug)
    if True == input_event.wait(0.5):
        print_my("add_new_frient_with_check, 被要求退出5")
        adb_click_back_with_check(input_event, 2)
        return -1  
    #     
    time.sleep(1)
    
    # 点击搜索item
    image_check_begin()
    adb_click_search_item_btn_for_add_friend()
    iRet = wait_image_change(input_event, 0.996)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出6")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        adb_click_back_with_check(input_event, 2)
        return iRet 
    #     
    time.sleep(0.5)
    #
    # 确保是在"添加到通讯录"页
    i_count = 0
    while i_count < WAIT_ENTER_ADD_FRIEND_PAGE_CONT_MAX:
        i_count += 1
        #iRet, page_type_return, _ = get_page_type_by_tesseract(input_event)
        iRet, page_type_return, _ = get_page_type_by_ocr(input_event)
        if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
            print_my("add_new_frient_with_check, 被要求退出7")
            adb_click_back_with_check(input_event, 2)
            return iRet
        if iRet != APP_RET_CODE_SUCESS:
            adb_click_back_with_check(input_event, 2)
            return iRet
        
        if page_type_return == PageType.Friend_No_Exist:
            i_return = APP_RET_CODE_CANNOT_ADD
            print_my("!!!!账号[{}]不存在".format(username))
            adb_click_close_add_to_friendbook_when_no_exist_btn()
            return i_return
        elif page_type_return == PageType.Friend_Information:
            i_return = APP_RET_CODE_CANNOT_ADD
            print_my("!!!!账号[{}]已添加过".format(username))
            adb_click_back_with_check(input_event, 3)
            return i_return
        elif page_type_return == PageType.Friend_Person_Exist:
            print("!!!!好友[{}]搜索到了，但在个人信息搜索到页面，还要再点击一次".format(username))
            # 点击搜索item
            image_check_begin()
            adb_click_search_item_btn_for_searched_person_page()
            iRet = wait_image_change(input_event, 0.996)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("add_new_frient_with_check, 被要求退出8")
                else:
                    print_my("!!!!, 444 加好友{}失败({})".format(username, iRet))
                adb_click_back_with_check(input_event, 3)
                return iRet 
        
        if page_type_return == PageType.Add_to_FriendBook:
            break 
        
        if True == input_event.wait(1):
            print_my("add_new_frient_with_check, 被要求退出9")
            return -1     
            
        continue 
    if i_count >= WAIT_ENTER_ADD_FRIEND_PAGE_CONT_MAX:
        i_return = APP_RET_CODE_UNKNOW
        print_my("!!!!添加好友[{}]失败".format(username))
        #adb_click_back_with_check(input_event, 2)
        ensure_in_message_list_page(input_event)
        return i_return
    """
    # 
    # 设置好友备注
    # 点击设置备注和标签按钮 
    image_check_begin()
    adb_click_set_remark_btn()
    iRet = wait_image_change(input_event, 0.99)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出9")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        adb_click_back_with_check(input_event, 2)
        return iRet 
    
    time.sleep(0.2)  
    
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Setting_Remark])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!!add_new_frient_with_check,当前不是在设置备注和标签页")
        return iRet
    
    #
    # 点击设置备注和标签页面的备注编辑框 
    image_check_begin()
    adb_click_edit_of_setting_remark()
    if True == input_event.wait(0.3):
        print_my("add_new_frient_with_check, 被要求退出10")
        TIME_END()
        adb_click_back_with_check(input_event, 4)
        return -1  
    iRet = wait_image_change(input_event, 0.9999)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出11")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        ensure_in_message_list_page(input_event)
        return iRet
    #
    # 粘贴文本  
    adb_paste_text(remark_prefix, b_debug)
    if True == input_event.wait(0.5):
        print_my("add_new_frient_with_check, 被要求退出12")
        adb_click_back_with_check(input_event, 2)
        return -1  
    #     
    time.sleep(1)
    #
    # 点击设置备注和标签页面的保存按钮 
    image_check_begin()
    adb_click_save_btn_of_setting_remark()
    iRet = wait_image_change(input_event, 0.99)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出13")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        adb_click_back_with_check(input_event, 3)
        return iRet 
    #
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Add_to_FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!!add_new_frient_with_check,当前不是在添加到通讯录页")
        return iRet
    """
    #
    time.sleep(0.5)
    #
    # 点击添加按钮 
    image_check_begin()
    adb_click_add_to_friendbook_btn()
    iRet = wait_image_change(input_event, 0.99)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出14")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        adb_click_back_with_check(input_event, 3)
        return iRet 
    #
    #
    # 点击申请添加好友页面的备注编辑框 
    image_check_begin()
    adb_click_remark_edit_of_apply_add()
    if True == input_event.wait(0.3):
        print_my("add_new_frient_with_check, 被要求退出15")
        TIME_END()
        adb_click_back_with_check(input_event, 4)
        return -1  
    iRet = wait_image_change(input_event, 0.9999)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_new_frient_with_check, 被要求退出16")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        ensure_in_message_list_page(input_event)
        return iRet
    #
    # 粘贴备注
    adb_paste_text(remark_prefix, b_debug)
    if True == input_event.wait(0.5):
        print_my("add_new_frient_with_check, 被要求退出17")
        adb_click_back_with_check(input_event, 2)
        return -1  
    #     
    time.sleep(0.7)
    
    # 点击发送按钮
    image_check_begin()
    adb_click_send_btn_for_add_friend()
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my(", 被要求退出18")
        else:
            print_my("!!!!, 加好友{}失败({})".format(username, iRet))
        adb_click_back_with_check(input_event, 3)
        return iRet 
    # 因为有一闪的过程，所以这里等待一下
    time.sleep(0.5)     
    adb_click_back_with_check(input_event, 3, 0.9925)  
    
    return APP_RET_CODE_SUCESS
#add_new_frient_with_check(g_Event_test, "15280006531", "当前日期")
   
# 将消息列表中的用户置顶
def set_username_top_with_check(input_event, username):
    global g_monitor_object_info_dict
    iRet = APP_RET_CODE_UNKNOW
    
    iRet, username_failed = get_monitor_rect_of_new_msg(input_event, [username], False, True) 
    if iRet != APP_RET_CODE_SUCESS:
        print("set_username_top_with_check失败, {}".format(iRet))
        return iRet
    
    iRet = APP_RET_CODE_UNKNOW
    for username_ in g_monitor_object_info_dict:
        if username_ == username:
            if "rect_of_new_msg" not in g_monitor_object_info_dict[username_]:
                continue
            rect_of_new_msg_of_username = g_monitor_object_info_dict[username_]["rect_of_new_msg"]
            print("set_username_top_with_check, 微信用户[{}]的新消息区域锚定:{}".format(username, rect_of_new_msg_of_username))

            # 
            # 判断用户是不是已经置顶
            temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v2.png"  
            try:
                img = Image.open(temp_png) 
                x = rect_of_new_msg_of_username[0] + 22
                y = rect_of_new_msg_of_username[1]
                bbox = (x, y, x + 10, y + 10)
                cropped_img = img.crop(bbox)
                crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_is_top.png"
                cropped_img.save(crop_path)
                crop_mage = imread(crop_path)
                if False == image_is_white(crop_mage):
                    print("!!!【{}】已经是置顶了".format(username))
                    return APP_RET_CODE_SUCESS
            except Exception as e:
                print("!!!!set_username_top_with_check异常\n{}".format(e))
                return APP_RET_CODE_UNKNOW
            
            # 长按
            image_check_begin()
            # [lt_x_of_new_msg, lt_y_of_new_msg, rb_x_of_new_msg, rb_y_of_new_msg]
            if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
                windows_right_click(rect_of_new_msg_of_username[0], rect_of_new_msg_of_username[1])
            else:
                adb_longpress(rect_of_new_msg_of_username[0], rect_of_new_msg_of_username[1])
            iRet = wait_image_change(input_event, 0.998)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("set_username_top_with_check, 被要求退出3")
                else:
                    print_my("set_username_top_with_check!!!!, 长按用户{}失败({})".format(username, iRet))
                return iRet
            #
            # 选择“置顶该聊天”
            image_check_begin()
            adb_click(rect_of_new_msg_of_username[0] + 26, rect_of_new_msg_of_username[1] + 26)
            iRet = wait_image_change(input_event, 0.997)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("set_username_top_with_check, 被要求退出4")
                else:
                    print_my("set_username_top_with_check!!!!, 按用户{}置顶该聊天失败({})".format(username, iRet))
                return iRet
            print("【{}】成功置顶".format(username))
            iRet = APP_RET_CODE_SUCESS
            break 
            
    return iRet
    
# 增加一个托管对象到消息列表页中并置顶
def add_deposit_to_frient_list_and_set_top_with_check(input_event, username, b_debug = True):
    # 点击编辑框 
    image_check_begin()
    adb_click_edit_of_add_friend()
    if True == input_event.wait(0.3):
        print_my("add_deposit_to_frient_list_and_set_top_with_check, 被要求退出1")
        TIME_END()
        return -1  
    iRet = wait_image_change(input_event, 0.9994)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_deposit_to_frient_list_and_set_top_with_check, 被要求退出2")
        else:
            print_my("!!!!,添加用户{}到列表失败({})".format(username, iRet))
        return iRet
    if True == input_event.wait(0.3):
        print_my("add_deposit_to_frient_list_and_set_top_with_check, 被要求退出3")
        TIME_END()
        return -1  
    
    # 粘贴文本  
    adb_paste_text(username, b_debug)
    if True == input_event.wait(0.5):
        print_my("wait_image_change, 被要求退出2")
        ensure_in_message_list_page(input_event, PageType.Search)
        return -1 
    # 选中
    image_check_begin()
    adb_click_search_item_btn_for_add_friend()
    iRet = wait_image_change(input_event, 0.998)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_deposit_to_frient_list_and_set_top_with_check, 被要求退出4")
        else:
            print_my("!!!!, 添加用户{}到列表失败({})".format(username, iRet))
        return iRet 
    # 
    # 对于从来没用过“文件传输助手”的用户，此时会遇到“添加到通讯录(文件传输助手)页”，要做特殊处理
    iRet, _ = is_in_page(input_event, [PageType.Add_to_FriendBook_FILE_CHANGE], 1)
    if iRet == APP_RET_CODE_SUCESS:
        print("add_deposit_to_frient_list,当前是在添加到通讯录(文件传输助手)页")
        # 点击添加按钮 
        image_check_begin()
        adb_click_add_to_friendbook_of_file_trange_btn()
        iRet = wait_image_change(input_event, 0.99)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("add_deposit_to_frient_list, 被要求退出5")
            else:
                print_my("!!!!, 添加加好友{}失败({})".format(username, iRet))
            adb_click_back_with_check(input_event, 2)
            return iRet 
            
        # 点击发送按钮
        image_check_begin()
        adb_click_send_btn_for_add_friend()
        iRet = wait_image_change(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("add_deposit_to_frient_list, 被要求退出6")
            else:
                print_my("!!!!, 添加加好友{}失败({})".format(username, iRet))
            adb_click_back_with_check(input_event, 3)
            return iRet 
            
        #
        # 点击发送消息按钮
        # 说明：这个现在还没做（怎么做，参考通用加好友的过程）
        pass  
        
    # 点击编辑框 
    adb_click_chat_edit_for_send_btn()
    if True == input_event.wait(0.5):
        print_my("add_deposit_to_frient_list, 被要求退出7")
        ensure_in_message_list_page(input_event, PageType.Chat)
        ensure_in_message_list_page(input_event, PageType.Search)
        return -1 
    # 粘贴草稿文字
    adb_paste_text("1", b_debug)
    if True == input_event.wait(0.5):
        print_my("wait_image_change, 被要求退出8")
        ensure_in_message_list_page(input_event, PageType.Chat)
        ensure_in_message_list_page(input_event, PageType.Search)
        return -1 

    # 
    # 置顶(此动作不允许被用户退出)
    iRet = set_username_top_with_check(g_Event_test, username)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("add_deposit_to_frient_list, 被要求退出9")
        else:
            print_my("!!!!, 置顶失败({})".format(username, iRet))
        return iRet 
    
    return APP_RET_CODE_SUCESS
#add_deposit_to_frient_list(g_Event_test, USERNAME_FOR_NOTICE)

# 截取搜索页的联系人的截图
def get_screen_of_lian_xi_ren_of_search_page(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v13.png"      
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (int(20/W_SCREEN*g_w_screen), int(138/H_SCREEN*g_h_screen), int(113/W_SCREEN*g_w_screen), int(165/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(30), int(244), int(232), int(288))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(30), int(244), int(232), int(288))
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)

    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_has_searched_frient" + ".png"
#get_screen_of_lian_xi_ren_of_search_page(path)

# 判断搜索页中是否有搜索到好友 
def has_searched_friend_of_search_page(input_event):

    TIME_BEGIN()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_has_searched_frient" + ".png"
    get_screen_of_lian_xi_ren_of_search_page(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("has_searched_friend_of_search_page, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT
        
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!has_searched_friend_of_search_page get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR
    if json_return is None: 
        print_my("!!!!!has_searched_friend_of_search_page, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR

    if len(json_return["words_result"]) == 2:
        json_return["words_result"] = [json_return["words_result"][0]]
    if len(json_return["words_result"]) != 1:   
        return APP_RET_CODE_FRIEND_NO_FOUND
    
    for result in json_return["words_result"]:
        content = result["words"]
        if "联系人" in content or "最常使用" in content:
            return RET_SUCESS
        break
    TIME_END()
    
    return APP_RET_CODE_FRIEND_NO_FOUND
# 测试
#iRet = has_searched_friend_of_search_page(g_Event_test)
#print("是否已经搜索到好友:{}".format("是" if iRet == RET_SUCESS else "否"))

# 通过搜索流程给某用户发送消息
def send_message_by_search(input_event, username,  msg_str, img_paths, b_debug = True):
    i_send_img_count = 0
    b_in_need_check_is_chat = False
    
    # 先把图片通过adb传到手机里
    for img_path in img_paths:
        # 判断图片是否存在 
        if os.path.isfile(img_path) == True: 
            adb_send_image_to_phone(img_path)
            i_send_img_count += 1
        else:
            print("!!!send_message_by_search, 图片{}不存在啊".format(img_path))
    # chenyj debug
    if i_send_img_count == 0:
        print("此次回答是文本回答模式")
    else:
        print("此次回答是图片回答模式")
        
    image_check_begin()
    adb_click_search_btn()
    iRet = wait_image_change(input_event, 0.995)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_message_by_search, 被要求退出1")
        ensure_in_message_list_page(input_event)
        return iRet
    
    # 粘贴文本    
    # chenyj test
    username_of_before_emoji = clean_string(username)
    # 使之能模糊匹配
    username_of_before_emoji = insert_star_except_between_digits(username_of_before_emoji)
    #username_of_before_emoji = "*".join(username_of_before_emoji)
    username_of_before_emoji = "*" + username_of_before_emoji
    if username_of_before_emoji == "*":
        # chenyj test 临时处理
        if "?" == username:
            username = "？"
        username_of_before_emoji = username
    adb_paste_text(username_of_before_emoji, b_debug)
    #adb_paste_text(username, b_debug)
    if True == input_event.wait(0.5):
        print_my("send_message_by_search, 被要求退出2")
        ensure_in_message_list_page(input_event, PageType.Search)
        return -1 
    # 判断是否有搜索到好友 
    iRet = has_searched_friend_of_search_page(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_message_by_search, 被要求退出3")
        else:
            print_my("!!!无法搜索到好友{}:{}".format(iRet, username))
            upload_snape()
        adb_click_back()
        _ = ensure_in_message_list_page(input_event, PageType.Search)
        return iRet
    
        
    # 选中
    image_check_begin()
    adb_click_search_item_btn()
    iRet = wait_image_change(input_event, 0.998)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_message_by_search, 被要求退出4")
        ensure_in_message_list_page(input_event, PageType.Chat)
        ensure_in_message_list_page(input_event, PageType.Search)
        return iRet
        
    #
    # 确保是在"聊天"页
    i_count = 0
    while i_count < TRY_COUNT_MAX_FOR_CHAT:
        i_count += 1
        iRet, b_is_in_chat, user_name_of_chat = is_in_chat_page_by_title()
        if iRet != APP_RET_CODE_SUCESS:
            ensure_in_message_list_page(input_event)
            return iRet
        if b_is_in_chat == True:
            break

        if True == input_event.wait(1):
            print_my("send_message_by_search, 被要求退出5")
            return -1     
            
        continue 
    if i_count >= TRY_COUNT_MAX_FOR_CHAT:
        iRet = APP_RET_CODE_UNKNOW
        print_my("!!!!通过搜索流程给某用户[{}]发送消息失败".format(username))
        ensure_in_message_list_page(input_event)
        return iRet
    # 模式1：发送文本
    if len(msg_str) > 0:
        TRY_COUNT_MAX = 2
        i_try_count = 0
        b_send_ready = False
        while i_try_count < TRY_COUNT_MAX:
            i_try_count += 1
            # 点击编辑框 
            adb_click_chat_edit_for_send_btn()
            if True == input_event.wait(0.3):
                print_my("send_message_by_search, 被要求退出6")
                TIME_END()
                return -1   
            """
            if is_weChat_running() == False:
                print_my("微信应用退出了")
                TIME_END()
                return APP_RET_CODE_APP_EXIT
            """
            # 粘贴文本    
            adb_paste_text(msg_str)
            if True == input_event.wait(0.4):
                print_my("send_message_by_search, 被要求退出7")
                TIME_END()
                return -1  
            # 判断“发送”按钮是否出现
            if b_in_need_check_is_chat == True:
                if is_send_ready() == True:
                    b_send_ready = True
                    break
                else:
                    # chenyj debug
                    print("发送按钮还没出现,继续等待...")
            else: 
                b_send_ready = True
                break
          
        if b_send_ready == False:
            TIME_END()
            return APP_RET_CODE_NO_READY
        # 发送文本
        adb_click_send_btn()
        # 发送完等一下
        if True == input_event.wait(0.4):
            print_my("send_message_by_search, 被要求退出8")
            TIME_END()
            return -1  
    # 模式2：发送图片
    if i_send_img_count != 0:
        # 点击加号按钮 
        adb_click_chat_add_btn()
        if True == input_event.wait(0.3):
            print_my("send_message_by_search, 被要求退出9")
            TIME_END()
            return -1  
        
        # 点击相册按钮
        iRet = adb_click_chat_album_btn_with_check(input_event)
        if iRet == APP_RET_CODE_APP_KA_ZHU:
            print_my("send_message_by_search, 点击相册卡时无效，有异常页面，等待6秒")
            if True == input_event.wait(8):
                print_my("send_message_by_search, 被要求退出10")
                TIME_END()
                return -1  
            # 点击相册按钮
            adb_click_chat_album_btn()

        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Img_And_Video], 6)
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_message_by_search, 当前不是在图片和视频页页面,但我忽略")
            
        # 选中第一张图片按钮
        adb_click_album_first_img_btn()
        if True == input_event.wait(1):
            print_my("send_message_by_search, 被要求退出11")
            TIME_END()
            return -1  
        # 点击发送图片按钮
        adb_click_send_img_btn()
        
    # 返回消息列表页
    """
    image_check_begin()
    adb_click_back_of_chat()
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_message_by_search, 被要求退出12")
        upload_snape()
        return iRet 
    """
        
    image_check_begin()
    adb_click_back()
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_message_by_search, 被要求退出13")
        return iRet
        
    return APP_RET_CODE_SUCESS
#send_message_by_search(g_Event_test, "教培老师◆北辰职校", "测试", [".\\示例图片.JPG"])

# 给主人发送通知消息
def send_bussiness(input_event, msg_str):
    if g_b_Open_Notice == False:
        print("send_bussiness，配置为不需要通知，直接返回")
        return APP_RET_CODE_SUCESS
        
    if input_event == None:
        input_event = g_Event_test
    
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        return iRet
    #
    msg_str = "【个微私域精灵】" + msg_str
    print_my("!!!!给主人手机微信里的[个人传输助手]发送通知:{}".format(msg_str))
    #return send_message_by_search(g_Event_test, USERNAME_FOR_NOTICE, msg_str, False)
    iRet, b_is_groud = enter_chat_ui(input_event, USERNAME_FOR_NOTICE)
    if iRet != 0:
        print_my("!!!!!send_bussiness,失败({})".format(iRet))
        if iRet == APP_RET_CODE_UNEXPECT_CHAT_PAGE:
            adb_click_back_of_chat()
        return iRet
    # 点击编辑框 
    adb_click_chat_edit_for_send_btn(False)
    if True == input_event.wait(0.5):
        print_my("send_bussiness, 被要求退出2")
        return -1 
    # 粘贴文本 
    adb_paste_text(msg_str, False)
    if True == input_event.wait(0.5):
        print_my("send_bussiness, 被要求退出5")
        return -1 
    # 发送文本
    adb_click_send_btn(False)
    if True == input_event.wait(0.5):
        print_my("send_bussiness, 被要求退出6")
        return -1 
        
    return APP_RET_CODE_SUCESS

# 截取朋友圈搜索页搜索后第一个联系人的截图
def get_screen_of_first_username_of_cicle_search_page(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v16.png"       
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (int(166/W_SCREEN*g_w_screen), int(264/H_SCREEN*g_h_screen), int(403/W_SCREEN*g_w_screen), int(350/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(296), int(471), int(965), int(530))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(296), int(471), int(965), int(570))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (int(156), int(255), int(395), int(287))
        
    else:
        #bbox = (int(296), int(471), int(965), int(530))
        #bbox = (int(296), int(517), int(965), int(570))
        bbox = (int(296), int(471), int(965), int(570))
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)
    #print_my(bbox)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_has_searched_circle_frient" + ".png"
#get_screen_of_first_username_of_cicle_search_page(path)

# 等待朋友圈搜索页出现搜索的好友
def wait_searched_friend_of_circle_search_page(input_event, username_require):
    i_count = 0
    TRY_COUNT_MAX_FOR_CIRCLE_SEARCH = 5
    username_require = username_require.replace("*", "")
    while i_count < TRY_COUNT_MAX_FOR_CIRCLE_SEARCH:
        i_count += 1
        iRet, username_found = has_searched_friend_of_circle_search_page(input_event)
        if iRet != RET_SUCESS:
            print("没有搜索到好友【{}】{}".format(username_require, username_found))
        else:
            # chenyj debug
            print(f"搜索到了好友【{username_found}】")
            i_found_count = 0
            for char in username_require:
                if char in username_found:
                    i_found_count += 1
            if i_found_count > 1:
                return APP_RET_CODE_SUCESS
        
        if True == input_event.wait(1):
            print_my("wait_searched_friend_of_circle_search_page, 被要求退出1")
            return -1 
        continue
            
    return APP_RET_CODE_UNKNOW
      
# 判断朋友圈搜索页中是否有搜索到好友 
def has_searched_friend_of_circle_search_page(input_event):
    username = ""
    
    TIME_BEGIN()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_has_searched_circle_frient" + ".png"
    get_screen_of_first_username_of_cicle_search_page(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("has_searched_friend_of_circle_search_page, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, username
        
    try:
        iRet, text_return = get_ocr_result_with_small_my(path)
        # 如果是因为设备没有准备好导致截图失败，那么先认为没有异常
        if iRet == APP_RET_CODE_NO_READY:
            return APP_RET_CODE_OCR_ERROR, username
        if iRet != APP_RET_CODE_SUCESS:
            return APP_RET_CODE_OCR_ERROR, username
    
        #json_return = test_baidu_ocr.get_ocr_result(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!has_searched_friend_of_circle_search_page tesseract_get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, username
    """
    if json_return is None: 
        print_my("!!!!!has_searched_friend_of_circle_search_page, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR, username

    if len(json_return["words_result"]) == 2:
        json_return["words_result"] = [json_return["words_result"][0]]
    if len(json_return["words_result"]) != 1:   
        return APP_RET_CODE_FRIEND_NO_FOUND, username
    
    for result in json_return["words_result"]:
        content = result["words"]
        username = content
        if "联系人" in content or "最常使用" in content:
            return APP_RET_CODE_FRIEND_NO_FOUND, username
        
        break
    """
    username = text_return.strip()
    if len(username) <= 1:
        return APP_RET_CODE_FRIEND_NO_FOUND, username
    
    TIME_END()
    
    return RET_SUCESS, username
# 测试
#iRet, username = has_searched_friend_of_circle_search_page(g_Event_test)
#print("朋友圈好友搜索页是否已经搜索到好友:{}, 好友:{}".format("是" if iRet == RET_SUCESS else "否", username))

# username_of_can_see_list 为[]表示所有朋友可见
def send_circle_with_check(input_event, str_wenAn, username_of_can_see_list = [], img_path_list = []):
    i_send_img_count = 0    
    
    # 判断发送模式，并把图片上传
    if len(img_path_list) > 0:
        img_path = img_path_list[0]
        img_path = img_path.strip().replace("‪", "")
        # 判断图片是否存在 
        if os.path.isfile(img_path) == True:  
            adb_send_image_to_phone(img_path)
            i_send_img_count = 1  
        else:
            print("!!!send_circle_with_check, 图片{}不存在啊".format(img_path))
    # chenyj debug
    if i_send_img_count == 0:
        print_my("此次发送朋友圈是文本模式")
    else:
        print_my("此次发送朋友圈是图片模式")
    
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        return iRet
    # 点击发现tab页
    image_check_begin()
    adb_click_discover_table_btn()
    iRet = wait_image_change(input_event, 0.992)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_circle_with_check, 被要求退出1")
        ensure_in_message_list_page(input_event)
        return iRet
    # 确保页面正确 
    """
    iRet, _ = is_in_page(input_event, [PageType.Discover])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!send_circle_with_check, 当前不是在发现页面")
        return iRet
        
    # 按发现页中的朋友圈按钮 
    image_check_begin()
    adb_click_friend_circle_of_discord()     
    iRet = wait_image_change(input_event, 0.988)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_circle_with_check, 被要求退出3")
        ensure_in_message_list_page(input_event)
        return iRet
    """
        
    # 长按右上角发送朋友圈按钮
    image_check_begin()
    if i_send_img_count == 0:
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
            iRet = windows_longpress_send_circle_btn()
        else:
            iRet = adb_longpress_send_circle_btn()
    else:
        adb_click_send_circle_btn()
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_circle_with_check, 被要求退出4")
        ensure_in_message_list_page(input_event)
        return iRet
        
    # 确保页面正确
    # 因为有可能马上就会进入朋友圈发表页(只有模拟器模式才会有)
    b_in_circle_send = False 
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        iRet, _ = is_in_page(input_event, [PageType.Circle_Send])
        if iRet == APP_RET_CODE_SUCESS:
            b_in_circle_send = True
    #
    """
    if i_send_img_count > 0 and b_in_circle_send == False: 
        #     因为第1次有权限申请问题
        i_try_count = 0
        WAIT_CIRCLE_SEND_MAX_COUNT = 10
        while i_try_count < WAIT_CIRCLE_SEND_MAX_COUNT:
            i_try_count += 1  
            iRet, _ = is_in_page(input_event, [PageType.Select_From_Album])
            if iRet != APP_RET_CODE_SUCESS:
                # chenyj debug
                print("!!!!send_circle_with_check, [{}]th当前不是[从相册选择页]，请稍等".format(i_try_count))
                print("等待中...")
                if True == input_event.wait(1):
                    print_my("send_circle_with_check, 被要求退出9")
                    ensure_in_message_list_page(input_event)
                    return APP_RET_CODE_ZHU_DONG_EXIT
                # 确保去除掉拍照记录生活页 
                iRet, _ = is_in_page(input_event, [PageType.Circle_Photo_Record])
                if iRet == APP_RET_CODE_SUCESS:
                    print("send_circle_with_check, 当前是在Circle_Photo_Record页面")
                    adb_click_i_know_of_circle_photo_record_page()
                continue
            break
        if i_try_count >= WAIT_CIRCLE_SEND_MAX_COUNT:            
            print("send_circle_with_check, 一直无法进入从相册选择页,发朋友圈失败")
            ensure_in_message_list_page(input_event)
            return APP_RET_CODE_UNKNOW   
    
        
    # 
    #if i_send_img_count > 0: 
        # 点击朋友圈页的从相册选择按钮
        image_check_begin()
        adb_click_select_from_album_btn_of_circle()
        iRet = wait_image_change(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出5")
            ensure_in_message_list_page(input_event)
            return iRet
            
        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Img_And_Video], 5)
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_circle_with_check, 当前不是在图片和视频页页面,但我忽略")
        
        # 选中相册的第一张图片按钮  
        image_check_begin()
        adb_click_album_first_img_btn()
        iRet = wait_image_change(input_event, 0.988)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出6")
            ensure_in_message_list_page(input_event)
            return iRet  
            
        # 点击完成按钮
        image_check_begin()
        adb_click_send_img_btn()
        iRet = wait_image_change(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出7")
            ensure_in_message_list_page(input_event)
            return iRet
    """
       
    # 确保现在是在“朋友圈发表页”
    i_try_count = 0
    WAIT_CIRCLE_SEND_MAX_COUNT = 5
    while i_try_count < WAIT_CIRCLE_SEND_MAX_COUNT:
        i_try_count += 1
        if i_try_count == WAIT_CIRCLE_SEND_MAX_COUNT - 1:
            iRet, page_type_return, _ = get_page_type_by_ocr(input_event)
        else:
            iRet, page_type_return, _ = get_page_type_by_tesseract(input_event)
        if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
            print_my("send_circle_with_check, 被要求退出8")
            ensure_in_message_list_page(input_event)
            return iRet
        if page_type_return != PageType.Circle_Send:
            # chenyj debug
            print("!!!!send_circle_with_check, [{}]th当前不是[发送朋友圈页]，请稍等[{}]".format(i_try_count, page_type_return))
            print("等待中...")
            if True == input_event.wait(1):
                print_my("send_circle_with_check, 被要求退出9")
                ensure_in_message_list_page(input_event)
                return APP_RET_CODE_ZHU_DONG_EXIT
            continue
        break
    if i_try_count >= WAIT_CIRCLE_SEND_MAX_COUNT:            
        print("send_circle_with_check, 一直无法进入发送朋友圈页面,发朋友圈失败")
        ensure_in_message_list_page(input_event)
        return APP_RET_CODE_UNKNOW
    
    # 点击发送朋友圈文本输入的编辑框 
    adb_click_edit_of_wenAn_of_send_circle()
    if True == input_event.wait(0.5):
        ensure_in_message_list_page(input_event, PageType.Circle_Send)
        return -1 
    
    # 粘贴文案
    adb_paste_text(str_wenAn, False)
    if True == input_event.wait(0.5):
        print_my("send_circle_with_check, 被要求退出20")
        ensure_in_message_list_page(input_event, PageType.Circle_Send)
        return -1 

    # 设置谁可以看
    if len(username_of_can_see_list) > 0:
        # 点击“谁可以看”按钮
        """
        image_check_begin()
        if i_send_img_count == 0: 
            adb_click_who_can_see_of_text_mode()
        else:
            adb_click_who_can_see_of_img_mode()
        iRet = wait_image_change(input_event, 0.994)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出10")
            ensure_in_message_list_page(input_event)
            return iRet
        """
        iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["谁可以看"])
        if iRet != APP_RET_CODE_SUCESS:
            print("send_circle_with_check 没法找到[谁可以看]按钮")
            ensure_in_message_list_page(input_event, PageType.Circle_Send)
            return iRet

        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Circle_Who_Can_See])
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_circle_with_check, 当前不是在Circle_Who_Can_See页面")
            return iRet

        # 点击“部分可见”按钮 
        image_check_begin()
        adb_click_part_can_see()
        iRet = wait_image_change(input_event, 0.998)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出11")
            ensure_in_message_list_page(input_event)
            return iRet
        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Circle_Select_Frient], 4)
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_circle_with_check, 当前不是在Circle_Who_Can_See页面")
            return iRet
        # 点击“选择朋友”按钮 
        image_check_begin()
        adb_click_select_friend()
        iRet = wait_image_change(input_event, 0.992)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出12")
            ensure_in_message_list_page(input_event, PageType.Circle_Select_Frient)
            return iRet  
        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Circle_Select_Frient])
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_circle_with_check, 当前不是在Circle_Select_Frient页面")
            return iRet
 
        for i, username in enumerate(username_of_can_see_list):
            print("send_circle_with_check, 第[{}]个/{}可见好友:{}".format(i+1, len(username_of_can_see_list), username))
            
            # 点击搜索可见好友栏的编辑框 
            adb_click_edit_of_search_can_see()
            if True == input_event.wait(0.2):
                print_my("send_circle_with_check, 被要求退出13")
                ensure_in_message_list_page(input_event, PageType.Circle_Select_Frient)
                return -1 
            windows_click_ctrl_z("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")    
            # 粘贴用户名
            # chenyj test
            username_of_before_emoji = clean_string(username)
            #"""
            # 使之能模糊匹配
            if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
                username_of_before_emoji = insert_star_except_between_digits(username_of_before_emoji)
            #username_of_before_emoji = "*".join(username_of_before_emoji)
            # 在朋友圈中搜索好好时，如果前面加*，会搜索不到
            #username_of_before_emoji = "*" + username_of_before_emoji
            if username_of_before_emoji.startswith("*"):
                username_of_before_emoji = username_of_before_emoji[1:]
                
            if username_of_before_emoji == "*":
                # chenyj test 临时处理
                if "?" == username:
                    username = "？"
                username_of_before_emoji = username
            #"""
            adb_paste_text(username_of_before_emoji, False)
            #adb_paste_text(username, False)
            if True == input_event.wait(1):
                print_my("send_circle_with_check, 被要求退出14")
                ensure_in_message_list_page(input_event, PageType.Circle_Select_Frient)
                return -1 
            # 这里对搜索后的item项的文本进行检查 
            iRet = wait_searched_friend_of_circle_search_page(input_event, username_of_before_emoji)
            if iRet != RET_SUCESS:
                print("没有搜索到好友【{}】".format(username))
                if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
                    adb_click_ctrl_z(username_of_before_emoji)
                else:
                    windows_click_ctrl_z(username_of_before_emoji)
                continue 
            
            # 选择搜索到的用户 
            adb_click_select_friend_of_searched()
            if True == input_event.wait(0.5):
                print_my("send_circle_with_check, 被要求退出15")
                ensure_in_message_list_page(input_event, PageType.Circle_Select_Frient)
                return -1 
        # 点击选择朋友页面的选择按钮
        image_check_begin()
        adb_click_select_of_select_friend_page()
        iRet = wait_image_change(input_event, 0.994)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出16")
            ensure_in_message_list_page(input_event, PageType.Circle_Select_Frient)
            return iRet 
        """
        # 点击“保存为标签”页面的忽略按钮 
        image_check_begin()
        adb_click_ingor_of_save_label_page()
        iRet = wait_image_change(input_event, 0.988)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出17")
            ensure_in_message_list_page(input_event, PageType.Circle_Select_Frient)
            return iRet 
        """
        # 确保页面正确 
        iRet, _ = is_in_page(input_event, [PageType.Circle_Who_Can_See])
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!send_circle_with_check, 当前不是在Circle_Who_Can_See页面")
            return iRet
            
        # 点击“谁可以看”页面的完成按钮 
        image_check_begin()
        adb_click_finish_of_who_can_see_page()
        iRet = wait_image_change(input_event, 0.992)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("send_circle_with_check, 被要求退出18")
            ensure_in_message_list_page(input_event)
            return iRet 

    """  
    # 确保页面正确 
    iRet, page_type_return = is_in_page(input_event, [PageType.Circle_Send])
    if iRet != APP_RET_CODE_SUCESS:
        print(f"!!!send_circle_with_check, 当前不是在Circle_Send页面,而是在[{page_type_return}]")
        return iRet
       
    # 点击发送朋友圈文本输入的编辑框 
    adb_click_edit_of_wenAn_of_send_circle()
    if True == input_event.wait(0.5):
        ensure_in_message_list_page(input_event, PageType.Circle_Send)
        return -1 
    
    # 粘贴文案
    adb_paste_text(str_wenAn, False)
    if True == input_event.wait(0.5):
        print_my("send_circle_with_check, 被要求退出20")
        ensure_in_message_list_page(input_event, PageType.Circle_Send)
        return -1 
    """
    
    # 点击“发表”按钮
    """
    image_check_begin()
    adb_click_send_btn_of_send_circle(False) 
    iRet = wait_image_change(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("send_circle_with_check, 被要求退出21")
        else:
            print_my("!!!!, 发送朋友圈失败({})".format(iRet))
        ensure_in_message_list_page(input_event, PageType.Circle_Send)
        return iRet 
    """
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["发表"])
    if iRet != APP_RET_CODE_SUCESS:
        print("send_circle_with_check 没法找到[发表]按钮")
        ensure_in_message_list_page(input_event, PageType.Circle_Send)
        return iRet
    adb_click_close_circle_btn()
    adb_click_message_list_table_btn()
    
    return APP_RET_CODE_SUCESS  

# 判断通讯录是否属于业务内容 
def is_friend_business(content):
    # 第一种情况
    for str_business in BUSINESS_FRIENDBOOK_LIST:
        if str_business in content:
            return True 
    # 第二种情况 
    if content.endswith("个朋友") == True:
        return True 
        
    return False 

# 把字符串中从后面数过来的第一个这样的子串  "(5)" 去掉
def remove_last_parenthesized_number(s):
    # 找到所有匹配的左括号+数字+右括号的子串
    matches = list(re.finditer(r'\(\d+\)', s))
    
    # 如果没有找到匹配的子串，直接返回原字符串
    if not matches:
        return s
    
    # 获取最后一个匹配的子串的起始和结束位置
    last_match = matches[-1]
    start, end = last_match.span()
    
    # 构建新字符串，去掉最后一个匹配的子串
    return s[:start] + s[end:]
# 测试用例
#test_str = "abc(1)(2)(3)def(4)ghi(5)jkl"
#result = remove_last_parenthesized_number(test_str)
#print(result)  # 应该输出: abc(1)(2)(3)def(4)ghi jkl

# 结构化标签页的标签基本信息
def struct_single_tag_info(i_tag_loop_count):
    iRet = APP_RET_CODE_UNKNOW
    tag_info = {}
    
    TIME_BEGIN()

    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_taginfo" + ".png"
    iRet, i_left, i_top = get_screen_of_taginfo(i_tag_loop_count, path)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, tag_info
    
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        #_, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!struct_single_tag_info,get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        TIME_END()
        return iRet, tag_info
    if json_return is None: 
        print_my("!!!!!struct_single_tag_info, get_ocr_result_with_small 失败")
        TIME_END()
        return iRet, tag_info
    # chenyj debug
    #print(json_return["words_result"])
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        # chenyj debug 
        print("处理前:{}".format(content))
        content = content.replace("（", "(").replace("）", ")")
        content = remove_last_parenthesized_number(content)
        print("处理后:{}".format(content))
        if len(content) <= 0:
            continue
        
        tag_info["tag_name"] = content
        tag_info["click_location"] = [i_left + int(x + width/2), i_top + int(y + height/2)] 
        break

    iRet = APP_RET_CODE_SUCESS
    
    return iRet, tag_info

# 结构化一屏通讯录信息内容
def struct_single_friend_book():
    global g_i_friendbook_count
    iRet = APP_RET_CODE_UNKNOW
    friend_list = []

    TIME_BEGIN()
    g_i_friendbook_count += 1
    
    #path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friendbook_{}".format(g_i_friendbook_count) + ".png"
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friendbook" + ".png"
    iRet = get_screen_of_friendbook(path)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, friend_list
    
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        #_, json_return = test_baidu_ocr.get_ocr_result_with_small(path)
    except Exception as e:
        print_my("!!!!!struct_single_friend_book,get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        TIME_END()
        return iRet, friend_list
    if json_return is None: 
        print_my("!!!!!struct_single_friend_book, get_ocr_result_with_small 失败")
        TIME_END()
        return iRet, friend_list
    # chenyj debug
    #print(json_return["words_result"])
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        # chenyj debug 
        print(content)
        if is_friend_business(content) == True: 
            continue
            
        friend_list.append(content)
        
    iRet = APP_RET_CODE_SUCESS
    
    return iRet, friend_list  

# 同步好友
def sync_frient_with_check(input_event):
    i_gun_up_count = 0
    friend_list = []
    
    print("===>sync_frient_with_check")
    TIME_BEGIN()
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        yield iRet, friend_list
        
    # 点击通讯录tab页
    image_check_begin()
    adb_click_friendbook_table_btn()
    iRet = wait_image_change(input_event, 0.988)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("sync_frient_with_check, 被要求退出1")
        ensure_in_message_list_page(input_event)
        yield iRet, friend_list
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!sync_frient_with_check, 当前不是在通讯录面")
        ensure_in_message_list_page(input_event)
        yield iRet, friend_list
    #
    # 确保是在第一页
    pass 

    #
    print_my("读取通讯录")
    while i_gun_up_count < MAX_SLIDE_UP_COUNT_FRIENDBOOK:
        i_gun_up_count += 1
        iRet, friend_list = struct_single_friend_book()
        if iRet != APP_RET_CODE_SUCESS:
            print("通讯录读取还没完成就提前结束了，已读取【{}】页".format(i_gun_up_count))
            ensure_in_message_list_page(input_event)
            yield iRet, friend_list
        #friend_list_all.extend(friend_list)
        yield APP_RET_CODE_SUCESS, friend_list
        
        if i_gun_up_count == MAX_SLIDE_UP_COUNT_FRIENDBOOK:
            # chenyj debug
            print("达到滑动最大次数，不再向上刷了")
            break
        # 向上滚动一屏
        iRet = adb_slide_friendbook_down_with_check(input_event)
        if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
            print_my("sync_frient_with_check, 被要求退出")
            ensure_in_message_list_page(input_event)
            TIME_END()
            yield APP_RET_CODE_ZHU_DONG_EXIT, friend_list
        elif iRet == APP_RET_CODE_APP_KA_ZHU:
            # chenyj debug
            print("sync_frient_with_check, 滚动了消息的顶部")
            break    
        # chenyj debug 
        print("第{}屏".format(i_gun_up_count))
        
        if True == input_event.wait(0.1):
            print_my("sync_frient_with_check, 被要求退出")
            ensure_in_message_list_page(input_event)
            TIME_END()
            yield APP_RET_CODE_ZHU_DONG_EXIT, friend_list 
        """
        if is_weChat_running() == False:
            print_my("!!!!微信应用退出了")
            TIME_END()
            yield APP_RET_CODE_APP_EXIT, message_all_list_now, message_all_list_new
        """
        continue
    print_my("通讯录读取成功")
    print("<===sync_frient_with_check 共【{}】页".format(i_gun_up_count))
    
    adb_click_message_list_table_btn()
    TIME_END()    
    yield APP_RET_CODE_HAS_FINISH, friend_list
 
# 同步微信标签组
def sync_tag_group_with_check(input_event):
    i_tag_loop_count = 0
    add_usergroup_data_dict = {}
    
    print("===>sync_tag_group_with_check")
    TIME_BEGIN()
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        yield iRet, add_usergroup_data_dict
        
    # 点击通讯录tab页
    image_check_begin()
    adb_click_friendbook_table_btn()
    iRet = wait_image_change(input_event, 0.988)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("sync_tag_group_with_check, 被要求退出1")
        ensure_in_message_list_page(input_event)
        yield iRet, add_usergroup_data_dict
    # 确保是在通讯录页面
    iRet, _ = is_in_page(input_event, [PageType.FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!sync_tag_group_with_check, 当前不是在通讯录面")
        ensure_in_message_list_page(input_event)
        yield iRet, add_usergroup_data_dict

    #
    # 确保是在第一页
    i_gun_down_count = 0
    while i_gun_down_count < MAX_SLIDE_DOWN_COUNT_FRIENDBOOK:
        i_gun_down_count += 1 
        if i_gun_down_count == MAX_SLIDE_DOWN_COUNT_FRIENDBOOK:
            # chenyj debug
            print("    达到滑动最大次数，不再向下刷了")
            break
        # 向上滚动一屏
        iRet = adb_slide_friendbook_up_with_check(input_event)
        if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
            print_my("    sync_tag_group_with_check, 被要求退出3")
            adb_click_back_with_check(input_event, 1) 
            TIME_END()
            yield APP_RET_CODE_SUCESS, add_usergroup_data_dict
            break
        elif iRet == APP_RET_CODE_APP_KA_ZHU:
            # chenyj debug
            print("    sync_tag_group_with_check, 滚动到了顶部")
            break    
        # chenyj debug 
        print("    第{}屏".format(i_gun_down_count))
        
        if True == input_event.wait(0.1):
            print_my("sync_tag_group_with_check, 被要求退出4")
            ensure_in_message_list_page(input_event)
            TIME_END()
            yield APP_RET_CODE_ZHU_DONG_EXIT, add_usergroup_data_dict 
        continue

    # 点击“通讯录管理”按钮
    image_check_begin()
    adb_click_friendbook_manage_btn()
    iRet = wait_image_change(input_event, 0.988)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("sync_tag_group_with_check, 被要求退出5")
        ensure_in_message_list_page(input_event)
        yield iRet, add_usergroup_data_dict

    # chenyj debug
    print(f"================点击了通讯录管理按钮，等待1秒")
    # 这里会弹出设置的新窗口，所以要等待下
    time.sleep(1)
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.FriendBook_Manage], 3)
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!sync_tag_group_with_check, 当前不是在通讯录管理页面")
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    # chenyj debug
    print(f"================确定当前是在通讯录管理页面")

    # 点击标签item 
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["标签"])
    if iRet != APP_RET_CODE_SUCESS:
        print("sync_tag_group_with_check， 没法找到标签按钮")
        ensure_in_message_list_page(input_event)
        yield iRet, add_usergroup_data_dict
    
    # 确保是在标签页面
    """
    iRet, page_type_return = is_in_page(input_event, [PageType.Tag])
    if iRet != APP_RET_CODE_SUCESS:
        if page_type_return == PageType.Tag_Empty:
            print_my("标签页为空，没有标签")
            yield APP_RET_CODE_HAS_FINISH, add_usergroup_data_dict
        print("!!!sync_tag_group_with_check, 当前不是在标签页面")
        ensure_in_message_list_page(input_event)
        yield iRet, add_usergroup_data_dict
    """
    # 开始循环
    while i_tag_loop_count < MAX_LOOP_COUNT_OF_TAG:
        add_usergroup_data_dict = {}
        
        # tag_info = {"tag_name":"随意加的"}
        iRet, tag_info = struct_single_tag_info(i_tag_loop_count)
        i_tag_loop_count += 1
        if iRet != APP_RET_CODE_SUCESS:
            print("标签读取还没完成就提前结束了，已读取【{}】个TAG".format(i_tag_loop_count))
            ensure_in_message_list_page(input_event)
            yield iRet, add_usergroup_data_dict
        if "tag_name" not in tag_info or len(tag_info["tag_name"]) <= 0:
            yield APP_RET_CODE_HAS_FINISH, add_usergroup_data_dict
            
        #print_my("===>开始读取第{}个TAG:{}".format(i_tag_loop_count, tag_info["tag_name"]))
        # 获取当前日期和时间
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H:%M:%S")
        add_usergroup_data_dict["usergroup_name"] = tag_info["tag_name"] + "_微信标签组_" + formatted_datetime
        add_usergroup_data_dict["add_model_name"] = ""
        add_usergroup_data_dict["usergroup_member"] = []
        # 点击进入此标签
        image_check_begin()
        adb_click(tag_info["click_location"][0], tag_info["click_location"][1])
        iRet = wait_image_change(input_event, 0.994)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("sync_tag_group_with_check, 被要求退出5")
            ensure_in_message_list_page(input_event)
            yield iRet, add_usergroup_data_dict
        # 确保是在此标签通讯录页面
        """
        iRet, _ = is_in_page(input_event, [PageType.FriendBookTag])
        if iRet != APP_RET_CODE_SUCESS:
            print("!!!sync_tag_group_with_check, 当前不是在【{}】标签通讯录面".format(tag_info["tag_name"]))
            ensure_in_message_list_page(input_event)
            yield iRet, add_usergroup_data_dict
        """
        
        # 读取通讯录
        i_gun_up_count = 0
        print_my("  开始读取第{}个标签组【{}】".format(i_tag_loop_count, tag_info["tag_name"]))
        while i_gun_up_count < MAX_SLIDE_UP_COUNT_FRIENDBOOK:
            i_gun_up_count += 1
            iRet, friend_list = struct_single_friend_book()
            if iRet != APP_RET_CODE_SUCESS:
                print("    此标签下的好友读取还没完成就提前结束了，已读取【{}】页".format(i_gun_up_count))
                #ensure_in_message_list_page(input_event)
                #yield iRet, friend_list
                adb_click_back_with_check(input_event, 1) 
                yield APP_RET_CODE_SUCESS, add_usergroup_data_dict
                break
            add_usergroup_data_dict["usergroup_member"].extend(friend_list)
            #yield APP_RET_CODE_SUCESS, friend_list
            
            if i_gun_up_count == MAX_SLIDE_UP_COUNT_FRIENDBOOK:
                # chenyj debug
                print("    达到滑动最大次数，不再向上刷了")
                adb_click_back_with_check(input_event, 1) 
                yield APP_RET_CODE_SUCESS, add_usergroup_data_dict
                break
            # 向上滚动一屏
            iRet = adb_slide_friendbook_down_with_check(input_event)
            if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                print_my("    sync_tag_group_with_check, 被要求退出6")
                adb_click_back_with_check(input_event, 1) 
                TIME_END()
                yield APP_RET_CODE_SUCESS, add_usergroup_data_dict
                break
            elif iRet == APP_RET_CODE_APP_KA_ZHU:
                # chenyj debug
                print("    sync_tag_group_with_check, 滚动到了底部")
                adb_click_back_with_check(input_event, 1, 0.993) 
                yield APP_RET_CODE_SUCESS, add_usergroup_data_dict 
                break    
            # chenyj debug 
            print("    第{}屏".format(i_gun_up_count))
            
            if True == input_event.wait(0.1):
                print_my("sync_tag_group_with_check, 被要求退出7")
                ensure_in_message_list_page(input_event)
                TIME_END()
                yield APP_RET_CODE_ZHU_DONG_EXIT, add_usergroup_data_dict 
            """
            if is_weChat_running() == False:
                print_my("!!!!微信应用退出了")
                TIME_END()
                yield APP_RET_CODE_APP_EXIT, message_all_list_now, message_all_list_new
            """
            continue
        print_my("  完成【{}】标签组的读取，共读取此标签组的好友{}个".format(tag_info["tag_name"], len(add_usergroup_data_dict["usergroup_member"])))
        
        continue
    #     
    ensure_in_message_list_page(input_event)
    TIME_END()    
    add_usergroup_data_dict = {}
    yield APP_RET_CODE_HAS_FINISH, add_usergroup_data_dict
 
 
# 确保消息列表中第二行开始后面是没置顶的 
def ensure_msg_no_top(input_event):
    MAX_COUNT_OF_CHECK_TOP = 4
    i_count_check_top = 0
    
    while i_count_check_top < MAX_COUNT_OF_CHECK_TOP:
        i_count_check_top += 1
            
        temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v9.png"     
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            x = 949
            y = 247
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            x = 1039
            y = 541
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            x = 560
            y = 282

        bbox = (x, y, x + 10, y + 10) 
        iRet = adb_get_screen(temp_png, bbox)
        if iRet != APP_RET_CODE_SUCESS:
            return iRet 
            
        try:
            img = Image.open(temp_png) 
            cropped_img = img.crop(bbox)
            crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_is_top_1.png"
            cropped_img.save(crop_path)
            crop_mage = imread(crop_path)
            if True == image_is_white(crop_mage):
                print("!!!第二行已经是非置顶了")
                return APP_RET_CODE_SUCESS
                
            # 长按
            image_check_begin()
            # [lt_x_of_new_msg, lt_y_of_new_msg, rb_x_of_new_msg, rb_y_of_new_msg]
            adb_longpress(x, y)
            iRet = wait_image_change(input_event, 0.9986)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("set_username_top_with_check, 被要求退出3")
                else:
                    print_my("set_username_top_with_check!!!!, 长按第二行失败({})".format(iRet))
                return iRet
            #
            # 选择“取消置顶该聊天”
            image_check_begin()
            adb_click(812, 410)
            iRet = wait_image_change(input_event, 0.997)
            if iRet == -1:
                if iRet == -1:
                    print_my("set_username_top_with_check, 被要求退出4")
                else:
                    print_my("set_username_top_with_check!!!!, 按第二行用户置顶该聊天失败({})".format(iRet))
                return iRet
            print("第二行取消置顶成功")
            if True == input_event.wait(0.1):
                print_my("set_username_top_with_check, 被要求退出5")
                TIME_END()
                return APP_RET_CODE_ZHU_DONG_EXIT
            continue
        except Exception as e:
            print("!!!!ensure_msg_no_top异常\n{}".format(e))
            return APP_RET_CODE_UNKNOW
    if i_count_check_top >= MAX_COUNT_OF_CHECK_TOP:
        return APP_RET_CODE_UNKNOW
        
    return APP_RET_CODE_SUCESS

# 截取新朋友页面的状态列的截图
def get_screen_of_state_info_of_new_friend_page(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v14.png"     
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (int(899/W_SCREEN*g_w_screen), int(183/H_SCREEN*g_h_screen), int(1073/W_SCREEN*g_w_screen), int(1915/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(899/W_SCREEN*g_w_screen), int(183/H_SCREEN*g_h_screen), int(1073/W_SCREEN*g_w_screen), int(1915/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(899/W_SCREEN*g_w_screen), int(183/H_SCREEN*g_h_screen), int(1073/W_SCREEN*g_w_screen), int(1915/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (int(326+G_X_PIAN_YI), int(227+G_Y_PIAN_YI), int(404+G_X_PIAN_YI), int(984+G_Y_PIAN_YI))
    #print_my(bbox)    
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_check_has_need_jie_shou_by_tesseract" + ".png"
#get_screen_of_state_info_of_new_friend_page(path)

# 使用tesseract判断判断是否有需要接受的加好友请求
def check_has_need_jie_shou_request_by_tesseract(input_event):
    b_has_need_jie_shou = False
    
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_for_check_has_need_jie_shou_by_tesseract" + ".png"
    if True == os.path.exists(path):
        os.remove(path)
    get_screen_of_state_info_of_new_friend_page(path)
    
    # chenyj test
    #path = SCREENSHOT_SAVE_DIR + "/" + "test" + ".png"
    if True == input_event.wait(0.1):
        print_my("check_has_need_jie_shou_request_by_tesseract, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, b_has_need_jie_shou
    iRet, text_return = get_ocr_result_with_small_my(path)
    # 如果是因为设备没有准备好导致截图失败，那么先认为没有异常
    if iRet == APP_RET_CODE_NO_READY:
        return APP_RET_CODE_SUCESS, b_has_need_jie_shou
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, b_has_need_jie_shou
    
    # 检查是否有 
    if "接受" in text_return:
        b_has_need_jie_shou = True
 
    return APP_RET_CODE_SUCESS, b_has_need_jie_shou


# 点击添加到通讯录页(对方主动请求)页面的完成按钮  
def adb_click_finish_btn_of_add_to_friendbook_page(b_debug = True):
    # chenyj debug
    print("动作:【点击完成按钮】")
    if b_debug == True:
        print("动作:【点击完成按钮】")
    adb_click(int(541/W_SCREEN*g_w_screen), int(1813/H_SCREEN*g_h_screen))     
    return 

# 带检查地点击添加到通讯录页(对方主动请求)页面的完成按钮 
def adb_click_finish_btn_of_add_to_friendbook_page_with_check(b_debug = True):
    image_check_begin()
    adb_click_finish_btn_of_add_to_friendbook_page(b_debug)
    #time.sleep(0.5)
    # 在电脑慢的时间这里要设置大一些
    time.sleep(2)
    iRet, bChange = image_check_end(0.99)
    if iRet == 0 and bChange == False:
        return APP_RET_CODE_APP_KA_ZHU
    return APP_RET_CODE_SUCESS

# 截取好友资料页的昵称的截图
def get_screen_of_nickname_of_friend_information_page(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v15.png"  
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        bbox = (int(156/W_SCREEN*g_w_screen), int(143/H_SCREEN*g_h_screen), int(549/W_SCREEN*g_w_screen), int(183/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(377), int(351), int(818), int(405))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        bbox = (int(377), int(351), int(818), int(405))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        bbox = (int(585+G_X_PIAN_YI), int(97+G_Y_PIAN_YI), int(864+G_X_PIAN_YI), int(132+G_Y_PIAN_YI))
    #print_my(bbox)   
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_nickname_of_friend_information_page" + ".png"
#get_screen_of_nickname_of_friend_information_page(path)
    
# 获取”好友资料“页的用户昵称
def get_friend_nickname_of_friend_information_page(input_event):
    nickname_return = ""
    
    TIME_BEGIN()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_nickname_of_friend_information_page" + ".png"
    get_screen_of_nickname_of_friend_information_page(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("get_friend_nickname_of_friend_information_page, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, nickname_return
        
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!get_friend_nickname_of_friend_information_page get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, nickname_return
    if json_return is None: 
        print_my("!!!!!get_friend_nickname_of_friend_information_page, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR, nickname_return

    if len(json_return["words_result"]) == 2:
        json_return["words_result"] = [json_return["words_result"][0]]
    if len(json_return["words_result"]) != 1:   
        return APP_RET_CODE_UNKNOW, nickname_return
    
    for result in json_return["words_result"]:
        content = result["words"]
        _, nickname_return = username_standard(content)
        # chenyj debug
        print("昵称:【{}】".format(nickname_return))
        break
    TIME_END()
    
    return RET_SUCESS, nickname_return
# 测试
#iRet, nickname_return = get_friend_nickname_of_friend_information_page(g_Event_test)
#print("用户的昵称是:{}".format(nickname_return))

# 获得新的朋友页的好友列表
g_img_befor_path_of_new_friend = SCREENSHOT_SAVE_DIR + "/" + "screen_of_of_new_friend_list_befor" + ".png"
g_img_after_path_of_new_friend = SCREENSHOT_SAVE_DIR + "/" + "screen_of_new_friend_list" + ".png"
def get_username_list_of_new_friend(input_event):
    global g_img_befor_path_of_new_friend, g_img_after_path_of_new_friend
    # chenyj debug
    print("===>get_username_list_of_new_friend") 
    username_list = []
    
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        return iRet, username_list
    
    # 点击通讯录tab页
    image_check_begin()
    adb_click_friendbook_table_btn()
    iRet = wait_image_change(input_event, 0.988)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("get_username_list_of_new_friend, 被要求退出1")
        ensure_in_message_list_page(input_event)
        return iRet, username_list
    # 确保页面正确 
    iRet, page_type_return, text_return = get_page_type_by_ocr(input_event)
    #iRet, _ = is_in_page(input_event, [PageType.FriendBook, PageType.New_Friend_Of_FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!get_username_list_of_new_friend, 当前不是在通讯录面")
        ensure_in_message_list_page(input_event)
        return iRet, username_list
    if page_type_return == PageType.FriendBook:
        # 点击新的朋友item 
        image_check_begin()
        adb_click_new_friend_item_btn_for_auto_pass()
        iRet = wait_image_change(input_event, 0.996)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("get_username_list_of_new_friend, 被要求退出2")
            ensure_in_message_list_page(input_event)
            return iRet, username_list   
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.New_Friend_Of_FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!get_username_list_of_new_friend, 当前不是在新的朋友页")
        ensure_in_message_list_page(input_event)
        return iRet, username_list
    
    # 截图
    # 判断图片是否变化
    bChange = False
    if True == os.path.exists(g_img_after_path_of_new_friend):
        shutil.copy(g_img_after_path_of_new_friend, g_img_befor_path_of_new_friend)
        iRet = get_screen_of_new_friend_list(g_img_after_path_of_new_friend)
        if iRet == APP_RET_CODE_SUCESS:
             _, bChange = has_img_change(g_img_befor_path_of_new_friend, g_img_after_path_of_new_friend, NEW_FRIEND_CHANGE_RATIO)
        else:
            bChange = False
    else:
        _ = get_screen_of_new_friend_list(g_img_after_path_of_new_friend)
        bChange = True
    if bChange == False:
        print("新的朋友的图片与上一次没有变化，肯定没有新的好友")
        ensure_in_message_list_page(input_event, PageType.New_Friend_Of_FriendBook)
        return APP_RET_CODE_SUCESS, username_list
    # OCR
    try:
        _, json_return = test_baidu_ocr.get_ocr_result_with_small(g_img_after_path_of_new_friend)
    except Exception as e:
        print_my("!!!!!get_username_list_of_new_friend get_ocr_result_with_small, 出现异常\n Exception: {}".format(e))
        ensure_in_message_list_page(input_event, PageType.New_Friend_Of_FriendBook)
        return APP_RET_CODE_OCR_ERROR, username_list
    if json_return is None: 
        print_my("!!!!!get_username_list_of_new_friend, get_ocr_result_with_small失败")
        ensure_in_message_list_page(input_event, PageType.New_Friend_Of_FriendBook)
        return APP_RET_CODE_OCR_ERROR, username_list
    # chenyj debug
    #print(json_return)
    
    # 在好友列表中找到指定的好友
    for result in json_return["words_result"]:
        content = result["words"]
        x = result["location"]["left"]
        y = result["location"]["top"]
        width = result["location"]["width"]
        height = result["location"]["height"]
        
        try:
            img = Image.open(g_img_after_path_of_new_friend)
            bbox = (x, y, x + width, y + height)
            cropped_img = img.crop(bbox)
            #g_i_crop_count += 1
            #crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_{}.png".format(g_i_crop_count)
            crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp.png"
            cropped_img.save(crop_path)
            crop_mage = imread(crop_path)
            # chenyj debug
            #print("g_i_crop_count:{}, content:{}".format(g_i_crop_count, content))
        except Exception as e:
            print("!!!!get_username_list_of_new_friend, 出现异常:{}".format(e))
            continue 
        # chenyj debug
        #print(f"【{content}】")
        if True == image_is_black(crop_mage):
            # chenyj debug
            #print("此用户{}可能是新用户".format(content))

            # 找此用户的状态
            if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
                x_of_lt_expect = 860
            elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
                x_of_lt_expect = 881
            elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
                x_of_lt_expect = 881
            elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
                x_of_lt_expect = 124
            y_of_lt_expect = result["location"]["top"] - 5
            
            b_has_added = False
            if "已添加" in content:
                b_has_added = True
            for result_ in json_return["words_result"]:
                content_ = result_["words"]
                x_ = result_["location"]["left"]
                y_ = result_["location"]["top"]
                width_ = result_["location"]["width"]
                height_ = result_["location"]["height"]
                
                if result == result_:
                    continue
                
                # chenyj debug
                #print(f"判断【{content_}】是否满足宽高{abs(x_ - x_of_lt_expect)}, {abs(y_ - y_of_lt_expect)}")
                if abs(x_ - x_of_lt_expect) < 30 and abs(y_ - y_of_lt_expect) < 30:
                    # chenyj debug
                    #print(f"    满足")
                    if content_ == "已添加":
                        b_has_added = True
                        break
            if b_has_added == True:
                # 获取真实的昵称
                #     点击用户名
                image_check_begin()
                adb_click(g_rb_x_of_nickname_of_new_friend_information_page + int(x+width/2), g_rb_y_of_nickname_of_new_friend_information_page + int(y+height/2))
                """
                iRet = wait_image_change(input_event, 0.996)
                if iRet != APP_RET_CODE_SUCESS:
                    if iRet == -1:
                        print_my("get_username_list_of_new_friend, 被要求退出3")
                    ensure_in_message_list_page(input_event)
                    return iRet, username_list   
                """
                #     确保页面正确
                """
                iRet, _ = is_in_page(input_event, [PageType.Friend_Information])
                if iRet!= APP_RET_CODE_SUCESS:
                    print("!!!get_username_list_of_new_friend, 当前不是在好友资料页")
                    ensure_in_message_list_page(input_event)
                    return iRet, username_list
                """
                #    读取好友昵称
                iRet, nickname_return = get_friend_nickname_of_friend_information_page(input_event)
                if iRet != APP_RET_CODE_SUCESS:
                    print("!!!get_username_list_of_new_friend, 读取好友昵称失败")
                    ensure_in_message_list_page(input_event)
                    return iRet, username_list
                #    返回 
                #adb_click_back_with_check(input_event, 1)  
                
                username_list.append(nickname_return.strip())
                
    ensure_in_message_list_page(input_event, PageType.New_Friend_Of_FriendBook)
    
    # chenyj debug    
    print("<===get_username_list_of_new_friend, 昵称列表:{}".format(username_list))     
    username_list = list(set(username_list))
    
    return RET_SUCESS, username_list
# 测试
#iRet, new_username_list = get_username_list_of_new_friend(g_Event_test)
#print("新的用户是:{}".format(new_username_list))

# 自动通过好友
def auto_pass_friend_with_check(input_event, remark_prefix):
    i_sucess_pass_count = 0
    
    print("===>auto_pass_friend_with_check")
    TIME_BEGIN()
    
    remark_prefix = get_remark_prefix_str(remark_prefix)
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        return iRet, i_sucess_pass_count
    # 点击通讯录tab页
    image_check_begin()
    adb_click_friendbook_table_btn()
    iRet = wait_image_change(input_event, 0.988)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("auto_pass_friend_with_check, 被要求退出1")
        ensure_in_message_list_page(input_event)
        return iRet, i_sucess_pass_count
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!auto_pass_friend_with_check, 当前不是在通讯录面")
        ensure_in_message_list_page(input_event)
        return iRet, i_sucess_pass_count
            
    # 点击新的朋友item 
    image_check_begin()
    adb_click_new_friend_item_btn_for_auto_pass()
    iRet = wait_image_change(input_event, 0.996)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("auto_pass_friend_with_check, 被要求退出2")
        ensure_in_message_list_page(input_event)
        return iRet, i_sucess_pass_count   
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.New_Friend_Of_FriendBook])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!auto_pass_friend_with_check, 当前不是在新的朋友面")
        ensure_in_message_list_page(input_event)
        return iRet, i_sucess_pass_count
    # 
    # 判断是否有需要“接受”的好友请求，有就执行接受
    PROCESS_NEED_JIE_SHOU_MAX_COUNT = 5
    i_check_need_jie_shou_count = 0
    while i_check_need_jie_shou_count < PROCESS_NEED_JIE_SHOU_MAX_COUNT:
        i_check_need_jie_shou_count += 1
        iRet, b_has_need_jie_shou = check_has_need_jie_shou_request_by_tesseract(input_event)
        if iRet != APP_RET_CODE_SUCESS:
            ensure_in_message_list_page(input_event)
            return iRet, i_sucess_pass_count
        if b_has_need_jie_shou == True: 
            # 点击“接受”按钮 
            iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, ["接受"])
            if iRet != APP_RET_CODE_SUCESS:
                ensure_in_message_list_page(input_event, PageType.New_Friend_Of_FriendBook) 
                return iRet, i_sucess_pass_count

            # 确保页面正确 
            iRet, _ = is_in_page(input_event, [PageType.Add_to_FriendBook_OTHER_ZHU_DONG])
            if iRet != APP_RET_CODE_SUCESS:
                print("!!!auto_pass_friend_with_check, 当前不是在添加到通讯录页(对方主动请求)页面")
                ensure_in_message_list_page(input_event)
                return iRet, i_sucess_pass_count
            #
            #
            # 点击通过朋友验证页面的备注编辑框 
            image_check_begin()
            adb_click_remark_edit_of_pass_new_frient()
            if True == input_event.wait(0.3):
                print_my("auto_pass_friend_with_check, 被要求退出3")
                TIME_END()
                adb_click_back_with_check(input_event, 4)
                return -1  
            iRet = wait_image_change(input_event, 0.9999)
            if iRet != APP_RET_CODE_SUCESS:
                if iRet == -1:
                    print_my("auto_pass_friend_with_check, 被要求退出4")
                else:
                    print_my("!!!!, 加好友{}失败({})".format(username, iRet))
                ensure_in_message_list_page(input_event)
                return iRet
            #
            # 粘贴备注
            adb_paste_text(remark_prefix, True)
            if True == input_event.wait(0.5):
                print_my("auto_pass_friend_with_check, 被要求退出5")
                adb_click_back_with_check(input_event, 2)
                return -1  
            #     
            time.sleep(0.7)
    
            # 点击“完成”按钮   
            iRet = adb_click_finish_btn_of_add_to_friendbook_page_with_check()
            if iRet != APP_RET_CODE_SUCESS:
                print_my("auto_pass_friend_with_check, 正在执行自动通过好好，可是点击完成时有异常")
                ensure_in_message_list_page(input_event)
                return iRet, i_sucess_pass_count             
            
            # 执行返回按钮  
            adb_click_back_with_check(input_event, 1, 0.995)
            
            print("成功接受1个加好友的请求")   
            i_sucess_pass_count += 1            
            # 等待一会儿
            if True == input_event.wait(0.2):
                ensure_in_message_list_page(input_event, PageType.New_Friend_Of_FriendBook)
                print_my("auto_pass_friend_with_check, 正在执行自动通过好好，可是被要求退出3")
                return APP_RET_CODE_ZHU_DONG_EXIT, i_sucess_pass_count
            
            continue 
        break 
    #### 
    ensure_in_message_list_page(input_event)    
   
    print("<===auto_pass_friend_with_check 共通过{}个好友请求".format(i_sucess_pass_count))
    print_my("共通过{}个好友请求".format(i_sucess_pass_count))
    TIME_END()    
    return APP_RET_CODE_SUCESS, i_sucess_pass_count
#auto_pass_friend_with_check(g_Event_test, "当前日期")

# 判断"接收新消息通知开关"是否打开
def is_jie_shou_new_message_notice_open():
    b_is_open = False
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v10.png"   
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        x = 987
        y = 211
        bbox = (x, y, x + 10, y + 10)   
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        x = 913
        y = 268
        bbox = (x, y, x + 12, y + 12)   
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
        x = 611
        y = 168
        bbox = (x, y, x + 12, y + 12)   
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet 
        
    try:
        img = Image.open(temp_png) 
        cropped_img = img.crop(bbox)
        crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_is_new_msg_open.png"
        cropped_img.save(crop_path)
        crop_mage = imread(crop_path)
        if True == image_is_white(crop_mage):
            print("!!!接收新消息通知开关是关闭的")
            b_is_open = False
            return APP_RET_CODE_SUCESS, b_is_open 
        else:
            print("!!!接收新消息通知开关是打开的")
            b_is_open = True
            return APP_RET_CODE_SUCESS, b_is_open
    except Exception as e:
        print("!!!is_jie_shou_new_message_notice_open, 出现异常: {}".format(e))
        return APP_RET_CODE_UNKNOW, b_is_open
    return  APP_RET_CODE_UNKNOW, b_is_open

#iRet, b_is_open = is_jie_shou_new_message_notice_open()        
#print("接收新消息通知开关是否打开:{}".format(b_is_open))

# 判断"接收语音和视频通话开关"是否打开
def is_jie_shou_sound_and_video_open():
    b_is_open = False
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v11.png"   
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:  
        x = 987
        y = 296
        bbox = (x, y, x + 10, y + 10)
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        x = 920
        y = 416
        bbox = (x, y, x + 12, y + 12)  
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
        x = 611
        y = 268
        bbox = (x, y, x + 12, y + 12)  
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet 
        
    try:
        img = Image.open(temp_png) 
        cropped_img = img.crop(bbox)
        crop_path = SCREENSHOT_SAVE_DIR + "/" + "crop_temp_is_sound_and_video_open.png"
        cropped_img.save(crop_path)
        crop_mage = imread(crop_path)
        if True == image_is_white(crop_mage):
            print("!!!接收语音和视频通话开关是关闭的")
            b_is_open = False
            return APP_RET_CODE_SUCESS, b_is_open 
        else:
            print("!!!接收语音和视频通话开关是打开的")
            b_is_open = True
            return APP_RET_CODE_SUCESS, b_is_open
    except Exception as e:
        print("!!!is_jie_shou_sound_and_video_open, 出现异常: {}".format(e))
        return APP_RET_CODE_UNKNOW, b_is_open
    return  APP_RET_CODE_UNKNOW, b_is_open

#iRet, b_is_open = is_jie_shou_sound_and_video_open()        
#print("接收语音和视频通话开关是否打开:{}".format(b_is_open))

# 点击新消息通知页面的接收新消息通知开关按钮
def adb_click_new_msg_btn_for_of_new_msg_notice_page():
    # chenyj debug
    print("动作:【点击新消息通知页面的接收新消息通知开关按钮】")
    adb_click(int(1002/W_SCREEN*g_w_screen), int(220/H_SCREEN*g_h_screen))
    return APP_RET_CODE_SUCESS
#adb_click_new_msg_btn_for_of_new_msg_notice_page()

# 点击关闭系统消息通知按钮
def adb_click_close_system_msg_notice_btn():
    # chenyj debug
    print("动作:【点击关闭系统消息通知按钮】")
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        adb_click(int(550/W_SCREEN*g_w_screen), int(1776/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        adb_click(int(550), int(2046))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
        adb_click(int(356), int(1036))
    return APP_RET_CODE_SUCESS
#adb_click_close_system_msg_notice_btn()

# 截取我的页的当前登录微信昵称的截图
def get_screen_of_username_of_me_page(path):
    temp_png = SCREENSHOT_SAVE_DIR + "/tmp_v20.png"   
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:  
        bbox = (int(150/W_SCREEN*g_w_screen), int(150/H_SCREEN*g_h_screen), int(406/W_SCREEN*g_w_screen), int(203/H_SCREEN*g_h_screen))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
        bbox = (int(271), int(265), int(882), int(336))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:# OK
        bbox = (int(177), int(179), int(545), int(237))
    elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:# OK
        bbox = (int(377), int(84), int(559), int(113)) 
    #print_my(bbox) 
    iRet = adb_get_screen(temp_png, bbox)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet
    img = Image.open(temp_png)
    cropped_img = img.crop(bbox)
    cropped_img.save(path)   
    return APP_RET_CODE_SUCESS
#path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_username_of_me_page" + ".png"
#get_screen_of_username_of_me_page(path)

# 获取我的页中登录微信的昵称 
def get_username_of_me_page(input_event):
    username_return = ""
    
    TIME_BEGIN()
    path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_username_of_me_page" + ".png"
    get_screen_of_username_of_me_page(path)
    
    # chenyj test
    if True == input_event.wait(0.1):
        print_my("get_username_of_me_page, 被要求退出1")
        return APP_RET_CODE_ZHU_DONG_EXIT, username_return
        
    try:
        json_return = test_baidu_ocr.get_ocr_result(path)
        # chenyj debug 
        #print("json_return:\n{}".format(json_return))
    except Exception as e:
        print_my("!!!!!get_username_of_me_page get_ocr_result, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_OCR_ERROR, username_return
    if json_return is None: 
        print_my("!!!!!get_username_of_me_page, get_ocr_result 失败")
        return APP_RET_CODE_OCR_ERROR, username_return

    if len(json_return["words_result"]) == 2:
        json_return["words_result"] = [json_return["words_result"][0]]
    if len(json_return["words_result"]) != 1:   
        return APP_RET_CODE_FRIEND_NO_FOUND, username_return
    
    for result in json_return["words_result"]:
        username_return = result["words"]
        break
    TIME_END()
    
    return RET_SUCESS, username_return
# 测试
#iRet, username = get_username_of_me_page(g_Event_test)
#print("我的页中登录微信的昵称:{}".format(username))

# 执行微信相关的设置
def do_weichat_setting_with_check(input_event):
    username_of_me = ""
    
    print("===>do_weichat_setting_with_check")
    TIME_BEGIN()
    
    # 确保是在消息列表页
    iRet = ensure_in_message_list_page(input_event)
    if iRet == APP_RET_CODE_UNKNOW:
        upload_snape()
        return iRet, username_of_me
    # 点击“我的”tab页
    image_check_begin()
    adb_click_me_table_btn()
    iRet = wait_image_change(input_event, 0.998)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("do_weichat_setting_with_check, 被要求退出1")
        upload_snape()
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    """
    # chenyj debug
    print(f"================判断是否是我的页面")
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Me])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 当前不是在我的页面")
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    # chenyj debug
    print(f"================确认现在是在我的页面")
    """
    # 点击设置item 
    image_check_begin()
    print("点击设置item")
    adb_click(int(131), int(906))
    iRet = wait_image_change(input_event, 0.998)
    if iRet != APP_RET_CODE_SUCESS:
        if iRet == -1:
            print_my("do_weichat_setting_with_check, 被要求退出2")
        upload_snape()
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me

    # chenyj debug
    print(f"================点击了设置按钮，等待1秒")
    # 这里会弹出设置的新窗口，所以要等待下
    time.sleep(1)
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Setting], 3)
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 当前不是在设置页面")
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    # chenyj debug
    print(f"================确定当前是在设置页面")
    # 获取当前登录的微信号
    iRet, username_of_me = get_username_of_me_page(input_event)

    if iRet != APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 获取当前登录的微信号失败")
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    print_my("识别到当前登录的微信账号是:{}".format(username_of_me))
    
    '''
    # 点击新消息通知item 
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        keyWord_list = ["新消息通知"]
    else:
        keyWord_list = ["通知"]
    iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, keyWord_list)
    if iRet != APP_RET_CODE_SUCESS:
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    
    # 确保页面正确 
    iRet, _ = is_in_page(input_event, [PageType.Setting_New_message_notice])
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 当前不是在新消息通知页面")
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    
    # 设置“接收新消息通知开关”
    iRet, b_is_open = is_jie_shou_new_message_notice_open()       
    if iRet !=  APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 判断接收新消息通知开关失败{}".format(iRet))
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    if b_is_open == True:
        # 点接收新消息通知开关按钮 
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            keyWord_list = ["接收新消息通知"]
            i_pian_yi = 907
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            keyWord_list = ["消息通知"]
            i_pian_yi = 838
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            keyWord_list = ["消息通知"]
            i_pian_yi = 555
        iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, keyWord_list, i_pian_yi, 0)
        if iRet != APP_RET_CODE_SUCESS:
            ensure_in_message_list_page(input_event)
            return iRet, username_of_me
        """image_check_begin()
        adb_click_new_msg_btn_for_of_new_msg_notice_page()
        iRet = wait_image_change(input_event, 0.990)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("do_weichat_setting_with_check, 被要求退出2")
            upload_snape()
            ensure_in_message_list_page(input_event)
            return iRet  
        """
        # 点击关闭系统消息通知按钮
        image_check_begin()
        adb_click_close_system_msg_notice_btn()
        # 不允许被中止的操作，所以使用g_Event_test
        iRet = wait_image_change(g_Event_test, 0.990)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("do_weichat_setting_with_check, 被要求退出3")
            ensure_in_message_list_page(input_event)
            return iRet, username_of_me
        
    # 设置“接收语音和视频通话开关”
    iRet, b_is_open = is_jie_shou_sound_and_video_open()       
    if iRet !=  APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 判断接收语音和视频通话开关失败{}".format(iRet))
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    if b_is_open == True:
        # 点接收语音和视频通话开关按钮 
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            keyWord_list = ["接收语音和视频通话邀请提醒"]
            i_pian_yi = 831
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
            keyWord_list = ["语音和视频通话通知"]
            i_pian_yi = 725
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
            keyWord_list = ["语音和视频通话通知"]
            i_pian_yi = 475
        iRet = adb_click_btn_by_ocr_if_no_finish_with_check(input_event, keyWord_list, i_pian_yi, 0)
        if iRet != APP_RET_CODE_SUCESS:
            ensure_in_message_list_page(input_event)
            return iRet, username_of_me
        
        # 点击关闭系统消息通知按钮
        image_check_begin()
        adb_click_close_system_msg_notice_btn()
        # 不允许被中止的操作，所以使用g_Event_test
        iRet = wait_image_change(g_Event_test, 0.990)
        if iRet != APP_RET_CODE_SUCESS:
            if iRet == -1:
                print_my("do_weichat_setting_with_check, 被要求退出5")
            ensure_in_message_list_page(input_event)
            return iRet, username_of_me
              
    ensure_in_message_list_page(input_event, PageType.Setting_New_message_notice)    
    '''
    # 点击设置页面的关闭按钮
    iRet = adb_click_close_setting_btn()
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!do_weichat_setting_with_check, 点击设置页面的关闭按钮失败{}".format(iRet))
        ensure_in_message_list_page(input_event)
        return iRet, username_of_me
    
    print("<===do_weichat_setting_with_check")
    TIME_END()    
    return APP_RET_CODE_SUCESS, username_of_me

#do_weichat_setting_with_check(g_Event_test)

# 获得微信窗口的焦点
def get_focus_for_windows():
    adb_click(132+G_X_PIAN_YI, 21+G_Y_PIAN_YI)  
    
# 点击朋友圈页面的关闭按钮
def adb_click_close_circle_btn():
    adb_click(int(787), int(30))
    return  APP_RET_CODE_SUCESS

# 点击朋友圈发送页面的取消按钮
def adb_click_close_circle_send_btn():
    adb_click(int(499), int(725))
    return  APP_RET_CODE_SUCESS

# 点击谁可见页面的取消按钮
def adb_click_close_who_can_see_btn():
    adb_click(int(394), int(616))
    return  APP_RET_CODE_SUCESS

# 选择谁可见页面的取消按钮
def adb_click_close_select_who_can_see_btn():
    adb_click(int(945), int(783))
    return  APP_RET_CODE_SUCESS

# 点击Windows系统的Ctrl+Z组合键，用于撤销输入的内容
def windows_click_ctrl_z(content):
    pyautogui.press('backspace', presses=len(content))