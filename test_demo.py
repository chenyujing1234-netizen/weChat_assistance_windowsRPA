

#代码：
#变量、函数、表达式

print("hello, pipi")
i_result = 0

for i in range(0, 100):
    print("第{}次取到的数据是:{}".format(i, i))
    i_result = i_result + i

print("最后的结果是:{}".format(i_result))

# 自己写一个函数
def da_pi_pi():
    print("打皮皮")

da_pi_pi()

import os 
img_path = "‪C:\\Users\\admin\\Desktop\\weChat_assistance\\激活智能体\\1.JPG"
img_path = img_path.strip().replace("‪", "")
print(img_path)
bExist = os.path.isfile(img_path)
print("是否存在:{}".format(bExist))