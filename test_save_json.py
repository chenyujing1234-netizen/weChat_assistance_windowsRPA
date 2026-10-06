import json

# 使用模拟数据，不发送实际请求
try:
    # 模拟响应数据
    response_data = {
        "userId": 1,
        "id": 1,
        "title": "测试数据",
        "completed": False
    }
    print(f"请求后返回的数据是:{response_data}")
    
    # 将响应数据保存到log.txt文件
    with open("log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(json.dumps(response_data, ensure_ascii=False, indent=4))
    print("响应数据已保存到log.txt文件")
    
except Exception as e:
    print(f"发生错误: {e}")