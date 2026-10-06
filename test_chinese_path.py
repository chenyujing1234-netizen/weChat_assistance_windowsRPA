# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from log_helper import print_my
from app_info import APP_HTML_DIR

# 自定义WebEnginePage类，用于捕获JavaScript控制台日志
class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS控制台] {level}: {message} (行号: {lineNumber}, 源: {sourceID})")

class TestWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        print("TestWindow 初始化")
        # 设置窗口标题和大小
        self.setWindowTitle('测试中文路径')
        self.setGeometry(300, 300, 800, 600)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 添加标签显示当前工作目录
        current_dir = os.getcwd()
        dir_label = QLabel(f"当前工作目录: {current_dir}")
        layout.addWidget(dir_label)
        
        # 测试按钮
        test_btn = QPushButton("测试创建WebEngineView")
        test_btn.clicked.connect(self.test_web_engine)
        layout.addWidget(test_btn)
        
        self.setLayout(layout)
        
    def test_web_engine(self):
        print("开始测试WebEngineView")
        try:
            # 创建WebEngineView
            self.web_view = QWebEngineView()
            print("WebEngineView 创建成功")
            
            # 设置自定义的WebEnginePage以捕获JavaScript控制台日志
            self.custom_page = CustomWebEnginePage()
            print("CustomWebEnginePage 创建成功")
            
            # 这里是可能导致程序退出的代码
            self.web_view.setPage(self.custom_page)
            print("setPage 执行成功")
            
            # 尝试加载HTML文件
            me_html_path = os.path.join(os.getcwd(), f"{APP_HTML_DIR}/me.html")
            print(f"HTML文件路径: {me_html_path}")
            print(f"文件是否存在: {os.path.exists(me_html_path)}")
            
            if os.path.exists(me_html_path):
                self.web_view.load(QUrl.fromLocalFile(me_html_path))
                print("HTML文件加载成功")
            
            # 添加到布局
            self.layout().addWidget(self.web_view)
            print("WebEngineView 添加到布局成功")
            
        except Exception as e:
            print(f"测试过程中发生异常: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    # 确保中文显示正常
    QApplication.setApplicationName("测试中文路径")
    
    app = QApplication(sys.argv)
    dialog = TestWindow()
    dialog.show()
    sys.exit(app.exec_())