import sys
import random
import time
import os
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from log_helper import print_my
from app_info import APP_HTML_DIR
from html_backend import HtmlBackend

class LoginWindow(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self, config_json_data):
        super().__init__()
        self.config_json_data = config_json_data
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('手机号验证码登录')
        self.setGeometry(300, 300, 500, 500)
        
        # 移除对话框右上角的问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 创建中心部件
        layout = QVBoxLayout()
        
        # 创建WebEngineView
        self.web_view = QWebEngineView()
        
        # 设置WebChannel，用于与页面通信
        self.channel = QWebChannel()
        self.backend = HtmlBackend(self.config_json_data)
        self.backend._signal.connect(self.signal_recv_func)
        self.channel.registerObject("backend", self.backend)
        
        self.web_view.page().setWebChannel(self.channel)
        
        # 加载本地HTML文件 - 使用绝对路径确保从当前脚本目录加载
        current_dir = os.getcwd()
        login_html_path = os.path.join(current_dir, f"{APP_HTML_DIR}/login.html")
        self.web_view.load(QUrl.fromLocalFile(login_html_path))
        
        # 添加到布局
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def signal_recv_func(self, para): 
        if para.startswith("login_sucess_"):
            print("LoginWindow事件收到信号:{}".format(para))
            self.close()
            self._signal.emit(para)
        return 

if __name__ == '__main__':
    # 确保中文显示正常
    QApplication.setApplicationName("登录系统")
    
    app = QApplication(sys.argv)
    dialog = LoginWindow()
    dialog.show()
    sys.exit(app.exec_())