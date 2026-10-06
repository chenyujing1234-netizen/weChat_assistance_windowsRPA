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
from app_info import APP_NAME, REMARK_PREFIX_TYPE_LIST_FOR_PASS, LLM_MODEL_NAME_TYPE_DICT, LLM_MODEL_TYPE_NAME_DICT
from hover_label import HoverLabel
from coze_helper import check_is_coze_agent_availed

class AddCozeAgentWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, coze_agent_info, coze_agent_info_list, parent):
        super().__init__()
        self.title = title
        self.agent_name = ""
        if "agent_name" in coze_agent_info:
            self.agent_name = coze_agent_info["agent_name"]
        self.bot_id = ""
        if "bot_id" in coze_agent_info:
            self.bot_id = coze_agent_info["bot_id"]
        self.api_token = ""
        if "api_token" in coze_agent_info:
            self.api_token = coze_agent_info["api_token"]
        self.coze_agent_info_list = coze_agent_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(850), int(205))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 智能体的名称
        self.layout1 = QHBoxLayout()
        self.labelAgentName = HoverLabel("智能体名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要添加的扣子智能体随意取个名称", self)
        self.agentNameEdit = QTextEdit()
        self.agentNameEdit.setPlaceholderText("在这里输入要添加的扣子智能体的名称（可随意取）")
        font_metrics = self.agentNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.agentNameEdit.setFixedHeight(line_height + 10) 
        self.agentNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.agentNameEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.agentNameEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.agentNameEdit.setAcceptRichText(False)
        if len(self.agent_name) > 0:
            self.agentNameEdit.setText(self.agent_name)
            self.agentNameEdit.setReadOnly(True)
            self.agentNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                agent_name = "扣子智能体" + str(i)
                if agent_name not in [coze_agent_info["agent_name"] for coze_agent_info in self.coze_agent_info_list]:
                    break
            self.agentNameEdit.setText(agent_name)
        self.layout1.addWidget(self.labelAgentName)
        self.layout1.addWidget(self.agentNameEdit)
        # BOT_ID
        self.layout2 = QHBoxLayout()
        self.labelBotId = HoverLabel("BotId:<font color='red'>*</font> <font color='blue'>?</font>", "设置Coze智能体的BOT ID", self)
        self.botIdEdit = QTextEdit()
        self.botIdEdit.setPlaceholderText("在这里输入要使用的扣子智能体的Bot Id")
        font_metrics = self.botIdEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.botIdEdit.setFixedHeight(line_height + 10) 
        self.botIdEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.botIdEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.botIdEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.botIdEdit.setAcceptRichText(False)
        if len(self.bot_id) > 0:
            self.botIdEdit.setText(self.bot_id)
        self.layout2.addWidget(self.labelBotId)
        self.layout2.addWidget(self.botIdEdit)
        # api token
        self.layout3 = QHBoxLayout()
        self.labelApiToken = HoverLabel("api token:<font color='red'>*</font> <font color='blue'>?</font>", "填入Coze智能体的API token。", self)
        #
        self.apiTokenEdit = QTextEdit()
        self.apiTokenEdit.setPlaceholderText("在这里输入您从平台上获取的扣子智能体的api token")
        font_metrics = self.apiTokenEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.apiTokenEdit.setFixedHeight(line_height + 10) 
        self.apiTokenEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.apiTokenEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.apiTokenEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.apiTokenEdit.setAcceptRichText(False)
        if len(self.api_token) > 0:
            self.apiTokenEdit.setText(self.api_token)
        #
        self.layout3.addWidget(self.labelApiToken)
        self.layout3.addWidget(self.apiTokenEdit)
        ##########################################
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        # 创建垂直布局并添加QTabWidget
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        self.layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(self.layout)
       
    def confirmBtnFun(self):
        # 获智能体的名称
        str_agentName = self.agentNameEdit.toPlainText()
        if len(str_agentName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入智能体的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for coze_agent_info in self.coze_agent_info_list:
            if coze_agent_info["agent_name"] == str_agentName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加扣子智能体":
            QMessageBox.information(self, APP_NAME, "扣子智能体的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        
        # 获取BOT_ID
        str_botId = self.botIdEdit.toPlainText()
        if len(str_botId) == 0:
            QMessageBox.information(self, APP_NAME, "请输入Bot Id", QMessageBox.Yes)
            return
        # 获取api token
        str_apiToken = self.apiTokenEdit.toPlainText()
        if len(str_apiToken) == 0:
            QMessageBox.information(self, APP_NAME, "请输入api token", QMessageBox.Yes)
            return
        if self.api_token == str_apiToken:
            QMessageBox.information(self, APP_NAME, "输入的 api token 是一样的", QMessageBox.Yes)
            return

        add_coze_agent_dict = {}
        if len(self.agent_name) != 0:
            add_coze_agent_dict["agent_name_orig"] = self.agent_name
        add_coze_agent_dict["agent_name"] = str_agentName
        add_coze_agent_dict["bot_id"] = str_botId
        add_coze_agent_dict["api_token"] = str_apiToken
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
        # 发送信号
        self._signal.emit("add_coze_agent_dict_{}".format(json.dumps(add_coze_agent_dict)))
        
        self.close()

        return
                    
# 测试
"""
app = QApplication(sys.argv)
dialog = AddCozeAgentWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""