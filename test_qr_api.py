import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from html_backend import HtmlBackend
from PyQt5.QtWebChannel import QWebChannel
from server_http_opt import http_init, APP_RET_CODE_SUCESS, g_b_Inited
import json

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('QrCodeApiTest')

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

# 自定义DebugBackend类，完全独立实现，不继承HtmlBackend
class DebugBackend(QObject):
    # 提供给原生main程序的信号 
    _signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        logger.info("初始化DebugBackend...")
    
    @pyqtSlot(str, str, str, result=str)
    def get_payment_qr_code(self, phone, subject, total_amount):
        """独立实现获取支付二维码方法"""
        logger.info(f"DebugBackend.get_payment_qr_code - 手机号: {phone}, 商品: {subject}, 金额: {total_amount}")
        
        try:
            # 直接返回一个测试用的二维码图片
            test_qr_code_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=test_payment_data"
            
            logger.info(f"DebugBackend: 返回测试二维码URL: {test_qr_code_url}")
            
            # 返回成功的响应
            return json.dumps({
                "success": True,
                "qr_code": test_qr_code_url
            })
        except Exception as e:
            logger.error(f"DebugBackend异常: {str(e)}")
            return json.dumps({
                "success": False,
                "message": f"DebugBackend异常: {str(e)}"
            })
    
    @pyqtSlot(str, result=str)
    def test_message(self, message):
        """测试消息方法"""
        logger.info(f"DebugBackend: 收到测试消息: {message}")
        return f"后端已收到消息: {message}"

# 创建一个QObject子类来正确处理信号和槽
class SignalHandler(QObject):
    def __init__(self):
        super().__init__()
        self.app_instance = None
        
    def set_app_instance(self, app_instance):
        self.app_instance = app_instance
    
    @pyqtSlot()
    def on_load_started(self):
        if self.app_instance and hasattr(self.app_instance, 'web_view'):
            logger.debug(f"开始加载页面: {self.app_instance.web_view.url().toString()}")
    
    @pyqtSlot(bool)
    def on_load_finished(self, success):
        if self.app_instance and hasattr(self.app_instance, 'web_view'):
            logger.debug(f"页面加载完成: {success}, 当前URL: {self.app_instance.web_view.url().toString()}")
            
            # 页面加载完成后，执行一些初始化JavaScript代码
            if success:
                init_js = """
                    console.log('Python端: 页面加载完成，准备测试');
                    // 等待WebChannel初始化完成后自动测试
                    setTimeout(function() {
                        console.log('Python端: 尝试自动测试获取二维码');
                        if (typeof getPaymentQrCode === 'function') {
                            console.log('Python端: 找到getPaymentQrCode函数');
                        } else {
                            console.log('Python端: 未找到getPaymentQrCode函数');
                        }
                    }, 2000);
                """
                self.app_instance.web_view.page().runJavaScript(init_js)
    
    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        logger.debug(f"URL已更改: {url.toString()}")
    
    @pyqtSlot(str)
    def on_backend_signal(self, para):
        logger.debug(f"收到后端信号: {para}")

class QrCodeApiTestApp:
    def __init__(self):
        logger.info("初始化二维码API测试应用")
        
        # 创建应用程序
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("二维码API测试")
        
        # 创建主窗口
        self.main_window = QWidget()
        self.main_window.setWindowTitle("二维码API测试")
        self.main_window.resize(800, 600)
        
        # 创建WebEngineView
        self.web_view = QWebEngineView(self.main_window)
        self.web_view.setPage(ConsoleMessageWebEnginePage(self.web_view))
        self.web_view.resize(800, 600)
        
        # 创建信号处理器
        self.signal_handler = SignalHandler()
        self.signal_handler.set_app_instance(self)
        
        # 设置WebChannel
        self.channel = QWebChannel()
        
        # 初始化配置数据
        self.config_data = {"BIND_PHONE": "15280006510"}
        
        # 初始化server_http_opt模块的全局变量
        logger.info("初始化server_http_opt模块...")
        try:
            # 导入全局变量
            from server_http_opt import g_str_mac_for_server, g_client_name, g_b_Inited
            
            # 设置必要的全局变量（按照测试用例中的值设置）
            g_str_mac_for_server = "345345346546757657"
            g_client_name = "wechat_assistant_test"
            g_b_Inited = True
            
            logger.info("server_http_opt模块初始化完成，已设置必要的全局变量")
            logger.info(f"g_str_mac_for_server: {g_str_mac_for_server}")
            logger.info(f"g_client_name: {g_client_name}")
            logger.info(f"g_b_Inited: {g_b_Inited}")
        except Exception as e:
            logger.error(f"初始化server_http_opt模块失败: {str(e)}")
        
        # 创建HtmlBackend实例
        self.backend = HtmlBackend(self.config_data)
        self.backend._signal.connect(self.signal_handler.on_backend_signal)
        
        # 注册backend对象
        self.channel.registerObject("backend", self.backend)
        self.web_view.page().setWebChannel(self.channel)
        
        # 加载测试HTML文件
        current_dir = os.getcwd()
        test_html_path = os.path.join(current_dir, "test_qr_code_api.html")
        logger.debug(f"加载测试HTML文件: {test_html_path}")
        
        if not os.path.exists(test_html_path):
            logger.error(f"测试HTML文件不存在: {test_html_path}")
            sys.exit(1)
        
        self.web_view.load(QUrl.fromLocalFile(test_html_path))
        
        # 连接信号
        self.web_view.loadStarted.connect(self.signal_handler.on_load_started)
        self.web_view.loadFinished.connect(self.signal_handler.on_load_finished)
        self.web_view.urlChanged.connect(self.signal_handler.on_url_changed)
        
        # 显示窗口
        self.main_window.show()
        
    def run(self):
        logger.info("启动应用程序...")
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    test_app = QrCodeApiTestApp()
    test_app.run()