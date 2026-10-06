from __future__ import annotations
from character_base_character_template import BaseCharacterTemplate
from character_template_zh import ChineseCharacterTemplate
from character import Character
from character_aili_zh import aili_zh
from character_datatime_utils import get_current_time_str
import sys
import os
# 添加上一级目录到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_helper import llm_get_result_from_kimi
from log_helper import print_my
from app_info import * 
from error_code import *
from time_helper import TIME_BEGIN, TIME_END

def init_character():
    character = None

    character = aili_zh
    character_template_dict: dict[str, BaseCharacterTemplate] = {}
    character_template_dict["zh"] = ChineseCharacterTemplate()
    character_template = character_template_dict[
                character.custom_role_template_type]      
    # 第1次得到prompt
    output_prompt = character_template.format(character)
    return output_prompt
    
g_output_prompt = init_character()



def llm_get_result_from_character(username = "", history=[], msg_send = "", str_mac = ""):
    """
    history . eg: [{"role":"user", "content":"你好"}, {"role":"assistant", "content":"很高兴认识你"}]
    """
    msg_return = ""
    
    try:
        messages_str = ""
        for i, msg in enumerate(reversed(history)):
            rol_str = ""
            if msg["role"] == "assistant":
                rol_str = "爱莉"
            else:
                rol_str = "问"
                
            # 跳过最后一条是对方问的
            if i == len(history) - 1 and rol_str == "问":
                break 
                
            content = msg["content"]
            msg_str = ""
            #msg_str = "\n第{}轮\n{}:{}".format(i, rol_str, content)
            if i != 0:
                msg_str += "\n"
            msg_str += "{}:{}".format(rol_str, content)
            messages_str += msg_str
        
        you_name = "222"
        long_history = messages_str
        current_time = get_current_time_str()
        system_prompt = g_output_prompt.format(
            you_name=you_name, long_history=long_history, current_time=current_time)
        #print("llm_get_result_from_character, 得到的proimpt是:{}".format(system_prompt))
        
        iRet, msg_return = llm_get_result_from_kimi(username, [], msg_send, str_mac, system_prompt)

        return iRet, msg_return
    except Exception as e:
        print_my("!!!!!llm_get_result_from_character, 出现异常\n Exception: {}".format(e))
        except_str = str(e)
        if "The request was rejected" in except_str:
            return APP_RET_CODE_UN_SAFE_QUESTION, msg_return

        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_get_result_from_character, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
    
#llm_get_result_from_character("username", history=[], msg_send = "5555", str_mac = "4444")