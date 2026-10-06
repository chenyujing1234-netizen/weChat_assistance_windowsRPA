# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QStyledItemDelegate
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_file_item import FileItem
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap
import json
import ast
import tkinter as tk
from tkinter import filedialog
from app_info import APP_NAME
from log_helper import print_my

class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return
        
class SetFileDialog(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, file_paths, b_auto_start_after = False):
        super().__init__()
        self.title = title
        self.file_paths = file_paths
        self.b_auto_start_after = b_auto_start_after
        self.initUI()
        return

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        #self.resize(int(450/1920*g_desktop_w), int(300/1080*g_desktop_h))
        # 禁止窗口大小拉伸
        #self.setFixedSize(self.width(), self.height())
        
        layout = QVBoxLayout()

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)
        
        # 加载列表中的内容
        self.load_list_item_data()
        
        self.add_button = QPushButton('增加')
        self.add_button.clicked.connect(self.add_file)
        layout.addWidget(self.add_button)
        
        self.confirmBtn = QPushButton('确定')
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        layout.addWidget(self.confirmBtn)
        
        self.setLayout(layout)
        return
        
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
        max_width = int(450/1920*1920)
        for item in self.list_widget.findItems("", Qt.MatchWildcard):
            width = self.list_widget.visualItemRect(item).width()
            if width > max_width:
                max_width = width
        self.resize(max_width + 50, self.height())  # 加上一些额外的空间
        
    def open_file(self, file_path):
        try:
            os.startfile(file_path)
        except Exception as e:
            print("打开文件{},出现异常:\n{}".format(file_path, e))
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
        print_my("confirmBtnFun, 设置文件列表:{}".format(self.file_paths))
        self.close()
        return
        
    """
    重写closeEvent方法
    """
    def closeEvent(self, event):
        print_my("SetFileDialog, 设置文件列表:{}".format(self.file_paths))
        self._signal.emit("hua_su_file_paths_{}_b_auto_start_after_{}".format(self.file_paths, self.b_auto_start_after))
        self.close()
        return