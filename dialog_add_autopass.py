# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QSpacerItem, QLineEdit
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_add_product import AddProductWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from task_helper import get_task_detail_data
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap, QTextCursor, QIntValidator
import json
import ast
import tkinter as tk
import random
from tkinter import filedialog
from app_info import APP_NAME, REMARK_PREFIX_TYPE_LIST_FOR_PASS
from hover_label import HoverLabel

class AddAutoPassWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, autopass_name, remark_prefix, autopass_info_list, parent):
        super().__init__()
        self.title = title
        self.autopass_name = autopass_name
        self.remark_prefix = remark_prefix
        self.autopass_info_list = autopass_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(550), int(165))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 加友机器人的名称
        self.layout1 = QHBoxLayout()
        self.labelAutoPassName = HoverLabel("机器人的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的自动通过好友添加请求的机器人取个名称", self)
        self.autoPassNameEdit = QTextEdit()
        self.autoPassNameEdit.setPlaceholderText("在这里输入要添加的机器人的名称")
        font_metrics = self.autoPassNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.autoPassNameEdit.setFixedHeight(line_height + 10) 
        self.autoPassNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.autopass_name) > 0:
            self.autoPassNameEdit.setText(self.autopass_name)
            self.autoPassNameEdit.setReadOnly(True)
            self.autoPassNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        self.layout1.addWidget(self.labelAutoPassName)
        self.layout1.addWidget(self.autoPassNameEdit)
        # 备注前缀
        self.layout2 = QHBoxLayout()
        self.labelRemarkPrefix = HoverLabel("好友备注前缀:<font color='red'>*</font> <font color='blue'>?</font>", "设置当自动通过对方的添加好友请求后,\n你想给此好友的备注前缀", self)
        self.remark_prefix_combo_box = QComboBox(self)
        for remark_prefix in REMARK_PREFIX_TYPE_LIST_FOR_PASS:
            self.remark_prefix_combo_box.addItem(remark_prefix)
        self.remark_prefix_combo_box.setCurrentIndex(0) 
        if len(self.remark_prefix) > 0:
            for i, remark_prefix in enumerate(REMARK_PREFIX_TYPE_LIST_FOR_PASS):
                if self.remark_prefix == remark_prefix:
                    self.remark_prefix_combo_box.setCurrentIndex(i)
                    break
        self.layout2.addWidget(self.labelRemarkPrefix)
        self.layout2.addWidget(self.remark_prefix_combo_box)
         
        ##########################################
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        # 创建垂直布局并添加QTabWidget
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(self.layout)
 
    def confirmBtnFun(self):
        # 获取加友机器人的名称
        str_autoPassName = self.autoPassNameEdit.toPlainText()
        if len(str_autoPassName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入通友机器人的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for autopass_info in self.autopass_info_list:
            if autopass_info["autopass_name"] == str_autoPassName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加通过好友机器人":
            QMessageBox.information(self, APP_NAME, "机器人的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取备注前缀
        remark_prefix = self.remark_prefix_combo_box.currentText()
        if len(remark_prefix) == 0:
            QMessageBox.information(self, APP_NAME, "请选择好友备注前缀", QMessageBox.Yes)
            return
            
        add_autopass_data_dict = {}
        if len(self.autopass_name) != 0:
            add_autopass_data_dict["autopass_name_orig"] = self.autopass_name
        add_autopass_data_dict["autopass_name"] = str_autoPassName
        add_autopass_data_dict["remark_prefix"] = remark_prefix
        self._signal.emit("add_autopass_dict_{}".format(json.dumps(add_autopass_data_dict)))
        
        self.close()
        return
        
    def signal_recv_func(self, para): 
        if para.startswith("set_friend_username_"):
            print("AddAutoPassWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
        elif para.startswith("hua_su_file_paths_"):
            print("AddAutoPassWindow事件收到信号:{}".format(para))
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
            self.file_paths = file_paths      
            self.reload_will_add_count_from_files() 
        elif para.startswith("add_usergroup_dict_"):
            print("AddAutoPassWindow事件收到信号:{}".format(para))
            add_usergroup_data_dict_str = para.strip("add_usergroup_dict_")
            try:
                add_usergroup_data_dict = json.loads(add_usergroup_data_dict_str)
                print(add_usergroup_data_dict)
                #self.usergroup_info_list.append(add_usergroup_data_dict)
                self._signal.emit(para)        
                self.response_usergroupname = add_usergroup_data_dict["usergroup_name"]               
                self.reload_response_usergroup_combo_box() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
        return  
                    
# 测试
"""
app = QApplication(sys.argv)
dialog = AddAutoPassWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""