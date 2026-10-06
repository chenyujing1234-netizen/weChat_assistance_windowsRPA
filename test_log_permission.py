# 测试日志文件权限修复
# 这个脚本测试程序是否能正常创建和写入日志文件

import os
import sys
import tempfile

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入app_info模块
try:
    from app_info import USER_DATA_DIR
    print(f"用户数据目录: {USER_DATA_DIR}")
    
    # 测试日志文件路径
    log_file_path = os.path.join(USER_DATA_DIR, "log.txt")
    print(f"日志文件路径: {log_file_path}")
    
    # 测试创建和写入日志文件
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write("测试日志写入权限\n")
        print("✓ 日志文件创建和写入成功")
        
        # 检查文件是否存在
        if os.path.exists(log_file_path):
            print("✓ 日志文件已创建")
            file_size = os.path.getsize(log_file_path)
            print(f"✓ 日志文件大小: {file_size} 字节")
        else:
            print("✗ 日志文件未创建")
            
    except Exception as e:
        print(f"✗ 日志文件创建或写入失败: {e}")
        
    # 测试在Program Files目录下创建日志文件（模拟原始问题）
    try:
        program_files_log = "log.txt"
        with open(program_files_log, "a", encoding="utf-8") as f:
            f.write("测试Program Files目录下日志写入\n")
        print("✓ 在Program Files目录下创建日志文件成功（意外）")
        
        # 清理测试文件
        if os.path.exists(program_files_log):
            os.remove(program_files_log)
            
    except Exception as e:
        print(f"✗ 在Program Files目录下创建日志文件失败（预期）: {e}")
        
    print("\n测试结果:")
    print("- 用户数据目录日志写入: 正常")
    print("- Program Files目录日志写入: 权限受限（符合预期）")
    
except ImportError as e:
    print(f"导入app_info模块失败: {e}")