# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from enum import Enum
from screeninfo import get_monitors
from psutil import net_if_addrs, AF_LINK

# 是否是debug版本
g_b_Debug = False 
# 是否画出缩略图
g_b_Draw_snap = False
# 是否是开发模式
g_b_Develop_Mode = False
# 是否是手机远程调试开发者模式 
# 设备类型
class DEVICE_MODEL_TYPE(Enum):
    Local_Emulator = 0           # 本地模拟器  1920*1080
    WiFi_Phone_Xiaomi_8_Pro = 1  # 小米8Pro   1080*2340
    Yun_Phone_720_1080 = 2       # 云手机     720*1080
    Windows = 3                  # windows版本 1920*1080
    Windows_1366_768 = 4         # windows版本 1366*1768
    Unknow = -1                  # 未知
#g_deivce_MODEL = DEVICE_MODEL_TYPE.Yun_Phone_720_1080
g_deivce_MODEL = DEVICE_MODEL_TYPE.Windows
#g_deivce_MODEL = DEVICE_MODEL_TYPE.Windows_1366_768

if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    APP_NAME = "个微私域精灵V1.0_虚拟机RPA单机版"
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    APP_NAME = "个微私域精灵V1.0_手机RPA+Wifi版"
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    APP_NAME = "个微私域精灵V1.0_云手机RPA版"
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    APP_NAME = "个微私域精灵V1.0_WindowsRPA版"

# 支持的微信版本号 
# https://pc.weixin.qq.com
WINDOWS_WECHAT_OK_VERSION_DICT = {
    "4.1.0.18":{"download_url":"https://www.wechatai365.top:8002/download/WeChatWin_4.1.0.18.exe"},
    "4.1.0.30":{"download_url":"https://www.wechatai365.top:8002/download/WeChatWin_4.1.0.18.exe"}}

# 窗体的所有坐标的偏移
G_X_PIAN_YI = 0
G_Y_PIAN_YI = 0 
#G_X_PIAN_YI = 17
#G_Y_PIAN_YI = 17
   
CLIENT_NAME = "wechatSiYuGenie"
#LEI_DIAN_DIR = "./LDPlayer9"
APP_IMG_DIR = "./img"
APP_HTML_DIR = "./html"

HTTP_TAIL = "https"
SERVER_URL_BASE = "114.55.254.123"
#HTTP_TAIL = "https"
#SERVER_URL_BASE = "www.wechatai365.top"
SERVER_PORT = "8002"
#SERVER_URL_BASE = "183.240.111.138"
#SERVER_PORT = "8003"
#dst_filename = 'wechatAiAssistantV1.0-2024-08-29.zip'
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    #UPDATE_DST_FILENAME = 'Tesseract-OCR_TuoGuanContainer_v2.zip'  # 雷电9.0.74_微信有配置过
    UPDATE_DST_FILENAME = 'Tesseract-OCR_TuoGuanContainer_v1.zip'  # 雷电9.0.74
    #UPDATE_DST_FILENAME = 'Tesseract-OCR_TuoGuanContainer_v3.zip'   # 雷电9.1.38
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    UPDATE_DST_FILENAME = 'Tesseract-OCR_TuoGuanContainer_v4.zip'  # 手机+wifi版本
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    UPDATE_DST_FILENAME = 'Tesseract-OCR_TuoGuanContainer_v4.zip'  # 云手机版本
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    UPDATE_DST_FILENAME = 'Tesseract-OCR_TuoGuanContainer_v4.zip'  # Windows版本
    
UPDATE_DOWNLOAD_URL = '{}://{}:{}/download/'.format(HTTP_TAIL, SERVER_URL_BASE, SERVER_PORT) + UPDATE_DST_FILENAME

# 是否打开业务通知消息（通过文件传输助手）
g_b_Open_Notice = True 

# 允许雷电的最大内存(单位:MB)(超过此内存，模拟器将被重启)
# 雷电9.0.74
MAX_LEI_DIAN_MEMORY_M = 800
# 雷电9.1.38
#MAX_LEI_DIAN_MEMORY_M = 1200

# 允许雷电的最小内存(单位:MB)(小于此内存，模拟器将被重启)
MIN_LEI_DIAN_MEMORY_M = 20

