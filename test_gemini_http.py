import base64
import json
import os
import requests

# ========== 参数 ==========
IMG_PATH = r"D:\weChat_assistance\素材\专辑、通用知识-AI落地应用分享\第37期、试用 Gemini 2.5 Flash Image，我们的顶尖图像模型\1.jpg"          # 本地猫照片
PROMPT_TEXT = "把图片的背景换成篮球场"
OUTPUT_PATH = r"D:\weChat_assistance\素材\专辑、通用知识-AI落地应用分享\第37期、试用 Gemini 2.5 Flash Image，我们的顶尖图像模型\gemini-edited-image.png"      # 生成结果保存路径

#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # 建议用环境变量传密钥
# https://llmxapi.com/ 平台上的
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
# ==========================

if not GEMINI_API_KEY:
    raise SystemExit("请先 export GEMINI_API_KEY=你的密钥")

# 1. 把图片读进来并做 base64 编码
try:
    with open(IMG_PATH, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    print(f"图片文件不存在: {IMG_PATH}")
    raise SystemExit("请检查图片路径是否正确")

# 2. 构造请求体
#url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"
# https://llmxapi.com/ 平台上的
url = "https://llmxapi.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent"

payload = {
    "contents": [{
        "parts": [
            {"text": PROMPT_TEXT},
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_b64
                }
            }
        ]
    }]
}

# 3. 发请求
resp = requests.post(
    url,
    headers={
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    },
    data=json.dumps(payload),
    timeout=60
)
resp.raise_for_status()

# 4. 从返回里抠出 base64 图片并解码保存
try:
    # 返回格式：{"candidates": [{"content": {"parts": [{"inlineData": {"data": "xxx..."}}]}}]}
    b64_new_img = resp.json()["candidates"][0]["content"]["parts"][1]["inlineData"]["data"]
except (KeyError, IndexError) as e:
    response_data = resp.json()
    # 将响应数据保存到log.txt文件
    with open("log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(json.dumps(response_data, ensure_ascii=False, indent=4))
    print("响应数据已保存到log.txt文件")
    
    raise SystemExit("返回结构异常，无法提取图片字段:", e)

with open(OUTPUT_PATH, "wb") as f:
    f.write(base64.b64decode(b64_new_img))

print("已生成图片:", OUTPUT_PATH)