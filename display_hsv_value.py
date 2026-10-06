import cv2
import numpy as np

# 读取图片
#image_path = '.\\screenshot_img\\crop_temp_1.png'
#image_path = '.\\screenshot_img\\crop_temp_4.png'
#image_path = '.\\screenshot_img\\test5.png'
#image_path = '.\\screenshot_img\\first_item_of_friend_chat_list_befor.png'
image_path = 'C:\\Users\\admin\\Desktop\\44.png'
image = cv2.imread(image_path)

# 转换到HSV颜色空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 创建一个窗口来显示HSV图像
cv2.imshow('HSV Image', hsv_image)

# 创建一个事件处理函数来获取鼠标点击的HSV值
def get_hsv_value(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        h, s, v = hsv_image[y, x]
        print(f"HSV value at ({x}, {y}): ({h}, {s}, {v})")
        # 这里可以添加代码来更新你的阈值范围

# 绑定鼠标点击事件到上面的函数
cv2.setMouseCallback('HSV Image', get_hsv_value)

# 等待用户操作
cv2.waitKey(0)
cv2.destroyAllWindows()