# 主线程启动后允许循环的最大次数
WAIT_MAIN_LOOP_MAX_COUNT = 200

# 启动后等待“消息列表”页的等待次数(约每次20秒)
WAIT_MSG_LIST_MAX_COUNT = 6
# 在“消息列表”页的最小次数
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
    NEED_MIN_IN_MSG_LIST_COUNT = 3
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro:
    NEED_MIN_IN_MSG_LIST_COUNT = 1
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Yun_Phone_720_1080:
    NEED_MIN_IN_MSG_LIST_COUNT = 1
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    NEED_MIN_IN_MSG_LIST_COUNT = 1

# 检查消息允许的最大次数
LOOP_COUNT_MAX = 300000

# Agent或LLM请求的最多次数
AGENT_TRY_COUNT_MAX = 3

# 等待微信准备好的最多次数
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    WAIT_WECHAT_TRY_COUNT_MAX = 7
else:
    WAIT_WECHAT_TRY_COUNT_MAX = 30

# 请求LLM或Agent时多轮的最大轮次
#MAX_HISTORY_COUNT = 3
MAX_HISTORY_COUNT = 10

# 等待进入聊天页面的最大次数（每次等待1秒）
TRY_COUNT_MAX_FOR_CHAT = 6

# 任务执行的时间间隔（秒）
TASK_TIME_INTER = 60
#TASK_TIME_INTER = 5
# 是否执行过期的任务
g_b_Do_Exceed_Task = True
# 批量加好友任务执行的时间间隔（秒）
TASK_TIME_INTER_OF_ADD_NEW_FRIENT = 60*10
# 加微信群好友任务每次加好友的最大个数 
MAX_ADD_FRIEND_COUNT = 10
# 自动通过好友执行的时间间隔（秒）
AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT = 60*5
# 检索新的好友的用户名的时间间隔(秒)
#GET_NEW_FRIEND_TIME_INTER = 60*5
GET_NEW_FRIEND_TIME_INTER = 60*60*2
#GET_NEW_FRIEND_TIME_INTER = 30*1

# 等待进入添加好友页面最大次数
WAIT_ENTER_ADD_FRIEND_PAGE_CONT_MAX = 5

# 触发发现消息列表首条目变化的像素变化比例
FIRST_ITEM_CHANGE_RATIO = 0.9995

# 触发新的朋友变化的像素变化比例
NEW_FRIEND_CHANGE_RATIO = 0.9995

# 通知用对象名称
USERNAME_FOR_NOTICE = "文件传输助手"

# 自动生成图片的正向文本
POS_TEXT = ""
# 自动生成图片的反向文本 
NEG_TEXT = ""

# 判断当前是在哪个页面中
class PageType(Enum):
    Message_List = 0        # 消息列表页
    Chat = 1                # 聊天页面
    FriendBook = 2          # 通讯录页面
    Tag = 3                 # 标签页面
    Tag_Empty = 4           # 标签为空页面
    Discover = 5            # 发现页面
    Me = 6                  # 我的页面
    Setting = 7             # 设置页面
    Setting_New_message_notice = 8 # 新消息通知页面
    Add_to_FriendBook = 9   # 添加到通讯录页面
    Add_to_FriendBook_FILE_CHANGE = 10    # 添加到通讯录页面（文件传输助手）
    Add_to_FriendBook_OTHER_ZHU_DONG = 11 # 添加到通讯录页(对方主动请求)
    Friend_No_Exist = 12     # 该用户不存在
    Friend_Person_Exist = 13 # 搜索到个人信息页
    Circle = 14              # 朋友圈页
    Circle_Send = 15         # 朋友圈发表页
    Circle_Who_Can_See = 16  # 朋友圈谁可以看页
    Circle_Select_Frient =17 # 朋友圈选择朋友页
    Circle_Photo_Record = 18 # 朋友圈拍照记录生活页
    Img_And_Video = 19       # 图片和视频页
    Add_Frient = 20          # 添加朋友页
    Select_From_Album = 21   # 从相册选择页
    Search = 22              # 搜索页
    Friend_Information = 23  # 好友资料页
    New_Friend_Of_FriendBook = 24 # 新的朋友页
    Setting_Remark = 25      # 设置备注和标签页
    Subscription = 26        # 订阅号页
    GroupInfo = 27           # 群聊信息页
    GroupMember = 28         # 群成员页
    ServerNotice = 29        # 服务通知页
    CardCag = 30             # 卡包页
    ApplyAddFriend = 31      # 申请添加朋友
    OfficalAccount = 32      # 公众号页
    ChatInfo = 33            # 聊天信息页
    Collect = 34             # 收藏页
    FriendBook_Manage = 35   # 通讯录管理页
    Except = -1              # 异常页面
    Unknow = -2              # 未知
    
