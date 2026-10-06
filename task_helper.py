from log_helper import print_my
import random
import json
from threading import Lock
from yang_hao_opt import add_new_frient_with_check, add_new_frient_with_check_windows, send_circle_with_check, send_message_by_search, add_friends_in_group_with_check
from config_helper import g_config_path, load_config_data, save_config_data
from error_code import *
from app_info import *
from datetime import datetime, timedelta
import time

print("===2===========TASK_TIME_INTER_OF_ADD_NEW_FRIENT:{}".format(TASK_TIME_INTER_OF_ADD_NEW_FRIENT))

g_lock_task = Lock()
g_last_process_add_new_friend_time = 0
g_last_process_add_group_new_friend_time = 0
# 从任务列表中随机取出一个任务
def get_random_one_task(config_json_data):
    global g_last_process_add_new_friend_time
    global g_last_process_add_group_new_friend_time
    g_lock_task.acquire()
    
    task_info_list = config_json_data["TASK_INFO_LIST"]
    # 取出还没完成的任务
    task_info_list_no_finish = [task_info for task_info in task_info_list if task_info["task_process"] not in ["100", "-1"] ]
    if len(task_info_list_no_finish) <= 0:
        print("!!!当前没有可执行的任务")
        
        g_lock_task.release()
        
        return APP_RET_CODE_NO_CAN_EXE_TASK, {}
        
    # 找出所有定时时间到的任务
    task_info_list_no_finish_and_timed = []
    for task_info in task_info_list_no_finish:
        # 对几类任务进行频率的控制
        if task_info["task_type"] in ["批量加好友"]:
            time_taken = time.time() - g_last_process_add_new_friend_time
            print("TASK_TIME_INTER_OF_ADD_NEW_FRIENT:{}".format(TASK_TIME_INTER_OF_ADD_NEW_FRIENT))
            if time_taken < TASK_TIME_INTER_OF_ADD_NEW_FRIENT:
                continue 
        if task_info["task_type"] in ["加微信群好友"]:
            time_taken = time.time() - g_last_process_add_group_new_friend_time
            TASK_TIME_INTER_OF_ADD_GROUP_NEW_FRIENT = int(task_info["task_detail_data"]["ADD_INTER"])*60
            print("TASK_TIME_INTER_OF_ADD_GROUP_NEW_FRIENT:{}".format(TASK_TIME_INTER_OF_ADD_GROUP_NEW_FRIENT))
            if time_taken < TASK_TIME_INTER_OF_ADD_GROUP_NEW_FRIENT:
                continue 
        # 判断是否达到当天加好友的最大个数
        if task_info["task_type"] in ["批量加好友", "加微信群好友"] and "max_count_everyday" in task_info:
            task_finish_detail_data = task_info["task_finish_detail_data"]
            max_count_everyday = int(task_info["max_count_everyday"])
            i_today_count = 0
            current_date = datetime.now().date()
            time_format = '%Y-%m-%d'
            current_date_str = current_date.strftime(time_format)
            for task_finish_detail_data_ in task_finish_detail_data:
                if "happen_time" in task_finish_detail_data_:
                    happen_time_str = task_finish_detail_data_["happen_time"]
                    date_time_obj = datetime.strptime(happen_time_str, "%Y-%m-%d %H:%M:%S")
                    date_obj = date_time_obj.date()
                    happen_date_str = date_obj.strftime("%Y-%m-%d")
                    if current_date_str == happen_date_str:
                        i_today_count += 1
            if i_today_count >= max_count_everyday:
                print("!!!当天已达到加好友的最大个数{},等明天再执行".format(max_count_everyday))
                continue
        
        task_data = task_info["task_data"]
        # 定义时间格式
        time_format = "%Y-%m-%d %H:%M:%S"
        # 将字符串解析为datetime对象
        datetime_str_of_task = "{} {}".format(task_data["date"], task_data["time"])
        datetime_of_task = datetime.strptime(datetime_str_of_task, time_format)
        datetime_of_now = datetime.now()
        difference_seconds = abs((datetime_of_task - datetime_of_now).total_seconds())
        if datetime_of_now > datetime_of_task or (datetime_of_now < datetime_of_task and difference_seconds < 60):
            task_info_list_no_finish_and_timed.append(task_info)
            #g_lock_task.release()
            #return APP_RET_CODE_SUCESS, task_info
            
    if len(task_info_list_no_finish_and_timed) <= 0:
        print("!!!当前没有可执行的到达执行时间的任务")
        g_lock_task.release()
        return APP_RET_CODE_NO_CAN_EXE_TASK, {}   
    # 
    # 1.人工规则：优先取出“同步好友”的任务
    for task_info in task_info_list_no_finish_and_timed:
        task_type = task_info["task_type"]
        if task_type == "同步好友":
            g_lock_task.release()
            return APP_RET_CODE_SUCESS, task_info
            
    # 随机抽一个任务 
    task_info = random.choice(task_info_list_no_finish_and_timed)
    if task_info["task_type"] in ["批量加好友"]:
        g_last_process_add_new_friend_time = time.time() 
    if task_info["task_type"] in ["加微信群好友"]:
        g_last_process_add_group_new_friend_time = time.time()    
         
    g_lock_task.release()
    
    return APP_RET_CODE_SUCESS, task_info

