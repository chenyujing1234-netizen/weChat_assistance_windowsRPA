# -*- coding: utf-8 -*-

import requests
import json
from log_helper import print_my
from app_info import * 
from error_code import *
from time_helper import TIME_BEGIN, TIME_END

############################### 百度 ############################################
# 讲笑话智能体
#APP_ID = "DAKOunU01uI7K6SlwViwrjGCHdt9D57n"
#SECRET_KEY= "sE0UvgWlJkHEm9SvFjD0axIlxJJnghDJ"
# 电商的智能客服智能体
APP_ID = "3dIyf1ob7TapDje9tHezK8D9cyo5wvz1"
SECRET_KEY= "TinVx6se5197MhUQHS9DCcmadrzsiQC4"

g_host_url = 'https://agentapi.baidu.com/assistant/getAnswer?appId={}&secretKey={}'.format(APP_ID, SECRET_KEY)
TIME_OUT = 40

def agent_get_result_from_baidu(username = "", agent_name="", history=[], msg_send = "", str_mac = ""):
    msg_return = ""
    
    request_url = g_host_url
    headers = {'content-type': 'application/json'}
    
    TIME_BEGIN()
    try:
        data_dict = {}
        message_dict = {}
        content_dict = {}
        content_dict["type"] = "text"
        content_dict["value"] = {"showText": msg_send}
        message_dict["content"] = content_dict
        data_dict["message"] = message_dict 
        data_dict["source"] = APP_ID
        data_dict["from"] = "openapi" 
        # openId:外部用户ID（串联对话上下文使用，可自行定义，需要保证唯一性）
        # 接入方需要为每位使用接入方服务的用户生成唯一 ID 具体要求如下：
        #• 唯一性：每个用户具有唯一的 ID,不同用户的 ID 不能相同
        #• 格式：可以是数字或者字符串（数字、下划线、大小写字母），字符串的长度 <= 100字符
        #• 可追溯：每个用户 ID，接入方可以追溯到用户
        data_dict["openId"] = "{}_{}_{}".format(CLIENT_NAME, str_mac, username)

        # 将字典转换为JSON字符串
        json_data = json.dumps(data_dict)
        # chenyj debug
        #print(json_data)
        print_my("动作:【请求agent】文本是:{}".format(msg_send))

        response = requests.post(request_url, data=json_data, headers=headers, timeout=TIME_OUT)
    except Exception as e:
        print_my("!!!!!agent_get_result_from_baidu, 出现异常，\n Exception: {}".format(e))
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
    if response:
        try:
            json_return = response.json()
            # chenyj debug
            #print(json_return)
            
        except Exception as e:
            print_my("!!!!!agent_get_result_from_baidu, 出现异常，response:{}. \n Exception: {}".format(response, e))
            TIME_END()
            return APP_RET_CODE_NET_ERROR, msg_return
        if json_return["status"] == 0:
            TIME_END()
            msg_return = json_return["data"]["content"][0]["data"]
            return RET_SUCESS, msg_return
        else:
            print_my("!!!!!请求文心智能体返回错误，json_return:{}.".format(json_return))
            TIME_END()
            return APP_RET_CODE_NET_ERROR, msg_return
    TIME_END()
    print("agent_get_result_from_baidu, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
#agent_get_result_from_baidu("", [], "你好")

############################### 讯飞星火 ############################################
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
# 1.1 请求地址
#    Tips: 星火大模型API当前有Lite、V2.0、Pro、Pro-128K、Max和4.0 Ultra六个版本，各版本独立计量tokens。
#    传输协议 ：ws(s),为提高安全性，强烈推荐wss
# 电商客服
#SPARKAI_URL = 'wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/cnkthyxctjw1_v1'

#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
# 知识问答小助手
SPARKAI_URL = 'wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/nd4apv6k2opk_v1'
SPARKAI_APP_ID = 'YOUR_SPARKAI_APP_ID'
SPARKAI_API_SECRET = 'YOUR_SPARKAI_API_SECRET'
SPARKAI_API_KEY = 'YOUR_SPARKAI_API_KEY'
# 讲笑话智能体
"""
SPARKAI_URL = 'wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/tpwb4a9aun2w_v1'
SPARKAI_APP_ID = 'YOUR_SPARKAI_APP_ID'
SPARKAI_API_SECRET = 'YOUR_SPARKAI_API_SECRET'
SPARKAI_API_KEY = 'YOUR_SPARKAI_API_KEY'
"""

AGENT_INFO_DICT = [
                    {"name":"星火百科常识智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/nd4apv6k2opk_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    },
                    {"name":"星火讲笑话智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/tpwb4a9aun2w_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    },
                    {"name":"星火电影剧情大师智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/1zkho8kcym7d_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    },
                    {"name":"星火广告语创意达人智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/qre95injanq7_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    },
                    {"name":"星火小红书种草文案助手智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/ufk14hjgo8p2_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    },
                    {"name":"星火高考志愿助手智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/pscr56x6i388_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    },
                    {"name":"星火商业文案智能体", 
                    "SPARKAI_URL":"wss://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/xb4dkk1qy49f_v1", 
                    "SPARKAI_APP_ID":"YOUR_SPARKAI_APP_ID", 
                    "SPARKAI_API_SECRET":"YOUR_SPARKAI_API_SECRET", 
                    "SPARKAI_API_KEY":"YOUR_SPARKAI_API_KEY" 
                    }
                    ]
 
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

# 要去看下：
# https://www.xfyun.cn/doc/spark/Web.html#%E5%BF%AB%E9%80%9F%E8%B0%83%E7%94%A8%E9%9B%86%E6%88%90%E6%98%9F%E7%81%AB%E8%AE%A4%E7%9F%A5%E5%A4%A7%E6%A8%A1%E5%9E%8B%EF%BC%88python%E7%A4%BA%E4%BE%8B%EF%BC%89
# https://www.xfyun.cn/doc/spark/SparkAssistantAPI.html#_3-%E8%AF%B7%E6%B1%82
def agent_get_result_from_xing_huo(username = "", agent_name="", history=[], msg_send = "", str_mac = ""):
    msg_return = ""
    sparkai_url = ""
    sparkai_app_id = ""
    sparkai_api_secret = ""
    sparkai_api_key = ""
    
    for agent_info in AGENT_INFO_DICT:
        if agent_info["name"] == agent_name:
            sparkai_url = agent_info["SPARKAI_URL"]
            sparkai_app_id = agent_info["SPARKAI_APP_ID"]
            sparkai_api_secret = agent_info["SPARKAI_API_SECRET"]
            sparkai_api_key = agent_info["SPARKAI_API_KEY"]
            break 
    if len(sparkai_url) == 0 or len(sparkai_app_id) == 0 and len(sparkai_api_secret) == 0 and len(sparkai_api_key) == 0:   
        print("agent_get_result_from_xing_huo, agent info is wrong\nsparkai_url:{}\nsparkai_app_id:{}\nsparkai_api_secret:{}\nsparkai_api_key:{}".format(sparkai_url, sparkai_app_id, sparkai_api_secret, sparkai_api_key))
        return APP_RET_CODE_NET_ERROR, msg_return
    
    TIME_BEGIN()
    try:
        print_my("动作:【请求{}agent】文本是:{}".format(agent_name, msg_send))
        spark = ChatSparkLLM(
            spark_api_url=sparkai_url,
            spark_app_id=sparkai_app_id,
            spark_api_key=sparkai_api_key,
            spark_api_secret=sparkai_api_secret,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )
        messages = [ChatMessage(
            role="user",
            content=msg_send
        )]
        handler = ChunkPrintHandler()
        #llmResult = spark.generate([messages], callbacks=[handler])
        llmResult = spark.generate([messages])
        # chenyj debug
        # 返回值类型:<class 'sparkai.core.outputs.llm_result.LLMResult'>,   
        #  返回值:generations=[[ChatGeneration(text='如果您的订单还未发货，您可以在订单管理页面直接取消。如果已经发货，请联系客服协助处理。', message=AIMessage(content='如果您的订单还未发货，您可以在订单管理页面直接取消。如果已经发货，请联系客服协助处理。'))]] llm_output={'token_usage': {'question_tokens': 403, 'prompt_tokens': 1255, 'completion_tokens': 23, 'total_tokens': 1278}} run=[RunInfo(run_id=UUID('1cdad34c-b783-4131-92d8-b8b29e56c1c5'))]
        # chenyj debug
        #print("返回值类型:{}, 返回值:{}".format(type(llmResult), llmResult))
        llmResult_json_str = llmResult.json()
        llmResult_json = json.loads(llmResult_json_str)
        # chenyj debug
        #print(type(llmResult_json))
        msg_return = llmResult_json["generations"][0][0]["text"]
        # chenyj debug
        #print(msg_return)
        TIME_END()
        return RET_SUCESS, msg_return
    except Exception as e:
        print_my("!!!!!agent_get_result_from_xing_huo, 出现异常\n Exception: {}".format(e))
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("agent_get_result_from_xing_huo, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
#agent_get_result_from_xing_huo("任小玲", "百科常识智能体", [], "怎么取消订单")
################################################################################################
agent_get_result = agent_get_result_from_xing_huo