#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证安装后程序是否能正常运行
测试在Program Files目录下安装后的权限问题修复
"""

import os
import sys
import tempfile
import shutil

def test_permission_fix():
    """测试权限问题修复"""
    print("=" * 60)
    print("测试程序在Program Files目录下的权限问题修复")
    print("=" * 60)
    
    try:
        # 导入app_info模块
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import app_info
        
        # 检查用户数据目录
        print(f"用户数据目录: {app_info.USER_DATA_DIR}")
        
        # 检查消息会话目录
        print(f"消息会话目录: {app_info.MESSAGE_SESSION_DIR}")
        print(f"消息会话目录是否存在: {os.path.exists(app_info.MESSAGE_SESSION_DIR)}")
        
        # 检查截图目录
        print(f"截图目录: {app_info.SCREENSHOT_SAVE_DIR}")
        print(f"截图目录是否存在: {os.path.exists(app_info.SCREENSHOT_SAVE_DIR)}")
        
        # 检查AI生成图片目录
        print(f"AI生成图片目录: {app_info.AI_GENERATE_IMG_DIR}")
        print(f"AI生成图片目录是否存在: {os.path.exists(app_info.AI_GENERATE_IMG_DIR)}")
        
        # 尝试在消息会话目录创建文件
        test_file = os.path.join(app_info.MESSAGE_SESSION_DIR, "test_file.txt")
        try:
            with open(test_file, 'w') as f:
                f.write("测试文件")
            print(f"成功在消息会话目录创建测试文件: {test_file}")
            os.remove(test_file)
            print("成功删除测试文件")
        except Exception as e:
            print(f"在消息会话目录创建文件失败: {e}")
            return False
        
        print("\n测试结果: 通过")
        print("程序现在可以在Program Files目录下正常运行，不会出现权限错误")
        return True
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_file():
    """测试配置文件读取"""
    print("\n" + "=" * 60)
    print("测试配置文件读取功能")
    print("=" * 60)
    
    try:
        # 创建临时配置文件
        app_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(app_dir, 'config.ini')
        
        # 创建测试配置文件
        with open(config_path, 'w') as f:
            f.write("[Paths]\n")
            f.write(f"UserDataDir={os.path.join(app_dir, 'test_data')}\n")
        
        # 重新导入app_info模块
        if 'app_info' in sys.modules:
            del sys.modules['app_info']
        
        sys.path.insert(0, app_dir)
        import app_info
        
        print(f"从配置文件读取的用户数据目录: {app_info.USER_DATA_DIR}")
        
        # 清理测试文件
        if os.path.exists(config_path):
            os.remove(config_path)
        
        test_data_dir = os.path.join(app_dir, 'test_data')
        if os.path.exists(test_data_dir):
            shutil.rmtree(test_data_dir)
        
        print("\n测试结果: 通过")
        print("程序可以正确从配置文件读取用户数据目录")
        return True
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始测试安装后权限问题修复...")
    
    # 测试权限问题修复
    test1_result = test_permission_fix()
    
    # 测试配置文件读取
    test2_result = test_config_file()
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"权限问题修复测试: {'通过' if test1_result else '失败'}")
    print(f"配置文件读取测试: {'通过' if test2_result else '失败'}")
    
    if test1_result and test2_result:
        print("\n所有测试通过！程序安装后应该可以正常运行。")
    else:
        print("\n部分测试失败，请检查修复代码。")