# coding: utf-8
# 测试微信窗口置顶功能

import time
from yang_hao_opt_helper_of_windows import set_windows_wechat_top, set_windows_wechat_normal

def test_window_top():
    print("测试微信窗口置顶功能")
    
    # 设置微信窗口置顶
    print("\n1. 设置微信窗口置顶")
    result = set_windows_wechat_top()
    print(f"置顶结果: {result}")
    
    # 等待5秒
    print("\n等待5秒...")
    time.sleep(5)
    
    # 取消微信窗口置顶
    print("\n2. 取消微信窗口置顶")
    result = set_windows_wechat_normal()
    print(f"取消置顶结果: {result}")

if __name__ == "__main__":
    test_window_top()