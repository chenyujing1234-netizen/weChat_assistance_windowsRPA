# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox
from dialog_set_friend_object import SetFriendObjectWindow
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap
import json
import ast
import tkinter as tk
from tkinter import filedialog
from app_info import APP_NAME
        
class SendCircleWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, username_of_can_deposit_list, username_of_can_see_list, img_paths, parent):
        super().__init__()
        self.mainWindow = parent
        self.username_of_can_deposit_list = username_of_can_deposit_list
        self.username_of_can_see_list = username_of_can_see_list
        self.img_paths = img_paths
        self.initUI()
        self.load_img_data()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('定时发送朋友圈')
        self.resize(int(550), int(450))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 第1个tab: 固定文案
        self.tab1 = QWidget()
        self.layout1 = QVBoxLayout()
        self.wenAnEdit = QTextEdit()
        self.wenAnEdit.setPlaceholderText("在这里输入要发送的朋友圈的文本")
        self.layout1.addWidget(self.wenAnEdit)
        self.tab1.setLayout(self.layout1)
        # 第2个tab:图片
        self.tab2 = QWidget()
        self.layout2 = QVBoxLayout()
        self.imageLabel = QLabel("图片")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.selectImgBtn = QPushButton("选择图片")
        self.selectImgBtn.clicked.connect(self.selectImgBtnFun)
        self.layout2.addWidget(self.imageLabel)
        self.layout2.addWidget(self.selectImgBtn)
        self.tab2.setLayout(self.layout2)
        ##########################################
        # 将表格添加到QTabWidget中
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.tab1, "固定文案")
        self.tab_widget.addTab(self.tab2, "图片")

        # 创建日期时间选择器
        self.dateEdit = QDateEdit(QDate.currentDate())
        self.dateEdit.setDateRange(QDate(2020, 1, 1), QDate(2030, 12, 31))
        self.timeEdit = QTimeEdit(QTime.currentTime())
        # 设置可见对象 
        self.setCanSeeBtn = QPushButton("设置可见好友")
        self.setCanSeeBtn.clicked.connect(self.setCanSeeBtnFun)
        self.labelCanSeeFriend = QLabel("可见好友:无")
        self.labelCanSeeFriend.setWordWrap(True)
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        # 创建垂直布局并添加QTabWidget
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.dateEdit)
        layout.addWidget(self.timeEdit)
        layout.addWidget(self.setCanSeeBtn)
        layout.addWidget(self.labelCanSeeFriend)
        layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(layout)

        # 设置对话框大小
        self.resize(400, 400)
        
    def confirmBtnFun(self):
        # 获取文案
        str_wenAn = self.wenAnEdit.toPlainText()
        if len(str_wenAn) == 0:
            QMessageBox.information(self, APP_NAME, "请输入文案", QMessageBox.Yes)
            return
        # 获取日期和时间
        date = self.dateEdit.date().toString('yyyy-MM-dd')
        time = self.timeEdit.time().toString('HH:mm:ss')
        print(f'选择的日期是：{date}，选择的时间是：{time}')
        circle_data_dict = {}
        circle_data_dict["wenAn"] = str_wenAn
        circle_data_dict["img_paths"] = self.img_paths
        circle_data_dict["date"] = date
        circle_data_dict["time"] = time
        circle_data_dict["username_of_can_see_list"] = self.username_of_can_see_list
        self._signal.emit("send_circle_dict_{}".format(json.dumps(circle_data_dict)))
        
        self.close()
        return
        
    def setCanSeeBtnFun(self):
        self.setCanSeeObject_Win = SetFriendObjectWindow('设置可见好友窗口', self.username_of_can_deposit_list, self.username_of_can_see_list)
        self.setCanSeeObject_Win._signal.connect(self.signal_recv_func)
        self.setCanSeeObject_Win.setWindowModality(Qt.ApplicationModal)
        self.setCanSeeObject_Win.show()
        self.setCanSeeObject_Win.exec_()
        
        return
        
    def selectImgBtnFun(self):
        # 创建一个Tkinter根窗口，但不显示
        root = tk.Tk()
        root.withdraw()

        # 打开文件选择对话框，设置过滤器只显示图片文件
        file_path = filedialog.askopenfilename(
            title='选择图片',
            filetypes=[("图片文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("所有文件", "*.*")]
        )

        # 检查用户是否选择了图片
        if file_path:
            print(f'选择的图片路径: {file_path}')
            self.img_paths.append(file_path)
            self.load_img_data()
        else:
            print('没有选择图片')
        return
        
    def load_img_data(self):
        # 加载并显示图片
        for img_path in self.img_paths:
            pixmap = QPixmap(img_path)
            self.imageLabel.setPixmap(pixmap.scaled(
                self.imageLabel.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )) 
            # 先只设置一张图片
            break 
        
    def signal_recv_func(self, para): 
        if para.startswith("set_friend_username_"):
            print("SendCircleWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_can_see_list = usename_list
            labelText = "可见好友:{}".format("、".join(self.username_of_can_see_list))
            self.labelCanSeeFriend.setText(labelText)
            
        return
        
# 测试
"""
app = QApplication(sys.argv)
dialog = SendCircleWindow(["aaa", "bbb"], ["aaa"], [], None)
dialog.show()
sys.exit(app.exec_())
"""