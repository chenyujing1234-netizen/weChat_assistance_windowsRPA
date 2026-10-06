from memory_profiler_helper import DEBUG_CURREN_MEM
DEBUG_CURREN_MEM("windows_helper.py 000")
import pyautogui
pyautogui.FAILSAFE = False
#from pyautogui import getAllWindows, screenshot
DEBUG_CURREN_MEM("windows_helper.py 111")
from app_info import * 
DEBUG_CURREN_MEM("windows_helper.py 222")
from log_helper import print_my
DEBUG_CURREN_MEM("windows_helper.py 333")
from error_code import *
DEBUG_CURREN_MEM("windows_helper.py 4444")
from pynput import keyboard
from pynput import mouse
import pyperclip

LEI_DIAN_TITLE_BEGIN = "雷电模拟器"

g_lei_dian_fw = None
g_lei_dian_fw_left = -1
g_lei_dian_fw_right = -1
g_lei_dian_fw_top = -1
g_lei_dian_fw_bottom = -1
g_lei_dian_fw_width = -1
g_lei_dian_fw_height = -1

# 找到雷电窗口
def windows_find_lei_dian_window(b_input_windows_visible = True):
    global  g_lei_dian_fw
    global g_lei_dian_fw_left
    global g_lei_dian_fw_right
    global g_lei_dian_fw_top
    global g_lei_dian_fw_bottom
    global g_lei_dian_fw_width
    global g_lei_dian_fw_height
    
    g_lei_dian_fw = None
    g_lei_dian_fw_left = -1
    g_lei_dian_fw_right = -1
    g_lei_dian_fw_top = -1
    g_lei_dian_fw_bottom = -1
    g_lei_dian_fw_width = -1
    g_lei_dian_fw_height = -1
    bRet = False
    fw_all = pyautogui.getAllWindows() # 返回屏幕上每个可见窗口的窗口对象列表。
 
    for fw in fw_all:
        #if True == fw.title.startswith(LEI_DIAN_TITLE_BEGIN):
        if fw.title == LEI_DIAN_TITLE_BEGIN:

            if b_input_windows_visible == True and fw.left < -10 and fw.top < -20:
                continue
             
            g_lei_dian_fw = fw
            g_lei_dian_fw_left = fw.left
            g_lei_dian_fw_right = fw.right
            g_lei_dian_fw_top = fw.top
            g_lei_dian_fw_bottom = fw.bottom
            g_lei_dian_fw_width = fw.right - fw.left
            g_lei_dian_fw_height = fw.bottom - fw.top
            # chenyj debug
            #print("雷电窗口对象:{}".format(g_lei_dian_fw))
            #print_my("找到了托管容器的窗口:[{}, {}, {}, {}], w:{} h:{}".format(g_lei_dian_fw_left, g_lei_dian_fw_top, g_lei_dian_fw_right, g_lei_dian_fw_bottom, g_lei_dian_fw_width, g_lei_dian_fw_height))
        
            # 保存截图
            if b_input_windows_visible == True:
                img_windows_path = SCREENSHOT_SAVE_DIR + "/" + "lei_dian_windows.png"
                #print("===>windows_find_lei_dian_window, screenshot")
                #pyautogui.screenshot(img_windows_path, region=(g_lei_dian_fw_left, g_lei_dian_fw_top, g_lei_dian_fw_width, g_lei_dian_fw_height))
                #print("<===windows_find_lei_dian_window, screenshot")
                
                print('雷电截图保存到:{}'.format(img_windows_path))
            bRet = True
            break 

    return bRet
#windows_find_lei_dian_window(True)

# 最小化雷电窗口
def windows_minimize_lei_dian():
    if False == windows_find_lei_dian_window(True):
        # chenyj debug
        #print("没有可见的托管容器窗口,无法最小化")
        return APP_RET_CODE_NO_FOUND
    
    #print_my("动作:【将托管容器最小化】")    
    g_lei_dian_fw.minimize()    
    
    return APP_RET_CODE_SUCESS
#windows_minimize_lei_dian()

# 还原雷电窗口
def windows_restore_lei_dian():
    if False == windows_find_lei_dian_window(False):
        # chenyj debug
        print_my("没有找到托管容窗口")
        return APP_RET_CODE_NO_FOUND
    # chenyj debug
    print("动作:【将托管容器还原】")    
    g_lei_dian_fw.restore()    
    
    return APP_RET_CODE_SUCESS
#windows_restore_lei_dian()

######################################## 分辨率 #############################################
import win32api
import win32con
import pywintypes
import time

def enum_resolutions():
    """返回显示器支持的所有模式，列表元素为 (宽, 高, 色深, 刷新率)"""
    i = 0
    modes = []
    while True:
        try:
            dm = win32api.EnumDisplaySettings(None, i)
            modes.append((dm.PelsWidth, dm.PelsHeight,
                          dm.BitsPerPel, dm.DisplayFrequency))
            i += 1
        except pywintypes.error:
            break
    # 去重并保持顺序
    seen = set()
    return [x for x in modes if not (x in seen or seen.add(x))]