# 语言大模型类型
class LLM_MODEL_TYPE(Enum):
    Kimi = 0                # Kimi
    GLM = 1                 # GLM
    DouBao = 2              # 豆包
    DeepSeek_V3_GuanWang = 3 # DeepSeekV3官网
    DeepSeek_R1_GuanWang = 4   # DeepSeekR1官网
    DeepSeek_R1_Silicon = 5    # DeepseekR1硅基流动
    DeepSeek_R1_Infini = 6     # DeepseekR1无问芯穹
    DeepSeek_R1_Distill_32b_Infini = 7     # Deepseek-r1-distill-qwen-32无问芯穹
    Qwen_Qwq_Plus = 8         # Qwen-QWQ-Plus
    Qwen_Deepseek_R1 = 9      # Qwen-Deepseek_R1
    Unknow = -1             # 未知
# 真正要展示的LLM在这里配置
# "Deepseek_R1":LLM_MODEL_TYPE.DeepSeek_Infini
LLM_MODEL_NAME_TYPE_DICT = {"Deepseek_R1官网":LLM_MODEL_TYPE.DeepSeek_R1_GuanWang,
                            "Deepseek_R1阿里":LLM_MODEL_TYPE.Qwen_Deepseek_R1,
                            "Deepseek_V3官网":LLM_MODEL_TYPE.DeepSeek_V3_GuanWang,
                            "Deepseek_R1_Distill_32B无问芯穹":LLM_MODEL_TYPE.DeepSeek_R1_Distill_32b_Infini,
                            "Kimi":LLM_MODEL_TYPE.Kimi, 
                            "智谱GLM":LLM_MODEL_TYPE.GLM, 
                            "豆包":LLM_MODEL_TYPE.DouBao,
                            "千问QWQ_Plus":LLM_MODEL_TYPE.Qwen_Qwq_Plus
                            }
LLM_MODEL_TYPE_NAME_DICT = {v: k for k, v in LLM_MODEL_NAME_TYPE_DICT.items()}

# 图片生成大模型类型
class IMAGE_GEN_LLM_MODEL_TYPE(Enum):
    Qwen_wanx2_1_t2i_turbo = 0      # wanx2.1-t2i-turbo
    Unknow = -1                     # 未知
# 真正要展示的IMGAGE_GEN_LLM在这里配置
IMAGE_GEN_LLM_MODEL_NAME_TYPE_DICT = {"通义万相-文生图2.1-Turbo":IMAGE_GEN_LLM_MODEL_TYPE.Qwen_wanx2_1_t2i_turbo                          
                            }

# 系统内容旅程类型 
LV_CHENG_INFO_LIST = {"系统内置旅程_新客户":[{"DAYS_AFTER_ADD":{"START_DAY":0, "END_DAY":20}}]}
# 智能体的类型
#AGENT_CONFIG_DICT = ["激活智能体", "节日智能体"]
AGENT_CONFIG_DICT = {"种草智能体":{"time":"21:10:02"}, 
                     "知识分享智能体":{"time":"21:10:02"}, 
                     "激活智能体":{"time":"21:10:02"}, 
                     "造势智能体":{"time":"21:10:02"}, 
                     "跟进智能体":{"time":"21:10:02"}, 
                     "邀约智能体":{"time":"21:10:02"},
                     "发售智能体":{"time":"21:10:02"},
                     "交付智能体":{"time":"21:10:02"},
                     "复购智能体":{"time":"21:10:02"}}
                  
