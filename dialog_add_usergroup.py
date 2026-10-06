# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QRadioButton, QLineEdit, QSpacerItem, QSizePolicy, QScrollArea
from dialog_set_friend_object import SetFriendObjectWindow
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap, QIntValidator
import json
import ast
import tkinter as tk
from tkinter import filedialog
from app_info import APP_NAME
from hover_label import HoverLabel

#ADD_MODEL_LIST = ["根据时间规则创建", "根据昵称规则创建", "根据互动活跃度创建", "手动"]  
ADD_MODEL_LIST = ["根据时间规则创建", "根据昵称规则创建", "根据聊天内容关键字创建", "手动"] 
class AddUserGroupWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, usergroup_name, add_model_name, rule_info_list, friend_info_list, username_of_group_list, usergroup_info_list, parent):
        super().__init__()
        self.title = title
        self.usergroup_name = usergroup_name
        if len(add_model_name) == 0:
            add_model_name = "手动"
        self.rule_info_list = rule_info_list
        self.add_model_name = add_model_name        
        self.friend_info_list = friend_info_list
        self.username_of_group_list = username_of_group_list
        self.usergroup_info_list = usergroup_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(830), int(450))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 客户客户组名称
        self.layout1 = QHBoxLayout()
        self.labelGroupName = HoverLabel("客户组的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的客户组取个名称吧", self)
        self.usergroupNameEdit = QTextEdit()
        self.usergroupNameEdit.setPlaceholderText("在这里输入要添加的客户组的名称")
        font_metrics = self.usergroupNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.usergroupNameEdit.setFixedHeight(line_height + 10)  # 增加一些 padding
        self.usergroupNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.usergroup_name) > 0:
            self.usergroupNameEdit.setText(self.usergroup_name)
            self.usergroupNameEdit.setReadOnly(True)
            self.usergroupNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                usergroup_name = "客户组" + str(i)
                if usergroup_name not in [usergroup_info["usergroup_name"] for usergroup_info in self.usergroup_info_list]:
                    break
            self.usergroupNameEdit.setText(usergroup_name)
        self.layout1.addWidget(self.labelGroupName)
        self.layout1.addWidget(self.usergroupNameEdit)
        ##########################################
        # 添加方式
        self.layout2 = QHBoxLayout()
        self.labelAddModel = HoverLabel("创建方式:<font color='red'>*</font> <font color='blue'>?</font>", "根据时间规则创建的客户组，将根据好友添加时间的规则来创建客户组；\n根据互动活跃度创建的客户组，是指根据用户回复的频率来创建客户组 ；\n手动创建的客户组，需要手动添加好友", self)
        self.add_model_radio_button_list = []
        for i, add_model_name in enumerate(ADD_MODEL_LIST):
            add_model_radio_button = QRadioButton(add_model_name, self)
            add_model_radio_button.clicked.connect(self.update_add_model_dynamic_content)
            self.add_model_radio_button_list.append(add_model_radio_button)
        self.add_model_radio_button_list[0].setChecked(True) 
        if len(self.add_model_name) > 0:
            for i, add_model_name in enumerate(ADD_MODEL_LIST):
                if self.add_model_name == add_model_name:
                    self.add_model_radio_button_list[i].setChecked(True) 
                    break          
        self.layout2.addWidget(self.labelAddModel)
        for add_model_radio_button in self.add_model_radio_button_list:
            self.layout2.addWidget(add_model_radio_button)
            if self.title == "编辑客户组":
                add_model_radio_button.setEnabled(False)
             
        # 创建一个占位标签，用于动态显示内容
        self.dynamic_layout = QVBoxLayout()
        ##########################################
        # 创建垂直布局并添加QTabWidget
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.dynamic_layout)
        #layout.addWidget(self.setMemberBtn)
        #layout.addWidget(self.labelMembers)
        #self.layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(self.layout)
        
        self.update_add_model_dynamic_content()

    def update_add_model_dynamic_content(self):
        # 清除旧内容
        #self.layout.removeLayout(self.dynamic_layout)
        #self.dynamic_layout.deleteLater()     
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            # 检查是否为子布局
            if item.layout() == self.dynamic_layout:
                # 移除子布局
                self.layout.removeItem(item)
                # 删除子布局及其所有控件
                self.delete_layout(self.dynamic_layout)
                break

        for i, add_model_radio_button in enumerate(self.add_model_radio_button_list):
            model_name = ADD_MODEL_LIST[i]
            if add_model_radio_button.isChecked():
                if model_name == "根据时间规则创建":
                    # label
                    self.label_gui_ze = QLabel("符合以下规则的用户将被放到此用户组：")
                    # 
                    self.start_day_layout = QHBoxLayout()
                    label_start_day_left = QLabel("1.添加好友后")
                    self.input_box_start_day = QLineEdit()
                    self.input_box_start_day.setValidator(QIntValidator(0, 99))  # 设置输入范围为0到99
                    self.input_box_start_day.setMaxLength(2)  # 设置最大输入长度为2
                    self.input_box_start_day.setFixedWidth(50)  # 设置输入框宽度为50像素
                    if len(self.rule_info_list) > 0:
                        str_start_day = str(self.rule_info_list[0]["DAYS_AFTER_ADD"]["START_DAY"])
                        self.input_box_start_day.setText(str_start_day)
                    else:
                        self.input_box_start_day.setText("0")
                    label_start_day_right = QLabel("天开始")
                    self.start_day_layout.addWidget(label_start_day_left)
                    self.start_day_layout.addWidget(self.input_box_start_day)
                    self.start_day_layout.addWidget(label_start_day_right)
                    self.start_day_layout.addStretch(1) 
                    # 且 
                    self.label_and = QLabel("且")
                    # 添加好友后天结束
                    self.end_day_layout = QHBoxLayout()
                    label_end_day_left = QLabel("2.添加好友后")
                    self.input_box_end_day = QLineEdit()
                    self.input_box_end_day.setValidator(QIntValidator(0, 99))  # 设置输入范围为0到99
                    self.input_box_end_day.setMaxLength(2)  # 设置最大输入长度为2
                    self.input_box_end_day.setFixedWidth(50)  # 设置输入框宽度为50像素
                    if len(self.rule_info_list) > 0:
                        str_start_day = str(self.rule_info_list[0]["DAYS_AFTER_ADD"]["END_DAY"])
                        self.input_box_end_day.setText(str_start_day)
                    else:
                        self.input_box_end_day.setText("7")
                    label_end_day_right = QLabel("天结束")
                    self.end_day_layout.addWidget(label_end_day_left)
                    self.end_day_layout.addWidget(self.input_box_end_day)
                    self.end_day_layout.addWidget(label_end_day_right)
                    self.end_day_layout.addStretch(1) 
                    
                    # 成员label
                    labelText = ""
                    if len(self.username_of_group_list) > 0:
                        labelText = "已有成员:{}".format("、".join(self.username_of_group_list))
                    else:
                        labelText = "已有成员:无"
                    self.labelMembers = QLabel(labelText)
                    self.labelMembers.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.labelMembers.setWordWrap(True)
                    # 创建一个滚动区域
                    self.scroll = QScrollArea()
                    # 设置滚动区域的部件为标签
                    self.scroll.setWidget(self.labelMembers)
                    # 设置滚动区域的大小策略，以便它可以调整大小
                    self.scroll.setWidgetResizable(True)
                    # 设置滚动区域的背景颜色以便区分内容
                    self.scroll.setStyleSheet("background-color: #f0f0f0;")
                    
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
                    
                    #self.dynamic_layout.setAlignment(Qt.AlignTop)  # 设置对齐方式为顶上对齐
                    self.dynamic_layout.addWidget(self.label_gui_ze)
                    self.dynamic_layout.addLayout(self.start_day_layout)
                    self.dynamic_layout.addWidget(self.label_and)
                    self.dynamic_layout.addLayout(self.end_day_layout)
                    self.dynamic_layout.addWidget(self.scroll)
                    # 添加一个伸缩空间，让第一个控件顶上显示
                    spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.dynamic_layout.addSpacerItem(spacer)

                    self.dynamic_layout.addWidget(self.confirmBtn)
                elif model_name == "根据昵称规则创建":
                    # label
                    self.label_gui_ze_of_username = QLabel("符合以下规则的用户将被放到此用户组：")
                    # 1.
                    self.front_content_layout = QHBoxLayout()
                    label_front_content_left = QLabel("1.以")
                    
                    self.input_box_front_str = QTextEdit()
                    self.input_box_front_str.setPlaceholderText("在这里输入昵称的前缀")
                    if len(self.rule_info_list) > 0:
                        str_front_str = str(self.rule_info_list[0]["USERNAME"]["FRONT_STR"])
                        self.input_box_front_str.setText(str_front_str)
                        
                    font_metrics = self.input_box_front_str.fontMetrics()
                    line_height = font_metrics.lineSpacing()
                    self.input_box_front_str.setFixedHeight(line_height + 10)  # 增加一些 padding
                    self.input_box_front_str.setLineWrapMode(QTextEdit.NoWrap)
        
                    label_front_content_right = QLabel("前缀开始的用户昵称")
                    self.front_content_layout.addWidget(label_front_content_left)
                    self.front_content_layout.addWidget(self.input_box_front_str)
                    self.front_content_layout.addWidget(label_front_content_right)
                    self.front_content_layout.addStretch(1)  
                    
                    # 或
                    self.label_or = QLabel("或")
                    
                    # 2.
                    self.contain_content_layout = QHBoxLayout()
                    label_container_content_left = QLabel("2.含")
                    
                    self.input_box_contain_str = QTextEdit()
                    self.input_box_contain_str.setPlaceholderText("在这里输入昵称的部分字符")
                    if len(self.rule_info_list) > 0:
                        str_contain_str = str(self.rule_info_list[0]["USERNAME"]["CONTAIN_STR"])
                        self.input_box_contain_str.setText(str_contain_str)
                        
                    font_metrics = self.input_box_contain_str.fontMetrics()
                    line_height = font_metrics.lineSpacing()
                    self.input_box_contain_str.setFixedHeight(line_height + 10)  # 增加一些 padding
                    self.input_box_contain_str.setLineWrapMode(QTextEdit.NoWrap)
        
                    label_contain_content_right = QLabel("的用户昵称")
                    self.contain_content_layout.addWidget(label_container_content_left)
                    self.contain_content_layout.addWidget(self.input_box_contain_str)
                    self.contain_content_layout.addWidget(label_contain_content_right)
                    self.contain_content_layout.addStretch(1)  
                    
                    # 成员label
                    labelText = ""
                    if len(self.username_of_group_list) > 0:
                        labelText = "已有成员:{}".format("、".join(self.username_of_group_list))
                    else:
                        labelText = "已有成员:无"
                    self.labelMembers = QLabel(labelText)
                    self.labelMembers.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.labelMembers.setWordWrap(True)
                    # 创建一个滚动区域
                    self.scroll = QScrollArea()
                    # 设置滚动区域的部件为标签
                    self.scroll.setWidget(self.labelMembers)
                    # 设置滚动区域的大小策略，以便它可以调整大小
                    self.scroll.setWidgetResizable(True)
                    # 设置滚动区域的背景颜色以便区分内容
                    self.scroll.setStyleSheet("background-color: #f0f0f0;")
                                       
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
                    
                    #self.dynamic_layout.setAlignment(Qt.AlignTop)  # 设置对齐方式为顶上对齐
                    self.dynamic_layout.addWidget(self.label_gui_ze_of_username)
                    self.dynamic_layout.addLayout(self.front_content_layout)
                    self.dynamic_layout.addWidget(self.label_or)
                    self.dynamic_layout.addLayout(self.contain_content_layout) 
                    self.dynamic_layout.addWidget(self.scroll)
                    # 添加一个伸缩空间，让第一个控件顶上显示
                    spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.dynamic_layout.addSpacerItem(spacer)

                    self.dynamic_layout.addWidget(self.confirmBtn)
                elif model_name == "根据聊天内容关键字创建":
                    # label
                    self.label_gui_ze_of_chat_content = QLabel("聊天内容符合以下规则的用户将被放到此用户组：")
                    # 1.
                    self.include_content_layout = QHBoxLayout()
                    label_front_content_left = QLabel("1.含以下关键词:")
                    
                    self.input_box_include_str = QTextEdit()
                    self.input_box_include_str.setPlaceholderText("在这里输入关键词,若有多个请以,隔开")
                    if len(self.rule_info_list) > 0:
                        str_include_str = str(self.rule_info_list[0]["CHAT_CONTENT"]["INCLUDE_STR"])
                        self.input_box_include_str.setText(str_include_str)
                        
                    font_metrics = self.input_box_include_str.fontMetrics()
                    line_height = font_metrics.lineSpacing()
                    self.input_box_include_str.setFixedHeight(line_height + 10)  # 增加一些 padding
                    self.input_box_include_str.setLineWrapMode(QTextEdit.NoWrap)
        
                    self.include_content_layout.addWidget(label_front_content_left)
                    self.include_content_layout.addWidget(self.input_box_include_str)
                    #self.include_content_layout.addStretch(1)  
                    
                    # 或
                    self.label_but = QLabel("但")
                    
                    # 2.
                    self.exclude_content_layout = QHBoxLayout()
                    label_exclude_content_left = QLabel("2.不含以下关键词:")
                    
                    self.input_box_exclude_str = QTextEdit()
                    self.input_box_exclude_str.setPlaceholderText("在这里输入关键词,若有多个请以,隔开")
                    if len(self.rule_info_list) > 0:
                        str_exclude_str = str(self.rule_info_list[0]["CHAT_CONTENT"]["EXCLUDE_STR"])
                        self.input_box_exclude_str.setText(str_exclude_str)
                        
                    font_metrics = self.input_box_exclude_str.fontMetrics()
                    line_height = font_metrics.lineSpacing()
                    self.input_box_exclude_str.setFixedHeight(line_height + 10)  # 增加一些 padding
                    self.input_box_exclude_str.setLineWrapMode(QTextEdit.NoWrap)
        
                    self.exclude_content_layout.addWidget(label_exclude_content_left)
                    self.exclude_content_layout.addWidget(self.input_box_exclude_str)
                    #self.exclude_content_layout.addStretch(1)  
                    
                    # 成员label
                    labelText = ""
                    if len(self.username_of_group_list) > 0:
                        labelText = "已有成员:{}".format("、".join(self.username_of_group_list))
                    else:
                        labelText = "已有成员:无"
                    self.labelMembers = QLabel(labelText)
                    self.labelMembers.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.labelMembers.setWordWrap(True)
                    # 创建一个滚动区域
                    self.scroll = QScrollArea()
                    # 设置滚动区域的部件为标签
                    self.scroll.setWidget(self.labelMembers)
                    # 设置滚动区域的大小策略，以便它可以调整大小
                    self.scroll.setWidgetResizable(True)
                    # 设置滚动区域的背景颜色以便区分内容
                    self.scroll.setStyleSheet("background-color: #f0f0f0;")
                                       
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
                    
                    #self.dynamic_layout.setAlignment(Qt.AlignTop)  # 设置对齐方式为顶上对齐
                    self.dynamic_layout.addWidget(self.label_gui_ze_of_chat_content)
                    self.dynamic_layout.addLayout(self.include_content_layout)
                    self.dynamic_layout.addWidget(self.label_but)
                    self.dynamic_layout.addLayout(self.exclude_content_layout) 
                    self.dynamic_layout.addWidget(self.scroll)
                    # 添加一个伸缩空间，让第一个控件顶上显示
                    spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.dynamic_layout.addSpacerItem(spacer)

                    self.dynamic_layout.addWidget(self.confirmBtn)
                elif model_name == "手动":
                    # 按钮
                    self.setMemberBtn = QPushButton("设置成员(必填)")

                    self.setMemberBtn.clicked.connect(self.setMemberBtnFun)
                    # 成员label
                    labelText = ""
                    if len(self.username_of_group_list) > 0:
                        labelText = "成员:{}".format("、".join(self.username_of_group_list))
                    else:
                        labelText = "成员:无"
                    self.labelMembers = QLabel(labelText)
                    self.labelMembers.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.labelMembers.setWordWrap(True)
                    # 创建一个滚动区域
                    self.scroll = QScrollArea()
                    # 设置滚动区域的部件为标签
                    self.scroll.setWidget(self.labelMembers)
                    # 设置滚动区域的大小策略，以便它可以调整大小
                    self.scroll.setWidgetResizable(True)
                    # 设置滚动区域的背景颜色以便区分内容
                    self.scroll.setStyleSheet("background-color: #f0f0f0;")
                    
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
                    self.dynamic_layout.addWidget(self.setMemberBtn)
                    self.dynamic_layout.addWidget(self.scroll)
                    self.dynamic_layout.addWidget(self.confirmBtn)
                break 
                
        self.layout.addLayout(self.dynamic_layout)

    def delete_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.delete_layout(sub_layout)
        
    def confirmBtnFun(self):
        add_model_name = ""
        rule_info_list = []
        
        # 获取客户组名称
        str_usergroupName = self.usergroupNameEdit.toPlainText()
        if len(str_usergroupName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入客户组名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for usergroup_info in self.usergroup_info_list:
            if usergroup_info["usergroup_name"] == str_usergroupName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加客户组":
            QMessageBox.information(self, APP_NAME, "客户组的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取添加方式    
        for i, add_model_radio_button in enumerate(self.add_model_radio_button_list):
            if add_model_radio_button.isChecked():
                add_model_name = ADD_MODEL_LIST[i]
                break
        if add_model_name == "手动":
            if len(self.username_of_group_list) == 0:
                QMessageBox.information(self, APP_NAME, "请设置成员", QMessageBox.Yes)
                return
        elif add_model_name == "根据时间规则创建":
            str_start_day = self.input_box_start_day.text()
            if len(str_start_day) == 0:
                QMessageBox.information(self, APP_NAME, "请输入多少天后开始", QMessageBox.Yes)
                return
        
            str_end_day = self.input_box_end_day.text()
            if len(str_end_day) == 0:
                QMessageBox.information(self, APP_NAME, "请输入多少天后结束", QMessageBox.Yes)
                return
            if int(str_end_day) == 0:
                QMessageBox.information(self, APP_NAME, "结束天数不能为0，请重新输入", QMessageBox.Yes)
                return
            if int(str_end_day) <= int(str_start_day):
                QMessageBox.information(self, APP_NAME, "结束天数不能小于开始天数，请重新输入", QMessageBox.Yes)
                return
        
            rule_info_list = [{"DAYS_AFTER_ADD":{"START_DAY":int(str_start_day), "END_DAY":int(str_end_day)}}]
        elif add_model_name == "根据昵称规则创建":
            rule_info_list = [{"USERNAME":{"FRONT_STR":"", "CONTAIN_STR":""}}]
            str_front_str = self.input_box_front_str.toPlainText()
            if len(str_front_str) != 0:
                rule_info_list[0]["USERNAME"]["FRONT_STR"] = str_front_str
            str_contain_str = self.input_box_contain_str.toPlainText()
            if len(str_contain_str) != 0:
                rule_info_list[0]["USERNAME"]["CONTAIN_STR"] = str_contain_str
                
            if len(str_front_str) == 0 and len(str_contain_str) == 0:
                QMessageBox.information(self, APP_NAME, "请输入文本", QMessageBox.Yes)
                return
        elif add_model_name == "根据聊天内容关键字创建":
            pass
        elif add_model_name == "根据互动活跃度创建":
            pass 

        add_usergroup_data_dict = {}
        if len(self.usergroup_name) != 0:
            add_usergroup_data_dict["usergroup_name_orig"] = self.usergroup_name
        add_usergroup_data_dict["usergroup_name"] = str_usergroupName
        add_usergroup_data_dict["add_model_name"] = add_model_name
        add_usergroup_data_dict["rule_info_list"] = rule_info_list
        add_usergroup_data_dict["usergroup_member"] = self.username_of_group_list
        self._signal.emit("add_usergroup_dict_{}".format(json.dumps(add_usergroup_data_dict)))
        
        self.close()
        return
        
    def setMemberBtnFun(self):
        self.setCanSeeObject_Win = SetFriendObjectWindow('设置组成员窗口', self.friend_info_list, self.username_of_group_list)
        self.setCanSeeObject_Win._signal.connect(self.signal_recv_func)
        self.setCanSeeObject_Win.setWindowModality(Qt.ApplicationModal)
        self.setCanSeeObject_Win.show()
        self.setCanSeeObject_Win.exec_()
        
        return

    def signal_recv_func(self, para): 
        if para.startswith("set_friend_username_"):
            print("AddUserGroupWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
            
        return
        
# 测试
"""
app = QApplication(sys.argv)
dialog = AddUserGroupWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""