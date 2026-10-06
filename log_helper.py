from memory_profiler_helper import DEBUG_CURREN_MEM
DEBUG_CURREN_MEM("log_helper.py 刚开始")
from server_http_opt import *
DEBUG_CURREN_MEM("log_helper.py 加载server_http_opt")
from threading import Lock
DEBUG_CURREN_MEM("log_helper.py 加载threading")

# 写到窗口日志控件的函数
g_table_object = None

# 日志模型初始函数
def print_init(table_object):
    global g_table_object
    
    g_table_object = table_object
    return 
    
g_lock_print = Lock()
def print_my(text):
    global g_table_object
    
    iRet = APP_RET_CODE_SUCESS
    g_lock_print.acquire()
    try:

        # 仅上报服务器 
        if "####" in text:
            iRet = http_report_log(text)
            pass
        else:
            # chenyj test
            #    让更多的日志上报服务器端
            iRet = http_report_log(text)
            if iRet == APP_RET_CODE_SERVER_ERRE:
                if g_table_object != None:
                    g_table_object.signal_of_table.emit("log_{}".format("!!!!服务器日志服务失败"))
            elif iRet == APP_RET_CODE_NET_ERROR:
                if g_table_object != None:
                    g_table_object.signal_of_table.emit("log_{}".format("!!!!请确保本机可以访问互联网7"))
            """    
            if "!!" in text or ("动作" in text and "【" in text):
                iRet = http_report_log(text)
                if iRet == APP_RET_CODE_SERVER_ERRE:
                    if g_table_object != None:
                        g_table_object.signal_of_table.emit("log_{}".format("!!!!服务器日志服务失败"))
                elif iRet == APP_RET_CODE_NET_ERROR:
                    if g_table_object != None:
                        g_table_object.signal_of_table.emit("log_{}".format("!!!!请确保本机可以访问互联网7"))
            """        
            if g_table_object != None:
                g_table_object.signal_of_table.emit("log_{}".format(text))
        print(text)
    finally:
        g_lock_print.release()
    return iRet