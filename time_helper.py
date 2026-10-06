import time
import threading
import sys
from app_info import * 

g_time_begin_dict = {}

def get_caller_name(depth=1):
    # 获取当前的帧
    frame = sys._getframe(depth)
    try:
        # 获取调用者（caller）的帧
        caller_frame = frame.f_back
        if caller_frame == None:
            return ""
        # 获取调用者的帧对象中的函数名
        caller_name = caller_frame.f_code.co_name
        return caller_name
    finally:
        # 避免保留对帧对象的引用，以防发生内存泄漏
        del frame
        
def TIME_BEGIN(time_obj_name = ""):
    global g_time_begin_dict
    
    if g_b_Debug == False:
        return 

    # 构建时间唯一标识
    if len(time_obj_name) == 0:
        current_thread = threading.current_thread()
        thread_id_str = str(current_thread.ident)
        current_func_name = get_caller_name()
        time_obj_name = thread_id_str + "_" + current_func_name
    start_time = time.time() 
    g_time_begin_dict[time_obj_name] = start_time
    return 
    
def TIME_END(time_obj_name = ""):
    global g_time_begin_dict
    
    b_has_input_time_obj_name = False
    if g_b_Debug == False:
        return 
     
    # 构建时间唯一标识
    if len(time_obj_name) == 0:
        current_thread = threading.current_thread()
        thread_id_str = str(current_thread.ident)
        current_func_name = get_caller_name()
        time_obj_name = thread_id_str + "_" + current_func_name
        b_has_input_time_obj_name = False    
    else: 
        b_has_input_time_obj_name = True  
    if time_obj_name not in g_time_begin_dict:
        print("!!!!请先调用TIME_BEGIN")
        return 
    start_time = g_time_begin_dict[time_obj_name]
    time_taken = time.time() - start_time   
    
    caller_name = get_caller_name()
    
    if b_has_input_time_obj_name == True: 
        print("******[{}]函数内的\"{}\"耗时【{:.2f}】秒******".format(caller_name, time_obj_name, time_taken))
    else: 
        print("******[{}]函数耗时【{:.2f}】秒******".format(caller_name, time_taken))
    return     

#TIME_BEGIN()
#time.sleep(1)
#TIME_END()