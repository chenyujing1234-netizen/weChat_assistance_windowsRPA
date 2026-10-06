import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout,QWidget, QLabel, QFrame, QTextEdit)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QWindow, QFont, QPen, QColor, QBrush, QTextCursor
import time
from PyQt5.QtCore import Qt
from app_info import APP_NAME
import win32gui
import win32con
from PyQt5.QtCore import QRect
import win32process
import ctypes
import threading
from ctypes import wintypes
from PyQt5.QtCore import QTimer
from app_info import APP_IMG_DIR, g_b_Debug
from yang_hao_opt_helper_of_windows import *
from error_code import *


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

class RightPanelWindow(QWidget):
    _signal = pyqtSignal(str)
    _signal_self = pyqtSignal(str)
    def __init__(self, main_win):
        super().__init__()
        self.main_win = main_win           
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)  # 保留标题栏
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)       # 禁用最大化按钮
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)    # 禁用最小化按钮
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)       # 禁用关闭按钮

        # 1. 取屏幕可用几何
        screen = QApplication.primaryScreen().availableGeometry()
        sw, sh = screen.width(), screen.height()
        print(f"屏幕分辨率是:{sw} {sh}")
        # 2. 计算尺寸
        # 顶部对齐
        y = 30                
        #ww = int(sw * 4// 6) # 1280 ,1280的4/5是1024
        ww = int(sw * 5// 6) # 1600 ,1600的4/5是1280，如果要保存1024的话，比例改为  64 36 => 16 9
        #ww = 1280
        x = sw - ww          
        wh = sh - y
        #wh = 990

        # 3. 设置几何
        self.setGeometry(x, y, ww, wh)

        # 4.左侧微信预留窗口
        self.layoutWeChat = QVBoxLayout()
        #pixmap = QPixmap('app_logo.jpeg')
        pixmap = QPixmap(f"{APP_IMG_DIR}\\off_line.png")
        #self.wechat_width = int(ww*5/6)
        self.wechat_width = 1066
        self.wechat_height = wh
        #self.wechat_width = 1066
        #self.wechat_height = 990
        print(f"设置给微信停留的嵌入大小是:{self.wechat_width} {self.wechat_height}")
    
        pixmap = pixmap.scaled(self.wechat_width, self.wechat_height)
        self.labelWeChat = QLabel()
        self.labelWeChat.setPixmap(pixmap)
        self.layoutWeChat.addWidget(self.labelWeChat)
        self.wechat_container = None
        # 5. 右侧面板
        self.layoutRight = QVBoxLayout()
        # 创建日志显示控件
        self.layout_log = QVBoxLayout()
        self.logTextEdit = QTextEdit("初始化中...请稍候...")
        self.logTextEdit.setReadOnly(True)  # 设置为只读
        #     设置字体
        font = QFont("Arial", 15)  # Arial字体，12号大小
        self.logTextEdit.setFont(font)
        self.last_text_of_logTextEdit = ""
        self.layout_log.addWidget(self.logTextEdit)

        return_btn = QPushButton('运行中键鼠禁用\n恢复请按Esc键', self)
        return_btn.setStyleSheet("""
            QPushButton {
                background-color: #3366FF; /* 蓝色背景 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:hover {
                background-color: #1A387B; /* 鼠标悬停时的背景颜色 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:disabled {
                background-color: gray; /* 灰色背景 */
                color: black; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
            QPushButton:enabled {
                background-color: #3366FF; /* 蓝色背景 */
                color: red; /* 白色字体 */
                font-size: 38px; /* 字体大小 */
                font-weight: bold; /* 字体加粗 */
                border: 2px solid #1A387B; /* 边框样式 */
                border-radius: 10px; /* 圆角边框 */
                padding: 10px 20px; /* 增加按钮的内边距，使按钮看起来更大 */
            }
		""") 
        return_btn.clicked.connect(self.back_to_main)
        self.layoutRight.addLayout(self.layout_log)
        self.layoutRight.addWidget(return_btn)

        self.layout = QHBoxLayout()
        """
        self.frameWeChat = QFrame()
        self.frameWeChat.setLayout(self.layoutWeChat)
        self.frameWeChat.setFixedWidth(1066)
        self.frameWeChat.setFixedHeight(990)
        self.layout.addWidget(self.frameWeChat)
        self.layout.addLayout(self.layoutRight)
        """
        self.layout.addLayout(self.layoutWeChat, 19)
        self.layout.addLayout(self.layoutRight, 9)
        #self.layout.addLayout(self.layoutWeChat, 5)
        #self.layout.addLayout(self.layoutRight, 1)
        # 设置布局
        self.setLayout(self.layout)
        
        self._signal_self.connect(self.self_signal_recv_func) 
        self.hwd_wechat = None
        self.wechat_application_window = None
        self.hwd_wechat_child_list = []
        self.timer_monitor_child_windows_close = None
        self.timer_monitor_wechat_child_windows = None
        return

    def back_to_main(self):
        if self.timer_monitor_child_windows_close is not None: 
            self.timer_monitor_child_windows_close.stop()
            self.timer_monitor_child_windows_close = None
        if self.timer_monitor_wechat_child_windows is not None:
            self.timer_monitor_wechat_child_windows.stop()
            self.timer_monitor_wechat_child_windows = None

        self.restore_WeChat()
        # 关掉自己
        self.close()         

        # 重新显示主窗口
        self.main_win.show() 
        self.main_win.rightPanelWin = None
        # 给主窗口发停止的信号
        self._signal.emit("stop_btn_fun")
 
    def self_signal_recv_func(self, para): 
        if para.startswith("merge_wechat_windows_"):
            str_hwd_wechat = para.replace("merge_wechat_windows_", "")
            self.hwd_wechat = int(str_hwd_wechat)
            print("self_signal_recv_func，RightPanelWindow事件收到信号:{}".format(para))
            
            self.merge_WeChat()
        elif para == "back_to_main":
            print("self_signal_recv_func，RightPanelWindow事件收到信号:{}".format(para))
            self.back_to_main()
        elif para.startswith("log_"):
            message = para.strip("log_")
            self.write_log_to_windows(message)
        return 
    
    # 将微信嵌入窗体
    def merge_WeChat(self):
        print(f"merge_WeChat, 微信句柄号为{self.hwd_wechat}")
        if  self.hwd_wechat == None:
            return
        # 打印当前线程ID
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        print(f"merge_WeChat， 当前线程ID: {thread_id}")
        
        self.wechat_rect = win32gui.GetWindowRect(self.hwd_wechat)
        self.wechat_application_window = QWindow.fromWinId(self.hwd_wechat)
        print(f"微信对象为:{self.wechat_application_window}")
        print(f"设置微信的宽高为:({self.wechat_width}, {self.wechat_height})")
        self.wechat_application_window.resize(self.wechat_width, self.wechat_height) 
        self.labelWeChat.hide()
        if self.wechat_container is not None:
            self.layoutWeChat.removeWidget(self.wechat_container)
            self.wechat_container.setParent(None)
            self.wechat_container.deleteLater()
            self.wechat_container = None
        
        # 创建微信容器
        self.wechat_container = QWidget.createWindowContainer(self.wechat_application_window)
        self.layoutWeChat.addWidget(self.wechat_container)
        win32gui.SetParent(self.hwd_wechat, int(self.wechat_container.winId()))
        # 2. 让它“不拉伸”
        #self.wechat_container.setFixedSize(1066, 990)          # 按需要改
        # 或者只给最小尺寸
        # self.wechat_container.setMinimumSize(360, 640)
        #self.wechat_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #self.layoutWeChat.addWidget(self.wechat_container, alignment=Qt.AlignTop | Qt.AlignLeft)
        print(f"微信嵌入窗体成功")
        
        # ✅ 启动定时器，定时扫描子窗口
        if self.timer_monitor_wechat_child_windows is None:
            self.timer_monitor_wechat_child_windows = QTimer(self)
            self.timer_monitor_wechat_child_windows.timeout.connect(self.attach_wechat_child_windows)
            self.timer_monitor_wechat_child_windows.start(1000)  # 每 1 秒扫描一次
 
    def attach_wechat_child_windows(self):
        """扫描并让微信子窗口叠加在 Qt 容器中的主窗体上"""
        if not self.hwd_wechat or not self.wechat_container:
            return

        threadId, pid = win32process.GetWindowThreadProcessId(self.hwd_wechat)

        def callback(hwnd, extra):
            if hwnd == self.hwd_wechat:
                return True
            child_thread, child_pid = win32process.GetWindowThreadProcessId(hwnd)
            if child_pid != pid:
                return True

            title = win32gui.GetWindowText(hwnd)
            if extra is None and title not in ["设置", "添加朋友", "申请添加朋友", "朋友圈", "通讯录管理"]:
                # chenyj debug
                """
                if len(title) != 0:
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    parent_hwnd = win32gui.GetParent(hwnd)
                    b_parent_has_merge = False
                    if parent_hwnd in [hwd_wechat_child_info["hwnd"] for hwd_wechat_child_info in self.hwd_wechat_child_list]:
                        b_parent_has_merge = True
                    print(f"=======无法识别的微信子窗体[{hwnd}]:{title}【{left}, {top}, {right}, {bottom}】。父窗口[{parent_hwnd}]是否合并:{b_parent_has_merge}。线程id:{child_thread}(微信主窗体的线程id:{threadId})")
                """
                return True
            
            # 将不可见的微信子窗口显示出来,如果还是不可见就跳过
            if not win32gui.IsWindowVisible(hwnd):
                print(f"   微信子窗体{hwnd} - {title} 不可见，偿试将它显示出来")
                ShowWindow(hwnd, SW_RESTORE)
                BringWindowToTop(hwnd)
                SetForegroundWindow(hwnd)
                if not win32gui.IsWindowVisible(hwnd):
                    print(f"   微信子窗体{hwnd} - {title} 不可见，忽略")
                    return True

            
            if hwnd in [hwd_wechat_child_info["hwnd"] for hwd_wechat_child_info in self.hwd_wechat_child_list]:
                print("     !!!!这个窗口之前已经保存过了，忽略")
                return True
            
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            parent_hwnd = win32gui.GetParent(hwnd)
            b_parent_has_merge = False
            if parent_hwnd in [hwd_wechat_child_info["hwnd"] for hwd_wechat_child_info in self.hwd_wechat_child_list]:
                b_parent_has_merge = True
            print(f"确认微信子窗口 [{hwnd} - {title}] 【{left}, {top}, {right}, {bottom}】可以嵌入。父窗口{parent_hwnd}是否合并:{b_parent_has_merge}  ")
            try:
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                style = (style & ~win32con.WS_POPUP) | win32con.WS_CHILD
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

                container_hwnd = int(self.wechat_container.winId())
                print(f"设置微信子窗体{hwnd}的父窗口是:{container_hwnd}")
                if container_hwnd == self.hwd_wechat:
                    print("   这个父窗体是微信主窗体")
                else:
                    print("   这个父窗体不是微信主窗体")
                win32gui.SetParent(hwnd, container_hwnd)

                rect = win32gui.GetClientRect(container_hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOP,
                    0, 0, width, height,
                    win32con.SWP_SHOWWINDOW
                )
                print(f"子窗体覆盖成功: {hwnd} {title} w:{width} h:{height}")

                self.hwd_wechat_child_list.append({"hwnd":hwnd, "title":title})
                
                # 🔹 启动一个定时器监控子窗体是否关闭
                def check_child_closed():
                    if len(self.hwd_wechat_child_list) == 0:
                        if self.timer_monitor_child_windows_close is not None:
                            self.timer_monitor_child_windows_close.stop()
                            self.timer_monitor_child_windows_close = None
                        return False
                    hwd_top = self.hwd_wechat_child_list[-1]["hwnd"]
                    title_top = self.hwd_wechat_child_list[-1]["title"]
                    if not win32gui.IsWindow(hwd_top):  # 子窗体已销毁
                        print(f"检测到微信子窗体[{title_top}]{hwd_top}已销毁")
                        for hwd_wechat_child_info in self.hwd_wechat_child_list:
                            if hwd_top == hwd_wechat_child_info["hwnd"]:
                                self.hwd_wechat_child_list.remove(hwd_wechat_child_info)
                                break
                            
                        if len(self.hwd_wechat_child_list) == 0:
                            print("子窗体已全部关闭，恢复微信主窗体")
                            if self.timer_monitor_child_windows_close is not None:
                                self.timer_monitor_child_windows_close.stop()
                                self.timer_monitor_child_windows_close = None
                            
                            ShowWindow(self.hwd_wechat, SW_RESTORE)
                            BringWindowToTop(self.hwd_wechat)
                            SetForegroundWindow(self.hwd_wechat)
                            # chenyj test
                            container_hwnd = int(self.wechat_container.winId())
                            win32gui.SetParent(self.hwd_wechat, container_hwnd)
                            
                            if  self.wechat_container is not None:
                                self.wechat_container.update()
                            """
                            self.wechat_rect = win32gui.GetWindowRect(self.hwd_wechat)
                            self.wechat_application_window = QWindow.fromWinId(self.hwd_wechat)
                            print(f"微信对象为:{self.wechat_application_window}")
                            print(f"设置微信的宽高为:({self.wechat_width}, {self.wechat_height})")
                            self.wechat_application_window.resize(self.wechat_width, self.wechat_height) 
                            if self.wechat_container is not None:
                                self.layoutWeChat.removeWidget(self.wechat_container)
                                self.wechat_container.setParent(None)
                                self.wechat_container.deleteLater()
                                self.wechat_container = None
                            # 创建微信容器
                            self.wechat_container = QWidget.createWindowContainer(self.wechat_application_window)
                            self.layoutWeChat.addWidget(self.wechat_container)
                            """
                        else: 
                            hwd_top = self.hwd_wechat_child_list[-1]["hwnd"]
                            title_top = self.hwd_wechat_child_list[-1]["title"]
                            print(f"子窗体已关闭，恢复下一个窗体[{title_top}]{hwd_top}")
                            ShowWindow(hwd_top, SW_RESTORE)
                            BringWindowToTop(hwd_top)
                            SetForegroundWindow(hwd_top)
                            if  self.wechat_container is not None:
                                self.wechat_container.update()
                        
                        return False  # 停止定时器
                        
                    return True  # 继续检测

                # 每 500ms 检查一次子窗体是否关闭
                if self.timer_monitor_child_windows_close is None:
                    self.timer_monitor_child_windows_close = QTimer(self)
                    self.timer_monitor_child_windows_close.timeout.connect(lambda: (check_child_closed()))
                    self.timer_monitor_child_windows_close.start(500)

            except Exception as e:
                print(f"子窗体覆盖失败: {e}")

            return True

        win32gui.EnumWindows(callback, None)
        # 专门处理弹出的模态对话框窗体
        title_by_getAllWindows_list = ["Weixin", "微信谁可以看"]
        for title in title_by_getAllWindows_list:
            iRet, wechat_fw_x, wechat_fw_y, wechat_fw_width, wechat_fw_height, hwnd = find_windows_frame_info_by_title(title, False, True, False)
            
            if hwnd == -1:
                continue
            # 保证进程id一样
            child_thread, child_pid = win32process.GetWindowThreadProcessId(hwnd)
            if child_pid != pid:
                continue
            b_is_enable = win32gui.IsWindowEnabled(hwnd)
            if b_is_enable == False:
                continue

            """            
            if iRet == APP_RET_CODE_SUCESS:
                # chenyj test
                print(f"===^-^====[{title}]窗口准备嵌入: 【({wechat_fw_x}, {wechat_fw_y}, {wechat_fw_width}, {wechat_fw_height})】")
                callback(hwnd, True)
                pass
            """
            if iRet in [APP_RET_CODE_SUCESS, APP_RET_CODE_WECHAT_NO_IN_OUT, APP_RET_CODE_WECHAT_NO_IN_CENTER] and hwnd != -1:
                if "朋友圈" in [hwd_wechat_child_info["title"] for hwd_wechat_child_info in self.hwd_wechat_child_list] \
                or "添加朋友" in [hwd_wechat_child_info["title"] for hwd_wechat_child_info in self.hwd_wechat_child_list] \
                or "申请添加朋友" in [hwd_wechat_child_info["title"] for hwd_wechat_child_info in self.hwd_wechat_child_list]:
                    # 1.将窗体移动到当前显示器正中央
                    #iRet = move_window_to_center(hwnd)
                    #if iRet != APP_RET_CODE_SUCESS:
                    #    print(f"!!!将[{title}]移动到当前显示器正中央失败")
                    # 2. 置顶
                    iRet = set_windows_top(hwnd)
                    if iRet != APP_RET_CODE_SUCESS:
                        print(f"!!!将[{title}]置顶失败")
                    # 3.将窗体移到嵌入主窗体内
                    #
                    wechat_info = get_wechat_info()
                    #
                    container_hwnd = int(self.wechat_container.winId())
                    rect = win32gui.GetClientRect(container_hwnd)
                    width = rect[2] - rect[0]
                    height = rect[3] - rect[1]
                    #
                    win32gui.SetWindowPos(
                        hwnd, win32con.HWND_TOP,
                        wechat_info.rect.left, wechat_info.rect.top, width, height,
                        win32con.SWP_SHOWWINDOW
                    )
                    print(f"将弹出窗体[{title}]{hwnd}移动到主窗体中的【{wechat_info.rect.left}， {wechat_info.rect.top}， {width}， {height}】")

                # chenyj test
                """
                if "朋友圈" in [hwd_wechat_child_info["title"] for hwd_wechat_child_info in self.hwd_wechat_child_list]:
                    print(f"===^-^====[{title}]窗口准备嵌入")
                    callback(hwnd, True)
                """

    def restore_WeChat(self):
        """将微信窗口从嵌入状态还原为独立窗口"""
        if not self.wechat_application_window:
            print("当前没有已嵌入的微信窗口")
            return
            
        # 打印当前线程ID
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        print(f"当前线程ID: {thread_id}")
        
        hwnd_wechat = int(self.wechat_application_window.winId())
        print(f"准备还原微信窗口, hwnd = {hwnd_wechat}")
        if self.wechat_container:
            self.layoutWeChat.removeWidget(self.wechat_container)
            self.wechat_container.setParent(None)
            self.wechat_container.deleteLater()
            self.wechat_container = None
            print("微信窗口容器已移除。")
        desktop_hwnd = GetDesktopWindow()
        # 微信主窗口
        SetParent(hwnd_wechat, desktop_hwnd)
        style = GetWindowLong(hwnd_wechat, GWL_STYLE)
        style = (style & ~WS_CHILD) | WS_OVERLAPPEDWINDOW
        SetWindowLong(hwnd_wechat, GWL_STYLE, style)
        ShowWindow(hwnd_wechat, SW_RESTORE)
        # 最大化
        ShowWindow(hwnd_wechat, 3)
        BringWindowToTop(hwnd_wechat)
        SetForegroundWindow(hwnd_wechat)
        print(f"微信主窗口[{hwnd_wechat}]还原到桌面")

        # 微信子窗口
        if len(self.hwd_wechat_child_list) > 0:
            for hwd_wechat_child_info in self.hwd_wechat_child_list:
                hwd_wechat_child = hwd_wechat_child_info["hwnd"]
                SetParent(hwd_wechat_child, desktop_hwnd)
                style = GetWindowLong(hwd_wechat_child, GWL_STYLE)
                style = (style & ~WS_CHILD) | WS_OVERLAPPEDWINDOW
                SetWindowLong(hwd_wechat_child, GWL_STYLE, style)
                ShowWindow(hwd_wechat_child, SW_RESTORE)
                BringWindowToTop(hwd_wechat_child)
                SetForegroundWindow(hwd_wechat_child)
                print(f"微信子窗口[{hwd_wechat_child}]还原到桌面")
            
        if self.labelWeChat:
            self.labelWeChat.show()
        print("微信窗口已从嵌入状态还原为独立窗口。")

    def append_log(self, text, color):
        if text == self.last_text_of_logTextEdit:
            return 
            
        self.save_color = self.logTextEdit.textColor()
        self.logTextEdit.setTextColor(QColor(color))
        self.logTextEdit.append(text)
        self.logTextEdit.setTextColor(self.save_color)  
        self.last_text_of_logTextEdit = text
        return
    def write_log_to_windows(self, message):  
        # 追加日志消息前检查长度限制
        #if self.logTextEdit.document().blockCount() >= 2:
        #	self.logTextEdit.clear()  
        """
        if "!!" in message:
            self.append_log(message, "black") 
        """
        #"""
        if "!!" in message:
            self.append_log(message, "red")
        else:
            self.append_log(message, "black")
        #"""
        # 自动滚动到文本框的底部
        if g_b_Debug == False:
            self.logTextEdit.moveCursor(QTextCursor.End)
            self.logTextEdit.ensureCursorVisible()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 300)

        # 开始按钮
        self.start_btn = QPushButton('开始', self)
        self.start_btn.clicked.connect(self.switch_to_side)

        #self.setCentralWidget(self.start_btn)

    def switch_to_side(self):
        self.hide()              # 主窗口消失
        self.side = RightPanelWindow(self)
        self.side.show()         # 显示右侧窄窗


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())