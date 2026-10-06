import sys
import os
import time
import ctypes
import subprocess
import winreg
import pyautogui
import threading
from ctypes import wintypes

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QWindow

# Windows API 准备
user32 = ctypes.windll.user32
SetParent = user32.SetParent
SetWindowLong = user32.SetWindowLongW
GetWindowLong = user32.GetWindowLongW
ShowWindow = user32.ShowWindow
BringWindowToTop = user32.BringWindowToTop
SetForegroundWindow = user32.SetForegroundWindow
GetDesktopWindow = user32.GetDesktopWindow

GWL_STYLE = -16
WS_CHILD = 0x40000000
WS_OVERLAPPEDWINDOW = 0x00CF0000
SW_RESTORE = 9

APP_RET_CODE_UNKNOW = -1
APP_RET_CODE_SUCESS = 0

# ------------------------------------------------
# 微信路径和启动逻辑
# ------------------------------------------------
def get_wechat_path():
    """返回 WeChat/Weixin.exe 的完整路径；找不到返回 None"""
    # 1. 注册表查找
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\Weixin") as key:
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            exe_path = os.path.join(install_path, "Weixin.exe")
            if os.path.isfile(exe_path):
                return exe_path
    except (FileNotFoundError, OSError):
        pass

    # 2. 常见安装目录
    candidates = [
        r"%ProgramFiles%\Tencent\WeChat\WeChat.exe",
        r"%ProgramFiles(x86)%\Tencent\WeChat\WeChat.exe",
        r"%ProgramFiles%\Tencent\Weixin\Weixin.exe",
        r"%ProgramFiles(x86)%\Tencent\Weixin\Weixin.exe",
    ]
    for cand in candidates:
        exe_path = os.path.expandvars(cand)
        if os.path.isfile(exe_path):
            return exe_path
    return None

def start_wechat():
    """启动微信；成功返回 True，失败返回 False"""
    exe = get_wechat_path()
    if not exe:
        print("未找到 Weixin/WeChat.exe，请确认已安装微信或手动指定路径")
        return False
    try:
        subprocess.Popen([exe])
        print("微信启动成功")
        return True
    except Exception as e:
        print("启动失败：", e)
        return False

# ------------------------------------------------
# 微信窗口句柄获取逻辑
# ------------------------------------------------
def get_wechat_window():
    """通过 pyautogui 查找微信窗口句柄"""
    hwd_wechat = None
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows()  # 所有窗口
    for fw in fw_all:
        if fw.title.startswith("微信"):   # 找微信
            iRet = APP_RET_CODE_SUCESS
            hwd_wechat = fw._hWnd
            break
    return iRet, hwd_wechat

# ------------------------------------------------
# 主窗口逻辑
# ------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("微信嵌入/还原 Demo")
        self.setGeometry(100, 100, 800, 600)

        self.application_window = None
        self.app_container = None
        self.wechat_hwnd = None

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        self.layout = QVBoxLayout(mainWidget)

        self.label = QLabel("这里会嵌入微信窗口")
        self.layout.addWidget(self.label)

        self.button_launch_wechat = QPushButton("启动微信")
        self.button_launch_wechat.clicked.connect(self.launch_wechat)
        self.layout.addWidget(self.button_launch_wechat)

        self.button_merge_wechat = QPushButton("嵌入微信窗口")
        self.button_merge_wechat.clicked.connect(self.merge_wechat)
        self.layout.addWidget(self.button_merge_wechat)

        self.button_restore_wechat = QPushButton("还原微信窗口")
        self.button_restore_wechat.clicked.connect(self.restore_wechat)
        self.layout.addWidget(self.button_restore_wechat)

    def launch_wechat(self):
        """启动微信，并查找窗口句柄"""
        # 打印当前线程ID
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        print(f"当前线程ID: {thread_id}")
        
        if not start_wechat():
            return
        print("等待微信窗口就绪...")
        time.sleep(5)
        iRet, hwnd = get_wechat_window()
        if iRet == APP_RET_CODE_SUCESS and hwnd:
            print(f"找到微信窗口句柄: {hwnd}")
            self.wechat_hwnd = hwnd
        else:
            print("未找到微信窗口，请确保微信已启动并登录。")

    def merge_wechat(self):
        """将微信窗口嵌入 PyQt 窗口"""
        if not self.wechat_hwnd:
            print("请先启动并找到微信窗口。")
            return
        
        # 打印当前线程ID
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        print(f"当前线程ID: {thread_id}")
        
        print(f"准备嵌入微信窗口 hwnd = {self.wechat_hwnd}")
        self.application_window = QWindow.fromWinId(self.wechat_hwnd)
        self.app_container = QWidget.createWindowContainer(self.application_window)
        self.layout.addWidget(self.app_container)
        if self.label:
            self.label.hide()
        print("微信窗口已嵌入。")

    def restore_wechat(self):
        """将微信窗口从嵌入状态还原为独立窗口"""
        if not self.application_window:
            print("当前没有已嵌入的微信窗口")
            return
            
        # 打印当前线程ID
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        print(f"当前线程ID: {thread_id}")
        
        hwnd_wechat = int(self.application_window.winId())
        print(f"准备还原微信窗口, hwnd = {hwnd_wechat}")
        if self.app_container:
            self.layout.removeWidget(self.app_container)
            self.app_container.setParent(None)
            self.app_container.deleteLater()
            self.app_container = None
            print("微信窗口容器已移除。")
        desktop_hwnd = GetDesktopWindow()
        SetParent(hwnd_wechat, desktop_hwnd)
        style = GetWindowLong(hwnd_wechat, GWL_STYLE)
        style = (style & ~WS_CHILD) | WS_OVERLAPPEDWINDOW
        SetWindowLong(hwnd_wechat, GWL_STYLE, style)
        ShowWindow(hwnd_wechat, SW_RESTORE)
        BringWindowToTop(hwnd_wechat)
        SetForegroundWindow(hwnd_wechat)
        if self.label:
            self.label.show()
        print("微信窗口已从嵌入状态还原为独立窗口。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
