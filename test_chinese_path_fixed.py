#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：验证中文路径下QWebEngineView的问题修复
"""
import sys
import os
import tempfile
import shutil
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QUrl, Qt

def test_chinese_path():
    """测试在中文路径下创建QWebEngineView是否会导致程序退出"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = QWidget()
    layout = QVBoxLayout()
    
    # 显示当前路径信息
    current_path = os.getcwd()
    path_label = QLabel(f"当前路径: {current_path}")
    path_label.setWordWrap(True)
    layout.addWidget(path_label)
    
    # 检查路径是否包含中文
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in current_path)
    chinese_label = QLabel(f"路径包含中文: {'是' if has_chinese else '否'}")
    layout.addWidget(chinese_label)
    
    # 测试按钮
    test_button = QPushButton("测试QWebEngineView")
    result_label = QLabel("测试结果: 未开始")
    result_label.setWordWrap(True)
    layout.addWidget(test_button)
    layout.addWidget(result_label)
    
    def test_webengine():
        try:
            from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
            
            # 创建自定义WebEnginePage
            class CustomWebEnginePage(QWebEnginePage):
                def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
                    print(f"[JS控制台] {level}: {message} (行号: {lineNumber}, 源: {sourceID})")
            
            # 创建WebEngineView和自定义页面
            web_view = QWebEngineView()
            custom_page = CustomWebEnginePage()
            web_view.setPage(custom_page)
            
            # 加载一个简单的HTML页面
            web_view.setHtml("""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>测试页面</title>
            </head>
            <body>
                <h1>QWebEngineView测试成功!</h1>
                <p>如果你能看到这个页面，说明QWebEngineView在中文路径下工作正常。</p>
            </body>
            </html>
            """)
            
            result_label.setText("测试结果: 成功! QWebEngineView在中文路径下工作正常。")
            
            # 显示WebEngineView
            web_view.show()
            
        except Exception as e:
            result_label.setText(f"测试结果: 失败! 错误信息: {str(e)}")
            print(f"测试QWebEngineView时出错: {e}")
    
    test_button.clicked.connect(test_webengine)
    
    window.setLayout(layout)
    window.setWindowTitle("中文路径测试")
    window.resize(400, 300)
    window.show()
    
    sys.exit(app.exec_())

def test_with_chinese_directory():
    """在临时创建的中文目录中测试"""
    # 创建临时中文目录
    temp_dir = tempfile.mkdtemp(prefix="测试目录_")
    print(f"创建临时中文目录: {temp_dir}")
    
    # 切换到中文目录
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    
    try:
        # 在中文目录中运行测试
        test_chinese_path()
    finally:
        # 清理临时目录
        os.chdir(original_dir)
        try:
            shutil.rmtree(temp_dir)
            print(f"已删除临时目录: {temp_dir}")
        except Exception as e:
            print(f"删除临时目录失败: {e}")

if __name__ == "__main__":
    print("开始测试QWebEngineView在中文路径下的表现...")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查当前路径是否包含中文
    current_path = os.getcwd()
    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in current_path)
    
    if has_chinese:
        print("当前路径已包含中文，直接进行测试...")
        test_chinese_path()
    else:
        print("当前路径不包含中文，创建临时中文目录进行测试...")
        test_with_chinese_directory()