# 根据用户配置在更新任务状态 
def update_task_state_by_setting(config_json_data):
    g_lock_task.acquire()

    task_info_list = config_json_data["TASK_INFO_LIST"]
    if False == config_json_data["g_b_Do_Exceed_Task"]:
        for task_info in task_info_list:
            if task_info["task_process"] in ["100", "-1"]:
                continue
            task_data = task_info["task_data"]
            # 定义时间格式
            time_format = "%Y-%m-%d %H:%M:%S"
            # 将字符串解析为datetime对象
            datetime_str_of_task = "{} {}".format(task_data["date"], task_data["time"])
            #print(datetime_str_of_task)
            datetime_of_task = datetime.strptime(datetime_str_of_task, time_format)
            datetime_of_now = datetime.now()
            difference_seconds = abs((datetime_of_task - datetime_of_now).total_seconds())
            if datetime_of_now > datetime_of_task and  difference_seconds > 60:
                task_info["task_process"] = "-1"
                print("!!!将过期的任务[{}]标记为-1".format(task_info["task_distribe"]))
    save_config_data(config_json_data, g_config_path) 
    
    g_lock_task.release()
    
    return 
            
# 获得任务的详细数据
def get_task_detail_data(task_info):
    data_list_of_detail = []
    
    task_type = task_info["task_type"]
    task_data = task_info["task_data"]
    if task_type == "批量加好友":
        file_paths = task_data["file_paths"]
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        username = line.strip() 
                        if len(username) == 0:
                            continue
                        data_list_of_detail.append(username)
            except FileNotFoundError:
                print("文件{}未找到，请检查文件路径是否正确".format(file_path))
            except Exception as e:
                print("读取文件{}时发生错误:\n {}".format(file_path, e))
    return data_list_of_detail
    
# 获得可用于加好友的列表 
def get_add_user_name_list(task_info):
    user_name_of_add_list = []
    
    task_type = task_info["task_type"]
    task_distribe = task_info["task_distribe"]
    task_process = task_info["task_process"]
    task_data = task_info["task_data"]
    task_deatail_data = task_info["task_detail_data"]
    task_finish_detail_data = task_info["task_finish_detail_data"]
    
    for data in task_deatail_data:
        if data not in [data_["name"] for data_ in task_finish_detail_data]:
           user_name_of_add_list.append(data)
    print("从[{}]任务中共读取到{}个要添加的好友，扣除已经添加用户{}个后，待添加的好友有{}个".format(task_distribe, len(task_deatail_data), len(task_finish_detail_data), len(user_name_of_add_list)))    
      
    return user_name_of_add_list

# 获得可用于发单聊消息的好友列表 
def get_single_chat_user_name_list(task_info):
    user_name_of_send_list = []
    
    task_type = task_info["task_type"]
    task_distribe = task_info["task_distribe"]
    task_process = task_info["task_process"]
    task_data = task_info["task_data"]
    username_of_can_see_list = task_data["username_of_can_see_list"]  
    username_of_finish_list = task_data["username_of_finish_list"] 
    
    for data in username_of_can_see_list:
        if data not in username_of_finish_list:
           user_name_of_send_list.append(data)
    print("从[{}]任务中共读取到{}个要发单聊消息的好友，扣除已经发过用户{}个后，待发送的好友有{}个".format(task_distribe, len(username_of_can_see_list), len(username_of_finish_list), len(user_name_of_send_list)))    
      
    return user_name_of_send_list
    
