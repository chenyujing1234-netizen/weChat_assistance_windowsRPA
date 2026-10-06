# pip install -q -U google-genai
from google import genai
import os
from google.genai import types
from PIL import Image
from io import BytesIO

# 设置环境变量
#os.environ['GEMINI_API_KEY'] = 'AIzaSyDYaMscqQZLMeJw6V7GB4b_uzucSSPXlCQ'  # 我自己的
os.environ['GEMINI_API_KEY'] = 'AIzaSyBUXxNhlh_tULfVfGId2nVz_YYgAK_0vgA'   # 闲鱼的
print("GEMINI_API_KEY:", os.getenv('GEMINI_API_KEY')) 

""" 文本生成
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
"""



################### 图图片修改（文本和图片转图片）############################
client = genai.Client()

prompt = (
    "Create a picture of my cat eating a nano-banana in a "
    "fancy restaurant under the Gemini constellation",
)

image = Image.open(r"D:\weChat_assistance\素材\专辑、通用知识-AI落地应用分享\第37期、试用 Gemini 2.5 Flash Image，我们的顶尖图像模型\1.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt, image],
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        img_save_path = "generated_image.png"
        image.save(img_save_path)
        print(f"图片保存到{img_save_path}")