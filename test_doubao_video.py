

api_key = "YOUR_DOU_BAO_API_KEY"
#pip install --upgrade "volcengine-python-sdk[ark]"
import os
import time  
# 通过 pip install 'volcengine-python-sdk[ark]' 安装方舟SDK
from volcenginesdkarkruntime import Ark

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=api_key,
)

if __name__ == "__main__":
    print("----- create request -----")
    create_result = client.content_generation.tasks.create(
        model="doubao-seedance-1-0-pro-250528", # 模型 Model ID 已为您填入
        content=[
            {
                # 文本提示词与参数组合
                "type": "text",
                "text": "帮我生成视频：帮我把附件图片生成视频。表达：先用 AI 工具把 MVP（最小可行产品）堆出来  --resolution 720p  --duration 5 --camerafixed false --watermark false"
            },
            { # 若仅需使用文本生成视频功能，可对该大括号内的内容进行注释处理，并删除上一行中大括号后的逗号。
                # 首帧图片URL
                "type": "image_url",
                "image_url": {
                    "url": "https://www.wechatai365.top:8002/download/img_1/5.png" 
                }
            }
        ]
    )
    print(f"create_result:{create_result}")

    # 轮询查询部分
    print("----- polling task status -----")
    task_id = create_result.id
    while True:
        get_result = client.content_generation.tasks.get(task_id=task_id)
        status = get_result.status
        if status == "succeeded":
            print("----- task succeeded -----")
            print(get_result)
            if get_result.content.video_url:
                print(f"video_url:{get_result.content.video_url}")

            break
        elif status == "failed":
            print("----- task failed -----")
            print(f"Error: {get_result.error}")
            break
        else:
            print(f"Current status: {status}, Retrying after 3 seconds...")
            time.sleep(3)

# 更多操作请参考下述网址
# 查询视频生成任务列表：https://www.volcengine.com/docs/82379/1521675
# 取消或删除视频生成任务：https://www.volcengine.com/docs/82379/1521720