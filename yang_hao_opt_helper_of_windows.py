# coding: utf-8
from __future__ import annotations
from log_helper import print_my
from pywinauto import Application
import pyautogui
import time
import pyperclip
import win32gui
import win32con
import win32com.client
import pyautogui
pyautogui.FAILSAFE = False
from app_info import G_X_PIAN_YI, G_Y_PIAN_YI, PageType, APP_IMG_DIR
from error_code import *
import ctypes
from ctypes import wintypes
import os
import winreg
import psutil   # 需先安装：pip install psutil
import subprocess
import win32process 
import win32api
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 缺失的 Toolbar 消息常量
TB_BUTTONCOUNT      = 0x0418
TB_GETBUTTONTEXTW   = 0x040B

# RECT 结构体
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]

class WECHAT_INFO(ctypes.Structure):
    _fields_ = [("rect", RECT),
                ("hwd", wintypes.LONG)]
    
g_rightPanelWin = None
g_rightPanelWin_hwnd = 0  # 在GUI线程缓存的面板句柄，工作线程禁止调用winId()（线程不安全）
g_wechat_info = WECHAT_INFO()
# 初始化
g_wechat_info.rect.left = -1
g_wechat_info.rect.top = -1
g_wechat_info.rect.right = -1
g_wechat_info.rect.bottom = -1
g_wechat_info.hwd = -1
# 设置rightPanelWin对象
def set_rightPanelWin(rightPanelWin):
    global g_rightPanelWin
    global g_rightPanelWin_hwnd
    g_rightPanelWin = rightPanelWin
    # 此函数只在GUI线程调用，此处获取winId()安全（必要时会同步创建native window）
    if rightPanelWin is not None:
        try:
            g_rightPanelWin_hwnd = int(rightPanelWin.winId())
        except Exception as e:
            print(f"!!!!set_rightPanelWin获取面板句柄失败:{e}")
            g_rightPanelWin_hwnd = 0
    else:
        g_rightPanelWin_hwnd = 0
    
