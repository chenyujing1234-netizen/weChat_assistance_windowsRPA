import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, QObject, Qt
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from dialog_payment import PaymentWindow

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('PaymentWindowTest')

# 自定义WebEnginePage以捕获JavaScript控制台消息
class ConsoleMessageWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # 转换Qt的日志级别到Python的logging级别
        log_level = logging.DEBUG
        if level == QWebEnginePage.InfoMessageLevel:
            log_level = logging.INFO
        elif level == QWebEnginePage.WarningMessageLevel:
            log_level = logging.WARNING
        elif level == QWebEnginePage.ErrorMessageLevel:
            log_level = logging.ERROR
        
        logger.log(log_level, f"JS Console [{sourceID}:{lineNumber}]: {message}")

# 重写PaymentWindow类以便添加更多的调试信息
class DebugPaymentWindow(PaymentWindow):
    def __init__(self, config_json_data=None):
        super().__init__(config_json_data)
        logger.debug("PaymentWindow initialized")
        
        # 使用自定义的WebEnginePage来捕获控制台消息
        self.web_view.setPage(ConsoleMessageWebEnginePage(self.web_view))
        
        # 连接信号以获取更多信息
        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.urlChanged.connect(self.on_url_changed)
        self.backend._signal.connect(self.on_backend_signal)
    
    @pyqtSlot()
    def on_load_started(self):
        logger.debug(f"开始加载页面: {self.web_view.url().toString()}")
    
    @pyqtSlot(bool)
    def on_load_finished(self, success):
        logger.debug(f"页面加载完成: {success}, 当前URL: {self.web_view.url().toString()}")
        
        # 尝试执行JavaScript来测试后端调用
        self.web_view.page().runJavaScript("console.log('测试JavaScript执行');")
        
        # 强制触发一次二维码获取，用于测试
        self.web_view.page().runJavaScript("setTimeout(function() {\n" \
                                          "    console.log('强制触发二维码获取');\n" \
                                          "    if (typeof getPaymentQrCode === 'function') {\n" \
                                          "        getPaymentQrCode();\n" \
                                          "    } else {\n" \
                                          "        console.error('getPaymentQrCode函数未定义');\n" \
                                          "    }\n" \
                                          "}, 1000);")
    
    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        logger.debug(f"URL已更改: {url.toString()}")
    
    def on_backend_signal(self, para):
        logger.debug(f"收到后端信号: {para}")
        super().signal_recv_func(para)

if __name__ == '__main__':
    logger.info("开始测试PaymentWindow")
    
    # 确保中文显示正常
    QApplication.setApplicationName("续费充值测试")
    
    app = QApplication(sys.argv)
    
    # 创建一个简单的配置数据对象
    config_data = {"BIND_PHONE": "15280006510"}
    logger.debug(f"配置数据: {config_data}")
    
    # 检查HTML文件是否存在
    current_dir = os.getcwd()
    payment_html_path = os.path.join(current_dir, "html/payment.html")
    logger.debug(f"检查HTML文件: {payment_html_path}")
    if os.path.exists(payment_html_path):
        logger.debug(f"HTML文件存在，大小: {os.path.getsize(payment_html_path)} 字节")
    else:
        logger.error(f"HTML文件不存在: {payment_html_path}")
    
    # 创建并显示PaymentWindow
    dialog = DebugPaymentWindow(config_data)
    dialog.show()
    
    # 运行应用程序
    logger.info("应用程序已启动")
    sys.exit(app.exec_())