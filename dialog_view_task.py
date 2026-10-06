# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QTableView, QHeaderView
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
import json
import ast
import tkinter as tk
from tkinter import filedialog
from app_info import APP_NAME
from hover_label import HoverLabel
from error_code import *
        
class ViewTaskWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, task_info, parent):
        super().__init__()
        self.title = title
        self.task_info = task_info
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
		# 创建任务列表控件
        self.layout_itemlist = QVBoxLayout()
        self.itemTableView=QTableView()
        self.itemModel=QStandardItemModel(0, 2);
        #self.taskModel.setHorizontalHeaderLabels(['任务类型', '任务描述', '任务进度'])
        self.itemTableView.setModel(self.itemModel)
        self.itemTableView.setItemDelegateForColumn(1, ReadOnlyDelegate())
        #下面代码让表格100%填满窗口
        self.itemTableView.horizontalHeader().setStretchLastSection(True)
        self.itemTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout_itemlist.addWidget(self.itemTableView)
        # 填充数据
        self.reload_item_list_view()
        
        # 设置布局
        # 创建垂直布局并添加QTabWidget
        layout = QVBoxLayout()
        layout.addLayout(self.layout_itemlist)
        self.setLayout(layout)

        # 设置对话框大小
        self.resize(400, 400)
        
    def reload_item_list_view(self):

        self.itemModel.clear()
        self.itemModel.setHorizontalHeaderLabels(['子项', '状态', '执行时间'])
        task_detail_data = self.task_info["task_detail_data"]
        task_finish_detail_data = self.task_info["task_finish_detail_data"]
        for i, task_detail_item in enumerate(task_detail_data):
            item0_0 = QStandardItem(task_detail_item)
            item0_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            # 1.
            self.itemModel.setItem(i, 0, item0_0)
            
            finish_detail_data = {}
            for task_finish_detail_item in task_finish_detail_data:
                name_of_finish = task_finish_detail_item
                if "name" in task_finish_detail_item:
                    name_of_finish = task_finish_detail_item["name"]
                if name_of_finish == task_detail_item:
                    finish_detail_data = task_finish_detail_item
                    break
            #
            if len(finish_detail_data) == 0:
                self.itemModel.setItem(i, 1, QStandardItem("待执行"))
                self.itemModel.setItem(i, 2, QStandardItem(""))
            else:
                # 2.状态
                if "result_code" in finish_detail_data:
                    if finish_detail_data["result_code"] == APP_RET_CODE_SUCESS:
                        self.itemModel.setItem(i, 1, QStandardItem("成功"))
                    else:
                    	self.itemModel.setItem(i, 1, QStandardItem("失败"))
                else:
                    self.itemModel.setItem(i, 1, QStandardItem("已完成"))
                # 3.执行时间
                if "happen_time" in finish_detail_data:
                    self.itemModel.setItem(i, 2, QStandardItem(finish_detail_data["happen_time"]))
                else:
                    self.itemModel.setItem(i, 2, QStandardItem(""))
        return 

# 测试
"""
app = QApplication(sys.argv)
dialog = ViewTaskWindow("查看任务信息", None, None)
dialog.show()
sys.exit(app.exec_())
"""