def get_current_resolution():
    dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    return dm.PelsWidth, dm.PelsHeight, dm.BitsPerPel, dm.DisplayFrequency

def set_resolution(width, height, depth=32, freq=60, temporary=True):
    """
    切换分辨率。temporary=True 表示重启后失效（安全）。
    返回 True/False 表示是否成功。
    """
    dm = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
    # 修改字段
    dm.PelsWidth = width
    dm.PelsHeight = height
    dm.BitsPerPel = depth
    dm.DisplayFrequency = freq
    dm.Fields = (win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT |
                 win32con.DM_BITSPERPEL | win32con.DM_DISPLAYFREQUENCY)

    flags = win32con.CDS_UPDATEREGISTRY
    if temporary:
        flags = win32con.CDS_TEST | win32con.CDS_FULLSCREEN  # 不写入注册表
    try:
        win32api.ChangeDisplaySettings(dm, flags)
        if temporary:
            # 真正应用
            win32api.ChangeDisplaySettings(dm, win32con.CDS_UPDATEREGISTRY)
        return True
    except pywintypes.error as e:
        print("切换失败:", e)
        return False

if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
    NEDD_WELS_WIDTH = 1920
    NEED_WELS_HEIGHT = 1080
elif g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows_1366_768:
    NEDD_WELS_WIDTH = 1366
    NEED_WELS_HEIGHT = 768
    
# 判断当前分辨率是否满足要求
def is_resolution_satify():
    modes = enum_resolutions()
    for idx, mode in enumerate(modes):
        print(idx, mode)
        if mode[0] == NEDD_WELS_WIDTH and mode[1] == NEED_WELS_HEIGHT:
            return APP_RET_CODE_SUCESS
    # chenyj debug
    for idx, mode in enumerate(modes):
        print(idx, mode)
    return APP_RET_CODE_UNKNOW

# 判断当前分辨率是否正确
def is_resolution_right():
    PelsWidth, PelsHeight, BitsPerPel, DisplayFrequency = get_current_resolution()
    if PelsWidth == NEDD_WELS_WIDTH and PelsHeight == NEED_WELS_HEIGHT:
        return APP_RET_CODE_SUCESS
    return APP_RET_CODE_UNKNOW

g_PelsWidth_befor_set = 0
g_PelsHeight_befor_set = 0
def set_resolution_to_1920x1080():
    PelsWidth, PelsHeight, BitsPerPel, DisplayFrequency = get_current_resolution()
    g_PelsWidth_befor_set = PelsWidth
    g_PelsHeight_befor_set = PelsHeight
    if PelsWidth == NEDD_WELS_WIDTH and PelsHeight == NEED_WELS_HEIGHT:
        print("当前分辨率已经是1920x1080, 无需切换")
        return APP_RET_CODE_UNKNOW
    ok = set_resolution(1920, 1080, 32, 60, temporary=False)
    if ok:
        return APP_RET_CODE_SUCESS
    else:
        return APP_RET_CODE_UNKNOW

# 还原分辨率
def reset_resolution():
    if g_PelsWidth_befor_set == 0 and g_PelsHeight_befor_set == 0:
        return APP_RET_CODE_UNKNOW
    ok = set_resolution(g_PelsWidth_befor_set, g_PelsHeight_befor_set, 32, 60, temporary=False)
    if ok:
        return APP_RET_CODE_SUCESS
    else:
        return APP_RET_CODE_UNKNOW
 
"""
if __name__ == "__main__":
    print("当前分辨率:", get_current_resolution())
    print("支持的分辨率:")
    for idx, mode in enumerate(enum_resolutions()):
        print(idx, mode)

    # 示例：改成 1920×1080，32 位色，60 Hz
    ok = set_resolution(1920, 1080, 32, 60, temporary=False)
    if ok:
        print("已切换，3 秒后恢复演示...")
        time.sleep(3)
        # 演示完再恢复原来的
        w, h, d, f = get_current_resolution()
        set_resolution(w, h, d, f, temporary=False)
"""

######################################## 禁用键鼠 #############################################
import ctypes
from ctypes import wintypes
import atexit
import time
import threading

# Load DLLs
user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

# Set restype and argtypes for functions
kernel32.GetLastError.restype = wintypes.DWORD

user32.SetWindowsHookExW.restype = wintypes.HHOOK
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, ctypes.c_void_p, wintypes.HINSTANCE, wintypes.DWORD]

user32.UnhookWindowsHookEx.restype = wintypes.BOOL
user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]

user32.CallNextHookEx.restype = wintypes.LPARAM
user32.CallNextHookEx.argtypes = [wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]

user32.GetMessageW.restype = wintypes.BOOL
user32.TranslateMessage.restype = wintypes.BOOL
user32.DispatchMessageW.restype = wintypes.LPARAM

user32.PostThreadMessageW.restype = wintypes.BOOL
user32.PostThreadMessageW.argtypes = [wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]

kernel32.GetCurrentThreadId.restype = wintypes.DWORD
kernel32.GetCurrentThreadId.argtypes = []

# Constants
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104
VK_ESCAPE = 0x1B
VK_1 = 0x31
LLKHF_INJECTED = 0x00000010
LLMHF_INJECTED = 0x00000001
WM_QUIT = 0x0012