def process_one_task(table, input_event, task_info, config_json_data):
    global g_last_process_add_new_friend_time
    global g_last_process_add_group_new_friend_time
    
    b_has_process_task = False

    task_type = task_info["task_type"]
    task_distribe = task_info["task_distribe"]
    task_process = task_info["task_process"]
    task_data = task_info["task_data"]
    #task_finish_data = task_info["task_finish_detail_data"]
    
    if task_process == "100":
        return APP_RET_CODE_SUCESS, b_has_process_task

	# 更新原有的变量
    # 放在这里是为了使客户组调整了成员后能马上生效
    if "usergroup_name_of_can_see" in task_data:
        username_of_can_see_list = []
        usergroup_info_select = {}
        usergroup_info_list = config_json_data["USERGROUP_INFO_LIST"]
        for usergroup_info in usergroup_info_list:
            if usergroup_info["usergroup_name"] == task_data["usergroup_name_of_can_see"]:
                usergroup_info_select = usergroup_info
                break
        if "usergroup_member" in usergroup_info_select:
            for member in usergroup_info_select["usergroup_member"]:
                username_of_can_see_list.append(member)
        if len(username_of_can_see_list) == 0:
            print_my("原有的客户组:【{}】没有成员或者不存在".format(task_data["usergroup_name_of_can_see"]))
        task_data["username_of_can_see_list"] = username_of_can_see_list
        print("触达成员:{}".format(username_of_can_see_list))
        
        # 更新已完成成员的数据
        username_of_finish_list = []
        if "username_of_finish_list" in task_data:
            for username_of_finish in task_data["username_of_finish_list"]:
                if username_of_finish not in username_of_can_see_list:
                    continue
                username_of_finish_list.append(username_of_finish)
            task_data["username_of_finish_list"] = username_of_finish_list
            
    if task_type == "批量加好友":
        username_of_new_friend = ""
        if "remark_prefix" not in task_data:
            task_data["remark_prefix"] = ""
            
        user_name_of_add_list = get_add_user_name_list(task_info)
        print("共有{}个待加好友".format(len(user_name_of_add_list)))
        username_of_new_friend = random.choice(user_name_of_add_list)
        print_my("随机选到要加的好友是:{}".format(username_of_new_friend))
        if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows:
            iRet = add_new_frient_with_check_windows(input_event, username_of_new_friend, task_data["remark_prefix"], False)
        else:
            iRet = add_new_frient_with_check(input_event, username_of_new_friend, task_data["remark_prefix"], False)
        g_last_process_add_new_friend_time = time.time()
        if iRet not in [APP_RET_CODE_CANNOT_ADD, APP_RET_CODE_SUCESS]:
            return iRet, b_has_process_task
         
        b_has_process_task = True  
        if iRet == APP_RET_CODE_SUCESS:
            print_my("成功发送加好友【{}】消息".format(username_of_new_friend))
            
        task_detail_data = task_info["task_detail_data"]
        task_finish_detail_data = task_info["task_finish_detail_data"]
        current_time = current_datetime = datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        task_finish_detail_data.append({"name":username_of_new_friend, "result_code": iRet, "happen_time": current_time_str})
        task_info["task_process"] = str(int(len(task_finish_detail_data)/len(task_detail_data) * 100))
        print("[{}/{}]更新进度为:{}".format(len(task_finish_detail_data), len(task_detail_data), task_info["task_process"]))
        task_info["task_finish_detail_data"] = task_finish_detail_data
    elif task_type == "加微信群好友":
        if "remark_prefix" not in task_data:
            task_data["remark_prefix"] = ""
        group_add_rule_info = task_info["task_detail_data"]
        task_finish_detail_data = task_info["task_finish_detail_data"]
        
        #{"GROUP_NAME": groupName, "MAX_COUNT_ONE_DAY": max_count_one_day, "ADD_INTER": group_add_inter}
        # "鲸跃资源 前后端对接"
        print_my("群【{}】已经完成{}个成员的加好友动作。现在继续剩下的...".format(group_add_rule_info["GROUP_NAME"], len(task_finish_detail_data)))
        iRet, username_new_add_list = add_friends_in_group_with_check(input_event, group_add_rule_info["GROUP_NAME"], [data_["name"] for data_ in task_finish_detail_data], task_data["remark_prefix"])
        g_last_process_add_group_new_friend_time = time.time() 
        if iRet not in [APP_RET_CODE_GROUP_HAS_RELEASE, APP_RET_CODE_NO_FINISH, APP_RET_CODE_SUCESS] and len(username_new_add_list) == 0:
            return iRet, b_has_process_task
        
        b_has_process_task = True  
            
        if iRet == APP_RET_CODE_GROUP_HAS_RELEASE:
            print_my("!!!此群【{}】已经解散，不可用于添加群成员为好友。更新此任务【加微信群好友】的进度为100".format(group_add_rule_info["GROUP_NAME"]))    
            task_info["task_process"] = str(100)
        elif iRet == APP_RET_CODE_SUCESS:
            print_my("!!!此群【{}】所有成员添加完成。更新此任务【加微信群好友】的进度为100".format(group_add_rule_info["GROUP_NAME"]))    
            task_info["task_process"] = str(100)
        else:
            if len(username_new_add_list) > 0:
                print_my("成功发送加微信群【{}】好友【{}】个".format(group_add_rule_info["GROUP_NAME"], len(username_new_add_list)))
            #task_detail_data = task_info["task_detail_data"]
            task_finish_detail_data = task_info["task_finish_detail_data"]
            current_time = current_datetime = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            task_finish_detail_data_this = [{"name": username_new_add, "happen_time":current_time_str} for username_new_add in username_new_add_list]
            task_finish_detail_data.extend(task_finish_detail_data_this)
            # chenyj debug
            print("已经添加的取成员是：【{}】".format(task_finish_detail_data))
            print("目前群【{}】已经完成{}个,为了安全，现在要暂停下".format(group_add_rule_info["GROUP_NAME"], len(task_finish_detail_data)))
            task_info["task_process"] = str(int(len(task_finish_detail_data)/200 * 100))
            print("[{}/{}]更新进度为:{}".format(len(task_finish_detail_data), 200, task_info["task_process"]))
            task_info["task_finish_detail_data"] = task_finish_detail_data
    elif task_type == "定时发朋友圈": 
        circle_data_dict = task_data
        str_wenAn = circle_data_dict["wenAn"] 
        img_paths = circle_data_dict["img_paths"]        
        username_of_can_see_list = circle_data_dict["username_of_can_see_list"]            
        iRet = send_circle_with_check(input_event, str_wenAn, username_of_can_see_list, img_paths)
        if iRet not in [APP_RET_CODE_SUCESS]:
            print_my("!!!发送朋友圈失败{}【请再试一次】".format(iRet))
            return iRet, b_has_process_task
        
        b_has_process_task = True  
        print_my("发送朋友圈成功")
        task_info["task_process"] = "100"
    elif task_type == "定时发单聊消息":
        circle_data_dict = task_data
        str_wenAn = circle_data_dict["wenAn"] 
        img_paths = circle_data_dict["img_paths"]        
 
        
        user_name_of_send_list = get_single_chat_user_name_list(task_info)
        print("共有{}个待发送单聊消息好友".format(len(user_name_of_send_list)))
        if len(user_name_of_send_list) == 0:
            task_info["task_process"] = str(100)
            print_my("没有待发送的单聊消息好友，更新进度为:{}".format(task_info["task_process"]))
            b_has_process_task = True  
            return APP_RET_CODE_SUCESS, b_has_process_task
        
        username_of_new_friend = random.choice(user_name_of_send_list)
        print_my("随机选到要发送单聊消息的好友是:{}".format(username_of_new_friend))
        iRet = send_message_by_search(input_event, username_of_new_friend, str_wenAn, img_paths)       
        if iRet not in [APP_RET_CODE_SUCESS, APP_RET_CODE_FRIEND_NO_FOUND]:
            print_my("!!!发送单聊消息失败{}【请再试一次】".format(iRet))
            return iRet, b_has_process_task
        
        if iRet == APP_RET_CODE_FRIEND_NO_FOUND:
            print_my("!!!执行了动作，但没有成功。 原因:好友[{}]搜索不到".format(username_of_new_friend))
            # 将此用户从好友列表中清除
            friend_info_list = config_json_data["FRIEND_INFO_LIST"]
            position = next((i for i, item in enumerate(friend_info_list) if item["friend_name"] == username_of_new_friend), None)
            if position is not None:
                print_my("好友[{}]已经被删除，从好友列表里删除掉".format(username_of_new_friend))
                del friend_info_list[position]  
                config_json_data["FRIEND_INFO_LIST"] = friend_info_list
                save_config_data(config_json_data, g_config_path) 
                table.signal_of_table.emit("reload_friend_list_view") 
                # 更新客户组
                for usergroup in config_json_data["USERGROUP_INFO_LIST"]:
                    if username_of_new_friend in usergroup["usergroup_member"]:
                        usergroup["usergroup_member"].remove(username_of_new_friend)
                save_config_data(config_json_data, g_config_path)
                table.signal_of_table.emit("reload_usergroup_list_view")
        
        username_of_can_see_list = circle_data_dict["username_of_can_see_list"] 
        # 去重
        username_of_can_see_list = list(set(username_of_can_see_list))
        username_of_finish_list = circle_data_dict["username_of_finish_list"] 
        username_of_finish_list.append(username_of_new_friend)
        task_info["task_process"] = str(int(len(username_of_finish_list)/len(username_of_can_see_list) * 100))
        print("[{}/{}]更新进度为:{}".format(len(username_of_finish_list), len(username_of_can_see_list), task_info["task_process"]))
        task_info["username_of_finish_list"] = username_of_finish_list
 
        
        b_has_process_task = True  
        print_my("发送单聊消息成功")
        #task_info["task_process"] = "100"
        
    return APP_RET_CODE_SUCESS, b_has_process_task
    
