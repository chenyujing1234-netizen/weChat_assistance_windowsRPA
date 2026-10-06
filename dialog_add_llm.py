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
from llm_helper import G_KEY_DEFAULT, check_is_llm_availed

class AddLLMWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, llm_info, llm_info_list, parent):
        super().__init__()
        self.title = title
        self.llm_type_name = llm_info["llm_type_name"]
        self.model_name = llm_info["model_name"]
        self.key = llm_info["key"]
        self.llm_info_list = llm_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(750), int(205))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # LLM的名称
        self.layout1 = QHBoxLayout()
        self.labelLLMType = HoverLabel("大模型的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的大模型取个名称", self)
        self.llmTypeEdit = QTextEdit()
        self.llmTypeEdit.setPlaceholderText("在这里输入要添加的大模型的名称")
        font_metrics = self.llmTypeEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.llmTypeEdit.setFixedHeight(line_height + 10) 
        self.llmTypeEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.llm_type_name) > 0:
            self.llmTypeEdit.setText(self.llm_type_name)
            self.llmTypeEdit.setReadOnly(True)
            self.llmTypeEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                llm_type_name = "大语言模型" + str(i)
                if llm_type_name not in [llm_info["llm_type_name"] for llm_info in self.llm_info_list]:
                    break
            self.llmTypeEdit.setText(llm_type_name)
        self.layout1.addWidget(self.labelLLMType)
        self.layout1.addWidget(self.llmTypeEdit)
        # modelName
        self.layout2 = QHBoxLayout()
        self.labelModelName = HoverLabel("使用的模型名称:<font color='red'>*</font> <font color='blue'>?</font>", "设置要使用的模型名称", self)
        self.modelNameEdit = QTextEdit()
        self.modelNameEdit.setPlaceholderText("在这里输入要使用的模型的名称")
        font_metrics = self.modelNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.modelNameEdit.setFixedHeight(line_height + 10) 
        self.modelNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.model_name) > 0:
            self.modelNameEdit.setText(self.model_name)
        self.layout2.addWidget(self.labelModelName)
        self.layout2.addWidget(self.modelNameEdit)
        # key
        self.layout3 = QHBoxLayout()
        self.labelKey = HoverLabel("调用key:<font color='red'>*</font> <font color='blue'>?</font>", "填入您从平台上获取的调用key。使用你自己的key,生成速度更快，使用公共Key,生成速度慢。", self)
        #
        self.keyEdit = QTextEdit()
        self.keyEdit.setPlaceholderText("在这里输入您从平台上获取的调用Key")
        font_metrics = self.keyEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.keyEdit.setFixedHeight(line_height + 10) 
        self.keyEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.key) > 0:
            self.keyEdit.setText(self.key)
        #
        self.useDefaultBtn = QPushButton("使用公共Key")
        self.useDefaultBtn.clicked.connect(self.useDefaultBtnFun)
        self.layout3.addWidget(self.labelKey)
        self.layout3.addWidget(self.keyEdit)
        self.layout3.addWidget(self.useDefaultBtn)
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
 
    def useDefaultBtnFun(self):
        self.keyEdit.setText(G_KEY_DEFAULT)
        return
       
    def confirmBtnFun(self):
        # 获取加友机器人的名称
        str_llmTypeName = self.llmTypeEdit.toPlainText()
        if len(str_llmTypeName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入大模型的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for llm_info in self.llm_info_list:
            if llm_info["llm_type_name"] == str_llmTypeName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加大模型":
            QMessageBox.information(self, APP_NAME, "大模型的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        
        # 获取要调用的模型名称
        str_modelName = self.modelNameEdit.toPlainText()
        if len(str_modelName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入要调用的模型的名称", QMessageBox.Yes)
            return
        # 获取key
        str_key = self.keyEdit.toPlainText()
        if len(str_key) == 0:
            QMessageBox.information(self, APP_NAME, "请输入调用key", QMessageBox.Yes)
            return
        if self.key == str_key:
            QMessageBox.information(self, APP_NAME, "输入的key是一样的", QMessageBox.Yes)
            return

        add_llm_info_dict = {}
        if len(self.llm_type_name) != 0:
            add_llm_info_dict["llm_type_name_orig"] = self.llm_type_name
        add_llm_info_dict["llm_type_name"] = str_llmTypeName
        add_llm_info_dict["llm_type"] = LLM_MODEL_NAME_TYPE_DICT[str_llmTypeName].name
        add_llm_info_dict["model_name"] = str_modelName
        add_llm_info_dict["key"] = str_key
        if True == check_is_llm_availed(add_llm_info_dict):
            QMessageBox.information(self, APP_NAME, "测试通过，大模型信息修改成功。", QMessageBox.Yes)
        else:
            QMessageBox.information(self, APP_NAME, "测试不通过（可能是key不可用），大模型信息修改失败。", QMessageBox.Yes)    
            return
        # 发送信号
        self._signal.emit("add_llm_info_dict_{}".format(json.dumps(add_llm_info_dict)))
        
        self.close()

        return
                    
# 测试
"""
app = QApplication(sys.argv)
dialog = AddLLMWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""