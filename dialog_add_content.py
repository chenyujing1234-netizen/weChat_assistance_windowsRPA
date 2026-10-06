# -*- coding: utf-8 -*-
import sys
import os
from threading import Thread
from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QTextEdit, QDateEdit, QTimeEdit, QMessageBox, QComboBox, QRadioButton, QScrollArea, QFrame, QLineEdit
from dialog_set_friend_object import SetFriendObjectWindow
from dialog_add_product import AddProductWindow
from dialog_set_file import ReadOnlyDelegate, SetFileDialog
from dialog_waiting import WaitingWindow
from dialog_add_one_content import AddOneContentWindow
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QTime, QEvent, QPoint
from PyQt5.QtGui import QPixmap, QFont, QColor, QTextCursor, QIntValidator

import json
import ast
import tkinter as tk
from tkinter import filedialog
import app_info
from app_info import APP_NAME, LLM_MODEL_TYPE, LLM_MODEL_NAME_TYPE_DICT, LLM_MODEL_TYPE_NAME_DICT, g_desktop_w, g_desktop_h, AGENT_CONFIG_DICT
from llm_helper import llm_generate_content, llm_get_result_image, llm_generate_pos_neg_text_by_wenAn, extract_json_to_dict
from error_code import *
from hover_label import HoverLabel
from log_helper import print_my
from excel_helper import *

class ImageZoomWindow(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.init_ui()
        self.setWindowModality(Qt.WindowModal)  # 设置为模态窗口
        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)  # 添加关闭按钮，总是在最上面
        self.setWindowOpacity(0.95)  # 设置窗口透明度，可选

        # 初始化拖动功能
        self.dragging = False
        self.offset = QPoint()

    def init_ui(self):
        self.setWindowTitle("图片放大")
        self.setGeometry(100, 100, 800, 600)  # 设置窗口大小

        # 创建一个 QLabel 用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 加载图片并设置到 QLabel
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)

        # 创建关闭按钮
        self.close_button = QPushButton("×", self)
        self.close_button.clicked.connect(self.close)
        self.close_button.move(self.width() - self.close_button.width() - 10, 10)  # 放置在右上角
        # 设置关闭按钮的样式表
        self.close_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
             