# chenyj test  
WEN_AN_DATA_FILE_PATH = "C:\\Users\\admin\\Desktop\\weChat_assistance\\激活智能体\\激活智能体的30天话术.json"
CONFIG_FILE_PATH = g_config_path
USERNAME_LIST = ["直奔主题网上认识", "锦不认识", "点网上认识", "笑网上认识", "闷网上认识", "公子网上认识", "姚星网上认识", "焦糖网上认识", "脚本网上认识", "象象网上认识", "迪克网上认识", "阿浪网上认识", "黑马网上认识", "AAA网上认识", "Leo网上认识", "加菲猫网上认识", "张立博网上认识", "徐俊华网上认识", "雷公子网上认识", "干就完了网上认识", "最早的早安网上认识", "热心丙火男网上认识", "美国本土仓网上认识", "教培老师", "笑一笑十年少网上认识", "爱喝奶茶", "Alston Ling宝乐介绍书", "Anki记忆卡淑清", "A派大星", "A五谷杂粮小麻花", "A移动办宽带办卡升", "报佳音书店", "贝壳家的茶", "biendata小助手", "潮漫酒店广州天河", "CV君", "AMY宏举", "anki赵金鹏", "蔡超", "彩凤", "长春", "产品研发-陈建辉", "超超", "超艺", "承龙", "陈建辉", "陈仕镇网龙", "陈毅宁", "陈传校", "春松"]


