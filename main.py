# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sys
from splash_screen import SplashScreen
import ctypes  

ERROR_ALREADY_EXISTS = 183
# 定义一个全局唯一的名称（GUID）  
MUTEX_NAME = r'Global\weChatAssistanceNameMutex'  
def is_already_running():  
    """  
    检查并防止多个实例运行。  
    如果当前是第一个实例，返回True；否则，显示已运行的实例并退出。  
    """  
    hMutex = ctypes.windll.kernel32.CreateMutexW(  
        ctypes.c_void_p(),  # lpMutexAttributes  
        0,                  # bInitialOwner  
        MUTEX_NAME          # lpName  
    )  
  
    errorCode = ctypes.GetLastError()  
    if errorCode == ERROR_ALREADY_EXISTS:  
        # 互斥量已存在，表示另一个实例正在运行  
        ctypes.windll.kernel32.CloseHandle(hMutex)  
        # 可选：查找并显示已运行的实例窗口  
        hwnd = ctypes.windll.user32.FindWindowW(None, "Your Application Window Title")  
        if hwnd != 0:  
            ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_RESTORE)  
            ctypes.windll.user32.SetForegroundWindow(hwnd)  
        return True 
    else:  
        # 当前是第一个实例  
        return False  
    return False
if True == is_already_running():
    print("程序已经在运行中。")
    sys.exit(0)

app = QApplication(sys.argv)
# 创建并显示启动画面
splash = SplashScreen()
splash.show()
app.processEvents()  # 确保启动画面立即显示
splash.updateMessage("正在加载模块...")



from memory_profiler_helper import DEBUG_CURREN_MEM
DEBUG_CURREN_MEM("main.py 刚开始")
import gc
DEBUG_CURREN_MEM("main.py 加载gc")
import ctypes  
DEBUG_CURREN_MEM("main.py 加载ctypes")
import sys  
import traceback
DEBUG_CURREN_MEM("main.py 加载sys")
import time  
DEBUG_CURREN_MEM("main.py 加载time")
import win32con  
DEBUG_CURREN_MEM("main.py 加载win32con")
from server_http_opt import *
DEBUG_CURREN_MEM("main.py 加载server_http_opt")
from coze_helper import COZE_FRON_STR

# 定义全局异常处理函数
def handle_exception_global(exc_type, exc_value, exc_traceback):
    # 忽略中断信号（如 Ctrl+C）
    if issubclass(exc_type, KeyboardInterrupt):
        print("全局异常处理函数中捕获到程序被用户中断。")
        return
    
    # 打印异常信息到控制台
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print("全局异常处理函数中捕获到未处理的异常：", error_msg)
    http_report_log("全局异常处理函数中捕获到未处理的异常：" + error_msg)
    
    return  
    
# 替换默认的异常处理函数
sys.excepthook = handle_exception_global
###############################################################################################
# 先把窗口显示出来 
from PyQt5.QtWidgets import QWidget, QMainWindow, QDialog, QProgressDialog, QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QTextEdit, QLabel, QSystemTrayIcon, QMenu, QAction, QListWidget, QCheckBox, QMessageBox, QListWidgetItem, QTableView, QHeaderView, QTabWidget, QTableWidget, QLineEdit, QVBoxLayout, QTabBar, QStylePainter, QStyleOptionTab, QStyle, QSpacerItem, QSizePolicy, QRadioButton
from PyQt5.QtGui import QStandardItem, QPixmap, QFontMetrics, QPainter, QIntValidator, QImageReader, QPen, QColor, QBrush
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSortFilterProxyModel, QPropertyAnimation, QEasingCurve, QPointF
import random

class LoadingDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Loading...')
        self.setGeometry(300, 300, 200, 100)
        layout = QVBoxLayout()
        self.label = QLabel('Loading, please wait...', self)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()
        

#loading_dialog = LoadingDialog()
# 创建并启动加载线程
#loading_thread = LoadingThread()
#loading_thread.finished.connect(lambda: (loading_dialog.close()))
#loading_thread.start()
    
###############################################################################################
import webbrowser
import os
import copy
DEBUG_CURREN_MEM("main.py 加载copy")
import ast
DEBUG_CURREN_MEM("main.py 加载ast")
import datetime
DEBUG_CURREN_MEM("main.py 加载datetime")
import threading
DEBUG_CURREN_MEM("main.py 加载threading")
import zipfile
from random import randint, uniform
import tkinter as tk
from tkinter import filedialog
import psutil
from threading import Event
DEBUG_CURREN_MEM("main.py 加载zipfile、random、tkinter、psutil、threading")
from log_helper import print_init, print_my
DEBUG_CURREN_MEM("main.py 加载log_helper")
from app_info import *
import app_info
DEBUG_CURREN_MEM("main.py 加载app_info")
from config_helper import *
from error_code import *
DEBUG_CURREN_MEM("main.py 222")
from windows_helper import windows_find_lei_dian_window, windows_minimize_lei_dian, windows_restore_lei_dian, is_resolution_satify, is_resolution_right, set_resolution_to_1920x1080, reset_resolution, start_block_inputs, stop_block_inputs
DEBUG_CURREN_MEM("main.py 333")
from image_helper import has_img_change, get_md5_of_image
from download_helper import download_file
DEBUG_CURREN_MEM("main.py 444")
from excel_helper import *
from pic_button import PicButton
from llm_helper import *
from custom_tab_bar import CustomTabBar
from clickable_label import ClickableLabel
from dialog_right_panel import RightPanelWindow
from dialog_login import LoginWindow
from dialog_payment import PaymentWindow
from custom_main_title_bar import CustomMainTitleBar
from dialog_me import MeWindow
######################配置文件处理########################3
g_config_json_data = {}
g_str_mac = ""
   
g_config_json_data = load_config_data(g_config_path)
if "HAS_SETTING_SUCESS" not in g_config_json_data:
    g_config_json_data["HAS_SETTING_SUCESS"] = False
    save_config_data(g_config_json_data, g_config_path)
else:
    print_my("HAS_SETTING_SUCESS:{} -- 从配置文件里读取".format(g_config_json_data["HAS_SETTING_SUCESS"]))
    pass

g_config_json_data = load_config_data(g_config_path)
if "CURRENT_LOGON_USERNAME" not in g_config_json_data:
    g_config_json_data["CURRENT_LOGON_USERNAME"] = ""
    g_config_json_data["CURRENT_LOGON_USERNAME_ONLINE"] = "0"
    g_config_json_data["PHONE_CONNECTED"] = "0"
    # 为了那些以前那些正在使用，但没有获取登录用户名的用户，这里会要求去获取一次
    g_config_json_data["HAS_SETTING_SUCESS"] = False
    save_config_data(g_config_json_data, g_config_path)
else:
    print_my("CURRENT_LOGON_USERNAME:{} -- 从配置文件里读取".format(g_config_json_data["CURRENT_LOGON_USERNAME"]))
    pass
# chenyj test 先跳过微信初始化配置
"""
if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
	g_config_json_data["HAS_SETTING_SUCESS"] = True
	save_config_data(g_config_json_data, g_config_path)
"""

if "FIRST" not in g_config_json_data:
    #time_now = datetime.datetime.now()
    time_now = time.time()
    print_my("第一次运行的时间是:{}".format(time_now))
    g_config_json_data["FIRST"] = time_now
    g_config_json_data["USER_TYPE"] = "-2"
    save_config_data(g_config_json_data, g_config_path)

if "MAC_ADDRESS" not in g_config_json_data:
    g_str_mac = get_mac()
    if len(g_str_mac) == 0:
        print_my("!!!!!!无法获得本机mac地址")
    print_my("本机的mac地址是:{} -- 从api中读取".format(g_str_mac))
    g_config_json_data["MAC_ADDRESS"] = g_str_mac
    save_config_data(g_config_json_data, g_config_path)
else:
    g_str_mac = g_config_json_data["MAC_ADDRESS"]
    print_my("本机的mac地址是:{} -- 从配置文件里读取".format(g_str_mac))

if "BIND_PHONE" not in g_config_json_data:
    g_config_json_data["BIND_PHONE"] = ""
    save_config_data(g_config_json_data, g_config_path)
else:
    print_my("话术文件列表:{} -- 从配置文件里读取".format(g_config_json_data["BIND_PHONE"]))
    
if "HUA_SU_FILES" not in g_config_json_data:
    g_config_json_data["HUA_SU_FILES"] = ["自定义本地话术库.txt"]
    save_config_data(g_config_json_data, g_config_path)
else:
    print_my("话术文件列表:{} -- 从配置文件里读取".format(g_config_json_data["HUA_SU_FILES"]))

if "sel_agent_list" not in g_config_json_data:
    g_config_json_data["sel_agent_list"] = ["闲聊专家自定义本地话术库"]
    save_config_data(g_config_json_data, g_config_path)
else:
    sel_agent_list = g_config_json_data["sel_agent_list"]
    #if len(sel_agent_list) == 0:
    #    g_config_json_data["sel_agent_list"] = ["KimiChat大模型"]
    #    save_config_data(g_config_json_data, g_config_path)

