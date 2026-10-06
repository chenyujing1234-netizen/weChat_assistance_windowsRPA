from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
import sys
import os
import json

# 确保中文正常显示
import matplotlib
matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS控制台] {level}: {message} (行号: {lineNumber}, 源: {sourceID})")

# 创建一个后端对象，用于与前端JavaScript通信
class Backend(QObject):
    # 定义信号
    userInfoLoaded = pyqtSignal(bool, dict)
    rechargeHistoryLoaded = pyqtSignal(bool, list)
    
    @pyqtSlot()
    def load_user_info(self):
        print("后端: 加载用户信息")
        # 模拟用户信息数据
        user_info = {
            "phone_number": "15280006510",
            "multi_open_expire": "2025-10-21 13:57:48",
            "multi_open_remaining": "24",
            "ai_expire": "-"
        }
        print(f"后端: 用户信息数据: {user_info}")
        # 发出信号，通知前端用户信息已加载
        self.userInfoLoaded.emit(True, user_info)
    
    @pyqtSlot()
    def load_recharge_history(self):
        print("后端: 加载充值记录")
        # 模拟充值记录数据
        recharge_records = [{
            "time": "2024-04-21 10:30:00",
            "duration": "1个月",
            "description": "多开服务充值"
        }]
        print(f"后端: 充值记录数据: {recharge_records}")
        # 发出信号，通知前端充值记录已加载
        self.rechargeHistoryLoaded.emit(True, recharge_records)
    
    @pyqtSlot(str)
    def switch_menu(self, menu_name):
        print(f"后端: 切换菜单到: {menu_name}")
    
    @pyqtSlot()
    def lock_screen(self):
        print("后端: 锁屏")
    
    @pyqtSlot()
    def switch_account(self):
        print("后端: 切换账号")
    
    @pyqtSlot()
    def renew_service(self):
        print("后端: 续费")

class MeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 打印应用程序信息
        print(f"PyQt5应用程序初始化")
        
        # 设置窗口标题和大小
        self.setWindowTitle("账户设置")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建WebEngineView
        self.web_view = QWebEngineView()
        
        # 创建自定义页面以捕获JavaScript控制台输出
        self.web_page = CustomWebEnginePage()
        self.web_view.setPage(self.web_page)
        
        # 创建WebChannel
        self.channel = QWebChannel()
        
        # 创建后端对象
        self.backend = Backend()
        
        # 将后端对象注册到WebChannel
        self.channel.registerObject('backend', self.backend)
        
        # 将WebChannel设置到WebEnginePage
        self.web_view.page().setWebChannel(self.channel)
        
        print("WebChannel已初始化，后端对象已注册")
        
        # 启用JavaScript
        settings = self.web_view.settings()
        settings.setAttribute(settings.JavascriptEnabled, True)
        
        print("WebEngine设置: JavaScript已启用")
        
        # 获取当前工作目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"当前工作目录: {current_dir}")
        
        # 构建me.html的完整路径
        html_path = os.path.join(current_dir, "html", "me.html")
        print(f"HTML文件路径: {html_path}")
        
        # 检查文件是否存在
        if os.path.exists(html_path):
            print(f"文件存在，大小: {os.path.getsize(html_path)} 字节")
        else:
            print(f"错误: 文件不存在: {html_path}")
            # 尝试列出html目录内容
            html_dir = os.path.join(current_dir, "html")
            if os.path.exists(html_dir):
                print(f"html目录内容: {os.listdir(html_dir)}")
            else:
                print(f"html目录不存在: {html_dir}")
        
        # 转换为URL格式
        url = QUrl.fromLocalFile(html_path)
        
        # 打印加载的URL以进行调试
        print(f"加载URL: {url.toString()}")
        
        # 连接信号以获取加载状态
        self.web_view.loadStarted.connect(lambda: print("开始加载页面"))
        self.web_view.loadFinished.connect(lambda success: print(f"页面加载完成: {success}"))
        self.web_view.urlChanged.connect(lambda url: print(f"URL已更改: {url.toString()}"))
        
        # 加载HTML文件
        self.web_view.setUrl(url)
        
        # 设置中心部件
        self.setCentralWidget(self.web_view)

if __name__ == "__main__":
    print("开始运行测试应用程序")
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建并显示窗口
    window = MeWindow()
    window.show()
    
    print("应用程序已启动，等待用户交互...")
    # 运行应用程序
    sys.exit(app.exec_())