# 获取用户数据目录
def get_user_data_dir():
    import os
    import sys
    import configparser
    
    # 尝试从配置文件读取用户数据目录
    try:
        # 获取程序目录
        if hasattr(sys, 'frozen'):
            # 如果是打包后的exe
            app_dir = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            app_dir = os.path.dirname(os.path.abspath(__file__))
        
        config_path = os.path.join(app_dir, 'config.ini')
        
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path)
            if 'Paths' in config and 'UserDataDir' in config['Paths']:
                user_data_dir = config['Paths']['UserDataDir']
                # 确保目录存在
                if not os.path.exists(user_data_dir):
                    os.makedirs(user_data_dir)
                return user_data_dir
    except Exception as e:
        print(f"从配置文件读取用户数据目录失败: {e}")
    
    # 如果无法从配置文件读取，使用默认路径
    if os.name == 'nt':  # Windows系统
        user_data_dir = os.path.join(os.environ.get('APPDATA', ''), 'wechatSiYuGenie_WindowsRPA')
    else:  # 其他系统
        user_data_dir = os.path.join(os.path.expanduser('~'), '.wechatSiYuGenie_WindowsRPA')
    
    # 确保目录存在
    if not os.path.exists(user_data_dir):
        try:
            os.makedirs(user_data_dir)
        except Exception as e:
            print(f"创建用户数据目录失败: {e}")
            # 如果创建失败，使用当前目录
            return os.getcwd()
    
    return user_data_dir

# 获取用户数据目录
USER_DATA_DIR = get_user_data_dir()

# Tesseract-OCR目录
TESSERACT_DIR = os.path.join(USER_DATA_DIR, "Tesseract-OCR")

# TuoGuanContainer目录
LEI_DIAN_DIR = os.path.join(USER_DATA_DIR, "TuoGuanContainer")
if not os.path.exists(LEI_DIAN_DIR):
    try:
        os.makedirs(LEI_DIAN_DIR)
    except Exception as e:
        print(f"创建TuoGuanContainer目录失败: {e}")
        # 如果创建失败，使用当前目录下的子目录
        LEI_DIAN_DIR = "./TuoGuanContainer"
        if not os.path.exists(LEI_DIAN_DIR):
            os.makedirs(LEI_DIAN_DIR)

MESSAGE_SESSION_DIR = os.path.join(USER_DATA_DIR, "message_sessions")
if not os.path.exists(MESSAGE_SESSION_DIR):
    try:
        os.makedirs(MESSAGE_SESSION_DIR)
    except Exception as e:
        print(f"创建消息会话目录失败: {e}")
        # 如果创建失败，使用当前目录下的子目录
        MESSAGE_SESSION_DIR = "./message_sessions"
        if not os.path.exists(MESSAGE_SESSION_DIR):
            os.makedirs(MESSAGE_SESSION_DIR)

# 存截图图片的目录   
SCREENSHOT_SAVE_DIR = os.path.join(USER_DATA_DIR, "screenshot_img")
if not os.path.exists(SCREENSHOT_SAVE_DIR):
    try:
        os.makedirs(SCREENSHOT_SAVE_DIR)
    except Exception as e:
        print(f"创建截图目录失败: {e}")
        # 如果创建失败，使用当前目录下的子目录
        SCREENSHOT_SAVE_DIR = "./screenshot_img"
        if not os.path.exists(SCREENSHOT_SAVE_DIR):
            os.makedirs(SCREENSHOT_SAVE_DIR)

# 存自动生成的图片的目录   
AI_GENERATE_IMG_DIR = os.path.join(USER_DATA_DIR, "ai_generate_img")
if not os.path.exists(AI_GENERATE_IMG_DIR):
    try:
        os.makedirs(AI_GENERATE_IMG_DIR)
    except Exception as e:
        print(f"创建AI生成图片目录失败: {e}")
        # 如果创建失败，使用当前目录下的子目录
        AI_GENERATE_IMG_DIR = "./ai_generate_img"
        if not os.path.exists(AI_GENERATE_IMG_DIR):
            os.makedirs(AI_GENERATE_IMG_DIR)
 