class ContentRow(QWidget):
    _signal = pyqtSignal(str)
    def __init__(self, str_date, str_time, content, image_list, b_has_title_layout, parent):
        super().__init__()

        self.str_date = str_date
        self.str_time = str_time
        self.content = content
        self.image_list = image_list
        self.b_has_title_layout = b_has_title_layout
        self.parent = parent
        
        # 设置标题
        self.title_layout = QHBoxLayout()
        self.dateEdit = QDateEdit(QDate.currentDate())
        self.dateEdit.setDateRange(QDate(2020, 1, 1), QDate(2030, 12, 31))
        self.timeEdit = QTimeEdit(QTime.currentTime())
        self.title_layout.addWidget(self.dateEdit)
        self.title_layout.addWidget(self.timeEdit)
        self.title_layout.addStretch()
        #self.title_label = QLabel(title)
        #self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        #self.title_label.setStyleSheet("color: green;")

        # 创建方框
        self.box_frame = QFrame()
        self.box_frame.setFrameShape(QFrame.StyledPanel)  # 设置方框样式
        self.box_frame.setFrameShadow(QFrame.Raised)      # 设置阴影效果
        #self.box_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 10px;")
        self.box_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 2px;")

        # 正文
        self.content_text = QTextEdit(content)
        self.content_text.setReadOnly(True)
        self.content_text.setFrameShape(QFrame.NoFrame)
        #self.content_text.setStyleSheet("background-color: transparent; border: none;")
        self.content_text.setStyleSheet("background-color: transparent; border: none; padding: 0;")
        
        # 设置按钮
        self.copy_button = QPushButton(" 复制 ")
        self.del_button = QPushButton(" 删除 ")
        self.edit_button = QPushButton(" 编辑 ")
        self.generate_img_button = QPushButton(" 自动生成图片 ")
        self.copy_button.clicked.connect(self.copy_text)
        self.del_button.clicked.connect(self.del_text)
        self.edit_button.clicked.connect(self.edit_text)
        self.generate_img_button.clicked.connect(self.generate_img)
        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.copy_button)
        self.button_layout.addWidget(self.del_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.generate_img_button)
        self.button_layout.addStretch()
        

        # 方框内的布局
        self.box_layout = QVBoxLayout()
        self.box_layout.setSpacing(1)  # 设置控件之间的间隔为5像素（可根据需要调整）
        self.box_layout_subtilte = QHBoxLayout()
        self.box_layout_subtilte.addLayout(self.button_layout)
        self.box_layout.addLayout(self.box_layout_subtilte)
        self.box_layout.addWidget(self.content_text)
        
        # 图片列表控件
        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.image_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.image_scroll_area.setVisible(False)  # 默认不显示

        self.image_container = QWidget()
        self.image_layout = QHBoxLayout()
        self.image_layout.setSpacing(1)
        self.image_layout.addStretch()
        self.image_container.setLayout(self.image_layout)
        self.image_scroll_area.setWidget(self.image_container)
        self.image_scroll_area.setStyleSheet("padding: 0;")

        self.box_layout.addWidget(self.image_scroll_area)
        self.box_frame.setLayout(self.box_layout)

        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(1)
        # chenyj test
        # 主标标题太占位置了，先把它去掉
        if b_has_title_layout == True:
            #self.main_layout.addWidget(self.title_label)
            self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.box_frame)
        #self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        # 刷新页面
        self.reload_ui()
        
    def add_images(self):
        """添加图片到图片列表"""
        for image_path in self.image_list:
            # 创建图片标签
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            # 设置点击事件
            image_label.mousePressEvent = lambda event, img_path=image_path: self.show_zoomed_image(img_path)

            # 创建关闭按钮
            close_button = QPushButton("×")
            close_button.setStyleSheet("background-color: red; color: white; border: none;")
            close_button.clicked.connect(lambda checked, img_path=image_path: self.delete_image(img_path))
            close_button.setFixedSize(20, 20)

            # 创建布局，将图片和关闭按钮组合在一起
            image_layout_ = QVBoxLayout()
            image_layout_.addWidget(image_label)
            image_layout_.addStretch()  # 添加弹性空间，确保关闭按钮在右上角
            image_layout_.addWidget(close_button, alignment=Qt.AlignTop | Qt.AlignRight)

            # 创建一个容器控件，用于放置图片和关闭按钮
            container_widget = QWidget()
            container_widget.setLayout(image_layout_)

            # 将容器控件添加到图片布局中
            self.image_layout.insertWidget(self.image_layout.count() - 1, container_widget)

    def delete_image(self, image_path):
        """删除指定的图片"""
        if image_path in self.image_list:
            self.image_list.remove(image_path)
            self.reload_ui()  # 重新加载图片列表
        
    def show_zoomed_image(self, image_path):
        """显示放大图片窗口"""
        # 确保父窗口是当前的模态窗口
        self.zoom_window = ImageZoomWindow(image_path, parent=self.parent)
        self.zoom_window.show()
          
    def clear_image_layout(self):
        # 遍历布局中的所有项
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # 移除并销毁控件
                widget.setParent(None)
                widget.deleteLater() 
                
    def reload_ui(self):
        self.content_text.setText(self.content)  
        self.clear_image_layout() 
        if len(self.image_list) > 0:
            self.add_images()
            self.image_scroll_area.setVisible(True)
        else: 
            self.image_scroll_area.setVisible(False)
            
        if self.b_has_title_layout == True:
            date = QDate.fromString(self.str_date, "yyyy-MM-dd")
            if date.isValid():
                self.dateEdit.setDate(date)
            else:
                print("Invalid date string:", self.str_date)
                
            time = QTime.fromString(self.str_time, "HH:mm:ss")
            if time.isValid():
                self.timeEdit.setTime(time)
            else:
                print("Invalid time string:", self.str_time)
                
    def copy_text(self):
        #clipboard = QApplication.clipboard()
        #clipboard.setText(self.content_text.toPlainText())
        self._signal.emit("copy_one_content_dict_{}".format(json.dumps(self.get_content_data())))
        

    def del_text(self):
        #clipboard = QApplication.clipboard()
        #clipboard.setText(self.content_text.toPlainText())
        result = QMessageBox.question(self, APP_NAME, "你确定想删除?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            return 
        self.parent.del_one_content_data(self.content_text.toPlainText(), self.image_list)

        self._signal.emit("reload_content_data_layout")

    def edit_text(self):
        self.addOneContent_Win = AddOneContentWindow("编辑内容", self.content_text.toPlainText(),  "", "", self.image_list, False, self)
        self.addOneContent_Win._signal.connect(self.signal_recv_func)
        self.addOneContent_Win.setWindowModality(Qt.ApplicationModal)
        self.addOneContent_Win.show()
        self.addOneContent_Win.exec_()
        
        #self.content_text.setReadOnly(False)
        #self.content_text.setFocus()
        #self.content_text.moveCursor(QTextCursor.End)

    def generate_img(self):
        self.waiting_Win = WaitingWindow(self)
        self.waiting_Win.setWindowModality(Qt.ApplicationModal)
        self.waiting_Win.show() 
        
        content_text = self.content_text.toPlainText()
        thread = Thread(target=self.generate_img_thread, args=(content_text, ))
        thread.start()
        
        return

    def generate_img_thread(self, content_text):
        pos_text = app_info.POS_TEXT
        neg_text = app_info.NEG_TEXT
        
        # 获取文案的正向文本、反向文本
        if len(pos_text) == 0 or len(neg_text) == 0:
            iRet, msg_return = llm_generate_pos_neg_text_by_wenAn(content_text, LLM_MODEL_TYPE.Kimi)
            if iRet == APP_RET_CODE_SUCESS:
                try:
                    # 解决可能的异常1：
                    data_return = extract_json_to_dict(msg_return)
                    print("llm_generate_pos_neg_text_by_wenAn, 生成的数据类型是{}, 是:{}".format(type(data_return), data_return))
                    if False == isinstance(data_return, dict):
                        print_my("!!!获取文案的正向文本、反向文本：返回的json文件格式错误")
                        iRet = APP_RET_CODE_FORMAT_ERROR
                    else:
                        if len(pos_text) == 0:
                            pos_text = data_return["pos_text"]
                        if len(neg_text) == 0:
                            neg_text = data_return["neg_text"]
                except Exception as e:
                    print("generate_img_thread, 异常:{}".format(e))
                    #QMessageBox.information(self, APP_NAME, "创建内容失败{结果解析异常}", QMessageBox.Yes)
                    print_my("!!!获取文案的正向文本、反向文本：结果解析异常")
                    iRet = APP_RET_CODE_FORMAT_ERROR 
            else:
                # 不能在线程里弹出框，会出错
                #QMessageBox.information(self, APP_NAME, "创建内容失败{}".format(iRet), QMessageBox.Yes)
                print_my("!!!创建内容失败:{}".format(iRet))
            
        if len(pos_text) > 0 or len(neg_text) > 0:
            print_my("【文生图】使用的正向文本是【{}】    反向文本是【{}】".format(pos_text, neg_text))
            iRet, img_url_return = llm_get_result_image(pos_text, neg_text)
            
        # 关闭等待框口
        if self.waiting_Win is not None:
            print("generate_img_thread,关闭加载中窗口开始")
            self.waiting_Win.close()
            self.waiting_Win = None
            print("generate_img_thread,关闭加载中窗口成功")
        
        
        if iRet == APP_RET_CODE_SUCESS:
            try:
                if len(img_url_return) != 0 and True == os.path.exists(img_url_return):
                    self.image_list.append(img_url_return)
                    self._signal.emit("get_data_and_reload_content_data_layout")
                else:
                    print_my("!!!生成图片失败:{}, {}".format(iRet, img_url_return))
                return
            except json.JSONDecodeError as e:
                print("generate_img_thread, 异常:{}".format(e))
                #QMessageBox.information(self, APP_NAME, "创建内容失败{结果解析异常}", QMessageBox.Yes)
                print_my("!!!创建图片失败：结果解析异常")
                return
        else:
            # 不能在线程里弹出框，会出错
            #QMessageBox.information(self, APP_NAME, "创建内容失败{}".format(iRet), QMessageBox.Yes)
            print_my("!!!生成图片失败:{}".format(iRet))
            return 
        
    def get_content_data(self):
        content_info_data = {}

        # 获取日期和时间
        str_date = self.dateEdit.date().toString('yyyy-MM-dd')
        str_time = self.timeEdit.time().toString('HH:mm:ss')
        print(f'选择的日期是：{str_date}，选择的时间是：{str_time}')
        
        content_info_data["date"] = str_date
        content_info_data["time"] = str_time

        content_info_data["content"] = self.content_text.toPlainText()
        content_info_data["image_list"] = self.image_list
        #content_info_data["title"] = self.title_label.text()
        return content_info_data
    def signal_recv_func(self, para): 
        if para.startswith("add_one_content_dict_"):
            print("ContentRow事件收到信号:{}".format(para))
            add_one_content_dict_str = para.strip("add_one_content_dict_")
            try:
                add_one_content_dict = json.loads(add_one_content_dict_str)
                print(add_one_content_dict)   
                self.content = add_one_content_dict["wenAn"]
                self.image_list = add_one_content_dict["img_paths"]        
                self.reload_ui() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
            
        return
        
class AddContentWindow(QDialog):
    _signal = pyqtSignal(str)
    _signal_self = pyqtSignal(str)
    def __init__(self, title, content_name, content_product_name, content_scene_type, go_where, tong_dian, superiority, content_count, content_data_list, product_info_list, content_info_list, parent):
        super().__init__()
        self.title = title
        self.content_name = content_name
        self.content_product_name = content_product_name
        self.content_scene_type = content_scene_type
        self.go_where = go_where
        self.tong_dian = tong_dian
        self.superiority = superiority
        self.content_count = content_count
        self.content_data_list = content_data_list
        self.product_info_list = product_info_list
        self.content_info_list = content_info_list
        # 补充空的图片
        for content_data in self.content_data_list:
            if "image_list" not in content_data:
                content_data["image_list"] = []
                
        self.mainWindow = parent
        print("AddContentWindow, __init__")
        self.initUI()
        self._signal_self.connect(self.self_signal_recv_func) 

    def initUI(self):
        # 设置对话框标题
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.title)
        #self.resize(int(1250), int(535))
        self.resize(int(g_desktop_w*6/7), int(g_desktop_h*9/10))
        # 禁止窗口大小拉伸
        self.setFixedSize(self.width(), self.height())
        
        #########################################
        # 文案的名称
        self.layout1 = QHBoxLayout()
        self.labelContentName = HoverLabel("文案的名称:<font color='red'>*</font> <font color='blue'>?</font>", "给要创建的文案取一个名称", self)
        self.contentNameEdit = QTextEdit()
        self.contentNameEdit.setPlaceholderText("在这里输入要添加的文案的名称")
        font_metrics = self.contentNameEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.contentNameEdit.setFixedHeight(line_height + 10) 
        self.contentNameEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.content_name) > 0:
            self.contentNameEdit.setText(self.content_name)
            self.contentNameEdit.setReadOnly(True)
            self.contentNameEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        else:
            # 随机生成一个名字
            for i in range(1, 100):
                content_name = "文案" + str(i)
                if content_name not in [content_info["content_name"] for content_info in self.content_info_list]:
                    break
            self.contentNameEdit.setText(content_name)
        self.layout1.addWidget(self.labelContentName)
        self.layout1.addWidget(self.contentNameEdit)
        # 内容关联的产品 
        self.layout2 = QHBoxLayout()
        self.labelProduct = HoverLabel("关联的产品:<font color='red'>*</font> <font color='blue'>?</font>", "将根据产品的信息(如:产品名称、产品描述)来创建对应此产品的内容", self)
        self.content_product_combo_box = QComboBox(self)
        self.reload_product_combo_box()
        self.content_product_combo_box.currentIndexChanged.connect(self.on_item_changed_of_content_product_combo_box)
        self.layout2.addWidget(self.labelProduct)
        self.layout2.addWidget(self.content_product_combo_box)
        # 内容的场景
        self.layout3 = QHBoxLayout()
        self.labelSceneType = HoverLabel("场景:<font color='red'>*</font> <font color='blue'>?</font>", "我们提供了一些场景的类型，并对这些场景进行了符合人心理习惯的定制。\n不同的场景类型，我们在生成的文案上做了优化，达到更好的营销效果。", self)
        self.scene_combo_box = QComboBox(self)
        for agent_name in AGENT_CONFIG_DICT:
            self.scene_combo_box.addItem(agent_name)
        self.scene_combo_box.setCurrentIndex(0)
        if len(self.content_scene_type) > 0:
            for i, agent_name in enumerate(AGENT_CONFIG_DICT):
                if self.content_scene_type == agent_name:
                    self.scene_combo_box.setCurrentIndex(i)
                    break
        self.layout3.addWidget(self.labelSceneType)
        self.layout3.addWidget(self.scene_combo_box)
        # 引流去向
        self.layout4 = QHBoxLayout()
        self.labelGoWhereType = HoverLabel("引流去向: <font color='blue'>?</font>", "在文案中，当别人想对你的产品有更多了解时，可以到哪里查看更多消息，比如：官网地址、视频号地址、微信号、直播间地址等。", self)
        self.goWhereEdit = QTextEdit()
        self.goWhereEdit.setPlaceholderText("在这里输入引流去向")
        font_metrics = self.goWhereEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.goWhereEdit.setFixedHeight(line_height + 10) 
        self.goWhereEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.go_where) > 0:
            self.goWhereEdit.setText(self.go_where)
            self.goWhereEdit.setReadOnly(True)
            self.goWhereEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        self.layout4.addWidget(self.labelGoWhereType)
        self.layout4.addWidget(self.goWhereEdit)
        # 客户痛点 
        self.layout5 = QHBoxLayout()
        self.labelTongDian = HoverLabel("客户痛点: <font color='blue'>?</font>", "根据你对客户的了解，客户的痛点是什么。描述好痛点，将使文案更符合你的要求，比如：价格不透明、服务态度差、缺乏个性化等。", self)
        self.tongDianEdit = QTextEdit()
        self.tongDianEdit.setPlaceholderText("用一句话描述客户的痛点")
        font_metrics = self.tongDianEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.tongDianEdit.setFixedHeight(line_height + 10) 
        self.tongDianEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.tong_dian) > 0:
            self.tongDianEdit.setText(self.tong_dian)
            self.tongDianEdit.setReadOnly(True)
            self.tongDianEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        self.layout5.addWidget(self.labelTongDian)
        self.layout5.addWidget(self.tongDianEdit)
        # 重点突出的产品优势 
        self.layout6 = QHBoxLayout()
        self.labelSuperiority = HoverLabel("重点突出的产品优势: <font color='blue'>?</font>", "将描述“产品的优势”的内容加入文案中，能够使文案更吸引关注、增强竞争力、满足需求、提升信心。比如：长效的续航能力、优质的服务态度、允许个性化定制等。", self)
        self.superiorityEdit = QTextEdit()
        self.superiorityEdit.setPlaceholderText("用一句话描述你在文案中要重点突出的产品优势")
        font_metrics = self.superiorityEdit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.superiorityEdit.setFixedHeight(line_height + 10) 
        self.superiorityEdit.setLineWrapMode(QTextEdit.NoWrap)
        if len(self.superiority) > 0:
            self.superiorityEdit.setText(self.superiority)
            self.superiorityEdit.setReadOnly(True)
            self.superiorityEdit.setStyleSheet("""
            QTextEdit {
                background-color: #E0E0E0;  /* 灰色背景 */
                color: #808080;            /* 灰色文字 */
                border: 1px solid #D0D0D0; /* 灰色边框 */
            }
            """)
        self.layout6.addWidget(self.labelSuperiority)
        self.layout6.addWidget(self.superiorityEdit)
        # 条数
        self.layout7 = QHBoxLayout()
        self.labelContentCount = HoverLabel("条数:<font color='red'>*</font> <font color='blue'>?</font>", "您要创建的内容的条数(1-10条)", self)
        self.contentCountEdit = QLineEdit(self)
        self.contentCountEdit.setPlaceholderText("在这里输入要添加的内容的条数(1-10条)")
        int_validator = QIntValidator(1, 10)
        self.contentCountEdit.setValidator(int_validator)
        if len(self.content_count) > 0:
            self.contentCountEdit.setText(self.content_count)
        self.layout7.addWidget(self.labelContentCount)
        self.layout7.addWidget(self.contentCountEdit)
        # 使用的大模型
        self.layout8 = QHBoxLayout()
        #
        self.labelLlmType = HoverLabel("大模型/Coze智能体:<font color='red'>*</font> <font color='blue'>?</font>", "选择自动创建内容时使用的大模型或扣子智能体的类型", self)
        #
        self.llm_combo_box = QComboBox(self)
        for llm_name in LLM_MODEL_NAME_TYPE_DICT:
            self.llm_combo_box.addItem(llm_name)
        self.llm_combo_box.setCurrentIndex(0)
        #
        self.addNewLLMBtn = QPushButton("添加新的智能体")
        self.addNewLLMBtn.clicked.connect(self.addNewLLMBtnFun)
        self.layout8.addWidget(self.labelLlmType, 4)
        self.layout8.addWidget(self.llm_combo_box, 8)
        self.layout8.addWidget(self.addNewLLMBtn, 1)
        
        # 按钮
        self.layout9 = QHBoxLayout()
        #    生成按钮
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
        #    手动添加文案
        self.button_human_add = QPushButton("手动添加文案", self)
        self.button_human_add.clicked.connect(self.humanAddBtnFun)
        #    导出文案
        self.button_export = QPushButton("导出文案", self)
        self.button_export.clicked.connect(self.exportContentBtnFun)
        #    导入文案
        self.button_import = QPushButton("导入文案", self)
        self.button_import.clicked.connect(self.importContentBtnFun)
        self.layout9.addWidget(self.button_generate)
        self.layout9.addWidget(self.button_human_add)
        self.layout9.addWidget(self.button_export)
        self.layout9.addWidget(self.button_import)
        self.layout9.addStretch()
        
        # 内容数据列表
        self.scroll_area_content = QScrollArea()
        self.scroll_area_content.setWidgetResizable(True)

        self.container_content = QWidget()
        self.container_layout_content = QVBoxLayout()
        self.container_layout_content.setSpacing(1) 
        self.container_layout_content.setAlignment(Qt.AlignTop)
        self.container_content.setLayout(self.container_layout_content)

        self.scroll_area_content.setWidget(self.container_content)
        self.reload_content_data_layout()
        
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
        layout.addLayout(self.layout8)
        layout.addLayout(self.layout9)
        layout.addWidget(self.scroll_area_content)
        layout.addWidget(self.confirmBtn)
        
        # 设置布局
        self.setLayout(layout)

    def add_content_row(self, content, image_list):
        row = ContentRow("", "", content, image_list, False, self)
        row._signal.connect(self.signal_recv_func)
        self.container_layout_content.addWidget(row)

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
        content_data_list_new = []
        for content_data in self.content_data_list:
            if content_data["content"] == content and content_data["image_list"] == image_list:
                print("删除了一条数据")
                continue
            content_data_list_new.append(content_data)
        self.content_data_list = content_data_list_new
                    
    def reload_content_data_layout(self):
        self.clear_container_layout_content()
        for content_data in self.content_data_list:
            self.add_content_row(content_data["content"], content_data["image_list"])
        #self.add_content_row("标题2", "子标题2", "这是第二行的正文内容")
        if len(self.content_data_list) == 0:
            self.button_generate.setText("开始自动生成")
        else:
            self.button_generate.setText("重新自动生成")

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
     
    def confirmBtnFun(self):
        # 获取文案的名称
        str_contentName = self.contentNameEdit.toPlainText()
        if len(str_contentName) == 0:
            QMessageBox.information(self, APP_NAME, "请输入文案的名称", QMessageBox.Yes)
            return
        b_repeat_name = False 
        for content_info in self.content_info_list:
            if content_info["content_name"] == str_contentName:
                b_repeat_name = True 
                break
        if b_repeat_name == True and self.title == "添加文案":
            QMessageBox.information(self, APP_NAME, "文案的名称已经存在，请换另一个名称", QMessageBox.Yes)
            return
        # 获取文案关联的产品 
        content_product_name = self.content_product_combo_box.currentText()
        content_product_name = content_product_name.strip(" ")
        if len(content_product_name) == 0:
            QMessageBox.information(self, APP_NAME, "请选择文案关联的产品", QMessageBox.Yes)
            return
        # 获取内容的场景
        content_scene_type = self.scene_combo_box.currentText()
        if len(content_scene_type) == 0:
            QMessageBox.information(self, APP_NAME, "请选择场景", QMessageBox.Yes)
            return
        # 获得引流去向
        str_goWhere = self.goWhereEdit.toPlainText()
        str_goWhere = str_goWhere.strip()
        # 客户痛点
        str_tongDian = self.tongDianEdit.toPlainText()
        str_tongDian = str_tongDian.strip()
        # 重点突出的产品优势
        str_superiority = self.superiorityEdit.toPlainText()
        str_superiority = str_superiority.strip()
        # 获取内容
        self.content_data_list = self.get_content_data_info_list()
        if len(self.content_data_list) <= 0:
            QMessageBox.information(self, APP_NAME, "请生成或填写内容", QMessageBox.Yes)
            return
            
        add_content_data_dict = {}
        if len(self.content_name) != 0:
            add_content_data_dict["content_name_orig"] = self.content_name
        add_content_data_dict["content_name"] = str_contentName
        add_content_data_dict["content_product_name"] = content_product_name
        add_content_data_dict["content_scene_type"] = content_scene_type
        add_content_data_dict["go_where"] = str_goWhere
        add_content_data_dict["tong_dian"] = str_tongDian
        add_content_data_dict["superiority"] = str_superiority
        add_content_data_dict["content_count"] = str(len(self.content_data_list))
        add_content_data_dict["content_data_list"] = self.content_data_list
        self._signal.emit("add_content_dict_{}".format(json.dumps(add_content_data_dict)))
        
        self.close()
        return

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
        content_scene_type = self.scene_combo_box.currentText()   
        
        # 获得引流去向
        str_goWhere = self.goWhereEdit.toPlainText()
        str_goWhere = str_goWhere.strip()
        # 客户痛点
        str_tongDian = self.tongDianEdit.toPlainText()
        str_tongDian = str_tongDian.strip()
        # 重点突出的产品优势
        str_superiority = self.superiorityEdit.toPlainText()
        str_superiority = str_superiority.strip()
        # 获取条数 
        text_count = self.contentCountEdit.text()
        text_count = text_count.strip(" ")
        if len(text_count) == 0:
            QMessageBox.information(self, APP_NAME, "请输入要添加的内容的条数", QMessageBox.Yes)
            return 
        if int(text_count) <= 0:
            QMessageBox.information(self, APP_NAME, "请输入正确的条数", QMessageBox.Yes)
            return 
        if int(text_count) > 10:
            QMessageBox.information(self, APP_NAME, "输入的条数只能是1-10条", QMessageBox.Yes)
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
        thread = Thread(target=self.generate_content_thread, args=(content_scene_type, content_product_name, product_summary, content_examples, str_goWhere, str_tongDian, str_superiority, text_count, llm_type_enum))
        thread.start()
        
        return
    
    def addNewLLMBtnFun(self):
        self.mainWindow.signal_of_table.emit("jump_to_setting_tab_llm") 
        self.close()
        return
    
    # 手动添加文案按钮的响应函数
    def humanAddBtnFun(self):
        self.addOneContent_Win = AddOneContentWindow("添加文案", "", "", "", [], False, self)
        self.addOneContent_Win._signal.connect(self.signal_recv_func)
        self.addOneContent_Win.setWindowModality(Qt.ApplicationModal)
        self.addOneContent_Win.show()
        self.addOneContent_Win.exec_()
        return        

    # 导出文案按钮的响应函数
    def exportContentBtnFun(self):
        excel_file_path = ""
        # 获取内容
        content_data_list = self.get_content_data_info_list()
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

    # 导入内容按钮的响应函数
    def importContentBtnFun(self):
        # 创建一个Tkinter根窗口，但不显示
        root = tk.Tk()
        root.withdraw()

        # 打开文件选择对话框，设置过滤器只显示xlsx文件
        excel_file_path = filedialog.askopenfilename(
            title='选择一个Excel文件',
            filetypes=[('Excel文件', '*.xlsx')]
        )

        # 检查用户是否选择了文件
        if excel_file_path:
            print(f'选择的excel文件路径: {excel_file_path}')
            content_data_list = load_content_from_excel(excel_file_path)
            if len(content_data_list) <= 0:
                QMessageBox.information(self, APP_NAME, "没有加载到内容", QMessageBox.Yes)
                return
            self.content_data_list = content_data_list
            self.reload_content_data_layout()
        else:
            print('没有选择excel文件')
             
    def generate_content_thread(self, agent_type, content_product_name, product_summary, content_examples, go_where, tong_dian, str_superiority, text_count, llm_type_enum):
        iRet, data_return = llm_generate_content(agent_type, content_product_name, product_summary, content_examples, go_where, tong_dian, str_superiority, text_count, llm_type_enum)
        # 关闭等待框口
        if self.waiting_Win is not None:
            print("generate_content_thread,关闭加载中窗口开始")
            self.waiting_Win.close()
            self.waiting_Win = None
            print("generate_content_thread,关闭加载中窗口成功")
        
        
        if iRet == APP_RET_CODE_SUCESS:
            try:
                # 解决可能的异常1：
                data_return_list = json.loads(data_return)
                print("llm_generate_content, 生成的数据类型是{}, 是:{}".format(type(data_return_list), data_return_list))
                if True == isinstance(data_return_list, dict):
                    data_return_list = [data_return_list]
                # 解决可能的异常2：
                for data_return in data_return_list:
                    if True == isinstance(data_return["index"], int):
                        data_return["index"] = str(data_return["index"])
                # 解决可能的异常3:
                pass 
            
                # 补充空的图片
                for data_return in data_return_list:
                    if "image_list" not in data_return:
                        #data_return["image_list"] = [".\\示例图片.JPG"]
                        data_return["image_list"] = []
                
                self.content_data_list = data_return_list
                self._signal_self.emit("reload_content_data_layout")
            except json.JSONDecodeError as e:
                print("generate_content_thread, 异常:{}".format(e))
                #QMessageBox.information(self, APP_NAME, "创建内容失败{结果解析异常}", QMessageBox.Yes)
                print_my("!!!创建内容失败：结果解析异常（可能条数太多了，请控制在20条以内）")
                return
        else:
            # 不能在线程里弹出框，会出错
            #QMessageBox.information(self, APP_NAME, "创建内容失败{}".format(iRet), QMessageBox.Yes)
            print_my("!!!创建内容失败:{}".format(iRet))
            return 
        
    def on_item_changed_of_content_product_combo_box(self, index):
        sel_text = self.content_product_combo_box.currentText()
        print("内容关联产品的索引发生变化，当前选中：{}".format(sel_text))
        if sel_text == "添加...":
            self.content_product_combo_box.setCurrentIndex(self.previous_index_of_content_product_combo_box)
            self.addProduct_Win = AddProductWindow('添加产品', "", "", "", [], self.product_info_list, self)
            self.addProduct_Win._signal.connect(self.signal_recv_func)
            self.addProduct_Win.setWindowModality(Qt.ApplicationModal)
            self.addProduct_Win.show()
            self.addProduct_Win.exec_()
        else:
            self.previous_index_of_content_product_combo_box = index
        return

    def self_signal_recv_func(self, para): 
        if para == "reload_content_data_layout":
            print("self_signal_recv_func，AddContentWindow事件收到信号:{}".format(para))
            self.reload_content_data_layout()
        return 
            
    def signal_recv_func(self, para): 
        if para == "reload_content_data_layout":
            print("signal_recv_func， AddContentWindow事件收到信号:{}".format(para))
            self.reload_content_data_layout()
        elif para == "get_data_and_reload_content_data_layout":
            print("signal_recv_func， AddContentWindow事件收到信号:{}".format(para))
            self.content_data_list = self.get_content_data_info_list()
            self.reload_content_data_layout()
        elif para.startswith("set_friend_username_"):
            print("AddContentWindow事件收到信号:{}".format(para))
            
            usename_list_str = para.strip("set_friend_username_")
            usename_list = ast.literal_eval(usename_list_str) 
            print(usename_list)
            self.username_of_group_list = usename_list
            labelText = "成员:{}".format("、".join(self.username_of_group_list))
            self.labelMembers.setText(labelText)
        elif para.startswith("hua_su_file_paths_"):
            print("AddContentWindow事件收到信号:{}".format(para))
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
            print("AddContentWindow事件收到信号:{}".format(para))
            add_product_data_dict_str = para.strip("add_product_dict_")
            try:
                add_product_data_dict = json.loads(add_product_data_dict_str)
                print(add_product_data_dict)
                # 因为这个类里使用的self.product_info_list是外面传进来的，当下面emit给Table发信号时，会把新数据添加到变量里，
                # 这个动作后，这里的变量也会变化的，所以这里不需要再append一次  
                #self.product_info_list.append(add_product_data_dict)
                self._signal.emit(para)        
                self.content_product_name = add_product_data_dict["product_name"]               
                self.reload_product_combo_box() 
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")    
        elif para.startswith("add_one_content_dict_"):
            print("AddContentWindow事件收到信号:{}".format(para))
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
                self.content_data_list.append(content_data)
                self.reload_content_data_layout()

            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
        elif para.startswith("copy_one_content_dict_"):
            print("AddContentWindow事件收到信号:{}".format(para))
            copy_one_content_dict_str = para.strip("copy_one_content_dict_")
            try:
                copy_one_content_dict = json.loads(copy_one_content_dict_str)
                print(copy_one_content_dict)           
                self.addOneContent_Win = AddOneContentWindow("添加文案", copy_one_content_dict["content"], "", "", copy_one_content_dict["image_list"], False, self)
                self.addOneContent_Win._signal.connect(self.signal_recv_func)
                self.addOneContent_Win.setWindowModality(Qt.ApplicationModal)
                self.addOneContent_Win.show()
                self.addOneContent_Win.exec_()
            except json.JSONDecodeError as e:
                print(f"json解析错误：{e}")   
        return

    def reload_product_combo_box(self): 
        self.content_product_combo_box.clear()
        for product_info in self.product_info_list:
            self.content_product_combo_box.addItem(product_info["product_name"])
        if len(self.product_info_list) > 0:
            self.content_product_combo_box.setCurrentIndex(0)
            self.previous_index_of_content_product_combo_box = 0
            
        # 没数据时做特殊处理
        if len(self.product_info_list) == 0:
            self.content_product_combo_box.addItem("  ")
            self.content_product_combo_box.setCurrentIndex(0)
            self.previous_index_of_content_product_combo_box = 0
            
        self.content_product_combo_box.addItem("添加...")
        if len(self.content_product_name) > 0:
            for i, product_info in enumerate(self.product_info_list):
                if self.content_product_name == product_info["product_name"]:
                    self.content_product_combo_box.setCurrentIndex(i)
                    self.previous_index_of_content_product_combo_box = i
                    break
                        
# 测试
"""
app = QApplication(sys.argv)
dialog = AddContentWindow([], [], None)
dialog.show()
sys.exit(app.exec_())
"""