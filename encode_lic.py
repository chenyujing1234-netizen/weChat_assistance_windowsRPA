# -*- coding: utf-8 -*-
from base64 import b64encode
from pyperclip import copy

SECTRY_STR = "%￥#*&#" 
# user_type
#        -2 过期 
#        -1 试用
#         0 永久 
#         1 1个月
#         2 1年
USER_TYPE_DICT = {"user_type_-1":"-1", "user_type_0":"0", "user_type_1":"1", "user_type_2":"2"}
user_type_str = "user_type_0"
#g_str_mac = "98:fa:9b:bc:f0:57"
#g_str_mac = "04:ed:33:14:24:41" # 我的笔计本
#g_str_mac = "a1:19:30:6d:30:62" # 金鹏
#g_str_mac = "7d:7a:0b:18:a2:7d"
#g_str_mac = "00-E2-69-68-91-10"  # 陈文
#g_str_mac = "98-FA-9B-BC-F0-57" # 我自己的
g_str_mac = "B4-2E-99-BC-F5-61" # 我的私人台式机1
#g_str_mac = "00-FF-D9-76-3D-2E"
#g_str_mac = "FC-34-97-DF-1B-A2"
#g_str_mac = "D8-C4-97-0E-F0-83" # 北宸教育网上认识
#g_str_mac = "58-11-22-2D-A7-0F" # 网上认识汇黔汽车科技-官方1
#g_str_mac = "28-C5-C8-D2-62-C4" # 网上认识汇黔汽车科技-官方2
str_input = g_str_mac + SECTRY_STR + user_type_str
res = b64encode(str_input.encode()).decode()  
print("得到的授权码是:{}".format(res))
print("已经复制到剪切板里")
copy(res) 