#REMARK_PREFIX_TYPE_LIST = ["当前日期", "数字", "字母"]
#REMARK_PREFIX_TYPE_LIST = ["当前日期", "【字符】：随机加的"]
REMARK_PREFIX_TYPE_LIST = ["【当前日期】", "【添加时的搜索账号】", "【字符】：随机加的"]
REMARK_PREFIX_TYPE_LIST_FOR_PASS = ["【当前日期】", "【字符】：随机加的"]
# 根据前缀类型获得前缀串
def get_remark_prefix_str(remark_prefix_type, username = ""):
    if remark_prefix_type == "【当前日期】":
        current_date = datetime.now().date()
        date_str = current_date.strftime('%Y-%m-%d')  
        return date_str
    elif remark_prefix_type == "【添加时的搜索账号】":         
        return username
    elif remark_prefix_type == "数字":
        return "1111"
    elif remark_prefix_type == "字母":
        return "aaa"
    elif remark_prefix_type == "【字符】：随机加的":
        return "随机加的"
    else:
        return ""

#"""
def get_mac():
    str_mac_return = ""
    
    mac_addresses_dict = {}
    # 获取所有网络接口的信息
    interfaces = net_if_addrs()
    for interface, addrs in interfaces.items():
        # 排除虚拟接口和loopback接口
        if "vmnet" not in interface.lower() and "virtual" not in interface.lower() and "loopback" not in interface.lower() and "vmware" not in interface.lower() and "microsoft" not in interface.lower():
            for addr in addrs:
                if addr.family == AF_LINK:
                    mac_addresses_dict[interface] = addr.address
                    break  # 假设每个物理接口只有一个MAC地址，找到后即跳出循环
    # chenyj debug 
    #print(mac_addresses_dict)
    # 先只取第一个
    for interface_name in mac_addresses_dict:
        str_mac_return = mac_addresses_dict[interface_name]
        break
    return str_mac_return
#"""

#print(get_mac())

def get_normal_string_before_emoji(s):
    # 定义正则表达式，匹配正常的英文、汉字、数字和常见字符
    pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9&()（）]+'
    match = re.search(pattern, s)
    if match:
        return match.group(0)
    return ""
# 测试字符串
"""
#s = "董俊鑫🐘北辰职校&中南培训中心"
#s = "董俊鑫(北辰职校&中南培训中心"
s = "董俊鑫◆北辰职校@中南培训中心"
result = get_normal_string_before_emoji(s)
print(result)
"""

def clean_string(input_string):
    # 使用正则表达式只保留英文、汉字和数字
    cleaned_string = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', input_string)
    return cleaned_string
# 测试字符串
"""
#s = "董俊鑫🐘北辰职校&中南培训中心"
#s = "董俊鑫(北辰职校&中南培训中心"
#s = "董俊q鑫◆北辰①、②职校@中（南(培aaz训中04心"
#s = "董俊鑫☒北辰职校&中南培训中心"
#s = "教培老师《※。北辰职校"
#s = "®叶灵13560758149"
#s = "☒施夏贤〔资质认证融资)"
s = "吻■江嘉君知新教育"
s = "信吹▣"
result = clean_string(s)
print(result)
"""

import re

def insert_star_except_between_digits(input_string):
    # 匹配连续字母的起始位置或需要插入星号的其他边界
    pattern = r'''
        (?<![A-Za-z])(?=[A-Za-z])   # 连续字母的起始位置
        |                           
        (?<=\D)(?=\D)(?<![A-Za-z])(?![A-Za-z])  # 非字母之间的非连续位置
        |                           
        (?<=\D)(?=\d)               # 非数字与数字的边界
        |                           
        (?<=\d)(?=\D)               # 数字与非数字的边界
    '''
    result = re.sub(pattern, '*', input_string, flags=re.X)
    return result

# 测试字符串
"""
s = "学adc府北辰教育&晶晶老师18028707364"
s = "hello123world"
#s = "123你好"
s = "Neo网上1合作"
s = "J.M蒋敏"
s = clean_string(s)
print(s)
result = insert_star_except_between_digits(s)
print(result)
"""

# 这种方法不准
#g_desktop_w = win32api.GetSystemMetrics(0)
#g_desktop_h = win32api.GetSystemMetrics(1)
#print("Windows桌面屏幕分辨率为:{}x{}".format(g_desktop_w, g_desktop_h))

# 获取桌面分辨率
def get_resolution():
    monitors = get_monitors()
    for monitor in monitors:
        if monitor.is_primary:
            return monitor.width, monitor.height
    return None, None
g_desktop_w, g_desktop_h = get_resolution()
print("Windows桌面屏幕分辨率为:{}x{}".format(g_desktop_w, g_desktop_h))