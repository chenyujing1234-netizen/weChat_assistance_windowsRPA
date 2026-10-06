# -*- coding: utf-8 -*-
"""
坐标标注工具
用于可视化标注和管理 location.cfg 配置文件中的坐标
"""

import sys
import os
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QListWidget, QListWidgetItem, QFileDialog,
                             QMessageBox, QSplitter, QGroupBox, QLineEdit, QComboBox,
                             QScrollArea, QCheckBox, QSpinBox)
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage, QFont


class ImageLabel(QLabel):
    """支持绘制坐标点和矩形框的图片标签"""
    
    # 信号：点击坐标 (x, y)
    point_clicked = pyqtSignal(int, int)
    # 信号：矩形框绘制完成 (x1, y1, x2, y2)
    rect_drawn = pyqtSignal(int, int, int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #2b2b2b; border: 2px solid #555;")
        
        self.original_pixmap = None  # 原始图片
        self.scale_factor = 1.0  # 缩放比例
        
        # 绘制模式：'point' 点坐标, 'rect' 矩形框
        self.draw_mode = 'point'
        
        # 矩形框绘制相关
        self.drawing = False
        self.rect_start = None
        self.rect_end = None
        
        # 当前显示的坐标标注
        self.annotations = []  # [(type, x, y) or (type, x1, y1, x2, y2), ...]
        
    def set_image(self, image_path):
        """加载图片"""
        if not os.path.exists(image_path):
            QMessageBox.warning(self, "错误", f"图片文件不存在：{image_path}")
            return False
        
        self.original_pixmap = QPixmap(image_path)
        if self.original_pixmap.isNull():
            QMessageBox.warning(self, "错误", "无法加载图片")
            return False
        
        # 自适应缩放
        self.fit_to_window()
        return True
    
    def fit_to_window(self):
        """图片自适应窗口大小"""
        if self.original_pixmap is None:
            return
        
        # 计算缩放比例
        widget_width = self.width()
        widget_height = self.height()
        img_width = self.original_pixmap.width()
        img_height = self.original_pixmap.height()
        
        scale_w = widget_width / img_width
        scale_h = widget_height / img_height
        self.scale_factor = min(scale_w, scale_h, 1.0)  # 不放大，只缩小
        
        self.update_display()
    
    def zoom_in(self):
        """放大"""
        self.scale_factor *= 1.2
        self.update_display()
    
    def zoom_out(self):
        """缩小"""
        self.scale_factor /= 1.2
        self.update_display()
    
    def reset_zoom(self):
        """重置缩放"""
        self.fit_to_window()
    
    def update_display(self):
        """更新显示"""
        if self.original_pixmap is None:
            return
        
        # 缩放图片
        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * self.scale_factor),
            int(self.original_pixmap.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 在缩放后的图片上绘制标注
        self.draw_annotations(scaled_pixmap)
    
    def draw_annotations(self, pixmap):
        """在图片上绘制标注"""
        if not self.annotations:
            self.setPixmap(pixmap)
            return
        
        # 创建一个可编辑的副本
        result_pixmap = QPixmap(pixmap)
        painter = QPainter(result_pixmap)
        
        # 绘制已有标注
        for annotation in self.annotations:
            if len(annotation) == 3:  # 点坐标
                ann_type, x, y = annotation
                # 缩放坐标
                scaled_x = int(x * self.scale_factor)
                scaled_y = int(y * self.scale_factor)
                
                # 绘制十字标记
                pen = QPen(QColor(0, 255, 0), 2)
                painter.setPen(pen)
                size = 10
                painter.drawLine(scaled_x - size, scaled_y, scaled_x + size, scaled_y)
                painter.drawLine(scaled_x, scaled_y - size, scaled_x, scaled_y + size)
                
                # 绘制坐标文本
                painter.setPen(QColor(255, 255, 0))
                painter.setFont(QFont("Arial", 10, QFont.Bold))
                painter.drawText(scaled_x + 15, scaled_y - 5, f"({x}, {y})")
                
            elif len(annotation) == 5:  # 矩形框
                ann_type, x1, y1, x2, y2 = annotation
                # 缩放坐标
                scaled_x1 = int(x1 * self.scale_factor)
                scaled_y1 = int(y1 * self.scale_factor)
                scaled_x2 = int(x2 * self.scale_factor)
                scaled_y2 = int(y2 * self.scale_factor)
                
                # 绘制矩形框
                pen = QPen(QColor(255, 0, 0), 2)
                painter.setPen(pen)
                painter.drawRect(scaled_x1, scaled_y1, 
                               scaled_x2 - scaled_x1, scaled_y2 - scaled_y1)
                
                # 绘制坐标文本
                painter.setPen(QColor(255, 255, 0))
                painter.setFont(QFont("Arial", 9, QFont.Bold))
                painter.drawText(scaled_x1 + 5, scaled_y1 - 5, 
                               f"({x1},{y1})-({x2},{y2})")
        
        # 绘制正在绘制的矩形框
        if self.drawing and self.rect_start and self.rect_end:
            pen = QPen(QColor(0, 255, 255), 2, Qt.DashLine)
            painter.setPen(pen)
            rect = QRect(self.rect_start, self.rect_end)
            painter.drawRect(rect.normalized())
        
        painter.end()
        self.setPixmap(result_pixmap)
    
    def set_annotations(self, annotations):
        """设置要显示的标注"""
        self.annotations = annotations
        self.update_display()
    
    def clear_annotations(self):
        """清除所有标注"""
        self.annotations = []
        self.update_display()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if self.original_pixmap is None:
            return
        
        if event.button() == Qt.LeftButton:
            # 获取点击位置相对于图片的坐标
            click_pos = event.pos()
            
            # 计算图片在label中的偏移
            pixmap_rect = self.pixmap().rect()
            label_rect = self.rect()
            offset_x = (label_rect.width() - pixmap_rect.width()) // 2
            offset_y = (label_rect.height() - pixmap_rect.height()) // 2
            
            # 转换为图片坐标
            img_x = click_pos.x() - offset_x
            img_y = click_pos.y() - offset_y
            
            # 检查是否在图片范围内
            if 0 <= img_x < pixmap_rect.width() and 0 <= img_y < pixmap_rect.height():
                if self.draw_mode == 'point':
                    # 点坐标模式：转换回原始图片坐标
                    orig_x = int(img_x / self.scale_factor)
                    orig_y = int(img_y / self.scale_factor)
                    self.point_clicked.emit(orig_x, orig_y)
                    
                elif self.draw_mode == 'rect':
                    # 矩形框模式：开始绘制
                    self.drawing = True
                    self.rect_start = click_pos
                    self.rect_end = click_pos
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.drawing and self.draw_mode == 'rect':
            self.rect_end = event.pos()
            self.update_display()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            
            if self.rect_start and self.rect_end and self.rect_start != self.rect_end:
                # 计算图片偏移
                pixmap_rect = self.pixmap().rect()
                label_rect = self.rect()
                offset_x = (label_rect.width() - pixmap_rect.width()) // 2
                offset_y = (label_rect.height() - pixmap_rect.height()) // 2
                
                # 转换为图片坐标
                x1 = self.rect_start.x() - offset_x
                y1 = self.rect_start.y() - offset_y
                x2 = self.rect_end.x() - offset_x
                y2 = self.rect_end.y() - offset_y
                
                # 转换回原始图片坐标
                orig_x1 = int(x1 / self.scale_factor)
                orig_y1 = int(y1 / self.scale_factor)
                orig_x2 = int(x2 / self.scale_factor)
                orig_y2 = int(y2 / self.scale_factor)
                
                # 确保坐标顺序正确
                min_x = min(orig_x1, orig_x2)
                max_x = max(orig_x1, orig_x2)
                min_y = min(orig_y1, orig_y2)
                max_y = max(orig_y1, orig_y2)
                
                self.rect_drawn.emit(min_x, min_y, max_x, max_y)
            
            self.rect_start = None
            self.rect_end = None
            self.update_display()


class LocationAnnotationTool(QMainWindow):
    """坐标标注工具主窗口"""
    
    def __init__(self):
        super().__init__()
        self.config_file = 'location.cfg'
        self.config = None
        self.current_device = 'Windows'  # 当前标注的设备类型
        self.current_coord_key = None  # 当前标注的坐标key
        
        # 坐标类型定义（key: (显示名称, 标注类型, 是否成对)）
        self.coord_types = {
            # 单点坐标
            'FRIEND_CHAT_LIST_LT_X': ('好友列表左上角X', 'x', 'FRIEND_CHAT_LIST_LT_Y'),
            'FRIEND_CHAT_LIST_LT_Y': ('好友列表左上角Y', 'y', 'FRIEND_CHAT_LIST_LT_X'),
            'CHAT_LT_X': ('聊天窗口左上角X', 'x', 'CHAT_LT_Y'),
            'CHAT_LT_Y': ('聊天窗口左上角Y', 'y', 'CHAT_LT_X'),
            'BTN_NAV_WEIXIN_X': ('微信按钮X', 'x', 'BTN_NAV_WEIXIN_Y'),
            'BTN_NAV_WEIXIN_Y': ('微信按钮Y', 'y', 'BTN_NAV_WEIXIN_X'),
            'BTN_NAV_CONTACTS_X': ('通讯录按钮X', 'x', 'BTN_NAV_CONTACTS_Y'),
            'BTN_NAV_CONTACTS_Y': ('通讯录按钮Y', 'y', 'BTN_NAV_CONTACTS_X'),
            'BTN_NAV_DISCOVER_X': ('发现按钮X', 'x', 'BTN_NAV_DISCOVER_Y'),
            'BTN_NAV_DISCOVER_Y': ('发现按钮Y', 'y', 'BTN_NAV_DISCOVER_X'),
            'BTN_NAV_ME_X': ('我按钮X', 'x', 'BTN_NAV_ME_Y'),
            'BTN_NAV_ME_Y': ('我按钮Y', 'y', 'BTN_NAV_ME_X'),
            
            # 矩形框坐标（4个值）
            'FRIEND_LIST_BBOX': ('好友列表截图区域', 'bbox', ['FRIEND_LIST_BBOX_X1', 'FRIEND_LIST_BBOX_Y1', 'FRIEND_LIST_BBOX_X2', 'FRIEND_LIST_BBOX_Y2']),
            'CHAT_CONTENT_BBOX': ('聊天内容截图区域', 'bbox', ['CHAT_CONTENT_BBOX_X1', 'CHAT_CONTENT_BBOX_Y1', 'CHAT_CONTENT_BBOX_X2', 'CHAT_CONTENT_BBOX_Y2']),
        }
        
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("微信坐标标注工具 v1.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # === 左侧面板：设备和坐标列表 ===
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # === 中间面板：图片显示区域 ===
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)
        
        # === 右侧面板：坐标信息和控制 ===
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割比例
        splitter.setSizes([300, 700, 300])
        
        self.statusBar().showMessage("就绪")
    
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 设备选择
        device_group = QGroupBox("设备类型")
        device_layout = QVBoxLayout()
        
        self.device_combo = QComboBox()
        self.device_combo.addItems([
            'Local_Emulator',
            'WiFi_Phone_Xiaomi_8_Pro',
            'Yun_Phone_720_1080',
            'Windows',
            'Windows_1366_768'
        ])
        self.device_combo.setCurrentText('Windows')
        self.device_combo.currentTextChanged.connect(self.on_device_changed)
        device_layout.addWidget(self.device_combo)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # 坐标类型列表
        coord_group = QGroupBox("坐标类型")
        coord_layout = QVBoxLayout()
        
        self.coord_list = QListWidget()
        self.coord_list.itemClicked.connect(self.on_coord_selected)
        coord_layout.addWidget(self.coord_list)
        
        coord_group.setLayout(coord_layout)
        layout.addWidget(coord_group)
        
        # 刷新列表
        refresh_btn = QPushButton("🔄 刷新配置")
        refresh_btn.clicked.connect(self.load_config)
        layout.addWidget(refresh_btn)
        
        return panel
    
    def create_center_panel(self):
        """创建中间面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        load_img_btn = QPushButton("📁 加载图片")
        load_img_btn.clicked.connect(self.load_image)
        toolbar.addWidget(load_img_btn)
        
        toolbar.addStretch()
        
        zoom_in_btn = QPushButton("🔍+ 放大")
        zoom_in_btn.clicked.connect(lambda: self.image_label.zoom_in())
        toolbar.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton("🔍- 缩小")
        zoom_out_btn.clicked.connect(lambda: self.image_label.zoom_out())
        toolbar.addWidget(zoom_out_btn)
        
        reset_zoom_btn = QPushButton("↺ 适应窗口")
        reset_zoom_btn.clicked.connect(lambda: self.image_label.reset_zoom())
        toolbar.addWidget(reset_zoom_btn)
        
        layout.addLayout(toolbar)
        
        # 图片显示区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #1e1e1e;")
        
        self.image_label = ImageLabel()
        self.image_label.point_clicked.connect(self.on_point_clicked)
        self.image_label.rect_drawn.connect(self.on_rect_drawn)
        scroll_area.setWidget(self.image_label)
        
        layout.addWidget(scroll_area)
        
        return panel
    
    def create_right_panel(self):
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 当前坐标信息
        info_group = QGroupBox("当前坐标")
        info_layout = QVBoxLayout()
        
        self.current_coord_label = QLabel("未选择")
        self.current_coord_label.setWordWrap(True)
        self.current_coord_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        info_layout.addWidget(self.current_coord_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 标注模式
        mode_group = QGroupBox("标注模式")
        mode_layout = QVBoxLayout()
        
        self.mode_point_radio = QCheckBox("点坐标模式 (点击图片)")
        self.mode_point_radio.setChecked(True)
        self.mode_point_radio.toggled.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_point_radio)
        
        self.mode_rect_radio = QCheckBox("矩形框模式 (拖拽绘制)")
        self.mode_rect_radio.toggled.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_rect_radio)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # 坐标值输入
        value_group = QGroupBox("坐标值")
        value_layout = QVBoxLayout()
        
        # X坐标
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X:"))
        self.x_input = QSpinBox()
        self.x_input.setRange(0, 99999)
        x_layout.addWidget(self.x_input)
        value_layout.addLayout(x_layout)
        
        # Y坐标
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y:"))
        self.y_input = QSpinBox()
        self.y_input.setRange(0, 99999)
        y_layout.addWidget(self.y_input)
        value_layout.addLayout(y_layout)
        
        # X2坐标（矩形框用）
        x2_layout = QHBoxLayout()
        x2_layout.addWidget(QLabel("X2:"))
        self.x2_input = QSpinBox()
        self.x2_input.setRange(0, 99999)
        x2_layout.addWidget(self.x2_input)
        value_layout.addLayout(x2_layout)
        
        # Y2坐标（矩形框用）
        y2_layout = QHBoxLayout()
        y2_layout.addWidget(QLabel("Y2:"))
        self.y2_input = QSpinBox()
        self.y2_input.setRange(0, 99999)
        y2_layout.addWidget(self.y2_input)
        value_layout.addLayout(y2_layout)
        
        value_group.setLayout(value_layout)
        layout.addWidget(value_group)
        
        # 操作按钮
        btn_layout = QVBoxLayout()
        
        save_btn = QPushButton("💾 保存当前坐标")
        save_btn.clicked.connect(self.save_current_coord)
        save_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; font-weight: bold;")
        btn_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("🗑️ 清除标注")
        clear_btn.clicked.connect(self.clear_annotations)
        btn_layout.addWidget(clear_btn)
        
        save_all_btn = QPushButton("💾 保存配置文件")
        save_all_btn.clicked.connect(self.save_config)
        save_all_btn.setStyleSheet("background-color: #007bff; color: white; padding: 8px; font-weight: bold;")
        btn_layout.addWidget(save_all_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        return panel
    
    def load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            QMessageBox.warning(self, "警告", f"配置文件不存在：{self.config_file}")
            return
        
        try:
            self.config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
            self.config.read(self.config_file, encoding='utf-8')
            
            # 更新坐标列表
            self.update_coord_list()
            
            self.statusBar().showMessage(f"配置文件加载成功：{self.config_file}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置文件失败：{str(e)}")
    
    def update_coord_list(self):
        """更新坐标列表"""
        self.coord_list.clear()
        
        if self.config is None or self.current_device not in self.config.sections():
            return
        
        # 获取当前设备的所有配置项
        items = self.config.items(self.current_device)
        
        # 添加到列表
        for key, value in items:
            key_upper = key.upper()
            item = QListWidgetItem(f"{key_upper} = {value}")
            item.setData(Qt.UserRole, key_upper)
            self.coord_list.addItem(item)
    
    def on_device_changed(self, device):
        """设备类型改变"""
        self.current_device = device
        self.update_coord_list()
        self.statusBar().showMessage(f"切换到设备：{device}")
    
    def on_coord_selected(self, item):
        """坐标类型被选中"""
        self.current_coord_key = item.data(Qt.UserRole)
        self.current_coord_label.setText(f"{self.current_coord_key}")
        
        # 读取当前坐标值
        self.load_current_coord_value()
        
        # 显示在图片上
        self.show_coord_on_image()
        
        self.statusBar().showMessage(f"选中坐标：{self.current_coord_key}")
    
    def load_current_coord_value(self):
        """加载当前坐标的值"""
        if self.config is None or self.current_coord_key is None:
            return
        
        try:
            value = self.config.get(self.current_device, self.current_coord_key)
            
            # 解析值
            if '_X' in self.current_coord_key or self.current_coord_key.endswith('X1'):
                self.x_input.setValue(int(value))
            elif '_Y' in self.current_coord_key or self.current_coord_key.endswith('Y1'):
                self.y_input.setValue(int(value))
            elif self.current_coord_key.endswith('X2'):
                self.x2_input.setValue(int(value))
            elif self.current_coord_key.endswith('Y2'):
                self.y2_input.setValue(int(value))
                
        except Exception as e:
            print(f"加载坐标值失败：{e}")
    
    def show_coord_on_image(self):
        """在图片上显示当前坐标"""
        if self.image_label.original_pixmap is None:
            return
        
        annotations = []
        
        # 获取成对的坐标（如X和Y）
        if self.current_coord_key and self.current_coord_key.endswith('_X'):
            base_key = self.current_coord_key[:-2]
            x_key = base_key + '_X'
            y_key = base_key + '_Y'
            
            try:
                x = int(self.config.get(self.current_device, x_key))
                y = int(self.config.get(self.current_device, y_key))
                annotations.append(('point', x, y))
            except:
                pass
        
        elif self.current_coord_key and self.current_coord_key.endswith('_Y'):
            base_key = self.current_coord_key[:-2]
            x_key = base_key + '_X'
            y_key = base_key + '_Y'
            
            try:
                x = int(self.config.get(self.current_device, x_key))
                y = int(self.config.get(self.current_device, y_key))
                annotations.append(('point', x, y))
            except:
                pass
        
        # 显示矩形框
        elif self.current_coord_key and 'BBOX' in self.current_coord_key:
            base_key = self.current_coord_key.replace('_X1', '').replace('_Y1', '').replace('_X2', '').replace('_Y2', '')
            
            try:
                x1 = int(self.config.get(self.current_device, base_key + '_X1'))
                y1 = int(self.config.get(self.current_device, base_key + '_Y1'))
                x2 = int(self.config.get(self.current_device, base_key + '_X2'))
                y2 = int(self.config.get(self.current_device, base_key + '_Y2'))
                annotations.append(('rect', x1, y1, x2, y2))
            except:
                pass
        
        self.image_label.set_annotations(annotations)
    
    def on_mode_changed(self):
        """标注模式改变"""
        if self.mode_point_radio.isChecked():
            self.image_label.draw_mode = 'point'
            self.mode_rect_radio.setChecked(False)
            self.x2_input.setEnabled(False)
            self.y2_input.setEnabled(False)
        elif self.mode_rect_radio.isChecked():
            self.image_label.draw_mode = 'rect'
            self.mode_point_radio.setChecked(False)
            self.x2_input.setEnabled(True)
            self.y2_input.setEnabled(True)
    
    def on_point_clicked(self, x, y):
        """点击图片获取坐标"""
        self.x_input.setValue(x)
        self.y_input.setValue(y)
        self.statusBar().showMessage(f"点击坐标：({x}, {y})")
    
    def on_rect_drawn(self, x1, y1, x2, y2):
        """绘制矩形框完成"""
        self.x_input.setValue(x1)
        self.y_input.setValue(y1)
        self.x2_input.setValue(x2)
        self.y2_input.setValue(y2)
        self.statusBar().showMessage(f"矩形框：({x1}, {y1}) - ({x2}, {y2})")
    
    def load_image(self):
        """加载图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            if self.image_label.set_image(file_path):
                self.statusBar().showMessage(f"图片加载成功：{file_path}")
                self.show_coord_on_image()
    
    def save_current_coord(self):
        """保存当前坐标"""
        if self.config is None or self.current_coord_key is None:
            QMessageBox.warning(self, "警告", "请先选择要标注的坐标")
            return
        
        try:
            # 保存坐标值
            if self.current_coord_key.endswith('_X') or self.current_coord_key.endswith('_X1'):
                self.config.set(self.current_device, self.current_coord_key, str(self.x_input.value()))
            elif self.current_coord_key.endswith('_Y') or self.current_coord_key.endswith('_Y1'):
                self.config.set(self.current_device, self.current_coord_key, str(self.y_input.value()))
            elif self.current_coord_key.endswith('_X2'):
                self.config.set(self.current_device, self.current_coord_key, str(self.x2_input.value()))
            elif self.current_coord_key.endswith('_Y2'):
                self.config.set(self.current_device, self.current_coord_key, str(self.y2_input.value()))
            
            # 更新列表显示
            self.update_coord_list()
            
            # 更新图片上的显示
            self.show_coord_on_image()
            
            self.statusBar().showMessage(f"坐标已更新：{self.current_coord_key}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存坐标失败：{str(e)}")
    
    def save_config(self):
        """保存配置文件"""
        if self.config is None:
            QMessageBox.warning(self, "警告", "没有可保存的配置")
            return
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            
            QMessageBox.information(self, "成功", f"配置文件已保存：{self.config_file}")
            self.statusBar().showMessage("配置文件保存成功")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置文件失败：{str(e)}")
    
    def clear_annotations(self):
        """清除标注"""
        self.image_label.clear_annotations()
        self.statusBar().showMessage("已清除标注")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = LocationAnnotationTool()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

