import sys
import os
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from log_helper import print_my
from app_info import APP_HTML_DIR
from html_backend import HtmlBackend
import sys

# 自定义WebEnginePage类，用于捕获JavaScript控制台日志
class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS控制台] {level}: {message} (行号: {lineNumber}, 源: {sourceID})")

class PaymentWindow(QDialog):
    _signal = pyqtSignal(str)
    
    def __init__(self, config_json_data=None):
        super().__init__()
        self.config_json_data = config_json_data
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('续费充值')
        self.setGeometry(300, 50, 800, 950)
        
        # 移除对话框右上角的问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 创建中心部件
        layout = QVBoxLayout()
        
        # 创建WebEngineView
        self.web_view = QWebEngineView()
        
        # 设置自定义的WebEnginePage以捕获JavaScript控制台日志
        self.custom_page = CustomWebEnginePage()
        self.web_view.setPage(self.custom_page)
        
        # 设置WebChannel，用于与页面通信
        self.channel = QWebChannel()
        self.backend = HtmlBackend(self.config_json_data)
        self.backend._signal.connect(self.signal_recv_func)
        self.channel.registerObject("backend", self.backend)
        
        self.web_view.page().setWebChannel(self.channel)
        
        # 加载本地HTML文件 - 使用项目根目录确保正确加载
        current_dir = os.getcwd()
        payment_html_path = os.path.join(current_dir, f"{APP_HTML_DIR}/payment.html")
        print(f"加载HTML文件路径: {payment_html_path}")
        self.web_view.load(QUrl.fromLocalFile(payment_html_path))
        
        # 添加到布局
        layout.addWidget(self.web_view)
        self.setLayout(layout)
        
    def signal_recv_func(self, para): 
        print(f"PaymentWindow事件收到信号:{para}")
        # 处理不同类型的信号
        if para.startswith("switch_product"):
            # 切换产品
            self._signal.emit(para)
        elif para.startswith("select_wechat_number"):
            # 选择微信数量
            self._signal.emit(para)
        elif para.startswith("select_subscription_plan"):
            # 选择订阅计划
            self._signal.emit(para)
        elif para.startswith("switch_payment_method"):
            # 切换支付方式
            self._signal.emit(para)
        elif para.startswith("verify_activation_code"):
            # 验证激活码
            self._signal.emit(para)
        elif para.startswith("close_payment"):
            # 关闭支付窗口
            self.close()
        return 

if __name__ == '__main__':
    # 确保中文显示正常
    QApplication.setApplicationName("续费充值")
    
    app = QApplication(sys.argv)
    dialog = PaymentWindow()
    dialog.show()
    sys.exit(app.exec_())