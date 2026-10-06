# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QSpacerItem, QLineEdit, QSizePolicy
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
from app_info import APP_NAME, REMARK_PREFIX_TYPE_LIST
from datetime import datetime, timedelta
from hover_label import HoverLabel

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
    
#STRATEGY_TYPE_LIST = ["仅1天", "连续5天", "连续10天", "连续20天"] 
#STRATEGY_TYPE_LIST = ["仅1天"] 
STRATEGY_TYPE_LIST = ["每天10个直到完成", "每天20个直到完成", "每天30个直到完成"] 
ADD_MODEL_LIST = ["微信群", "自动", "手动"] 
#ADD_MODEL_LIST = ["自动", "手动"] 
class AddAutoAddWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, autoadd_name, strategy_type, remark_prefix, add_model_name, start_time, willing_add_count_list, file_paths, autoadd_info_list, parent):
        super().__init__()
        self.title = title
        self.autoadd_name = autoadd_name
        self.strategy_type = strategy_type
        self.remark_prefix = remark_prefix
        self.add_model_name = add_model_name
        self.start_time = start_time
        self.willing_add_count_list = willing_add_count_list
        self.file_paths = file_paths
        self.autoadd_info_list = autoadd_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(550), int(465))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 获客机器人的名称
        self.layout1 = QHBoxLayout()
        self.labelAutoAddName = HoverLabel("获客机器人的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的自动加好友机器人取个名称吧", self)
        self.autoAddNameEdit = QTextEdit()
        self.autoAddNameEdit.setPlaceholderText("在这里输入要添加的获客机器人的名称")
        font_metrics = self.autoAddNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.autoAddNameEdit.setFixedHeight(line_height + 10) 
        self.autoAddNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.autoadd_name) > 0:
            self.autoAddNameEdit.setText(self.autoadd_name)
            self.autoAddNameEdit.setReadOnly(True)
            self.autoAddNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                autoadd_name = "获客智能体" + str(i)
                if autoadd_name not in [autoadd_info["autoadd_name"] for autoadd_info in self.autoadd_info_list]:
                    break
            self.autoAddNameEdit.setText(autoadd_name)
        self.layout1.addWidget(self.labelAutoAddName)
        self.layout1.addWidget(self.autoAddNameEdit)
        # 机器人策略
        self.layout2 = QHBoxLayout()
        self.labelStrategy = HoverLabel("机器人策略:<font color='red'>*</font> <font color='blue'>?</font>", "你想定制持续几天的自动加好友的任务", self)
        self.strategy_combo_box = QComboBox(self)
        for strategy_name in STRATEGY_TYPE_LIST:
            self.strategy_combo_box.addItem(strategy_name)
        self.strategy_combo_box.setCurrentIndex(0) 
        if len(self.strategy_type) > 0:
            for i, strategy_name in enumerate(STRATEGY_TYPE_LIST):
                if self.strategy_type == strategy_name:
                    self.strategy_combo_box.setCurrentIndex(i)
                    break
        self.layout2.addWidget(self.labelStrategy)
        self.layout2.addWidget(self.strategy_combo_box)
        # 备注前缀
        self.layout3 = QHBoxLayout()
        self.labelRemarkPrefix = HoverLabel("好友备注前缀:<font color='red'>*</font> <font color='blue'>?</font>", "你自动加的好友，如果对方通过了，你要在此好友的前缀备注什么内容呢?", self)
        self.remark_prefix_combo_box = QComboBox(self)
        for remark_prefix in REMARK_PREFIX_TYPE_LIST:
            self.remark_prefix_combo_box.addItem(remark_prefix)
        self.remark_prefix_combo_box.setCurrentIndex(0) 
        if len(self.remark_prefix) > 0:
            for i, remark_prefix in enumerate(REMARK_PREFIX_TYPE_LIST):
                if self.remark_prefix == remark_prefix:
                    self.remark_prefix_combo_box.setCurrentIndex(i)
                    break
        self.layout3.addWidget(self.labelRemarkPrefix)
        self.layout3.addWidget(self.remark_prefix_combo_box)
        # 启动时间
        self.layout4 = QHBoxLayout()
        self.labelStartTime = HoverLabel("启动时间:<font color='red'>*</font> <font color='blue'>?</font>", "设置在每天什么时间启动加好友的动作", self)
        self.starTimeEdit = QTimeEdit(QTime.currentTime())
        self.layout4.addWidget(self.labelStartTime)
        self.layout4.addWidget(self.starTimeEdit)
        # 添加方式
        self.layout5 = QHBoxLayout()
        self.labelAddModel = HoverLabel("账号来源:<font color='red'>*</font> <font color='blue'>?</font>", "你要加的好友的账号来源于哪里呢？", self)
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
        self.layout5.addWidget(self.labelAddModel)
        for add_model_radio_button in self.add_model_radio_button_list:
            self.layout5.addWidget(add_model_radio_button)
            if self.title == "编辑加好友机器人":
                add_model_radio_button.setEnabled(False)
            
        # 创建一个占位标签，用于动态显示内容
        self.dynamic_layout = QVBoxLayout()
        
        ##########################################

        # 创建垂直布局并添加QTabWidget
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        self.layout.addLayout(self.layout4)
        self.layout.addLayout(self.layout5)
        self.layout.addLayout(self.dynamic_layout)
        
        # 设置布局
        self.setLayout(self.layout)
        
        self.update_add_model_dynamic_content()

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
            model_name_sel = ADD_MODEL_LIST[i]
            if add_model_radio_button.isChecked():
                if model_name_sel == "微信群":
                    # 微信群名称
                    self.group_name_layout = QHBoxLayout()
                    self.labelGroupName = HoverLabel("群信群的名称:<font color='red'>*</font> <font color='blue'>?</font>", "指定群信昵称，机器人将按安全的策略添加群里的成员。", self)
                    self.groupNameEdit = QLineEdit(self)
                    self.groupNameEdit.setPlaceholderText("在这里输入群信群的名称")
                    self.group_name_layout.addWidget(self.labelGroupName)
                    self.group_name_layout.addWidget(self.groupNameEdit)
                    # label
                    self.label_gui_ze = QLabel("执行策略(<font color='red'>非常关键，防止被封号</font>)：")
                    # 每天最多个数
                    self.one_day_max_count_layout = QHBoxLayout()
                    label_one_day_left = QLabel("1.每天最多")
                    self.input_box_one_day = QLineEdit()
                    self.input_box_one_day.setValidator(QIntValidator(0, 99))  # 设置输入范围为0到99
                    self.input_box_one_day.setMaxLength(2)  # 设置最大输入长度为2
                    self.input_box_one_day.setFixedWidth(50)  # 设置输入框宽度为50像素
                    #if len(self.rule_info_list) > 0:
                    #    str_start_day = str(self.rule_info_list[0]["DAYS_AFTER_ADD"]["START_DAY"])
                    #    self.input_box_one_day.setText(str_start_day)
                    #else:
                    #    self.input_box_one_day.setText("0")
                    self.input_box_one_day.setText("20")

                    label_one_day_right = QLabel("个")
                    self.one_day_max_count_layout.addWidget(label_one_day_left)
                    self.one_day_max_count_layout.addWidget(self.input_box_one_day)
                    self.one_day_max_count_layout.addWidget(label_one_day_right)
                    self.one_day_max_count_layout.addStretch(1) 
                    # 每个成员添加时间间隔
                    self.add_frequency_layout = QHBoxLayout()
                    label_add_frequency_left = QLabel("2.间隔")
                    self.input_box_add_inter = QLineEdit()
                    self.input_box_add_inter.setValidator(QIntValidator(0, 99))  # 设置输入范围为0到99
                    self.input_box_add_inter.setMaxLength(2)  # 设置最大输入长度为2
                    self.input_box_add_inter.setFixedWidth(50)  # 设置输入框宽度为50像素
                    #if len(self.rule_info_list) > 0:
                    #    str_start_day = str(self.rule_info_list[0]["DAYS_AFTER_ADD"]["END_DAY"])
                    #    self.input_box_add_inter.setText(str_start_day)
                    #else:
                    #    self.input_box_add_inter.setText("7")
                    self.input_box_add_inter.setText("30")
                    label_add_frequency_right = QLabel("分钟执行对此群一部分成员的添加")
                    self.add_frequency_layout.addWidget(label_add_frequency_left)
                    self.add_frequency_layout.addWidget(self.input_box_add_inter)
                    self.add_frequency_layout.addWidget(label_add_frequency_right)
                    self.add_frequency_layout.addStretch(1) 
                    
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
                    
                    self.dynamic_layout.addLayout(self.group_name_layout)
                    self.dynamic_layout.addWidget(self.label_gui_ze)
                    self.dynamic_layout.addLayout(self.one_day_max_count_layout)
                    self.dynamic_layout.addLayout(self.add_frequency_layout)
                    # 添加一个伸缩空间，让第一个控件顶上显示
                    spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
                    self.dynamic_layout.addSpacerItem(spacer)
                    self.dynamic_layout.addWidget(self.confirmBtn)
                elif model_name_sel == "自动":
                    # 个数
                    self.count_layout = QHBoxLayout()
                    self.labelAccountCount = HoverLabel("账号个数:<font color='red'>*</font> <font color='blue'>?</font>", "每天要加的账号的个数是多少呢？\n我将根据你的要求来自动生成对应个数的账号", self)
                    self.accountCountEdit = QLineEdit(self)
                    self.accountCountEdit.setPlaceholderText("在这里输入要生成的账号的个数")
                    int_validator = QIntValidator(1, 10000)
                    self.accountCountEdit.setValidator(int_validator)
                    self.accountCountEdit.setText("10")
                    if len(self.willing_add_count_list) > 0:
                        self.accountCountEdit.setText(str(len(self.willing_add_count_list)))
                    self.count_layout.addWidget(self.labelAccountCount)
                    self.count_layout.addWidget(self.accountCountEdit)
                    # 生成按钮
                    self.button_generate = QPushButton("开始自动生成手机号", self)
                    self.button_generate.setStyleSheet("""
                        QPushButton {
                            color: blue;          /* 设置字体颜色为蓝色 */
                            font-weight: bold;    /* 设置字体为粗体 */
                            font-size: 14px;      /* 可选：设置字体大小 */
                        }
                    """)
                    self.button_generate.setFixedWidth(self.width() // 5)
                    self.button_generate.clicked.connect(self.generateBtnFun)
                    # 列表
                    self.addFriendListView = QListWidget()
                    #self.addFriendListView.addItems(self.willing_add_count_list)
                    self.reload_account_data_layout()
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
                    
                    self.dynamic_layout.addLayout(self.count_layout)
                    self.dynamic_layout.addWidget(self.button_generate)
                    self.dynamic_layout.addWidget(self.addFriendListView)
                    self.dynamic_layout.addWidget(self.confirmBtn)
                elif model_name_sel == "手动":
                    self.manualSetCountBtn = QPushButton("手动设置待添加微信号")
                    self.manualSetCountBtn.clicked.connect(self.manualSetCountBtnFun)
                    self.labelWillAddCountFile = QLabel("待添加微信号文件:无")
                    self.labelWillAddCountFile.setWordWrap(True)
                    self.reload_will_add_count_from_files()
                    # 确定按钮
                    self.confirmBtn = QPushButton("确定")
                    self.confirmBtn.clicked.connect(self.confirmBtnFun)
                    
                    self.dynamic_layout.addWidget(self.manualSetCountBtn)
                    self.dynamic_layout.addWidget(self.labelWillAddCountFile)
                    self.dynamic_layout.addWidget(self.confirmBtn)
                break 
                
        self.layout.addLayout(self.dynamic_layout)

    def reload_account_data_layout(self):
        self.addFriendListView.clear()
        self.addFriendListView.addItems(self.willing_add_count_list)
        if len(self.willing_add_count_list) == 0:
            self.button_generate.setText("开始生成手机号")
        else:
            self.button_generate.setText("重新生成手机号")
            
    def confirmBtnFun(self):
        groupName = ""
        max_count_one_day = ""
        group_add_inter = ""
        self.group_add_rule_info = {}
        
        # 获取获客机器人的名称
        str_autoAddName = self.autoAddNameEdit.toPlainText()
        if len(str_autoAddName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入获客机器人的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for autoadd_info in self.autoadd_info_list:
            if autoadd_info["autoadd_name"] == str_autoAddName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加加好友机器人":
            QMessageBox.information(self, APP_NAME, "机器人的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取机器人策略 
        strategy_type = self.strategy_combo_box.currentText()
        if len(strategy_type) == 0:
            QMessageBox.information(self, APP_NAME, "请选择机器人的策略", QMessageBox.Yes)
            return
        # 获取备注前缀
        remark_prefix = self.remark_prefix_combo_box.currentText()
        if len(remark_prefix) == 0:
            QMessageBox.information(self, APP_NAME, "请选择好友备注前缀", QMessageBox.Yes)
            return
        # 获取启动时间
        start_time = self.starTimeEdit.time().toString('HH:mm:ss')
        print(f'选择的启动时间是：{start_time}')
        # 获取添加方式    
        for i, add_model_radio_button in enumerate(self.add_model_radio_button_list):
            if add_model_radio_button.isChecked():
                add_model_name = ADD_MODEL_LIST[i]
                break
        if add_model_name in ["自动", "手动"]:
            if len(self.willing_add_count_list) == 0:
                QMessageBox.information(self, APP_NAME, "没有待添加微信号", QMessageBox.Yes)
                return
        elif add_model_name == "微信群":
            groupName = self.groupNameEdit.text()
            max_count_one_day = self.input_box_one_day.text()
            group_add_inter = self.input_box_add_inter.text()
            if len(groupName) == 0:
                QMessageBox.information(self, APP_NAME, "请输入群名称", QMessageBox.Yes)
                return
            if len(max_count_one_day) == 0 or (int(max_count_one_day) <= 0  or int(max_count_one_day) > 50):
                QMessageBox.information(self, APP_NAME, "请输入每天最多添加的个数", QMessageBox.Yes)
                return
            if len(group_add_inter) == 0 or (int(group_add_inter) <= 0  or int(group_add_inter) > 99):
                QMessageBox.information(self, APP_NAME, "请输入执行对此群成员加好友动作的间隔分数数", QMessageBox.Yes)
                return
            
        # 构造任务数据  
        task_info_list_of_autoadd = []
        i_max_count_everyday = 10
        if strategy_type == "每天10个直到完成":
            i_max_count_everyday = 10
        elif strategy_type == "每天20个直到完成":
            i_max_count_everyday = 20
        elif strategy_type == "每天10个直到完成":
            i_max_count_everyday = 30

        i_day_count = 1
        for i in range(0, int(i_day_count)):
            task_info = {}
            add_friend_data_dict = {}
            
            if add_model_name == "自动":
                add_friend_data_dict["willing_add_count_list"] = self.willing_add_count_list
            elif add_model_name == "手动":
                add_friend_data_dict["file_paths"] = self.file_paths
            elif add_model_name == "微信群":
                self.group_add_rule_info = {"GROUP_NAME": groupName, "MAX_COUNT_ONE_DAY": max_count_one_day, "ADD_INTER": group_add_inter}
                add_friend_data_dict["group_add_rule_info"] = self.group_add_rule_info
                
            days_inter = i
            current_date = datetime.now().date()
            next_date = current_date + timedelta(days=days_inter)
            add_friend_data_dict["date"] = next_date.strftime('%Y-%m-%d')
            add_friend_data_dict["time"] = start_time
            add_friend_data_dict["remark_prefix"] = remark_prefix
            
            if add_model_name in ["自动", "手动"]:
                task_info["task_type"] = "批量加好友"
                task_info["task_distribe"] = "以好友列表文件方式添加好友"
                task_info["task_process"] = "0"
                task_info["task_data"] = add_friend_data_dict
                if add_model_name == "自动":
                    task_info["task_detail_data"] = self.willing_add_count_list
                elif add_model_name == "手动":
                    task_info["task_detail_data"] = get_task_detail_data(task_info)
                task_info["task_finish_detail_data"] = []
                task_info["max_count_everyday"] = str(i_max_count_everyday)
                task_info["task_source"] = "获客机器人_{}".format(str_autoAddName)
                task_info_list_of_autoadd.append(task_info)
            elif add_model_name == "微信群": 
                task_info["task_type"] = "加微信群好友"
                task_info["task_distribe"] = "从微信群的成员列表中添加好友"
                task_info["task_process"] = "0"
                task_info["task_data"] = add_friend_data_dict
                task_info["task_detail_data"] = self.group_add_rule_info
                task_info["task_finish_detail_data"] = []
                task_info["max_count_everyday"] = str(i_max_count_everyday)
                task_info["task_source"] = "获客机器人_{}".format(str_autoAddName)
                task_info_list_of_autoadd.append(task_info)
                
        add_autoadd_data_dict = {}
        if len(self.autoadd_name) != 0:
            add_autoadd_data_dict["autoadd_name_orig"] = self.autoadd_name
        add_autoadd_data_dict["autoadd_name"] = str_autoAddName
        add_autoadd_data_dict["strategy_type"] = strategy_type
        add_autoadd_data_dict["remark_prefix"] = remark_prefix
        add_autoadd_data_dict["start_time"] = start_time
        add_autoadd_data_dict["add_model_name"] = add_model_name
        add_autoadd_data_dict["willing_add_count_list"] = self.willing_add_count_list
        add_autoadd_data_dict["file_paths"] = self.file_paths
        add_autoadd_data_dict["group_add_rule_info"] = self.group_add_rule_info
        add_autoadd_data_dict["task_info_list_of_autoadd"] = task_info_list_of_autoadd
        self._signal.emit("add_autoadd_dict_{}".format(json.dumps(add_autoadd_data_dict)))
        
        self.close()
        return

    def manualSetCountBtnFun(self):
        # 添加默认话术库
        if len(self.file_paths) == 0:
            path_default = ".\\示例_待添加好友微信号列表.txt"
            if True == os.path.exists(path_default):
                self.file_paths = [path_default]
        self.manualSetCount_Win = SetFileDialog('手动设置待添加好友账号', self.file_paths, False)
        self.manualSetCount_Win._signal.connect(self.signal_recv_func)
        self.manualSetCount_Win.setWindowModality(Qt.ApplicationModal)
        self.manualSetCount_Win.show()
        self.manualSetCount_Win.exec_()     
        return

    def generateBtnFun(self):
        # 获取个数 
        text_count = self.accountCountEdit.text()
        text_count = text_count.strip(" ")
        if len(text_count) == 0:
            QMessageBox.information(self, APP_NAME, "请输入要生成的账号的个数", QMessageBox.Yes)
            return 

        # 随机生成手机号码
        willing_add_count_list = []
        for i in range(0, int(text_count)):
            willing_add_count_list.append(generate_phone_number())
        self.willing_add_count_list = willing_add_count_list
        self.reload_account_data_layout()
        return 
        
    def reload_will_add_count_from_files(self):  
        self.willing_add_count_list.clear()
        for file_path in self.file_paths: 
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if len(line) != 0:
                        self.willing_add_count_list.append(line)
        labelText = "待添加微信号文件:无\n待添加微信号:无"
        if len(self.file_paths) > 0:
            labelText = "待添加微信号文件:\n{}\n从账号文件中解析出待添加微信号:\n{}".format("\n".join(self.file_paths), "、".join(self.willing_add_count_list))
        self.labelWillAddCountFile.setText(labelText)   
    def signal_recv_func(self, para): 
        if para.startswith("set_friend_username_"):
            print("AddAutoAddWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
        elif para.startswith("hua_su_file_paths_"):
            print("AddAutoAddWindow事件收到信号:{}".format(para))
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
            self.reload_will_add_count_from_files()  
        return  
                    
# 测试
"""
app = QApplication(sys.argv)
dialog = AddAutoAddWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""