# 检测窗口是否被其它窗口遮挡（至少一个像素可见即返回 False）
def is_window_covered(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return True

    # 获取窗口矩形
    rect = RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        return True

    # 取窗口中心点
    x = (rect.left + rect.right) // 2
    y = (rect.top + rect.bottom) // 2

    # WindowFromPoint 返回最上层的窗口句柄
    hwnd_at_pos = user32.WindowFromPoint(wintypes.POINT(x, y))
    if hwnd_at_pos:
        # 如果返回的句柄不是微信窗口，也可能属于微信的子窗口
        # 因此向上遍历父窗口直到找到顶层窗口
        root = hwnd_at_pos
        while user32.GetParent(root):
            root = user32.GetParent(root)
        return root != hwnd
    return True
# ------------------------------------------------
# 判断窗口是否在最前端显示
def is_windows_foreground(hwnd_wechat):
    #hwnd_fore = win32gui.GetForegroundWindow()
    #if hwnd_fore != hwnd_wechat:
    #    print("微信不是当前前景窗口")
    #    return False

    # 检查是否被最小化
    if win32gui.IsIconic(hwnd_wechat):
        #print("is_windows_foreground， !!!窗体处于最小化")
        return False

    # 检查窗口可见性
    if not win32gui.IsWindowVisible(hwnd_wechat):
        #print("is_windows_foreground， !!!窗体窗口不可见")
        return False

    # 可选：进一步检查是否有遮挡
    if is_window_covered(hwnd_wechat):
        #print("is_windows_foreground， !!!窗体窗口被其他窗口遮挡\n")
        return False

    #print("is_windows_foreground， 窗体处于最前端且未被遮挡")
    return True
    
def is_window_centered(hwnd, tolerance: int = 40) -> bool:
    """
    判断窗口 hwnd 是否在当前显示器工作区正中央。
    tolerance：允许的中心偏移像素。
    注意：微信窗口会自行微调位置（如自动贴顶），±1像素的容差会导致
    误判"未居中"进而触发反复重启微信的死循环，故放宽到±40像素。
    """
    if not win32gui.IsWindowVisible(hwnd):
        return False

    # 1. 窗口当前矩形
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    ww = right - left
    wh = bottom - top

    # 2. 窗口所在显示器工作区
    monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    mon_info = win32api.GetMonitorInfo(monitor)
    work = mon_info['Work']          # (left, top, right, bottom)
    sw = work[2] - work[0]
    sh = work[3] - work[1]

    # 3. 期望的左上角坐标
    expect_left = work[0] + (sw - ww) // 2
    expect_top  = work[1] + (sh - wh) // 2

    # 4. 判断是否重合（带容错）
    return abs(left - expect_left) <= tolerance and abs(top - expect_top) <= tolerance

# 通过窗口标题查找窗口位置
def find_windows_frame_info_by_title(title = "微信", b_found_by_child = True, need_out = False, b_debug = True):
    global g_rightPanelWin
    
    iRet = APP_RET_CODE_UNKNOW
    wechat_fw_x = -1
    wechat_fw_y = -1
    wechat_fw_width = -1
    wechat_fw_height = -1
    wechat_hwd = -1
    
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        # chenyj debug
        """
        #print(f"遍历窗口 信息:{fw}") 
        child_thread, child_pid = win32process.GetWindowThreadProcessId(fw._hWnd)
        left, top, right, bottom = win32gui.GetWindowRect(fw._hWnd)
        parent_hwnd = win32gui.GetParent(fw._hWnd)
        b_is_enable = win32gui.IsWindowEnabled(fw._hWnd)
        print(f"  【{fw.title}】, 窗口句柄:{fw._hWnd}, 是否可操作:{b_is_enable}, 位置:{left, top, right, bottom}, tid:{child_thread},pid:{child_pid} 父句柄:{parent_hwnd}")
        """
        #if True == fw.title.startswith(title):
        if fw.title == title:
            # chenyj debug
            #"""
            child_thread, child_pid = win32process.GetWindowThreadProcessId(fw._hWnd)
            left, top, right, bottom = win32gui.GetWindowRect(fw._hWnd)
            parent_hwnd = win32gui.GetParent(fw._hWnd)
            b_is_enable = win32gui.IsWindowEnabled(fw._hWnd)
            print(f"  找到窗口【{fw.title}】, 窗口句柄:{fw._hWnd}, 是否可操作:{b_is_enable}, 位置:{left, top, right, bottom}, tid:{child_thread},pid:{child_pid} 父句柄:{parent_hwnd}")
            # 只找可操作的页面
            if b_is_enable == False:
                continue 

            #"""
            #print(f"find_windows_frame_info_by_title， 可能是{title}的窗口:{fw}")
            if False == is_windows_foreground(fw._hWnd):
                print(f"!!!find_windows_frame_info_by_title，{title}窗口存在，但没在上层显示")
                wechat_hwd = fw._hWnd
                iRet = APP_RET_CODE_WECHAT_NO_VISIBLE 
                continue
            if fw.left < -10 or fw.top < -20:
                print(f"!!!find_windows_frame_info_by_title，{title}窗口存在，但位置不在屏幕内")
                wechat_hwd = fw._hWnd
                iRet = APP_RET_CODE_WECHAT_NO_IN_SCREEN
                continue 
            #"""
            if need_out == False and False == is_window_centered(fw._hWnd):
                print(f"!!!find_windows_frame_info_by_title，[{title}]窗口存在，但位置不在屏幕中央")
                wechat_hwd = fw._hWnd
                iRet = APP_RET_CODE_WECHAT_NO_IN_CENTER
                continue 
            #"""
            if need_out == True and g_wechat_info.rect.left != -1 and g_wechat_info.rect.top != -1:
                rect = RECT()
                if not user32.GetWindowRect(fw._hWnd, ctypes.byref(rect)):
                    print(f"!!!find_we_chat_frame_info 2，[{title}]窗口获取坐标失败")
                    continue
                if (rect.left > g_wechat_info.rect.left and rect.left  < g_wechat_info.rect.right ) and \
                    (rect.top > g_wechat_info.rect.top and rect.top < g_wechat_info.rect.bottom):
                    print(f"!!!find_we_chat_frame_info 2，[{title}]窗口存在，但它没在微信主窗体以外")
                    wechat_hwd = fw._hWnd
                    iRet = APP_RET_CODE_WECHAT_NO_IN_OUT
                    continue

            """
            # 判断是否是部分显示
            rect = RECT()
            if not user32.GetWindowRect(fw._hWnd, ctypes.byref(rect)):
                print(f"!!!find_we_chat_frame_info，微信窗口存在，但被部分挡住")
                iRet = APP_RET_CODE_WECHAT_NO_VISIBLE_PART
                continue
            width_real = rect.right - rect.left
            height_real = rect.bottom - rect.top
            wechat_fw_width_ = fw.right - fw.left
            wechat_fw_height_ = fw.bottom - fw.top
            if width_real != wechat_fw_width_ or height_real != wechat_fw_height_:
                print(f"!!!find_we_chat_frame_info，微信窗口存在，但大小与实际不一致")
                iRet = APP_RET_CODE_WECHAT_NO_VISIBLE_PART
                continue
            """
            wechat_fw_x = fw.left
            wechat_fw_y = fw.top
            wechat_fw_width = fw.right - fw.left
            wechat_fw_height = fw.bottom - fw.top
            wechat_hwd = fw._hWnd
            
            #print(f"   find_we_chat_frame_info确定是微信的窗口:{fw}")
            iRet = APP_RET_CODE_SUCESS
            break 
    if iRet == APP_RET_CODE_UNKNOW and b_found_by_child == True:
        if g_rightPanelWin_hwnd != 0:
            wechat_hwnd = find_child_windows_hwnd(g_rightPanelWin_hwnd, title)
            if wechat_hwnd == None:
                iRet = APP_RET_CODE_UNKNOW
            else:
                left, top, right, bottom = win32gui.GetWindowRect(wechat_hwnd)
                wechat_fw_x = left
                wechat_fw_y = top
                wechat_fw_width = right - left
                wechat_fw_height = bottom - top
                wechat_hwd = wechat_hwnd
                
                iRet = APP_RET_CODE_SUCESS
    if iRet == APP_RET_CODE_UNKNOW and b_debug == True:
        if b_found_by_child == True:
            print(f"!!!!find_windows_frame_info_by_title, 桌面窗体、rightPanelWin子窗口下都无法找到[{title}]窗体")
        else:     
            print(f"!!!!find_windows_frame_info_by_title, 桌面窗体下都无法找到[{title}]窗体")
    return iRet, wechat_fw_x, wechat_fw_y, wechat_fw_width, wechat_fw_height, wechat_hwd
#find_windows_frame_info_by_title("微信谁可以看")

# 查找微信窗口位置
def find_we_chat_frame_info():
    global g_wechat_info

    iRet, wechat_fw_x, wechat_fw_y, wechat_fw_width, wechat_fw_height, wechat_hwd = find_windows_frame_info_by_title("微信")
    if iRet == APP_RET_CODE_SUCESS:
        g_wechat_info.rect.left = wechat_fw_x
        g_wechat_info.rect.top = wechat_fw_y
        g_wechat_info.rect.right = wechat_fw_x + wechat_fw_width
        g_wechat_info.rect.bottom = wechat_fw_y + wechat_fw_height
        g_wechat_info.hwd = wechat_hwd
    return iRet, wechat_fw_x, wechat_fw_y, wechat_fw_width, wechat_fw_height, wechat_hwd
#find_we_chat_frame_info()

def find_child_windows_hwnd(parent_hwnd, title = "微信"):
    """
    在指定父窗口下查找微信的子窗口
    :param parent_hwnd: 父窗口句柄
    :return: 微信窗口句柄 或 None
    """
    result_hwnd = None
    #print(f"find_child_wechat_hwnd, parent_hwnd = {parent_hwnd}")
    def callback(hwnd, extra):
        nonlocal result_hwnd
        title_child = win32gui.GetWindowText(hwnd)
        cls_name = win32gui.GetClassName(hwnd)
        # 有些版本微信窗口类名为 "WeChatMainWndForPC"
        if title == title_child:
            result_hwnd = hwnd
            # chenyj debug
            #print(f"find_child_wechat_hwnd, 找到微信窗体 {result_hwnd}")
            return False  # 停止枚举

    try:
        win32gui.EnumChildWindows(parent_hwnd, callback, None)
    except Exception:
        # 关键：回调返回False提前停止枚举时，EnumChildWindows返回FALSE，
        # pywin32会随之抛异常（last error为残留值，如5或0）——这恰恰说明已找到目标。
        # 另外无子窗口时也会抛error 0。因此这里绝不能丢弃result_hwnd，
        # 否则已嵌入面板的微信会被误判为"未找到"。
        pass
    return result_hwnd

def find_child_wechat_hwnd(parent_hwnd):
    return find_child_windows_hwnd(parent_hwnd, "微信")

# 检查微信是否在最前面
def is_we_chat_top():
    iRet, wechat_fw_x, wechat_fw_y, width, height, _ = find_we_chat_frame_info()
    if iRet == APP_RET_CODE_UNKNOW:
        iRet = APP_RET_CODE_WECHAT_NO_TOP
    if iRet != APP_RET_CODE_SUCESS and g_rightPanelWin_hwnd != 0:
        wechat_hwnd = find_child_wechat_hwnd(g_rightPanelWin_hwnd)
        if wechat_hwnd == None:
            print(f"rightPanelWin子窗口下也是没有找到微信窗体")
            iRet = APP_RET_CODE_WECHAT_NO_TOP
        else:
            iRet = APP_RET_CODE_SUCESS
    return iRet

# 截图
def capture_screenshot(x1, y1, width, height, img_save_path = "now.png"):
    try:
        pyautogui.screenshot(img_save_path, region=(x1, y1, width, height))
        # chenyj debug
        #print(f"capture_screenshot图片保存到{img_save_path}")
    except Exception as e:
        print(f"!!!!capture_screenshot异常:\n{e}")
        return APP_RET_CODE_UNKNOW
    return APP_RET_CODE_SUCESS

# 对整个屏幕截图
def capture_screenshot_of_whole_screen(img_save_path = "now.png"):
    try:
        pyautogui.screenshot(img_save_path)
        # chenyj debug
        print(f"capture_screenshot图片保存到{img_save_path}")
    except Exception as e:
        print(f"!!!!capture_screenshot异常:\n{e}")
        return APP_RET_CODE_UNKNOW
    return APP_RET_CODE_SUCESS

# 使用Windows判断当前页面的类型
def get_page_type_by_windows(input_event, right_panel):
    page_type_return = PageType.Unknow
    iRet = APP_RET_CODE_UNKNOW

    iRet, wechat_fw_x, wechat_fw_y, width, height, _ = find_we_chat_frame_info()
    if iRet != APP_RET_CODE_SUCESS:
        return iRet, page_type_return

    # 1.通过windows原生序列
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        # 只找可操作的页面
        b_is_enable = win32gui.IsWindowEnabled(fw._hWnd)
        if b_is_enable == False:
            continue 
        if False == is_windows_foreground(fw._hWnd):
            continue

        if not ((fw.left > wechat_fw_x and fw.left <  wechat_fw_x+width) and (fw.right > wechat_fw_x and fw.right <  wechat_fw_x+width) \
            and (fw.top > wechat_fw_y and fw.top < wechat_fw_y+height) and (fw.bottom > wechat_fw_y and fw.bottom < wechat_fw_y+height)):
            continue

        if fw.title == "微信谁可以看":
            page_type_return = PageType.Circle_Select_Frient
            iRet = APP_RET_CODE_SUCESS
            break

    if iRet == APP_RET_CODE_SUCESS:
        return iRet, page_type_return
    # 2.通过右边panel
    if right_panel is None:
        return iRet, page_type_return

    for hwd_wechat_child_info in right_panel.hwd_wechat_child_list:
        # 只找可操作的页面
        b_is_enable = win32gui.IsWindowEnabled(hwd_wechat_child_info["hwnd"])
        if b_is_enable == False:
            continue 
        if hwd_wechat_child_info["title"] == "朋友圈":
            page_type_return = PageType.Circle
            iRet = APP_RET_CODE_SUCESS
            break
    return iRet, page_type_return

def windows_get_screen(path):
    iRet = APP_RET_CODE_UNKNOW
    iRet, wechat_fw_x, wechat_fw_y, width, height, _ = find_we_chat_frame_info()
    if iRet == APP_RET_CODE_SUCESS:
        iRet = capture_screenshot(wechat_fw_x, wechat_fw_y, width, height, path)
    else:
        iRet = APP_RET_CODE_UNKNOW
    return iRet

def windows_slide_friendbook_down(input_event):
    global g_wechat_info
    
    if g_wechat_info.rect.left == -1:
        print(f"!!!!微信的主窗体还没有出现")
        return APP_RET_CODE_UNKNOW
    # 通讯录列表向上滚
    pyautogui.moveTo(g_wechat_info.rect.left + 197+G_X_PIAN_YI, g_wechat_info.rect.top + 153+G_Y_PIAN_YI, duration=0.1)
    """
    system_scroll_lines = 3          # 系统默认，可注册表读
    qt_pixels_per_line  = 20         # Qt 默认
    need_pixels = 324
    need_rows   = need_pixels / qt_pixels_per_line
    need_delta  = int(need_rows * 120 / system_scroll_lines)
    pyautogui.scroll(-need_delta)    # 这次就接近 324 px 了
    """
    for i in range(10): 
        pyautogui.scroll(-(324))  
    print("动作:【向下滑动通讯录1屏】")
    if True == input_event.wait(0.1):
        print_my("windows_slide_friendbook_down, 被要求退出")
        return -1 
    return APP_RET_CODE_SUCESS

def windows_slide_friendbook_up(input_event):
    global g_wechat_info
    
    if g_wechat_info.rect.left == -1:
        print(f"!!!!微信的主窗体还没有出现")
        return APP_RET_CODE_UNKNOW
    # 通讯录列表向下滚
    pyautogui.moveTo(g_wechat_info.rect.left + 197+G_X_PIAN_YI, g_wechat_info.rect.top + 153+ 700 + G_Y_PIAN_YI, duration=0.1)
    """
    system_scroll_lines = 3          # 系统默认，可注册表读
    qt_pixels_per_line  = 20         # Qt 默认
    need_pixels = 324
    need_rows   = need_pixels / qt_pixels_per_line
    need_delta  = int(need_rows * 120 / system_scroll_lines)
    pyautogui.scroll(-need_delta)    # 这次就接近 324 px 了
    """
    for i in range(10): 
        pyautogui.scroll(324)  
    print("动作:【向上滑动通讯录1屏】")
    if True == input_event.wait(0.1):
        print_my("windows_slide_friendbook_up, 被要求退出")
        return -1 
    return APP_RET_CODE_SUCESS

# 检查微信是否安装
def is_wechat_installed():
    # 检查注册表1
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat")
        install_path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        if install_path and os.path.isdir(install_path):
            return True
    except Exception as e:
        #print(f"!!!!is_wechat_installed异常:{e}")
        pass
    # 检查注册表2
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\Weixin")
        install_path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        if install_path and os.path.isdir(install_path):
            return True
    except Exception as e:
        print(f"!!!!is_wechat_installed异常:\n{e}")
        pass
    
    # 检查常见安装路径
    common_paths = [
        os.path.expandvars(r"%ProgramFiles%\Tencent\WeChat"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Tencent\WeChat"),
        os.path.expandvars(r"%APPDATA%\Tencent\WeChat"),
        os.path.expandvars(r"%ProgramFiles%\Tencent\Weixin"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Tencent\Weixin"),
        os.path.expandvars(r"%APPDATA%\Tencent\Weixin")
    ]
    for path in common_paths:
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "WeChat.exe")):
            return True 
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "Weixin.exe")):
            return True 
    return False

