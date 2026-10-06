#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证在中文路径下dialog_me.py的修复效果
"""

import sys
import os
import tempfile
import shutil
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

# 添加当前目录到路径，以便导入dialog_me模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chinese_path():
    """测试在中文路径下创建MeWindow"""
    print("开始测试中文路径下MeWindow的创建...")
    
    # 设置环境变量
    os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu'
    
    # 创建应用
    app = QApplication(sys.argv)
    
    try:
        # 导入dialog_me模块
        from dialog_me import MeWindow
        
        # 创建模拟配置
        mock_config = {
            "BIND_PHONE": "15280006511",
            "USERNAME": "测试用户"
        }
        
        # 创建MeWindow
        print("正在创建MeWindow...")
        window = MeWindow(mock_config)
        print("MeWindow创建成功！")
        
        # 显示窗口
        window.show()
        print("MeWindow显示成功！")
        
        # 显示成功消息
        QMessageBox.information(None, "测试成功", 
                              "MeWindow在中文路径下创建成功！\n"
                              "窗口将显示5秒后自动关闭。")
        
        # 5秒后自动关闭
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(5000, app.quit)
        
        # 运行应用
        return app.exec_()
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 显示错误消息
        QMessageBox.critical(None, "测试失败", 
                           f"MeWindow在中文路径下创建失败！\n"
                           f"错误信息: {str(e)}")
        return 1

def test_with_temp_chinese_dir():
    """在临时中文目录下测试"""
    print("在临时中文目录下测试...")
    
    # 创建临时中文目录
    temp_dir = tempfile.mkdtemp(prefix="测试目录_")
    print(f"创建临时目录: {temp_dir}")
    
    # 保存当前目录
    original_dir = os.getcwd()
    
    try:
        # 切换到中文目录
        os.chdir(temp_dir)
        print(f"切换到中文目录: {os.getcwd()}")
        
        # 在中文目录下创建必要的子目录
        html_dir = os.path.join(temp_dir, "html")
        os.makedirs(html_dir, exist_ok=True)
        
        # 创建一个简单的me.html文件
        me_html_path = os.path.join(html_dir, "me.html")
        with open(me_html_path, 'w', encoding='utf-8') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>账户设置</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .success { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <h1>账户设置</h1>
    <p class="success">成功加载HTML文件！</p>
    <p>当前路径: {current_path}</p>
    <p>测试在中文路径下的WebEngineView功能</p>
</body>
</html>
            """.format(current_path=temp_dir))
        
        print(f"创建测试HTML文件: {me_html_path}")
        
        # 运行测试
        return test_chinese_path()
        
    finally:
        # 恢复原始目录
        os.chdir(original_dir)
        # 删除临时目录
        try:
            shutil.rmtree(temp_dir)
            print(f"删除临时目录: {temp_dir}")
        except Exception as e:
            print(f"删除临时目录失败: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("测试中文路径下MeWindow的创建")
    print("=" * 50)
    
    # 首先在当前目录测试
    print("\n1. 在当前目录测试:")
    result1 = test_chinese_path()
    
    # 然后在临时中文目录测试
    print("\n2. 在临时中文目录测试:")
    result2 = test_with_temp_chinese_dir()
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"当前目录测试: {'成功' if result1 == 0 else '失败'}")
    print(f"中文目录测试: {'成功' if result2 == 0 else '失败'}")
    print("=" * 50)
    
    # 退出
    sys.exit(0 if result1 == 0 and result2 == 0 else 1)