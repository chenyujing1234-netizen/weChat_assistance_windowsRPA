# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QScrollArea
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_add_usergroup import AddUserGroupWindow
from dialog_add_product import AddProductWindow
from dialog_add_content import ContentRow, AddContentWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from custom_calendar import CustomCalendarWidget
from dialog_add_one_content import AddOneContentWindow
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt5.QtGui import QPixmap
import json
import ast
import copy
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
from app_info import APP_NAME, g_desktop_w, g_desktop_h, AGENT_CONFIG_DICT
from hover_label import HoverLabel
from excel_helper import *

TOUCH_TYPE = ["朋友圈", "单聊"]
#TOUCH_TYPE = ["朋友圈"]
class AddAgentWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, title, agent_name, agent_type, agent_product_name, agent_touch_type, agent_touch_usergroupname, agent_sop, task_info_list_of_agent, product_info_list, usergroup_info_list, friend_info_list, content_info_list, agent_info_list, parent):
        super().__init__()
        self.title = title
        self.agent_name_orig = agent_name
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.agent_product_name = agent_product_name
        self.agent_touch_type = agent_touch_type
        self.agent_touch_usergroupname = agent_touch_usergroupname
        self.agent_sop = agent_sop
        self.task_info_list_of_agent = task_info_list_of_agent
        self.product_info_list = product_info_list
        self.usergroup_info_list = usergroup_info_list
        self.friend_info_list = friend_info_list
        self.content_info_list = content_info_list
        print("8888888888888888888  content_info_list:{}".format(content_info_list))
        self.agent_info_list = agent_info_list
        self.mainWindow = parent
        self.initUI()

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        self.resize(int(g_desktop_w*6/7), int(g_desktop_h*9/10))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 智能体的名称
        self.layout1 = QHBoxLayout()
        self.labelAgentName = HoverLabel("智能体的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的智能体取个名称", self)
        self.agentNameEdit = QTextEdit()
        self.agentNameEdit.setPlaceholderText("在这里输入要添加的智能体的名称")
        font_metrics = self.agentNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.agentNameEdit.setFixedHeight(line_height + 10) 
        self.agentNameEdit.setLineWrapMode(QTextEdit.NoWrap)
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
                agent_name = "营销智能体" + str(i)
                if agent_name not in [agent_info["agent_name"] for agent_info in self.agent_info_list]:
                    break
            self.agentNameEdit.setText(agent_name)
        self.layout1.addWidget(self.labelAgentName)
        self.layout1.addWidget(self.agentNameEdit)
        # 智能体的类型
        self.layout2 = QHBoxLayout()
        self.labelAgentType = HoverLabel("智能体的类型:<font color='red'>*</font> <font color='blue'>?</font>", "我们提供了一些智能体的类型，并对这些智能体进行了符合人心理习惯的定制。\n不同的智能体类型，我们将定制不同的SOP时间规律，达到更好的营销效果。", self)
        self.agent_combo_box = QComboBox(self)
        for agent_name in AGENT_CONFIG_DICT:
            self.agent_combo_box.addItem(agent_name)
        self.agent_combo_box.setCurrentIndex(0)
        if len(self.agent_type) > 0:
            for i, agent_name in enumerate(AGENT_CONFIG_DICT):
                if self.agent_type == agent_name:
                    self.agent_combo_box.setCurrentIndex(i)
                    break
        self.layout2.addWidget(self.labelAgentType)
        self.layout2.addWidget(self.agent_combo_box)
        # 智能体关联的产品 
        self.layout3 = QHBoxLayout()
        self.labelProductWebsite = HoverLabel("关联的产品:<font color='red'>*</font> <font color='blue'>?</font>", "当你重新生成内容时，我们将根据你关联的产品的信息来生成内容", self)
        self.agent_product_combo_box = QComboBox(self)
        self.reload_product_combo_box()
        self.agent_product_combo_box.currentIndexChanged.connect(self.on_item_changed_of_agent_product_combo_box)
        self.layout3.addWidget(self.labelProductWebsite)
        self.layout3.addWidget(self.agent_product_combo_box)
        # 触达方式
        self.layout4 = QHBoxLayout()
        self.labelAgentTouchType = HoverLabel("触达方式:<font color='red'>*</font> <font color='blue'>?</font>", "这个智能体创建的营销SOP(内容序列)通过什么方式发给客户", self)
        self.agent_touch_type_radio_button_list = []
        for i, touch_type_name in enumerate(TOUCH_TYPE):
            agent_touch_type_radio_button = QRadioButton(touch_type_name, self)
            self.agent_touch_type_radio_button_list.append(agent_touch_type_radio_button)
        self.agent_touch_type_radio_button_list[0].setChecked(True) 
        if len(self.agent_touch_type) > 0:
            for i, touch_type_name in enumerate(TOUCH_TYPE):
                if self.agent_touch_type == touch_type_name:
                    self.agent_touch_type_radio_button_list[i].setChecked(True) 
                    break
                    
        self.layout4.addWidget(self.labelAgentTouchType)
        for agent_touch_type_radio_button in self.agent_touch_type_radio_button_list:
            self.layout4.addWidget(agent_touch_type_radio_button)
        # 智能体触达的客户组 
        self.layout5 = QHBoxLayout()
        self.labelAgentTouchObject = HoverLabel("智能体触达客户组:<font color='red'>*</font> <font color='blue'>?</font>", "这个智能体创建的营销SOP(内容序列)将发给哪些好友。\n如果触达方式是\"朋友圈\"时，这里指朋友圈的可见好友；\n如果触达方式是\"单聊\"时，这里指给哪些好友发单聊消息")
        self.agent_touch_object_combo_box = QComboBox(self)
        self.reload_usergroup_combo_box()
        self.agent_touch_object_combo_box.currentIndexChanged.connect(self.on_item_changed_of_agent_touch_object_combo_box)
        self.layout5.addWidget(self.labelAgentTouchObject)
        self.layout5.addWidget(self.agent_touch_object_combo_box)
        # 智能体的SOP 
        self.layout6 = QHBoxLayout()
        self.labelAgentSOP = HoverLabel("智能体的SOP(内容):<font color='red'>*</font> <font color='blue'>?</font>", "这个智能体的将使用哪个内容（在内容页中展示的内容），绑定了内容后，\n在智能体里可以给每个内容设置执行的日期时间，这样就得到了SOP(内容序列)", self)
        self.agent_sop_combo_box = QComboBox(self)
        self.previous_index_of_agent_sop_combo_box = 0
        self.reload_sop_combo_box()
        self.agent_sop_combo_box.currentIndexChanged.connect(self.on_item_changed_of_agent_sop_combo_box)
        self.layout6.addWidget(self.labelAgentSOP)
        self.layout6.addWidget(self.agent_sop_combo_box)
        
        # 按钮
        self.layout7 = QHBoxLayout()
        # 生成按钮
        '''
        self.button_generate = QPushButton("开始自动生成", self)
        self.button_generate.setStyleSheet("""
            QPushButton {
                color: blue;          /* 设置字体颜色为蓝色 */
                font-weight: bold;    /* 设置字体为粗体 */
                font-size: 14px;      /* 可选：设置字体大小 */
            }
        """)
        #self.button_generate.setFixedWidth(self.width() // 6)
        self.button_generate.clicked.connect(self.generateBtnFun)
        '''
        # 手动添加文案
        self.button_human_add = QPushButton("手动添加文案", self)
        self.button_human_add.clicked.connect(self.humanAddBtnFun)
        #    导出文案
        self.button_export = QPushButton("导出文案", self)
        self.button_export.clicked.connect(self.exportContentBtnFun)

        #self.layout7.addWidget(self.button_generate)
        self.layout7.addWidget(self.button_human_add)
        self.layout7.addWidget(self.button_export)
        self.layout7.addStretch()
        
        # 内容数据列表
        self.layout8 = QHBoxLayout()
        self.scroll_area_content = QScrollArea()
        self.scroll_area_content.setWidgetResizable(True)

        self.container_content = QWidget()
        self.container_layout_content = QVBoxLayout()
        self.container_layout_content.setAlignment(Qt.AlignTop)
        self.container_content.setLayout(self.container_layout_content)

        self.scroll_area_content.setWidget(self.container_content)
        self.layout8.addWidget(self.scroll_area_content, 3)
        self.calendar = CustomCalendarWidget(self)
        self.calendar._signal.connect(self.signal_recv_func)
        self.layout8.addWidget(self.calendar, 1)
        self.reload_content_data_layout(False)
        ##########################################
       
        # 确定按钮
        self.confirmBtn = QPushButton("确定")
        self.confirmBtn.clicked.connect(self.confirmBtnFun)
        
        # 创建垂直布局并添加QTabWidget
        layout = QVBoxLayout()
        layout.addLayout(self.layout1)
        layout.addLayout(self.layout2)
        layout.addLayout(self.layout3)
        layout.addLayout(self.layout4)
        layout.addLayout(self.layout5)
        layout.addLayout(self.layout6)
        layout.addLayout(self.layout7)
        #layout.addWidget(self.scroll_area_content)
        layout.addLayout(self.layout8)
        layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(layout)

        # 设置对话框大小
        #self.resize(400, 400)

    def add_content_row(self, date, time, content, image_list):
        row = ContentRow(date, time, content, image_list, True, self)
        row._signal.connect(self.signal_recv_func)
        self.container_layout_content.addWidget(row)

    def get_content_data_info_list(self):
        content_info_data_list = []
        # 遍历布局中的所有项
        while self.container_layout_content.count():
            item = self.container_layout_content.takeAt(0)
            widget = item.widget()
            if widget:
                content_info_data = widget.get_content_data()
                content_info_data_list.append(content_info_data)
        return content_info_data_list
                
    def clear_container_layout_content(self):
        # 遍历布局中的所有项
        while self.container_layout_content.count():
            item = self.container_layout_content.takeAt(0)
            widget = item.widget()
            if widget:
                # 移除并销毁控件
                widget.setParent(None)
                widget.deleteLater()

    # 删除一条内容            
    def del_one_content_data(self, content, image_list):
        task_info_list_of_agent_new = []
        for task_info in self.task_info_list_of_agent:
            task_data = task_info["task_data"]
            if task_data["wenAn"] == content and task_data["img_paths"] == image_list:
                continue
            task_info_list_of_agent_new.append(task_info)
        self.task_info_list_of_agent = task_info_list_of_agent_new

    def sort_tasks_by_date_and_time(self, task_info_list_of_agent):
        """
        按照日期和时间对任务信息列表进行排序的函数。
        :param task_info_list_of_agent: 包含任务信息的列表，每个元素是一个字典，包含键'date'和'time'
        :return: 排序后的任务信息列表
        """
        # 使用sorted函数和lambda表达式进行排序
        # 先按'date'排序，再按'time'排序
        sorted_list = sorted(task_info_list_of_agent, key=lambda x: (x["task_data"]['date'], x["task_data"]['time']))
        return sorted_list
 
    def reload_content_data_layout(self, b_use_sop_data):
        self.clear_container_layout_content()
        
        if b_use_sop_data == True or len(self.task_info_list_of_agent) == 0:
             # 获取智能体的SOP            
            content_name = self.agent_sop_combo_box.currentText()
            content_name = content_name.strip(" ")
            content_info_select = {}
            content_data_list = []
            for content_info in self.content_info_list:
                if content_info["content_name"] == content_name:
                    content_info_select = content_info
                    break
            if "content_data_list" in content_info_select:
                content_data_list = content_info_select["content_data_list"]
                # 补充空的图片
                for content_data in content_data_list:
                    if "image_list" not in content_data:
                        content_data["image_list"] = []
                # 把日期、时间去掉
                for content_data in content_data_list:
                    if "date" in content_data:
                        content_data["date"] = ""
                    if "time" in content_data:
                        content_data["time"] = ""
                        
            self.task_info_list_of_agent.clear()
            self.task_info_list_of_agent = self.create_task_list_from_content_data(content_data_list)
            """
            for i, content_data in enumerate(content_data_list):
                str_wenAn = content_data["content"]
                image_list = content_data["image_list"]
                
                if "date" in content_data:
                    date = content_data["date"]
                    time = content_data["time"]
                else:
                    days_inter = i
                    current_date = datetime.now().date()
                    next_date = current_date + timedelta(days=days_inter)
                    date = next_date.strftime('%Y-%m-%d')
                    time = "10:17:00"
                
                self.add_content_row(date, time, str_wenAn, image_list)
            """
        # 对任务的数据按日期时间排序
        self.task_info_list_of_agent = self.sort_tasks_by_date_and_time(self.task_info_list_of_agent)
        
        for i, task_info in enumerate(self.task_info_list_of_agent):
            task_data = task_info["task_data"]
            str_wenAn = task_data["wenAn"]
            image_list = task_data["img_paths"]
            date = task_data["date"]
            time = task_data["time"]
            self.add_content_row(date, time, str_wenAn, image_list)
            
        # 更新日历
        #   设置日历月份
        current_date = datetime.now().date()
        date_str_of_show = current_date.strftime('%Y-%m-%d')
        if len(self.task_info_list_of_agent) > 0:
            date_str_of_show = self.task_info_list_of_agent[0]["task_data"]["date"]
        target_date = QDate.fromString(date_str_of_show, "yyyy-MM-dd")
        self.calendar.setSelectedDate(target_date) 
        self.calendar.showSelectedDate() 
        #   设置日历打勾
        self.calendar.clear_checked_dates()
        for task_info in self.task_info_list_of_agent:
            task_data = task_info["task_data"]
            date = task_data["date"]
            self.calendar.set_checked_date(date)

    def create_task_list_from_content_data(self, content_info_data_list):
        task_info_list_of_agent = []

        for i, content_info_data in enumerate(content_info_data_list):
            content_text = content_info_data["content"]
            image_list = content_info_data["image_list"]
            str_date = ""
            str_time = ""
            if "date" in content_info_data and len(content_info_data["date"]) > 0:
                str_date = content_info_data["date"]
                str_time = content_info_data["time"]
                print("已经有日期了。。。。{}".format(str_date))
            else:
                days_inter = i
                print("没有日期，现在是第 {}天".format(i))
                current_date = datetime.now().date()
                next_date = current_date + timedelta(days=days_inter)
                str_date = next_date.strftime('%Y-%m-%d')
                agent_type = self.agent_combo_box.currentText()
                str_time = AGENT_CONFIG_DICT[agent_type]["time"]

        
            task_info = {}
            task_data = {}
            
            task_info["task_process"] = "0"
            task_info["task_detail_data"] = []
            task_info["task_finish_detail_data"] = []
            task_info["task_source"] = "智能体_{}".format(self.agent_name)
            
            if self.agent_touch_type == "朋友圈":  
                task_info["task_type"] = "定时发朋友圈"  
                task_info["task_distribe"] = "定时发朋友朋友圈\nsdlfja fasfasffaskfjaskfjalksdjfsadf"
            elif self.agent_touch_type == "单聊": 
                task_info["task_type"] = "定时发单聊消息"
                task_info["task_distribe"] = "定时发单聊消息\nsdlfja fasfasffaskfjaskfjalksdjfsadf"
            
            # 
            task_data["wenAn"] = content_text
            task_data["img_paths"] = image_list
            task_data["username_of_can_see_list"] = []
            task_data["username_of_finish_list"] = []
            
            #
            """
            days_inter = i
            current_date = datetime.now().date()
            next_date = current_date + timedelta(days=days_inter)
            task_data["date"] = next_date.strftime('%Y-%m-%d')
            task_data["time"] = "8:17:00"
            """
            task_data["date"] = str_date
            task_data["time"] = str_time
            
            # 改为在执行时再去获得成员
            username_of_can_see_list = []
            """ 
            usergroup_info_select = {}
            for usergroup_info in self.usergroup_info_list:
                if usergroup_info["usergroup_name"] == agent_touch_object:
                    usergroup_info_select = usergroup_info
                    break
            if "usergroup_member" in usergroup_info_select:
                for member in usergroup_info_select["usergroup_member"]:
                    username_of_can_see_list.append(member)
            """
            task_data["usergroup_name_of_can_see"] = self.agent_touch_usergroupname
            task_data["username_of_can_see_list"] = username_of_can_see_list
            

            task_info["task_data"] = task_data

            task_info_list_of_agent.append(task_info)
        return task_info_list_of_agent
    
    # 开始生成按钮的响应函数
    def generateBtnFun(self):
        # 获取内容关联的产品 
        content_product_name = self.content_product_combo_box.currentText()
        content_product_name = content_product_name.strip(" ")
        if len(content_product_name) == 0:
            QMessageBox.information(self, APP_NAME, "请选择内容关联的产品", QMessageBox.Yes)
            return 
        product_info_select = {}
        for product_info in self.product_info_list:
            if product_info["product_name"] == content_product_name:
                product_info_select = product_info
                break 
            
        # 获取内容的场景
        agent_type = self.agent_combo_box.currentText()  
        
        # 获取条数 
        text_count = self.contentCountEdit.text()
        text_count = text_count.strip(" ")
        if len(text_count) == 0:
            QMessageBox.information(self, APP_NAME, "请输入要添加的内容的条数", QMessageBox.Yes)
            return 
        if int(text_count) <= 0:
            QMessageBox.information(self, APP_NAME, "请输入正确的条数", QMessageBox.Yes)
            return 
        # 获取大模型的类型
        llm_name_sel = self.llm_combo_box.currentText()
        llm_type_enum = LLM_MODEL_TYPE.Unknow
        for llm_name in LLM_MODEL_NAME_TYPE_DICT:
            if llm_name == llm_name_sel:
                llm_type_enum = LLM_MODEL_NAME_TYPE_DICT[llm_name]
                break 
                
        self.waiting_Win = WaitingWindow(self)
        self.waiting_Win.setWindowModality(Qt.ApplicationModal)
        self.waiting_Win.show() 
        
        product_summary = product_info_select["product_summary"]
        content_examples = ""
        thread = Thread(target=self.generate_content_thread, args=(agent_type, content_product_name, product_summary, content_examples, text_count, llm_type_enum))
        thread.start()
        
        return
    
    # 手动添加文案按钮的响应函数
    def humanAddBtnFun(self, date_str="", time_str=""):
        print("date_str:{}".format(date_str))
        if isinstance(date_str, str) == False:
            date_str = ""
        if isinstance(time_str, str) == False:
            time_str = ""
        self.addOneContent_Win = AddOneContentWindow("添加文案", "", date_str, time_str, [], True, self)
        self.addOneContent_Win._signal.connect(self.signal_recv_func)
        self.addOneContent_Win.setWindowModality(Qt.ApplicationModal)
        self.addOneContent_Win.show()
        self.addOneContent_Win.exec_()
        return      

    # 导出内容按钮的响应函数
    def exportContentBtnFun(self):
        excel_file_path = ""
        # 获取内容
        content_data_list = copy.deepcopy(self.get_content_data_info_list())
        if len(content_data_list) <= 0:
            QMessageBox.information(self, APP_NAME, "没有要导出的内容", QMessageBox.Yes)
            return
        
        # 弹出框选择保存的目录及文件名
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 弹出“另存为”对话框
        excel_file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择保存路径和文件名"
        )
        
        # 如果用户选择了路径，则保存文件
        if excel_file_path:
            if True == save_content_to_excel(content_data_list, excel_file_path):
                self.mainWindow.signal_of_table.emit("tooltip_{}".format("导出内容成功"))
                print_my("导出内容成功")
                return
            else:
                QMessageBox.information(self, APP_NAME, "内容导出失败", QMessageBox.Yes)
                print_my("！！！导出内容失败")
                return 
        else:
            print("用户取消了保存操作")

        return
        
    def confirmBtnFun(self):
        # 获取智能体的名称
        self.agent_name = self.agentNameEdit.toPlainText()
        if len(self.agent_name) == 0:
            QMessageBox.information(self, APP_NAME, "请输入智能体的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for agent_info in self.agent_info_list:
            if agent_info["agent_name"] == self.agent_name:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加营销智能体":
            QMessageBox.information(self, APP_NAME, "产品的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取智能体的类型 
        agent_type = self.agent_combo_box.currentText()
        if len(agent_type) == 0:
            QMessageBox.information(self, APP_NAME, "请选择智能体的类型", QMessageBox.Yes)
            return
        # 获取智能体关联的产品 
        agent_product_name = self.agent_product_combo_box.currentText()
        agent_product_name = agent_product_name.strip(" ")
        if len(agent_product_name) == 0:
            QMessageBox.information(self, APP_NAME, "请选择智能体关联的产品", QMessageBox.Yes)
            return
        # 获取智能体触达方式
        self.agent_touch_type = ""
        for agent_touch_type_radio_button in self.agent_touch_type_radio_button_list:
            if agent_touch_type_radio_button.isChecked():
                self.agent_touch_type = agent_touch_type_radio_button.text()
                break
        if len(self.agent_touch_type) == 0:
            QMessageBox.information(self, APP_NAME, "请选择智能体触达方式", QMessageBox.Yes)
            return
        # 获取智能体触达的客户组 
        agent_touch_usergroupname = self.agent_touch_object_combo_box.currentText()
        self.agent_touch_usergroupname = agent_touch_usergroupname.strip(" ")
        if len(self.agent_touch_usergroupname) == 0:
            QMessageBox.information(self, APP_NAME, "请选择智能体触达的客户组", QMessageBox.Yes)
            return
        # 获取智能体的SOP  
        agent_sop = self.agent_sop_combo_box.currentText()
        agent_sop = agent_sop.strip(" ")
        if len(agent_sop) == 0:
            QMessageBox.information(self, APP_NAME, "请选择智能体的SOP ", QMessageBox.Yes)
            return
        # 获取内容数据创建task 
        content_info_data_list = self.get_content_data_info_list()
        self.task_info_list_of_agent.clear()  
        self.task_info_list_of_agent = self.create_task_list_from_content_data(content_info_data_list)
            
        add_agent_data_dict = {}
        if len(self.agent_name) != 0:
            add_agent_data_dict["agent_name_orig"] = self.agent_name_orig
        add_agent_data_dict["agent_name"] = self.agent_name
        add_agent_data_dict["agent_type"] = agent_type
        add_agent_data_dict["agent_product_name"] = agent_product_name
        add_agent_data_dict["agent_touch_type"] = self.agent_touch_type
        add_agent_data_dict["agent_touch_object"] = self.agent_touch_usergroupname
        add_agent_data_dict["agent_sop"] = agent_sop
        add_agent_data_dict["task_info_list_of_agent"] = self.task_info_list_of_agent
        self._signal.emit("add_agent_dict_{}".format(json.dumps(add_agent_data_dict)))
        
        self.close()
        return

    def on_item_changed_of_agent_touch_object_combo_box(self, index):
        sel_text = self.agent_touch_object_combo_box.currentText()
        print("智能体触达的客户组的索引发生变化，当前选中：{}".format(sel_text))
        if sel_text == "添加...":
            self.agent_touch_object_combo_box.setCurrentIndex(self.previous_index_of_agent_touch_object_combo_box)
            self.addUserGroup_Win = AddUserGroupWindow("添加客户组", "", "", [], self.friend_info_list, [], self.usergroup_info_list, self)
            self.addUserGroup_Win._signal.connect(self.signal_recv_func)
            self.addUserGroup_Win.setWindowModality(Qt.ApplicationModal)
            self.addUserGroup_Win.show()
            self.addUserGroup_Win.exec_()
        else:
            self.previous_index_of_agent_touch_object_combo_box = index
        return
 
    def on_item_changed_of_agent_sop_combo_box(self, index):
        sel_text = self.agent_sop_combo_box.currentText()
        print("智能体触达的SOP的索引发生变化，当前选中：{}".format(sel_text))
        sel_text = sel_text.strip(" ")
        if len(sel_text) == 0:
            return 
            
        if sel_text == "添加...":
            self.agent_sop_combo_box.setCurrentIndex(self.previous_index_of_agent_sop_combo_box)
            self.addContent_Win = AddContentWindow('添加文案', "", "", "", "", "", "", '5', [], self.product_info_list, self.content_info_list, self)
            self.addContent_Win._signal.connect(self.signal_recv_func)
            self.addContent_Win.setWindowModality(Qt.ApplicationModal)
            self.addContent_Win.show()
            self.addContent_Win.exec_()
        else:
            if index != self.previous_index_of_agent_sop_combo_box:
                result = QMessageBox.question(self, APP_NAME, "切换文案将清空列表中的文案，确定要切换?", QMessageBox.Yes | QMessageBox.No)
                if(result == QMessageBox.No):
                    self.agent_sop_combo_box.setCurrentIndex(self.previous_index_of_agent_sop_combo_box)
                    return 

            self.previous_index_of_agent_sop_combo_box = index
            self.reload_content_data_layout(True)
        return
        
    def on_item_changed_of_agent_product_combo_box(self, index):
        sel_text = self.agent_product_combo_box.currentText()
        print("智能体关联产品的索引发生变化，当前选中：{}".format(sel_text))
        if sel_text == "添加...":
            self.agent_product_combo_box.setCurrentIndex(self.previous_index_of_agent_product_combo_box)
            self.addProduct_Win = AddProductWindow('添加产品', "", "", "", [], self.product_info_list, self)
            self.addProduct_Win._signal.connect(self.signal_recv_func)
            self.addProduct_Win.setWindowModality(Qt.ApplicationModal)
            self.addProduct_Win.show()
            self.addProduct_Win.exec_()
        else:
            self.previous_index_of_agent_product_combo_box = index
        return
    
    def signal_recv_func(self, para): 
        if para == "reload_content_data_layout":
            print("AddAgentWindow事件收到信号:{}".format(para))
            self.reload_content_data_layout(False)
        elif para == "get_data_and_reload_content_data_layout":
            print("AddAgentWindow事件收到信号:{}".format(para))
            self.content_data_list = self.get_content_data_info_list()
            self.reload_content_data_layout(False)
        elif para.startswith("set_friend_username_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
        elif para.startswith("hua_su_file_paths_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
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
        elif para.startswith("add_product_dict_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            add_product_data_dict_str = para.strip("add_product_dict_")
            try:
                add_product_data_dict = json.loads(add_product_data_dict_str)
                print(add_product_data_dict)
                # 因为这个类里使用的self.product_info_list是外面传进来的，当下面emit给Table发信号时，会把新数据添加到变量里，
                # 这个动作后，这里的变量也会变化的，所以这里不需要再append一次
                #self.product_info_list.append(add_product_data_dict)
                self._signal.emit(para)        
                self.agent_product_name = add_product_data_dict["product_name"]               
                self.reload_product_combo_box() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")    
        elif para.startswith("add_usergroup_dict_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            add_usergroup_data_dict_str = para.strip("add_usergroup_dict_")
            try:
                add_usergroup_data_dict = json.loads(add_usergroup_data_dict_str)
                print(add_usergroup_data_dict)
                # 因为这个类里使用的self.usergroup_info_list是外面传进来的，当下面emit给Table发信号时，会把新数据添加到变量里，
                # 这个动作后，这里的变量也会变化的，所以这里不需要再append一次
                #self.usergroup_info_list.append(add_usergroup_data_dict)
                self._signal.emit(para)        
                self.agent_touch_usergroupname = add_usergroup_data_dict["usergroup_name"]               
                self.reload_usergroup_combo_box() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
        elif para.startswith("add_content_dict_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            add_content_data_dict_str = para.strip("add_content_dict_")
            try:
                add_content_data_dict = json.loads(add_content_data_dict_str)
                print(add_content_data_dict)
                # 因为这个类里使用的self.content_info_list是外面传进来的，当下面emit给Table发信号时，会把新数据添加到变量里，
                # 这个动作后，这里的变量也会变化的，所以这里不需要再append一次
                #self.content_info_list.append(add_content_data_dict)
                self._signal.emit(para)                 
                self.agent_sop = add_content_data_dict["content_name"]               
                self.reload_sop_combo_box() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}") 
        elif para.startswith("add_one_content_dict_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            add_one_content_dict_str = para.strip("add_one_content_dict_")
            try:
                add_one_content_dict = json.loads(add_one_content_dict_str)
                print(add_one_content_dict)   

                content_data = {}
                content_data["content"] = add_one_content_dict["wenAn"]
                content_data["image_list"] = add_one_content_dict["img_paths"]
                content_data["date"] = ""
                if "date" in add_one_content_dict:
                    content_data["date"] = add_one_content_dict["date"]
                content_data["time"] = ""
                if "time" in  add_one_content_dict: 
                    content_data["time"] = add_one_content_dict["time"]
                task_info_list = self.create_task_list_from_content_data([content_data])
                self.task_info_list_of_agent.append(task_info_list[0])
                self.reload_content_data_layout(False)

            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
        elif para.startswith("copy_one_content_dict_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            copy_one_content_dict_str = para.strip("copy_one_content_dict_")
            try:
                copy_one_content_dict = json.loads(copy_one_content_dict_str)
                print(copy_one_content_dict)           
                self.addOneContent_Win = AddOneContentWindow("添加文案", copy_one_content_dict["content"], copy_one_content_dict["date"], copy_one_content_dict["time"], copy_one_content_dict["image_list"], True, self)
                self.addOneContent_Win._signal.connect(self.signal_recv_func)
                self.addOneContent_Win.setWindowModality(Qt.ApplicationModal)
                self.addOneContent_Win.show()
                self.addOneContent_Win.exec_()
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")  
        elif para.startswith("double_clicked_"):
            print("AddAgentWindow事件收到信号:{}".format(para))
            double_clicked_str = para.strip("double_clicked_")
            try:
                print("double_clicked_str:{}".format(double_clicked_str))
                self.humanAddBtnFun(double_clicked_str)

            except Exception as e:
                print(f"double_clicked_异常：{e}")   
        return

    def reload_product_combo_box(self): 
        self.agent_product_combo_box.clear()
        for product_info in self.product_info_list:
            self.agent_product_combo_box.addItem(product_info["product_name"])
        if len(self.product_info_list) > 0:
            self.agent_product_combo_box.setCurrentIndex(0)
            self.previous_index_of_agent_product_combo_box = 0
        # 没数据时做特殊处理
        if len(self.product_info_list) == 0:
            self.agent_product_combo_box.addItem("  ")
            self.agent_product_combo_box.setCurrentIndex(0)
            self.previous_index_of_agent_product_combo_box = 0  
        self.agent_product_combo_box.addItem("添加...")
        if len(self.agent_product_name) > 0:
            for i, product_info in enumerate(self.product_info_list):
                if self.agent_product_name == product_info["product_name"]:
                    self.agent_product_combo_box.setCurrentIndex(i)
                    self.previous_index_of_agent_product_combo_box = i
                    break
                        
    def reload_usergroup_combo_box(self):
        self.agent_touch_object_combo_box.clear()
        for usergroup_info in self.usergroup_info_list:
            self.agent_touch_object_combo_box.addItem(usergroup_info["usergroup_name"])
        if len(self.usergroup_info_list) > 0:
            self.agent_touch_object_combo_box.setCurrentIndex(0)
            self.previous_index_of_agent_touch_object_combo_box = 0
        # 没数据时做特殊处理
        if len(self.usergroup_info_list) == 0:
            self.agent_touch_object_combo_box.addItem("  ")
            self.agent_touch_object_combo_box.setCurrentIndex(0)
            self.previous_index_of_agent_touch_object_combo_box = 0  
        self.agent_touch_object_combo_box.addItem("添加...")
        if len(self.agent_touch_usergroupname) > 0:
            for i, usergroup_info in enumerate(self.usergroup_info_list):
                if self.agent_touch_usergroupname == usergroup_info["usergroup_name"]:
                    self.agent_touch_object_combo_box.setCurrentIndex(i)
                    self.previous_index_of_agent_touch_object_combo_box = i
                    break
                    
    def reload_sop_combo_box(self):
        self.agent_sop_combo_box.clear()
        for content_info in self.content_info_list:
            self.agent_sop_combo_box.addItem(content_info["content_name"])
            print("reload_sop_combo_box, content_name:{}".format(content_info["content_name"]))

        # 没数据时做特殊处理
        if len(self.content_info_list) == 0:
            self.agent_sop_combo_box.addItem("  ")
        self.agent_sop_combo_box.addItem("添加...")
        if len(self.agent_sop) > 0:
            for i, content_info in enumerate(self.content_info_list):
                if self.agent_sop == content_info["content_name"]:
                    self.agent_sop_combo_box.setCurrentIndex(i)
                    self.previous_index_of_agent_sop_combo_box = i
                    return
        elif len(self.content_info_list) == 0: 
            self.agent_sop_combo_box.setCurrentIndex(0)
            self.previous_index_of_agent_sop_combo_box = 0
            return 
        elif len(self.content_info_list) > 0:
            self.agent_sop_combo_box.setCurrentIndex(0)
            self.previous_index_of_agent_sop_combo_box = 0
            return 
        return 
# 测试
"""
app = QApplication(sys.argv)
dialog = AddUserGroupWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""