# 检查微信进程是否正在运行
def is_wechat_process_running():
    for proc in psutil.process_iter(['name']):
        try:
            #print(f"进程名称:{proc.info['name'].lower()}")
            if proc.info['name'].lower() == 'weixin.exe':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# 判断本地的微信应用程序是否在运行并可见
def is_windows_wechat_running_and_top():  
    # 2. 判断微信是否已经运行
    if False == is_wechat_process_running():
        print('!!!!微信未启动')
        return APP_RET_CODE_WECHAT_NO_RUNNING
        
    # 3. 判断应用程序是否在顶层
    iRet = is_we_chat_top()
    if iRet != APP_RET_CODE_SUCESS:
        print("!!!微信窗口不存在、或没有置顶、或没在屏幕内")
        return iRet
    
    return APP_RET_CODE_SUCESS

# 获取微信的安装路径
def get_wechat_path():
    """返回 WeChat.exe 的完整路径；找不到返回 None"""
    # 1. 先查注册表
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\Weixin") as key:
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            exe_path = os.path.join(install_path, "Weixin.exe")
            if os.path.isfile(exe_path):
                return exe_path
    except (FileNotFoundError, OSError):
        pass

    # 2. 查常见默认目录
    candidates = [
        r"%ProgramFiles%\Tencent\Weixin\Weixin.exe",
        r"%ProgramFiles(x86)%\Tencent\Weixin\Weixin.exe",
    ]
    for cand in candidates:
        exe_path = os.path.expandvars(cand)
        if os.path.isfile(exe_path):
            return exe_path

    return None

