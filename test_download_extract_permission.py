#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import shutil
from app_info import *

def test_download_extract_permission():
    """测试下载和解压文件到用户数据目录的权限"""
    
    print("=== 测试下载和解压文件权限 ===")
    
    # 1. 测试用户数据目录访问权限
    print(f"1. 用户数据目录: {USER_DATA_DIR}")
    if os.path.exists(USER_DATA_DIR):
        print("   ✓ 用户数据目录存在")
        # 检查是否可写
        test_file = os.path.join(USER_DATA_DIR, "test_write_permission.txt")
        try:
            with open(test_file, 'w') as f:
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
    
    # 2. 测试在用户数据目录创建临时zip文件
    print("\n2. 测试在用户数据目录创建临时zip文件")
    test_zip_path = os.path.join(USER_DATA_DIR, "test_download.zip")
    try:
        # 创建一个简单的测试zip文件
        import zipfile
        import io
        # 创建一个内存中的zip文件，避免编码问题
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("test.txt", "这是一个测试文件")
        
        # 将内存中的zip文件写入磁盘
        with open(test_zip_path, 'wb') as f:
            f.write(zip_buffer.getvalue())
        print(f"   ✓ 成功创建测试zip文件: {test_zip_path}")
        
        # 检查文件大小
        file_size = os.path.getsize(test_zip_path)
        print(f"   ✓ 文件大小: {file_size} 字节")
    except Exception as e:
        print(f"   ✗ 创建测试zip文件失败: {e}")
        return False
    
    # 3. 测试解压文件到用户数据目录
    print("\n3. 测试解压文件到用户数据目录")
    extract_dir = os.path.join(USER_DATA_DIR, "test_extract")
    try:
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)
        
        with zipfile.ZipFile(test_zip_path, 'r') as zip_ref:
            # 使用cp437编码读取文件名，这是zip文件的标准编码
            for file_info in zip_ref.infolist():
                # 解码文件名
                filename = file_info.filename.encode('cp437').decode('utf-8')
                # 读取文件内容
                content = zip_ref.read(file_info)
                # 写入解压目录
                output_path = os.path.join(extract_dir, filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(content)
        
        extracted_file = os.path.join(extract_dir, "test.txt")
        if os.path.exists(extracted_file):
            print(f"   ✓ 成功解压文件到: {extract_dir}")
            
            # 检查解压后的文件内容
            with open(extracted_file, 'r') as f:
                content = f.read()
                if content == "这是一个测试文件":
                    print("   ✓ 解压后的文件内容正确")
                else:
                    print("   ✗ 解压后的文件内容不正确")
                    return False
        else:
            print("   ✗ 解压失败，文件不存在")
            return False
    except Exception as e:
        print(f"   ✗ 解压文件失败: {e}")
        return False
    finally:
        # 清理测试文件
        try:
            if os.path.exists(test_zip_path):
                os.remove(test_zip_path)
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            print("   ✓ 测试文件已清理")
        except Exception as e:
            print(f"   ⚠ 清理测试文件失败: {e}")
    
    # 4. 测试模拟下载和解压Tesseract-OCR_TuoGuanContainer_v4.zip
    print("\n4. 模拟下载和解压Tesseract-OCR_TuoGuanContainer_v4.zip")
    try:
        # 模拟下载路径
        download_path = os.path.join(USER_DATA_DIR, UPDATE_DST_FILENAME)
        print(f"   模拟下载路径: {download_path}")
        
        # 创建一个模拟的zip文件
        import io
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("Tesseract-OCR/tesseract.exe", "模拟的tesseract.exe")
            zipf.writestr("TuoGuanContainer/container.exe", "模拟的container.exe")
        
        # 将内存中的zip文件写入磁盘
        with open(download_path, 'wb') as f:
            f.write(zip_buffer.getvalue())
        
        print(f"   ✓ 成功创建模拟的{UPDATE_DST_FILENAME}文件")
        
        # 模拟解压
        extract_to = USER_DATA_DIR
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            # 使用cp437编码读取文件名，这是zip文件的标准编码
            for file_info in zip_ref.infolist():
                # 解码文件名
                filename = file_info.filename.encode('cp437').decode('utf-8')
                # 读取文件内容
                content = zip_ref.read(file_info)
                # 写入解压目录
                output_path = os.path.join(extract_to, filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(content)
        
        # 检查解压结果
        tesseract_path = os.path.join(extract_to, "Tesseract-OCR", "tesseract.exe")
        container_path = os.path.join(extract_to, "TuoGuanContainer", "container.exe")
        
        if os.path.exists(tesseract_path) and os.path.exists(container_path):
            print("   ✓ 成功解压Tesseract-OCR和TuoGuanContainer目录")
            
            # 检查文件内容
            with open(tesseract_path, 'r') as f:
                content = f.read()
                if content == "模拟的tesseract.exe":
                    print("   ✓ Tesseract-OCR文件内容正确")
            
            with open(container_path, 'r') as f:
                content = f.read()
                if content == "模拟的container.exe":
                    print("   ✓ TuoGuanContainer文件内容正确")
        else:
            print("   ✗ 解压失败，文件不存在")
            return False
        
        # 清理模拟文件
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(os.path.join(extract_to, "Tesseract-OCR")):
            shutil.rmtree(os.path.join(extract_to, "Tesseract-OCR"))
        if os.path.exists(os.path.join(extract_to, "TuoGuanContainer")):
            shutil.rmtree(os.path.join(extract_to, "TuoGuanContainer"))
        
        print("   ✓ 模拟文件已清理")
        
    except Exception as e:
        print(f"   ✗ 模拟下载和解压失败: {e}")
        return False
    
    print("\n=== 所有测试通过，下载和解压权限正常 ===")
    return True

if __name__ == "__main__":
    success = test_download_extract_permission()
    if success:
        print("\n✓ 测试结果: 成功")
        sys.exit(0)
    else:
        print("\n✗ 测试结果: 失败")
        sys.exit(1)