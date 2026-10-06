import os
# 通过 pip install 'volcengine-python-sdk[ark]' 安装方舟SDK
# SDK 版本要求≥ 4.0.6，建议使用最新版 SDK，参考文档https://www.volcengine.com/docs/82379/1541595
from volcenginesdkarkruntime import Ark


api_key = "YOUR_DOU_BAO_API_KEY"
"""
# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=api_key,
)

imagesResponse = client.images.generate(
    model="doubao-seededit-3-0-i2i-250628",
    prompt="改成爱心形状的泡泡",
    image="https://ark-project.tos-cn-beijing.volces.com/doc_image/seededit_i2i.jpeg",
    seed=123,
    guidance_scale=5.5,
    size="adaptive",
    watermark=True 
)

print(imagesResponse.data[0].url)
"""
import os
# 通过 pip install 'volcengine-python-sdk[ark]' 安装方舟SDK
# SDK 版本要求≥ 4.0.6，建议使用最新版 SDK，参考文档https://www.volcengine.com/docs/82379/1541595
from volcenginesdkarkruntime import Ark

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key=api_key,
)

imagesResponse = client.images.generate(
    model="doubao-seededit-3-0-i2i-250628",
    prompt="参考附件中图片的风格，生成一张图片，表达：【现在，就把你的朋友圈托管给系统。  剩下的1%，从这一秒开始】 ",
    image="https://www.wechatai365.top:8002/download/man_hua/1.jpg",
    seed=123,
    guidance_scale=5.5,
    size="adaptive",
    watermark=True 
)

print(imagesResponse.data[0].url)