# 创建朋友圈SOP 
def test_create_cirle_SOP_of_ji_huo_agent():
    #
    #
    wenAn_list = []
    try:
        with open(WEN_AN_DATA_FILE_PATH, 'r', encoding='utf-8') as file:
            wenAn_list = json.load(file)
            print("{}文件加载成功！共有{}条数据".format(WEN_AN_DATA_FILE_PATH, len(wenAn_list)))
    except Exception as e:
        print("加载文件{}时发生错误：{}".format(WEN_AN_DATA_FILE_PATH, e))
    #
    # 去掉前10条
    wenAn_list = wenAn_list[10:]
    #   
    data_config = {}
    try:
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as file:
            data_config = json.load(file)
            print("{}文件加载成功！".format(CONFIG_FILE_PATH))
    except Exception as e:
        print("加载文件{}时发生错误：{}".format(WEN_AN_DATA_FILE_PATH, e))
    #
    #
    task_info_list = []
    for i, wenAn_data in enumerate(wenAn_list):
        task_info = {}
        task_data = {}
        
        #
        task_info["task_type"] = "定时发朋友圈"
        task_info["task_distribe"] = "定时发朋友圈"
        task_info["task_process"] = "0"
        task_info["task_detail_data"] = [],
        task_info["task_finish_detail_data"] = []
        #
        task_data["wenAn"] = wenAn_data["content"]
        task_data["img_paths"] = ["‪C:/Users/admin/Desktop/weChat_assistance/激活智能体/1.JPG"]
        task_data["username_of_can_see_list"] = USERNAME_LIST
        #days_inter = int(wenAn_data["index"]) - 1
        days_inter = i
        current_date = datetime.now().date()
        next_date = current_date + timedelta(days=days_inter)

        task_data["date"] = next_date.strftime('%Y-%m-%d')
        task_data["time"] = "12:17:42"
 
        task_info["task_data"] = task_data
 
        task_info_list.append(task_info)
    data_config["TASK_INFO_LIST"] = task_info_list
    
    #
    # 保存配置文件
    save_config_data(data_config, CONFIG_FILE_PATH)
    print("共{}个任务。配置文件{}保存成功".format(len(data_config["TASK_INFO_LIST"]), CONFIG_FILE_PATH))
#test_create_cirle_SOP_of_ji_huo_agent()