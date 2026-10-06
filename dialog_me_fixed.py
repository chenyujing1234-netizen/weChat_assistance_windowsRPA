import sys
import os
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QCoreApplication
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
        
        # 加载本地HTML文件 - 使用绝对路径并确保编码正确
        try:
            # 使用QCoreApplication.applicationDirPath()获取程序目录，避免中文路径问题
            app_dir = QCoreApplication.applicationDirPath()
            html_dir = os.path.join(app_dir, APP_HTML_DIR)
            me_html_path = os.path.join(html_dir, "me.html")
            
            # 确保路径使用正斜杠，避免Windows路径问题
            me_html_path = me_html_path.replace('\\', '/')
            
            print(f"加载HTML文件路径: {me_html_path}")
            
            # 检查文件是否存在
            if os.path.exists(me_html_path):
                # 使用fromLocalFile加载本地文件，确保路径编码正确
                url = QUrl.fromLocalFile(me_html_path)
                self.web_view.load(url)
                print(f"HTML文件加载成功: {url.toString()}")
            else:
                print(f"HTML文件不存在: {me_html_path}")
                # 如果文件不存在，尝试使用相对路径
                current_dir = os.getcwd().replace('\\', '/')
                relative_path = f"{current_dir}/{APP_HTML_DIR}/me.html"
                print(f"尝试使用相对路径: {relative_path}")
                if os.path.exists(relative_path):
                    self.web_view.load(QUrl.fromLocalFile(relative_path))
                else:
                    # 如果都不存在，加载一个简单的HTML页面
                    print("使用默认HTML内容")
                    self.web_view.setHtml("""
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>账户设置</title>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 20px; }
                            .error { color: red; }
                        </style>
                    </head>
                    <body>
                        <h1>账户设置</h1>
                        <p class="error">无法加载HTML文件，请检查程序路径是否包含中文字符。</p>
                        <p>当前程序路径: {}</p>
                        <p>尝试加载的HTML路径: {}</p>
                    </body>
                    </html>
                    """.format(app_dir, me_html_path))
        except Exception as e:
            print(f"加载HTML文件时出错: {e}")
            # 如果加载失败，显示错误信息
            self.web_view.setHtml(f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>账户设置 - 错误</title>
            </head>
            <body>
                <h1>账户设置</h1>
                <p>加载HTML文件时出错: {str(e)}</p>
            </body>
            </html>
            """)
        
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