# 启动微信
def start_wechat():
    """启动微信；成功返回 True，失败返回 False"""
    exe = get_wechat_path()
    if not exe:
        print("未找到 Weixin.exe，请确认已安装微信或手动指定路径")
        return False
    print(f"要启动的微信路径:{exe}")
    try:
        subprocess.Popen([exe])
        print("微信启动成功")
        return True
    except Exception as e:
        print("启动失败：", e)
        return False
    return False

# 需要用到 Win32 API 发送关闭消息
user32 = ctypes.windll.user32
WM_CLOSE = 0x0010
def _send_close_window(pid: int, timeout: float = 3.0) -> bool:
    """
    向指定 PID 所属的主窗口发送 WM_CLOSE，等待其自行退出。
    返回 True 表示进程已消失；False 表示仍在运行。
    """
    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def enum_proc(hwnd, lParam):
        # 只看顶层窗口
        if user32.IsWindowVisible(hwnd) and user32.IsWindow(hwnd):
            _, found_pid = wintypes.DWORD(), wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(found_pid))
            if found_pid.value == pid:
                user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
        return True

    user32.EnumWindows(enum_proc, 0)
    # 等待进程退出
    give_up = time.time() + timeout
    while time.time() < give_up:
        if not psutil.pid_exists(pid):
            return True
        time.sleep(0.2)
    return False


