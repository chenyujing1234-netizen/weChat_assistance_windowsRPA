from pynput import keyboard, mouse
import logging
from datetime import datetime
import os

# 配置日志
log_dir = os.path.join(os.path.expanduser("~"), "input_logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"input_log_{datetime.now().strftime('%Y%m%d')}.txt")
print(f"日志文件路径: {log_file}")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_key_press(key):
    """键盘按下事件处理"""
    try:
        # 普通字符按键
        logging.info(f"键盘按下: {key.char}")
    except AttributeError:
        # 特殊按键（如Ctrl、Shift等）
        logging.info(f"键盘按下: {key}")

def on_key_release(key):
    """键盘释放事件处理"""
    # 如果按下Esc键，则停止监听
    if key == keyboard.Key.esc:
        print("已停止监控（用户按下Esc键）")
        return False

def on_mouse_move(x, y):
    """鼠标移动事件处理"""
    logging.info(f"鼠标移动: ({x}, {y})")

def on_mouse_click(x, y, button, pressed):
    """鼠标点击事件处理"""
    action = "按下" if pressed else "释放"
    logging.info(f"鼠标{action}: {button} 在 ({x}, {y})")

def on_mouse_scroll(x, y, dx, dy):
    """鼠标滚轮事件处理"""
    logging.info(f"鼠标滚动: 在 ({x}, {y})，水平滚动: {dx}，垂直滚动: {dy}")

def start_monitoring():
    """开始监控输入设备"""
    print("开始监控键盘和鼠标动作...")
    print("按下Esc键停止监控")
    
    # 启动键盘监听
    keyboard_listener = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release
    )
    
    # 启动鼠标监听
    mouse_listener = mouse.Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click,
        on_scroll=on_mouse_scroll
    )
    
    # 开始监听
    keyboard_listener.start()
    mouse_listener.start()
    
    # 等待监听线程结束
    keyboard_listener.join()
    mouse_listener.stop()

if __name__ == "__main__":
    try:
        start_monitoring()
    except Exception as e:
        print(f"监控过程中发生错误: {e}")
