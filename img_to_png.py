from PIL import Image
# 打开 JPEG 图片
img = Image.open("weichat_logo.jpeg")
# 保存为 PNG 格式
img.save("weichat_logo.png")