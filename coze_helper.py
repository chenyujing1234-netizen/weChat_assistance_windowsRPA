import requests
import json
import time
from log_helper import print_my
from app_info import * 
from error_code import *

COZE_FRON_STR = "Coze智能体_"
COZE_BASE_URL = "https://api.coze.cn/v3"

# Coze图片生成智能体的 API 配置
BOT_ID_OF_IMAGE_GEN_AGENT = "7434185029179654163"
API_TOKEN_OF_IMAGE_GEN_AGENT = "pat_poawkwTAR9NMqrxCc4m5Msv6e4eaIfLpvl0KXB4qHS3U3278r0ehkQnTP5vF89ak"
# Coze电商智能客服的 API 配置
BOT_ID_OF_DIAN_SHANG_KE_FU_AGENT = "7407699828379074623"
API_TOKEN_OF_DIAN_SHANG_KE_FU_AGENT = "pat_poawkwTAR9NMqrxCc4m5Msv6e4eaIfLpvl0KXB4qHS3U3278r0ehkQnTP5vF89ak"

# 发送Coze请求
def send_coze_chat_request(question, user_id, str_mac, bot_id, api_token):
    url = f"{COZE_BASE_URL}/chat"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "bot_id": bot_id,
        "user_id": str_mac + user_id,  # 可以使用任意用户ID
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": question,
                "content_type": "text"
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 获取Coze聊天回复的消息
def get_coze_chat_messages(chat_id, conversation_id, api_token):
    url = f"{COZE_BASE_URL}/chat/message/list?chat_id={chat_id}&conversation_id={conversation_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

# 请求Coze智能体并得到回答的结果
def llm_get_result_for_coze_for_chat(username = "", history=[], msg_send = "", str_mac = "", bot_id = "", api_token = ""):
    msg_return = ""
    msg_answer = ""
    
    try:
        # 发送聊天请求
        print_my("动作:【请求Coze智能体】文本是:{}".format(msg_send))
        chat_response = send_coze_chat_request(msg_send, username, str_mac, bot_id, api_token)
        print("Chat response:", json.dumps(chat_response, indent=2, ensure_ascii=False))
        
        if "code" in chat_response and chat_response["code"] == 0 and "data" in chat_response:
            chat_id = chat_response["data"].get("id")
            conversation_id = chat_response["data"].get("conversation_id")
            
            if chat_id and conversation_id:
                # 尝试获取聊天消息，最多重试5次
                for attempt in range(6):
                    print(f"Coze智能体尝试获取消息，第 {attempt + 1} 次")
                    messages = get_coze_chat_messages(chat_id, conversation_id, api_token)
                    print("Coze智能体Messages response:", json.dumps(messages, indent=2, ensure_ascii=False))
                    b_is_answer_finish = False
                    if "code" in messages and messages["code"] == 0 and "data" in messages and messages["data"]:
                        for message in messages["data"]:
                            if message["role"] == "assistant":
                                if message["type"] == "answer":
                                    content = message["content"]
                                    print(f"Coze智能体的回答：{content}")
                                    msg_answer += content
                                    continue
                                elif message["type"] == "verbose":
                                    content = message["content"]
                                    try:    
                                        content_json = json.loads(content)
                                        msg_type = content_json["msg_type"]
                                        if "generate_answer_finish" == msg_type:
                                            print_my("Coze智能体收到回答完成标志")
                                            b_is_answer_finish = True
                                            break
                                    except Exception:
                                        print_my("!!!收到verbose标识，但不是json格式")
                                        continue
                                #return RET_SUCESS, msg_return
                    else:
                        print("Coze智能体获取聊天消息失败或返回格式不正确，等待5秒后重试")
                        
                    if b_is_answer_finish == True:
                        break
                    
                    time.sleep(5)  
                    continue
                    
                if len(msg_answer) > 0:
                    print_my("Coze智能体的回答：{}".format(msg_answer))
                    msg_return = msg_answer
                    return RET_SUCESS, msg_return
                else:
                    print_my("所有重试都失败，无法获取智能体的回答")
                    return APP_RET_CODE_NET_ERROR, msg_return
            else:
                print_my("!!!!Coze智能体的chat_id 或 conversation_id 未在响应中找到")
                return APP_RET_CODE_NET_ERROR, msg_return
        else:
            print_my("!!!发送Coze智能体请求失败或返回格式不正确")
            return APP_RET_CODE_NET_ERROR, msg_return
    except Exception as e:
        print_my("!!!!!发送Coze智能体请求, 出现异常\n Exception: {}".format(e))
        return APP_RET_CODE_NET_ERROR, msg_return
    return APP_RET_CODE_NET_ERROR, msg_return
# 测试Coze图片生成智能体
#llm_get_result_for_coze_for_chat("123456", [], "一只地板上的鱼", "", BOT_ID_OF_IMAGE_GEN_AGENT, API_TOKEN_OF_IMAGE_GEN_AGENT)
# 测试Coze电商智能客服
#llm_get_result_for_coze_for_chat("test", [], "你好", "", BOT_ID_OF_DIAN_SHANG_KE_FU_AGENT, API_TOKEN_OF_DIAN_SHANG_KE_FU_AGENT)

# 检查扣子智能体是否可用
def check_is_coze_agent_availed(coze_agent_info):
    msg_return = ""
        
    bot_id = ""
    if "bot_id" in coze_agent_info:
        bot_id = coze_agent_info["bot_id"]
    api_token = ""
    if "api_token" in coze_agent_info:
        api_token = coze_agent_info["api_token"]
        
    if len(bot_id) == 0 or len(api_token) == 0:
        return False, msg_return
    
    chat_response = send_coze_chat_request("你好", "user_test_12345", "mac_111", bot_id, api_token)
    print("check_is_coze_agent_availed, Chat response:", json.dumps(chat_response, indent=2, ensure_ascii=False))
        
    if "code" in chat_response and chat_response["code"] == 0 and "data" in chat_response:
        chat_id = chat_response["data"].get("id")
        conversation_id = chat_response["data"].get("conversation_id")
        
        if chat_id and conversation_id:
            return True, msg_return
    if "msg" in chat_response:
        msg_return = chat_response["msg"]
        
    return False, msg_return