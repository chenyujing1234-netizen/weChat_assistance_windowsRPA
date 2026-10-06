#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from app_info import *

def test_directories():
    """测试TESSERACT_DIR和LEI_DIAN_DIR目录是否正确设置"""
    
    print("=== 测试TESSERACT_DIR和LEI_DIAN_DIR目录 ===")
    
    # 1. 测试TESSERACT_DIR目录
    print(f"1. TESSERACT_DIR目录: {TESSERACT_DIR}")
    if os.path.exists(TESSERACT_DIR):
        print("   ✓ TESSERACT_DIR目录存在")
        # 检查是否可写
        test_file = os.path.join(TESSERACT_DIR, "test_write_permission.txt")
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write("测试写入权限")
            print("   ✓ TESSERACT_DIR目录可写")
            os.remove(test_file)
            print("   ✓ 测试文件已删除")
        except Exception as e:
            print(f"   ✗ TESSERACT_DIR目录不可写: {e}")
            return False
    else:
        print("   ✗ TESSERACT_DIR目录不存在")
        return False
    
    # 2. 测试LEI_DIAN_DIR目录
    print(f"\n2. LEI_DIAN_DIR目录: {LEI_DIAN_DIR}")
    if os.path.exists(LEI_DIAN_DIR):
        print("   ✓ LEI_DIAN_DIR目录存在")
        # 检查是否可写
        test_file = os.path.join(LEI_DIAN_DIR, "test_write_permission.txt")
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write("测试写入权限")
            print("   ✓ LEI_DIAN_DIR目录可写")
            os.remove(test_file)
            print("   ✓ 测试文件已删除")
        except Exception as e:
            print(f"   ✗ LEI_DIAN_DIR目录不可写: {e}")
            return False
    else:
        print("   ✗ LEI_DIAN_DIR目录不存在")
        return False
    
    # 3. 检查目录是否在用户数据目录下
    user_data_dir = USER_DATA_DIR
    print(f"\n3. 用户数据目录: {user_data_dir}")
    
    if TESSERACT_DIR.startswith(user_data_dir):
        print("   ✓ TESSERACT_DIR在用户数据目录下")
    else:
        print("   ✗ TESSERACT_DIR不在用户数据目录下")
        return False
    
    if LEI_DIAN_DIR.startswith(user_data_dir):
        print("   ✓ LEI_DIAN_DIR在用户数据目录下")
    else:
        print("   ✗ LEI_DIAN_DIR不在用户数据目录下")
        return False
    
    print("\n=== 所有目录测试通过 ===")
    return True

if __name__ == "__main__":
    success = test_directories()
    if success:
        print("\n✓ 测试结果: 成功")
        sys.exit(0)
    else:
        print("\n✗ 测试结果: 失败")
        sys.exit(1)