if "TASK_INFO_LIST" not in g_config_json_data:
    g_config_json_data["TASK_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("任务列表:{} -- 从配置文件里读取".format(g_config_json_data["TASK_INFO_LIST"]))
    pass

if "PRODUCT_INFO_LIST" not in g_config_json_data:
    g_config_json_data["PRODUCT_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("产品列表:{} -- 从配置文件里读取".format(g_config_json_data["PRODUCT_INFO_LIST"]))
    pass

if "FRIEND_INFO_LIST" not in g_config_json_data:
    g_config_json_data["FRIEND_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("好友列表:{} -- 从配置文件里读取".format(g_config_json_data["FRIEND_INFO_LIST"]))
    pass

if "USERGROUP_INFO_LIST" not in g_config_json_data:
	# 增加系统内置旅程组
	usergroup_info_list = []
	for lv_cheng_name in LV_CHENG_INFO_LIST:
		if lv_cheng_name in [usergroup_info["usergroup_name"] for usergroup_info in usergroup_info_list]:
			continue
		rule_info_list = LV_CHENG_INFO_LIST[lv_cheng_name]
		add_usergroup_data_dict = {}
		add_usergroup_data_dict["usergroup_name"] = lv_cheng_name
		add_usergroup_data_dict["add_model_name"] = "根据时间规则创建"
		add_usergroup_data_dict["rule_info_list"] = rule_info_list
		add_usergroup_data_dict["usergroup_member"] = []
		usergroup_info_list.append(add_usergroup_data_dict)
	g_config_json_data["USERGROUP_INFO_LIST"] = usergroup_info_list
	save_config_data(g_config_json_data, g_config_path)
    #g_config_json_data["USERGROUP_INFO_LIST"] = []
    #save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("客户组列表:{} -- 从配置文件里读取".format(g_config_json_data["USERGROUP_INFO_LIST"]))
	pass

if "CONTENT_INFO_LIST" not in g_config_json_data:
    g_config_json_data["CONTENT_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("内容列表:{} -- 从配置文件里读取".format(g_config_json_data["CONTENT_INFO_LIST"]))
    for content_info in g_config_json_data["CONTENT_INFO_LIST"]:
        if "go_where" not in content_info:
            content_info["go_where"] = ""
        if "tong_dian" not in content_info:
            content_info["tong_dian"] = ""
        if "superiority" not in content_info:
            content_info["superiority"] = ""

    pass
 
if "AUTOREPLY_INFO_LIST" not in g_config_json_data:
    g_config_json_data["AUTOREPLY_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("智能客服机器人列表:{} -- 从配置文件里读取".format(g_config_json_data["AUTOREPLY_INFO_LIST"]))
    pass
    
if "AUTOADD_INFO_LIST" not in g_config_json_data:
    g_config_json_data["AUTOADD_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("智能添加机器人列表:{} -- 从配置文件里读取".format(g_config_json_data["AUTOADD_INFO_LIST"]))
    pass
    
if "AUTOPASS_INFO_LIST" not in g_config_json_data:
    g_config_json_data["AUTOPASS_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    print("智能通友机器人列表:{}个数据 -- 从配置文件里读取".format(len(g_config_json_data["AUTOPASS_INFO_LIST"])))
    pass
       
if "AGENT_INFO_LIST" not in g_config_json_data:
    g_config_json_data["AGENT_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("智能体列表:{} -- 从配置文件里读取".format(g_config_json_data["AGENT_INFO_LIST"]))
    pass

if "COZE_AGENT_INFO_LIST" not in g_config_json_data:
    g_config_json_data["COZE_AGENT_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("扣子智能体列表:{} -- 从配置文件里读取".format(g_config_json_data["COZE_AGENT_INFO_LIST"]))
    pass

if "PHONE_INFO_LIST" not in g_config_json_data:
    g_config_json_data["PHONE_INFO_LIST"] = []
    save_config_data(g_config_json_data, g_config_path)
else:
    #print_my("手机对象列表:{} -- 从配置文件里读取".format(g_config_json_data["PHONE_INFO_LIST"]))
    pass

if "LLM_INFO_LIST" not in g_config_json_data:
	# 增加系统内置LLM

	llm_info_list = get_default_llm_info_list()
	g_config_json_data["LLM_INFO_LIST"] = llm_info_list	
	save_config_data(g_config_json_data, g_config_path)
else:
	do_reload_llm_info()
    #print_my("大模型配置列表:{} -- 从配置文件里读取".format(g_config_json_data["LLM_INFO_LIST"]))
	pass

    
if "device_ready_befor" not in g_config_json_data:
    g_config_json_data["device_ready_befor"] = False

if "info_of_deposit_list" not in g_config_json_data:
    g_config_json_data["info_of_deposit_list"] = []     
            
if "GET_NEW_FRIEND_TIME_INTER" not in g_config_json_data:
    g_config_json_data["GET_NEW_FRIEND_TIME_INTER"] = GET_NEW_FRIEND_TIME_INTER
else:
    GET_NEW_FRIEND_TIME_INTER = g_config_json_data["GET_NEW_FRIEND_TIME_INTER"]

if "TASK_TIME_INTER" not in g_config_json_data:
    g_config_json_data["TASK_TIME_INTER"] = TASK_TIME_INTER
else:
    app_info.TASK_TIME_INTER = g_config_json_data["TASK_TIME_INTER"]

if "g_b_Do_Exceed_Task" not in g_config_json_data:
    g_config_json_data["g_b_Do_Exceed_Task"] = g_b_Do_Exceed_Task
else:
    g_b_Do_Exceed_Task = g_config_json_data["g_b_Do_Exceed_Task"]

if "TASK_TIME_INTER_OF_ADD_NEW_FRIENT" not in g_config_json_data:
    g_config_json_data["TASK_TIME_INTER_OF_ADD_NEW_FRIENT"] = TASK_TIME_INTER_OF_ADD_NEW_FRIENT
else:
    app_info.TASK_TIME_INTER_OF_ADD_NEW_FRIENT = g_config_json_data["TASK_TIME_INTER_OF_ADD_NEW_FRIENT"]

if "AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT" not in g_config_json_data:
    g_config_json_data["AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT"] = AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT
else:
    AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT = g_config_json_data["AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT"]
   
if "POS_TEXT" not in g_config_json_data:
    g_config_json_data["POS_TEXT"] = POS_TEXT
else:
    app_info.POS_TEXT = g_config_json_data["POS_TEXT"]

if "NEG_TEXT" not in g_config_json_data:
    g_config_json_data["NEG_TEXT"] = POS_TEXT
else:
    app_info.NEG_TEXT = g_config_json_data["NEG_TEXT"]
    
#http_init(g_str_mac, CLIENT_NAME, g_config_json_data)
###############################常量数据配置区################################

LOG_FILE_PATH = os.path.join(USER_DATA_DIR, "log.txt")
SECTRY_STR = "%￥#*&#"
#SECONDS_LIMIT_OF_TRIAL = 3600*24*265*10
SECONDS_LIMIT_OF_TRIAL = 3600*24*7
#SECONDS_LIMIT_OF_TRIAL = 2
#SECONDS_LIMIT_OF_TRIAL = 60
SECONDS_LIMIT_OF_ONE_MONTH = 3600*24*30
SECONDS_LIMIT_OF_ONE_YEAR = 3600*24*30*12

#############################其它全局变量############################################
g_Event_for_heart_beat = Event()
g_Event_for_app_check = Event()
g_Event_for_main_work = Event()    

##############################日志处理相关#######################################################
g_lock_logger = threading.Lock()
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.filename = filename
        
    def write(self, message):
        g_lock_logger.acquire()
        try:
            self.log = open(self.filename, "a", encoding="utf-8")  # 防止编码错误
            # 注意：如果是打包成exe，下面这行要注释掉，不然运行报错
            if g_b_Debug == True and self.terminal != None:
                self.terminal.write(message)
            # 添加当前日期时间
            current_datetime = datetime.now()
            current_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            #current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 避免重复添加时间戳
            if not message.startswith("\n"):
                message = "[{}] ".format(current_time) + message
            self.log.write(message)
            self.log.close()
        finally:
            g_lock_logger.release()
            
    def flush(self):
        pass
    def reset(self):
        #self.log.close()
        sys.stdout=self.terminal

sys.stdout = Logger(LOG_FILE_PATH) 
#############################################################################
import shutil 
#from PyQt5.QtWidgets import QWidget, QDialog, QProgressDialog, QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QTextEdit, QLabel, QSystemTrayIcon, QMenu, QAction, QListWidget, QCheckBox, QMessageBox, QStyledItemDelegate, QListWidgetItem
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor, QStandardItemModel
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QProcess, QProcessEnvironment, pyqtSlot
#import dou_yin_by_ye_shen_opt as dou_yin_by_ye_shen_opt
#import dou_yin_by_lei_dian_opt_baidu_ocr as dou_yin_by_lei_dian_opt
#import dou_yin_by_xiang_ri_kui_opt as dou_yin_by_xiang_ri_kui_opt
from base64 import b64decode
import pyperclip as pc
DEBUG_CURREN_MEM("main.py 555")
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from dialog_add_task import AddTaskWindow
from dialog_add_deposit_object import AddDepositObjectWindow
from dialog_add_usergroup import AddUserGroupWindow
from dialog_add_product import AddProductWindow
from dialog_add_content import AddContentWindow
from dialog_add_agent import AddAgentWindow
from dialog_add_autoreply import AddAutoReplyWindow
from dialog_add_autoadd import AddAutoAddWindow
from dialog_add_autopass import AddAutoPassWindow
from dialog_add_llm import AddLLMWindow
from dialog_add_coze_agent import AddCozeAgentWindow
from dialog_add_phone import AddPhoneWindow
from dialog_waiting import WaitingWindow
from dialog_view_task import ViewTaskWindow
from agent_helper import AGENT_INFO_DICT
DEBUG_CURREN_MEM("main.py 666")
from yang_hao_opt import *
from enviroment_check_helper import check_virtualization, is_another_lei_dian_running, is_360_running, is_windows_defender_enabled, open_windows_defender_panel, is_virtual_machine
from test_baidu_ocr import get_access_token
from task_helper import get_random_one_task, process_one_task, get_task_detail_data, update_task_state_by_setting

# 判断是否授权过期
# user_type
#        -2 过期 
#        -1 试用
#         0 永久 
#         1 1个月
#         2 1年
def is_out_of_time():
    global g_config_json_data
    
    first_time = g_config_json_data["FIRST"]
    user_type = g_config_json_data["USER_TYPE"]
    if user_type == "-2":
        return True, 0
    elif user_type == "0":  
        return False, 0
    # 防止时间篡改    
    time_now = time.time()
    if time_now < first_time:
        g_config_json_data["FIRST"] = time_now
        g_config_json_data["USER_TYPE"] = "-2"
        save_config_data(g_config_json_data, g_config_path)
        return True, 0
    dela_time = time_now - first_time
    
    seconds_limit = SECONDS_LIMIT_OF_TRIAL
    if user_type == "-1":
        seconds_limit = SECONDS_LIMIT_OF_TRIAL
    elif user_type == "1":
        seconds_limit = SECONDS_LIMIT_OF_ONE_MONTH
    elif user_type == "2":
        seconds_limit = SECONDS_LIMIT_OF_ONE_YEAR
    # chenyj debug
    #print_my("经过了{}秒时间".format(dela_time))
    #if dela_time > seconds_limit and g_config_json_data["USER_TYPE"] == "-1":
    if dela_time > seconds_limit and g_config_json_data["USER_TYPE"] in ["-1", "1", "2"]:
        return True,  0
    return False, int(seconds_limit - dela_time)
########################################################
g_table = None
g_new_msg_count = 0
# 设置table中某个作品的作品数
# i_zhu_ye_index ： 作品数的index(0:表示第一个）
def update_new_msg_count(i_new_msg_count):
    global g_table 
    global g_new_msg_count
    
    if g_table  is None: 
        return
        
    g_new_msg_count = i_new_msg_count
    g_table.signal_of_table.emit("update_new_msg_count")
    return
    
# 组件下载线程
def download_thread(table):
    dialog_downloading = table.dialog_downloading

    #"""
    try:
        # chenyj debug
        print_my("!!!!【托管软件初始化】开始下载文件{}".format(UPDATE_DST_FILENAME))
        # 修改下载路径到用户数据目录
        download_path = os.path.join(USER_DATA_DIR, UPDATE_DST_FILENAME)
        for finish_count in download_file(UPDATE_DOWNLOAD_URL, download_path):
            if finish_count is None:
                break 
            #dialog_downloading.setValue(finish_count)
            table.signal_of_table.emit("download_finish_count_{}".format(finish_count))
        # chenyj debug
        print_my("!!!!【托管软件初始化】文件{}下载成功".format(UPDATE_DST_FILENAME))
    except Exception as e:
        print_my("!!!!【托管软件初始化】文件{}下载异常[网络异常]\n{}".format(UPDATE_DST_FILENAME, e))
        table.signal_of_table.emit("download_failed")
        return 
    #"""
    
    # 原有文件夹先删除 
    try:
        if True == os.path.exists(LEI_DIAN_DIR):
            print("删除原有目录:{}".format(LEI_DIAN_DIR))
            shutil.rmtree(LEI_DIAN_DIR)  
        if True == os.path.exists(TESSERACT_DIR):
            print("删除原有目录:{}".format(TESSERACT_DIR))
            shutil.rmtree(TESSERACT_DIR)   
    except Exception as e:
        print_my("!!!!【托管软件初始化】删除文件异常\n{}".format(e))
        table.signal_of_table.emit("download_failed")
        return 
        
    # 解压
    try:
        print_my("开始解压，请稍候...")
        # 修改解压路径到用户数据目录
        extract_to = USER_DATA_DIR
        download_path = os.path.join(USER_DATA_DIR, UPDATE_DST_FILENAME)
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            # 使用内存缓冲方式解压，避免编码问题
            import io
            zip_buffer = io.BytesIO()
            with open(download_path, 'rb') as f:
                zip_buffer.write(f.read())
            zip_buffer.seek(0)
            
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref_new:
                zip_ref_new.extractall(extract_to)
            # chenyj debug
            print("解压完成：{} -> {}".format(UPDATE_DST_FILENAME, extract_to))
    except Exception as e:
        print_my("!!!!【托管软件初始化】解压异常\n{}".format(e))
        table.signal_of_table.emit("download_failed")
        return 
    
    print_my("!!!!!【托管软件初始化】成功")
    table.signal_of_table.emit("download_sucess")
     
    return

# 进程Ld9BoxHeadless.exe进程缺失次数
g_i_ld9box_headless_process_missing_count = 0
# 当雷电占用内存太大时，将雷电模拟器重启
g_rss_M_last = 0.0
# 内存连续异常的次数
g_i_mem_exception_couunt = 0
def restart_lei_dian_when_memory_high(table):
    global g_i_ld9box_headless_process_missing_count
    global g_rss_M_last
    global g_i_mem_exception_couunt
    
    b_should_restart = False 
    
    PROCESS_NAME_OF_VIRTUALBOX = 'Ld9BoxHeadless.exe'
    process_of_VirtualBox = None
    PROCESS_NAME_OF_LEIDIAN = 'dnplayer.exe'
    process_of_leiDian = None

    # 获取所有进程信息
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == PROCESS_NAME_OF_VIRTUALBOX:
            process_of_VirtualBox = proc
        if proc.info['name'] == PROCESS_NAME_OF_LEIDIAN:
            process_of_leiDian = proc
    if process_of_VirtualBox is None and process_of_leiDian is None:
        print("[{}]进程找不到".format(PROCESS_NAME_OF_VIRTUALBOX))
        return
    if process_of_VirtualBox is None and process_of_leiDian is not None:
        g_i_ld9box_headless_process_missing_count += 1
        if g_i_ld9box_headless_process_missing_count >= 20:
            print_my("!!!![{}]进程缺失, {}次, 将重启托管器".format(PROCESS_NAME_OF_VIRTUALBOX, g_i_ld9box_headless_process_missing_count))
            g_i_ld9box_headless_process_missing_count = 0
            try:
                process_of_leiDian.terminate()  # 发送terminate信号，相当于在Windows上点击结束任务
                process_of_leiDian.wait()  # 等待进程结束
                print_my("!!!!![{}]进程停止成功, 通知主业务线程要停止0".format(PROCESS_NAME_OF_VIRTUALBOX))
                g_Event_for_main_work.set()
                # 给一定时间,让主线程退出下
                time.sleep(20)
                table.signal_of_table.emit("start_btn_fun") 
            except psutil.NoSuchProcess:
                print_my("[{}]进程已经不存在.0".format(PROCESS_NAME_OF_VIRTUALBOX))
            except psutil.AccessDenied:
                print_my("!!!!!在停止[{}]进程时,权限不被允许.0".format(PROCESS_NAME_OF_VIRTUALBOX))
            except Exception as e:
                print_my("!!!!!在停止[{}]进程时,发生了异常0\n:{}".format(PROCESS_NAME_OF_VIRTUALBOX, e))
            return
        else:
            print_my("[{}]进程缺失, {}次, 继续等待".format(PROCESS_NAME_OF_VIRTUALBOX, g_i_ld9box_headless_process_missing_count))
            return
    
    g_i_ld9box_headless_process_missing_count = 0
        
    # 启动1分钟后再检查 
    start_time = process_of_VirtualBox.create_time()
    current_time = time.time()
    elapsed_time = current_time - start_time
    # chenyj debug
    #print("[{}]进程已经运行了{:.2f}秒".format(process_name_of_VirtualBox, elapsed_time))
    if elapsed_time < 60:
        return
    
    # 获取内存信息
    memory_info = process_of_VirtualBox.memory_info()
    # 打印RSS（常驻集大小，即实际使用的物理内存）
    rss_M = memory_info.rss / (1024 * 1024)
    
    # chenyj debug
    #print("[{}]进程占用{:.2f} MB内存(RSS)".format(process_name_of_VirtualBox, rss_M))
    if rss_M > MAX_LEI_DIAN_MEMORY_M:
        g_i_mem_exception_couunt += 1
    elif rss_M < MIN_LEI_DIAN_MEMORY_M:
        g_i_mem_exception_couunt += 1
    else:
        g_i_mem_exception_couunt = 0
    if g_i_mem_exception_couunt >= 6:
        print_my("!!!![{}]托管器占用{:.2f}MB内存(RSS)({}->{}),大于极限值{}MB或小于极限值{}MB, {}次, 将重启托管器".format(process_name_of_VirtualBox, rss_M, g_rss_M_last, rss_M, MAX_LEI_DIAN_MEMORY_M, MIN_LEI_DIAN_MEMORY_M, g_i_mem_exception_couunt))
        b_should_restart = True
        g_i_mem_exception_couunt = 0
    """
    if rss_M > MAX_LEI_DIAN_MEMORY_M or rss_M < MIN_LEI_DIAN_MEMORY_M:
        # chenyj debug
        print("[{}]托管器占用{:.2f}MB内存(RSS)({}->{}).存在波动,继续观察".format(process_name_of_VirtualBox, rss_M, g_rss_M_last, rss_M))
        if rss_M - g_rss_M_last < 50:
            print_my("!!!![{}]托管器占用{:.2f}MB内存(RSS)({}->{}),大于极限值{}MB或小于极限值{}MB, 将重启托管器".format(process_name_of_VirtualBox, rss_M, g_rss_M_last, rss_M, MAX_LEI_DIAN_MEMORY_M, MIN_LEI_DIAN_MEMORY_M))
            b_should_restart = True
    """    
    # 结束进程
    if b_should_restart == True:
        try:
            process_of_leiDian.terminate()  # 发送terminate信号，相当于在Windows上点击结束任务
            process_of_leiDian.wait()  # 等待进程结束
            print_my("!!!!![{}]进程停止成功, 通知主业务线程要停止".format(process_name_of_VirtualBox))
            g_Event_for_main_work.set()
            # 给一定时间,让主线程退出下
            time.sleep(20)
            table.signal_of_table.emit("start_btn_fun") 
        except psutil.NoSuchProcess:
            print_my("[{}]进程已经不存在.".format(process_name_of_VirtualBox))
        except psutil.AccessDenied:
            print_my("!!!!!在停止[{}]进程时,权限不被允许.".format(process_name_of_VirtualBox))
        except Exception as e:
            print_my("!!!!!在停止[{}]进程时,发生了异常\n:{}".format(process_name_of_VirtualBox, e))
            
    g_rss_M_last = rss_M
    
    return

def do_when_wechat_logoff(table):
    global g_config_json_data
    global g_config_path
    
    g_config_json_data["HAS_SETTING_SUCESS"] = False
    g_config_json_data["CURRENT_LOGON_USERNAME"] = ""
    g_config_json_data["CURRENT_LOGON_USERNAME_ONLINE"] = "0"
    save_config_data(g_config_json_data, g_config_path)
    table.signal_of_table.emit("update_logon_wechat_state") 
    #table.signal_of_table.emit("start_btn_fun")
    return 

def do_when_device_no_ready(table):
    global g_config_json_data
    global g_config_path

    g_config_json_data["CURRENT_LOGON_USERNAME_ONLINE"] = "0"
    save_config_data(g_config_json_data, g_config_path)
    table.signal_of_table.emit("update_logon_wechat_state") 
    return 

def do_when_device_ready(table):
    global g_config_json_data
    global g_config_path

    g_config_json_data["CURRENT_LOGON_USERNAME_ONLINE"] = "1"
    save_config_data(g_config_json_data, g_config_path)
    table.signal_of_table.emit("update_logon_wechat_state") 
    return 

g_i_second_wait = 30
# 心跳线程  
def heart_beat_thread(table):
    global g_config_json_data
    global g_config_path
    global g_i_second_wait

    # chenyj debug
    print("===>心跳线程名称:{} 参数：{} 开始时间:{}".format(threading.current_thread().name, table, time.strftime("%Y-%m-%d %H:%M:%S")))
    while True:
        # 授权
        b_outdate, delta_second = is_out_of_time()
        if b_outdate == True:
            if "BIND_PHONE"  in g_config_json_data and len(g_config_json_data["BIND_PHONE"]) > 0:
                bRet, licences_return = http_get_licence(g_config_json_data["BIND_PHONE"])
                if bRet == True and len(licences_return) > 0:
                    licence_info = licences_return[0]
                    user_type = licence_info["user_type"]             
                    time_now = time.time()
                    g_config_json_data["FIRST"] = time_now
                    g_config_json_data["USER_TYPE"] = user_type
                    save_config_data(g_config_json_data, g_config_path)
                    b_outdate, delta_second = is_out_of_time()        
                    print_my("下发授权配置成功。当前状态：{}".format("试用(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != "0" else "永久会员"))
			
                    # 
                    if True == hasattr(table, 'payment_Win') and table.payment_Win != None:
                        table.signal_of_table.emit("close_payment_win")

        if True == g_Event_for_heart_beat.wait(g_i_second_wait):
            print_my("heart_beat_thread, 被要求退出1")
            break
        continue
    # chenyj debug
    print("<===心跳线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
    
    return

# 运行状态监控线程  
def app_check_thread(table):
    global g_config_json_data
    global g_config_path
    
    # chenyj debug
    print("===>程序检查线程名称:{} 参数：{} 开始时间:{}".format(threading.current_thread().name, table, time.strftime("%Y-%m-%d %H:%M:%S")))
    
    b_shou_lei_dian_minimize = True
    i_check_count = 0
    i_last_exception_state = APP_RET_CODE_SUCESS
    i_last_phone_ready = True
    while True:
        i_check_count += 1
        # 通过窗口判断雷电模拟器是否存在 
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            if False == windows_find_lei_dian_window(False):
                print_my("!!!!托管容器还没启动，请点击“启动智能客服”按钮来启动...")
                table.set_state(EnvStateType.Env_Start_Simulator_State, False)
                # 暂停间隔时间
                if True == g_Event_for_app_check.wait(2):
                    print_my("app_check_thread, 被要求退出1")
                    break
                continue
        elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
            # 保证微信在前台运行
            if is_weChat_running() == False:
                print("!!!!app_check_thread, 检测到微信没有启动或没有置顶，偿试启动并置顶")
                open_wechat_app_and_set_top() 
            else:
                # 将窗口嵌入到我们的窗口内
                iRet, hwd_wechat = get_wechat_window()
                if iRet == APP_RET_CODE_SUCESS:
                    if table.rightPanelWin is not None:
                        print(f"app_check_thread,微信窗口的句柄是:{hwd_wechat},请求右边窗口更新")
                        table.rightPanelWin._signal_self.emit(f"merge_wechat_windows_{hwd_wechat}") 
        else:
            # 远程模式下，需要判断是否有设备
            if i_check_count % 3 == 0:
                # 保证设备正常
                iRet = adb_is_remote_phone_ready(table)
                #  先更新是否连接的标志位
                if iRet == APP_RET_CODE_PHONE_NO_CONNECT:
                    if i_last_phone_ready == True:
                    	g_config_json_data["PHONE_CONNECTED"] = "0"
                else:
                   if i_last_phone_ready == False:      
                        g_config_json_data["PHONE_CONNECTED"] = "1"
                        
                if iRet == APP_RET_CODE_SUCESS:
                    # 设备已就绪
                    do_when_device_ready(table)
                    i_last_phone_ready = True
                else:
                    do_when_device_no_ready(table)
                    if iRet == APP_RET_CODE_PHONE_NO_CONNECT:
                        #print_my("!!!!远程手机无线调试还没连接，请配置连接信息")
                        table.signal_of_table.emit("remote_phone_no_connect")
                        if i_last_phone_ready == True:
                        	table.signal_of_table.emit("remote_phone_prepare")
                    elif iRet == APP_RET_CODE_PHONE_NO_LIGHT:
                        if i_last_phone_ready == True:
                        	table.signal_of_table.emit("screen_no_light")
                    elif iRet == APP_RET_CODE_PHONE_NO_UNLOCK:
                        if i_last_phone_ready == True:
                        	table.signal_of_table.emit("screen_lock")
                    i_last_phone_ready = False
                    continue
				# 保证微信在前台运行
                if is_weChat_running() == False:
                    print("!!!!app_check_thread, 检测到微信没有启动或没有置顶，偿试启动并置顶")
                    open_wechat_app_and_set_top() 
                    

        table.set_state(EnvStateType.Env_Start_Simulator_State, True) 
        # 动作：异常检查并处理  
        if i_check_count % 3 == 0:
            #TIME_BEGIN("app_check_thread里判断是否有异常页面")
            iRet_state = adb_get_screen_with_exception_check_and_proc(g_Event_for_app_check)
            #TIME_END("app_check_thread里判断是否有异常页面")
            if iRet_state == APP_RET_CODE_ZHU_DONG_EXIT:
                break 
            if iRet_state != APP_RET_CODE_SUCESS:
                # 更新登录状态
                if iRet_state in [APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, 
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT,
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_NEED_PHONE_LOGION,
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_WAIT_CONFIRM, 
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LODING_DATA, 
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LOGIN_LOSS,
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_HAS_LOGIN_IN_OTHER,
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SECRET_LOGIN,
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_RE_LOGIN,
                                  APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SAFE_RE_LOGIN,
                                  APP_RET_CODE_YOU_HAS_LOGOUT_WECHAT]:
                    do_when_wechat_logoff(table)
                    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
                        print_my("!!!!请您用手机扫二维码登录微信")
                    else:
                        print_my("!!!!请在手机上登录微信")
                elif iRet_state == APP_RET_CODE_NO_READY:    
                    do_when_device_no_ready(table)
                    
                if iRet_state in [APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_NEED_PHONE_LOGION, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_WAIT_CONFIRM]: 
                    # chenyj debug 通知业务线程要停止了
                    print("通知主业务线程要停止")
                    if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
                    	g_Event_for_main_work.set()
                    
                    #print_my("!!!!!此时应该要弹出雷电窗口，让用户交互了1")
                    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
                        print_my("!!!!请您用手机扫二维码登录微信")
                    else:
                    	print_my("!!!!请您用手机扫托管器中的二维码登录微信【说明:不会影响原有手机上的正常使用】")
                    do_when_wechat_logoff(table)
                    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
                        if APP_RET_CODE_NO_FOUND == windows_restore_lei_dian():
                            table.set_state(EnvStateType.Env_Start_Simulator_State, False)
                        else:
                            table.set_state(EnvStateType.Env_Start_Simulator_State, True)
                            table.set_state(EnvStateType.Env_WeiChat_State, False)
						
                    # 如果是由正常转为需要交互时，上传一次截图
                    if b_shou_lei_dian_minimize == True:
                        upload_snape()
                    b_shou_lei_dian_minimize = False 
                elif iRet_state == APP_RET_CODE_NO_READY and g_config_json_data["device_ready_befor"] == False:
                    print_my("!!!!托管器正在启动中，请稍候...\n!!!!1.如果有弹出[抱歉,模拟器遇到错误,请偿试修复]，请点击【一键修复】\n!!!!2.如果有弹出[用户权限控制]雷电修复工具，请点击【是】")
                    b_shou_lei_dian_minimize = False 
                else:
                    if iRet_state == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LODING_DATA:
                        print_my("正在载入微信数据(大约5分钟)，请稍候...")
                        app_info.WAIT_MSG_LIST_MAX_COUNT = 18
                    b_shou_lei_dian_minimize = True
                    iRet = do_exception_proc(iRet_state, g_Event_for_app_check)
                    if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                        break 
            else: 
                b_shou_lei_dian_minimize = True
                do_when_device_ready(table)
                table.set_state(EnvStateType.Env_WeiChat_State, True)
            # APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LEI_DIAN_MAIN
            if i_last_exception_state in [APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_QRCODE_LOGION, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_NEED_PHONE_LOGION, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_ENTER_WECHAT, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LODING_DATA, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_WAIT_CONFIRM] and iRet_state in [APP_RET_CODE_SUCESS, APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_SETTING_FONT]:
                # 再检查3次，如果都没有“载入数据”的异常页面，就认为真的载入成功了，否则等待
                ENSURE_LOADING_SUCESSS_CHECK_MAX_COUNT = 4
                i_ensure_loading_sucess_check_count = 0
                # chenyj debug
                print(f"chenyj debug, i_last_exception_state:{i_last_exception_state}, iRet_state:{iRet_state}")
                b_really_loadding_sucess = True 
                while i_ensure_loading_sucess_check_count < ENSURE_LOADING_SUCESSS_CHECK_MAX_COUNT:
                    i_ensure_loading_sucess_check_count += 1
                    iRet_state = adb_get_screen_with_exception_check_and_proc(g_Event_for_app_check)
                    if iRet_state == APP_RET_CODE_ZHU_DONG_EXIT:
                        break 
                    if iRet_state == APP_RET_CODE_HAS_MESSAGBOX_EXCEPTION_LODING_DATA:
                        b_really_loadding_sucess = False 
                        break 
                    # 暂停间隔时间
                    if True == g_Event_for_app_check.wait(1):
                        print_my("app_check_thread, 被要求退出2")
                        iRet_state = APP_RET_CODE_ZHU_DONG_EXIT       
                if iRet_state == APP_RET_CODE_ZHU_DONG_EXIT:
                    break
                #
                if b_really_loadding_sucess == True:    
                    print_my("载入微信数据成功") 
                    table.signal_of_table.emit("start_btn_fun")
                else: 
                    print("!!!!假载入微信数据成功，再等待")
            i_last_exception_state = iRet_state
        # 动作：雷电窗口最小化
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            if b_shou_lei_dian_minimize == True:
                # chenyj test
                #   录制视频，所以先去掉最小化
                windows_minimize_lei_dian()
                pass
        
            # 当雷电占用内存太大时，将雷电模拟器重启
            if i_check_count % 10 == 0:
                restart_lei_dian_when_memory_high(table)
        
        if i_check_count % 20 == 0:
            gc.collect()
            
        # 暂停间隔时间
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
            i_second_wait = 0.1
        else:
            i_second_wait = 1
        if True == g_Event_for_app_check.wait(i_second_wait):
            print_my("app_check_thread, 被要求退出2")
            break
            
        continue
    # chenyj debug
    print("<===程序检查线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
    
    return

def do_after_ka_zhu(event_for_main_work):
    upload_snape()
    # 先不用弹提示框，因为这是我们导致的，不应该让用户处理才对
    #table.signal_of_table.emit("app_ka_zhu")            
    # 判断到是正常页面卡住时要执行强制关闭微信的动作
    iRet = adb_get_screen_with_exception_check_and_proc(event_for_main_work)
    if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
        return iRet 
    if iRet == APP_RET_CODE_SUCESS:
        if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows: 
            adb_stop_dou_yin_app()
        else:
            print(f"因为判断到卡住了，我将重启微信")
            # 上传屏幕截图
            img_save_path = f"{SCREENSHOT_SAVE_DIR}/screenwill_restart_wechat_ka_zhu.png"
            adb_get_whole_screen(img_save_path)
            if True == event_for_main_work.wait(0.1):
                print("main_work_thread, 被要求退出4")
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return
            upload_snape(img_save_path)
            #
            iRet = restart_wechat(event_for_main_work)
            if iRet == -1:
                return iRet
            
            # restart_wechat返回后立即再次检查event状态
            # 因为restart_wechat内部的open_wechat_app_and_set_top()是耗时操作，期间可能收到退出信号
            if True == event_for_main_work.wait(0.1):
                print("do_after_ka_zhu, 被要求退出（restart_wechat执行后检测到）")
                return APP_RET_CODE_ZHU_DONG_EXIT
            
    return iRet

# 应用程序状态
class ApplicationState(Enum):
    Normal = 0        # 正常
    Running = 1       # 运行中
    UnValid = 2       # 不可用
    NoLicence = 3     # 授权到期
    UnValid_But_Setting = 4     # 不可用但可配置
    Unknow = -1       # 未知
    
def main_thread_exit_proce(table):
    table.signal_of_table.emit("close_waiting_win") 
    if table.rightPanelWin is not None:
        table.rightPanelWin._signal_self.emit("back_to_main") 
    table.set_btn_state(ApplicationState.Normal)
    """
    if len (table.username_of_can_deposit_list) == 0:
        table.setDepositObjectBtn.setEnabled(False)
    else:
        table.setDepositObjectBtn.setEnabled(True)
    """ 
    table.Timer_for_time.stop()
    if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
        set_wechat_normal()
    print_my("私域精灵停止成功")
    return
    
g_last_process_task_time =  time.time()  
# 处理任务 
def process_task(table, input_event, b_immediately = False, b_need_ensure_in_friend_list_page = False):
    global g_last_process_task_time 
    global g_config_json_data
    
    b_has_process_task = False
    # 判断时间
    time_taken = time.time() - g_last_process_task_time
    # chenyj debug
    print("process_task， TASK_TIME_INTER:{} ".format(app_info.TASK_TIME_INTER))
    if time_taken < app_info.TASK_TIME_INTER and b_immediately == False:
        return APP_RET_CODE_TIME_NOT_READY, b_has_process_task
    # 取出任务
    iRet, task_info = get_random_one_task(g_config_json_data)
    
    if iRet == APP_RET_CODE_NO_CAN_EXE_TASK:
        return iRet, b_has_process_task
    # 执行任务
    task_type = task_info["task_type"]
    task_distribe = task_info["task_distribe"]
    task_process = task_info["task_process"]
    task_data = task_info["task_data"]
    #print_my("【\n选到要执行的任务\n任务类型:{}\n任务描述:{}\n任务数据:{}\n】".format(task_type, task_distribe, task_data))
    #print_my("【\n选到要执行的任务\n任务类型:{}\n任务描述:{}\n任务时间:{}\n】".format(task_type, task_distribe,  "{} {}".format(task_data["date"], task_data["time"])))
    print_my("【\n选到要执行的任务\n任务类型:{}\n任务时间:{}\n】".format(task_type,  "{} {}".format(task_data["date"], task_data["time"])))
    
    if b_need_ensure_in_friend_list_page == True: 
        ensure_in_message_list_page(input_event)
        
    iRet, b_has_process_task = process_one_task(table, input_event, task_info, g_config_json_data)  
    save_config_data(g_config_json_data, g_config_path)    
    #if iRet == APP_RET_CODE_SUCESS and b_has_process_task == True:
    #    save_config_data(g_config_json_data, g_config_path)
        
    g_last_process_task_time =  time.time()
    
    return iRet, b_has_process_task
   
g_last_process_autopass_time =  time.time()  
# 处理自动通过好友任务 
def process_autopass(input_event, remark_prefix):
    global g_last_process_autopass_time 
    global g_config_json_data
    
    i_sucess_pass_count = 0
    
    time_taken = time.time() - g_last_process_autopass_time
    if time_taken < g_config_json_data["AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT"]:
        return APP_RET_CODE_TIME_NOT_READY, i_sucess_pass_count
    
    # chenyj test 
    #iRet = APP_RET_CODE_SUCESS
    #bHasNewPass = True 
    iRet, bHasNewPass = check_has_new_pass(input_event)
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, i_sucess_pass_count
    if bHasNewPass == True:
        print_my("有新的好友请求,准备开始自动通过好友处理")
        iRet, i_sucess_pass_count = auto_pass_friend_with_check(input_event, remark_prefix)  
        #save_config_data(g_config_json_data, g_config_path)    
    else: 
        print("没有新的好友请求")
    g_last_process_autopass_time = time.time()
        
    return iRet, i_sucess_pass_count

g_last_process_get_new_friend_time =  time.time()  
# 处理自动通过好友任务 
def process_get_new_friend(input_event, b_immediately = False):
    global g_last_process_get_new_friend_time 
    new_username_list = []
    
    time_taken = time.time() - g_last_process_get_new_friend_time

    if time_taken < int(g_config_json_data["GET_NEW_FRIEND_TIME_INTER"]) and b_immediately == False:
        return APP_RET_CODE_TIME_NOT_READY, new_username_list

    print_my("======>开始检查新好友信息")
    iRet, new_username_list = get_username_list_of_new_friend(input_event)
    print_my("<======检查新好友信息结束")
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, new_username_list
    g_last_process_get_new_friend_time = time.time()
        
    return iRet, new_username_list

def main_work_thread(table, bSyncFriend, bSyncTagGroup):
    global g_config_json_data
    global g_new_msg_count
    global g_str_mac

    # chenyj debug
    print("===>主业务线程名称:{} 参数：{} 开始时间:{} 同步通讯录模式:{} 同步标签组模式:{}".format(threading.current_thread().name, table, time.strftime("%Y-%m-%d %H:%M:%S"), bSyncFriend, bSyncTagGroup))
    
    i_main_loop_count = 0
    b_has_notice_start = False
    i_restart_wechat_count_after_error = 0
    while i_main_loop_count <= WAIT_MAIN_LOOP_MAX_COUNT:
        i_main_loop_count += 1
        
        while True:
            if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
                b_ready = adb_is_lei_dian_device_ready(table)
                if b_ready == True:
                    print_my("托管设备准备好了")
                    g_config_json_data["device_ready_befor"] = True
                    save_config_data(g_config_json_data, g_config_path)  
                    break
                else:
                    print_my("!!!!托管器正在启动中，请稍候...\n!!!!1.如果有弹出[抱歉,模拟器遇到错误,请偿试修复]，请点击【一键修复】\n!!!!2.如果有弹出[用户权限控制]雷电修复工具，请点击【是】")
                    #print_my("托管设备还没准备好，请稍等...")
				
                if True == g_Event_for_main_work.wait(1):
                    print("main_work_thread, 被要求退出")
                    main_thread_exit_proce(table)
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
            elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
                iRet = is_windows_wechat_ready(table)
                if iRet == APP_RET_CODE_SUCESS:
                    print_my("本地的微信应用程序已经准备好")
                    g_config_json_data["device_ready_befor"] = True
                    save_config_data(g_config_json_data, g_config_path)  
                    break
                elif iRet == APP_RET_CODE_WECHAT_NO_INSTALL:
                    print_my("!!!!本地的微信应用程序还未安装，请先安装程序")
                    main_thread_exit_proce(table)
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
            else:
                iRet = adb_is_remote_phone_ready(table)
                if iRet == APP_RET_CODE_SUCESS:
                    print_my("远程手机无线调试已经准备好了")
                    g_config_json_data["device_ready_befor"] = True
                    save_config_data(g_config_json_data, g_config_path)  
                    break
                else:
                    i_last_phone_ready = False
                    #print_my("!!!!手机还没亮锁处于锁定状态")
                    #table.signal_of_table.emit("remote_phone_prepare")
                    main_thread_exit_proce(table)
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
 
        if is_weChat_running() == False:
            print_my("!!!!微信没有启动，偿试启动")
            open_wechat_app_and_set_top() 
            
            # 启动后等待启动成功
            #TRY_COUNT_MAX = 5
            #TRY_COUNT_MAX = 30
            i_try_count = 0
            while i_try_count < WAIT_WECHAT_TRY_COUNT_MAX:
                i_try_count += 1
                if True == g_Event_for_main_work.wait(1):
                    print("main_work_thread, 被要求退出2")
                    main_thread_exit_proce(table)
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
                if is_weChat_running() == True and adb_get_phone_size() == True:
                    print_my("确定微信已经准备好,但我再等2秒")
                    # 再等10秒，让设备准备好
                    if True == g_Event_for_main_work.wait(2):
                        print("main_work_thread, 被要求退出3")
                        main_thread_exit_proce(table)
                        # chenyj debug
                        print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                        return  
                    if is_weChat_running() == True and adb_get_phone_size() == True:
                        break
                continue   
                 
            if is_weChat_running() == False:
                print("偿试检查微信窗口是否准备好，试了{}次，还是失败了，此时【失败后重启微信的次数】是{}次".format(i_try_count, i_restart_wechat_count_after_error))
                if i_restart_wechat_count_after_error >= 1:
                    print_my("!!!!!!奇怪微信一直无法启动，请求客服支援") 
                    table.signal_of_table.emit("app_not_run")
                    main_thread_exit_proce(table)
                    #upload_snape()
					
                    table.set_state(EnvStateType.Env_Start_Simulator_State, False)
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
                else:
                    i_restart_wechat_count_after_error += 1
                    print(f"准备第{i_restart_wechat_count_after_error}次重新启动微信")
					# 上传屏幕截图
                    img_save_path = f"{SCREENSHOT_SAVE_DIR}/screen_will_restart_wechat_{i_restart_wechat_count_after_error}.png"
                    adb_get_whole_screen(img_save_path)
                    if True == g_Event_for_main_work.wait(0.1):
                        print("main_work_thread, 被要求退出4")
                        main_thread_exit_proce(table)
                        # chenyj debug
                        print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                        return
                    upload_snape(img_save_path)
					#
                    iRet = restart_wechat(g_Event_for_main_work)
                    if iRet == -1:
                        print("main_work_thread, 被要求退出5")
                        main_thread_exit_proce(table)
                        # chenyj debug
                        print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                        return
                    
                    # restart_wechat返回后立即再次检查event状态
                    # 因为restart_wechat内部的open_wechat_app_and_set_top()是耗时操作，期间可能收到退出信号
                    if True == g_Event_for_main_work.wait(0.1):
                        print("main_work_thread, 被要求退出（restart_wechat执行后检测到）")
                        main_thread_exit_proce(table)
                        print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                        return
                    
                    continue
                
        table.set_state(EnvStateType.Env_Start_Simulator_State, True)
        
        # 检查多遍确保页面是正常的
        """
        #TRY_COUNT_MAX = 3
        i_try_count = 0
        while i_try_count < WAIT_WECHAT_TRY_COUNT_MAX:
            i_try_count += 1
            iRet = adb_get_screen_with_exception_check_and_proc(g_Event_for_main_work)
            if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                print("main_work_thread, 被要求退出4")
                main_thread_exit_proce(table)
                print_my("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return 
            if iRet != APP_RET_CODE_SUCESS:
                print_my("!!!!main_work_thread, 遇到需要用户交互的界面[{}]，继续等待".format(iRet))
                if True == g_Event_for_main_work.wait(2):
                    print("main_work_thread, 被要求退出5")
                    main_thread_exit_proce(table)
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
                continue  
            break
        if i_try_count >= WAIT_WECHAT_TRY_COUNT_MAX:
            print_my("!!!!main_work_thread, 遇到需要用户交互的界面[{}]，线程先退出".format(iRet))
            main_thread_exit_proce(table)
            table.set_state(EnvStateType.Env_WeiChat_State, False)
            print_my("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return 
        """
        # 检查多遍确保页面是在消息列表页面
        i_try_count = 0
        i_in_msg_list_count = 0
        assert app_info.WAIT_MSG_LIST_MAX_COUNT > NEED_MIN_IN_MSG_LIST_COUNT and app_info.WAIT_MSG_LIST_MAX_COUNT -NEED_MIN_IN_MSG_LIST_COUNT > 1
        while i_try_count < app_info.WAIT_MSG_LIST_MAX_COUNT:
            i_try_count += 1
            iRet, page_type_return, _ = get_page_type_by_tesseract(g_Event_for_main_work)
            if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                print("main_work_thread, 被要求退出6")
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return 

            if page_type_return not in [PageType.Message_List, PageType.Chat]:
                # chenyj debug
                print("!!!!main_work_thread, [{}]th当前不是[消息列表页或聊天贾]，请稍等[{}]".format(i_try_count, page_type_return))
                print_my("等待中...")
                if True == g_Event_for_main_work.wait(2):
                    print("main_work_thread, 被要求退出7")
                    main_thread_exit_proce(table)
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
                # 回到消息列表页的动作
                ensure_in_message_list_page(g_Event_for_main_work) 
                
                # 等待到一半时执行回到消息列表页的动作
                """
                if i_try_count == int(app_info.WAIT_MSG_LIST_MAX_COUNT / 4):
                    #_ = adb_click_back_of_chat() 
                    ensure_in_message_list_page(g_Event_for_main_work)
                """
                continue  
            i_in_msg_list_count += 1
            if i_in_msg_list_count >= NEED_MIN_IN_MSG_LIST_COUNT:
                break
        if i_try_count >= app_info.WAIT_MSG_LIST_MAX_COUNT:
            # 按卡住的情况处理
            iRet = do_after_ka_zhu(g_Event_for_main_work)
            if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                print("main_work_thread, 被要求退出8")
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return 
            continue 
            # 直接退出
            """    
            print_my("!!!!main_work_thread, 当前不是[消息列表页]，线程先退出")
            main_thread_exit_proce(table)
            table.set_state(EnvStateType.Env_WeiChat_State, False)
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return 
            """
        # chenyj debug
        print("当前是在[消息列表页]")
        app_info.WAIT_MSG_LIST_MAX_COUNT = 6
        
        if True == g_Event_for_main_work.wait(0.1):
            print("main_work_thread, 被要求退出9")
            main_thread_exit_proce(table)
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return

        i_restart_wechat_count_after_error = 0
        # 获得焦点
        get_focus_for_windows()
        #
        # 执行微信相关设置
        #if g_config_json_data["HAS_SETTING_SUCESS"] == False:
        # chenyj test 去掉微信初始化设置
        if False:
            print_my("开始执行微信初始化配置")
            iRet, username_of_me = do_weichat_setting_with_check(g_Event_for_main_work)
            if iRet != APP_RET_CODE_SUCESS:
                print_my("!!!!main_work_thread, 微信相关设置失败[{}]".format(iRet))
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return
            print_my("微信初始化配置成功")
            get_focus_for_windows()
            g_config_json_data["HAS_SETTING_SUCESS"] = True
            #save_config_data(g_config_json_data, g_config_path)
            g_config_json_data["CURRENT_LOGON_USERNAME"] = username_of_me
            g_config_json_data["CURRENT_LOGON_USERNAME_ONLINE"] = "1"
            save_config_data(g_config_json_data, g_config_path)
            table.signal_of_table.emit("update_logon_wechat_state") 
            
		#
        # 同步好友
        if bSyncFriend == True:
            friend_list_all = []
            for iRet, friend_list in sync_frient_with_check(g_Event_for_main_work):
                if iRet == APP_RET_CODE_HAS_FINISH:
                    print_my("^-^同步通讯录成功,共有{}个好友".format(len(friend_list_all)))
                    break
                elif iRet not in [APP_RET_CODE_SUCESS]:
                    print_my("!!!同步通讯录失败{}【请再试一次】".format(iRet))
                    break
                else:
                    print_my("^-^同步通讯录进行中(已同步{}个)...".format(len(friend_list_all)))
                    for friend_name in friend_list:
                        # 排重 
                        bExist = False 
                        for friend_info_ in friend_list_all:
                            if friend_name == friend_info_["friend_name"]:
                                bExist = True
                                break
                        if bExist == True: 
                            continue 
                            
                        friend_info = {}
                        friend_info["friend_name"] = friend_name
                        friend_info["add_date"] = ""
                        friend_info["friend_remark"] = ""
                        friend_list_all.append(friend_info)
                    g_config_json_data["FRIEND_INFO_LIST"] = friend_list_all
                    save_config_data(g_config_json_data, g_config_path) 
                    # 刷新列表
                    table.signal_of_table.emit("reload_friend_list_view") 
                    continue
            # 更新原有的变量
            g_config_json_data["username_of_can_deposit_list"] =  [friend_info["friend_name"] for friend_info in g_config_json_data["FRIEND_INFO_LIST"]]
            save_config_data(g_config_json_data, g_config_path)  
            if "username_of_can_deposit_list" in g_config_json_data:
                table.username_of_can_deposit_list = g_config_json_data["username_of_can_deposit_list"]
            """
            iRet, friend_list = sync_frient_with_check(g_Event_for_main_work)
            if iRet not in [APP_RET_CODE_SUCESS]:
                print_my("!!!同步好友失败{}".format(iRet))
            else:
                print_my("^-^同步好友成功")
                friend_info_list = []
                for friend_name in friend_list:
                    friend_info = {}
                    friend_info["friend_name"] = friend_name
                    friend_info["friend_remark"] = ""
                    friend_info_list.append(friend_info)
                g_config_json_data["FRIEND_INFO_LIST"] = friend_info_list
                save_config_data(g_config_json_data, g_config_path) 
                # 更新原有的变量
                g_config_json_data["username_of_can_deposit_list"] =  [friend_info["friend_name"] for friend_info in g_config_json_data["FRIEND_INFO_LIST"]]
                save_config_data(g_config_json_data, g_config_path)  
                if "username_of_can_deposit_list" in g_config_json_data:
                    table.username_of_can_deposit_list = g_config_json_data["username_of_can_deposit_list"]
            """
            table.signal_of_table.emit("sync_friend_finish") 
            main_thread_exit_proce(table)
            
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
		#
        # 同步微信标签组
        if bSyncTagGroup == True:
            usergroup_info_list_all = []
            for iRet, usergroup_info in sync_tag_group_with_check(g_Event_for_main_work):
                if iRet == APP_RET_CODE_HAS_FINISH:
                    print_my("^-^同步微信标签组成功,共有{}个标签组".format(len(usergroup_info_list_all)))
                    break
                elif iRet not in [APP_RET_CODE_SUCESS]:
                    print_my("!!!同步微信标签组失败{}【请再试一次】".format(iRet))
                    break
                else:
                    usergroup_info_list_all.append(usergroup_info)
                    print_my("^-^同步微信标签组进行中(已同步{}个标签组)...".format(len(usergroup_info_list_all)))
                    g_config_json_data["USERGROUP_INFO_LIST"].append(usergroup_info)
                    save_config_data(g_config_json_data, g_config_path) 
                    # 刷新列表
                    table.signal_of_table.emit("reload_usergroup_list_view") 
                    continue
            #
            ensure_in_message_list_page(g_Event_for_main_work)
            table.signal_of_table.emit("sync_usergroup_finish") 
            main_thread_exit_proce(table)
            
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
        
        if auto_opt_init() == True: 
            print_my("自动化操作初始化成功")
        else:
            print_my("!!!!自动化操作初始化失败")
            main_thread_exit_proce(table)
            table.signal_of_table.emit("auto_init_error") 
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return 
        table.set_state(EnvStateType.Env_WeiChat_State, True)

        if True == g_Event_for_main_work.wait(0.1):
            print("main_work_thread, 被要求退出10")
            main_thread_exit_proce(table)
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
            
        loop_count = 0
        i_return = 0
        
        # 
        # 确保消息列表中第2个好友没有置顶
        if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
            iRet = ensure_msg_no_top(g_Event_for_main_work)
            if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                print("main_work_thread, 被要求退出11")
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return 
            if iRet != APP_RET_CODE_SUCESS:
                continue
        
                
        # 获得聊天对象列表
        iRet, username_list_of_first_page = get_username_list_of_first_page(g_Event_for_main_work, False)
        # chenyj test 托管对象改版
        #table.username_of_can_deposit_list.extend(username_list_of_first_page)
        #table.username_of_can_deposit_list = list(set(table.username_of_can_deposit_list))
        #if RET_SUCESS != iRet or len(table.username_of_can_deposit_list) == 0:
        if RET_SUCESS != iRet:
            print("iRet:{}, len(table.username_of_can_deposit_list):{}".format(iRet, len(table.username_of_can_deposit_list)))
            table.set_state(EnvStateType.Env_Set_Tuo_State, False)
            main_thread_exit_proce(table)
            upload_snape()
            table.signal_of_table.emit("get_username_list_of_first_page_fail")
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
        # 添加“文件传输助手”对象
        #if USERNAME_FOR_NOTICE not in table.username_of_can_deposit_list:
        if USERNAME_FOR_NOTICE not in username_list_of_first_page:
            iRet = add_deposit_to_frient_list_and_set_top_with_check(g_Event_for_main_work, USERNAME_FOR_NOTICE, False)
            if iRet == -1:
                print("main_work_thread, 被要求退出12")
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return
            if iRet == 0:
                table.username_of_can_deposit_list.append(USERNAME_FOR_NOTICE)
        # chenyj test 托管对象改版
        #g_config_json_data["username_of_can_deposit_list"] = table.username_of_can_deposit_list
        #save_config_data(g_config_json_data, g_config_path)  
        
        if True == g_Event_for_main_work.wait(0.1):
            print_my("main_work_thread, 被要求退出13")
            main_thread_exit_proce(table)
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
            
        # 获得托管对象
        #username_list = ["惠安家人", "任小玲", "闲置优惠券专用群", "小朗自学公开课637群", "慕阳晨飞男足俱乐部", "约饭群"]
        #username_list = ["任小玲"]
        """
        if False == set(table.username_of_deposit_list).issubset(set(table.username_of_can_deposit_list)):
            table.set_state(EnvStateType.Env_Set_Tuo_State, False)
            print_my("!!!!之前设置托管好友对象[{}]没有都在当前列表里".format(table.username_of_deposit_list))
            main_thread_exit_proce(table)
            table.signal_of_table.emit("need_set_deposit")
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
        """
        """
        if len(table.username_of_deposit_list) == 0:
            table.set_state(EnvStateType.Env_Set_Tuo_State, False)
            print_my("!!!!还没有设置托管好友对象")
            main_thread_exit_proce(table)
            table.signal_of_table.emit("need_set_deposit")
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
        """
		# 更新原有的变量（客服机器人相关）
        # 放在这里是为了使客户组调整了成员后重启启动能马上生效
        info_of_deposit_list = []
        autoreply_info_list = g_config_json_data["AUTOREPLY_INFO_LIST"]
        llm_name = ""
        if len(autoreply_info_list) != 0:
            response_usergroupname = autoreply_info_list[0]["response_usergroupname"]
            for usergroup_info in g_config_json_data["USERGROUP_INFO_LIST"]:
                if usergroup_info["usergroup_name"] == response_usergroupname:
                    for username in usergroup_info["usergroup_member"]:
                        info_of_deposit = {}
                        info_of_deposit["username"] = username
                        info_of_deposit["b_hase_new_msg"] = False
                        info_of_deposit_list.append(info_of_deposit)
            g_config_json_data["HUA_SU_FILES"] = autoreply_info_list[0]["hua_su_file_paths"]
            g_config_json_data["info_of_deposit_list"] = info_of_deposit_list
            if "info_of_deposit_list" in g_config_json_data:
                table.username_of_deposit_list = [obj["username"] for obj in g_config_json_data["info_of_deposit_list"]]
            g_config_json_data["sel_agent_list"] = ["闲聊专家自定义本地话术库"]
            if "llm_name" in autoreply_info_list[0]:
                llm_name = autoreply_info_list[0]["llm_name"]
            else:
                llm_name = LLM_MODEL_TYPE_NAME_DICT[LLM_MODEL_TYPE.GLM]
            table.sel_agent_list = g_config_json_data["sel_agent_list"]
            table.hua_su_file_paths = g_config_json_data["HUA_SU_FILES"]
            init_knowledage_str(table.hua_su_file_paths)
            save_config_data(g_config_json_data, g_config_path) 
    
        print_my("设置的托管好友对象列表是:{}".format(table.username_of_deposit_list))
        username_list = table.username_of_deposit_list
        table.set_state(EnvStateType.Env_Set_Tuo_State, True)
        
        if True == g_Event_for_main_work.wait(0.1):
            print("main_work_thread, 被要求退出14")
            main_thread_exit_proce(table)
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
        
        # 设置本地方Agent
        if True == llm_name.startswith(COZE_FRON_STR):
            agent_name = "闲聊专家自定义本地话术库"
            print_my("设置的Agent是:【{}】".format(llm_name))
        else:
            if len(table.sel_agent_list) == 0 or \
				(table.sel_agent_list[0] == "电商客服自定义本地话术库" and len(table.hua_su_file_paths) == 0) \
			or (table.sel_agent_list[0] == "闲聊专家自定义本地话术库" and len(table.hua_su_file_paths) == 0) \
			or (table.sel_agent_list[0] == "销冠自定义本地话术库" and len(table.hua_su_file_paths) == 0):
                table.set_state(EnvStateType.Env_Set_Hua_Su_State, False)
                print_my("!!!!还没有设置Aent")
                main_thread_exit_proce(table)
                table.signal_of_table.emit("need_set_agent")
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                return
            print_my("设置的Agent是:【{}】".format(table.sel_agent_list[0]))    
            if table.sel_agent_list[0] in ["电商客服自定义本地话术库", "闲聊专家自定义本地话术库", "销冠自定义本地话术库"]:
                print_my("设置的话术库列表是:{}".format(table.hua_su_file_paths))
            agent_name = table.sel_agent_list[0]
            hua_su_file_paths = table.hua_su_file_paths
            table.set_state(EnvStateType.Env_Set_Hua_Su_State, True)
        
        if True == g_Event_for_main_work.wait(0.1):
            print("main_work_thread, 被要求退出15")
            main_thread_exit_proce(table)
            # chenyj debug
            print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
            return
        
        # 添加“文件传输助手”到托管对象中
        #if USERNAME_FOR_NOTICE not in username_list and USERNAME_FOR_NOTICE in table.username_of_can_deposit_list:
        if USERNAME_FOR_NOTICE not in username_list:
            username_list.append(USERNAME_FOR_NOTICE)
        
        # 获得托管对象的新消息区域
        while True:
            i_return, username_failed = get_monitor_rect_of_new_msg(g_Event_for_main_work, username_list, False, True)
            if i_return == -1:
                print("main_work_thread, 被要求退出16")
                main_thread_exit_proce(table)
                # chenyj debug
                print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M%S")))
                return
            if i_return != 0:
                # 如果没有找到“文件传输助手”的新消息区域，就把它从托管对象中去掉
                if APP_RET_CODE_NO_FOUND == i_return and username_failed == USERNAME_FOR_NOTICE:
                    print("找不到【文件传输助手】的新消息区域，把它从托管对象中去掉")
                    username_list = [username for username in username_list if username != USERNAME_FOR_NOTICE]
                    continue
                else:
                    table.set_state(EnvStateType.Env_Sucess, False)
                    print_my("!!!!!!【{}】用户的新消息区域无法获得(err_code:{})".format(username_failed, i_return))
                    main_thread_exit_proce(table)
                    upload_snape()
                    if i_return == APP_RET_CODE_NO_FOUND:
                        table.signal_of_table.emit("no_found_monitor_rect_{}".format(username_failed))
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M%S")))
                    return
            break
            
         
        table.set_state(EnvStateType.Env_Sucess, True)  
            
        # 上传开始托管的图片
        upload_snape()

        # 开始托管
        msg_log_txt = ""
        new_msg_username_for_unexpect_chat_page = ""
        # chenyj test 
        for obj in g_config_json_data["info_of_deposit_list"]:
            if obj["b_hase_new_msg"] == True:
                new_msg_username_for_unexpect_chat_page = obj["username"]
                print("发现上一次【{}】有新消息没有读取成功，补充读取".format(new_msg_username_for_unexpect_chat_page))
     
        print_my("====成功托管=====")
        # 发送业务通知
        if i_main_loop_count == 1:
            #send_bussiness(g_Event_for_main_work, "开始托管。Agent是:[{}] 托管对象是:{}".format(table.sel_agent_list[0], table.username_of_deposit_list))
            deposit_count = len(table.username_of_deposit_list) - 1 if USERNAME_FOR_NOTICE in table.username_of_deposit_list else len(table.username_of_deposit_list)
            if g_deivce_MODEL in [DEVICE_MODEL_TYPE.Local_Emulator, DEVICE_MODEL_TYPE.Windows]:
            	send_bussiness(g_Event_for_main_work, "开始运行。客服机器人启动，负责好友共{}个".format(deposit_count))
            b_has_notice_start = True
        
        b_has_process_autopass_rectent = False
        while loop_count < LOOP_COUNT_MAX and i_return == 0:
            loop_count += 1
            # chenyj debug
            print("===========第{}轮==========".format(loop_count))
            print_my("运行中...")
            b_need_ensure_in_friend_list_page = True
            # 判断现在是不是在消息列表页面
            if loop_count % 5 == 0:
                CHECK_IN_MESSAGE_LIST_COUNT = 3
                i_count_check = 0
                page_type_return = PageType.Unknow
                while i_count_check < CHECK_IN_MESSAGE_LIST_COUNT:
                    i_count_check += 1
                    iRet = ensure_in_message_list_page(g_Event_for_main_work)
                    if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                        print("main_work_thread, 被要求退出17")
                        main_thread_exit_proce(table)
                        # chenyj debug
                        print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                        return 
                    if iRet == APP_RET_CODE_HAS_IN_EXPECT_PAGE:
                        page_type_return = PageType.Message_List
                        b_need_ensure_in_friend_list_page = False
                        break
                    """
                    iRet, page_type_return, _ = get_page_type_by_tesseract(g_Event_for_main_work)
                    if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                        print("main_work_thread, 被要求退出18")
                        main_thread_exit_proce(table)
                        # chenyj debug
                        print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                        return 
                    if page_type_return == PageType.Message_List:
                        break
                    """
                    if True == g_Event_for_main_work.wait(1):
                        print("main_work_thread, 被要求退出19")
                        i_return = APP_RET_CODE_ZHU_DONG_EXIT
                        break
                    continue 
                if i_return == APP_RET_CODE_ZHU_DONG_EXIT:
                    break
                if page_type_return != PageType.Message_List:
                    i_return = APP_RET_CODE_APP_KA_ZHU
                    break 
            # 处理任务 
            iRet, b_has_process_task = process_task(table, g_Event_for_main_work, False, b_need_ensure_in_friend_list_page)
            if iRet == -1:
                i_return = APP_RET_CODE_ZHU_DONG_EXIT
                break
            if iRet == APP_RET_CODE_SUCESS and b_has_process_task == True:
                # 更新任务列表 
                table.signal_of_table.emit("reload_task_list_view") 
                # 每个循环随机等待一个间隔时间
                #random_float  = uniform(0.2, 1)
                random_float  = uniform(1, 2)
                print("随机停{:.2f}秒".format(random_float))
                if True == g_Event_for_main_work.wait(random_float):
                    print("main_work_thread, 被要求退出20")
                    i_return = APP_RET_CODE_ZHU_DONG_EXIT
                    break
                continue 
            
            # 处理通过好友请求
            remark_prefix = ""
            autopass_info_list = g_config_json_data["AUTOPASS_INFO_LIST"]
            if len(autopass_info_list) > 0:
                autopass_info = autopass_info_list[0]
                remark_prefix = autopass_info["remark_prefix"]
                iRet, i_sucess_pass_count = process_autopass(g_Event_for_main_work, remark_prefix)
                if iRet == -1:
                    i_return = APP_RET_CODE_ZHU_DONG_EXIT
                    break
                if iRet == APP_RET_CODE_SUCESS and i_sucess_pass_count > 0:
                    b_has_process_autopass_rectent = True
                    # 每个循环随机等待一个间隔时间
                    #random_float  = uniform(0.2, 1)
                    random_float  = uniform(1, 2)
                    print("随机停{:.2f}秒".format(random_float))
                    if True == g_Event_for_main_work.wait(random_float):
                        print("main_work_thread, 被要求退出21")
                        i_return = APP_RET_CODE_ZHU_DONG_EXIT
                        break
                    continue 
                
            # 处理获取新好友
            b_immediatel_process_get_new = False
            if b_has_process_autopass_rectent == True:
                b_has_process_autopass_rectent = False
                b_immediatel_process_get_new = True
            iRet, new_username_list = process_get_new_friend(g_Event_for_main_work, b_immediatel_process_get_new)
            if iRet == -1:
                i_return = APP_RET_CODE_ZHU_DONG_EXIT
                break
            if iRet == APP_RET_CODE_SUCESS and len(new_username_list) > 0:
                friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]
                friend_name_list = [friend_info["friend_name"] for friend_info in friend_info_list]
                b_has_new_friend = False
                for new_username in new_username_list:
                    if new_username not in friend_name_list:
                        print_my("发现新好友:{}，加入到新用户旅程中".format(new_username))
      
                        friend_info = {}
                        friend_info["friend_name"] = new_username
                        current_datetime = datetime.now()
                        date_str = current_datetime.strftime("%Y-%m-%d")
                        friend_info["add_date"] = date_str
                        friend_info["friend_remark"] = ""
                        friend_info_list.append(friend_info)
                        b_has_new_friend = True 
                    else:
                        # 给好友添加时间
                        for friend_info in friend_info_list:
                            if friend_info["friend_name"] == new_username and ("add_date" not in friend_info or len(friend_info["add_date"]) == 0):
                                friend_info["add_date"] = date_str
                                break
                if  b_has_new_friend == True:
                	g_config_json_data["FRIEND_INFO_LIST"] = friend_info_list
                	save_config_data(g_config_json_data, g_config_path)
                 
                table.update_lv_cheng_group_data()
                table.signal_of_table.emit("reload_usergroup_list_view") 
						 
                # 每个循环随机等待一个间隔时间
                #random_float  = uniform(0.2, 1)
                random_float  = uniform(1, 2)
                print("随机停{:.2f}秒".format(random_float))
                if True == g_Event_for_main_work.wait(random_float):
                    print("main_work_thread, 被要求退出21")
                    i_return = APP_RET_CODE_ZHU_DONG_EXIT
                    break
                continue 
              
            # 为解决聊天对象位置发生变化，在这里判断，如果有变化，就重新获取一次
            TIME_BEGIN("判断消息列表是否变化")
            """
            img_befor_path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list_befor" + ".png"
            img_after_path = SCREENSHOT_SAVE_DIR + "/" + "screen_of_friend_chat_list" + ".png"
            shutil.copy(img_after_path, img_befor_path)
            get_screen_of_friend_chat_list(img_after_path)
            _, bChange = has_img_change(img_befor_path, img_after_path, 0.992)
            """
            img_befor_path = SCREENSHOT_SAVE_DIR + "/" + "first_item_of_friend_chat_list_befor" + ".png"
            img_after_path = SCREENSHOT_SAVE_DIR + "/" + "first_item_of_friend_chat_list" + ".png"
            img_middle_path = SCREENSHOT_SAVE_DIR + "/" + "first_item_of_friend_chat_list_middle" + ".png"
            #md5_of_img_befor_path = ""
            #md5_of_img_after_path = ""
            #md5_of_img_middle_path = ""
            bChange = False
            if True == os.path.exists(img_after_path):
                shutil.copy(img_after_path, img_befor_path)
                #md5_of_img_befor_path = md5_of_img_after_path
                iRet = get_screen_of_first_item_of_friend_chat_list(img_after_path)
                #md5_of_img_after_path = get_md5_of_image(img_after_path)
                if iRet == APP_RET_CODE_SUCESS:
                    _, bChange = has_img_change(img_befor_path, img_after_path, FIRST_ITEM_CHANGE_RATIO)
                    #if md5_of_img_befor_path != md5_of_img_after_path:
                    #    bChange = True 
                else:
                    bChange = False
            else:
                _ = get_screen_of_first_item_of_friend_chat_list(img_after_path)
                #md5_of_img_after_path = get_md5_of_image(img_after_path)
                bChange = True
            if len(new_msg_username_for_unexpect_chat_page) > 0:
                print("有new_msg_username_for_unexpect_chat_page，所以我认为聊天列表页面发生变化")
                bChange = True 
            TIME_END("判断消息列表是否变化")
            
            #if bChange == True and loop_count > 1:
            if bChange == True or loop_count == 1:
                TIME_BEGIN("重新定位消息列表")
                # chenyj debug
                print("!!!!!聊天列表页面发生变化,重新定位")
                # 获得聊天对象列表
                iRet, username_of_can_deposit_list = get_username_list_of_first_page(g_Event_for_main_work, False)
                # chenyj test 托管对象改版
                #table.username_of_can_deposit_list.extend(username_of_can_deposit_list)
                #table.username_of_can_deposit_list = list(set(table.username_of_can_deposit_list))
                if RET_SUCESS != iRet or len(table.username_of_can_deposit_list) == 0:
                    """
                    table.set_state(EnvStateType.Env_Set_Tuo_State, False)
                    main_thread_exit_proce(table)
                    upload_snape()
                    table.signal_of_table.emit("get_username_list_of_first_page_fail")
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
                    """
                    break
                # chenyj test 托管对象改版
                #g_config_json_data["username_of_can_deposit_list"] = table.username_of_can_deposit_list
                #save_config_data(g_config_json_data, g_config_path)  
                 
                # 获得托管对象的新消息区域
                i_return, username_failed = get_monitor_rect_of_new_msg(g_Event_for_main_work, username_list, False, False)
                if i_return != APP_RET_CODE_SUCESS:
                    """
                    table.set_state(EnvStateType.Env_Sucess, False)
                    print_my("!!!!!!{}用户的新消息区域无法获得(err_code:{})".format(username_failed, i_return))
                    main_thread_exit_proce(table)
                    upload_snape()
                    if i_return == APP_RET_CODE_NO_FOUND:
                        table.signal_of_table.emit("no_found_monitor_rect_{}".format(username_failed))
                    # chenyj debug
                    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
                    return
                    """
                    break
                TIME_END("重新定位消息列表")
            
            # 获得锚定成功的好友 
            username_list_mao_ding = get_mao_ding_username_list()
            random.shuffle(username_list_mao_ding)
            print("锚定的好友有{}个:{}".format(len(username_list_mao_ding), username_list_mao_ding))
            i_return = 0
            # 动作：发现新消息就去读取
            #for i, username in enumerate(username_list):
            for i, username in enumerate(username_list_mao_ding):
                # 排除掉"文件传输助手"
                if username == USERNAME_FOR_NOTICE:
                    continue 

                # 确保图片没有变化，有的话可能导致新消息判断错误，所以为了保险起见，就先退出 
                bChange = False
                iRet = get_screen_of_first_item_of_friend_chat_list(img_middle_path)
                #md5_of_img_middle_path = get_md5_of_image(img_middle_path)
                if iRet == APP_RET_CODE_SUCESS:
                    _, bChange = has_img_change(img_after_path, img_middle_path, FIRST_ITEM_CHANGE_RATIO, False)
                    #if md5_of_img_middle_path != md5_of_img_after_path:
                    #    bChange = True
                else:
                    bChange = False
                if bChange == True:
                    print("中途发现图片变化，提前退出username_list循环")
                    break 
                    
                start_time_of_msg = time.time()
                # 上一次因为进入非期待的聊天页面，这次直接认为有新消息
                if username == new_msg_username_for_unexpect_chat_page:
                    new_msg_username_for_unexpect_chat_page = ""
                    i_return = APP_RET_CODE_SUCESS
                    bHas = True
                else:
                    i_return, bHas = check_has_new_msg(g_Event_for_main_work, username)
                if 0 != i_return:
                    break
                # chenyj test 
                #if True:
                if bHas == True:
                    print_my("!!!!收到【{}】的新消息".format(username))
                    msg_log_txt += "用户【{}】有新消息 {}\n".format(username, loop_count)
                    
                    # 更新配置文件中的消息标志位
                    for obj in g_config_json_data["info_of_deposit_list"]:
                        if obj["username"] == username:
                            obj["b_hase_new_msg"] = True
                            break 
                    save_config_data(g_config_json_data, g_config_path) 
                    
                    i_return, message_all_list_now, message_all_list_new = get_weChat_chat_content(g_Event_for_main_work, username, False)
                    
                    # 进入非期待的聊天页面
                    if APP_RET_CODE_UNEXPECT_CHAT_PAGE == i_return:
                        new_msg_username_for_unexpect_chat_page = username
                        adb_click_back_of_chat_with_check(g_Event_for_main_work)
                        break 
                    if APP_RET_CODE_SUCESS != i_return:
                        break
                    # 动作：发送消息
                    i_return_of_send, msg_send = send_webChat_message_with_agent(g_Event_for_main_work, username, agent_name, llm_name, g_config_json_data["COZE_AGENT_INFO_LIST"], message_all_list_now, message_all_list_new, g_str_mac, start_time_of_msg, False)
                    if i_return_of_send not in [RET_SUCESS, APP_RET_CODE_UNVALID_PARAM, APP_RET_CODE_UN_SAFE_QUESTION, APP_RET_CODE_NO_ANSWER_IN_KNOWLEDAGE]:
                        break
                        
                    # 更新配置文件中的消息标志位
                    for obj in g_config_json_data["info_of_deposit_list"]:
                        if obj["username"] == username:
                            obj["b_hase_new_msg"] = False
                            break 
                    save_config_data(g_config_json_data, g_config_path) 
                        
                    # 通知界面更新计数
                    g_new_msg_count += 1
                    update_new_msg_count(g_new_msg_count)
                    
                    # 动作：返回键
                    if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
                        i_return = adb_click_back_of_chat_with_check(g_Event_for_main_work)
                        if 0 != i_return:
                            break
                    # 通知
                    if i_return_of_send == APP_RET_CODE_UN_SAFE_QUESTION:
                        send_bussiness(g_Event_for_main_work, "[{}]存在非安全的问句[{}], 被大模型拒答了".format(username, msg_send))
                    elif i_return_of_send == APP_RET_CODE_NO_ANSWER_IN_KNOWLEDAGE:
                        send_bussiness(g_Event_for_main_work, "[{}]的问题[{}], 在知识库里无法找到对应答案".format(username, msg_send))
                else:
                    #print_my("【{}】没有新消息".format(username))
                    pass
            if i_return in [APP_RET_CODE_UNEXPECT_CHAT_PAGE]:
                i_return = 0
                continue
            if 0 != i_return:
                break        
            # 动作：发送消息
            """
            random_number = randint(1, 5)
            if random_number == 1:
                if len(msg_log_txt) == 0:
                    msg_log_txt = "没有新消息 {}".format(loop_count)
                i_return = send_webChat_message(g_Event_for_main_work, USERNAME_FOR_NOTICE, msg_log_txt)
                msg_log_txt = ""                
                if 0 != i_return:
                    break
                # 动作：返回键
                i_return = adb_click_back_of_chat_with_check(g_Event_for_main_work)
                if 0 != i_return:
                    break
            """
            # 每个循环随机等待一个间隔时间
            random_float  = uniform(0.1, 0.5)
            #random_float  = uniform(0.2, 1)
            #random_float  = uniform(1, 2)
            print("随机停{:.2f}秒".format(random_float))
            if True == g_Event_for_main_work.wait(random_float):
                print("main_work_thread, 被要求退出22")
                i_return = APP_RET_CODE_ZHU_DONG_EXIT
                break
            continue
        #if i_return in [APP_RET_CODE_APP_EXIT, APP_RET_CODE_NO_FOUND]:
        #    continue
        
        if APP_RET_CODE_ZHU_DONG_EXIT == i_return:
            break
        elif APP_RET_CODE_APP_KA_ZHU == i_return:
            iRet = do_after_ka_zhu(g_Event_for_main_work)
            if iRet == APP_RET_CODE_ZHU_DONG_EXIT:
                break 
            continue
        elif APP_RET_CODE_LIC_OUTDATE == i_return:
            table.signal_of_table.emit("lic_outdate") 
            break
        elif APP_RET_CODE_NET_ERROR == i_return:
            table.signal_of_table.emit("net_error")
            break
        #break
        continue
    table.signal_of_table.emit("show_app")    
    # 发送业务通知
    if b_has_notice_start == True:
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
        	send_bussiness(None, "停止运行")
    main_thread_exit_proce(table)
    
    # chenyj debug
    print("<===主业务线程名称:{} 开始时间:{}".format(threading.current_thread().name, time.strftime("%Y-%m-%d %H:%M:%S")))
    
    return
        
# 授权对话框
class LicenceWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        global g_str_mac
        
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('授权窗口')
        self.resize(int(490/1280*g_desktop_w), int(230/720*g_desktop_h))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        dlgLayout=QVBoxLayout()
        b_outdate, delta_second = is_out_of_time()
        self.stateLabel = QLabel("状态：{}".format("试用(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != "0" else "永久会员"))
        labelLayout1 = QHBoxLayout()
        labelLayout1.addWidget(self.stateLabel)
        
        self.macLabel = QLabel("本机mac地址：{}".format(g_str_mac))
        self.copyBtn = QPushButton("复制")
        self.copyBtn.clicked.connect(self.copyBtnFun)
        labelLayout2 = QHBoxLayout()
        labelLayout2.addWidget(self.macLabel)
        labelLayout2.addWidget(self.copyBtn)
        
        self.meLabel = QLabel("客服微信:")
        labelLayout3 = QHBoxLayout()
        labelLayout3.addWidget(self.meLabel)
        # 创建 QLabel 用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # 设置图片居中显示
        
        pixmap = QPixmap(f"{APP_IMG_DIR}\\ke_fu_image.png")
        parent_width = self.width()
        parent_height = self.height()
        display_width = parent_width // 4
        display_height = parent_height // 4
        scaled_pixmap = pixmap.scaled(display_width, display_height, Qt.KeepAspectRatio)
        # 设置图片到 QLabel
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.resize(scaled_pixmap.width(), scaled_pixmap.height())
        labelLayout3.addWidget(self.image_label)
        labelLayout3.addStretch(1)  # 添加伸缩因子

        
        self.licenIdEdit = QTextEdit()
        self.licenIdEdit.setPlaceholderText("请加客服微信,将mac地址发给客服,收到授权码后,粘贴到此处,然后点击\"验证\"")
        self.checkBtn = QPushButton("验证")
        self.checkBtn.clicked.connect(self.checkBtnFun)
        # chenyj test
        #   发布时一定要把此行代码关闭
        self.encodeBtn = QPushButton("编码")
        self.encodeBtn.clicked.connect(self.encodeBtnFun)
        self.encodeBtn.setHidden(True)
        vBoxLayout1=QVBoxLayout()
        vBoxLayout1.addWidget(self.checkBtn)
        #vBoxLayout1.addWidget(self.encodeBtn)
        
        labelLayout4 = QHBoxLayout()
        labelLayout4.addWidget(self.licenIdEdit)
        labelLayout4.addLayout(vBoxLayout1)
        
        labelLayout5 = QHBoxLayout()
        labelLayout5.addWidget(self.encodeBtn)
        
        dlgLayout.addLayout(labelLayout1)
        dlgLayout.addLayout(labelLayout2)
        dlgLayout.addLayout(labelLayout3)
        dlgLayout.addLayout(labelLayout4)
        dlgLayout.addLayout(labelLayout5)
        
        self.setLayout(dlgLayout)        
        return
    
    def copyBtnFun(self):
        pc.copy(g_str_mac)
        return

    def checkBtnFun(self):
        global g_config_json_data
        
        str_lic = self.licenIdEdit.toPlainText()
        if len(str_lic) == 0:
            QMessageBox.information(self, APP_NAME, "请输入授权码", QMessageBox.Yes)
            return
        try:
            str_lic_decoded = b64decode(str_lic.encode()).decode()
        except Exception as e:
            QMessageBox.information(self, APP_NAME, "输入授权码不合法", QMessageBox.Yes)
            return
        #print_my("解码后的lic：{}".format(str_lic_decoded))
        USER_TYPE_DICT = {"user_type_-1":"-1", "user_type_0":"0", "user_type_1":"1", "user_type_2":"2"}
        user_type = "0"
        for user_key in USER_TYPE_DICT:
            if user_key in str_lic_decoded:
                user_type = USER_TYPE_DICT[user_key]
                str_lic_decoded = str_lic_decoded.replace(user_key, "")
                break 
        if str_lic_decoded.replace(SECTRY_STR, "") == g_str_mac:
            print_my("授权成功")
            time_now = time.time()
            g_config_json_data["FIRST"] = time_now
            g_config_json_data["USER_TYPE"] = user_type
            save_config_data(g_config_json_data, g_config_path)
            b_outdate, delta_second = is_out_of_time()
            self.stateLabel.setText("状态：{}".format("试用(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != "0" else "永久会员"))
            self._signal.emit("lic_sucess")
            QMessageBox.information(self, APP_NAME, "授权成功", QMessageBox.Yes)
        else:
            print_my("!!!!授权失败(授权码不对应)")
            QMessageBox.information(self, APP_NAME, "授权失败(授权码不对应)", QMessageBox.Yes)
        return
    def encodeBtnFun(self):  
        return

# 设置托管对象对话框
class SetDepositObjectWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, username_of_can_deposit_list, username_of_deposit_list, b_auto_start_after):
        super().__init__()
        # 把“通用用对象”排除掉
        self.username_of_can_deposit_list = []
        for username in username_of_can_deposit_list:
            if username == USERNAME_FOR_NOTICE:
                continue 
            self.username_of_can_deposit_list.append(username)
        self.username_of_deposit_list = username_of_deposit_list
        self.b_auto_start_after = b_auto_start_after
        self.initUI()
 
    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('设置托管对象窗口')
        self.resize(int(450/1920*g_desktop_w), int(500/1080*g_desktop_h))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        dlgLayout=QVBoxLayout()
        
        # 输入框 
        """
        self.usernameEdit = QTextEdit()
        self.usernameEdit.setPlaceholderText("请输入要托管的微信聊天对象的完整昵称")
        labelLayout3 = QHBoxLayout()
        labelLayout3.addWidget(self.usernameEdit)
        """
        
        # 列表控件
        listLayout = QVBoxLayout()
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QListWidget.MultiSelection)  # 设置为多选模式
        # 添加列表项
        #for i, item_str in enumerate(self.username_of_can_deposit_list):
        #    self.listWidget.addItem(item_str)
        listLayout.addWidget(self.listWidget)
        self.reload_list_view()
        
        self.addBtn = QPushButton("手动输入好友名称")
        self.addBtn.clicked.connect(self.addBtnFun)
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        
        #dlgLayout.addLayout(labelLayout3)
        dlgLayout.addLayout(listLayout)
        dlgLayout.addWidget(self.addBtn)
        dlgLayout.addWidget(self.confirmBtn)
        
        self.setLayout(dlgLayout)
        return
        
    def reload_list_view(self):
        self.listWidget.clear()
        # 添加列表项
        for i, item_str in enumerate(self.username_of_can_deposit_list):
            self.listWidget.addItem(item_str)
        # 显示窗口时，添加勾选框
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            checkbox = QCheckBox(self.listWidget)
            checkbox.setText(item.text())
            if item.text() in self.username_of_deposit_list:
                checkbox.setChecked(True)
            item.setText("")
            item.setSizeHint(checkbox.sizeHint())
            self.listWidget.setItemWidget(item, checkbox)
            
    def getSelectedItems(self):
        selected_items = []
        for i in range(self.listWidget.count()):
            item_checkbox = self.listWidget.itemWidget(self.listWidget.item(i))
            if item_checkbox.isChecked():
                selected_items.append(item_checkbox.text())
        return selected_items
        
    def addBtnFun(self):
        self.addDepositObject_Win = AddDepositObjectWindow(self)
        self.addDepositObject_Win._signal.connect(self.signal_recv_func)
        self.addDepositObject_Win.setWindowModality(Qt.ApplicationModal)
        self.addDepositObject_Win.show()
        self.addDepositObject_Win.exec_()
        return
        
    def confirmBtnFun(self):
        selected_items = self.getSelectedItems()
        
        #if len(selected_items) == 0:
        #    QMessageBox.information(self, APP_NAME, "请选择托管对象的昵称", QMessageBox.Yes)
        #    return
        print_my("您选中的托管用户名是:{}".format(selected_items))
        self._signal.emit("deposit_username_{}_b_auto_start_after_{}".format(selected_items, self.b_auto_start_after))
        self.close()
        return
        
    def signal_recv_func(self, para):
        global g_config_json_data
        global g_config_path
        
        if para.startswith("add_deposit_object_"):
            print("SetDepositObjectWindow事件收到信号:{}".format(para))
            
            username_str = para.replace("add_deposit_object_", "")
            print("SetDepositObjectWindow, signal_recv_func, 添加新的托管对象:{}".format(username_str))
            self.username_of_can_deposit_list.append(username_str)
 
            # 保存到列表中
            g_config_json_data["username_of_can_deposit_list"] = self.username_of_can_deposit_list
            save_config_data(g_config_json_data, g_config_path)  
                
            self.reload_list_view() 
        return
      
# 设置Agent对话框
class SetAgentWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, can_agent_list, sel_agent_list, hua_su_file_paths, b_auto_start_after):
        super().__init__()
        self.can_agent_list = can_agent_list
        self.sel_agent_list = sel_agent_list
        self.hua_su_file_paths = hua_su_file_paths
        self.b_auto_start_after = b_auto_start_after
        
        self.selected_checkbox = None
        self.initUI()
 
    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('设置Agent窗口')
        # 设置窗口为全屏
        #self.resize(int(450/1920*g_desktop_w), int(300/1080*g_desktop_h))
        self.resize(int(g_desktop_w), int(g_desktop_h*9/10))
        
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        dlgLayout=QVBoxLayout()
        
        # 列表控件
        listLayout = QVBoxLayout()
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QListWidget.SingleSelection)  # 设置为单选模式
        self.listWidget.addItem("KimiChat大模型")
        self.listWidget.addItem("角色:女大学生闲聊")
        self.listWidget.addItem("Coze图片生成智能体")
        self.listWidget.addItem("闲聊专家自定义本地话术库")
        self.listWidget.addItem("销冠自定义本地话术库")
        self.listWidget.addItem("电商客服自定义本地话术库")

        # 添加列表项
        for i, item_str in enumerate(self.can_agent_list):
            self.listWidget.addItem(item_str)
       
        listLayout.addWidget(self.listWidget)
        
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        
        #dlgLayout.addLayout(labelLayout3)
        dlgLayout.addLayout(listLayout)
        dlgLayout.addWidget(self.confirmBtn)
        
        self.setLayout(dlgLayout)

        return
        
    def showEvent(self, event):
        # 显示窗口时，添加勾选框
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            checkbox = QCheckBox(self.listWidget)
            checkbox.setText(item.text())
            if item.text() in self.sel_agent_list:
                checkbox.setChecked(True)
                self.selected_checkbox = checkbox
            checkbox.stateChanged.connect(self.checkboxStateChanged)
            item.setText("")
            item.setSizeHint(checkbox.sizeHint())
                    # 连接itemClicked信号到事件处理函数
        
            self.listWidget.setItemWidget(item, checkbox)
        
    def checkboxStateChanged(self, state):
        checkbox = self.sender()
        checkbox_text = checkbox.text()
        if checkbox.isChecked():
            print(f"{checkbox_text} 被选中")
            if self.selected_checkbox is not None:
                self.selected_checkbox.setChecked(False)
            self.selected_checkbox = checkbox
            if checkbox_text in ["电商客服自定义本地话术库", "闲聊专家自定义本地话术库", "销冠自定义本地话术库"]:
                self.setHuaSu_Win = SetFileDialog('设置本地话术库', self.hua_su_file_paths, self.b_auto_start_after)
                self.setHuaSu_Win._signal.connect(self.signal_recv_func)
                self.setHuaSu_Win.setWindowModality(Qt.ApplicationModal)
                self.setHuaSu_Win.show()
                self.setHuaSu_Win.exec_()
        else:
            print(f"{checkbox_text} 被取消选中")
            self.selected_checkbox = None
            
    def getSelectedItems(self):
        selected_items = []
        for i in range(self.listWidget.count()):
            item_checkbox = self.listWidget.itemWidget(self.listWidget.item(i))
            if item_checkbox.isChecked():
                selected_items.append(item_checkbox.text())
        return selected_items
    
    def confirmBtnFun(self):
        selected_items = self.getSelectedItems()
        
        if len(selected_items) == 0:
            QMessageBox.information(self, APP_NAME, "请选择的Agent", QMessageBox.Yes)
            return
        # chenyj debug
        print("confirmBtnFun, 您选中的Agent是:{}".format(selected_items))
        self._signal.emit("agent_{}".format(selected_items))
        #if selected_items[0] == "电商客服自定义本地话术库":
        #    self._signal.emit("hua_su_file_paths_{}_b_auto_start_after_{}".format(self.hua_su_file_paths, self.b_auto_start_after))
        self._signal.emit("hua_su_file_paths_{}_b_auto_start_after_{}".format(self.hua_su_file_paths, self.b_auto_start_after))
        self.close()
        return
        
    def signal_recv_func(self, para):
        if para.startswith("hua_su_file_paths_"):
            print("SetAgentWindow事件收到信号:{}".format(para))
            b_auto_start_after = False 
            if "_b_auto_start_after_True" in para:
                para = para.replace("_b_auto_start_after_True", "")
                b_auto_start_after = True
            elif "_b_auto_start_after_False" in para:
                para = para.replace("_b_auto_start_after_False", "")
                b_auto_start_after = False
                
            #self.set_state(EnvStateType.Env_Set_Tuo_State, True)
            file_paths_str = para.strip("hua_su_file_paths_")
            
            file_paths = ast.literal_eval(file_paths_str)
            self.hua_su_file_paths = file_paths
        return
    """
    重写closeEvent方法
    """
    def closeEvent(self, event):
        selected_items = self.getSelectedItems()
        
        print_my("您选中的Agent是:{}".format(selected_items))
        self._signal.emit("agent_{}".format(selected_items))
 
        self._signal.emit("hua_su_file_paths_{}_b_auto_start_after_{}".format(self.hua_su_file_paths, self.b_auto_start_after))
        self.close()
        return    
        
class ButtonItem(QStandardItem):
    def __init__(self, button):
        super(ButtonItem, self).__init__()
        self.button = button
        
class CustomProgressDialog(QProgressDialog):
    def __init__(self, *args, **kwargs):
        super(CustomProgressDialog, self).__init__(*args, **kwargs)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()  # 忽略 Esc 键事件
        else:
            super(CustomProgressDialog, self).keyPressEvent(event)

# 环境状态
class EnvStateType(Enum):
    Env_Net_State = 0
    Env_Start_Simulator_State = 1
    Env_WeiChat_State = 2
    Env_Set_Tuo_State = 3
    Env_Set_Hua_Su_State = 4
    Env_Sucess = 5 

def is_thread_running(target_func_name):
    print("is_thread_running, {}".format(target_func_name))
    for thread in threading.enumerate():
        print("    {}".format(thread.name))
        if target_func_name in thread.name:  # 如果线程的名称（假设使用函数名作为线程名）匹配
            return True
    return False

class Table(QWidget):
	signal_of_table = pyqtSignal(str) #定义信号
    
	def __init__(self, arg=None):
		global g_table
		super(Table, self).__init__(arg)
		self.setWindowFlags(Qt.FramelessWindowHint)

		self.setWindowTitle(APP_NAME)
		self.setWindowIcon(QIcon('./logo.ico'))
        
		operatorLayout = QHBoxLayout()
		# 手机管理 
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			self.jiQunBtn = PicButton(f"{APP_IMG_DIR}\\ji_qun.png", "多手机管理")
		#
		self.startBtn = QPushButton("开始运行")
		#self.startBtn = PicButton(f"{APP_IMG_DIR}\\start.png", "开始运行")
		self.startBtn.setStyleSheet("""
            QPushButton {
                background-color: #3366FF; /* 蓝色背景 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:hover {
                background-color: #1A387B; /* 鼠标悬停时的背景颜色 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:enabled {
                background-color: #3366FF; /* 蓝色背景 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.stopBtn = QPushButton("停止运行")
		self.stopBtn.setStyleSheet("""
            QPushButton {
                color: blue;          /* 设置字体颜色为蓝色 */
                font-weight: bold;    /* 设置字体为粗体 */
                font-size: 14px;      /* 可选：设置字体大小 */
            }
            QPushButton:disabled {
                color: gray;
            }
        """)
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			operatorLayout.addWidget(self.jiQunBtn, 1)
		operatorLayout.addWidget(self.startBtn, 5)
		operatorLayout.addWidget(self.stopBtn, 5)
		#operatorLayout.addWidget(self.delBtn)

        # 按钮的信号槽连接
		self.startBtn.clicked.connect(self.startBtnFun)
		self.stopBtn.clicked.connect(self.stopBtnFun)
		self.startBtn.setEnabled(True)
		self.stopBtn.setEnabled(False)
        
        # 设置应用程序为全屏
		#self.resize(int(1100/1280*g_desktop_w),int(400/720*g_desktop_h))
		self.resize(int(g_desktop_w),int(g_desktop_h*9/10))
        # 设置贴着屏幕右边
		"""
  		ww_now = int(g_desktop_w/5)
		wh_now = int(g_desktop_h*9/10)
		self.setGeometry(g_desktop_w - ww_now, 50, ww_now, wh_now)
		"""

		update_task_state_by_setting(g_config_json_data)

		tableLayout = QHBoxLayout()
        # 创建日志显示控件
		self.layout_log = QVBoxLayout()
		self.logTextEdit = QTextEdit("初始化中...请稍候...")
		self.logTextEdit.setReadOnly(True)  # 设置为只读
		#     设置字体
		font = QFont("Arial", 15)  # Arial字体，12号大小
		self.logTextEdit.setFont(font)
		self.last_text_of_logTextEdit = ""
		self.layout_log.addWidget(self.logTextEdit, 1)
        
		self.layout_phone = QHBoxLayout()
		# 创建手机截屏显示控件
		self.phoneImageLabel = ClickableLabel()
		self.phoneImageLabel.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
		self.phoneImageLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.phoneImageLabel.clicked.connect(self.phoneImageLabelBtnFun)
		# 加载默认的off_line.png图片
		self.update_screen_img(f"{APP_IMG_DIR}\\off_line.png", "点击连接")
		
  		# 当前手机的微信状态
		self.currentLogonWechatBtn = PicButton(f"{APP_IMG_DIR}\\weichat_logo.png", "未登录")
  
		self.layout_phone.addWidget(self.phoneImageLabel)
		self.layout_phone.addWidget(self.currentLogonWechatBtn)
		self.layout_log.addLayout(self.layout_phone, 1)
		self.update_logon_wechat_state()
        
        # 创建一个提示标签，初始时隐藏
		self.toolTip = QLabel("这是一个提示消息", self)
		self.toolTip.setStyleSheet("background-color: #ffd700; padding: 10px; border-radius: 5px;")
		self.toolTip.setAlignment(Qt.AlignCenter)
		self.toolTip.setFixedSize(500, 50)
		self.toolTip.setWordWrap(True)
		self.toolTip.hide()
		self.layout_log.addWidget(self.toolTip)
        
		tableLayout.addLayout(self.layout_log, 1)
  
		self.applicationState = ApplicationState.Normal
        #################TAB控制##################################
		self.layout_table = QVBoxLayout()
		self.tab_widget = QTabWidget()
		self.tab_widget.setTabBar(CustomTabBar(True))  # 使用自定义的 QTabBar
		self.tab_widget.currentChanged.connect(self.on_tab_changed_func)
        #################### 第1个tab: 产品
		# 创建产品列表控件
		self.layout_productlist = QVBoxLayout()
		self.productTableView=QTableView()
		self.productModel=QStandardItemModel(0, 5)
		self.productTableView.setModel(self.productModel)
		self.productTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.productTableView.horizontalHeader().setStretchLastSection(True)
		self.productTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.productTableView.clicked.connect(self.productTable_cell_clicked)  
		self.productTable_click_last_time = time.time()
		self.layout_productlist.addWidget(self.productTableView)
        # 填充数据
		self.reload_product_list_view()
        
		self.addProductBtn = QPushButton("添加产品")
  		# 解决开始按钮样式丢失问题
		self.addProductBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.product_info_list = g_config_json_data["PRODUCT_INFO_LIST"]
		self.addProductBtn.clicked.connect(self.addProductBtnFun)
		self.layout_productlist.addWidget(self.addProductBtn)
		# 把layout_productlist加到tab里
		self.tab_product = QWidget()
		self.tab_product.setLayout(self.layout_productlist)
		idx = self.tab_widget.addTab(self.tab_product, "产品")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\product.png", f"{APP_IMG_DIR}\\product_disable.png")
        #################### 第2个tab: 好友
		# 创建客户组列表控件
		self.layout_friendlist = QVBoxLayout()
		self.friendTableView=QTableView()
		self.friendModel=QStandardItemModel(0, 5)
		self.friendTableView.setModel(self.friendModel)
		self.friendTableView.setVerticalScrollMode(QTableView.ScrollPerPixel)
		self.friendTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.friendTableView.horizontalHeader().setStretchLastSection(True)
		self.friendTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.friendTableView.clicked.connect(self.friendTable_cell_clicked)  
		self.friendTable_click_last_time = time.time()
		self.layout_friendlist.addWidget(self.friendTableView)
        # 填充数据
		self.friend_info_list_of_show = []
		self.reload_friend_list_view()
        
		####################################################################################
		# 添加搜索框
		self.searchBox = QLineEdit()
		self.searchBox.setPlaceholderText("搜索好友昵称")
		self.searchBox.textChanged.connect(self.filter_friend_list)
		self.layout_friendlist.addWidget(self.searchBox)
		###############################################################################
		self.layout_friendBtn = QHBoxLayout()
		# 
		self.exportFriendBtn = QPushButton("导出好友列表")
		self.exportFriendBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""")
		self.exportFriendBtn.clicked.connect(self.exportFriendBtnFun)
		self.layout_friendBtn.addWidget(self.exportFriendBtn)
        # 
		self.syncFriendBtn = QPushButton("同步好友")
		self.syncFriendBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]
		self.syncFriendBtn.clicked.connect(self.syncFriendBtnFun)
		self.layout_friendBtn.addWidget(self.syncFriendBtn)
		#self.layout_friendlist.addWidget(self.syncFriendBtn)
		self.layout_friendlist.addLayout(self.layout_friendBtn)
		# 把layout_productlist加到tab里
		self.tab_friend = QWidget()
		self.tab_friend.setLayout(self.layout_friendlist)
		idx = self.tab_widget.addTab(self.tab_friend, "客户")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\ke_hu.png", f"{APP_IMG_DIR}\\ke_hu_disable.png")
        
        #################### 第3个tab: 客户组
		# 创建客户组列表控件
		self.layout_usergrouplist = QVBoxLayout()
		self.layout_usergroupBtn = QHBoxLayout()
		self.usergroupTableView=QTableView()
		self.usergroupModel=QStandardItemModel(0, 5);
		self.usergroupTableView.setModel(self.usergroupModel)
		self.usergroupTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.usergroupTableView.horizontalHeader().setStretchLastSection(True)
		self.usergroupTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.usergroupTableView.clicked.connect(self.usergroupTable_cell_clicked)  
		self.usergroupTable_click_last_time = time.time()
		self.layout_usergrouplist.addWidget(self.usergroupTableView)
        # 填充数据
		self.update_lv_cheng_group_data()
		self.reload_usergroup_list_view()
        #    “添加客户组”按钮
		self.addUsergroupBtn = QPushButton("添加客户组")
		self.addUsergroupBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.usergroup_info_list = g_config_json_data["USERGROUP_INFO_LIST"]
		self.addUsergroupBtn.clicked.connect(self.addUsergroupBtnFun)
		self.layout_usergroupBtn.addWidget(self.addUsergroupBtn)
		#    “同步微信标签组”按钮
		self.syncTagGroupBtn = QPushButton("同步微信标签组")
		self.syncTagGroupBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.syncTagGroupBtn.clicked.connect(self.syncTagGroupBtnFun)
		# chenyj test
		#self.layout_usergroupBtn.addWidget(self.syncTagGroupBtn)
		self.layout_usergrouplist.addLayout(self.layout_usergroupBtn)
  
		# 把layout_productlist加到tab里
		self.tab_usergroup = QWidget()
		self.tab_usergroup.setLayout(self.layout_usergrouplist)
		idx = self.tab_widget.addTab(self.tab_usergroup, "客户组")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\ke_hu_group.png", f"{APP_IMG_DIR}\\ke_hu_group_disable.png")
        
        #################### 第4个tab: 内容
		# 创建内容列表控件
		self.layout_contentlist = QVBoxLayout()
		self.contentTableView=QTableView()
		self.contentModel=QStandardItemModel(0, 5);
		self.contentTableView.setModel(self.contentModel)
		self.contentTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.contentTableView.horizontalHeader().setStretchLastSection(True)
		self.contentTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.contentTableView.clicked.connect(self.contentTable_cell_clicked)  
		self.contentTable_click_last_time = time.time()
		self.layout_contentlist.addWidget(self.contentTableView)
        # 填充数据
		self.reload_content_list_view()
        
		self.addContentBtn = QPushButton("添加文案")
		self.addContentBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.content_info_list = g_config_json_data["CONTENT_INFO_LIST"]
		self.addContentBtn.clicked.connect(self.addContentBtnFun)
		self.layout_contentlist.addWidget(self.addContentBtn)
		# 把layout_contentlist加到tab里
		self.tab_content = QWidget()
		self.tab_content.setLayout(self.layout_contentlist)
		idx = self.tab_widget.addTab(self.tab_content, "文案")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\wen_an.png", f"{APP_IMG_DIR}\\wen_an_disable.png")
        
        #################### 第5个tab: 智能体
		# 创建智能体列表控件
		self.layout_agentlist = QVBoxLayout()
		self.agentTableView=QTableView()
		self.agentModel=QStandardItemModel(0, 5);
		self.agentTableView.setModel(self.agentModel)
		self.agentTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.agentTableView.horizontalHeader().setStretchLastSection(True)
		self.agentTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.agentTableView.clicked.connect(self.agentTable_cell_clicked)  
		self.agentTable_click_last_time = time.time()
		self.layout_agentlist.addWidget(self.agentTableView)
        # 填充数据
		self.reload_agent_list_view()
        
		self.addAgentBtn = QPushButton("添加营销智能体")
		self.addAgentBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.agent_info_list = g_config_json_data["AGENT_INFO_LIST"]
		self.addAgentBtn.clicked.connect(self.addAgentBtnFun)
		self.layout_agentlist.addWidget(self.addAgentBtn)
		# 把layout_productlist加到tab里
		self.tab_agent = QWidget()
		self.tab_agent.setLayout(self.layout_agentlist)
		idx = self.tab_widget.addTab(self.tab_agent, "营销智能体")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\ying_xiao.png", f"{APP_IMG_DIR}\\ying_xiao_disable.png")
        
        #################### 第6个tab: 客服机器人
		# 创建智能回复列表控件
		self.layout_autoreplylist = QVBoxLayout()
		self.autoReplyTableView=QTableView()
		self.autoReplyModel=QStandardItemModel(0, 5);
		self.autoReplyTableView.setModel(self.autoReplyModel)
		self.autoReplyTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.autoReplyTableView.horizontalHeader().setStretchLastSection(True)
		self.autoReplyTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.autoReplyTableView.clicked.connect(self.autoreplyTable_cell_clicked)  
		self.autoreplyTable_click_last_time = time.time()
		self.layout_autoreplylist.addWidget(self.autoReplyTableView)
        # 填充数据
		self.reload_autoreply_list_view()
        
		self.addAutoReplyBtn = QPushButton("添加自动客服机器人")
		self.addAutoReplyBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.autoreply_info_list = g_config_json_data["AUTOREPLY_INFO_LIST"]
		self.addAutoReplyBtn.clicked.connect(self.addAutoReplyBtnFun)
		self.layout_autoreplylist.addWidget(self.addAutoReplyBtn)
		# 把layout_productlist加到tab里
		self.tab_autoreply = QWidget()
		self.tab_autoreply.setLayout(self.layout_autoreplylist)
		idx = self.tab_widget.addTab(self.tab_autoreply, "客服机器人")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\ke_fu.png", f"{APP_IMG_DIR}\\ke_fu_disable.png")
        
        #################### 第7个tab: 获客机器人
		# 创建添加机器人列表控件
		self.layout_autoaddlist = QVBoxLayout()
		self.autoAddTableView=QTableView()
		self.autoAddModel=QStandardItemModel(0, 5);
		self.autoAddTableView.setModel(self.autoAddModel)
		self.autoAddTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.autoAddTableView.horizontalHeader().setStretchLastSection(True)
		self.autoAddTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.autoAddTableView.clicked.connect(self.autoaddTable_cell_clicked)  
		self.autoaddTable_click_last_time = time.time()
		self.layout_autoaddlist.addWidget(self.autoAddTableView)
        # 填充数据
		self.reload_autoadd_list_view()
        
		self.addAutoAddBtn = QPushButton("添加获客机器人")
		self.addAutoAddBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.autoadd_info_list = g_config_json_data["AUTOADD_INFO_LIST"]
		self.addAutoAddBtn.clicked.connect(self.addAutoAddBtnFun)
		self.layout_autoaddlist.addWidget(self.addAutoAddBtn)
		# 把layout_productlist加到tab里
		self.tab_autoadd = QWidget()
		self.tab_autoadd.setLayout(self.layout_autoaddlist)
		idx = self.tab_widget.addTab(self.tab_autoadd, "获客智能体")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\huo_ke.png", f"{APP_IMG_DIR}\\huo_ke_disable.png")
        
        #################### 第8个tab: 通友机器人
		self.addAutoPassBtn = None
		'''
		# 创建通友机器人列表控件
		self.layout_autopasslist = QVBoxLayout()
		self.autoPassTableView=QTableView()
		self.autoPassModel=QStandardItemModel(0, 5);
		self.autoPassTableView.setModel(self.autoPassModel)
		self.autoPassTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.autoPassTableView.horizontalHeader().setStretchLastSection(True)
		self.autoPassTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.autoPassTableView.clicked.connect(self.autopassTable_cell_clicked)  
		self.autopassTable_click_last_time = time.time()
		self.layout_autopasslist.addWidget(self.autoPassTableView)
        # 填充数据
		self.reload_autopass_list_view()
        
		self.addAutoPassBtn = QPushButton("添加通过好友机器人")
		self.addAutoPassBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.autopass_info_list = g_config_json_data["AUTOPASS_INFO_LIST"]
		self.addAutoPassBtn.clicked.connect(self.addAutoPassBtnFun)
		self.layout_autopasslist.addWidget(self.addAutoPassBtn)
		# 把layout_autopasslist加到tab里
		self.tab_autopass = QWidget()
		self.tab_autopass.setLayout(self.layout_autopasslist)
		self.tab_widget.addTab(self.tab_autopass, "通友机器人")
		'''
        #################### 第9个tab: 待执行任务列表
		# 创建任务列表控件
		self.layout_tasklist = QVBoxLayout()
		self.taskTableView=QTableView()
		self.taskModel=QStandardItemModel(0, 4);
		#self.taskModel.setHorizontalHeaderLabels(['任务类型', '任务描述', '任务进度'])
		self.taskTableView.setModel(self.taskModel)
		self.taskTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.taskTableView.horizontalHeader().setStretchLastSection(True)
		self.taskTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.taskTableView.clicked.connect(self.taskTable_cell_clicked)  
		self.taskTable_click_last_time = time.time()
		self.layout_tasklist.addWidget(self.taskTableView)
        # 填充数据
		self.reload_task_list_view()
        
		self.addTaskBtn = QPushButton("添加任务")
		self.addTaskBtn.setVisible(False)
		self.task_info_list = g_config_json_data["TASK_INFO_LIST"]
		self.addTaskBtn.clicked.connect(self.addTaskBtnFun)
		self.layout_tasklist.addWidget(self.addTaskBtn)
		# 把layout_tasklist加到tab里
		self.tab_task = QWidget()
		self.tab_task.setLayout(self.layout_tasklist)
		idx = self.tab_widget.addTab(self.tab_task, "待执行任务列表")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\task_list.png", f"{APP_IMG_DIR}\\task_list_disable.png")
        
		#################### 第10个tab: 设置
		self.tableLayout_of_setting = QVBoxLayout()
		self.tab_widget_of_setting = QTabWidget()
		self.tab_widget_of_setting.setTabBar(CustomTabBar())  # 使用自定义的 QTabBar
		#font = self.tab_widget_of_setting.tabBar().font()
		#font.setPointSize(5)  # 设置你想要的字号大小
		#self.tab_widget_of_setting.tabBar().setFont(font)
		#self.tab_widget_of_setting.currentChanged.connect(self.on_tab_changed_func)
  
		#   ################### 设置页的第1个子tab: 基本设置  
		# 创建基本设置layout
		self.layout_basic_setting = QVBoxLayout()
		# 1.设置项：同步新好友的时间间隔
		layout_inter_sync_new_frient = QHBoxLayout()
		interSyncNewFrientLabel1 = QLabel("1. 每天间隔", self)
		layout_inter_sync_new_frient.addWidget(interSyncNewFrientLabel1)
		self.interSyncNewFrientEdit = QLineEdit(self)
		self.interSyncNewFrientEdit.setValidator(QIntValidator(5, 9999))  # 设置输入范围为0到99
		self.interSyncNewFrientEdit.setMaxLength(4)  # 设置最大输入长度为3
		self.interSyncNewFrientEdit.setFixedWidth(50)  # 设置输入框宽度为50像素
		# 秒转为分钟 
		i_minutes = int(int(g_config_json_data["GET_NEW_FRIEND_TIME_INTER"])/60)
		self.interSyncNewFrientEdit.setText(str(i_minutes))
		layout_inter_sync_new_frient.addWidget(self.interSyncNewFrientEdit)
		interSyncNewFrientLabel2 = QLabel("分钟同步1次新好友信息(间隔越小任务执行越及时，但同时也更占CPU)", self)
		layout_inter_sync_new_frient.addWidget(interSyncNewFrientLabel2)
		layout_inter_sync_new_frient.addStretch(1)
		self.layout_basic_setting.addLayout(layout_inter_sync_new_frient)
		# 2.设置项：检测是否有待执行的任务的时间间隔
		layout_inter_do_task = QHBoxLayout()
		interDoTaskLabel1 = QLabel("2.     间隔", self)
		layout_inter_do_task.addWidget(interDoTaskLabel1)
		self.interDoTaskEdit = QLineEdit(self)
		self.interDoTaskEdit.setValidator(QIntValidator(5, 9999))  # 设置输入范围为0到99
		self.interDoTaskEdit.setMaxLength(4)  # 设置最大输入长度为2
		self.interDoTaskEdit.setFixedWidth(50)  # 设置输入框宽度为50像素
		self.interDoTaskEdit.setText(str(g_config_json_data["TASK_TIME_INTER"]))
		layout_inter_do_task.addWidget(self.interDoTaskEdit)
		interDoTaskLabel2 = QLabel("秒检查1次是否有待执行的任务(间隔越小任务执行越及时，但同时也更占CPU)", self)
		layout_inter_do_task.addWidget(interDoTaskLabel2)
		layout_inter_do_task.addStretch(1)
		self.layout_basic_setting.addLayout(layout_inter_do_task)
		# 3.设置项：执行自动加好友的时间间隔
		layout_inter_add_friend = QHBoxLayout()
		interAddFriendLabel1 = QLabel("3.     间隔", self)
		layout_inter_add_friend.addWidget(interAddFriendLabel1)
		self.interAddFriendEdit = QLineEdit(self)
		self.interAddFriendEdit.setValidator(QIntValidator(60, 9999))  # 设置输入范围为0到99
		self.interAddFriendEdit.setMaxLength(4)  # 设置最大输入长度为2
		self.interAddFriendEdit.setFixedWidth(50)  # 设置输入框宽度为50像素
		self.interAddFriendEdit.setText(str(g_config_json_data["TASK_TIME_INTER_OF_ADD_NEW_FRIENT"]))
		layout_inter_add_friend.addWidget(self.interAddFriendEdit)
		interAddFriendLabel2 = QLabel("秒自动加1个好友(间隔越大越不会被封)", self)
		layout_inter_add_friend.addWidget(interAddFriendLabel2)
		layout_inter_add_friend.addStretch(1)
		self.layout_basic_setting.addLayout(layout_inter_add_friend)
		# 4.设置项：检测是否有新好友请求的时间间隔
		layout_inter_auto_pass = QHBoxLayout()
		interAutoPassLabel1 = QLabel("4.     间隔", self)
		layout_inter_auto_pass.addWidget(interAutoPassLabel1)
		self.interAutoPassEdit = QLineEdit(self)
		self.interAutoPassEdit.setValidator(QIntValidator(60, 9999))  # 设置输入范围为0到99
		self.interAutoPassEdit.setMaxLength(4)  # 设置最大输入长度为2
		self.interAutoPassEdit.setFixedWidth(50)  # 设置输入框宽度为50像素
		self.interAutoPassEdit.setText(str(g_config_json_data["AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT"]))
		layout_inter_auto_pass.addWidget(self.interAutoPassEdit)
		interAutoPassLabel2 = QLabel("秒检查1次是否新好友请求(间隔越小任务执行越及时，但同时也更占CPU)", self)
		layout_inter_auto_pass.addWidget(interAutoPassLabel2)
		layout_inter_auto_pass.addStretch(1)
		self.layout_basic_setting.addLayout(layout_inter_auto_pass)

		# 5.设置项：是否执行过期的任务
		layout_is_do_exceed_task = QHBoxLayout()
		isDoExceedTaskLabel1 = QLabel("5.     是否执行过期的任务: ", self)
		layout_is_do_exceed_task.addWidget(isDoExceedTaskLabel1)
		self.is_do_exceed_task_radio_button_list = []
		self.IS_DO_EXCEED_TASK_LIST = ["是", "否"]
		for i, raddio_name in enumerate(self.IS_DO_EXCEED_TASK_LIST):
			radio_button = QRadioButton(raddio_name, self)
			#radio_button.clicked.connect(self.update_add_model_dynamic_content)
			self.is_do_exceed_task_radio_button_list.append(radio_button)
		if g_config_json_data["g_b_Do_Exceed_Task"] == True:
			self.is_do_exceed_task_radio_button_list[0].setChecked(True)
		else:
			self.is_do_exceed_task_radio_button_list[1].setChecked(True)
		for radio_button in self.is_do_exceed_task_radio_button_list:
			layout_is_do_exceed_task.addWidget(radio_button)
            
		layout_is_do_exceed_task.addStretch(1)
		self.layout_basic_setting.addLayout(layout_is_do_exceed_task)
  
		# 6.设置项：自动生成图片的正向文本、反向文本
		layout_text_of_gen_image = QHBoxLayout()
		posTextLabel = QLabel("6.     自动生成图片的正向文本: ", self)
		layout_text_of_gen_image.addWidget(posTextLabel)
		self.posTextEdit = QLineEdit(self)
		self.posTextEdit.setPlaceholderText("默认:根据文案内容自行决定")
		self.posTextEdit.setMaxLength(100)  # 设置最大输入长度为2
		self.posTextEdit.setFixedWidth(240)  # 设置输入框宽度为50像素
		self.posTextEdit.setText(g_config_json_data["POS_TEXT"])
		layout_text_of_gen_image.addWidget(self.posTextEdit)
  
		negTextLabel = QLabel("反向文本:", self)
		layout_text_of_gen_image.addWidget(negTextLabel)
		self.negTextEdit = QLineEdit(self)
		self.negTextEdit.setPlaceholderText("默认:根据文案内容自行决定")
		self.negTextEdit.setMaxLength(100)  # 设置最大输入长度为2
		self.negTextEdit.setFixedWidth(240)  # 设置输入框宽度为50像素
		self.negTextEdit.setText(g_config_json_data["NEG_TEXT"])
		layout_text_of_gen_image.addWidget(self.negTextEdit)
  
		layout_text_of_gen_image.addStretch(1)
		self.layout_basic_setting.addLayout(layout_text_of_gen_image)
  
  		# 添加一个伸缩空间，让第一个控件顶上显示
		spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.layout_basic_setting.addSpacerItem(spacer)
  
		################
		self.tab_basic_of_setting = QWidget()
		self.tab_basic_of_setting.setLayout(self.layout_basic_setting)
		self.tab_widget_of_setting.addTab(self.tab_basic_of_setting, "基本设置")
		#   ################### 设置页的第2个子tab: 大模型配置 
		# 创建大模型配置layout
		self.layout_llm_setting = QVBoxLayout()
		self.llmTableView=QTableView()
		self.llmModel=QStandardItemModel(0, 5)
		self.llmTableView.setModel(self.llmModel)
		self.llmTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.llmTableView.horizontalHeader().setStretchLastSection(True)
		self.llmTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.llmTableView.clicked.connect(self.llmTable_cell_clicked)  
		self.llmTable_click_last_time = time.time()
		self.layout_llm_setting.addWidget(self.llmTableView)
		self.reload_llm_list_view()
  		################
		self.tab_llm_of_setting = QWidget()
		self.tab_llm_of_setting.setLayout(self.layout_llm_setting)
		self.tab_widget_of_setting.addTab(self.tab_llm_of_setting, "大模型配置")
  		#   ################### 设置页的第3个子tab: 扣子智能体配置 
		# 创建扣子智能体配置layout
		self.layout_coze_setting = QVBoxLayout()
		self.cozeAgentTableView=QTableView()
		self.cozeAgentModel=QStandardItemModel(0, 5)
		self.cozeAgentTableView.setModel(self.cozeAgentModel)
		self.cozeAgentTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
		#下面代码让表格100%填满窗口
		self.cozeAgentTableView.horizontalHeader().setStretchLastSection(True)
		self.cozeAgentTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 连接信号
		self.cozeAgentTableView.clicked.connect(self.cozeAgentTable_cell_clicked)  
		self.cozeAgentTable_click_last_time = time.time()
		self.layout_coze_setting.addWidget(self.cozeAgentTableView)
		self.reload_coze_agent_list_view()
		# 添加按钮
		self.addCozeAgentBtn = QPushButton("添加Coze智能体")
		self.addCozeAgentBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.addCozeAgentBtn.clicked.connect(self.addCozeAgentBtnFun)
		self.layout_coze_setting.addWidget(self.addCozeAgentBtn)

  		################
		self.tab_coze_of_setting = QWidget()
		self.tab_coze_of_setting.setLayout(self.layout_coze_setting)
		self.tab_widget_of_setting.addTab(self.tab_coze_of_setting, "扣子智能体配置")
		#################################
		self.tableLayout_of_setting.addWidget(self.tab_widget_of_setting, 2)
		#   ################### 设置页的保存按钮
		self.saveSettingBtn = QPushButton("保存配置")
		self.saveSettingBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 22px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		self.saveSettingBtn.clicked.connect(self.saveSettingBtnFun)

		self.tableLayout_of_setting.addWidget(self.saveSettingBtn)
		################

  
		# 把layout_tasklist加到tab里
		self.tab_setting = QWidget()
		self.tab_setting.setLayout(self.tableLayout_of_setting)
		idx = self.tab_widget.addTab(self.tab_setting, "参数设置")
		self.tab_widget.tabBar().setTabIcon(idx, f"{APP_IMG_DIR}\\setting.png", f"{APP_IMG_DIR}\\setting_disable.png")
        
		###################################################
		self.tab_widget.setStyleSheet(self.tab_style_sheet)
		self.layout_table.addWidget(self.tab_widget)
        
        #######################################################################################
        # 底部banner
		shuoMingLayout=QVBoxLayout()
		shuo_ming_label1 = QLabel('<a href="https://gitee.com/chenyujing/dou_yin_yang_hao_real/blob/master/README.md">查看环境配置说明')
		shuo_ming_label1.setOpenExternalLinks(True)
		shuoMingLayout.addWidget(shuo_ming_label1)
        # chenyj test 
		#tableLayout.addLayout(shuoMingLayout)
        
		self.timeLabel = QLabel("此次运行时间:0秒")
		self.danCiLabel = QLabel("此次共收到:0条新消息,自动回复了0条")
        
		#self.meLabel = QLabel("                     ")
		# √①②③④⑤⑥⑦⑧⑨⑩╳◊
		#self.stateLabel = QLabel("环境检查：网络环境(√) -> 启动托管器(x) -> 微信登录 -> 设置托管对象 -> 正常运行")
		self.stateLabel = QLabel("环境检查:")
		self.stateNetLabel = QLabel("网络环境(*)")
		self.stateJianLabel1 = QLabel("->")
		self.stateSartLeiDianLabel = QLabel("启动托管器(*)")
		self.stateJianLabel2 = QLabel("->")
		self.stateWeiChatLabel = QLabel("微信登录(*)")
		self.stateJianLabel3 = QLabel("->")
		self.stateSetObjectLabel = QLabel("设置托管对象(*)")
		self.stateJianLabel4 = QLabel("->")
		self.stateSetHuasuLabel = QLabel("设置Agent(*)")
		self.stateJianLabel5 = QLabel("->")
		self.stateSucessLabel = QLabel("正常运行(*)")
        
		self.setDepositObjectBtn = QPushButton("设置的托管微信好友")
		self.setDepositObjectBtn.clicked.connect(self.setDepositObjectBtnFun)
        # chenyj
		self.setDepositObjectBtn.setVisible(False)
        
        # 初始化托管对象昵称列表
		#self.username_of_can_deposit_list = ["惠安家人", "任小玲"]
		self.username_of_can_deposit_list =  []
		if "username_of_can_deposit_list" in g_config_json_data:
			self.username_of_can_deposit_list = g_config_json_data["username_of_can_deposit_list"]
		# 初始化选中的托管对象昵称列表
		#self.username_of_deposit_list = ["任小玲"]
		self.username_of_deposit_list = []
		if "info_of_deposit_list" in g_config_json_data:
			self.username_of_deposit_list = [obj["username"] for obj in g_config_json_data["info_of_deposit_list"]]
		"""
		if len(self.username_of_can_deposit_list) == 0:
			self.setDepositObjectBtn.setEnabled(False)
		else:
			self.setDepositObjectBtn.setEnabled(True)
		"""
		self.setDepositObjectBtn.setEnabled(True)
        
        # 初始化Agent对象 
		self.can_agent_list = [agent_info["name"] for agent_info in AGENT_INFO_DICT]
		self.sel_agent_list = []
		if "sel_agent_list" in g_config_json_data:
			self.sel_agent_list = g_config_json_data["sel_agent_list"]
		if len(self.sel_agent_list) == 0:
			self.sel_agent_list = ["闲聊专家自定义本地话术库"]

            
		self.setAgentBtn = QPushButton("设置Agent")
		self.hua_su_file_paths = g_config_json_data["HUA_SU_FILES"]
		if len(self.hua_su_file_paths) == 0:
			self.hua_su_file_paths = [".\\示例_自定义本地话术库_销售.txt"]
      
		init_knowledage_str(self.hua_su_file_paths)
		self.setAgentBtn.clicked.connect(self.setAgentBtnFun)
        # chenyj 
		self.setAgentBtn.setVisible(False)
        
		b_outdate, delta_second = is_out_of_time()
		licenceState_str = "授权：{}".format("会员(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != 0 else "永久会员")
		self.licenceBtn = QPushButton(licenceState_str)
		#self.licenceBtn = QPushButton("授权")
		self.licenceBtn.clicked.connect(self.licenceBtnFun)
		self.licenceBtn.setVisible(True)
		
        
		labelLayout = QHBoxLayout()
        # 状态
		labelLayout_status = QVBoxLayout()
		labelLayout_status.addWidget(self.timeLabel)
		labelLayout_status.addWidget(self.danCiLabel)
		labelLayout.addLayout(labelLayout_status)
		# 客服二维码
		labelLayout_keFu = QHBoxLayout()
		self.meLabel = QLabel("客服微信:")
		labelLayout_keFu.addWidget(self.meLabel)
		# 	创建 QLabel 用于显示图片
		self.image_label = QLabel(self)
		self.image_label.setAlignment(Qt.AlignCenter)  # 设置图片居中显示
		pixmap = QPixmap(f"{APP_IMG_DIR}\\ke_fu_image.png")
		parent_width = self.width()
		parent_height = self.height()
		display_width = parent_width // 9
		display_height = parent_height // 9
		scaled_pixmap = pixmap.scaled(display_width, display_height, Qt.KeepAspectRatio)
        # 	设置图片到 QLabel
		self.image_label.setPixmap(scaled_pixmap)
		self.image_label.resize(scaled_pixmap.width(), scaled_pixmap.height())
		labelLayout_keFu.addWidget(self.image_label)
		labelLayout_keFu.addStretch(1)  # 添加伸缩因子
		labelLayout.addLayout(labelLayout_keFu) 
		# 使用说明二维码
		labelLayout_help = QHBoxLayout()
		self.helpLabel = QLabel("使用说明:")
		labelLayout_help.addWidget(self.helpLabel)
		# 	创建 QLabel 用于显示图片
		self.image_label_help = QLabel(self)
		self.image_label_help.setAlignment(Qt.AlignCenter)  # 设置图片居中显示

		pixmap = QPixmap(f"{APP_IMG_DIR}\\shi_pin_hao.png")
		parent_width = self.width()
		parent_height = self.height()
		display_width = parent_width // 9
		display_height = parent_height // 9
		scaled_pixmap_help = pixmap.scaled(display_width, display_height, Qt.KeepAspectRatio)
        # 	设置图片到 QLabel
		self.image_label_help.setPixmap(scaled_pixmap_help)
		self.image_label_help.resize(scaled_pixmap_help.width(), scaled_pixmap_help.height())
		labelLayout_help.addWidget(self.image_label_help)
		labelLayout_help.addStretch(1)  # 添加伸缩因子
		labelLayout.addLayout(labelLayout_help) 
		labelLayout.addStretch(1)  # 添加伸缩因子
		# 重要提示
		labelLayout_notice = QVBoxLayout()
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			self.label_notice = QLabel("<font color='red' size='20'>!!请千万不要去操作模拟器</font>")
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
			self.label_notice = QLabel("<font color='red' size='20'>!!请尽量不要去操作微信</font>")
		else:
			self.label_notice = QLabel("<font color='red' size='20'>!!请尽量不要去操作手机</font>")
		labelLayout_notice.addWidget(self.label_notice)
		labelLayout.addLayout(labelLayout_notice) 
		labelLayout.addStretch(1)  # 添加伸缩因子
  
		labelLayout.addWidget(self.setDepositObjectBtn)
		labelLayout.addWidget(self.setAgentBtn)
		labelLayout.addWidget(self.licenceBtn)
        
		labelLayout2 = QHBoxLayout()
		labelLayout3 = QHBoxLayout()
		
		labelLayout3.addWidget(self.stateLabel)
		labelLayout3.addWidget(self.stateNetLabel)
		labelLayout3.addWidget(self.stateJianLabel1)
		labelLayout3.addWidget(self.stateSartLeiDianLabel)
		labelLayout3.addWidget(self.stateJianLabel2)
		labelLayout3.addWidget(self.stateWeiChatLabel)
		labelLayout3.addWidget(self.stateJianLabel3)
		labelLayout3.addWidget(self.stateSetObjectLabel)
		labelLayout3.addWidget(self.stateJianLabel4)
		labelLayout3.addWidget(self.stateSetHuasuLabel)
		labelLayout3.addWidget(self.stateJianLabel5) 
		labelLayout3.addWidget(self.stateSucessLabel)

		#labelLayout2.addWidget(self.meLabel)
		#labelLayout2.addLayout(labelLayout_keFu)
		# 先去掉状态配置的提示
		#labelLayout2.addLayout(labelLayout3)
        
		self.layout_table.addLayout(labelLayout)
		tableLayout.addLayout(self.layout_table, 3)
  
        ##################################################
		dlgLayout=QVBoxLayout()
		dlgLayout.setContentsMargins(0, 0, 0, 0)
		titleBarLayout=QHBoxLayout()
		titleBarLayout.setContentsMargins(0, 0, 0, 0)  
		self.title_bar = CustomMainTitleBar(self)
		self.title_bar._signal.connect(self.signal_recv_func)
		titleBarLayout.addWidget(self.title_bar)
		dlgLayout.addLayout(titleBarLayout)
		operatorLayout.setContentsMargins(10, 10, 10, 10)
		dlgLayout.addLayout(operatorLayout)
		tableLayout.setContentsMargins(10, 10, 10, 10)
		dlgLayout.addLayout(tableLayout)
		#dlgLayout.addLayout(labelLayout)
		#dlgLayout.addLayout(labelLayout2)
        
		self.setLayout(dlgLayout)
        # 禁止窗口大小拉伸
		self.setFixedSize(self.width(), self.height())
        
		# 设置系统托盘 
		self.initTrayIcon()
        
		# 创建运行时间的定时器
		self.Timer_for_time = QTimer()
		self.Timer_for_showLogin = None
        # 检测授权
		self.signal_of_table.connect(self.signal_recv_func)  
		#self.signal_of_table.emit("check_lic") 
            
		g_table = self
		self.process_lei_dian = None
		# 
		self.set_btn_state(ApplicationState.Normal)
        
		self.waiting_Win = None
		self.rightPanelWin = None
        
		# 主窗口初始化成功
		self.Timer_for_Init_check = QTimer()
		self.Timer_for_Init_check.start(500*1)
		self.Timer_for_Init_check.timeout.connect(self.WindowsInitOk)
    
		return
		
	# 设置系统托盘
	def initTrayIcon(self):
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(QIcon('logo.ico'))
		self.tray_icon.setVisible(True)

		# 创建右键菜单
		self.menu = QMenu()
		self.action_show = QAction('显示', self)
		self.action_show.triggered.connect(self.show_window)
		self.action_quit = QAction('退出', self)
		self.action_quit.triggered.connect(self.quit_application)
		self.menu.addAction(self.action_show)
		self.menu.addAction(self.action_quit)

		self.tray_icon.setContextMenu(self.menu)
		return
        
	def show_window(self):
		if self.isMinimized():
			self.showNormal()
		elif not self.isActiveWindow():  # 如果窗口不是活动窗口
			self.activateWindow()  # 激活窗口
			self.raise_()  # 将窗口置于最前

	def quit_application(self):
		self.show_window()
		self.close()
        
    # 还原状态
	def restore_state(self):
		self.stateNetLabel.setText("网络环境(*)")
		self.stateNetLabel.setStyleSheet("color: black;")
		self.stateSartLeiDianLabel.setText("启动托管器(*)")
		self.stateSartLeiDianLabel.setStyleSheet("color: black;")
		self.stateWeiChatLabel.setText("微信登录(*)")
		self.stateWeiChatLabel.setStyleSheet("color: black;")
		self.stateSetObjectLabel.setText("设置托管对象(*)")
		self.stateSetObjectLabel.setStyleSheet("color: black;")
		self.stateSucessLabel.setText("正常运行(*)")
		self.stateSucessLabel.setStyleSheet("color: black;")
        
    # 设置状态
	def set_state(self, envStateType, bSucess):
		if EnvStateType.Env_Net_State == envStateType:
			if bSucess == True:
				self.stateNetLabel.setText("网络环境(√)")
				self.stateNetLabel.setStyleSheet("color: black;")
				self.stateSartLeiDianLabel.setText("启动托管器(*)")
				self.stateWeiChatLabel.setText("微信登录(*)")
				self.stateSetObjectLabel.setText("设置托管对象(*)")
				self.stateSucessLabel.setText("正常运行(*)")
			else:
				self.stateNetLabel.setText("网络环境(x)")
				self.stateNetLabel.setStyleSheet("color: red;")
		elif EnvStateType.Env_Start_Simulator_State == envStateType:
			if bSucess == True:
				self.stateSartLeiDianLabel.setText("启动托管器(√)")
				self.stateSartLeiDianLabel.setStyleSheet("color: black;")
			else:
				self.stateSartLeiDianLabel.setText("启动托管器(x)")
				self.stateSartLeiDianLabel.setStyleSheet("color: red;")
				self.stateWeiChatLabel.setText("微信登录(*)")
				self.stateSetObjectLabel.setText("设置托管对象(*)")
				self.stateSucessLabel.setText("正常运行(*)")
		elif EnvStateType.Env_WeiChat_State == envStateType:
			if bSucess == True:
				self.stateWeiChatLabel.setText("微信登录(√)")
				self.stateWeiChatLabel.setStyleSheet("color: black;")
			else:
				self.stateWeiChatLabel.setText("微信登录(x)")
				self.stateWeiChatLabel.setStyleSheet("color: red;")  
				self.stateSetObjectLabel.setText("设置托管对象(*)")
				self.stateSucessLabel.setText("正常运行(*)")                
		elif EnvStateType.Env_Set_Tuo_State == envStateType:
			if bSucess == True:
				self.stateSetObjectLabel.setText("设置托管对象(√)")
				self.stateSetObjectLabel.setStyleSheet("color: black;")
			else:
				self.stateSetObjectLabel.setText("设置托管对象(x)")
				self.stateSetObjectLabel.setStyleSheet("color: red;") 
				self.stateSetHuasuLabel.setText("设置Agent(*)") 
		elif EnvStateType.Env_Set_Hua_Su_State == envStateType:
			if bSucess == True:
				self.stateSetHuasuLabel.setText("设置Agent(√)")
				self.stateSetHuasuLabel.setStyleSheet("color: black;")
			else:
				self.stateSetHuasuLabel.setText("设置Agent(x)")
				self.stateSetHuasuLabel.setStyleSheet("color: red;") 
				self.stateSucessLabel.setText("正常运行(*)") 
		elif EnvStateType.Env_Sucess == envStateType:
			if bSucess == True:
				self.stateSucessLabel.setText("正常运行(√)")
				self.stateSucessLabel.setStyleSheet("color: black;")
			else:
				self.stateSucessLabel.setText("正常运行(x)")
				self.stateSucessLabel.setStyleSheet("color: red;")
		return
        
	def signal_recv_func(self, para):
		global g_new_msg_count
		global g_config_json_data
        
		# 判断试用是否结束
		if para == "check_lic":
			if True == is_out_of_time()[0]:
				#self.set_btn_state(ApplicationState.NoLicence)
				print_my("!!!判断到授权到期,请点击右下角“授权”按钮授权")
				#QMessageBox.information(self, APP_NAME, "试用结束，请点击右下角“授权”按钮授权", QMessageBox.Yes)   
				self.loginAndPaymentFunc()
		elif para == "lic_outdate": 
			#self.set_btn_state(ApplicationState.NoLicence)
			print_my("!!!判断到授权到期,请点击右下角“授权”按钮授权")
			#QMessageBox.information(table, APP_NAME, "试用结束，请点击右下角“授权”按钮授权", QMessageBox.Yes) 
			self.loginAndPaymentFunc()
		elif para == "lic_sucess":
			print_my("授权成功")
			table.set_btn_state(ApplicationState.Normal)
			b_outdate, delta_second = is_out_of_time()
			licenceState_str = "授权：{}".format("会员(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != 0 else "永久会员")
			self.licenceBtn.setText(licenceState_str)
		elif para == "app_ka_zhu":
			print_my("app卡住了")
			QMessageBox.information(table, APP_NAME, "环境检查不满足", QMessageBox.Yes)
		elif para == "net_error":
			self.set_state(EnvStateType.Env_Net_State, False) 
			QMessageBox.information(table, APP_NAME, "本机网络无法访问互联网", QMessageBox.Yes)
		elif para == "update_new_msg_count":
			strDiplay = "此次共收到:{}条新消息,自动回复了{}条".format(g_new_msg_count, g_new_msg_count)
			self.danCiLabel.setText(strDiplay)
		elif para == "device_not_ready":
			QMessageBox.information(self, APP_NAME, "请确保手机通过数据线连接到电脑，且开启开发者模式", QMessageBox.Yes)
		elif para == "app_not_run":
			if table.isMinimized():
				table.showNormal()
			QMessageBox.information(self, APP_NAME, "奇怪微信一直无法启动，请客服支援", QMessageBox.Yes)
			table.set_btn_state(ApplicationState.Normal)
		elif para == "remote_phone_no_connect":
			table.update_screen_img(f"{APP_IMG_DIR}\\off_line.png", "点击连接")
		elif para == "remote_phone_prepare":
			if table.isMinimized():
				table.showNormal()
			if False == hasattr(self, 'addPhone_Win') or self.addPhone_Win is None:
				phone_info = {}
				title = "添加手机对象"
				phone_info_list = g_config_json_data["PHONE_INFO_LIST"]
				# chenyj 
				if len(phone_info_list) > 0:
					phone_info = phone_info_list[0]
					title = "连接手机对象"
				self.clickCommonFun()
				print_my(f"!!!!!!远程手机无线调试还没连接，请配置连接信息")
				self.addPhone_Win = AddPhoneWindow(title, phone_info, phone_info_list, self)
				self.addPhone_Win._signal.connect(self.signal_recv_func)
				self.addPhone_Win.setWindowModality(Qt.ApplicationModal)
				self.addPhone_Win.show()
				self.addPhone_Win.exec_()
				self.addPhone_Win = None
		elif para == "env_ok":
			print_my("环境检测通过")
		elif para == "show_app":
			if table.isMinimized():
				table.showNormal()  
		elif para == "device_no_ready":
			if table.isMinimized():
				table.showNormal()  
			table.set_btn_state(ApplicationState.Normal)
			QMessageBox.information(self, APP_NAME, "请确保手机通过数据线连接到电脑，且开启开发者模式", QMessageBox.Yes)
		elif para == "screen_no_light":
            # 设置为置顶
			#if not(table.windowFlags() & Qt.WindowStaysOnTopHint):
			#	table.setWindowFlags(table.windowFlags() | Qt.WindowStaysOnTopHint)
			# 还原窗口
			if table.isMinimized():
				table.showNormal()  
			self.startBtn.setEnabled(True)
			self.stopBtn.setEnabled(False)
			if False == hasattr(self, 'b_show_no_light') or self.b_show_no_light == False:
				self.b_show_no_light = True
				print_my(f"!!!!!!远程手机没有亮屏，请确保手机亮屏")
				QMessageBox.information(self, APP_NAME, "远程手机没有亮屏，请确保手机亮屏", QMessageBox.Yes)
				self.b_show_no_light = False
			# 取消置顶
			#if table.windowFlags() & Qt.WindowStaysOnTopHint:
			#	table.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)   
		elif para == "screen_lock":
			if table.isMinimized():
				table.showNormal()  
			self.startBtn.setEnabled(True)
			self.stopBtn.setEnabled(False)
			if False == hasattr(self, 'b_show_lock') or self.b_show_lock == False:
				self.b_show_lock = True
				print_my(f"!!!!!远程手机还没解锁，请请确保手机解锁")
				QMessageBox.information(self, APP_NAME, "远程手机还没解锁，请请确保手机解锁", QMessageBox.Yes) 
				self.b_show_lock = False
		elif para == "auto_init_error":
			if table.isMinimized():
				table.showNormal() 
			QMessageBox.information(table, APP_NAME, "自动化操作初始化失败", QMessageBox.Yes) 
		elif para == "need_set_deposit":
			if table.isMinimized():
				table.showNormal() 
			QMessageBox.information(table, APP_NAME, "请先设置要托管的微信聊天对象，然后再启动", QMessageBox.Yes)  
			self.setDepositObjectBtnFun(True)
		elif para == "need_set_agent":
			if table.isMinimized():
				table.showNormal() 
			QMessageBox.information(table, APP_NAME, "请先设置Agent，然后再启动", QMessageBox.Yes)  
			self.setAgentBtnFun(True)
		elif para == "get_username_list_of_first_page_fail":
			if table.isMinimized():
				table.showNormal() 
			QMessageBox.information(table, APP_NAME, "获得可托管列对象列表失败", QMessageBox.Yes)
		elif "no_found_monitor_rect_" in para:
			self.set_state(EnvStateType.Env_Sucess, False) 
			if table.isMinimized():
				table.showNormal() 
			username = para.replace("no_found_monitor_rect_", "")
			QMessageBox.information(table, APP_NAME, "微信列表中无法找到用户【{}】".format(username), QMessageBox.Yes) 
		elif "update_screen_img_info_" in para:
			screen_img_info_dict_str = para.replace("update_screen_img_info_", "")
			screen_img_info_dict = ast.literal_eval(screen_img_info_dict_str)
			#print(f"手机新截图信息是:[{screen_img_info_dict}]")
			self.update_screen_img(screen_img_info_dict["image_path"], "", screen_img_info_dict["draw_box"])
		elif "update_click_screen_info_" in para:
			update_click_screen_info_dict_str = para.replace("update_click_screen_info_", "")
			update_click_screen_info_dict = ast.literal_eval(update_click_screen_info_dict_str)
			self.draw_red_circle_on_screen_imag(update_click_screen_info_dict["x0"], update_click_screen_info_dict["y0"])
		elif para.startswith("log_"):
			message = para.strip("log_")
			if table.rightPanelWin is not None:
				table.rightPanelWin._signal_self.emit(para) 
			else:
				self.write_log_to_windows(message)
		elif para.startswith("tooltip_"):
			message = para.strip("tooltip_")
			print_my(message)
			self.showToolTip(message)
		elif para.startswith("pair_"):
			print("Table事件收到信号:{}".format(para))
			ip, port, pairing_code = para.strip("pair_").split("_")
			thread = threading.Thread(target=self.pair_thread, args=(ip, port, pairing_code))
			thread.start()
			#iRet = adb_pair_remote_phone(ip, port, pairing_code)
			#self.pair_i_ret = iRet
		elif para.startswith("connect_"):
			print("Table事件收到信号:{}".format(para))
			ip, port = para.strip("connect_").split("_")
			thread = threading.Thread(target=self.connect_thread, args=(ip, port))
			thread.start()
			#restart_adb_server()
			#iRet = adb_connect_remote_phone(ip, port)
			#self.connect_i_ret = iRet
		elif para.startswith("login_sucess_"):	
			print("Table事件收到信号:{}".format(para))
			bind_phone = para.strip("login_sucess_")
			# 上报服务器
			iRet = http_report_login_status(bind_phone)
			if iRet != APP_RET_CODE_SUCESS:
				print_my(f"上报登录状态失败，bind_phone={bind_phone}")
				return
			g_config_json_data["BIND_PHONE"] = bind_phone
			save_config_data(g_config_json_data, g_config_path)
		elif para == "switch_account":	
			print("Table事件收到信号:{}".format(para))
			# 上报服务器
			iRet = http_report_login_status("")
			if iRet != APP_RET_CODE_SUCESS:
				print_my(f"上报登录状态失败，bind_phone={bind_phone}")
				return
			g_config_json_data["BIND_PHONE"] = ""
			save_config_data(g_config_json_data, g_config_path)
			self.Timer_for_showLogin = QTimer()
			self.Timer_for_showLogin.start(500*1)
			self.Timer_for_showLogin.timeout.connect(self.loginAndPaymentFunc)

		elif para == "me_click":	
			print("Table事件收到信号:{}".format(para))
			self.me_Win = MeWindow(g_config_json_data)
			print("111111")
			self.me_Win._signal.connect(self.signal_recv_func)
			self.me_Win.setWindowModality(Qt.ApplicationModal)
			print("22222")
			self.me_Win.show()
			print("333333")
			self.me_Win.exec_()
		elif para.startswith("deposit_username_"):
			print("Table事件收到信号:{}".format(para))
			b_auto_start_after = False 
			if "_b_auto_start_after_True" in para:
				para = para.replace("_b_auto_start_after_True", "")
				b_auto_start_after = True
			elif "_b_auto_start_after_False" in para:
				para = para.replace("_b_auto_start_after_False", "")
				b_auto_start_after = False
                
			if "username_of_can_deposit_list" in g_config_json_data:
				self.username_of_can_deposit_list = g_config_json_data["username_of_can_deposit_list"]
            
			self.set_state(EnvStateType.Env_Set_Tuo_State, True)
			usename_list_str = para.strip("deposit_username_")
            
			usename_list = ast.literal_eval(usename_list_str)
			self.username_of_deposit_list = usename_list
			g_config_json_data["info_of_deposit_list"] = [{"username":username, "b_hase_new_msg":False} for username in self.username_of_deposit_list]
			save_config_data(g_config_json_data, g_config_path) 
			if len(self.username_of_deposit_list) == 0:
				table.set_state(EnvStateType.Env_Set_Tuo_State, False)
			else:
				table.set_state(EnvStateType.Env_Set_Tuo_State, True)
			if b_auto_start_after == True and len(self.username_of_deposit_list) > 0: 
				self.startBtnFun()
		elif para.startswith("agent_"):
			print("Table事件收到信号:{}".format(para))
			agent_list_str = para.strip("agent_")
            
			agent_list = ast.literal_eval(agent_list_str)
			self.sel_agent_list = agent_list
			g_config_json_data["sel_agent_list"] = self.sel_agent_list
			save_config_data(g_config_json_data, g_config_path)       
		elif para.startswith("hua_su_file_paths_"):
			print("Table事件收到信号:{}".format(para))
			b_auto_start_after = False 
			if "_b_auto_start_after_True" in para:
				para = para.replace("_b_auto_start_after_True", "")
				b_auto_start_after = True
			elif "_b_auto_start_after_False" in para:
				para = para.replace("_b_auto_start_after_False", "")
				b_auto_start_after = False
                
			#self.set_state(EnvStateType.Env_Set_Tuo_State, True)
			file_paths_str = para.strip("hua_su_file_paths_")
            
			file_paths = ast.literal_eval(file_paths_str)
			self.hua_su_file_paths = file_paths
			g_config_json_data["HUA_SU_FILES"] = self.hua_su_file_paths
			save_config_data(g_config_json_data, g_config_path) 
			init_knowledage_str(self.hua_su_file_paths)
			if len(self.hua_su_file_paths) == 0:
				table.set_state(EnvStateType.Env_Set_Hua_Su_State, False)
			else:
				table.set_state(EnvStateType.Env_Set_Hua_Su_State, True)
			if b_auto_start_after == True and len(self.hua_su_file_paths) > 0: 
				self.startBtnFun()       
		elif para.startswith("download_finish_count_"):
			finish_count_str = para.strip("download_finish_count_")
			finish_count = int(finish_count_str) 
			self.dialog_downloading.setValue(finish_count)
		elif para == "download_sucess":
			self.dialog_downloading.close()
			QMessageBox.information(table, APP_NAME, "恭喜你,托管软件组件下载成功", QMessageBox.Yes) 
			# 重新走初始化
			self.Timer_for_Init_check = QTimer()
			self.Timer_for_Init_check.start(500*1)
			#self.Timer_for_Init_check.timeout.connect(self.WindowsInitOk)
			self.Timer_for_Init_check.timeout.connect(lambda: self.WindowsInitOk("start"))
		elif para == "download_failed":
			self.dialog_downloading.close()
			QMessageBox.information(table, APP_NAME, "托管软件初始化失败", QMessageBox.Yes) 
			print_my("!!!!程序强制退出")
			#exit(-11)
		elif para == "reload_task_list_view":
			print("Table事件收到信号:{}".format(para))
			self.reload_task_list_view()
		elif para == "reload_usergroup_list_view":
			print("Table事件收到信号:{}".format(para))
			self.reload_usergroup_list_view()
		elif para == "reload_friend_list_view":
			print("Table事件收到信号:{}".format(para))
			self.tab_widget.setCurrentIndex(1) 
			self.reload_friend_list_view() 
			# 滚动到最后一行(目前还没生效)
			self.friendTableView.viewport().update()
			self.friendTableView.setVerticalScrollMode(QTableView.ScrollPerItem)
			last_row_index = self.friendModel.index(self.friendModel.rowCount() - 1, 0)
			self.friendTableView.scrollTo(last_row_index)
		elif para == "update_logon_wechat_state":
			self.update_logon_wechat_state()
		elif para == "reload_usergroup_list_view":
			print("Table事件收到信号:{}".format(para))
			self.tab_widget.setCurrentIndex(1) 
			self.reload_usergroup_list_view() 
		elif para == "jump_to_setting_tab_coze":
			print("Table事件收到信号:{}".format(para))
			self.tab_widget.setCurrentIndex() 
			self.tab_widget_of_setting.setCurrentIndex(2) 
		elif para == "jump_to_setting_tab_llm":
			print("Table事件收到信号:{}".format(para))
			self.tab_widget.setCurrentIndex(8) 
			self.tab_widget_of_setting.setCurrentIndex(1) 
		elif para == "close_waiting_win":
			print("Table事件收到信号:{}".format(para))
			try:
			    # 关闭等待窗口
			    print("关闭等待窗口")
			    if self.waiting_Win is not None:
				    self.waiting_Win.close()
				    self.waiting_Win = None
			except Exception as e:
			    print("!!!!异常：\n{}".format(e))
		elif para == "close_payment_win":
			print("Table事件收到信号:{}".format(para))
			try:
			    # 关闭购买窗口
			    print("关闭购买窗口")
			    if True == hasattr(self, 'payment_Win') and self.payment_Win is not None:
				    self.payment_Win.close()
			except Exception as e:
			    print("!!!!异常：\n{}".format(e))
		elif para == "sync_friend_finish":
			print("Table事件收到信号:{}".format(para))
			try:
			    # 关闭等待窗口
			    print("关闭等待窗口")
			    if self.waiting_Win is not None:
				    self.waiting_Win.close()
				    self.waiting_Win = None
			except Exception as e:
			    print("!!!!异常：\n{}".format(e))
			self.tab_widget.setCurrentIndex(1) 
			self.reload_friend_list_view() 
		elif para == "sync_usergroup_finish":
			print("Table事件收到信号:{}".format(para))
			try:
			    # 关闭等待窗口
			    print("关闭等待窗口")
			    if self.waiting_Win is not None:
				    self.waiting_Win.close()
				    self.waiting_Win = None
			except Exception as e:
			    print("!!!!异常：\n{}".format(e))
			self.tab_widget.setCurrentIndex(2) 
			self.reload_usergroup_list_view() 
		elif para == "start_btn_fun":
			self.startBtnFun()
		elif para == "stop_btn_fun":
			self.stopBtnFun()
		elif para == "sync_friend":
			self.startBtnFun(b_need_sync_friend = True, b_need_sync_taggroup = False)
		elif para == "sync_taggroup":
			self.startBtnFun(b_need_sync_friend = False, b_need_sync_taggroup = True)
		elif para.startswith("add_friend_dict_"):
			print("Table事件收到信号:{}".format(para))
	
			add_friend_data_dict = para.strip("add_friend_dict_")
			try:
				add_friend_data_dict = json.loads(add_friend_data_dict)
				print(add_friend_data_dict)

				task_info_list = g_config_json_data["TASK_INFO_LIST"]
				task_info_add = {}
				task_info_add["task_type"] = "批量加好友"
				task_info_add["task_distribe"] = "以好友列表文件方式添加好友"
				task_info_add["task_process"] = "0"
				#task_info_add["task_data"] = {"file_paths":file_paths}
				task_info_add["task_data"] = add_friend_data_dict
				task_info_add["task_detail_data"] = get_task_detail_data(task_info_add)
				task_info_add["task_finish_detail_data"] = []
				task_info_list.append(task_info_add)
				g_config_json_data["TASK_INFO_LIST"] = task_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_task_list_view()   

			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		elif para.startswith("send_circle_dict_"):
			print("Table事件收到信号:{}".format(para))
			circle_data_dict_str = para.strip("send_circle_dict_")
			try:
				circle_data_dict = json.loads(circle_data_dict_str)
				print(circle_data_dict)
				task_info_list = g_config_json_data["TASK_INFO_LIST"]
				task_info_add = {}
				task_info_add["task_type"] = "定时发朋友圈"
				task_info_add["task_distribe"] = "定时发朋友朋友圈\nsdlfja fasfasffaskfjaskfjalksdjfsadf"
				task_info_add["task_process"] = "0"
				task_info_add["task_data"] = circle_data_dict
				task_info_add["task_detail_data"] = []
				task_info_add["task_finish_detail_data"] = []
				task_info_list.append(task_info_add)
				g_config_json_data["TASK_INFO_LIST"] = task_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_task_list_view() 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		elif para.startswith("add_agent_dict_"):
			print("Table事件收到add_agent_dict_信号:")
			add_agent_data_dict_str = para.strip("add_agent_dict_")
			try:
				add_agent_data_dict = json.loads(add_agent_data_dict_str)
				print(add_agent_data_dict)
				agent_info_list = g_config_json_data["AGENT_INFO_LIST"]
                # 编辑模式
				if "agent_name_orig" in add_agent_data_dict and len(add_agent_data_dict["agent_name_orig"]) > 0:
					for i, agent_info in enumerate(agent_info_list):
						if agent_info["agent_name"] == add_agent_data_dict["agent_name_orig"]:
							agent_info_list[i] = add_agent_data_dict
							# 删除智能体相关的旧的任务
							task_info_list = g_config_json_data["TASK_INFO_LIST"]
							task_info_list_new = []
							for task_info in task_info_list:
								if "task_source" in task_info:
									if agent_info["agent_name"] == task_info["task_source"].strip("智能体_"):
										continue 
								task_info_list_new.append(task_info)
       						# 创建任务
							task_info_list_of_agent = add_agent_data_dict["task_info_list_of_agent"]
							task_info_list_new.extend(task_info_list_of_agent)
							g_config_json_data["TASK_INFO_LIST"] = task_info_list_new
							save_config_data(g_config_json_data, g_config_path) 
							break
				# 添加模式
				else:
					agent_info_list.append(add_agent_data_dict)
					# 创建任务
					task_info_list_of_agent = add_agent_data_dict["task_info_list_of_agent"]
					task_info_list = g_config_json_data["TASK_INFO_LIST"]
					task_info_list.extend(task_info_list_of_agent)
					g_config_json_data["TASK_INFO_LIST"] = task_info_list
					save_config_data(g_config_json_data, g_config_path) 
                    
				g_config_json_data["AGENT_INFO_LIST"] = agent_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_agent_list_view() 
				self.reload_task_list_view()
                
 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		elif para.startswith("add_coze_agent_dict_"):
			print("Table事件收到add_coze_agent_dict_信号:")
			add_coze_agent_data_dict_str = para.strip("add_coze_agent_dict_")
			try:
				add_coze_agent_data_dict = json.loads(add_coze_agent_data_dict_str)
				print(add_coze_agent_data_dict)
				coze_agent_info_list = g_config_json_data["COZE_AGENT_INFO_LIST"]
                # 编辑模式
				if "agent_name_orig" in add_coze_agent_data_dict and len(add_coze_agent_data_dict["agent_name_orig"]) > 0:
					for i, agent_info in enumerate(coze_agent_info_list):
						if agent_info["agent_name"] == add_coze_agent_data_dict["agent_name_orig"]:
							coze_agent_info_list[i] = add_coze_agent_data_dict
							break
				# 添加模式
				else:
					coze_agent_info_list.append(add_coze_agent_data_dict)
                    
				g_config_json_data["COZE_AGENT_INFO_LIST"] = coze_agent_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_coze_agent_list_view() 
                
 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		elif para.startswith("add_phone_info_dict_"):
			print("Table事件收到add_phone_info_dict_信号:")
			add_phone_info_dict_str = para.strip("add_phone_info_dict_")
			try:
				add_phone_info_dict = json.loads(add_phone_info_dict_str)
				print(add_phone_info_dict)
				phone_info_list = g_config_json_data["PHONE_INFO_LIST"]
                # 编辑模式
				if "phone_name_orig" in add_phone_info_dict and len(add_phone_info_dict["phone_name_orig"]) > 0:
					for i, phone_info in enumerate(phone_info_list):
						if phone_info["phone_name"] == add_phone_info_dict["phone_name_orig"]:
							phone_info_list[i] = add_phone_info_dict
							break
				# 添加模式
				else:
					phone_info_list.append(add_phone_info_dict)
                    
				g_config_json_data["PHONE_INFO_LIST"] = phone_info_list
				save_config_data(g_config_json_data, g_config_path) 
				#self.reload_coze_agent_list_view() 
                
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")  
		elif para.startswith("add_autoadd_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_autoadd_data_dict_str = para.strip("add_autoadd_dict_")
			try:
				add_autoadd_data_dict = json.loads(add_autoadd_data_dict_str)
				print(add_autoadd_data_dict)
				autoadd_info_list = g_config_json_data["AUTOADD_INFO_LIST"]
                # 编辑模式
				if "autoadd_name_orig" in add_autoadd_data_dict and len(add_autoadd_data_dict["autoadd_name_orig"]) > 0:
					for i, autoadd_info in enumerate(autoadd_info_list):
						if autoadd_info["autoadd_name"] == add_autoadd_data_dict["autoadd_name_orig"]:
							autoadd_info_list[i] = add_autoadd_data_dict
							break
				# 添加模式
				else:
					autoadd_info_list.append(add_autoadd_data_dict)
					# 创建任务
					task_info_list_of_autoadd = add_autoadd_data_dict["task_info_list_of_autoadd"]
					task_info_list = g_config_json_data["TASK_INFO_LIST"]
					task_info_list.extend(task_info_list_of_autoadd)
					g_config_json_data["TASK_INFO_LIST"] = task_info_list
					save_config_data(g_config_json_data, g_config_path) 
                    
				g_config_json_data["AUTOADD_INFO_LIST"] = autoadd_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_autoadd_list_view() 
				self.reload_task_list_view()
                
 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		elif para.startswith("add_autopass_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_autopass_data_dict_str = para.strip("add_autopass_dict_")
			try:
				add_autopass_data_dict = json.loads(add_autopass_data_dict_str)
				print(add_autopass_data_dict)
				autopass_info_list = g_config_json_data["AUTOPASS_INFO_LIST"]
                # 编辑模式
				if "autopass_name_orig" in add_autopass_data_dict and len(add_autopass_data_dict["autopass_name_orig"]) > 0:
					for i, autopass_info in enumerate(autopass_info_list):
						if autopass_info["autopass_name"] == add_autopass_data_dict["autopass_name_orig"]:
							autopass_info_list[i] = add_autopass_data_dict
							break
				# 添加模式
				else:
					autopass_info_list.append(add_autopass_data_dict)
                    
				g_config_json_data["AUTOPASS_INFO_LIST"] = autopass_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_autopass_list_view()                
 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		elif para.startswith("add_usergroup_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_usergroup_data_dict_str = para.strip("add_usergroup_dict_")
			try:
				add_usergroup_data_dict = json.loads(add_usergroup_data_dict_str)
				print(add_usergroup_data_dict)
				usergroup_info_list = g_config_json_data["USERGROUP_INFO_LIST"]
                # 编辑模式
				if "usergroup_name_orig" in add_usergroup_data_dict and len(add_usergroup_data_dict["usergroup_name_orig"]) > 0:
					for i, usergroup_info in enumerate(usergroup_info_list):
						if usergroup_info["usergroup_name"] == add_usergroup_data_dict["usergroup_name_orig"]:
							usergroup_info_list[i] = add_usergroup_data_dict
							break
				# 添加模式
				else:
					usergroup_info_list.append(add_usergroup_data_dict)
				g_config_json_data["USERGROUP_INFO_LIST"] = usergroup_info_list
				# 检测用户组里是不是有手动添加的用户，有的话要更新到好友列表中  
				self.update_friend_data_from_usergroup_data()
				self.update_lv_cheng_group_data()
				
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_usergroup_list_view() 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")     
		elif para.startswith("add_product_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_product_data_dict_str = para.strip("add_product_dict_")
			try:
				add_product_data_dict = json.loads(add_product_data_dict_str)
				print(add_product_data_dict)
				product_info_list = g_config_json_data["PRODUCT_INFO_LIST"]
                # 编辑模式
				if "product_name_orig" in add_product_data_dict and len(add_product_data_dict["product_name_orig"]) > 0:
					for i, product_info in enumerate(product_info_list):
						if product_info["product_name"] == add_product_data_dict["product_name_orig"]:
							product_info_list[i] = add_product_data_dict
							break
				# 添加模式
				else:
					product_info_list.append(add_product_data_dict)
				g_config_json_data["PRODUCT_INFO_LIST"] = product_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_product_list_view() 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")   
		elif para.startswith("add_autoreply_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_autoreply_data_dict_str = para.strip("add_autoreply_dict_")
			try:
				add_autoreply_data_dict = json.loads(add_autoreply_data_dict_str)
				print(add_autoreply_data_dict)
				autoreply_info_list = g_config_json_data["AUTOREPLY_INFO_LIST"]
                # 编辑模式
				if "autoreply_name_orig" in add_autoreply_data_dict and len(add_autoreply_data_dict["autoreply_name_orig"]) > 0:
					for i, autoreply_info in enumerate(autoreply_info_list):
						if autoreply_info["autoreply_name"] == add_autoreply_data_dict["autoreply_name_orig"]:
							autoreply_info_list[i] = add_autoreply_data_dict
							break
				# 添加模式
				else:
					autoreply_info_list.append(add_autoreply_data_dict)
				g_config_json_data["AUTOREPLY_INFO_LIST"] = autoreply_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_autoreply_list_view() 

			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")                        
		elif para.startswith("add_content_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_content_data_dict_str = para.strip("add_content_dict_")
			try:
				add_content_data_dict = json.loads(add_content_data_dict_str)
				print(add_content_data_dict)
				content_info_list = g_config_json_data["CONTENT_INFO_LIST"]
                # 编辑模式
				if "content_name_orig" in add_content_data_dict and len(add_content_data_dict["content_name_orig"]) > 0:
					for i, content_info in enumerate(content_info_list):
						if content_info["content_name"] == add_content_data_dict["content_name_orig"]:
							content_info_list[i] = add_content_data_dict
							break
				# 添加模式
				else:
					content_info_list.append(add_content_data_dict)
				g_config_json_data["CONTENT_INFO_LIST"] = content_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_content_list_view() 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")   
		elif para.startswith("add_llm_info_dict_"):
			print("Table事件收到信号:{}".format(para))
			add_llm_info_dict_str = para.strip("add_llm_info_dict_")
			try:
				add_llm_info_dict = json.loads(add_llm_info_dict_str)
				print(add_llm_info_dict)
				llm_info_list = g_config_json_data["LLM_INFO_LIST"]
                # 编辑模式
				if "llm_type_name_orig" in add_llm_info_dict and len(add_llm_info_dict["llm_type_name_orig"]) > 0:
					for i, llm_info in enumerate(llm_info_list):
						if llm_info["llm_type_name"] == add_llm_info_dict["llm_type_name_orig"]:
							llm_info_list[i] = add_llm_info_dict
							break
				# 添加模式
				else:
					llm_info_list.append(add_llm_info_dict)
                    
				g_config_json_data["LLM_INFO_LIST"] = llm_info_list
				save_config_data(g_config_json_data, g_config_path) 
				self.reload_llm_list_view()                
 
			except json.JSONDecodeError as e:
				print(f"json解析错误：{e}")
		return
    
	def reload_task_list_view(self):
		task_info_list =  g_config_json_data["TASK_INFO_LIST"]
		# 将任务按执行时间排序
		def get_time(item):
			return item['task_data']["date"]+item['task_data']["time"]

		# 使用sorted函数对列表进行排序
		task_info_list = sorted(task_info_list, key=get_time)
		g_config_json_data["TASK_INFO_LIST"] = task_info_list
		save_config_data(g_config_json_data, g_config_path) 
            
		self.taskModel.clear()
		self.taskModel.setHorizontalHeaderLabels(['任务类型', '计划执行时间', '任务状态', '任务来源',  '触达客户组', '操作', '操作'])
        
		for i, task_info in enumerate(task_info_list):
			task_type = task_info["task_type"]
			task_source = ""
			if "task_source" in task_info:
				task_source = task_info["task_source"]
			#task_distribe = task_info["task_distribe"]
			task_data = task_info["task_data"]
			task_distribe = ""
			if "date" in task_data and "time" in task_data:
				task_distribe = "{}{}".format(task_data["date"], task_data["time"])
			task_state = "等待执行"
			task_process = task_info["task_process"] + "%"
			if task_info["task_process"] == "100":
				task_state = "已完成"
			elif task_info["task_process"] == "-1":
				task_state = "已过期"
			elif task_info["task_process"] == "0":
				task_state = "等待执行"
			else:
				task_state = "执行中(已完成{})".format(task_process)
   
			usergroup_name_of_can_see = ""
			if "task_data" in task_info:
				task_data = task_info["task_data"]
				if "usergroup_name_of_can_see" in task_data:
					usergroup_name_of_can_see = task_data["usergroup_name_of_can_see"]
     
			item0_0 = QStandardItem(task_type)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.taskModel.setItem(i, 0, item0_0)
			self.taskModel.setItem(i, 1, QStandardItem(task_distribe))
			#self.taskModel.setItem(i, 2, QStandardItem(task_process))
			self.taskModel.setItem(i, 2, QStandardItem(task_state))
			self.taskModel.setItem(i, 3, QStandardItem(task_source))
			self.taskModel.setItem(i, 4, QStandardItem(usergroup_name_of_can_see))
			self.taskModel.setItem(i, 5, QStandardItem("删除"))
			self.taskModel.setItem(i, 6, QStandardItem("详情"))
		return 
             
	def taskTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.taskTable_click_last_time < 2:
			return
		self.taskTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 5:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了任务列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			task_info_list = g_config_json_data["TASK_INFO_LIST"]
			del task_info_list[row]  
			g_config_json_data["TASK_INFO_LIST"] = task_info_list
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_task_list_view()
		elif column == 6:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了任务列表中的第{row}行的查看按钮")
   			
			task_info_list = g_config_json_data["TASK_INFO_LIST"]
			task_info = task_info_list[row]  
   
			if task_info["task_type"] not in ["批量加好友"]:
				print("暂时还不支持这种任务类型的查看操作")
				return
			viewTask_Win = ViewTaskWindow("查看任务信息", task_info, self)
			viewTask_Win._signal.connect(self.signal_recv_func)
			viewTask_Win.setWindowModality(Qt.ApplicationModal)
			viewTask_Win.show()
			viewTask_Win.exec_()
		return  

	# 检测用户组里是不是有手动添加的用户，有的话要更新到好友列表中  
	def update_friend_data_from_usergroup_data(self):
		usergroup_info_list = g_config_json_data["USERGROUP_INFO_LIST"]
		friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]
		friend_name_list = [friend_info["friend_name"] for friend_info in friend_info_list]
		for usergroup_info in usergroup_info_list:
			for username in usergroup_info["usergroup_member"]:
				if username not in friend_name_list:
					friend_info = {}
					friend_info["friend_name"] = username
					current_datetime = datetime.now()
					date_str = current_datetime.strftime("%Y-%m-%d")
					friend_info["add_date"] = date_str
					friend_info["friend_remark"] = ""
					friend_info_list.append(friend_info)
		g_config_json_data["FRIEND_INFO_LIST"] = friend_info_list
                
	def reload_product_list_view(self):
		product_info_list =  g_config_json_data["PRODUCT_INFO_LIST"]
		"""
		# 将任务按执行时间排序
		def get_time(item):
			return item['task_data']["date"]+item['task_data']["time"]

		# 使用sorted函数对列表进行排序
		product_info_list = sorted(product_info_list, key=get_time)
		g_config_json_data["PRODUCT_INFO_LIST"] = product_info_list
		save_config_data(g_config_json_data, g_config_path) 
        """
        
		self.productModel.clear()
		self.productModel.setHorizontalHeaderLabels(['产品名称', '产品的介绍', '产品的官网', '产品相关文档', '操作', '操作'])
        
		for i, product_info in enumerate(product_info_list):
			product_name = product_info["product_name"]
			product_summary = product_info["product_summary"]
			product_website = product_info["product_website"]
			product_docs = "、".join(product_info["product_docs"])
            
			item0_0 = QStandardItem(product_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.productModel.setItem(i, 0, item0_0)
			self.productModel.setItem(i, 1, QStandardItem(product_summary))
			self.productModel.setItem(i, 2, QStandardItem(product_website))
			self.productModel.setItem(i, 3, QStandardItem(product_docs))
			self.productModel.setItem(i, 4, QStandardItem("删除"))
			self.productModel.setItem(i, 5, QStandardItem("编辑"))
		
		return 
             
	def productTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.productTable_click_last_time < 2:
			return
		self.productTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了产品列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			product_info_list = g_config_json_data["PRODUCT_INFO_LIST"]
			del product_info_list[row]  
			g_config_json_data["PRODUCT_INFO_LIST"] = product_info_list
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_product_list_view()
		elif column == 5:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了产品列表中的第{row}行的编辑按钮")
			product_info_list = g_config_json_data["PRODUCT_INFO_LIST"]
			product_info = product_info_list[row]  
			
			self.addProduct_Win = AddProductWindow('编辑产品', product_info["product_name"], product_info["product_summary"], product_info["product_website"], product_info["product_docs"], product_info_list, self)
			self.addProduct_Win._signal.connect(self.signal_recv_func)
			self.addProduct_Win.setWindowModality(Qt.ApplicationModal)
			self.addProduct_Win.show()
			self.addProduct_Win.exec_()
        
            #g_config_json_data["PRODUCT_INFO_LIST"] = product_info_list
			#save_config_data(g_config_json_data, g_config_path) 
			#self.reload_product_list_view()
		return  

	def reload_friend_list_view(self):
		friend_info_list =  g_config_json_data["FRIEND_INFO_LIST"]

		self.friend_info_list_of_show.clear()
		self.friendModel.clear()
		self.friendModel.setHorizontalHeaderLabels(['好友昵称', '添加时间', '好友近况说明', '操作', '操作'])
        
		for i, friend_info in enumerate(friend_info_list):
			self.friend_info_list_of_show.append(friend_info)
       
			friend_name = friend_info["friend_name"]
			add_date_str = ""
			if "add_date" in friend_info:
				add_date_str = friend_info["add_date"]
			friend_remark = friend_info["friend_remark"]
            
			item0_0 = QStandardItem(friend_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.friendModel.setItem(i, 0, item0_0)
			self.friendModel.setItem(i, 1, QStandardItem(add_date_str))
			self.friendModel.setItem(i, 2, QStandardItem(friend_remark))
			self.friendModel.setItem(i, 3, QStandardItem("删除"))
			self.friendModel.setItem(i, 4, QStandardItem("编辑"))
		return 

	def filter_friend_list(self, keyword):
		friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]

		self.friend_info_list_of_show.clear()
		self.friendModel.clear()
		self.friendModel.setHorizontalHeaderLabels(['好友昵称', '添加时间', '好友近况说明', '操作', '操作'])
		i_count = 0
		for i, friend_info in enumerate(friend_info_list):
			friend_name = friend_info["friend_name"]
			if keyword.lower() in friend_name.lower():
				self.friend_info_list_of_show.append(friend_info)
    
				friend_remark = friend_info["friend_remark"]
				add_date_str = ""
				if "add_date" in friend_info:
					add_date_str = friend_info["add_date"]
				
				item0_0 = QStandardItem(friend_name)
				item0_0.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
				self.friendModel.setItem(i_count, 0, item0_0)
				self.friendModel.setItem(i_count, 1, QStandardItem(add_date_str))
				self.friendModel.setItem(i_count, 2, QStandardItem(friend_remark))
				self.friendModel.setItem(i_count, 3, QStandardItem("删除"))
				self.friendModel.setItem(i_count, 4, QStandardItem("编辑"))
				i_count += 1



	def update_lv_cheng_group_data(self):
		friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]
		usergroup_info_list = g_config_json_data["USERGROUP_INFO_LIST"]
		for usergroup_info in usergroup_info_list:
			if "add_model_name" not in usergroup_info:
				continue
			if usergroup_info["add_model_name"] == "根据时间规则创建":
				if "rule_info_list" not in usergroup_info:
					continue
				rule_info_list = usergroup_info["rule_info_list"]
				#rule_info_list = LV_CHENG_INFO_LIST[lv_cheng_name]
				usergroup_member = []
				for rule_info in rule_info_list:
					if "DAYS_AFTER_ADD" in rule_info:
						start_day = rule_info["DAYS_AFTER_ADD"]["START_DAY"]
						end_day = rule_info["DAYS_AFTER_ADD"]["END_DAY"]

						for friend_info in friend_info_list:
							if "add_date" not in friend_info:
								continue
							add_date_str = friend_info["add_date"]
							if len(add_date_str) == 0:
								continue
							add_date = datetime.strptime(add_date_str, "%Y-%m-%d")
							current_date = datetime.now()
							date_diff = current_date - add_date
							print("==========friend_info：{}, date_diff.days：{}".format(friend_info, date_diff.days))
							if float(date_diff.days) <= float(end_day) and float(date_diff.days) >= float(start_day):
								usergroup_member.append(friend_info["friend_name"])
			elif usergroup_info["add_model_name"] == "根据昵称规则创建":
				if "rule_info_list" not in usergroup_info:
					continue
				rule_info_list = usergroup_info["rule_info_list"]
				#rule_info_list = LV_CHENG_INFO_LIST[lv_cheng_name]
				usergroup_member = []
				for rule_info in rule_info_list:
					if "USERNAME" in rule_info:
						# 规则1：以XX为前缀
						front_str = rule_info["USERNAME"].get("FRONT_STR", "")
						if len(front_str) > 0:
							for friend_info in friend_info_list:
								if "friend_name" not in friend_info:
									continue
								friend_name = friend_info["friend_name"]
								if len(friend_name) == 0:
									continue
								if friend_name.startswith(front_str) and friend_name not in usergroup_member:
									usergroup_member.append(friend_name)
						# 规则2：包含XX
						contain_str = rule_info["USERNAME"].get("CONTAIN_STR", "")
						if len(contain_str) > 0:
							for friend_info in friend_info_list:
								if "friend_name" not in friend_info:
									continue
								friend_name = friend_info["friend_name"]
								if len(friend_name) == 0:
									continue
								if contain_str in friend_name and friend_name not in usergroup_member:
									usergroup_member.append(friend_info["friend_name"])
				usergroup_info["usergroup_member"] = usergroup_member	

		"""
		for lv_cheng_name in LV_CHENG_INFO_LIST:
			if lv_cheng_name == "系统内置旅程_新客户":
				days_after_add = LV_CHENG_INFO_LIST[lv_cheng_name]["days_after_add"]
				usergroup_info_of_lv_cheng = {}
				for usergroup_info in usergroup_info_list:
					if usergroup_info["usergroup_name"] == lv_cheng_name:
						usergroup_info_of_lv_cheng = usergroup_info
						break 
				if usergroup_info_of_lv_cheng:
					usergroup_member = []
					for friend_info in friend_info_list:
						if "add_date" not in friend_info:
							continue
						add_date_str = friend_info["add_date"]
						add_date = datetime.strptime(add_date_str, "%Y-%m-%d")
						current_date = datetime.now()
						date_diff = current_date - add_date
						if float(date_diff.days) < float(days_after_add):
							usergroup_member.append(friend_info["friend_name"])
						#if friend_info["add_time"] in LV_CHENG_INFO_LIST[lv_cheng_name]:
						pass
					usergroup_info_of_lv_cheng["usergroup_member"] = usergroup_member	
		"""				 
		save_config_data(g_config_json_data, g_config_path)
 
	def reload_usergroup_list_view(self):
		usergroup_info_list =  g_config_json_data["USERGROUP_INFO_LIST"]

		self.usergroupModel.clear()
		self.usergroupModel.setHorizontalHeaderLabels(['客户组名称', '成员', '成员个数', '操作', '操作'])
        
		for i, usergroup_info in enumerate(usergroup_info_list):
			usergroup_name = usergroup_info["usergroup_name"]
			usergroup_member = "、".join(usergroup_info["usergroup_member"])
			member_count = str(len(usergroup_info["usergroup_member"]))
            
			item0_0 = QStandardItem(usergroup_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.usergroupModel.setItem(i, 0, item0_0)
			self.usergroupModel.setItem(i, 1, QStandardItem(usergroup_member))
			self.usergroupModel.setItem(i, 2, QStandardItem(member_count))
			self.usergroupModel.setItem(i, 3, QStandardItem("删除"))
			self.usergroupModel.setItem(i, 4, QStandardItem("编辑"))
		return 

	def reload_content_list_view(self):
		content_info_list =  g_config_json_data["CONTENT_INFO_LIST"]

		self.contentModel.clear()
		self.contentModel.setHorizontalHeaderLabels(['文案名称', '相关产品', '场景', '条数', '操作', '操作'])
        
		for i, content_info in enumerate(content_info_list):
			content_name = content_info["content_name"]
			content_product_name = content_info["content_product_name"]
			content_scene_type = content_info["content_scene_type"]
			content_data_list = content_info["content_data_list"]
            
			item0_0 = QStandardItem(content_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.contentModel.setItem(i, 0, item0_0)
			self.contentModel.setItem(i, 1, QStandardItem(content_product_name))
			self.contentModel.setItem(i, 2, QStandardItem(content_scene_type))
			self.contentModel.setItem(i, 3, QStandardItem(str(len(content_data_list))))
			self.contentModel.setItem(i, 4, QStandardItem("删除"))
			self.contentModel.setItem(i, 5, QStandardItem("编辑"))
		return 
    
	def reload_agent_list_view(self):
		agent_info_list =  g_config_json_data["AGENT_INFO_LIST"]

		self.agentModel.clear()
		self.agentModel.setHorizontalHeaderLabels(['智能体名称', '智能体类型', '关联产品', '触达方式', '负责客户组', '操作', '操作'])
        
		for i, agent_info in enumerate(agent_info_list):
			agent_name = agent_info["agent_name"]
			agent_type = agent_info["agent_type"]
			agent_product_name = agent_info["agent_product_name"]
			agent_touch_type = agent_info["agent_touch_type"]
			usergroup_name = agent_info["agent_touch_object"]
            
			item0_0 = QStandardItem(agent_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.agentModel.setItem(i, 0, item0_0)
			self.agentModel.setItem(i, 1, QStandardItem(agent_type))
			self.agentModel.setItem(i, 2, QStandardItem(agent_product_name))
			self.agentModel.setItem(i, 3, QStandardItem(agent_touch_type))
			self.agentModel.setItem(i, 4, QStandardItem(usergroup_name))
			self.agentModel.setItem(i, 5, QStandardItem("删除"))
			self.agentModel.setItem(i, 6, QStandardItem("编辑"))
		return

	def reload_autoreply_list_view(self):
		autoreply_info_list =  g_config_json_data["AUTOREPLY_INFO_LIST"]

		self.autoReplyModel.clear()
		self.autoReplyModel.setHorizontalHeaderLabels(['机器人名称', '负责客户组', '话术库', '操作', '操作'])
        
		for i, autoreply_info in enumerate(autoreply_info_list):
			autoreply_name = autoreply_info["autoreply_name"]
			response_usergroupname = autoreply_info["response_usergroupname"]
			hua_su_file_paths = "、".join(autoreply_info["hua_su_file_paths"])
            
			item0_0 = QStandardItem(autoreply_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.autoReplyModel.setItem(i, 0, item0_0)
			self.autoReplyModel.setItem(i, 1, QStandardItem(response_usergroupname))
			self.autoReplyModel.setItem(i, 2, QStandardItem(hua_su_file_paths))
			self.autoReplyModel.setItem(i, 3, QStandardItem("删除"))
			self.autoReplyModel.setItem(i, 4, QStandardItem("编辑"))
		return 

	def reload_autoadd_list_view(self):
		autoadd_info_list =  g_config_json_data["AUTOADD_INFO_LIST"]

		self.autoAddModel.clear()
		self.autoAddModel.setHorizontalHeaderLabels(['机器人名称', '待添加微信号', '操作', '操作'])
        
		for i, autoadd_info in enumerate(autoadd_info_list):
			autoadd_name = autoadd_info["autoadd_name"]
			
			if "group_add_rule_info" in autoadd_info and len(autoadd_info["group_add_rule_info"]) > 0:
				autoadd_name = "微信群_" + autoadd_name
				will_add_friend_list = autoadd_info["group_add_rule_info"]["GROUP_NAME"]
			else:
				autoadd_name = "批量账号_" + autoadd_name
				will_add_friend_list = "、".join(autoadd_info["willing_add_count_list"])
    			       
			item0_0 = QStandardItem(autoadd_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.autoAddModel.setItem(i, 0, item0_0)
			self.autoAddModel.setItem(i, 1, QStandardItem(will_add_friend_list))
			self.autoAddModel.setItem(i, 2, QStandardItem("删除"))
			self.autoAddModel.setItem(i, 3, QStandardItem("编辑"))

	def reload_autopass_list_view(self):
		autopass_info_list =  g_config_json_data["AUTOPASS_INFO_LIST"]

		self.autoPassModel.clear()
		self.autoPassModel.setHorizontalHeaderLabels(['机器人名称', '好友备注前缀', '操作', '操作'])
        
		for i, autopass_info in enumerate(autopass_info_list):
			autopass_name = autopass_info["autopass_name"]
			remark_prefix = autopass_info["remark_prefix"]
			item0_0 = QStandardItem(autopass_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.autoPassModel.setItem(i, 0, item0_0)
			self.autoPassModel.setItem(i, 1, QStandardItem(remark_prefix))
			self.autoPassModel.setItem(i, 2, QStandardItem("删除"))
			self.autoPassModel.setItem(i, 3, QStandardItem("编辑"))
		return 

	def reload_llm_list_view(self):
		llm_info_list =  g_config_json_data["LLM_INFO_LIST"]

		self.llmModel.clear()
		self.llmModel.setHorizontalHeaderLabels(['大模型名称', 'key', '调用模型名称', '操作', '操作'])
 
		for i, llm_info in enumerate(llm_info_list):
			llm_type_name = llm_info["llm_type_name"]
			model_name = llm_info["model_name"]
			key = llm_info["key"]
            
			item0_0 = QStandardItem(llm_type_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.llmModel.setItem(i, 0, item0_0)
			self.llmModel.setItem(i, 1, QStandardItem(key))
			self.llmModel.setItem(i, 2, QStandardItem(model_name))
			self.llmModel.setItem(i, 3, QStandardItem("删除"))
			if key == G_KEY_DEFAULT:
				self.llmModel.setItem(i, 4, QStandardItem("使用自己的key"))
			else:
				self.llmModel.setItem(i, 4, QStandardItem("修改key"))
		return
 
	def reload_coze_agent_list_view(self):
		coze_agent_info_list =  g_config_json_data["COZE_AGENT_INFO_LIST"]

		self.cozeAgentModel.clear()
		self.cozeAgentModel.setHorizontalHeaderLabels(['智能体名称', 'BOT_ID', 'API_TOKEN', '操作', '操作'])
        
		for i, agent_info in enumerate(coze_agent_info_list):
			agent_name = agent_info["agent_name"]
			bot_id = agent_info["bot_id"]
			api_token = agent_info["api_token"]
            
			item0_0 = QStandardItem(agent_name)
			item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.cozeAgentModel.setItem(i, 0, item0_0)
			self.cozeAgentModel.setItem(i, 1, QStandardItem(bot_id))
			self.cozeAgentModel.setItem(i, 2, QStandardItem(api_token))
			self.cozeAgentModel.setItem(i, 3, QStandardItem("删除"))
			self.cozeAgentModel.setItem(i, 4, QStandardItem("编辑"))
		return

	def friendTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.friendTable_click_last_time < 2:
			return
		self.friendTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了好友列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
      
			friend_info_sel = self.friend_info_list_of_show[row]
		    
      
			friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]
			position = next((i for i, item in enumerate(friend_info_list) if item["friend_name"] == friend_info_sel["friend_name"]), None)
			del friend_info_list[position]  
			g_config_json_data["FRIEND_INFO_LIST"] = friend_info_list
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_friend_list_view()
		elif column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了好友列表中的第{row}行的编辑按钮")
			friend_info_list = g_config_json_data["FRIEND_INFO_LIST"]
			friend_info = friend_info_list[row]  
			"""
			editFriend_Win = AddUserGroupWindow("编辑好友", usergroup_info["usergroup_name"], self.username_of_can_deposit_list, usergroup_info["usergroup_member"], usergroup_info_list, self)
			editFriend_Win._signal.connect(self.signal_recv_func)
			editFriend_Win.setWindowModality(Qt.ApplicationModal)
			editFriend_Win.show()
			editFriend_Win.exec_()
			"""
		return 
        
	def usergroupTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.usergroupTable_click_last_time < 2:
			return
		self.usergroupTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了客户组列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 

			usergroup_info_list = g_config_json_data["USERGROUP_INFO_LIST"]
			#if usergroup_info_list[row]["usergroup_name"] in [lv_cheng_name for lv_cheng_name in LV_CHENG_INFO_LIST]:
			#	QMessageBox.information(self, APP_NAME, "禁止删除系统内置旅程客户组", QMessageBox.Yes)
			#	return
            # 确保此用户组没被其他对象关联 
			if usergroup_info_list[row]["usergroup_name"] in [agent_info["agent_touch_object"] for agent_info in g_config_json_data["AGENT_INFO_LIST"]]:
				QMessageBox.information(self, APP_NAME, "此用户组有关联“智能体“，请先解绑再进行删除操作", QMessageBox.Yes)
				return
			if usergroup_info_list[row]["usergroup_name"] in [autoreply_info["response_usergroupname"] for autoreply_info in g_config_json_data["AUTOREPLY_INFO_LIST"]]:
				QMessageBox.information(self, APP_NAME, "此用户组有关联“自动客服机器人”，请先解绑再进行删除操作", QMessageBox.Yes)
				return
            
			del usergroup_info_list[row]  
			g_config_json_data["USERGROUP_INFO_LIST"] = usergroup_info_list
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_usergroup_list_view()
		elif column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了客户组列表中的第{row}行的编辑按钮")
			usergroup_info_list = g_config_json_data["USERGROUP_INFO_LIST"]
			usergroup_info = usergroup_info_list[row]  
			#if usergroup_info["usergroup_name"] in [lv_cheng_name for lv_cheng_name in LV_CHENG_INFO_LIST]:
			#	QMessageBox.information(self, APP_NAME, "不可编辑系统内置旅程客户组", QMessageBox.Yes)
			#	return
			if "add_model_name" not in usergroup_info:
				usergroup_info["add_model_name"] = ""
			if "rule_info_list" not in usergroup_info:
				usergroup_info["rule_info_list"] = []
    
			editUserGroup_Win = AddUserGroupWindow("编辑客户组", usergroup_info["usergroup_name"], usergroup_info["add_model_name"], usergroup_info["rule_info_list"], g_config_json_data["FRIEND_INFO_LIST"], usergroup_info["usergroup_member"], usergroup_info_list, self)
			editUserGroup_Win._signal.connect(self.signal_recv_func)
			editUserGroup_Win.setWindowModality(Qt.ApplicationModal)
			editUserGroup_Win.show()
			editUserGroup_Win.exec_()
		return 

	def contentTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.contentTable_click_last_time < 2:
			return
		self.contentTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
		if column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了内容列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			content_info_list = g_config_json_data["CONTENT_INFO_LIST"]
			del content_info_list[row]  
			g_config_json_data["CONTENT_INFO_LIST"] = content_info_list
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_content_list_view()
		elif column == 5:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了内容列表中的第{row}行的编辑按钮")
			content_info_list = g_config_json_data["CONTENT_INFO_LIST"]
			content_info = content_info_list[row]
			editContent_Win = AddContentWindow("编辑内容", content_info["content_name"], content_info["content_product_name"], content_info["content_scene_type"], content_info["go_where"], content_info["tong_dian"], content_info["superiority"], content_info["content_count"], content_info["content_data_list"], g_config_json_data["PRODUCT_INFO_LIST"], g_config_json_data["CONTENT_INFO_LIST"], self)
			editContent_Win._signal.connect(self.signal_recv_func)
			editContent_Win.setWindowModality(Qt.ApplicationModal)
			editContent_Win.show()
			editContent_Win.exec_()
		return 
    
	def agentTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.agentTable_click_last_time < 2:
			return
		self.agentTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 5:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能体列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
            # 删除智能体的数据
			agent_info_list = g_config_json_data["AGENT_INFO_LIST"]
			agent_name_of_del = agent_info_list[row]["agent_name"]
			del agent_info_list[row]  
			g_config_json_data["AGENT_INFO_LIST"] = agent_info_list
			# 删除智能体相关的任务数据 
			task_info_list = g_config_json_data["TASK_INFO_LIST"]
			task_info_list_new = []
			for task_info in task_info_list:
				if "task_source" in task_info:
					if agent_name_of_del == task_info["task_source"].strip("智能体_"):
						continue 
				task_info_list_new.append(task_info)
			g_config_json_data["TASK_INFO_LIST"] = task_info_list_new
            
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_agent_list_view()
			self.reload_task_list_view()
		elif column == 6:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能体列表中的第{row}行的编辑按钮")
			agent_info_list = g_config_json_data["AGENT_INFO_LIST"]
			agent_info = agent_info_list[row]  
            
			editAgent_Win = AddAgentWindow("编辑智能体", agent_info["agent_name"], agent_info["agent_type"], agent_info["agent_product_name"], agent_info["agent_touch_type"], agent_info["agent_touch_object"], agent_info["agent_sop"], agent_info["task_info_list_of_agent"], g_config_json_data["PRODUCT_INFO_LIST"], g_config_json_data["USERGROUP_INFO_LIST"], g_config_json_data["FRIEND_INFO_LIST"], g_config_json_data["CONTENT_INFO_LIST"], g_config_json_data["AGENT_INFO_LIST"], self)
			editAgent_Win._signal.connect(self.signal_recv_func)
			editAgent_Win.setWindowModality(Qt.ApplicationModal)
			editAgent_Win.show()
			editAgent_Win.exec_()
		return 

	def autoreplyTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.autoreplyTable_click_last_time < 2:
			return
		self.autoreplyTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能客服机器人列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			autoreply_info_list = g_config_json_data["AUTOREPLY_INFO_LIST"]
			del autoreply_info_list[row]  
			g_config_json_data["AUTOREPLY_INFO_LIST"] = autoreply_info_list
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_autoreply_list_view()
            
            # 更新原有的变量
			if len(autoreply_info_list) == 0:
				g_config_json_data["HUA_SU_FILES"] = []
				g_config_json_data["info_of_deposit_list"] = []
				save_config_data(g_config_json_data, g_config_path) 
			else:
				g_config_json_data["HUA_SU_FILES"] = autoreply_info_list[0]["hua_su_file_paths"]
				g_config_json_data["username_of_can_deposit_list"] =  [friend_info["friend_name"] for friend_info in g_config_json_data["FRIEND_INFO_LIST"]]
				g_config_json_data["info_of_deposit_list"] = info_of_deposit_list
				save_config_data(g_config_json_data, g_config_path) 
                
		elif column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能客服机器人列表中的第{row}行的编辑按钮")
			autoreply_info_list = g_config_json_data["AUTOREPLY_INFO_LIST"]
			autoreply_info = autoreply_info_list[row]  

			editAutoReply_Win = AddAutoReplyWindow("编辑客服机器人", autoreply_info["autoreply_name"], autoreply_info["response_usergroupname"], autoreply_info["llm_name"], autoreply_info["hua_su_file_paths"], g_config_json_data["USERGROUP_INFO_LIST"], g_config_json_data["FRIEND_INFO_LIST"], g_config_json_data["COZE_AGENT_INFO_LIST"], g_config_json_data["AUTOREPLY_INFO_LIST"], self)
			editAutoReply_Win._signal.connect(self.signal_recv_func)
			editAutoReply_Win.setWindowModality(Qt.ApplicationModal)
			editAutoReply_Win.show()
			editAutoReply_Win.exec_()
		return

	def autoaddTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.autoaddTable_click_last_time < 2:
			return
		self.autoaddTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 2:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能添加机器人列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			autoadd_info_list = g_config_json_data["AUTOADD_INFO_LIST"]
			autoadd_name_of_del = autoadd_info_list[row]["autoadd_name"]
			del autoadd_info_list[row]  
			g_config_json_data["AUTOADD_INFO_LIST"] = autoadd_info_list
            # 删除获客机器人相关的任务数据
			task_info_list = g_config_json_data["TASK_INFO_LIST"]
			task_info_list_new = []
			for task_info in task_info_list:
				if "task_source" in task_info:
					if autoadd_name_of_del == task_info["task_source"].strip("获客机器人_"):
						continue 
				task_info_list_new.append(task_info)
			g_config_json_data["TASK_INFO_LIST"] = task_info_list_new
            
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_autoadd_list_view()
			self.reload_task_list_view()

		elif column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能添加机器人列表中的第{row}行的编辑按钮")
			autoadd_info_list = g_config_json_data["AUTOADD_INFO_LIST"]
			autoadd_info = autoadd_info_list[row]  
            
			if "remark_prefix" not in autoadd_info:
				autoadd_info["remark_prefix"] = ""
			editAutoAdd_Win = AddAutoAddWindow("编辑加好友机器人", autoadd_info["autoadd_name"], autoadd_info["strategy_type"], autoadd_info["remark_prefix"], autoadd_info["add_model_name"], autoadd_info["start_time"], autoadd_info["willing_add_count_list"], autoadd_info["file_paths"], g_config_json_data["AUTOADD_INFO_LIST"], self)
			editAutoAdd_Win._signal.connect(self.signal_recv_func)
			editAutoAdd_Win.setWindowModality(Qt.ApplicationModal)
			editAutoAdd_Win.show()
			editAutoAdd_Win.exec_()
		return

	def autopassTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.autopassTable_click_last_time < 2:
			return
		self.autopassTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 2:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能通过机器人列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			autopass_info_list = g_config_json_data["AUTOPASS_INFO_LIST"]
			del autopass_info_list[row]  
			g_config_json_data["AUTOPASS_INFO_LIST"] = autopass_info_list
            
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_autopass_list_view()

		elif column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了智能通友机器人列表中的第{row}行的编辑按钮")
			autopass_info_list = g_config_json_data["AUTOPASS_INFO_LIST"]
			autopass_info = autopass_info_list[row]  
		
			editAutoPass_Win = AddAutoPassWindow("编辑通过好友机器人", autopass_info["autopass_name"], autopass_info["remark_prefix"], g_config_json_data["AUTOPASS_INFO_LIST"], self)
			editAutoPass_Win._signal.connect(self.signal_recv_func)
			editAutoPass_Win.setWindowModality(Qt.ApplicationModal)
			editAutoPass_Win.show()
			editAutoPass_Win.exec_()

		return

	def llmTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.llmTable_click_last_time < 2:
			return
		self.llmTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			QMessageBox.question(self, APP_NAME, "内置模型不可删除！", QMessageBox.Yes)
			"""
			print(f"点击了LLM列表中的第{row}行的删除按钮")
			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
			llm_info_list = g_config_json_data["LLM_INFO_LIST"]
			del llm_info_list[row]  
			g_config_json_data["LLM_INFO_LIST"] = llm_info_list
            
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_llm_list_view()
			"""

		elif column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了LLM列表中的第{row}行的编辑按钮")
			llm_info_list = g_config_json_data["LLM_INFO_LIST"]
			llm_info = llm_info_list[row]  
		
			editLLM_Win = AddLLMWindow("编辑大模型", llm_info, g_config_json_data["LLM_INFO_LIST"], self)
			editLLM_Win._signal.connect(self.signal_recv_func)
			editLLM_Win.setWindowModality(Qt.ApplicationModal)
			editLLM_Win.show()
			editLLM_Win.exec_()

		return

	def cozeAgentTable_cell_clicked(self, index):
		self.clickCommonFun()
        # 解决bug:点击时，很容易同一时间触发两次
		if time.time() - self.cozeAgentTable_click_last_time < 2:
			return
		self.cozeAgentTable_click_last_time = time.time()
        
		row = index.row()
		column = index.column()
        
		if column == 3:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了LLM列表中的第{row}行的删除按钮")

			result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.No:
				return 
 
			coze_agent_info_list = g_config_json_data["COZE_AGENT_INFO_LIST"]
			# 确保无关联此智能体
			coze_agent_name_sel = coze_agent_info_list[row]["agent_name"]
			coze_agent_name_sel_with_fron_str = COZE_FRON_STR + coze_agent_name_sel
			for autoreply_info in g_config_json_data["AUTOREPLY_INFO_LIST"]:
				if "llm_name" not in autoreply_info:
					continue
				llm_name = autoreply_info["llm_name"]
				if llm_name == coze_agent_name_sel_with_fron_str:
					QMessageBox.information(self, APP_NAME, "此Coze智能体被“自动客服机器人”关联，请先解绑再进行删除操作", QMessageBox.Yes)
					return
 
			del coze_agent_info_list[row]  
			g_config_json_data["COZE_AGENT_INFO_LIST"] = coze_agent_info_list
            
			save_config_data(g_config_json_data, g_config_path) 
			self.reload_coze_agent_list_view()
   
		elif column == 4:
			#if False == self.startBtn.isEnabled():
			#	QMessageBox.information(self, APP_NAME, "请先停止任务再执行删除操作", QMessageBox.Yes)
			#	return
			print(f"点击了Coze智能体列表中的第{row}行的编辑按钮")
			coze_agent_info_list = g_config_json_data["COZE_AGENT_INFO_LIST"]
			coze_agent_info = coze_agent_info_list[row]  
		
			editCozeAgent_Win = AddCozeAgentWindow("编辑扣子智能体", coze_agent_info,  coze_agent_info_list, self)
			editCozeAgent_Win._signal.connect(self.signal_recv_func)
			editCozeAgent_Win.setWindowModality(Qt.ApplicationModal)
			editCozeAgent_Win.show()
			editCozeAgent_Win.exec_()

		return


	def startBtnFun(self, b_need_sync_friend = False, b_need_sync_taggroup = False):
		self.clickCommonFun()
		if False == self.startBtn.isEnabled():
			return
		print_my("开始运行")
		self.restore_state()
		if False == http_is_Inited():
			iRet, config_return = http_init(g_str_mac, CLIENT_NAME, g_config_json_data, adb_get_screen)
			if iRet != 0:
				if iRet == RET_CODE_NO_LICENCE:
					self.set_btn_state(ApplicationState.NoLicence)
					print_my("!!!!试用结束，请点击右下角“授权”按钮授权")
					QMessageBox.information(self, APP_NAME, "试用结束，请点击右下角“授权”按钮授权", QMessageBox.Yes)
					return
				elif iRet == APP_RET_CODE_NET_ERROR:
                    # chenyj 因为服务器不可用，所以先放过这个
					#"""
					self.set_btn_state(ApplicationState.Normal)
					print_my("!!!!请确保本机可以访问互联网4")
					self.set_state(EnvStateType.Env_Net_State, False)
					QMessageBox.information(self, APP_NAME, "请确保本机可以访问互联网4", QMessageBox.Yes)
					return 
					#"""
					pass
				elif iRet == APP_RET_CODE_NET_ERROR:
					self.set_btn_state(ApplicationState.Normal)
					print_my("!!!!本机无法访问托管服务器")
					self.set_state(EnvStateType.Env_Net_State, False)
					QMessageBox.information(self, APP_NAME, "本机无法访问托管服务器", QMessageBox.Yes)
					return
		if False == self.loginAndPaymentFunc():
			return

		if len(g_str_mac) == 0:
			self.set_btn_state(ApplicationState.Normal)
			print_my("!!!!获取本地mac地址失败")
			self.set_state(EnvStateType.Env_Net_State, False)
			QMessageBox.information(self, APP_NAME, "获取本地mac地址失败", QMessageBox.Yes)
			return 
		#'''
		access_token = get_access_token()
		if access_token is None:
			self.set_btn_state(ApplicationState.Normal)
			print_my("!!!!请确保本机可以访问互联网")
			self.set_state(EnvStateType.Env_Net_State, False)
			QMessageBox.information(self, APP_NAME, "请确保本机可以访问互联网", QMessageBox.Yes)
			return 
		#'''
		if True == is_out_of_time()[0]:
			print_my("!!!!试用结束，请点击右下角“授权”按钮授权")
			self.signal_of_table.emit("lic_outdate")
			return
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			b_ready = adb_is_lei_dian_device_ready(self)
			if b_ready == False:
				# 使用QProcess启动第三方应用
				"""
				self.process_lei_dian = QProcess(self)
				self.process_lei_dian.finished.connect(self.handleLeiDianProcessFinished)
				# 设置进程通道模式为独立模式
				#self.process_lei_dian.setProcessChannelMode(QProcess.SeparateChannels)
				self.process_lei_dian.start(LEI_DIAN_DIR + "\dnplayer.exe")
				self.process_lei_dian.waitForStarted()
				"""
				print_my("启动托管器")
				# 创建 QProcess 对象，且在后台运行
				self.process_lei_dian = QProcess(self)
				# 可选：设置环境变量
				env = QProcessEnvironment()
				# 例如：env.insert('MY_VAR', 'my_value')
				self.process_lei_dian.setProcessEnvironment(env)
				# 使用 startDetached 启动进程
				self.process_lei_dian.startDetached(LEI_DIAN_DIR + "\dnplayer.exe")
			else:
				if is_another_lei_dian_running() == True:
					print_my("!!!!检测到你的系统中有雷电模拟器在运行，请先将它关闭后再启动")
					QMessageBox.information(self, APP_NAME, "检测到你的系统中有雷电模拟器在运行，请先将它关闭后再启动", QMessageBox.Yes)
					return 
		elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
			iRet = is_windows_wechat_ready(self)
			if iRet == APP_RET_CODE_WECHAT_NO_INSTALL:
				print_my("!!!!本地的微信应用程序还没安装")
				QMessageBox.information(self, APP_NAME, "检测到你的系统中本地的微信应用程序还没安装", QMessageBox.Yes)
				return 

			pids = kill_wechat(False)
			if pids:
				print("已杀掉微信进程：", pids)
            # 保证微信在前台运行
			if is_weChat_running() == False:
				print("!!!!startBtnFun, 检测到微信没有启动或没有置顶，偿试启动并置顶")
				open_wechat_app_and_set_top() 
				"""
				if is_weChat_running() == False:
					print("!!!!startBtnFun, 检测到微信没有启动或没有置顶，偿试启动并置顶失败")
					QMessageBox.information(self, APP_NAME, "检测到你的系统中本地的微信应用程序无法启动或找不到窗口", QMessageBox.Yes)
					return 
				"""
                
		else:
			iRet = adb_is_remote_phone_ready(self)
			if iRet == APP_RET_CODE_PHONE_NO_CONNECT:
				self.signal_of_table.emit("remote_phone_prepare")
				return
			elif iRet == APP_RET_CODE_PHONE_NO_LIGHT:
				self.signal_of_table.emit("screen_no_light")
				return 
			elif iRet == APP_RET_CODE_PHONE_NO_UNLOCK:
				self.signal_of_table.emit("screen_lock")
				return 
            
		self.set_state(EnvStateType.Env_Net_State, True)
		g_Event_for_main_work.clear()
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
			g_Event_for_app_check.clear()
			g_Event_for_heart_beat.clear()
		#创建检测是否启动成功的线程
		self.set_btn_state(ApplicationState.Running)
		#self.tableView.setEnabled(False)
		if b_need_sync_friend == False:
			b_need_sync_friend = True if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0 else False
		if b_need_sync_friend == True or b_need_sync_taggroup == True:
			# 创建等待窗口
            # chenyj test 去掉所有的加载中的效果
			if self.waiting_Win is None and g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
				print("创建等待窗口, startBtnFun")
				self.waiting_Win = WaitingWindow(self)
				self.waiting_Win.setWindowModality(Qt.ApplicationModal)
				self.waiting_Win.show() 
				g_Event_for_main_work.clear()
				thread = threading.Thread(target = main_work_thread, args = (self, b_need_sync_friend, b_need_sync_taggroup))
				thread.start()
				if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
					g_Event_for_app_check.clear()
					thread = threading.Thread(target = app_check_thread, args = (self, ))  
					thread.start()
			else:
				if False == is_thread_running(main_work_thread.__name__):
					print("等待窗口依然存在, startBtnFun, 但是线程已经停止了, 启动线程")
					g_Event_for_main_work.clear()
					thread = threading.Thread(target = main_work_thread, args = (self, b_need_sync_friend, b_need_sync_taggroup))
					thread.start()
					if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
						g_Event_for_app_check.clear()
						thread = threading.Thread(target = app_check_thread, args = (self, ))  
						thread.start()
				else:
					print("等待窗口依然存在, startBtnFun, 但是线程依然在运行, 不做任何处理")
					return 
		else:
			g_Event_for_main_work.clear()
			thread = threading.Thread(target = main_work_thread, args = (self, b_need_sync_friend, b_need_sync_taggroup))  
			thread.start()
			if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
				g_Event_for_app_check.clear()
				thread = threading.Thread(target = app_check_thread, args = (self, ))  
				thread.start()

		if b_need_sync_friend == False and b_need_sync_taggroup == False:
			# 定时器每500ms工作一次
			self.Timer_for_time.start(500)
			# 建立定时器连接通道  注意这里调用TimeUpdate方法，不是方法返回的的结果，所以不能带括号，写成self.TimeUpdate()是不对的
			self.Timer_for_time.timeout.connect(self.TimeUpdate)
			self.datetimeStart = datetime.now()
		# 将主窗口隐蔽
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
			#set_resolution_to_1920x1080()
      		# 主窗口隐藏
			self.hide()              		
			self.rightPanelWin = RightPanelWindow(self)
			self.rightPanelWin._signal.connect(self.signal_recv_func)
   			# 显示右侧窄窗
			self.rightPanelWin.show()     
			set_rightPanelWin(self.rightPanelWin)
			# chenyj test
			start_block_inputs(self.stopBtnFun)
		return

	def phoneImageLabelBtnFun(self):
		"""
		if g_config_json_data["PHONE_CONNECTED"] == "0":
			self.signal_of_table.emit("remote_phone_prepare")
		"""
		return
    
	def stopBtnFun(self):
		stop_block_inputs()
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
			set_wechat_normal()
			set_rightPanelWin(None)
		self.clickCommonFun()
        # chenyj debug
		print('--- stopBtnFun ---')
		self.stopBtn.setEnabled(False)
		g_Event_for_main_work.set()
		g_Event_for_app_check.set()
		g_Event_for_heart_beat.set()

		self.Timer_for_time.stop()
		#reset_resolution()

		self.Timer_for_do_after_stop = QTimer()
		self.Timer_for_do_after_stop.start(500*1)
		self.Timer_for_do_after_stop.timeout.connect(self.do_after_stop)
		
		return


	def do_after_stop(self):
		self.Timer_for_do_after_stop.stop()
		restore_wechat_focus_via_taskbar()

	def licenceBtnFun(self):
		"""
		if False == self.loginAndPaymentFunc():
			return

		if False == is_thread_running(main_work_thread.__name__):
			print("licenceBtnFun, main_work_thread线程已经停止了")
		else:
			print("licenceBtnFun, main_work_thread线程依然在运行")	 
		self.clickCommonFun()
		self.licence_Win = LicenceWindow()
		self.licence_Win._signal.connect(self.signal_recv_func)
		self.licence_Win.setWindowModality(Qt.ApplicationModal)
		self.licence_Win.show()
		self.licence_Win.exec_()
		"""
		return
        
	def setAgentBtnFun(self, b_auto_start_after = False):    
		if False == self.loginAndPaymentFunc():
			return
		self.clickCommonFun()
		self.setAgent_Win = SetAgentWindow(self.can_agent_list, self.sel_agent_list, self.hua_su_file_paths, b_auto_start_after)
		self.setAgent_Win._signal.connect(self.signal_recv_func)
		self.setAgent_Win.setWindowModality(Qt.ApplicationModal)
		self.setAgent_Win.show()
		self.setAgent_Win.exec_()
		return
        
	def setDepositObjectBtnFun(self, b_auto_start_after = False):
		if False == self.loginAndPaymentFunc():
			return
		self.clickCommonFun()
		"""
		if len(self.username_of_can_deposit_list) == 0:
			print_my("!!!!没有可选的托管对象列表")
			QMessageBox.information(self, APP_NAME, "没有可选的托管对象,请启动客服来获取", QMessageBox.Yes)
			return 
		"""    
		self.setDepositObject_Win = SetDepositObjectWindow(self.username_of_can_deposit_list, self.username_of_deposit_list, b_auto_start_after)
		self.setDepositObject_Win._signal.connect(self.signal_recv_func)
		self.setDepositObject_Win.setWindowModality(Qt.ApplicationModal)
		self.setDepositObject_Win.show()
		self.setDepositObject_Win.exec_()
		return
        
	def addTaskBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		self.clickCommonFun()
		add_friend_file_paths = ["待添加好友昵称列表.txt"]
		self.addTask_Win = AddTaskWindow(add_friend_file_paths, self)
		self.addTask_Win._signal.connect(self.signal_recv_func)
		self.addTask_Win.setWindowModality(Qt.ApplicationModal)
		self.addTask_Win.show()
		self.addTask_Win.exec_()
		return  
        
	def addProductBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		self.clickCommonFun()
		self.addProduct_Win = AddProductWindow('添加产品', "", "", "", [], g_config_json_data["PRODUCT_INFO_LIST"], self)
		self.addProduct_Win._signal.connect(self.signal_recv_func)
		self.addProduct_Win.setWindowModality(Qt.ApplicationModal)
		self.addProduct_Win.show()
		self.addProduct_Win.exec_()
		return         

	def addContentBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		self.clickCommonFun()
		self.addContent_Win = AddContentWindow('添加文案', "", "", "", "", "", "", '5', [], g_config_json_data["PRODUCT_INFO_LIST"], g_config_json_data["CONTENT_INFO_LIST"], self)
		self.addContent_Win._signal.connect(self.signal_recv_func)
		self.addContent_Win.setWindowModality(Qt.ApplicationModal)
		self.addContent_Win.show()
		self.addContent_Win.exec_()
		return   

	def exportFriendBtnFun(self):
		excel_file_path = ""
		friend_data_list = g_config_json_data["FRIEND_INFO_LIST"]
		if len(friend_data_list) <= 0:
			result = QMessageBox.question(self, APP_NAME, "还没有好友信息，无需导出。请先同步好友信息", QMessageBox.Yes)
			return
        
		# 弹出框选择保存的目录及文件名
		root = tk.Tk()
		root.withdraw()  # 隐藏主窗口
        
		# 弹出“另存为”对话框
		excel_file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择保存路径和文件名"
        )
        
		# 如果用户选择了路径，则保存文件
		if excel_file_path:
			if True == save_friend_list_to_excel(friend_data_list, excel_file_path):
				self.signal_of_table.emit("tooltip_{}".format("好友导出成功"))
				print_my(f"好友导出成功，保存到:{excel_file_path}")
				return
			else:
				QMessageBox.information(self, APP_NAME, "好友导出失败", QMessageBox.Yes)
				print_my("！！！导出好友失败")
				return 
		else:
			print("用户取消了保存操作")

		return

	def syncFriendBtnFun(self):  
		if False == self.loginAndPaymentFunc():
			return
		if self.applicationState == ApplicationState.Running:
			print("!!!!请先停止任务")
			QMessageBox.information(self, APP_NAME, "请先停止\"私域精灵\"再同步好友", QMessageBox.Yes)
			return

		if len(g_config_json_data["FRIEND_INFO_LIST"]) > 0:
			result = QMessageBox.question(self, APP_NAME, "重新同步好友需要5-30分钟，你确定想同步?", QMessageBox.Yes | QMessageBox.No)
			if(result == QMessageBox.No):
				return
		self.signal_of_table.emit("sync_friend") 
		"""
		self.clickCommonFun()
		g_Event_for_main_work.clear()
        #创建检测是否启动成功的线程
		self.set_btn_state(ApplicationState.Running)
		#self.tableView.setEnabled(False)
        # 创建等待框口
		if self.waiting_Win is None:
			print("创建等待窗口, syncFriendBtnFun")
			self.waiting_Win = WaitingWindow(self)
			self.waiting_Win.setWindowModality(Qt.ApplicationModal)
			self.waiting_Win.show()
			thread = threading.Thread(target = main_work_thread, args = (self, True, False))  
			thread.start()
		else:
			if False == is_thread_running(main_work_thread.__name__):
				print("等待窗口依然存在, syncFriendBtnFun, 但是线程已经停止了, 启动线程")
				thread = threading.Thread(target = main_work_thread, args = (self, True, False))
				thread.start()
			else:
				print("等待窗口依然存在, syncFriendBtnFun, 但是线程依然在运行, 不做任何处理")
				return 
		"""
		return 

    # "添加客户组"按钮响应函数    
	def addUsergroupBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		# 确保好友已经同步
		if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			QMessageBox.information(self, APP_NAME, "当前没有好友，请行同步好友信息!", QMessageBox.Yes)
			self.tab_widget.setCurrentIndex(1) 
			return 
		self.clickCommonFun()
		self.addUserGroup_Win = AddUserGroupWindow("添加客户组", "", "", [], g_config_json_data["FRIEND_INFO_LIST"], [], g_config_json_data["USERGROUP_INFO_LIST"], self)
		self.addUserGroup_Win._signal.connect(self.signal_recv_func)
		self.addUserGroup_Win.setWindowModality(Qt.ApplicationModal)
		self.addUserGroup_Win.show()
		self.addUserGroup_Win.exec_()
		return    

    # "同步微信标签组"按钮响应函数 
	def syncTagGroupBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		if self.applicationState == ApplicationState.Running:
			print("!!!!请先停止任务")
			QMessageBox.information(self, APP_NAME, "请先停止\"私域精灵\"再同步微信标签组", QMessageBox.Yes)
			return

		result = QMessageBox.question(self, APP_NAME, "同步微信标签组需要5-30分钟，你确定想同步?", QMessageBox.Yes | QMessageBox.No)
		if(result == QMessageBox.No):
			return
   
		self.signal_of_table.emit("sync_taggroup") 
		"""              
		self.clickCommonFun()
		g_Event_for_main_work.clear()
        #创建检测是否启动成功的线程
		self.set_btn_state(ApplicationState.Running)
		#self.tableView.setEnabled(False)
        # 创建等待框口
		if self.waiting_Win is None:
			print("创建等待窗口, syncTagGroupBtnFun")
			self.waiting_Win = WaitingWindow(self)
			self.waiting_Win.setWindowModality(Qt.ApplicationModal)
			self.waiting_Win.show()
			thread = threading.Thread(target = main_work_thread, args = (self, False, True))  
			thread.start()
		else:
			if False == is_thread_running(main_work_thread.__name__):
				print("等待窗口依然存在, syncTagGroupBtnFun, 但是线程已经停止了, 启动线程")
				thread = threading.Thread(target = main_work_thread, args = (self, False, True))
				thread.start()
			else:
				print("等待窗口依然存在, syncTagGroupBtnFun, 但是线程依然在运行, 不做任何处理")
				return 
		"""
		return 
    
	def addAgentBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		# 确保好友已经同步
		if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			QMessageBox.information(self, APP_NAME, "当前没有好友，请行同步好友信息!", QMessageBox.Yes)
			self.tab_widget.setCurrentIndex(1) 
			return 
		self.clickCommonFun()
		self.addAgent_Win = AddAgentWindow("添加营销智能体", "", "", "", "", "", "", [], g_config_json_data["PRODUCT_INFO_LIST"], g_config_json_data["USERGROUP_INFO_LIST"], g_config_json_data["FRIEND_INFO_LIST"], g_config_json_data["CONTENT_INFO_LIST"], g_config_json_data["AGENT_INFO_LIST"], self)
		self.addAgent_Win._signal.connect(self.signal_recv_func)
		self.addAgent_Win.setWindowModality(Qt.ApplicationModal)
		self.addAgent_Win.show()
		self.addAgent_Win.exec_()
		return  

	def addAutoReplyBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		# 确保好友已经同步
		if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			QMessageBox.information(self, APP_NAME, "当前没有好友，请行同步好友信息!", QMessageBox.Yes)
			self.tab_widget.setCurrentIndex(1) 
			return 
            
		self.clickCommonFun()
		if len(g_config_json_data["AUTOREPLY_INFO_LIST"]) >= 1:
			QMessageBox.information(self, APP_NAME, "目前只支持最多一个客服机器人", QMessageBox.Yes)
			return 
            
		self.addAutoReply_Win = AddAutoReplyWindow("添加自动客服机器人", "", "", "智谱GLM", [], g_config_json_data["USERGROUP_INFO_LIST"], g_config_json_data["FRIEND_INFO_LIST"], g_config_json_data["COZE_AGENT_INFO_LIST"], g_config_json_data["AUTOREPLY_INFO_LIST"], self)
		self.addAutoReply_Win._signal.connect(self.signal_recv_func)
		self.addAutoReply_Win.setWindowModality(Qt.ApplicationModal)
		self.addAutoReply_Win.show()
		self.addAutoReply_Win.exec_()
		return  

	def addAutoAddBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		# 确保好友已经同步
		if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			QMessageBox.information(self, APP_NAME, "当前没有好友，请行同步好友信息!", QMessageBox.Yes)
			self.tab_widget.setCurrentIndex(1) 
			return 
            
		self.clickCommonFun()
        
		self.addAutoAdd_Win = AddAutoAddWindow("添加加好友机器人", "", "", "", "", "", [], [], g_config_json_data["AUTOADD_INFO_LIST"], self)
		self.addAutoAdd_Win._signal.connect(self.signal_recv_func)
		self.addAutoAdd_Win.setWindowModality(Qt.ApplicationModal)
		self.addAutoAdd_Win.show()
		self.addAutoAdd_Win.exec_()
		return 

	def addAutoPassBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		# 确保好友已经同步
		if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			QMessageBox.information(self, APP_NAME, "当前没有好友，请行同步好友信息!", QMessageBox.Yes)
			self.tab_widget.setCurrentIndex(1) 
			return 
            
		self.clickCommonFun()
		if len(g_config_json_data["AUTOPASS_INFO_LIST"]) >= 1:
			QMessageBox.information(self, APP_NAME, "目前只支持最多一个通过好友机器人", QMessageBox.Yes)
			return 
        
		self.addAutoPass_Win = AddAutoPassWindow("添加通过好友机器人", "", "", g_config_json_data["AUTOPASS_INFO_LIST"], self)
		self.addAutoPass_Win._signal.connect(self.signal_recv_func)
		self.addAutoPass_Win.setWindowModality(Qt.ApplicationModal)
		self.addAutoPass_Win.show()
		self.addAutoPass_Win.exec_()
		return 

	def addCozeAgentBtnFun(self):
		if False == self.loginAndPaymentFunc():
			return
		coze_agent_info = {}
		self.clickCommonFun()
		self.addCozeAgent_Win = AddCozeAgentWindow("添加扣子智能体", coze_agent_info, g_config_json_data["COZE_AGENT_INFO_LIST"], self)
		self.addCozeAgent_Win._signal.connect(self.signal_recv_func)
		self.addCozeAgent_Win.setWindowModality(Qt.ApplicationModal)
		self.addCozeAgent_Win.show()
		self.addCozeAgent_Win.exec_()
		return  

	def saveSettingBtnFun(self):
		str_is_do_exceed_task = ""
		# 1.
		str_inter_sync_friend_minute = self.interSyncNewFrientEdit.text()
		if len(str_inter_sync_friend_minute) == 0:
			QMessageBox.information(self, APP_NAME, "请输入多少分钟同步1次新好友信息", QMessageBox.Yes)
			return
		if int(str_inter_sync_friend_minute) < 5:
			QMessageBox.information(self, APP_NAME, "同步1次新好友信息分钟数不能小于5分钟，请重新输入", QMessageBox.Yes)
			return
		# 2.
		str_inter_do_task_second = self.interDoTaskEdit.text()
		if len(str_inter_do_task_second) == 0:
			QMessageBox.information(self, APP_NAME, "请输入多少秒检测1次是否有待执行的任务", QMessageBox.Yes)
			return
		if int(str_inter_do_task_second) < 5:
			QMessageBox.information(self, APP_NAME, "检测1次是否有待执行的任务的秒数不能小于5秒，请重新输入", QMessageBox.Yes)
			return
		# 3.
		str_inter_add_friend_second = self.interAddFriendEdit.text()
		if len(str_inter_add_friend_second) == 0:
			QMessageBox.information(self, APP_NAME, "请输入自动加好友的间隔秒数", QMessageBox.Yes)
			return
		if int(str_inter_add_friend_second) < 60:
			QMessageBox.information(self, APP_NAME, "自动加好友的间隔秒数不能小于60秒，请重新输入", QMessageBox.Yes)
			return
		# 4.
		str_inter_auto_pass_second = self.interAutoPassEdit.text()
		if len(str_inter_auto_pass_second) == 0:
			QMessageBox.information(self, APP_NAME, "请输入检查有新好友请求的间隔秒数", QMessageBox.Yes)
			return
		if int(str_inter_auto_pass_second) < 60:
			QMessageBox.information(self, APP_NAME, "检查有新好友请求的间隔秒数不能小于60秒，请重新输入", QMessageBox.Yes)
			return

		# 5.获取是否执行过期的任务    
		for i, radio_button in enumerate(self.is_do_exceed_task_radio_button_list):
			if radio_button.isChecked():
				str_is_do_exceed_task = self.IS_DO_EXCEED_TASK_LIST[i]
				break
		# 6.
		str_pos_text = self.posTextEdit.text()
		str_neg_text = self.negTextEdit.text()

		g_config_json_data["GET_NEW_FRIEND_TIME_INTER"] = int(str_inter_sync_friend_minute)*60
		g_config_json_data["TASK_TIME_INTER"] = int(str_inter_do_task_second)
		g_config_json_data["TASK_TIME_INTER_OF_ADD_NEW_FRIENT"] = int(str_inter_add_friend_second)
		g_config_json_data["AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT"] = int(str_inter_auto_pass_second)
		g_config_json_data["g_b_Do_Exceed_Task"] = True if str_is_do_exceed_task == "是" else False
		g_config_json_data["POS_TEXT"] = str_pos_text
		g_config_json_data["NEG_TEXT"] = str_neg_text
  
		app_info.GET_NEW_FRIEND_TIME_INTER = g_config_json_data["GET_NEW_FRIEND_TIME_INTER"]
		app_info.TASK_TIME_INTER = g_config_json_data["TASK_TIME_INTER"]
		app_info.TASK_TIME_INTER_OF_ADD_NEW_FRIENT = g_config_json_data["TASK_TIME_INTER_OF_ADD_NEW_FRIENT"]
		app_info.AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT = g_config_json_data["AUTO_PASS_TIME_INTER_OF_ADD_NEW_FRIENT"]
		g_b_Do_Exceed_Task = g_config_json_data["g_b_Do_Exceed_Task"]
		app_info.POS_TEXT = g_config_json_data["POS_TEXT"]
		app_info.NEG_TEXT = g_config_json_data["NEG_TEXT"]
  
		save_config_data(g_config_json_data, g_config_path)
		update_task_state_by_setting(g_config_json_data)
  
		self.signal_of_table.emit("tooltip_{}".format("保存配置成功"))
  
		return 

	# 用户登录及付款
	def loginAndPaymentFunc(self):
		global g_i_second_wait

		if self.Timer_for_showLogin is not None:
			self.Timer_for_showLogin.stop()
		if len(g_config_json_data["BIND_PHONE"]) == 0:
			self.login_Win = LoginWindow(g_config_json_data)
			self.login_Win._signal.connect(self.signal_recv_func)
			self.login_Win.setWindowModality(Qt.ApplicationModal)
			self.login_Win.show()
			self.login_Win.exec_()
			self.login_Win = None

			if len(g_config_json_data["BIND_PHONE"]) == 0:
				return False
		if True == is_out_of_time()[0]:
			g_i_second_wait = 2
			self.payment_Win = PaymentWindow(g_config_json_data)
			self.payment_Win._signal.connect(self.signal_recv_func)
			self.payment_Win.setWindowModality(Qt.ApplicationModal)
			self.payment_Win.show()
			self.payment_Win.exec_()
			self.payment_Win = None
			g_i_second_wait = 30
			if True == is_out_of_time()[0]:
				return False
			else:
				return True
		return True

	# 所有点击动作的共用处理函数
	def clickCommonFun(self):

		# 解决table样式丢失问题 
		width = int(g_desktop_w/16)
		height = int(g_desktop_h*1/22)
		self.tab_style_sheet = f"""
		QTabBar::tab {{
			border: 2px solid gray;
			padding: 1px;
			font-size: 26px; /* 设置字体大小 */
			color: blue; /* 设置字体颜色 */
			height: {height}px; /* 设置标签页的高度 */
		}}
		QTabBar::tab:selected {{
			background-color: lightblue;
			color: red; /* 设置字体颜色 */
		}}
		QTabWidget::pane {{
			border: 2px solid gray;
		}}
		"""
		self.tab_widget.style().unpolish(self.tab_widget)
		self.tab_widget.setStyleSheet("")
		self.tab_widget.style().polish(self.tab_widget)
		self.tab_widget.setStyleSheet(self.tab_style_sheet)

		# 解决开始按钮样式丢失问题
		self.startBtn.setStyleSheet("""
            QPushButton {
                background-color: #3366FF; /* 蓝色背景 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:hover {
                background-color: #1A387B; /* 鼠标悬停时的背景颜色 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:enabled {
                background-color: #3366FF; /* 蓝色背景 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
		# 解决停止按钮样式丢失问题
		self.stopBtn.setStyleSheet("""
            QPushButton {
                color: blue;          /* 设置字体颜色为蓝色 */
                font-weight: bold;    /* 设置字体为粗体 */
                font-size: 14px;      /* 可选：设置字体大小 */
            }
            QPushButton:disabled {
                color: gray;
            }
		""")
		return 

	def WindowsInitOk(self, strAction = ""):
		global g_str_mac

		self.Timer_for_Init_check.stop()
        
		# 先确保计算机开启了VT选项 
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			TIME_BEGIN("VT选项检查")
			if True == check_virtualization():
				print_my("BIOS-VT选项检测通过")
			else:
				print_my("!!!运行环境检查不通过(请在BIOS中开始VT选项)")
				print_my("开启方法参考:")
				print_my("https://help.ldmnq.com/docs/bd8Q4x")
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				return 
			TIME_END("VT选项检查")
  
		# 先确保不是在虚拟机里运行
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			TIME_BEGIN("虚拟机检查")
			if False == is_virtual_machine():
				print_my("很好，你是在真实机器里运行")
			else:
				print_my("!!!运行环境检查不通过(请不要在虚拟机中运行)")
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				QMessageBox.information(self, APP_NAME, "!!!运行环境检查不通过(请不要在虚拟机中运行)", QMessageBox.Yes)	
				return 
			TIME_END("虚拟机检查")
  
		# 先确保360等杀毒软件已经关闭
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator: 
			TIME_BEGIN("360等杀毒软件检查")  
			if False == is_360_running():
				print_my("360软件互斥检查通过")
			else:
				print_my("!!!检测到你的电脑里有360正在运行(请先卸载360软件)")
				#print_my("开启方法参考:")
				#print_my("https://help.ldmnq.com/docs/bd8Q4x")
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				QMessageBox.information(self, APP_NAME, "!!!检测到你的电脑里有360正在运行(请先卸载360软件)", QMessageBox.Yes)	
				return
			TIME_END("360等杀毒软件检查") 

		# 先确保Windows的defender实时保护已经关闭 
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
			TIME_BEGIN("Windows的defender实时保护检查") 
			if False == is_windows_defender_enabled():
				print_my("很好，Windows的defender实时保护是关闭的")
			else:
				print_my("!!!检测到你的电脑里Windows defender实时保护开启(请先关闭)")
				#print_my("请在弹出来的”Windows安全中心“应用中操作，关闭方法参考:")
				#print_my("https://zhuanlan.zhihu.com/p/494923217")
				print_my("请在弹出来的”Windows安全中心“应用中操作，关闭方法:”病毒和威胁防护“设置里关闭”实时保护“。关闭后再启动应用")
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				QMessageBox.information(self, APP_NAME, "!!!检测到你的电脑里Windows defender实时保护开启(请先关闭)。\n请在弹出来的”Windows安全中心“应用中操作，关闭方法:”病毒和威胁防护“设置里关闭”实时保护“", QMessageBox.Yes)	
				open_windows_defender_panel()
				return
				"""
				if True == disable_defender_registry():
					print_my("!!!!Windows defender实时保护关闭成功,请重启电脑")
				else:
					print_my("!!!!Windows defender实时保护关闭失败")
				return 
				"""
			TIME_END("Windows的defender实时保护检查") 
   
		if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
			iRet = is_resolution_satify()
			if iRet != APP_RET_CODE_SUCESS:
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				print_my("检测到你的系统不支持分辨率【1920x1080】，所以无法运行")
				QMessageBox.information(self, APP_NAME, "检测到你的系统不支持分辨率【1920x1080】，所以无法运行", QMessageBox.Yes)
				return 

			iRet = is_resolution_right()
			if iRet != APP_RET_CODE_SUCESS:
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				print_my("检测到你的系统分辨率不是【1920x1080】，现在我要将它切换这个分辨率，是否同意?")
				QMessageBox.information(self, APP_NAME, "检测到你的系统分辨率不是【1920x1080】，现在我要将它切换这个分辨率，是否同意?", QMessageBox.Yes)
				set_resolution_to_1920x1080() 
				iRet = is_resolution_right()
				if iRet != APP_RET_CODE_SUCESS:
					print_my("!!!!切换分辨率失败")
					QMessageBox.information(self, APP_NAME, "!!!!切换分辨率失败", QMessageBox.Yes)
					return 

			iRet = is_windows_wechat_ready(self)
			if iRet == APP_RET_CODE_WECHAT_NO_INSTALL:
				valid_version_list = list(WINDOWS_WECHAT_OK_VERSION_DICT.keys())
				download_url = WINDOWS_WECHAT_OK_VERSION_DICT[valid_version_list[0]]["download_url"]

				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				print_my(f"!!!!检测到你的系统中本地的微信应用程序还没安装，请先安装")
				msgBox = QMessageBox(QMessageBox.Information, APP_NAME, 
					f"检测到你的系统中本地的微信应用程序还没安装，请先安装\n"
					f"下载地址:<a href='{download_url}'>{download_url}</a>")
				msgBox.setTextFormat(Qt.RichText)
				msgBox.setStandardButtons(QMessageBox.Yes)
				msgBox.button(QMessageBox.Yes).setText("跳转到下载页面")
				msgBox.exec_()
				return

			v = get_wechat_version()
			if v is None:
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				print_my("检测到你的系统没有安装微信，所以无法运行")
				QMessageBox.information(self, APP_NAME, "检测到你的系统没有安装微信，所以无法运行", QMessageBox.Yes)
				return 
			if v not in WINDOWS_WECHAT_OK_VERSION_DICT:
				valid_version_list = list(WINDOWS_WECHAT_OK_VERSION_DICT.keys())
				download_url = WINDOWS_WECHAT_OK_VERSION_DICT[valid_version_list[0]]["download_url"]
				self.set_btn_state(ApplicationState.UnValid_But_Setting)
				print_my(f"!!!!检测到你的系统中本地的微信应用程序版本【{v}】不对，请更新到此版本,即：{valid_version_list}")
				msgBox = QMessageBox(QMessageBox.Information, APP_NAME, 
					f"检测到你的系统中本地的微信应用程序版本【{v}】不对，请更新到此版本,即：{valid_version_list}\n"
					f"下载地址:<a href='{download_url}'>{download_url}</a>")
				msgBox.setTextFormat(Qt.RichText)
				msgBox.setStandardButtons(QMessageBox.Yes)
				msgBox.button(QMessageBox.Yes).setText("跳转到下载页面")
				msgBox.exec_()
				return 

		# 根据判断根据下载所需要的组件
		b_file_complete = False
		if True == os.path.exists(LEI_DIAN_DIR) and True == os.path.exists(TESSERACT_DIR) and True == os.path.exists(os.path.join(TESSERACT_DIR, "tesseract.exe")):
			b_file_complete = True 
			print_my("^-^软件组件完整性检测通过")
            
        # chenyj test
		if b_file_complete == False: 
		#if True:
			print_my("!!!!软件组件完整性检测不通过")
            
			self.set_btn_state(ApplicationState.UnValid)
        
			self.dialog_downloading = CustomProgressDialog('组件下载中(预估需要10分钟)...', 'Abort', 0, 100, self)
			self.dialog_downloading.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
			#self.dialog_downloading.setWindowTitle('托管初始化')
			self.dialog_downloading.setMaximum(100)
			self.dialog_downloading.setMinimum(0)
			self.dialog_downloading.setWindowModality(Qt.WindowModal)
			self.dialog_downloading.setCancelButton(None)
			self.dialog_downloading.resize(400, 50)  
			self.dialog_downloading.show()

			self.thread_downloading = threading.Thread(target = download_thread, args = (self, ))  
			#self.thread_downloading = DownloadThread()
			#self.thread_downloading.progress.connect(self.dialog_downloading.setValue)
			#self.thread_downloading.progress.connect(self.setValue)
			#self.thread_downloading.finished.connect(self.dialog_downloading.close)
			self.thread_downloading.start()
			return

		self.set_btn_state(ApplicationState.Normal)
		"""
		if len(self.username_of_can_deposit_list) == 0:
			self.setDepositObjectBtn.setEnabled(False)
		else:
			self.setDepositObjectBtn.setEnabled(True)
		"""
		self.setDepositObjectBtn.setEnabled(True)
        
		self.setAgentBtn.setEnabled(True)  
		self.syncFriendBtn.setEnabled(True)
		self.licenceBtn.setEnabled(True)
		self.addTaskBtn.setEnabled(True)
        
		upload_snape()
		gc.collect()
		#'''
        # 启动雷电模拟器状态检查线程
		#"""
		if g_deivce_MODEL != DEVICE_MODEL_TYPE.Windows:
			g_Event_for_app_check.clear()
			thread = threading.Thread(target = app_check_thread, args = (self, ))  
			thread.start()
		#"""
        
		if False == http_is_Inited():
			iRet, config_return = http_init(g_str_mac, CLIENT_NAME, g_config_json_data, adb_get_screen)
			if iRet != 0:
				if iRet == RET_CODE_NO_LICENCE:
					self.set_btn_state(ApplicationState.Normal)
					print_my("!!!!试用结束，请点击右下角“授权”按钮授权")
					QMessageBox.information(self, APP_NAME, "试用结束，请点击右下角“授权”按钮授权", QMessageBox.Yes)
					return
				else:
					# chenyj 因为服务器不可用，所以先放过这个
					#"""
					self.set_btn_state(ApplicationState.Normal)
					self.set_state(EnvStateType.Env_Net_State, False)
					print_my("!!!!请确保本机可以访问互联网2")
					QMessageBox.information(self, APP_NAME, "请确保本机可以访问互联网2", QMessageBox.Yes)
					return 
					#"""
					pass
			if "lic_config" in config_return:
				lic_config = config_return["lic_config"]
				if "USER_TYPE" in lic_config:
					user_type = lic_config["USER_TYPE"]             
					time_now = time.time()
					g_config_json_data["FIRST"] = time_now
					g_config_json_data["USER_TYPE"] = user_type
					save_config_data(g_config_json_data, g_config_path)
					b_outdate, delta_second = is_out_of_time()        
					self.licenceBtn.setText("状态：{}".format("试用(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != "0" else "永久会员"))
					print_my("下发授权配置成功。当前状态：{}".format("试用(剩余:{:.2f}天)".format(delta_second/(3600*24)) if g_config_json_data["USER_TYPE"] != "0" else "永久会员"))
		print_my("恭喜:初始化网络正常")
		# 启动与服务端的心跳线程
		g_Event_for_heart_beat.clear()
		thread = threading.Thread(target = heart_beat_thread, args = (self, ))  
		thread.start()
        # 判断是否登录过，如果没有弹出登录页面
		if False == self.loginAndPaymentFunc():
			return
        
		self.signal_recv_func("check_lic")
		#'''
		access_token = get_access_token()
		if access_token is None:
			self.set_btn_state(ApplicationState.Normal)
			print_my("!!!!启动时:检测OCR失败，请确保本机可以访问互联网")
			self.set_state(EnvStateType.Env_Net_State, False)
			QMessageBox.information(self, APP_NAME, "请确保本机可以访问互联网1", QMessageBox.Yes)
			return 
        # chenyj debug 
		print("启动时:检测OCR正常")
		self.set_state(EnvStateType.Env_Net_State, True)
		print_my("恭喜:环境初始化成功")
		# chenyj test
		# 在windows上这里不直接启动
		if False:
		#if strAction == "start" or len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			self.startBtnFun()
		else:
			if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
				print_my("!!!!请点击“开始运行”按钮来启动托管")
			else:
				print_my("!!!!请点击“开始运行”按钮来启动任务")
		return
		
	def update_logon_wechat_state(self):
		if len(g_config_json_data["CURRENT_LOGON_USERNAME"]) == 0:
			self.currentLogonWechatBtn.setEnabled(False)
			self.currentLogonWechatBtn.setText("未登录")
		else:
			if g_config_json_data["CURRENT_LOGON_USERNAME_ONLINE"] == "1":
				self.currentLogonWechatBtn.setEnabled(True)
			else:
				self.currentLogonWechatBtn.setEnabled(False)
			if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
				username_display = "{}(平板)".format(g_config_json_data["CURRENT_LOGON_USERNAME"])
			if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
				username_display = "{}".format(g_config_json_data["CURRENT_LOGON_USERNAME"])
			else:
				username_display = "{}(手机)".format(g_config_json_data["CURRENT_LOGON_USERNAME"])
			self.currentLogonWechatBtn.setText(username_display)
		return

	def set_btn_state(self, applicationState):
		if len(g_config_json_data["FRIEND_INFO_LIST"]) == 0:
			self.syncFriendBtn.setText("同步好友")
		else:
			self.syncFriendBtn.setText("重新同步好友")
		
		if applicationState == ApplicationState.Normal:
			self.startBtn.setEnabled(True)
			if len(g_config_json_data["CURRENT_LOGON_USERNAME"]) == 0:
				if g_deivce_MODEL == DEVICE_MODEL_TYPE.Local_Emulator:
					self.startBtn.setText("登录微信(平板模式)")
				elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
					self.startBtn.setText("开始运行")
				else:
					self.startBtn.setText("连接手机(手机模式)")
			else:	
				self.startBtn.setText("开始运行")
			self.addProductBtn.setEnabled(True)      
			self.addUsergroupBtn.setEnabled(True) 
			self.addAgentBtn.setEnabled(True)
			self.addAutoReplyBtn.setEnabled(True)
			self.addAutoAddBtn.setEnabled(True)
			if 	self.addAutoPassBtn is not None:
				self.addAutoPassBtn.setEnabled(True)
			self.setDepositObjectBtn.setEnabled(True)
			self.setAgentBtn.setEnabled(True)
			self.addTaskBtn.setEnabled(True)
			self.syncFriendBtn.setEnabled(True)
			self.syncTagGroupBtn.setEnabled(True)
			self.stopBtn.setEnabled(False)
		elif applicationState == ApplicationState.Running:
			self.startBtn.setEnabled(False)
			self.startBtn.setText("私域精灵运行中...")
			self.addProductBtn.setEnabled(True)      
			self.addUsergroupBtn.setEnabled(True) 
			self.addAgentBtn.setEnabled(True)
			self.addAutoReplyBtn.setEnabled(True)
			self.addAutoAddBtn.setEnabled(True)
			if self.addAutoPassBtn is not None:
				self.addAutoPassBtn.setEnabled(True)
			self.setDepositObjectBtn.setEnabled(False)
			self.setAgentBtn.setEnabled(False)
			self.addTaskBtn.setEnabled(False)
			self.syncFriendBtn.setEnabled(True)
			self.syncTagGroupBtn.setEnabled(True)
			self.stopBtn.setEnabled(True)
		elif applicationState == ApplicationState.UnValid:
			self.startBtn.setEnabled(False)
			self.stopBtn.setEnabled(False)
			self.setDepositObjectBtn.setEnabled(False)
			self.setAgentBtn.setEnabled(False)
			self.addTaskBtn.setEnabled(False)
			self.syncFriendBtn.setEnabled(False)
			self.syncTagGroupBtn.setEnabled(False)
			self.licenceBtn.setEnabled(False)
			self.addProductBtn.setEnabled(False)      
			self.addUsergroupBtn.setEnabled(False) 
			self.addAgentBtn.setEnabled(False)
			self.addAutoReplyBtn.setEnabled(False)
			self.addAutoAddBtn.setEnabled(False)
			if self.addAutoPassBtn is not None:
				self.addAutoPassBtn.setEnabled(False)
		elif applicationState in [ApplicationState.NoLicence, ApplicationState.UnValid_But_Setting]:
			self.startBtn.setEnabled(False)
			self.startBtn.setText("开始运行")
			self.stopBtn.setEnabled(False)
			self.setDepositObjectBtn.setEnabled(False)
			self.setAgentBtn.setEnabled(False)
			#self.addTaskBtn.setEnabled(False)
			self.addTaskBtn.setEnabled(True)
			self.syncFriendBtn.setEnabled(False)
			self.syncTagGroupBtn.setEnabled(False)
			self.licenceBtn.setEnabled(True)
			#self.addProductBtn.setEnabled(False)
			self.addProductBtn.setEnabled(True)      
			#self.addUsergroupBtn.setEnabled(False) 
			self.addUsergroupBtn.setEnabled(True) 
			#self.addAgentBtn.setEnabled(False)
			self.addAgentBtn.setEnabled(True)
			#self.addAutoReplyBtn.setEnabled(False)
			self.addAutoReplyBtn.setEnabled(True)
			#self.addAutoAddBtn.setEnabled(False)
			self.addAutoAddBtn.setEnabled(True)
			if self.addAutoPassBtn is not None:
				#self.addAutoPassBtn.setEnabled(False)
				self.addAutoPassBtn.setEnabled(True)
		self.applicationState = applicationState
		return 
	def TimeUpdate(self):
		datetimeNow = datetime.now()
		intal_seconds = (datetimeNow - self.datetimeStart).seconds
		intal_hours = int(int(intal_seconds)/3600)
		intal_seconds = intal_seconds - 3600*intal_hours
		intal_minutes = int(int(intal_seconds)/60)
		intal_seconds = intal_seconds - 60*intal_minutes
		strDiplay = "私域托管正在进行:" + str(intal_hours) + "时" + str(intal_minutes) + "分" + str(intal_seconds) + "秒"
		self.timeLabel.setText(strDiplay)
        
		if intal_seconds % 10 == 0:
			self.clickCommonFun()
        
		return 

	# 更新手机屏幕件中的图片
	def update_screen_img(self, image_path, text = "", draw_box=None):
		if not hasattr(self, 'phoneImageLabel'):
			return

		# 1. 读原图
		base_pix = QPixmap(image_path)
		if base_pix.isNull():
			self.phoneImageLabel.setText("图片显示区域")
			return

		# 2. 以原图大小建一张画布
		canvas = QPixmap(base_pix.size())
		canvas.fill(Qt.transparent)

		# 3. 把原图先画上去
		painter = QPainter(canvas)
		painter.drawPixmap(0, 0, base_pix)

		# 4. 按原图坐标画矩形
		if draw_box not in [None, ""]:
			pen = QPen(QColor(255, 0, 0), 6)
			painter.setPen(pen)
			painter.drawRect(draw_box[0], draw_box[1],
							draw_box[2] - draw_box[0],
							draw_box[3] - draw_box[1])
			# chenyj 把画了框的图片保存起来
			try:
				# 创建保存目录（如果不存在）
				import os
				save_dir = os.path.join(app_info.USER_DATA_DIR, "boxed_click_images")
				if not os.path.exists(save_dir):
					os.makedirs(save_dir)
				
				# 生成带时间戳的文件名
				from datetime import datetime
				timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
				save_path = os.path.join(save_dir, f"boxed_{timestamp}.png")
				
				# 保存画了框的图片
				canvas.save(save_path, "PNG")
				#print_my(f"已保存画框图片到: {save_path}")
			except Exception as e:
				print_my(f"保存画框图片失败: {str(e)}")

		# 5. ===== 新增：在图片中下位置写“点击连接” =====
		if len(text) > 0:
			font = QFont("Microsoft YaHei", 10, QFont.Bold)
			painter.setFont(font)
			painter.setPen(QColor(0, 0, 0))       # 白色文字

			fm = QFontMetrics(font)
			try:
				text_w = fm.horizontalAdvance(text)  # Qt 5.11+
			except AttributeError:
				text_w = fm.width(text)  # 旧版 PyQt5 兼容
			text_h = fm.height()

			# 计算底边居中、距底边 15% 的位置
			base_w = base_pix.width()
			base_h = base_pix.height()
			x = (base_w - text_w) // 2
			y = int(base_h * 0.75)                      # 85% 高度处
			painter.drawText(x, y, text)

		painter.end()

		# 6. 显示
		self.phoneImageLabel.setPixmap(canvas)
		self.phoneImageLabel.setScaledContents(True)

	# 在屏幕截图上画点击的位置 
	def draw_red_circle_on_screen_imag(self, x0: int, y0: int, r: int = 30):
		"""
		x0, y0: 以原图为基准的坐标（左上角为 0,0）
		r     : 圆的半径
		"""
		# 1. 当前显示的 pixmap
		pm = self.phoneImageLabel.pixmap()
		if pm is None:
			return
		"""
		print(f"draw_red_circle_on_screen_imag, 点击的位置 [{x0}, {y0}] ")
		# 2. 原图宽高
		orig_w, orig_h = pm.width(), pm.height()
		print( f'draw_red_circle_on_screen_imag, 原图尺寸 w:{orig_w} h{orig_h}')

		# 3. 获取 QLabel 当前实际显示区域大小
		lbl_rect = self.phoneImageLabel.contentsRect()
		disp_w, disp_h = lbl_rect.width(), lbl_rect.height()
		print( f'draw_red_circle_on_screen_imag, 实际显示尺寸 w:{disp_w} h:{disp_h}')

		# 4. 计算缩放比例
		sx = disp_w / orig_w if orig_w else 1.0
		sy = disp_h / orig_h if orig_h else 1.0

		# 5. 把原图坐标映射到当前显示坐标

		dx = int(x0 * sx)
		dy = int(y0 * sy)
		dr = int(r * min(sx, sy))   # 半径也按最小比例缩放，保证圆不变椭圆
  		"""
		dx = x0
		dy = y0
		dr = r
		print(f"draw_red_circle_on_screen_imag, 最后画点的位置 [{dx}, {dy}] ")

		# 6. 深拷贝并绘制
		painted = pm.copy()
		painter = QPainter(painted)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(Qt.blue))
		painter.drawEllipse(QPointF(dx, dy), dr, dr)
		# chenyj 把painter的图片保存到本地  
		try:
			# 创建保存目录（如果不存在）
			import os
			save_dir = os.path.join(app_info.USER_DATA_DIR, "boxed_click_images")
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
			
			# 生成带时间戳的文件名
			from datetime import datetime
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			save_path = os.path.join(save_dir, f"click_{timestamp}.png")
			
			# 保存画了点击位置的图片
			painted.save(save_path, "PNG")
			#print_my(f"已保存点击位置图片到: {save_path}")
		except Exception as e:
			print_my(f"保存点击位置图片失败: {str(e)}")
		
		painter.end()

		# 7. 放回 QLabel
		self.phoneImageLabel.setPixmap(painted)
		return
    
	def append_log(self, text, color):
		if text == self.last_text_of_logTextEdit:
			return 
            
		self.save_color = self.logTextEdit.textColor()
		self.logTextEdit.setTextColor(QColor(color))
		self.logTextEdit.append(text)
		self.logTextEdit.setTextColor(self.save_color)  
		self.last_text_of_logTextEdit = text
		return
        
	def write_log_to_windows(self, message):  
		# 追加日志消息前检查长度限制
		#if self.logTextEdit.document().blockCount() >= 2:
		#	self.logTextEdit.clear()  
		"""
		if "!!" in message:
			self.append_log(message, "black") 
		"""
		#"""
		if "!!" in message:
			self.append_log(message, "red")
		else:
			self.append_log(message, "black")
		#"""
		# 自动滚动到文本框的底部
		if g_b_Debug == False:
			self.logTextEdit.moveCursor(QTextCursor.End)
			self.logTextEdit.ensureCursorVisible()
            
	def on_tab_changed_func(self, index):
		print(f"切换到标签页 {index}")
        
		self.clickCommonFun()
        
		return 

	def pair_thread(self, ip, port, pairing_code):
		iRet = adb_pair_remote_phone(ip, port, pairing_code)
		self.pair_i_ret = iRet
		return

	def connect_thread(self, ip, port):
		restart_adb_server()
		iRet = adb_connect_remote_phone(self, ip, port)
		self.connect_i_ret = iRet
		return
   
	def showToolTip(self, message):
		self.toolTip.setText(message)
		# 显示提示
		self.toolTip.show()

		# 创建动画，使提示逐渐显示
		self.animation = QPropertyAnimation(self.toolTip, b"windowOpacity")
		self.animation.setDuration(500)  # 动画持续时间（毫秒）
		self.animation.setStartValue(0)
		self.animation.setEndValue(1)
		self.animation.setEasingCurve(QEasingCurve.InOutQuart)
		self.animation.start()

		# 3秒后隐藏提示
		QTimer.singleShot(3000, self.hideToolTip)

	def hideToolTip(self):
		# 创建动画，使提示逐渐消失
		self.animation = QPropertyAnimation(self.toolTip, b"windowOpacity")
		self.animation.setDuration(500)  # 动画持续时间（毫秒）
		self.animation.setStartValue(1)
		self.animation.setEndValue(0)
		self.animation.setEasingCurve(QEasingCurve.InOutQuart)
		self.animation.start()

		# 动画结束后隐藏提示
		self.animation.finished.connect(self.toolTip.hide)
        
	"""
	重写showEvent方法
	"""
	def showEvent(self, event):
		"""窗口显示时调整imageLabel的尺寸"""
		super().showEvent(event)
		# 延迟调整尺寸，确保logTextEdit已经完全渲染
		QTimer.singleShot(100, self.adjust_image_label_size)
		
	def adjust_image_label_size(self):
		## 调整phoneImageLabel的尺寸：高度与logTextEdit相同，宽度为高度的一半
		log_height = self.logTextEdit.height()
		image_width = int(log_height *3/5)
		self.phoneImageLabel.setFixedSize(image_width, log_height)
  
		## 
		wechat_width = int(image_width*2/5)
		wechat_height = wechat_width
		self.currentLogonWechatBtn.setFixedSize(wechat_width, wechat_height)
  
		return

	def closeEvent(self, event):
		result = QMessageBox.question(self, APP_NAME, "你确定想关闭?", QMessageBox.Yes | QMessageBox.No)
		if(result == QMessageBox.Yes):
			print_my("应用程序正常退出")
			if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
				set_wechat_normal()
			event.accept()
			# 关闭前的所有子线程
			g_Event_for_main_work.set()
			g_Event_for_app_check.set()
			g_Event_for_heart_beat.set()

			self.Timer_for_time.stop()
            # 去掉系统托盘
			self.tray_icon.hide()
			time.sleep(0.5)
		else:
			event.ignore()
"""
if __name__ == '__main__':    
	app = QApplication(sys.argv)
    
	table = Table()
    # 将table传给日志模块,用于把消息输出到窗口
	print_init(table)
	table.show()
    
	sys.exit(app.exec_())
"""

# 创建主窗口
splash.updateMessage("正在创建主窗口...")
table = Table()
# 将table传给日志模块,用于把消息输出到窗口
print_init(table)
table.show()
splash.finish(table)

# 确保启动画面被关闭
splash.close()

sys.exit(app.exec_())
