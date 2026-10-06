# -*- coding: utf-8 -*-
from pathlib import Path, PurePosixPath
from openai import OpenAI
import json
import re
import requests
from log_helper import print_my
from app_info import * 
from error_code import *
from config_helper import *
from llm_prompt_generate_content_of_ji_huo import prompt_generate_content_of_ji_huo_system, prompt_generate_content_of_ji_huo_user
from llm_prompt_generate_content_of_zhong_cao import prompt_generate_content_of_zhong_cao_system, prompt_generate_content_of_zhong_cao_user
from llm_prompt_generate_content_of_zhi_shi import prompt_generate_content_of_zhi_shi_system, prompt_generate_content_of_zhi_shi_user
from llm_prompt_generate_content_of_zao_si import prompt_generate_content_of_zao_si_system, prompt_generate_content_of_zao_si_user
from llm_prompt_generate_content_of_gen_jin import prompt_generate_content_of_gen_jin_system, prompt_generate_content_of_gen_jin_user
from llm_prompt_generate_content_of_yao_yue import prompt_generate_content_of_yao_yue_system, prompt_generate_content_of_yao_yue_user
from llm_prompt_generate_content_of_fa_shou import prompt_generate_content_of_fa_shou_system, prompt_generate_content_of_fa_shou_user
from llm_prompt_generate_content_of_jiao_fu import prompt_generate_content_of_jiao_fu_system, prompt_generate_content_of_jiao_fu_user
from llm_prompt_generate_content_of_fu_gou import prompt_generate_content_of_fu_gou_system, prompt_generate_content_of_fu_gou_user
from llm_prompt_generate_pos_neg import prompt_generate_pos_neg_system, prompt_generate_pos_neg_user
from time_helper import TIME_BEGIN, TIME_END
from http import HTTPStatus
from urllib.parse import urlparse, unquote
# pip install zhipuai -i https://pypi.tuna.tsinghua.edu.cn/simple
from zhipuai import ZhipuAI
# pip install dashcope -i https://pypi.tuna.tsinghua.edu.cn/simple
from dashscope import ImageSynthesis
import os
import traceback

