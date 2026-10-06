# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QSpacerItem, QLineEdit
from numpy import True_
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_add_product import AddProductWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from task_helper import get_task_detail_data
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime, QTimer
from PyQt5.QtGui import QPixmap, QTextCursor, QIntValidator
from dialog_waiting import WaitingWindow
from threading import Thread
import json
import ast
import tkinter as tk
import random
import time
import ipaddress
from yang_hao_opt import adb_pair_remote_phone, adb_connect_remote_phone
from error_code import *
from ip_port_widget import IpPortWidget
from tkinter import filedialog
from app_info import APP_NAME, REMARK_PREFIX_TYPE_LIST_FOR_PASS, LLM_MODEL_NAME_TYPE_DICT, LLM_MODEL_TYPE_NAME_DICT
from hover_label import HoverLabel

class AddPhoneWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, phone_info, phone_info_list, parent):
        super().__init__()
        self.title = title
        self.phone_name = ""
        if "phone_name" in phone_info:
            self.phone_name = phone_info["phone_name"]
        self.ip_pair = ""
        if "ip_pair" in phone_info:
            self.ip_pair = phone_info["ip_pair"]
        self.port_pair = ""
        if "port_pair" in phone_info:
            self.port_pair = phone_info["port_pair"]
        self.pairing_code = ""
        if "pairing_code" in phone_info:
            self.pairing_code = phone_info["pairing_code"]
        self.ip_connect = ""
        if "ip_connect" in phone_info:
            self.ip_connect = phone_info["ip_connect"]
        self.port_connect = ""
        if "port_connect" in phone_info:
            self.port_connect = phone_info["port_connect"]
        self.phone_info_list = phone_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        self.waiting_Win = None
        self.Timer_for_time_pair = QTimer()
        self.Timer_for_time_connect = QTimer()
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(780), int(205))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 手机的名称
        self.layout1 = QHBoxLayout()
        self.labelPhoneName = HoverLabel("手机名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要添加的手机对象随意取个名称", self)
        self.phoneNameEdit = QTextEdit()
        self.phoneNameEdit.setPlaceholderText("在这里输入要添加的手机对象的名称（可随意取）")
        font_metrics = self.phoneNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.phoneNameEdit.setFixedHeight(line_height + 10) 
        self.phoneNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.phoneNameEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.phoneNameEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.phoneNameEdit.setAcceptRichText(False)
        if len(self.phone_name) > 0:
            self.phoneNameEdit.setText(self.phone_name)
            self.phoneNameEdit.setReadOnly(True)
            self.phoneNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                phone_name = "手机" + str(i)
                if phone_name not in [phone_info["phone_name"] for phone_info in self.phone_info_list]:
                    break
            self.phoneNameEdit.setText(phone_name)
        self.layout1.addWidget(self.labelPhoneName)
        self.layout1.addWidget(self.phoneNameEdit)
        # 匹配
        self.layout2 = QHBoxLayout()
        default_ip = '192.168..'
        default_port = ""
        if len(self.ip_pair) > 0:
            default_ip = self.ip_pair
        if len(self.port_pair) > 0:
            default_port = self.port_pair
        self.labelIpPair = HoverLabel("匹配用IP地址:<font color='red'>*</font> <font color='blue'>?</font>", "设置连接此手机的匹配用的IP地址", self)
        self.ip_port_pair = IpPortWidget(self, default_ip=default_ip, default_port=default_port, label_text="")
        self.ip_port_pair.valid_changed.connect(self.on_ip_port_pair_validity_changed)
        self.labelPairCode = QLabel('匹配码:')
        self.pairing_code_edit = QLineEdit()
        self.pairing_code_edit.setFixedWidth(70)
        self.pairing_code_edit.setValidator(QIntValidator(1, 999999, self))
        if len(self.pairing_code) > 0:
            self.pairing_code_edit.setText(self.pairing_code)
        self.pairCheckBtn = QPushButton("匹配测试")
        self.pairCheckBtn.clicked.connect(self.pairCheckBtnFun)
        self.layout2.addWidget(self.labelIpPair)
        self.layout2.addWidget(self.ip_port_pair)
        self.layout2.addWidget(self.labelPairCode)
        self.layout2.addWidget(self.pairing_code_edit)
        self.layout2.addWidget(self.pairCheckBtn)
        # ip_connect port_connect
        self.layout3 = QHBoxLayout()
        default_ip = '192.168..'
        default_port = ""
        if len(self.ip_connect) > 0:
            default_ip = self.ip_connect
        if len(self.port_connect) > 0:
            default_port = self.port_connect

        # 连接
        default_ip = '192.168..'
        default_port = ""
        if len(self.ip_connect) > 0:
            default_ip = self.ip_connect
        if len(self.port_connect) > 0:
            default_port = self.port_connect
        self.labelIpConnect = HoverLabel("连接用IP地址:<font color='red'>*</font> <font color='blue'>?</font>", "设置连接此手机的Connect用的IP地址", self)
        self.ip_port_connect = IpPortWidget(self, default_ip=default_ip, default_port=default_port, label_text="")
        self.ip_port_connect.valid_changed.connect(self.on_ip_port_connect_validity_changed)
        self.connectCheckBtn = QPushButton("连接测试")
        self.connectCheckBtn.clicked.connect(self.connectCheckBtnFun)
        self.layout3.addWidget(self.labelIpConnect)
        self.layout3.addWidget(self.ip_port_connect)
        self.layout3.addWidget(self.connectCheckBtn)
        ##########################################
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        self.confirmBtn.setEnabled(False)
        
        # 创建垂直布局并添加QTabWidget
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        self.layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(self.layout)
        
    def on_ip_port_pair_validity_changed(self, ok):
        return

    def on_ip_port_connect_validity_changed(self, ok):
        return

    def pairCheckBtnFun(self):
        # 获取ip和port
        ip, port = self.ip_port_pair.address()
        if ip is None or port is None:
            return
        # 获取匹配码
        pairing_code = self.pairing_code_edit.text().strip()
        if len(pairing_code) == 0:
            QMessageBox.information(self, APP_NAME, f"匹配码不能为空", QMessageBox.Yes) 
            return 
        i_pairing_code = int(pairing_code)
        if not (0 < i_pairing_code < 999999):
            QMessageBox.warning(self, "匹配码不合法", "匹配码必须是 1-999999 之间的整数。")
            return
        
        self.mainWindow.pair_i_ret = APP_RET_CODE_NO_FINISH
        self.ip_pair_doing = ip
        self.port_pair_doing = port
        self.paring_code_doing = pairing_code
        self.mainWindow.signal_of_table.emit(f"pair_{ip}_{port}_{pairing_code}")
        # 等待中提示框
        if self.waiting_Win is None:
            self.waiting_Win = WaitingWindow(self)
            self.waiting_Win.setWindowModality(Qt.ApplicationModal)
            self.waiting_Win.show() 
        # 定时器每500ms工作一次
        self.Timer_for_time_pair.stop()
        self.Timer_for_time_pair.start(1000)
        self.Timer_for_time_pair.timeout.connect(self.TimeUpdateFun_for_pair)

        return
    
    def TimeUpdateFun_for_pair(self):
        print("TimeUpdateFun_for_pair")
        if self.mainWindow.pair_i_ret == APP_RET_CODE_NO_FINISH:
            return
        if self.waiting_Win is not None:
            self.waiting_Win.close()
            self.waiting_Win = None
        self.Timer_for_time_pair.stop()    
         
        #iRet = adb_pair_remote_phone(ip, port)
        if self.mainWindow.pair_i_ret  == APP_RET_CODE_SUCESS:
            self.mainWindow.signal_of_table.emit(f"tooltip_手机[{self.ip_pair_doing}:{self.port_pair_doing}]匹配成功")
        else:
            self.mainWindow.signal_of_table.emit(f"tooltip_手机[{self.ip_pair_doing}:{self.port_pair_doing}]匹配失败")
            QMessageBox.information(self, APP_NAME, f"手机[{self.ip_pair_doing}:{self.port_pair_doing}]匹配失败", QMessageBox.Yes)  
        return 

    def connectCheckBtnFun(self):
        # 获取ip和port
        ip, port = self.ip_port_connect.address()
        if ip is None or port is None:
            return
        
        self.mainWindow.connect_i_ret = APP_RET_CODE_NO_FINISH
        self.ip_connect_doing = ip
        self.port_connect_doing = port
        self.mainWindow.signal_of_table.emit(f"connect_{ip}_{port}")
        # 等待中提示框
        if self.waiting_Win is None:
            self.waiting_Win = WaitingWindow(self)
            self.waiting_Win.setWindowModality(Qt.ApplicationModal)
            self.waiting_Win.show() 
        # 定时器每500ms工作一次
        self.Timer_for_time_connect.stop()
        self.Timer_for_time_connect.start(1000)
        self.Timer_for_time_connect.timeout.connect(self.TimeUpdateFun_for_connect) 
        return
    
    def TimeUpdateFun_for_connect(self):
        print("TimeUpdateFun_for_connect")
        if self.mainWindow.connect_i_ret == APP_RET_CODE_NO_FINISH:
            return
        self.Timer_for_time_connect.stop()  
        if self.waiting_Win is not None:
            self.waiting_Win.close()
            self.waiting_Win = None   
          
        #iRet = adb_pair_remote_phone(ip, port)
        if self.mainWindow.connect_i_ret  == APP_RET_CODE_SUCESS:
            self.mainWindow.signal_of_table.emit(f"tooltip_手机[{self.ip_connect_doing}:{self.port_connect_doing}]连接成功")
            # 保存连接信息并把弹出的连接手机对象对话框自动去掉
            self.confirmBtnFun(False)
        else:
            self.mainWindow.signal_of_table.emit(f"tooltip_手机[{self.ip_connect_doing}:{self.port_connect_doing}]连接失败")
            QMessageBox.information(self, APP_NAME, f"手机[{self.ip_connect_doing}:{self.port_connect_doing}]连接失败", QMessageBox.Yes) 
        return 
    
    def confirmBtnFun(self, b_check_data = True):
        # 获得手机对象的名称
        phone_name = self.phoneNameEdit.toPlainText()
        if len(phone_name) == 0:
            if b_check_data == True:
                QMessageBox.information(self, APP_NAME, "请输入手机的名称", QMessageBox.Yes)
                return
            else:
                phone_name = self.phone_name
            
        b_repeat_name = False 
        for phone_info in self.phone_info_list:
            if phone_info["phone_name"] == phone_name:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加手机对象":
            QMessageBox.information(self, APP_NAME, f"手机对象的名称{phone_name}已经存在，请换另一个名称", QMessageBox.Yes)
            return
        
        # 获取匹配
        ip_pair, port_pair = self.ip_port_pair.address()
        if ip_pair is None or port_pair is None:
            return
        # 获取匹配码
        pairing_code = self.pairing_code_edit.text().strip()
        if len(pairing_code) == 0:
            if b_check_data == True:
                QMessageBox.information(self, APP_NAME, f"匹配码不能为空", QMessageBox.Yes) 
                return
            else:
                pairing_code = self.pairing_code
                  
        i_pairing_code = int(pairing_code)
        if not (0 < i_pairing_code < 999999):
            if b_check_data == True:
                QMessageBox.warning(self, "匹配码不合法", "匹配码必须是 1-999999 之间的整数。")
                return
            else:
                pairing_code = self.pairing_code
        # 获取连接 
        ip_connect, port_connect = self.ip_port_connect.address()
        if ip_connect is None or port_connect is None:
            return
        
        add_phone_info_dict = {}
        if len(self.phone_name) != 0:
            add_phone_info_dict["phone_name_orig"] = self.phone_name
        if len(phone_name) != 0:
            add_phone_info_dict["phone_name"] = phone_name
        add_phone_info_dict["ip_pair"] = ip_pair
        add_phone_info_dict["port_pair"] = port_pair
        add_phone_info_dict["pairing_code"] = pairing_code
        add_phone_info_dict["ip_connect"] = ip_connect
        add_phone_info_dict["port_connect"] = port_connect
        """
        bAvailed, msgResult = check_is_coze_agent_availed(add_coze_agent_dict)
        if len(msgResult) == 0:
            msgResult = "bot id或api token不可用"
        if True == bAvailed:
            if self.title == "添加扣子智能体":
                QMessageBox.information(self, APP_NAME, "测试通过，扣子智能体信息创建成功。", QMessageBox.Yes)
            else:
                QMessageBox.information(self, APP_NAME, "测试通过，扣子智能体信息修改成功。", QMessageBox.Yes) 
        else:
            if self.title == "添加扣子智能体":
                QMessageBox.information(self, APP_NAME, f"测试不通过（{msgResult}），扣子智能体信息创建失败。", QMessageBox.Yes)    
            else:
                QMessageBox.information(self, APP_NAME, f"测试不通过（{msgResult}），扣子智能体信息修改失败。", QMessageBox.Yes)    
            return
        """
        # 发送信号
        self._signal.emit("add_phone_info_dict_{}".format(json.dumps(add_phone_info_dict)))
        self.close()

        return
                    
# 测试
"""
app = QApplication(sys.argv)
dialog = AddPhoneWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""