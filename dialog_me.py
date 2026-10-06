import sys
import os
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from log_helper import print_my
from app_info import APP_HTML_DIR
from html_backend import HtmlBackend

# 自定义WebEnginePage类，用于捕获JavaScript控制台日志
class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS控制台] {level}: {message} (行号: {lineNumber}, 源: {sourceID})")

class MeWindow(QDialog):
    _signal = pyqtSignal(str)
    
    def __init__(self, config_json_data):
        super().__init__()
        self.config_json_data = config_json_data
        self.initUI()
        
    def initUI(self):
        print("MeWindow 111111")
        # 设置窗口标题和大小
        self.setWindowTitle('账户设置')
        self.setGeometry(300, 300, 800, 600)
        
        # 移除对话框右上角的问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 创建中心部件
        layout = QVBoxLayout()
        print("MeWindow 22222")
        # 创建WebEngineView
        self.web_view = QWebEngineView()
        print("MeWindow 33333")
        # 设置自定义的WebEnginePage以捕获JavaScript控制台日志
        try:
            # 设置自定义的WebEnginePage以捕获JavaScript控制台日志
            self.custom_page = CustomWebEnginePage()
            print("MeWindow 33333 -- self.custom_page")
            self.web_view.setPage(self.custom_page)
            print("MeWindow 44444 - WebEnginePage设置成功")
        except Exception as e:
            print(f"设置WebEnginePage时出错: {e}")
            # 如果设置自定义页面失败，使用默认页面
            print("使用默认WebEnginePage")
        # 设置WebChannel，用于与页面通信
        self.channel = QWebChannel()
        self.backend = HtmlBackend(self.config_json_data)
        self.backend._signal.connect(self.signal_recv_func)
        self.channel.registerObject("backend", self.backend)
        print("MeWindow 5555")
        self.web_view.page().setWebChannel(self.channel)
        print("MeWindow 66666")
        # 加载本地HTML文件 - 使用项目根目录确保正确加载
        current_dir = os.getcwd()
        me_html_path = os.path.join(current_dir, f"{APP_HTML_DIR}/me.html")
        print(f"加载HTML文件路径: {me_html_path}")
        self.web_view.load(QUrl.fromLocalFile(me_html_path))
        
        # 添加到布局
        layout.addWidget(self.web_view)
        self.setLayout(layout)
        
    def signal_recv_func(self, para): 
        print(f"MeWindow事件收到信号:{para}")
        # 处理不同类型的信号
        if para.startswith("switch_account"):
            # 切换账号
            self.close()
            self._signal.emit(para)
        elif para.startswith("lock_screen"):
            # 锁屏操作
            self._signal.emit(para)
        elif para.startswith("renew_service"):
            # 续费操作
            self._signal.emit(para)
        elif para.startswith("menu_switch_"):
            # 菜单切换操作
            self._signal.emit(para)
        return 

if __name__ == '__main__':
    # 确保中文显示正常
    QApplication.setApplicationName("账户设置")
    
    # 导入sys模块
    import sys
    
    # 创建一个模拟的配置数据对象用于测试
    mock_config = {
        "BIND_PHONE": "15280006511",
        "USERNAME": "测试用户"
    }
    
    app = QApplication(sys.argv)
    dialog = MeWindow(mock_config)
    dialog.show()
    sys.exit(app.exec_())