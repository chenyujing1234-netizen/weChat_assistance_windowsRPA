# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap
import json
import ast
import tkinter as tk
from tkinter import filedialog
from app_info import APP_NAME
from hover_label import HoverLabel
        
class AddProductWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, product_name, product_summary, product_website, file_paths, product_info_list, parent):
        super().__init__()
        self.title = title
        self.product_name = product_name
        self.product_summary = product_summary
        self.product_website = product_website
        self.file_paths = file_paths
        self.product_info_list = product_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(550), int(450))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 产品的名称
        self.layout1 = QHBoxLayout()
        self.labelProductName = HoverLabel("产品的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给将要创建的产品取个名称", self)
        self.productNameEdit = QTextEdit()
        self.productNameEdit.setPlaceholderText("在这里输入要添加的产品的名称")
        font_metrics = self.productNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.productNameEdit.setFixedHeight(line_height + 10)  # 增加一些 padding
        self.productNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.product_name) > 0:
            self.productNameEdit.setText(self.product_name)
            self.productNameEdit.setReadOnly(True)
            self.productNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                product_name = "产品" + str(i)
                if product_name not in [product_info["product_name"] for product_info in self.product_info_list]:
                    break
            self.productNameEdit.setText(product_name)
        self.layout1.addWidget(self.labelProductName)
        self.layout1.addWidget(self.productNameEdit)
        # 产品的介绍
        self.layout2 = QVBoxLayout()
        self.labelProductIntroduct = HoverLabel("产品的介绍:<font color='red'>*</font> <font color='blue'>?</font>", "用一段话描述下你的产品，描述得越具体，创建的内容文案将越贴合您的产品。\n比如产品介绍包括:产品名称、产品作用、功能特点、受众群体等", self)
        self.productIntroductEdit = QTextEdit()
        self.productIntroductEdit.setPlaceholderText("在这里输入要添加的产品的介绍")
        if len(self.product_summary) > 0:
            self.productIntroductEdit.setText(self.product_summary)
        self.layout2.addWidget(self.labelProductIntroduct)
        self.layout2.addWidget(self.productIntroductEdit)
        # 产品的官网
        self.layout3 = QHBoxLayout()
        self.labelProductWebsite = QLabel("产品的官网:")
        self.productWebsiteEdit = QTextEdit()
        self.productWebsiteEdit.setPlaceholderText("在这里输入要添加的产品的官网(选填)")
        font_metrics = self.productWebsiteEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.productWebsiteEdit.setFixedHeight(line_height + 10)  
        self.productWebsiteEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.product_website) > 0:
            self.productWebsiteEdit.setText(self.product_website)
        self.layout3.addWidget(self.labelProductWebsite)
        self.layout3.addWidget(self.productWebsiteEdit)
        # 按钮
        self.setDocsBtn = QPushButton("设置产品相关文档")
        self.setDocsBtn.clicked.connect(self.setDocsBtnFun)
        labelText = "产品相关文档:无"
        if len(self.file_paths) > 0:
            labelText = "产品相关文档:\n{}".format("\n".join(self.file_paths))
        self.labelDocs = QLabel(labelText)
        self.labelDocs.setWordWrap(True)
        ##########################################
       
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        # 创建垂直布局并添加QTabWidget
        layout = QVBoxLayout()
        layout.addLayout(self.layout1)
        layout.addLayout(self.layout2)
        layout.addLayout(self.layout3)
        layout.addWidget(self.setDocsBtn)
        layout.addWidget(self.labelDocs)
        layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(layout)

        # 设置对话框大小
        self.resize(400, 400)

    def setDocsBtnFun(self):
        # 添加默认话术库
        if len(self.file_paths) == 0:
            path_default = ".\\示例_产品文档.txt"
            if True == os.path.exists(path_default):
                self.file_paths = [path_default]
        self.setDocs_Win = SetFileDialog('设置产品文档', self.file_paths, False)
        self.setDocs_Win._signal.connect(self.signal_recv_func)
        self.setDocs_Win.setWindowModality(Qt.ApplicationModal)
        self.setDocs_Win.show()
        self.setDocs_Win.exec_()     
        return
        
    def confirmBtnFun(self):
        # 获取产品的名称
        str_productName = self.productNameEdit.toPlainText()
        if len(str_productName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入产品的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for product_info in self.product_info_list:
            if product_info["product_name"] == str_productName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加产品":
            QMessageBox.information(self, APP_NAME, "产品的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取产品的介绍
        str_productInstroduce = self.productIntroductEdit.toPlainText()
        if len(str_productInstroduce) == 0:
            QMessageBox.information(self, APP_NAME, "请输入产品的介绍", QMessageBox.Yes)
            return
        # 获取产品的官网
        str_productWebsite = self.productWebsiteEdit.toPlainText()

        add_product_data_dict = {}
        if len(self.product_name) != 0:
            add_product_data_dict["product_name_orig"] = self.product_name
        add_product_data_dict["product_name"] = str_productName
        add_product_data_dict["product_summary"] = str_productInstroduce
        add_product_data_dict["product_website"] = str_productWebsite
        add_product_data_dict["product_docs"] = self.file_paths
        self._signal.emit("add_product_dict_{}".format(json.dumps(add_product_data_dict)))
        
        self.close()
        return

    def signal_recv_func(self, para): 
        if para.startswith("set_friend_username_"):
            print("AddProductWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
        elif para.startswith("hua_su_file_paths_"):
            print("AddProductWindow事件收到信号:{}".format(para))
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
            labelText = "产品相关文档:\n{}".format("\n".join(self.file_paths))
            self.labelDocs.setText(labelText)
        return
        
# 测试
"""
app = QApplication(sys.argv)
dialog = AddProductWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""