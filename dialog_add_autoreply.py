# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QComboBox, QRadioButton
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_add_usergroup import AddUserGroupWindow
from dialog_add_product import AddProductWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap
import json
import ast
import tkinter as tk
from tkinter import filedialog
from app_info import APP_NAME, LLM_MODEL_NAME_TYPE_DICT
from hover_label import HoverLabel
from coze_helper import COZE_FRON_STR
        
class AddAutoReplyWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, autoreply_name, response_usergroupname, llm_name, file_paths, usergroup_info_list, friend_info_list, coze_agent_info_list, autoreply_info_list, parent):
        super().__init__()
        self.title = title
        self.autoreply_name = autoreply_name
        self.response_usergroupname = response_usergroupname
        self.usergroup_info_list = usergroup_info_list
        self.llm_name = llm_name
        self.file_paths = file_paths
        self.friend_info_list = friend_info_list
        self.autoreply_info_list = autoreply_info_list
        self.coze_agent_info_list = coze_agent_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(650), int(265))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 客服机器人的名称
        self.layout1 = QHBoxLayout()
        self.labelAutoReplyName = HoverLabel("客服机器人的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的自动客服机器人取个名称", self)
        self.autoReplyNameEdit = QTextEdit()
        self.autoReplyNameEdit.setPlaceholderText("在这里输入要添加的客服机器人的名称")
        font_metrics = self.autoReplyNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.autoReplyNameEdit.setFixedHeight(line_height + 10) 
        self.autoReplyNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.autoreply_name) > 0:
            self.autoReplyNameEdit.setText(self.autoreply_name)
            self.autoReplyNameEdit.setReadOnly(True)
            self.autoReplyNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                autoreply_name = "客服机器人" + str(i)
                if autoreply_name not in [autoreply_info["autoreply_name"] for autoreply_info in self.autoreply_info_list]:
                    break
            self.autoReplyNameEdit.setText(autoreply_name)
        self.layout1.addWidget(self.labelAutoReplyName)
        self.layout1.addWidget(self.autoReplyNameEdit)
        # 机器人负责的客户组 
        self.layout2 = QHBoxLayout()
        self.labelResponseUserGroup = HoverLabel("机器人负责的客户组:<font color='red'>*</font> <font color='blue'>?</font>", "设置这个机器人要对哪个客户组中的好友自动回复。\n只有客户组中的好友发过来的消息，才会自动回复。", self)
        self.response_usergroup_combo_box = QComboBox(self)
        self.reload_response_usergroup_combo_box()
        self.response_usergroup_combo_box.currentIndexChanged.connect(self.on_item_changed_of_response_usergroup_combo_box)
        self.layout2.addWidget(self.labelResponseUserGroup)
        self.layout2.addWidget(self.response_usergroup_combo_box)
        # 使用的大模型
        self.layout3 = QHBoxLayout()
        #
        self.labelLlmType = HoverLabel("大模型/Coze智能体:<font color='red'>*</font> <font color='blue'>?</font>", "选择自动回复时使用的大模型或Coze智能体的类型", self)
        #
        self.llm_combo_box = QComboBox(self)
        for llm_name_ in LLM_MODEL_NAME_TYPE_DICT:
            self.llm_combo_box.addItem(llm_name_)
        for coze_agent_info in self.coze_agent_info_list:
            llm_name_ = f"{COZE_FRON_STR}{coze_agent_info['agent_name']}"
            self.llm_combo_box.addItem(llm_name_)
        #
        self.addNewLLMBtn = QPushButton("添加新的智能体")
        self.addNewLLMBtn.clicked.connect(self.addNewLLMBtnFun)
        self.layout3.addWidget(self.labelLlmType, 5)
        self.layout3.addWidget(self.llm_combo_box, 8)
        self.layout3.addWidget(self.addNewLLMBtn, 1)
        # 按钮
        self.setHuaSuBtn = QPushButton("设置话术库(必填)")
        self.setHuaSuBtn.setStyleSheet("""
            QPushButton {
                color: blue; /* 白色字体 */
                font-size: 15px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 1px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 15px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 5px; /* 圆角边框 */
                padding: 5px 10px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
        self.setHuaSuBtn.clicked.connect(self.setHuaSuBtnFun)
        labelText = "话术库文档:无"
        if len(self.file_paths) > 0:
            labelText = "话术库文档:\n{}".format("\n".join(self.file_paths))
        self.labelHuasu = QLabel(labelText)
        self.labelHuasu.setWordWrap(True)
        ##########################################
       
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        # 创建垂直布局并添加QTabWidget
        layout = QVBoxLayout()
        layout.addLayout(self.layout1)
        layout.addLayout(self.layout2)
        layout.addLayout(self.layout3)
        layout.addWidget(self.setHuaSuBtn)
        layout.addWidget(self.labelHuasu)
        layout.addWidget(self.confirmBtn)
        
        # load
        self.llm_combo_box.currentIndexChanged.connect(self.on_item_changed_of_llm_combo_box)
        self.llm_combo_box.setCurrentIndex(0)
        if len(self.llm_name) > 0:
            i_index = 0
            for i, llm_name_ in enumerate(LLM_MODEL_NAME_TYPE_DICT):
                if self.llm_name == llm_name_:
                    self.llm_combo_box.setCurrentIndex(i_index)
                i_index += 1
            for i, coze_agent_info in enumerate(self.coze_agent_info_list):
                llm_name_ = f"{COZE_FRON_STR}{coze_agent_info['agent_name']}"
                if self.llm_name == llm_name_:
                    self.llm_combo_box.setCurrentIndex(i_index)
                i_index += 1 
        # 设置布局
        self.setLayout(layout)
   
    def setHuaSuBtnFun(self):
        # 添加默认话术库
        if len(self.file_paths) == 0:
            path_default = ".\\示例_自定义本地话术库_销售.txt"
            if True == os.path.exists(path_default):
                self.file_paths = [path_default]
        self.setHuaSu_Win = SetFileDialog('设置本地话术库', self.file_paths, False)
        self.setHuaSu_Win._signal.connect(self.signal_recv_func)
        self.setHuaSu_Win.setWindowModality(Qt.ApplicationModal)
        self.setHuaSu_Win.show()
        self.setHuaSu_Win.exec_()     
        return

    def addNewLLMBtnFun(self):
        self.mainWindow.signal_of_table.emit("jump_to_setting_tab_coze") 
        self.close()
        return
    
    def confirmBtnFun(self):
        # 获取智能体的名称
        str_autoReplyName = self.autoReplyNameEdit.toPlainText()
        if len(str_autoReplyName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入客服机器人的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for autoreply_info in self.autoreply_info_list:
            if autoreply_info["autoreply_name"] == str_autoReplyName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加自动客服机器人":
            QMessageBox.information(self, APP_NAME, "机器人的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取智能体触达的客户组 
        response_usergroup = self.response_usergroup_combo_box.currentText()
        response_usergroup = response_usergroup.strip(" ")
        if len(response_usergroup) == 0:
            QMessageBox.information(self, APP_NAME, "请选择机器人负责的客户组", QMessageBox.Yes)
            return
        # 获取大模型的类型
        llm_name_sel = self.llm_combo_box.currentText()    
        if len(llm_name_sel) == 0:       
            QMessageBox.information(self, APP_NAME, "请选择使用的大模型类型", QMessageBox.Yes)
            return
        # 获取话术库
        if COZE_FRON_STR not in llm_name_sel and len(self.file_paths) == 0:
            QMessageBox.information(self, APP_NAME, "请选择机器人的话术库", QMessageBox.Yes)
            return
        
        add_autoreply_data_dict = {}
        if len(self.autoreply_name) != 0:
            add_autoreply_data_dict["autoreply_name_orig"] = self.autoreply_name
        add_autoreply_data_dict["autoreply_name"] = str_autoReplyName
        add_autoreply_data_dict["response_usergroupname"] = response_usergroup
        add_autoreply_data_dict["hua_su_file_paths"] = self.file_paths
        add_autoreply_data_dict["llm_name"] = llm_name_sel
        self._signal.emit("add_autoreply_dict_{}".format(json.dumps(add_autoreply_data_dict)))
        
        self.close()
        return

    def on_item_changed_of_response_usergroup_combo_box(self, index):
        sel_text = self.response_usergroup_combo_box.currentText()
        print("机器人负责的客户组的索引发生变化，当前选中：{}".format(sel_text))
        if sel_text == "添加...":
            self.response_usergroup_combo_box.setCurrentIndex(self.previous_index_of_response_usergroup_combo_box)
            self.addUserGroup_Win = AddUserGroupWindow("添加客户组", "", "", [], self.friend_info_list, [], self.usergroup_info_list, self)
            self.addUserGroup_Win._signal.connect(self.signal_recv_func)
            self.addUserGroup_Win.setWindowModality(Qt.ApplicationModal)
            self.addUserGroup_Win.show()
            self.addUserGroup_Win.exec_()
        else:
            self.previous_index_of_response_usergroup_combo_box = index
        return

    def signal_recv_func(self, para): 
        if para.startswith("set_friend_username_"):
            print("AddAutoReplyWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
        elif para.startswith("hua_su_file_paths_"):
            print("AddAutoReplyWindow事件收到信号:{}".format(para))
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
            labelText = "话术库文档:\n{}".format("\n".join(self.file_paths))
            self.labelHuasu.setText(labelText)   
        elif para.startswith("add_usergroup_dict_"):
            print("AddAutoReplyWindow事件收到信号:{}".format(para))
            add_usergroup_data_dict_str = para.strip("add_usergroup_dict_")
            try:
                add_usergroup_data_dict = json.loads(add_usergroup_data_dict_str)
                print(add_usergroup_data_dict)
                # 因为这个类里使用的self.usergroup_info_list是外面传进来的，当下面emit给Table发信号时，会把新数据添加到变量里，
                # 这个动作后，这里的变量也会变化的，所以这里不需要再append一次  
                #self.usergroup_info_list.append(add_usergroup_data_dict)
                self._signal.emit(para)        
                self.response_usergroupname = add_usergroup_data_dict["usergroup_name"]               
                self.reload_response_usergroup_combo_box() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
        return
                        
    def reload_response_usergroup_combo_box(self):
        self.response_usergroup_combo_box.clear()
        for usergroup_info in self.usergroup_info_list:
            self.response_usergroup_combo_box.addItem(usergroup_info["usergroup_name"])
        if len(self.usergroup_info_list) > 0:
            self.response_usergroup_combo_box.setCurrentIndex(0)
            self.previous_index_of_response_usergroup_combo_box = 0
        # 没数据时做特殊处理
        if len(self.usergroup_info_list) == 0:
            self.response_usergroup_combo_box.addItem("  ")
            self.response_usergroup_combo_box.setCurrentIndex(0)
            self.previous_index_of_response_usergroup_combo_box = 0   
        self.response_usergroup_combo_box.addItem("添加...")
        if len(self.response_usergroupname) > 0:
            for i, usergroup_info in enumerate(self.usergroup_info_list):
                if self.response_usergroupname == usergroup_info["usergroup_name"]:
                    self.response_usergroup_combo_box.setCurrentIndex(i)
                    self.previous_index_of_response_usergroup_combo_box = i
                    break
    def on_item_changed_of_llm_combo_box(self, index):
        sel_text = self.llm_combo_box.currentText()
        print("LLM的索引发生变化，当前选中：{}".format(sel_text))
        if True == sel_text.startswith(COZE_FRON_STR):
            self.setHuaSuBtn.setEnabled(False)
        else:
            self.setHuaSuBtn.setEnabled(True)
        return              
# 测试
"""
app = QApplication(sys.argv)
dialog = AddAutoReplyWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""