#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import shutil
from app_info import *

def test_real_download_extract():
    """测试真实下载和解压Tesseract-OCR_TuoGuanContainer_v4.zip"""
    
    print("=== 测试真实下载和解压Tesseract-OCR_TuoGuanContainer_v4.zip ===")
    
    # 1. 测试用户数据目录访问权限
    print(f"1. 用户数据目录: {USER_DATA_DIR}")
    if os.path.exists(USER_DATA_DIR):
        print("   ✓ 用户数据目录存在")
        # 检查是否可写
        test_file = os.path.join(USER_DATA_DIR, "test_write_permission.txt")
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write("测试写入权限")
            print("   ✓ 用户数据目录可写")
            os.remove(test_file)
            print("   ✓ 测试文件已删除")
        except Exception as e:
            print(f"   ✗ 用户数据目录不可写: {e}")
            return False
    else:
        print("   ✗ 用户数据目录不存在")
        return False
    
    # 2. 测试真实下载和解压Tesseract-OCR_TuoGuanContainer_v4.zip
    print("\n2. 测试真实下载和解压Tesseract-OCR_TuoGuanContainer_v4.zip")
    try:
        # 下载路径
        download_path = os.path.join(USER_DATA_DIR, UPDATE_DST_FILENAME)
        print(f"   下载路径: {download_path}")
        
        # 模拟下载过程
        print("   开始下载...")
        import requests
        response = requests.get(UPDATE_DOWNLOAD_URL, stream=True)
        if response.status_code == 200:
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("   ✓ 下载完成")
        else:
            print(f"   ✗ 下载失败，状态码: {response.status_code}")
            return False
        
        # 检查文件大小
        file_size = os.path.getsize(download_path)
        print(f"   文件大小: {file_size} 字节")
        
        # 解压
        print("   开始解压...")
        extract_to = USER_DATA_DIR
        import zipfile
        import io
        
        # 使用内存缓冲方式解压，避免编码问题
        zip_buffer = io.BytesIO()
        with open(download_path, 'rb') as f:
            zip_buffer.write(f.read())
        zip_buffer.seek(0)
        
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        print("   ✓ 解压完成")
        
        # 检查解压结果
        tesseract_path = os.path.join(extract_to, "Tesseract-OCR")
        container_path = os.path.join(extract_to, "TuoGuanContainer")
        
        if os.path.exists(tesseract_path) and os.path.exists(container_path):
            print("   ✓ 成功解压Tesseract-OCR和TuoGuanContainer目录")
        else:
            print("   ✗ 解压失败，目录不存在")
            return False
        
        # 清理文件
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(tesseract_path):
            shutil.rmtree(tesseract_path)
        if os.path.exists(container_path):
            shutil.rmtree(container_path)
        
        print("   ✓ 测试文件已清理")
        
    except Exception as e:
        print(f"   ✗ 下载和解压失败: {e}")
        return False
    
    print("\n=== 真实下载和解压测试通过 ===")
    return True

if __name__ == "__main__":
    success = test_real_download_extract()
    if success:
        print("\n✓ 测试结果: 成功")
        sys.exit(0)
    else:
        print("\n✗ 测试结果: 失败")
        sys.exit(1)