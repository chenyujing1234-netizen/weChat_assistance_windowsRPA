# -*- coding: utf-8 -*-
import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
import tkinter as tk
from tkinter import filedialog
from dialog_file_item import FileItem
import json
from datetime import datetime
        
# 随机生成一个11位的手机号码
def generate_phone_number():
    # 定义常见的手机号码号段
    prefix_list = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                   '147', '148', '149', '150', '151', '152', '153', '155', '156', '157',
                   '158', '159']
    
    # 随机选择一个号段
    prefix = random.choice(prefix_list)
    
    # 随机生成后8位数字
    suffix = ''.join(random.choices('0123456789', k=8))
    
    # 拼接完整的手机号码
    phone_number = prefix + suffix
    
    return phone_number

# 测试函数
#for i in range(0, 10):
#    print(generate_phone_number())

class AddFriendWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('添加好友')
        self.resize(int(550), int(350))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 第1个tab:好友列表文件
        self.tab1 = QWidget()
        
        self.layout1 = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.layout1.addWidget(self.list_widget)
       # 加载列表中的内容
        self.load_list_item_data()
        self.add_button = QPushButton('增加')
        self.add_button.clicked.connect(self.add_file)
        self.layout1.addWidget(self.add_button)
        
        # 将布局应用到标签页
        self.tab1.setLayout(self.layout1)
        #########################################
        # 第2个tab:规则批量
        self.tab2 = QWidget()
        self.layout2 = QVBoxLayout()
        self.label2 = QLabel("规则随机批量")
        self.layout2.addWidget(self.label2)
        # 将布局应用到标签页
        #self.tab2.setLayout(self.layout2)
        ##########################################

        # 将表格添加到QTabWidget中
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.tab1, "好友列表文件")
        #self.tab_widget.addTab(self.tab2, "规则随机批量")

        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        # 创建垂直布局并添加QTabWidget
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(layout)

        # 设置对话框大小
        self.resize(400, 300)
        
    def load_list_item_data(self):
        self.list_widget.clear()
        
        for path in self.file_paths:
            item = QListWidgetItem(self.list_widget)
            file_item = FileItem(path, self)
            item.setSizeHint(file_item.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, file_item)
        self.adjust_dialog_width()
        
        return  
        
    def adjust_dialog_width(self):
        max_width = int(450/1920*g_desktop_w)
        for item in self.list_widget.findItems("", Qt.MatchWildcard):
            width = self.list_widget.visualItemRect(item).width()
            if width > max_width:
                max_width = width
        self.resize(max_width + 50, self.height())  # 加上一些额外的空间
        
    def add_file(self):
        # 创建一个Tkinter根窗口，但不显示
        root = tk.Tk()
        root.withdraw()

        # 打开文件选择对话框，设置过滤器只显示TXT文件
        file_path = filedialog.askopenfilename(
            title='选择一个TXT文件',
            filetypes=[('Text files', '*.txt')]
        )

        # 检查用户是否选择了文件
        if file_path:
            print(f'选择的文件路径: {file_path}')
            self.file_paths.append(file_path)
            self.load_list_item_data()
        else:
            print('没有选择文件')
        return 
        
    def confirmBtnFun(self):
        #print_my("confirmBtnFun, 设置话术知识库文件列表:{}".format(self.file_paths))
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')

        add_friend_data_dict = {}
        add_friend_data_dict["file_paths"] = self.file_paths
        add_friend_data_dict["date"] = date
        add_friend_data_dict["time"] = time
        self._signal.emit("add_friend_dict_{}".format(json.dumps(add_friend_data_dict)))
        self.close()
        return
        
# 测试
"""
app = QApplication(sys.argv)
dialog = AddFriendDialog()
dialog.show()
sys.exit(app.exec_())
"""