def kill_wechat(graceful_first: bool = False) -> list[int]:
    """
    杀掉所有微信进程（WeChat.exe / Weixin.exe）。
    参数
    ----
    graceful_first : bool
        True  先尝试发送 WM_CLOSE，超时再强制杀；
        False 直接强制杀。
    返回
    ----
    list[int] : 被杀掉的 PID 列表
    """
    killed = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if name in ('wechat.exe', 'weixin.exe'):
                pid = proc.info['pid']
                if graceful_first and _send_close_window(pid):
                    killed.append(pid)
                else:
                    proc.kill()
                    proc.wait(timeout=3)
                    killed.append(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed
"""
pids = kill_wechat(False)
if pids:
    print("已杀掉微信进程：", pids)
else:
    print("微信未运行")
"""


# ---- Win32 常量 / 结构体 ----
VS_FF_INFOINFERRED        = 0x00000010
VS_FF_PATCHED             = 0x00000004
VS_FF_PRERELEASE          = 0x00000002
VS_FF_PRIVATEBUILD        = 0x00000008
VS_FF_SPECIALBUILD        = 0x00000020

class VS_FIXEDFILEINFO(ctypes.Structure):
    _fields_ = [
        ("dwSignature",        wintypes.DWORD),
        ("dwStrucVersion",     wintypes.DWORD),
        ("dwFileVersionMS",    wintypes.DWORD),
        ("dwFileVersionLS",    wintypes.DWORD),
        ("dwProductVersionMS", wintypes.DWORD),
        ("dwProductVersionLS", wintypes.DWORD),
        ("dwFileFlagsMask",    wintypes.DWORD),
        ("dwFileFlags",        wintypes.DWORD),
        ("dwFileOS",           wintypes.DWORD),
        ("dwFileType",         wintypes.DWORD),
        ("dwFileSubtype",      wintypes.DWORD),
        ("dwFileDateMS",       wintypes.DWORD),
        ("dwFileDateLS",       wintypes.DWORD),
    ]

def _get_file_version_number(exe_path: str) -> str | None:
    """
    读取 PE 文件版本号，形如 3.9.11.25；失败返回 None
    """
    kernel32 = ctypes.windll.kernel32
    ver = ctypes.windll.version

    if not os.path.isfile(exe_path):
        return None

    # 1. 获取版本信息大小
    size = ver.GetFileVersionInfoSizeW(exe_path, None)
    if size == 0:
        return None

    # 2. 申请内存并读取
    buf = ctypes.create_string_buffer(size)
    if not ver.GetFileVersionInfoW(exe_path, 0, size, buf):
        return None

    # 3. 查询 VS_FIXEDFILEINFO
    lplpBuffer = ctypes.POINTER(VS_FIXEDFILEINFO)()
    uLen = wintypes.UINT()
    if not ver.VerQueryValueW(buf, r"\\", ctypes.byref(lplpBuffer), ctypes.byref(uLen)):
        return None

    ffi = lplpBuffer.contents
    major = ffi.dwFileVersionMS >> 16
    minor = ffi.dwFileVersionMS & 0xFFFF
    build = ffi.dwFileVersionLS >> 16
    rev   = ffi.dwFileVersionLS & 0xFFFF
    return f"{major}.{minor}.{build}.{rev}"


def get_wechat_version() -> str | None:
    """
    返回当前系统已安装微信的版本号，失败返回 None
    优先级：注册表 DisplayVersion > 文件版本
    """
    # 1. 注册表捷径（官方数字版本）
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\Weixin") as key:
            version, _ = winreg.QueryValueEx(key, "DisplayVersion")
            if isinstance(version, str) and version.strip():
                return version.strip()
    except (FileNotFoundError, OSError):
        pass

    # 2. 拿不到注册表，就读文件版本
    exe_path = get_wechat_path()          # 复用你已有的函数
    if exe_path:
        return _get_file_version_number(exe_path)

    print(f"!!!get_wechat_version，不能获得到微信的版本号，原因:未检测到微信路径[{exe_path}]")
    return None


# ----------------- 测试 -----------------
"""
v = get_wechat_version()
print("微信版本：" + v if v else "未检测到微信")
"""

# 将窗口置顶显示
def set_windows_top(hwnd_wechat):
    try:
        # 设置窗口置顶
        win32gui.SetWindowPos(
            hwnd_wechat,
            win32con.HWND_TOPMOST,  # 置于所有窗口之上
            0, 0, 0, 0,  # 保持原位置和大小
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE  # 不改变位置和大小
        )
        
        return APP_RET_CODE_SUCESS
    except Exception as e:
        print(f"!!!set_windows_top， 设置窗口置顶失败: {e}")
        return APP_RET_CODE_UNKNOW

# 置顶微信窗口
def set_wechat_top():
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        #print(fw)
        #if True == fw.title.startswith("微信"):
        if fw.title == "微信":
            iRet = set_windows_top(fw._hWnd)
            if iRet != APP_RET_CODE_SUCESS:
                return iRet 
            print("置顶微信窗口")
    return iRet  
#set_wechat_top()

# 获得微信窗口的句柄
def get_wechat_window():
    hwd_wechat = None
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        #print(fw)
        #if True == fw.title.startswith("微信"):
        if fw.title == "微信":
            iRet = APP_RET_CODE_SUCESS
            hwd_wechat = fw._hWnd
            break
    return iRet, hwd_wechat
_, hwnd_wechat = get_wechat_window()

# 还原微信窗口
def restore_wechat_normal():
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        #print(fw)
        #if True == fw.title.startswith("微信"):
        if fw.title == "微信":
            print("还原微信窗口")
            fw.restore()
            iRet = APP_RET_CODE_SUCESS  
    return iRet  
#restore_wechat_normal()

def find_window_by_process_name(process_name):
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                if psutil.Process(pid).name().lower() == process_name.lower():
                    windows.append(hwnd)
            except:
                pass
        return True

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def restore_window(process_name):
    iRet = APP_RET_CODE_UNKNOW
    hwnds = find_window_by_process_name(process_name)
    for hwnd in hwnds:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        iRet = APP_RET_CODE_SUCESS
    return iRet

def restore_wechat_normal_by_process():
    iRet = APP_RET_CODE_UNKNOW
    weChatProcessName_list = ["Weixin.exe", "WeChat.exe"]
    for weChatProcessName in weChatProcessName_list:
        iRet = restore_window(weChatProcessName)
        if iRet != APP_RET_CODE_SUCESS:
            print(f"!!!!!restore_wechat_normal_by_process，通过进程名{weChatProcessName}还原微信失败")
        else:
            print(f"restore_wechat_normal_by_process，通过进程名{weChatProcessName}还原微信成功")
            break
    return iRet

# 取消窗口的置顶状态
def set_windows_normal(hwnd_wechat):
    try:
        # 取消窗口置顶
        win32gui.SetWindowPos(
            hwnd_wechat,
            win32con.HWND_NOTOPMOST,  # 恢复正常Z序
            0, 0, 0, 0,  # 保持原位置和大小
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE  # 不改变位置和大小
        )
        
        return APP_RET_CODE_SUCESS
    except Exception as e:
        print(f"取消窗口置顶失败: {e}")
        return APP_RET_CODE_UNKNOW

# 取消微信窗口的置顶状态
def set_wechat_normal():
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        #print(fw)
        #if True == fw.title.startswith("微信"):
        if fw.title == "微信":
            iRet = set_windows_normal(fw._hWnd)
            if iRet != APP_RET_CODE_SUCESS:
                return iRet 
            print("取消微信窗口的置顶状态")
    return iRet  
#set_wechat_normal()

# 获取系统托盘图标
def get_tray_tooltip_texts():
    texts = []
    h_tray  = user32.FindWindowW('Shell_TrayWnd', None)
    h_pager = user32.FindWindowExW(h_tray, 0, 'TrayNotifyWnd', None)
    h_tool  = user32.FindWindowExW(h_pager, 0, 'ToolbarWindow32', None)

    count = user32.SendMessageW(h_tool, TB_BUTTONCOUNT, 0, 0)
    for i in range(count):
        len_ = user32.SendMessageW(h_tool, TB_GETBUTTONTEXTW, i, 0)
        if len_ <= 0:
            continue
        buf = ctypes.create_unicode_buffer(len_ + 1)
        user32.SendMessageW(h_tool, TB_GETBUTTONTEXTW, i, buf)
        texts.append(buf.value)
    return texts

#print(get_tray_tooltip_texts())


def move_window_to_center(hwnd):
    """
    将指定窗口移动到当前显示器正中央。
    """
    # 2. 获取窗口当前大小（不含阴影）
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top

    # 3. 获取窗口当前所在的显示器信息
    monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    mon_info = win32api.GetMonitorInfo(monitor)
    work = mon_info['Work']          # (left, top, right, bottom)
    mw = work[2] - work[0]
    mh = work[1] - work[3] if work[1] > work[3] else work[3] - work[1]

    # 4. 计算居中坐标（基于工作区，避开任务栏）
    new_left = work[0] + (mw - w) // 2
    new_top  = work[1] + (mh - h) // 2

    # 5. 移动窗口（保持大小不变）
    win32gui.SetWindowPos(hwnd,
                          win32con.HWND_TOP,
                          new_left, new_top,
                          0, 0,
                          win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
    return APP_RET_CODE_SUCESS

# 将微信移动到当前显示器正中央
def move_wechat_to_center():
    iRet = APP_RET_CODE_UNKNOW
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
    for fw in fw_all:
        #print(fw)
        #if True == fw.title.startswith("微信"):
        if fw.title == "微信":
            iRet = move_window_to_center(fw._hWnd)
            if iRet != APP_RET_CODE_SUCESS:
                print(f"!!!将微信移动到当前显示器正中央失败")
                return iRet 
            print("将微信移动到当前显示器正中央")
    return iRet  
#move_wechat_to_center()

# 点击
def windows_click(x, y):
    global g_rightPanelWin
    global g_wechat_info
    if g_rightPanelWin is None:
        return APP_RET_CODE_UNKNOW
    print("动作:【点击坐标:({}, {})】".format(x, y))
    x = x + g_wechat_info.rect.left
    y = y + g_wechat_info.rect.top
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()
    
    return APP_RET_CODE_SUCESS

#  粘贴文本
def windows_paste_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
  
def windows_right_click(x, y):
    """在指定坐标(x, y)处执行鼠标右键点击"""
    try:
        x_real = x + g_wechat_info.rect.left
        y_real = y + g_wechat_info.rect.top
        # 移动鼠标到指定坐标
        pyautogui.moveTo(x_real, y_real, duration=0.5)  # duration参数控制移动速度，单位秒
        time.sleep(0.2)  # 短暂停顿，确保鼠标已移动到位
        
        # 执行右键点击
        pyautogui.rightClick()
        print(f"已在坐标({x}, {y})处执行右键点击")
    except Exception as e:
        print(f"windows_right_click, 操作出错: {str(e)}")
        return APP_RET_CODE_UNKNOW
    return APP_RET_CODE_SUCESS

def windows_longpress(x, y):
    DURATION = 1.2   # 按住多久（秒）
    # 把鼠标先移到起点
    x_real = x + g_wechat_info.rect.left
    y_real = y + g_wechat_info.rect.top
    pyautogui.moveTo(x_real, y_real)
    # 按下左键不放
    pyautogui.mouseDown()
    # 匀速往右拖 200 px
    pyautogui.moveRel(10, 5, duration=DURATION)   # 拖动过程就是“长按”
    # 松开
    pyautogui.mouseUp()
    return APP_RET_CODE_SUCESS

def get_wechat_info():
    global g_wechat_info
    return g_wechat_info

def restore_wechat_focus_via_taskbar():
    """
    通过模拟点击任务栏图标来恢复微信焦点。
    作为 back_to_main 函数的一个辅助步骤。
    """
    # 给系统一些时间来完成窗口状态的改变
    #time.sleep(4)
    
    # 指定微信图标的图像文件路径
    # 这里的路径需要根据你的实际文件位置修改
    wechat_icon_path = os.path.join(APP_IMG_DIR, 'wechat_taskbar_icon.png')
    
    if not os.path.exists(wechat_icon_path):
        print(f"错误: 找不到右下角微信toolbar图像文件 {wechat_icon_path}")
        return
    try:    
        icon_location = pyautogui.locateOnScreen(wechat_icon_path, confidence=0.8)
        if icon_location:
            icon_center = pyautogui.center(icon_location)
            print(f"找到微信图标，位置: {icon_center}")
            # 移动鼠标到图标位置
            #pyautogui.moveTo(icon_center)
            # 双击图标
            #pyautogui.doubleClick()
            # time.sleep(1)
            pyautogui.click(icon_center)
            print("已模拟点击任务栏上的微信图标。")
        else:
            print("未在屏幕上找到微信图标，无法模拟点击。")
    except Exception as e:
        print(f"右下角无法找到微信的图标(在没登录成功时是正常的): {str(e)}")
