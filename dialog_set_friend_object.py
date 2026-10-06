# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel, QLineEdit, QMessageBox, QListWidget, QCheckBox
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QProcess, QProcessEnvironment
from dialog_add_can_see_object import AddCanSeeObjectWindow
from app_info import *


# 设置好友对话框
class SetFriendObjectWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, friend_info_list, username_of_deposit_list):
        super().__init__()
        self.title = title
        # 把“通用用对象”排除掉
        self.username_of_can_deposit_list = []
        for friend_info in friend_info_list:
            username = friend_info["friend_name"]
            if username == USERNAME_FOR_NOTICE:
                continue 
            self.username_of_can_deposit_list.append(username)
        self.username_of_deposit_list = username_of_deposit_list
        self.initUI()
 
    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(450), int(500))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        dlgLayout=QVBoxLayout()
        
        # 输入框 
        """
        self.usernameEdit = QTextEdit()
        self.usernameEdit.setPlaceholderText("请输入要托管的微信聊天对象的完整昵称")
        labelLayout3 = QHBoxLayout()
        labelLayout3.addWidget(self.usernameEdit)
        """
        
        # 添加搜索框
        self.searchEdit = QLineEdit(self)
        self.searchEdit.setPlaceholderText("搜索好友")
        self.searchEdit.textChanged.connect(self.filter_list)  # 连接搜索框的文本变化信号
        
        # 列表控件
        listLayout = QVBoxLayout()
        self.listWidget = QListWidget(self)
        self.listWidget.setSelectionMode(QListWidget.MultiSelection)  # 设置为多选模式
        # 添加列表项
        #for i, item_str in enumerate(self.username_of_can_deposit_list):
        #    self.listWidget.addItem(item_str)
        listLayout.addWidget(self.listWidget)
        self.reload_list_view()
        
        self.addBtn = QPushButton("手动输入好友名称")
        self.addBtn.clicked.connect(self.addBtnFun)
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        
        #dlgLayout.addLayout(labelLayout3)
        dlgLayout.addWidget(self.searchEdit)  # 将搜索框添加到布局中
        dlgLayout.addLayout(listLayout)
        dlgLayout.addWidget(self.addBtn)
        dlgLayout.addWidget(self.confirmBtn)
        
        self.setLayout(dlgLayout)
        return
        
    def reload_list_view(self):
        self.listWidget.clear()
        # 添加列表项
        for i, item_str in enumerate(self.username_of_can_deposit_list):
            self.listWidget.addItem(item_str)
        # 显示窗口时，添加勾选框
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            checkbox = QCheckBox(self.listWidget)
            checkbox.setText(item.text())
            if item.text() in self.username_of_deposit_list:
                checkbox.setChecked(True)
            item.setText("")
            item.setSizeHint(checkbox.sizeHint())
            self.listWidget.setItemWidget(item, checkbox)

    def filter_list(self):
        filter_text = self.searchEdit.text().lower()
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            checkbox = self.listWidget.itemWidget(item)
            if filter_text and filter_text not in checkbox.text().lower():
                item.setHidden(True)  # 隐藏不匹配的项
            else:
                item.setHidden(False)  # 显示匹配的项
                    
    def getSelectedItems(self):
        selected_items = []
        for i in range(self.listWidget.count()):
            item_checkbox = self.listWidget.itemWidget(self.listWidget.item(i))
            if item_checkbox.isChecked():
                selected_items.append(item_checkbox.text())
        return selected_items
        
    def addBtnFun(self):
        self.addCanSeeObject_Win = AddCanSeeObjectWindow(self.username_of_can_deposit_list, self)
        self.addCanSeeObject_Win._signal.connect(self.signal_recv_func)
        self.addCanSeeObject_Win.setWindowModality(Qt.ApplicationModal)
        self.addCanSeeObject_Win.show()
        self.addCanSeeObject_Win.exec_()
        return
        
    def confirmBtnFun(self):
        selected_items = self.getSelectedItems()
        
        #if len(selected_items) == 0:
        #    QMessageBox.information(self, APP_NAME, "请选择托管对象的昵称", QMessageBox.Yes)
        #    return
        print("您选中的可见好友的用户名是:{}".format(selected_items))
        self._signal.emit("set_friend_username_{}".format(selected_items))
        self.close()
        return
        
    def signal_recv_func(self, para):
        global g_config_json_data
        global g_config_path
        
        if para.startswith("add_can_see_object_"):
            print("SetFriendObjectWindow事件收到信号:{}".format(para))
            
            username_str = para.replace("add_can_see_object_", "")
            print("SetFriendObjectWindow, signal_recv_func, 添加新的可见对象:{}".format(username_str))
            self.username_of_can_deposit_list.append(username_str)
            self.username_of_deposit_list.append(username_str)
            # 保存到列表中
            #g_config_json_data["username_of_can_deposit_list"] = self.username_of_can_deposit_list
            #save_config_data(g_config_json_data, g_config_path)  
                
            self.reload_list_view() 
        return
        

# 测试
"""
app = QApplication(sys.argv)
dialog = SetFriendObjectWindow()
dialog.show()
sys.exit(app.exec_())
"""