from PIL import Image

# 打开JPEG文件
image = Image.open("E:\\Source\MineContext-0.1.2\\frontend\\build\\icon.png")

# 将图片转换为32x32的图标
icon = image.resize((32, 32), Image.Resampling.LANCZOS)

# 保存为ICO文件
icon.save("E:\\Source\\MineContext-0.1.2\\frontend\\build\\icon.ico")