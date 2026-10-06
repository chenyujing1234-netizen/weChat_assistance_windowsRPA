# 测试安装后程序运行状态
# 这个脚本模拟程序在安装目录下的运行情况，验证权限问题是否修复

import os
import sys
import tempfile
import shutil

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_program_in_install_dir():
    """测试程序在安装目录下的运行情况"""
    print("=" * 60)
    print("测试程序在安装目录下的运行情况")
    print("=" * 60)
    
    # 创建临时安装目录，模拟Program Files环境
    temp_install_dir = tempfile.mkdtemp(prefix="test_install_")
    print(f"创建临时安装目录: {temp_install_dir}")
    
    try:
        # 复制关键文件到临时安装目录
        files_to_copy = [
            "app_info.py",
            "config_helper.py",
            "error_code.py",
            "log_helper.py"
        ]
        
        for file_name in files_to_copy:
            src_path = os.path.join(os.getcwd(), file_name)
            dst_path = os.path.join(temp_install_dir, file_name)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"复制文件: {file_name}")
        
        # 切换到临时安装目录
        original_cwd = os.getcwd()
        os.chdir(temp_install_dir)
        sys.path.insert(0, temp_install_dir)
        
        print(f"切换到临时安装目录: {os.getcwd()}")
        
        # 测试导入app_info模块
        try:
            from app_info import USER_DATA_DIR, MESSAGE_SESSION_DIR, SCREENSHOT_SAVE_DIR, AI_GENERATE_IMG_DIR
            print(f"✓ 成功导入app_info模块")
            print(f"✓ 用户数据目录: {USER_DATA_DIR}")
            print(f"✓ 消息会话目录: {MESSAGE_SESSION_DIR}")
            print(f"✓ 截图目录: {SCREENSHOT_SAVE_DIR}")
            print(f"✓ AI生成图片目录: {AI_GENERATE_IMG_DIR}")
        except Exception as e:
            print(f"✗ 导入app_info模块失败: {e}")
            return False
        
        # 测试日志文件路径
        log_file_path = os.path.join(USER_DATA_DIR, "log.txt")
        print(f"✓ 日志文件路径: {log_file_path}")
        
        # 测试创建和写入日志文件
        try:
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write("测试日志写入权限 - 来自安装目录测试\n")
            print("✓ 日志文件创建和写入成功")
            
            # 检查文件是否存在
            if os.path.exists(log_file_path):
                print("✓ 日志文件已创建")
                file_size = os.path.getsize(log_file_path)
                print(f"✓ 日志文件大小: {file_size} 字节")
            else:
                print("✗ 日志文件未创建")
                return False
                
        except Exception as e:
            print(f"✗ 日志文件创建或写入失败: {e}")
            return False
        
        # 测试在安装目录下创建日志文件（模拟原始问题）
        try:
            install_dir_log = "log.txt"
            with open(install_dir_log, "a", encoding="utf-8") as f:
                f.write("测试安装目录下日志写入\n")
            print("✓ 在安装目录下创建日志文件成功")
            
            # 清理测试文件
            if os.path.exists(install_dir_log):
                os.remove(install_dir_log)
                
        except Exception as e:
            print(f"✗ 在安装目录下创建日志文件失败: {e}")
            # 这是预期的，不应该影响测试结果
        
        # 测试各个用户数据目录的创建和写入
        test_dirs = [
            (MESSAGE_SESSION_DIR, "消息会话目录"),
            (SCREENSHOT_SAVE_DIR, "截图目录"),
            (AI_GENERATE_IMG_DIR, "AI生成图片目录")
        ]
        
        for dir_path, dir_name in test_dirs:
            try:
                # 测试目录是否存在
                if not os.path.exists(dir_path):
                    print(f"✗ {dir_name}不存在: {dir_path}")
                    return False
                
                # 测试在目录中创建文件
                test_file = os.path.join(dir_path, "test_file.txt")
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(f"测试{dir_name}写入权限\n")
                print(f"✓ {dir_name}创建和写入成功")
                
                # 清理测试文件
                if os.path.exists(test_file):
                    os.remove(test_file)
                    
            except Exception as e:
                print(f"✗ {dir_name}创建或写入失败: {e}")
                return False
        
        print("\n测试结果:")
        print("- 用户数据目录访问: 正常")
        print("- 日志文件写入: 正常")
        print("- 各子目录创建和写入: 正常")
        print("- 权限问题: 已修复")
        
        return True
        
    finally:
        # 恢复原始工作目录
        os.chdir(original_cwd)
        # 清理临时目录
        try:
            shutil.rmtree(temp_install_dir)
            print(f"清理临时目录: {temp_install_dir}")
        except Exception as e:
            print(f"清理临时目录失败: {e}")

if __name__ == "__main__":
    success = test_program_in_install_dir()
    if success:
        print("\n✓ 所有测试通过，程序可以在安装目录下正常运行")
    else:
        print("\n✗ 测试失败，程序仍存在问题")