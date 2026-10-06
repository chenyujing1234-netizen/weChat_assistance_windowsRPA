# -*- coding: utf-8 -*-

import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtGui import QMovie, QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

class WaitingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.center_on_parent()

    def initUI(self):
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        layout = QVBoxLayout()
        # 创建一个标签用于显示动画
        self.label = QLabel(self)
        # 这里可以替换为你自己的动画文件
        self.movie = QMovie('loading.gif')
        self.label.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setGeometry(200, 200, 100, 100)
        
    def center_on_parent(self):
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore() 
        else:
            super(WaitingWindow, self).keyPressEvent(event)