# Structures
class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

class MSG(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND),
                ("message", wintypes.UINT),
                ("wParam", wintypes.WPARAM),
                ("lParam", wintypes.LPARAM),
                ("time", wintypes.DWORD),
                ("pt", POINT)]

LPMSG = ctypes.POINTER(MSG)

user32.GetMessageW.argtypes = [LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.TranslateMessage.argtypes = [LPMSG]
user32.DispatchMessageW.argtypes = [LPMSG]

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vkCode", wintypes.DWORD),
                ("scanCode", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_ulonglong)]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("pt", POINT),
                ("mouseData", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_ulonglong)]

# Callback types
LowLevelKeyboardProc = ctypes.WINFUNCTYPE(wintypes.LPARAM, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
LowLevelMouseProc = ctypes.WINFUNCTYPE(wintypes.LPARAM, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

hook_kb = 0
hook_mouse = 0
unhooked = False
ptr_kb = None
ptr_mouse = None

def low_level_keyboard_proc(nCode, wParam, lParam):
    global unhooked
    if unhooked:
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    if nCode < 0:
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
    if kbd.flags & LLKHF_INJECTED:
        if kbd.vkCode == VK_ESCAPE:
            print("模拟Esc键被按下, unhooking...")
            unhook()
            unhooked = True
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    # Physical input
    if (wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN) and kbd.vkCode == VK_ESCAPE:
        print("物理Esc键被按下, unhooking...")
        unhook()
        unhooked = True
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    return 1  # Block physical event

def low_level_mouse_proc(nCode, wParam, lParam):
    global unhooked
    if unhooked:
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    if nCode < 0:
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
    if ms.flags & LLMHF_INJECTED:
        return user32.CallNextHookEx(None, nCode, wParam, lParam)
    return 1  # Block physical event

def hook():
    global hook_kb, hook_mouse, ptr_kb, ptr_mouse
    ptr_kb = LowLevelKeyboardProc(low_level_keyboard_proc)
    ptr_mouse = LowLevelMouseProc(low_level_mouse_proc)
    # For low-level hooks, hmod should be None (NULL)
    hook_kb = user32.SetWindowsHookExW(WH_KEYBOARD_LL, ptr_kb, None, 0)
    if not hook_kb:
        err = kernel32.GetLastError()
        raise RuntimeError(f"Failed to set keyboard hook, error {err}")
    hook_mouse = user32.SetWindowsHookExW(WH_MOUSE_LL, ptr_mouse, None, 0)
    if not hook_mouse:
        err = kernel32.GetLastError()
        raise RuntimeError(f"Failed to set mouse hook, error {err}")

def unhook():
    global hook_kb, hook_mouse
    if hook_kb:
        user32.UnhookWindowsHookEx(hook_kb)
        hook_kb = 0
    if hook_mouse:
        user32.UnhookWindowsHookEx(hook_mouse)
        hook_mouse = 0
    # Post WM_QUIT to break the message loop
    tid = kernel32.GetCurrentThreadId()
    user32.PostThreadMessageW(tid, WM_QUIT, 0, 0)

@atexit.register
def cleanup():
    unhook()

def message_loop():
    global unhooked

    msg = MSG()
    pmsg = ctypes.byref(msg)
    while not unhooked:
        print(f"GetMessageW, 11111")
        ret = user32.GetMessageW(pmsg, None, 0, 0)
        print(f"GetMessageW, 22222, ret:{ret}")
        if ret == 0 or ret == -1:
            break
        user32.TranslateMessage(pmsg)
        print(f"GetMessageW, 33333")
        user32.DispatchMessageW(pmsg)
        print(f"GetMessageW, 44444")


def block_inputs(func_when_stop):
    hook()
    message_loop()
    # 调用回答函数
    if func_when_stop is not None:
        print(f"block_inputs, 调用回调函数, func_when_stop:{func_when_stop}")
        func_when_stop()

def start_block_inputs(func_when_stop = None):
    global unhooked
    if unhooked:
        unhooked = False
    threading.Thread(target=block_inputs, daemon=True, args=(func_when_stop,)).start()

def stop_block_inputs():
    # 发送 ESC 键
    pyautogui.press('esc')

# Example usage
if __name__ == "__main__":
    import pyautogui  # Make sure to install pyautogui: pip install pyautogui
    
    # Start the blocking in a separate thread
    start_block_inputs(lambda: print("Blocked inputs stopped"))
    
    # Wait a bit for hooks to set up
    time.sleep(1)
    
    # Your code here, pyautogui inputs will work because they are injected
    # Example: Send a key press via pyautogui (will work)
    pyautogui.press('a')
    
    # Physical inputs are blocked until Esc is pressed
    
    # Keep the main thread running (e.g., your main program logic here)
    while not unhooked:
        pyautogui.moveTo(614, 833, duration=0.1)
        pyautogui.click()
        time.sleep(1)
        pyperclip.copy("123232323")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.moveTo(1816, 972, duration=0.1)
        pyautogui.click()

        time.sleep(1)