G_KEY_DEFAULT = "公共key"
####################################### Kimi ####################################
#"""
MODEL_OF_KIMI_DEFAULT = "moonshot-v1-8k"
G_MODEL_OF_KIMI = MODEL_OF_KIMI_DEFAULT
#model="moonshot-v1-32k"
#model="moonshot-v1-128k"
KEY_OF_KIMI_DEFAULT = "YOUR_KIMI_API_KEY"
G_KEY_OF_KIMI = KEY_OF_KIMI_DEFAULT
G_CLIENT_OF_KIMI = OpenAI(
    api_key = G_KEY_OF_KIMI,
    base_url = "https://api.moonshot.cn/v1",
)
#"""
####################################### Qwen-qwq-plus ####################################
MODEL_OF_QWEN_QWQ_PLUS_DEFAULT = "qwq-32b"
G_MODEL_OF_QWEN_QWQ_PLUS = MODEL_OF_QWEN_QWQ_PLUS_DEFAULT
# 初始化OpenAI客户端
KEY_OF_QWEN_PLUS_DEFAULT = "YOUR_QWEN_API_KEY"
G_KEY_OF_QWEN_PLUS = KEY_OF_QWEN_PLUS_DEFAULT
G_CLIENT_OF_QWEN_QWQ_PLUS = OpenAI(
    api_key = G_KEY_OF_QWEN_PLUS,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
####################################### Qwen-deepseek-r1 ####################################
MODEL_OF_QWEN_DEEPSEEK_R1_DEFAULT = "deepseek-r1"
G_MODEL_OF_QWEN_DEEPSEEK_R1 = MODEL_OF_QWEN_DEEPSEEK_R1_DEFAULT
KEY_OF_QWEN_DEEPSEEK_R1_DEFAULT = "YOUR_QWEN_API_KEY"
G_KEY_OF_QWEN_DEEPSEEK_R1 = KEY_OF_QWEN_DEEPSEEK_R1_DEFAULT
# 初始化OpenAI客户端
G_CLIENT_OF_QWEN_DEEPSEEK_R1 = OpenAI(
    api_key = G_KEY_OF_QWEN_DEEPSEEK_R1,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
####################################### GLM ####################################
MODEL_OF_GLM_DEFAULT = "glm-4-plus"
G_MODEL_OF_GLM = MODEL_OF_GLM_DEFAULT
KEY_OF_GLM_DEFAULT = "YOUR_GLM_API_KEY"
G_KEY_OF_GLM = KEY_OF_GLM_DEFAULT
G_CLIENT_OF_GLM = ZhipuAI(api_key=G_KEY_OF_GLM)  
####################################### 豆包 ####################################
# 豆包
#key = "YOUR_DOU_BAO_API_KEY"
MODEL_OF_DOU_BAO_DEFAULT = "ep-20250212214953-c6xps"
G_MODEL_OF_DOU_BAO = MODEL_OF_DOU_BAO_DEFAULT
url_dou_bao = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
KEY_OF_DOU_BAO_DEFAULT = "Bearer YOUR_DOU_BAO_API_KEY"
G_KEY_OF_DOU_BAO = KEY_OF_DOU_BAO_DEFAULT
G_HEADERS_DOU_BAO = {
    "Content-Type": "application/json",
    "Authorization": G_KEY_OF_DOU_BAO
}
"""
curl https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_DOU_BAO_API_KEY" \
  -d '{
    "model": "ep-20250212214953-c6xps",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "帮我写一首诗"
        }
    ]
  }'
"""
####################################### deepseek-V3官网 ####################################
# DeepSeek-V3
MODEL_OF_DEEPSEEK_V3_GUAN_WANG_DEFAULT ="deepseek-chat"
G_MODEL_OF_DEEPSEEK_V3_GUAN_WANG = MODEL_OF_DEEPSEEK_V3_GUAN_WANG_DEFAULT
KEY_OF_DEEPSEEK_V3_DEFAULT = "YOUR_DEEPSEEK_API_KEY"
G_KEY_OF_DEEPSEEK_V3 = KEY_OF_DEEPSEEK_V3_DEFAULT
G_CLIENT_OF_DEEPSEEK_V3_GUAN_WANG = OpenAI(
    api_key = G_KEY_OF_DEEPSEEK_V3,
    base_url = "https://api.deepseek.com",
)
####################################### deepseek-R1官网 ####################################
# DeepSeek-R1
MODEL_OF_DEEPSEEK_GUAN_WANG_DEFAULT ="deepseek-reasoner"
G_MODEL_OF_DEEPSEEK_GUAN_WANG = MODEL_OF_DEEPSEEK_GUAN_WANG_DEFAULT
KEY_OF_DEEPSEEK_GUAN_WANG_DEFAULT = "YOUR_DEEPSEEK_API_KEY"
G_KEY_OF_DEEPSEEK_GUAN_WANG = KEY_OF_DEEPSEEK_GUAN_WANG_DEFAULT
G_CLIENT_OF_DEEPSEEK_GUAN_WANG = OpenAI(
    api_key = G_KEY_OF_DEEPSEEK_GUAN_WANG,
    base_url = "https://api.deepseek.com",
)
####################################### 无问芯穹deepseek-R1####################################
MODEL_OF_DEEPSEEK_INFINI_DEFAULT = "deepseek-r1"
G_MODEL_OF_DEEPSEEK_INFINI = MODEL_OF_DEEPSEEK_INFINI_DEFAULT
KEY_OF_DEEPSEEK_INFINI_DEFAULT = "YOUR_INFINI_API_KEY"
G_KEY_OF_DEEPSEEK_INFINI = KEY_OF_DEEPSEEK_INFINI_DEFAULT
G_CLIENT_OF_DEEPSEEK_INFINI = OpenAI(
    api_key = G_KEY_OF_DEEPSEEK_INFINI,
    base_url = "https://cloud.infini-ai.com/maas/v1",
)
####################################### 无问芯穹deepseek-r1-distill-qwen-32b####################################
G_MODEL_DEEPSEEK_R1_DISTILL_QWEN_32B_INFINI = "deepseek-r1-distill-qwen-32b"

G_CLIENT_OF_DEEPSEEK_R1_DISTILL_QWEN_32B_INFINI = OpenAI(
    api_key = "YOUR_INFINI_API_KEY",
    base_url = "https://cloud.infini-ai.com/maas/v1",
)
####################################### 硅基流动deepseek-R1 #################################### 
G_MODEL_OF_DEEPSEEK_SILICON = "deepseek-ai/DeepSeek-V3"
url_deepseek_silicon = "https://api.siliconflow.cn/v1/chat/completions"
headers_deepseek_silicon = {
    "Authorization": "YOUR_SILICONFLOW_API_KEY",
    "Content-Type": "application/json"
}
##################################################################################
# 获得默认的大模型信息列表
def get_default_llm_info_list():
    llm_info_list = []
 
    for llm_type in LLM_MODEL_TYPE_NAME_DICT:
        llm_info = {}
        llm_info["llm_type"] = llm_type.name
        llm_info["llm_type_name"] = LLM_MODEL_TYPE_NAME_DICT[llm_type]
        llm_info["key"] = G_KEY_DEFAULT
        if llm_type == LLM_MODEL_TYPE.DeepSeek_R1_GuanWang:
            llm_info["model_name"] = MODEL_OF_DEEPSEEK_GUAN_WANG_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.Qwen_Deepseek_R1:
            llm_info["model_name"] = MODEL_OF_QWEN_DEEPSEEK_R1_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.DeepSeek_V3_GuanWang:
            llm_info["model_name"] = MODEL_OF_DEEPSEEK_V3_GUAN_WANG_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.DeepSeek_R1_Distill_32b_Infini:
            llm_info["model_name"] = MODEL_OF_DEEPSEEK_INFINI_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.Kimi:
            llm_info["model_name"] = MODEL_OF_KIMI_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.DouBao:
            llm_info["model_name"] = MODEL_OF_DOU_BAO_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.Qwen_Qwq_Plus:
            llm_info["model_name"] = MODEL_OF_QWEN_QWQ_PLUS_DEFAULT
        elif llm_type == LLM_MODEL_TYPE.GLM:
            llm_info["model_name"] = MODEL_OF_GLM_DEFAULT
        else:
            print("!!!!!get_default_llm_info_list,这种类型:{}没有找到".format(llm_type))
            continue
        llm_info_list.append(llm_info)

    return llm_info_list

# 设置LLM的配置
def set_llm_info(llm_info):
    llm_info_before = {}
    
    global G_MODEL_OF_DEEPSEEK_GUAN_WANG
    global G_KEY_OF_DEEPSEEK_GUAN_WANG
    global G_CLIENT_OF_DEEPSEEK_GUAN_WANG
    
    global G_MODEL_OF_QWEN_DEEPSEEK_R1
    global G_KEY_OF_QWEN_DEEPSEEK_R1
    global G_CLIENT_OF_QWEN_DEEPSEEK_R1
    
    global G_MODEL_OF_DEEPSEEK_V3_GUAN_WANG
    global G_KEY_OF_DEEPSEEK_V3
    global G_CLIENT_OF_DEEPSEEK_V3_GUAN_WANG
    
    global G_MODEL_OF_DEEPSEEK_INFINI
    global G_KEY_OF_DEEPSEEK_INFINI
    global G_CLIENT_OF_DEEPSEEK_INFINI
    
    global G_MODEL_OF_KIMI
    global G_KEY_OF_KIMI
    global G_CLIENT_OF_KIMI
    
    global G_MODEL_OF_DOU_BAO
    global G_KEY_OF_DOU_BAO
    global G_HEADERS_DOU_BAO
    
    global G_MODEL_OF_QWEN_QWQ_PLUS
    global G_KEY_OF_QWEN_PLUS
    global G_CLIENT_OF_QWEN_QWQ_PLUS
    
    global G_MODEL_OF_GLM
    global G_KEY_OF_GLM
    global G_CLIENT_OF_GLM
    
    llm_type = llm_info["llm_type"]
    key = llm_info["key"]
    model_name = llm_info["model_name"]

    llm_info_before["llm_type"] = llm_type
    if llm_type == LLM_MODEL_TYPE.DeepSeek_R1_GuanWang.name:
        llm_info_before["model_name"] = G_MODEL_OF_DEEPSEEK_GUAN_WANG
        llm_info_before["key"] = G_KEY_OF_DEEPSEEK_GUAN_WANG

        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_DEEPSEEK_GUAN_WANG_DEFAULT
            key = KEY_OF_DEEPSEEK_GUAN_WANG_DEFAULT
        G_MODEL_OF_DEEPSEEK_GUAN_WANG = model_name
        G_KEY_OF_DEEPSEEK_GUAN_WANG = key
        G_CLIENT_OF_DEEPSEEK_GUAN_WANG = OpenAI(
            api_key = G_KEY_OF_DEEPSEEK_GUAN_WANG,
            base_url = "https://api.deepseek.com",
        )
    elif llm_type == LLM_MODEL_TYPE.Qwen_Deepseek_R1.name:
        llm_info_before["model_name"] = G_MODEL_OF_QWEN_DEEPSEEK_R1
        llm_info_before["key"] = G_KEY_OF_QWEN_DEEPSEEK_R1
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_QWEN_DEEPSEEK_R1_DEFAULT
            key = KEY_OF_QWEN_DEEPSEEK_R1_DEFAULT
        G_MODEL_OF_QWEN_DEEPSEEK_R1 = model_name
        G_KEY_OF_QWEN_DEEPSEEK_R1 = key
        G_CLIENT_OF_QWEN_DEEPSEEK_R1 = OpenAI(
            api_key = G_KEY_OF_QWEN_DEEPSEEK_R1,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    elif llm_type == LLM_MODEL_TYPE.DeepSeek_V3_GuanWang.name:
        llm_info_before["model_name"] = G_MODEL_OF_DEEPSEEK_V3_GUAN_WANG
        llm_info_before["key"] = G_KEY_OF_DEEPSEEK_V3
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_DEEPSEEK_V3_GUAN_WANG_DEFAULT
            key = KEY_OF_DEEPSEEK_V3_DEFAULT
        G_MODEL_OF_DEEPSEEK_V3_GUAN_WANG = model_name
        G_KEY_OF_DEEPSEEK_V3 = key
        G_CLIENT_OF_DEEPSEEK_V3_GUAN_WANG = OpenAI(
            api_key = G_KEY_OF_DEEPSEEK_V3,
            base_url = "https://api.deepseek.com",
        )
    elif llm_type == LLM_MODEL_TYPE.DeepSeek_R1_Distill_32b_Infini.name:
        llm_info_before["model_name"] = G_MODEL_OF_DEEPSEEK_INFINI
        llm_info_before["key"] = G_KEY_OF_DEEPSEEK_INFINI
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_DEEPSEEK_INFINI_DEFAULT
            key = KEY_OF_DEEPSEEK_INFINI_DEFAULT
        G_MODEL_OF_DEEPSEEK_INFINI = model_name
        G_KEY_OF_DEEPSEEK_INFINI = key
        G_CLIENT_OF_DEEPSEEK_INFINI = OpenAI(
            api_key = G_KEY_OF_DEEPSEEK_INFINI,
            base_url = "https://cloud.infini-ai.com/maas/v1",
        )
    elif llm_type == LLM_MODEL_TYPE.Kimi.name:
        llm_info_before["model_name"] = G_MODEL_OF_KIMI
        llm_info_before["key"] = G_KEY_OF_KIMI
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_KIMI_DEFAULT
            key = KEY_OF_KIMI_DEFAULT
        G_MODEL_OF_KIMI = model_name
        G_KEY_OF_KIMI = key
        G_CLIENT_OF_KIMI = OpenAI(
            api_key = G_KEY_OF_KIMI,
            base_url = "https://api.moonshot.cn/v1",
        )
    elif llm_type == LLM_MODEL_TYPE.DouBao.name:
        llm_info_before["model_name"] = G_MODEL_OF_DOU_BAO
        llm_info_before["key"] = G_KEY_OF_DOU_BAO
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_DOU_BAO_DEFAULT
            key = KEY_OF_DOU_BAO_DEFAULT
        G_MODEL_OF_DOU_BAO = model_name
        G_KEY_OF_DOU_BAO = key
        G_HEADERS_DOU_BAO = {
            "Content-Type": "application/json",
            "Authorization": G_KEY_OF_DOU_BAO
        }
    elif llm_type == LLM_MODEL_TYPE.Qwen_Qwq_Plus.name:
        llm_info_before["model_name"] = G_MODEL_OF_QWEN_QWQ_PLUS
        llm_info_before["key"] = G_KEY_OF_QWEN_PLUS
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_QWEN_QWQ_PLUS_DEFAULT
            key = KEY_OF_QWEN_PLUS_DEFAULT
        G_MODEL_OF_QWEN_QWQ_PLUS = model_name
        G_KEY_OF_QWEN_PLUS = key
        G_CLIENT_OF_QWEN_QWQ_PLUS = OpenAI(
            api_key = G_KEY_OF_QWEN_PLUS,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    elif llm_type == LLM_MODEL_TYPE.GLM.name:
        llm_info_before["model_name"] = G_MODEL_OF_GLM
        llm_info_before["key"] = G_KEY_OF_GLM
        if key == G_KEY_DEFAULT:
            model_name = MODEL_OF_GLM_DEFAULT
            key = KEY_OF_GLM_DEFAULT
        G_MODEL_OF_GLM = model_name
        G_KEY_OF_GLM = key
        G_CLIENT_OF_GLM = ZhipuAI(api_key=G_KEY_OF_GLM)  
    else:
        print("do_reload_llm_info,没找到此这类型:{}".format(llm_type.name))
        return False, llm_info_before
    return True, llm_info_before 

# 检查LLM是否可用
def check_is_llm_availed(llm_info):
    llm_type = llm_info["llm_type"]
    key = llm_info["key"]
    model_name = llm_info["model_name"]
    if len(llm_type) == 0 or len(key) == 0 or len(model_name) == 0:
        print(f"入参不合法.{llm_info}")
        return False
    llm_type_enum_select = None
    
    for llm_type_enum in LLM_MODEL_TYPE_NAME_DICT:
        if llm_type_enum.name == llm_type:
            llm_type_enum_select = llm_type_enum
            break
    if llm_type_enum_select is None:
        print(f"入参不合法.{llm_info}")
        return False
    if key == G_KEY_DEFAULT:
        return True
    
    # 设置
    bRet, llm_info_befor = set_llm_info(llm_info)
    # 调用
    messages = [
                {
                    "role":"system",
                    "content":"You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "你好",
                }
            ]
    iRet, msg_return = llm_get_result_content(messages, llm_type_enum_select) 
    if iRet != RET_SUCESS:
        bRet, _ = set_llm_info(llm_info_befor)
        return False
    # 还原
    bRet, _ = set_llm_info(llm_info_befor)
    return True
    
# 重新加载大模型信息
def do_reload_llm_info():
    global g_config_path

    config_json_data = load_config_data(g_config_path)
    if "LLM_INFO_LIST" not in config_json_data:
        return
    llm_info_list = config_json_data["LLM_INFO_LIST"]
    for llm_info in llm_info_list:
        set_llm_info(llm_info)
    return 
##################################################################################
############################### 知识库 ##########################################
g_knowledage_str = ""
'''
g_knowledage_str = """
  - 用户问：“这款笔记本电脑的内存是多少？”
    回答：“这款笔记本电脑的内存是16GB。”
  - 用户问：“我昨天下的订单，什么时候能发货？”
    回答：“您的订单将在24小时内发货。”
  - 用户问：“你们接受哪些支付方式？”
    回答：“我们接受信用卡、借记卡、支付宝和微信支付。”
  - 用户问：“我如何申请退货？”
    回答：“您可以在订单详情页申请退货，按照页面提示操作即可。”
  - 用户问：“你们有实体店吗？”
    回答：“回答不了。”
"""
'''

# 初始化知识库
def init_knowledage_str(hua_su_file_paths = []):
    global g_knowledage_str
    
    g_knowledage_str = ""
    for hua_su_file_path in hua_su_file_paths:
        try:
            with open(hua_su_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # chenyj debug 
                    #print(line.strip())  
                    g_knowledage_str += line
        except FileNotFoundError:
            print("文件{}未找到，请检查文件路径是否正确".format(hua_su_file_path))
        except Exception as e:
            print("读取文件{}时发生错误:\n {}".format(hua_su_file_path, e))
    # chenyj debug 
    #print("init_knowledage_str, 得到的知识库串是:\n{}".format(g_knowledage_str))
    
    return APP_RET_CODE_SUCESS
    
############################### kimi电商客服自定义话术############################################
SYSTEM_OF_PROMPT_FOR_RAG = """
- Role: 电商领域的智能客服专家
- Background: 用户在电商平台上寻求帮助，需要快速、准确的回答关于商品、订单、支付、退换货等方面的问题。
- Profile: 你是一位专注于电商领域的智能客服，拥有丰富的产品知识和客户服务经验，能够理解并解决客户的各种疑问。
- Skills: 你具备高效的信息检索能力、准确的语言表达能力以及良好的问题解决技巧，能够快速从知识库中找到答案并提供给用户。
- Goals: 为用户提供及时、准确的帮助，提升用户满意度和购物体验。
- Constrains: 
  1. 只能根据提供的知识库回答问题，对于知识库中没有的信息，即使是常识，也应直接告知用户“回答不了”，无需多言。
  2. 如果你选中的示例中的回答有表达“发送图片路径”的意图，那么要求你原封不动地把示例中的回答返回即可
  3. 你的回答要参考历史对话，但不要拿历史对话中的回答直接来回复
  4. 不需要指出你参考了什么内容
- OutputFormat: 清晰、简洁、礼貌的回答，必要时提供进一步的帮助或引导。
- Workflow:
  1. 接收并分析客户的问题。
  2. 在知识库中检索与“客户问题”相似的问题。
  3. 如果在知识库中找到与“客户问题”相似的问题，将回答直接提供给用户。
  4. 如果在知识库中没有与“客户问题”相似的问题，即使是常识，也请告知用户“回答不了”，无需多言。
"""
USER_OF_PROMPT_FOR_RAG = """
- 知识库:
  {}
- Initialization: 下面我给出客户的问题，请根据知识库给出严谨的回答或者直接回复"回答不了"。根据提供的知识库谨慎判断，不懂就说“回答不了”，无需多言。
- 客户问题: {}
"""
def llm_get_result_for_local_rag(username = "", history=[], msg_send = "", str_mac = "", model_type=LLM_MODEL_TYPE.GLM):
    global g_knowledage_str
    
    """
    history . eg: [{"role":"user", "content":"你好"}, {"role":"assistant", "content":"很高兴认识你"}]
    """
    msg_return = ""
    
    TIME_BEGIN()
    try:
        print_my("动作:【请求自定义本地话术agent】开始")
        prompt_str = SYSTEM_OF_PROMPT_FOR_RAG
        user_str = USER_OF_PROMPT_FOR_RAG.format(g_knowledage_str, msg_send)
        messages = [
            {
                "role":"system",
                "content":prompt_str,
            }
        ]
        for msg in reversed(history):
            messages.append(msg)  
        user_msg = {
                "role": "user",
                "content": user_str,
            } 
        messages.append(user_msg)  
      
        # 
        iRet, msg_return = llm_get_result_content(messages, model_type)   
        if iRet != RET_SUCESS:
            return iRet, msg_return
        """
        completion = client_of_local_chat.chat.completions.create(
          model=model_local_chat,
          messages=messages,
          temperature=0.1,
          top_p = 0.1
        )
        print("66666")   
        msg_return = completion.choices[0].message.content
        """
        # chenyj debug
        print("回答:\n【\n{}\n】".format(msg_return))
        TIME_END()
        return RET_SUCESS, msg_return
    except Exception as e:
        print_my("!!!!!llm_get_result_for_local_rag, 出现异常\n Exception: {}".format(e))
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_get_result_for_local_rag, return error")
    return APP_RET_CODE_NET_ERROR, msg_return

############################### kimi闲聊专家自定义话术############################################
SYSTEM_OF_PROMPT_FOR_RAG_FOR_CHAT = """
- Role: 闲聊智能专家
- Background: 用户希望与智能体进行类似人与人之间自然流畅的对话，智能体需要根据用户提供的“知识库”中的样例来回答问题，如果样例中没有相关答案，则直接回答“回答不了”。
- Profile: 你是一位擅长模仿人类交流方式的智能专家，能够理解并运用语言的连贯性和合理性，同时具备快速检索和匹配知识库信息的能力。
- Skills: 你拥有自然语言处理、上下文理解、知识库检索和匹配等关键能力，能够根据用户的问题和对话内容，提供准确且连贯的回答。
- Goals: 与用户进行流畅、自然的对话，根据知识库中的样例回答问题，保持聊天的连贯性和合理性。
- Constrains: 
  1.回答问题时必须参考知识库中的问答对，如果样例中没有答案，则直接回答“回答不了”，无需多言。
  2.你的回答要参考历史对话，但不要拿历史对话中的回答直接来回复
  3. 不需要指出你参考了什么内容
- OutputFormat: 文字对话形式，保持语言的自然流畅和连贯性。
- Workflow:
  1. 接收并分析对方的问题。
  2. 在知识库中检索与“对方问题”相似的问题。
  3. 如果在知识库中找到与“对方问题”相似的问题，将此相似问题对应的回答提供给对方。
  4. 如果在知识库中没有与“对方问题”相似的问题，即使是常识，也请告知对方“回答不了”，无需多言。
"""
USER_OF_PROMPT_FOR_RAG_FOR_CHAT = """
- 知识库:
  {}
- Initialization: 下面我给出对方的问题，请根据知识库给出严谨的回答或者直接回复"回答不了"。根据提供的知识库谨慎判断，不懂就说“回答不了”，无需多言。
- 对方问题: {} 。
"""
def llm_get_result_for_local_rag_for_chat(username = "", history=[], msg_send = "", str_mac = "", model_type=LLM_MODEL_TYPE.GLM):
    global g_knowledage_str
    
    """
    history . eg: [{"role":"user", "content":"你好"}, {"role":"assistant", "content":"很高兴认识你"}]
    """
    msg_return = ""
    
    TIME_BEGIN()
    try:
        print_my("动作:【请求闲聊自定义本地话术agent】开始")
        prompt_str = SYSTEM_OF_PROMPT_FOR_RAG_FOR_CHAT
        user_str = USER_OF_PROMPT_FOR_RAG_FOR_CHAT.format(g_knowledage_str, msg_send)
        messages = [
            {
                "role":"system",
                "content":prompt_str,
            }
        ]
        for msg in reversed(history):
            messages.append(msg)  
        user_msg = {
                "role": "user",
                "content": user_str,
            } 
        messages.append(user_msg)  
        print("动作:【请求闲聊自定义本地话术agent】messages是:\n")
        for i, mesage_ in enumerate(messages):
            print("【{}】{}".format(i, mesage_))
            
        # 
        iRet, msg_return = llm_get_result_content(messages, model_type)   
        if iRet != RET_SUCESS:
            return iRet, msg_return
        """
        completion = client_of_local_chat.chat.completions.create(
          model=model_local_chat,
          messages=messages,
          temperature=0.1,
          top_p = 0.1
        )
        print("66666")   
        msg_return = completion.choices[0].message.content
        """
        # chenyj debug
        print("回答:\n【\n{}\n】".format(msg_return))
        TIME_END()
        return RET_SUCESS, msg_return
    except Exception as e:
        print_my("!!!!!llm_get_result_for_local_rag_for_chat, 出现异常\n Exception: {}".format(e))
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_get_result_for_local_rag_for_chat, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
# 测试
#init_knowledage_str(["自定义本地话术库_交友.txt"])
#history = [{"role":"user", "content":"函数怎么写"}, {"role":"assistant", "content":"你晚上回来吗"}, {'role': 'assistant', 'content': '要说下，不然我会反锁'}, {'role': 'user', 'content': '有的。'}, {'role': 'user', 'content': '约11点到家'}, {'role': 'assistant', 'content': '工资看下发了没，我要还款'}, {'role': 'user', 'content': '给你转了1.5w'}, {'role': 'user', 'content': '我下面测试'}]
#llm_get_result_for_local_rag_for_chat("任小玲", [], "你多大了")
#llm_get_result_for_local_rag_for_chat("任小玲", [], "你做什么的")
#llm_get_result_for_local_rag_for_chat("任小玲", [], "能给我个照片吗")
#llm_get_result_for_local_rag_for_chat("任小玲", [], "喜欢逛街吗")
#llm_get_result_for_local_rag_for_chat("任小玲", [], "你是干啥的")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "喜欢游戏吗")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "过年回家吗")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "以后工作的打算呢？")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "开始测试")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "出来约会")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "你是什么想法")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "你好")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "骗我")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "我想真诚一些")
#llm_get_result_for_local_rag_for_chat("任小玲", history, "安全措施是指")
###############################################通用kimi回答##################################
SYSTEM_OF_PROMPT = """你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"""
USER_OF_PROMPT = """{}"""
def llm_get_result_from_kimi(username = "", history=[], msg_send = "", str_mac = "", prompt_of_system = ""):
    """
    history . eg: [{"role":"user", "content":"你好"}, {"role":"assistant", "content":"很高兴认识你"}]
    """
    msg_return = ""
    
    TIME_BEGIN()
    try:
        print_my("动作:【请求{}大模型】文本是:{}".format(G_MODEL_OF_KIMI, msg_send))
        if len(prompt_of_system) == 0:
            prompt_of_system = SYSTEM_OF_PROMPT
        else:
            # chenyj debug 
            print("prompt_of_system:\n{}".format(prompt_of_system))
        user_str = USER_OF_PROMPT.format(msg_send)
        messages = [
            {
                "role":"system",
                "content":prompt_of_system,
            }
        ]
        for msg in reversed(history):
            messages.append(msg)  
        user_msg = {
                "role": "user",
                "content": user_str,
            } 
        messages.append(user_msg)  

        # 根据输入长度的总和，选择合适的model
        pass
        
        completion = G_CLIENT_OF_KIMI.chat.completions.create(
          model=G_MODEL_OF_KIMI,
          messages=messages,
          temperature=0.6,
          top_p = 0.1
        )
        #print("66666")   
        msg_return = completion.choices[0].message.content
        # chenyj debug
        print("回答:\n【\n{}\n】".format(msg_return))
        TIME_END()
        return RET_SUCESS, msg_return
    except Exception as e:
        print_my("!!!!!llm_get_result_from_kimi, 出现异常\n Exception: {}".format(e))
        except_str = str(e)
        if "The request was rejected" in except_str:
            return APP_RET_CODE_UN_SAFE_QUESTION, msg_return
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_get_result_from_kimi, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
#llm_get_result_from_kimi("任小玲", [], "怎么订机票")
#################################################################################
def remove_think_tags(text):
    """
    删除字符串中以<think>开头，以</think>结尾的所有文本，包括<think>和</think>标签。
    支持跨行内容。
    
    参数:
        text (str): 输入的字符串。
    
    返回:
        str: 删除指定文本和标签后的字符串。
    """
    # 使用正则表达式匹配<think>和</think>之间的所有内容，并删除标签
    pattern = r'<think>.*?</think>'
    result = re.sub(pattern, '', text, flags=re.DOTALL)  # 添加re.DOTALL标志
    result = result.strip("\n")
    return result
    
# 调用大模型生成回答
def llm_get_result_content(messages, model_type=LLM_MODEL_TYPE.Kimi):
    msg_return = ""
    
    TIME_BEGIN()
    try:
        #print("动作:【请求{}大模型】messages是:{}".format(model_type.name, messages))
        # chenyj debug
        print("动作:【请求{}大模型】".format(model_type.name))
        if len(messages) == 0:
            return APP_RET_CODE_UNVALID_PARAM, msg_return
        model_type_name = model_type
        if model_type in LLM_MODEL_TYPE_NAME_DICT:
            model_type_name = LLM_MODEL_TYPE_NAME_DICT[model_type]
            
        if model_type == LLM_MODEL_TYPE.Kimi:
            completion = G_CLIENT_OF_KIMI.chat.completions.create(
              model=G_MODEL_OF_KIMI,
              messages=messages,
              temperature=0.6,
              top_p = 0.1
            )
            msg_return = completion.choices[0].message.content
        elif model_type == LLM_MODEL_TYPE.GLM:
            completion = G_CLIENT_OF_GLM.chat.completions.create(
              model=G_MODEL_OF_GLM,
              messages=messages,
              temperature=0.6,
              top_p = 0.1
            )
            msg_return = completion.choices[0].message.content 
        elif model_type == LLM_MODEL_TYPE.DouBao:    
            # 豆包
            data = {
                "model": G_MODEL_OF_DOU_BAO,
                "messages": messages
            }
            response = requests.post(url_dou_bao, json=data, headers=G_HEADERS_DOU_BAO)
            response = response.json()
            print(response)
            msg_return = response["choices"][0]["message"]["content"]
        elif model_type == LLM_MODEL_TYPE.DeepSeek_V3_GuanWang:
            completion = G_CLIENT_OF_DEEPSEEK_V3_GUAN_WANG.chat.completions.create(
              model=G_MODEL_OF_DEEPSEEK_V3_GUAN_WANG,
              messages=messages,
              temperature=0.6
            )
            msg_return = completion.choices[0].message.content 
        elif model_type == LLM_MODEL_TYPE.DeepSeek_R1_GuanWang:
            completion = G_CLIENT_OF_DEEPSEEK_GUAN_WANG.chat.completions.create(
              model=G_MODEL_OF_DEEPSEEK_GUAN_WANG,
              messages=messages,
              temperature=0.6
            )
            msg_return = completion.choices[0].message.content 
        elif model_type == LLM_MODEL_TYPE.DeepSeek_R1_Silicon:
            data = {
                "model": G_MODEL_OF_DEEPSEEK_SILICON,
                "messages": messages,
                "stream": False,
                "max_tokens": 512,
                "stop": ["null"],
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"},
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "description": "<string>",
                            "name": "<string>",
                            "parameters": {},
                            "strict": False
                        }
                    }
                ]
            }
            response = requests.request("POST", url_deepseek_silicon, json=data, headers=headers_deepseek_silicon)
            response = response.json()
            msg_return = response["choices"][0]["message"]["content"] 
        elif model_type == LLM_MODEL_TYPE.DeepSeek_R1_Infini:
            completion = G_CLIENT_OF_DEEPSEEK_INFINI.chat.completions.create(
              model=G_MODEL_OF_DEEPSEEK_INFINI,
              messages=messages,
              temperature=0.6,
              top_p = 0.1
            )
            msg_return = completion.choices[0].message.content 
        elif model_type == LLM_MODEL_TYPE.DeepSeek_R1_Distill_32b_Infini:
            completion = G_CLIENT_OF_DEEPSEEK_R1_DISTILL_QWEN_32B_INFINI.chat.completions.create(
              model=G_MODEL_DEEPSEEK_R1_DISTILL_QWEN_32B_INFINI,
              messages=messages,
              temperature=0.6,
              top_p = 0.1
            )
            msg_return = completion.choices[0].message.content 
            msg_return = remove_think_tags(msg_return)
        elif model_type == LLM_MODEL_TYPE.Qwen_Qwq_Plus:
            reasoning_content = ""  # 定义完整思考过程
            answer_content = ""     # 定义完整回复
            is_answering = False   # 判断是否结束思考过程并开始回复
            
            completion = G_CLIENT_OF_QWEN_QWQ_PLUS.chat.completions.create(
              model=G_MODEL_OF_QWEN_QWQ_PLUS,
              messages=messages,
              # QwQ 模型仅支持流式输出方式调用
              stream=True
            )
            #msg_return = completion.choices[0].message.content
            for chunk in completion:
                # 如果chunk.choices为空，则打印usage
                if not chunk.choices:
                    print("\nUsage:")
                    print(chunk.usage)
                else:
                    delta = chunk.choices[0].delta
                    # 打印思考过程
                    if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                        #print(delta.reasoning_content, end='', flush=True)
                        reasoning_content += delta.reasoning_content
                    else:
                        # 开始回复
                        if delta.content != "" and is_answering is False:
                            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                            is_answering = True
                        # 打印回复过程
                        print(delta.content, end='', flush=True)
                        answer_content += delta.content

            #print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
            #print(reasoning_content)
            #print("=" * 20 + "完整回复" + "=" * 20 + "\n")
            #print(answer_content)
            msg_return = answer_content
        elif model_type == LLM_MODEL_TYPE.Qwen_Deepseek_R1:
            completion = G_CLIENT_OF_QWEN_DEEPSEEK_R1.chat.completions.create(
              model=G_MODEL_OF_QWEN_DEEPSEEK_R1,
              messages=messages
            )
            # 通过reasoning_content字段打印思考过程
            print("思考过程：")
            print(completion.choices[0].message.reasoning_content)

            # 通过content字段打印最终答案
            print("最终答案：")
            print(completion.choices[0].message.content)
            
            msg_return = completion.choices[0].message.content
        else:
            return APP_RET_CODE_UNVALID_PARAM, msg_return
        # chenyj debug
        print("【{}大模型】回答:\n【\n{}\n】".format(model_type.name, msg_return))
        TIME_END()
        return RET_SUCESS, msg_return
    except Exception as e:
        print("!!!!!llm_get_result, 出现异常\n Exception: {}".format(e))
        print("崩溃栈:{}".format(traceback.format_exc()))
        print_my("!!!!!大模型【{}】调用时出现异常，请检查网络或使用你自己的key(“设置”->“大模型配置”)".format(model_type_name))
        except_str = str(e)
        if "The request was rejected" in except_str:
            return APP_RET_CODE_UN_SAFE_QUESTION, msg_return
        if "exceeded_current_quot" in except_str:
            return APP_RET_CODE_LLM_API_EXCEEDED, msg_return
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_get_result, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
"""
messages = [
            {
                "role":"system",
                "content":"You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "帮我写一首诗",
            }
        ]
llm_get_result_content(messages, LLM_MODEL_TYPE.GLM)   
"""
############################################### 内容生成 ##################################
def llm_generate_content(agent_type = "", content_product_name = "", product_summary = "", content_examples = "", go_where = "", tong_dian = "", superiority = "", content_count = "", model_type=LLM_MODEL_TYPE.Kimi):
    msg_return = ""
    prompt_generate_content_system = None
    prompt_generate_content_user = None
    
    if agent_type == "种草智能体":
        prompt_generate_content_system = prompt_generate_content_of_zhong_cao_system
        prompt_generate_content_user = prompt_generate_content_of_zhong_cao_user
    elif agent_type == "知识分享智能体":
        prompt_generate_content_system = prompt_generate_content_of_zhi_shi_system
        prompt_generate_content_user = prompt_generate_content_of_zhi_shi_user
    elif agent_type == "激活智能体":
        prompt_generate_content_system = prompt_generate_content_of_ji_huo_system
        prompt_generate_content_user = prompt_generate_content_of_ji_huo_user
    elif agent_type == "造势智能体":
        prompt_generate_content_system = prompt_generate_content_of_zao_si_system  
        prompt_generate_content_user = prompt_generate_content_of_zao_si_user
    elif agent_type == "跟进智能体":
        prompt_generate_content_system = prompt_generate_content_of_gen_jin_system  
        prompt_generate_content_user = prompt_generate_content_of_gen_jin_user
    elif agent_type == "邀约智能体":
        prompt_generate_content_system = prompt_generate_content_of_yao_yue_system  
        prompt_generate_content_user = prompt_generate_content_of_yao_yue_user
    elif agent_type == "发售智能体":
        prompt_generate_content_system = prompt_generate_content_of_fa_shou_system  
        prompt_generate_content_user = prompt_generate_content_of_fa_shou_user
    elif agent_type == "交付智能体":
        prompt_generate_content_system = prompt_generate_content_of_jiao_fu_system  
        prompt_generate_content_user = prompt_generate_content_of_jiao_fu_user
    elif agent_type == "复购智能体":
        prompt_generate_content_system = prompt_generate_content_of_fu_gou_system  
        prompt_generate_content_user = prompt_generate_content_of_fu_gou_user 
    else:
        print("!!!!!!!!!!!!!找不到【{}】对应的prompt".format(agent_type))
        return APP_RET_CODE_UNKNOW, msg_return
    
    TIME_BEGIN()
    try:
        if len(go_where) == 0:
            go_where = "无"
        if len(tong_dian) == 0:
            tong_dian = "无"
        if len(superiority) == 0:
            superiority = "无"
        print_my("动作:【内容生成】开始_{}".format(model_type))
        prompt_of_system = prompt_generate_content_system.format(content_product_name=content_product_name, product_summary=product_summary, content_examples=content_examples, go_where=go_where, tong_dian=tong_dian, superiority=superiority, content_count=content_count)
        print("SYSTEM_PROMPT是:\n{}".format(prompt_of_system))
        prompt_of_user = prompt_generate_content_user.format(content_product_name=content_product_name, content_count=content_count)
        print("USER_PROMPT是:\n{}".format(prompt_of_user))
        messages = [
            {
                "role":"system",
                "content":prompt_of_system,
            }
        ]
        user_msg = {
                "role": "user",
                "content": prompt_of_user,
            } 
        messages.append(user_msg)  

        iRet, msg_return = llm_get_result_content(messages, model_type)   
        if iRet != RET_SUCESS:
            return iRet, msg_return
            
        # 对返回的文本后处理
        msg_return = msg_return.replace("```json", "").replace("```", "")
        
        TIME_END()
        print_my("动作:【内容生成】完成")
        return RET_SUCESS, msg_return
    except Exception as e:
        print_my("!!!!!llm_generate_content, 出现异常\n Exception: {}".format(e))
        except_str = str(e)
        if "The request was rejected" in except_str:
            return APP_RET_CODE_UN_SAFE_QUESTION, msg_return
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_generate_content, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
#
# 测试
''''
content_product_name = "微信私域营销系统"
product_summary = """
这是一款个人微信私域营销工具，这个工具可以帮助各行各业的人（包括：宠物、中医诊所、足疗仪器、机油、工业设备用油、高尿酸产品、编程、中老年、贷款中介、炒股、律师、考研等）做微信客户的维护。
这款产品通过智能体、内容、产品，使客户可以对不同的人，不同的群要配置不同的智能体。可以对特定人，特定群配不同智能体，这个智能体会在指定的时间发送特定的消息。此工具内置的智能体懂人性，将销冠经验复刻。
可以触达的方式包括：个微私聊消息、个微群聊、个微朋友圈 。我们的私聊是做到完全定制，朋友圈也是通过设置可见好友达到，用户看到的内容就是你想让他看的。这点说得明一点，就是给客户制作了信息茧房。脑袋转得快的人，马上就能意识到这个工具的可怕。
每个智能体可以根据不同的产品自动生成产品的内容 。 
"""
content_examples = ""
content_count = "1"
iRet, msg_return = llm_generate_content(content_product_name, product_summary, content_examples, content_count, LLM_MODEL_TYPE.DeepSeek_R1_Infini)
'''
############################################### 文案的正向文本、反向文本生成 ##################################
def llm_generate_pos_neg_text_by_wenAn(str_wenAn = "", model_type=LLM_MODEL_TYPE.Kimi):
    msg_return = ""
    
    TIME_BEGIN()
    try:
        print_my("动作:【文案的正向文本、反向文本生成】开始_{}".format(model_type))
        prompt_of_system = prompt_generate_pos_neg_system
        print("SYSTEM_PROMPT是:\n{}".format(prompt_of_system))
        prompt_of_user = prompt_generate_pos_neg_user.format(str_wenAn=str_wenAn)
        print("USER_PROMPT是:\n{}".format(prompt_of_user))
        messages = [
            {
                "role":"system",
                "content":prompt_of_system,
            }
        ]
        user_msg = {
                "role": "user",
                "content": prompt_of_user,
            } 
        messages.append(user_msg)  

        iRet, msg_return = llm_get_result_content(messages, model_type)   
        if iRet != RET_SUCESS:
            return iRet, msg_return
            
        # 对返回的文本后处理
        msg_return = msg_return.replace("```json", "").replace("```", "")
        
        TIME_END()
        print_my("动作:【文案的正向文本、反向文本生成】完成")
        return RET_SUCESS, msg_return
    except Exception as e:
        print_my("!!!!!llm_generate_pos_neg_text_by_wenAn, 出现异常\n Exception: {}".format(e))
        except_str = str(e)
        if "The request was rejected" in except_str:
            return APP_RET_CODE_UN_SAFE_QUESTION, msg_return
        TIME_END()
        return APP_RET_CODE_NET_ERROR, msg_return
        
    TIME_END()
    print("llm_generate_pos_neg_text_by_wenAn, return error")
    return APP_RET_CODE_NET_ERROR, msg_return
#
# 测试
''''
str_wenAn = """
这是一款个人微信私域营销工具，这个工具可以帮助各行各业的人（包括：宠物、中医诊所、足疗仪器、机油、工业设备用油、高尿酸产品、编程、中老年、贷款中介、炒股、律师、考研等）做微信客户的维护。
这款产品通过智能体、内容、产品，使客户可以对不同的人，不同的群要配置不同的智能体。可以对特定人，特定群配不同智能体，这个智能体会在指定的时间发送特定的消息。此工具内置的智能体懂人性，将销冠经验复刻。
可以触达的方式包括：个微私聊消息、个微群聊、个微朋友圈 。我们的私聊是做到完全定制，朋友圈也是通过设置可见好友达到，用户看到的内容就是你想让他看的。这点说得明一点，就是给客户制作了信息茧房。脑袋转得快的人，马上就能意识到这个工具的可怕。
每个智能体可以根据不同的产品自动生成产品的内容 。 
"""
iRet, msg_return = llm_generate_pos_neg_text_by_wenAn(str_wenAn, LLM_MODEL_TYPE.Kimi)
'''

############################################### 图片生成 ##################################
# 调用大模型生成图片
def llm_get_result_image(prompt_pos, prompt_negative, model_type=IMAGE_GEN_LLM_MODEL_TYPE.Qwen_wanx2_1_t2i_turbo):
    img_url_return = ""
    
    TIME_BEGIN()
    try:
        #print("动作:【请求{}大模型】正向prompt是:{}, 反向prompt是:{}".format(model_type.name, prompt_pos, prompt_negative))
        print("动作:【请求{}大模型】".format(model_type.name))
        if len(prompt_pos) == 0:
            return APP_RET_CODE_UNVALID_PARAM, img_url_return
        if model_type == IMAGE_GEN_LLM_MODEL_TYPE.Qwen_wanx2_1_t2i_turbo:
            print('----sync call, please wait a moment----')
            rsp = ImageSynthesis.call(api_key="YOUR_QWEN_API_KEY",
                                    model="wanx2.1-t2i-turbo",
                                    prompt=prompt_pos,
                                    n=1,
                                    size='1024*1024')
            print('response: %s' % rsp)
            file_path = ""
            if rsp.status_code == HTTPStatus.OK:
                # 在当前目录下保存图片
                for result in rsp.output.results:
                    file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                    file_path = "./{}/{}".format(AI_GENERATE_IMG_DIR, file_name)
                    with open(file_path, 'wb+') as f:
                        f.write(requests.get(result.url).content)
                        print("图片保存到:{}".format(file_path))
            else:
                print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                    (rsp.status_code, rsp.code, rsp.message))
                
            img_url_return = file_path
        else:
            return APP_RET_CODE_UNVALID_PARAM, img_url_return
        # chenyj debug
        print("【{}大模型】回答:\n【\n{}\n】".format(model_type.name, img_url_return))
        TIME_END()
        return RET_SUCESS, img_url_return
    except Exception as e:
        print_my("!!!!!llm_get_result_image, 出现异常\n Exception: {}".format(e))
        except_str = str(e)
        if "The request was rejected" in except_str:
            return APP_RET_CODE_UN_SAFE_QUESTION, img_url_return
        if "exceeded_current_quot" in except_str:
            return APP_RET_CODE_LLM_API_EXCEEDED, img_url_return
        TIME_END()
        return APP_RET_CODE_NET_ERROR, img_url_return
        
    TIME_END()
    print("llm_get_result_image, return error")
    return APP_RET_CODE_NET_ERROR, img_url_return
"""
#prompt_pos = "这是一款个人微信私域营销工具，这个工具可以帮助各行各业的人（包括：宠物、中医诊所、足疗仪器、机油、工业设备用油、高尿酸产品、编程、中老年、贷款中介、炒股、律师、考研等）做微信客户的维护。这款产品通过智能体、内容、产品，使客户可以对不同的人，不同的群要配置不同的智能体。可以对特定人，特定群配不同智能体，这个智能体会在指定的时间发送特定的消息。此工具内置的智能体懂人性，将销冠经验复刻。可以触达的方式包括：个微私聊消息、个微群聊、个微朋友圈 。我们的私聊是做到完全定制，朋友圈也是通过设置可见好友达到，用户看到的内容就是你想让他看的。这点说得明一点，就是给客户制作了信息茧房。脑袋转得快的人，马上就能意识到这个工具的可怕。每个智能体可以根据不同的产品自动生成产品的内容"
prompt_pos = "供应商稳定时怎么切入？这些问题的本质是销售策略的缺失，而不是话术模板的匮乏。"
prompt_negative = "文字;男人"
llm_get_result_image(prompt_pos, prompt_negative, IMAGE_GEN_LLM_MODEL_TYPE.Qwen_wanx2_1_t2i_turbo)   
"""
#################################################################################

# 用于解析一个字符串里的json对象
def extract_json_to_dict(text):
    # 尝试直接解析整个文本
    try:
        json_dict = json.loads(text)
        return json_dict
    except json.JSONDecodeError as e:
        # 如果直接解析失败，尝试提取花括号内的 JSON 格式内容
        json_pattern = r'\{.*?\}'
        matches = re.findall(json_pattern, text, re.DOTALL)

        for match in matches:
            try:
                json_dict = json.loads(match)
                return json_dict
            except json.JSONDecodeError as e:
                print(f"尝试解析提取的JSON字符串时出错: {e}")
        
        print("未找到符合要求的JSON格式的字符串")
        return None
    
#llm_get_result_for_local_rag("任小玲", [], "怎么取消订单")
#llm_get_result_for_local_rag("任小玲", [], "今天心情怎么样")
#llm_get_result_for_local_rag("任小玲", [], "哪里可以找到你们的优惠活动信息")