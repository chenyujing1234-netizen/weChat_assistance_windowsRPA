# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

class SplashScreen(QSplashScreen):
    def __init__(self):
        # 创建一个启动画面
        super().__init__()
        
        # 设置启动画面大小和样式
        self.setFixedSize(400, 200)
        
        # 设置窗口标志
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        
        # 设置启动画面文本
        self.showMessage("正在启动程序，请稍候...", 
                        Qt.AlignBottom | Qt.AlignHCenter, 
                        Qt.white)
        
        # 设置样式
        self.setStyleSheet("""
            QSplashScreen {
                background-color: #2b5797;
                border-radius: 10px;
            }
        """)
        
    def showMessage(self, message, alignment=Qt.AlignBottom | Qt.AlignHCenter, color=Qt.white):
        """重写showMessage方法以支持自定义字体"""
        super().showMessage(message, alignment, color)
        
        # 设置字体
        font = QFont("Arial", 12)
        font.setBold(True)
        self.setFont(font)
        
    def updateMessage(self, message):
        """更新启动画面消息"""
        self.showMessage(message)
        QApplication.processEvents()  # 立即更新显示