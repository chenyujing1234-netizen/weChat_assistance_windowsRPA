# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

# pip install alibabacloud_dysmsapi20170525==4.2.0
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

accessKeyId = 'YOUR_ALIYUN_SMS_ACCESS_KEY_ID'
accessKeySecret = 'YOUR_ALIYUN_SMS_ACCESS_KEY_SECRET'
class PhoneSmsOptAliyun:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码建议使用更安全的无AK方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        credential = CredentialClient()
        config = open_api_models.Config(
            credential=credential,
            access_key_id=accessKeyId,
            access_key_secret=accessKeySecret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send_sms(phone_num, verification_code) -> None:
        print(f"send_sms 1111")
        client = PhoneSmsOptAliyun.create_client()
        print(f"send_sms 2222")
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='哈希流光',
            template_code='SMS_495955218',
            phone_numbers=phone_num,
            template_param=f'{{"code":"{verification_code}"}}'
        )
        print(f"send_sms 3333")
        runtime = util_models.RuntimeOptions()
        print(f"send_sms 4444")
        try:
            # 复制代码运行请自行打印 API 的返回值
            result = client.send_sms_with_options(send_sms_request, runtime)
            #print(f"发送短信结果: {result}")
            # 成功时，得到的result信息是
            # 发送短信结果: {'headers': {'date': 'Sat, 27 Sep 2025 09:03:36 GMT', 'content-type': 'application/json;charset=utf-8', 'content-length': '110', 'connection': 'keep-alive', 'keep-alive': 'timeout=25', 'access-control-allow-origin': '*', 'access-control-expose-headers': '*', 'x-acs-request-id': '37423015-9E62-5726-903F-76A382D3BB8B', 'x-acs-trace-id': '828b24cd873fb85805cdce692642d187', 'etag': '1EJqUTHH7UBsPmW01P/9XWw0'}, 'statusCode': 200, 'body': {'BizId': '495717958963816607^0', 'Code': 'OK', 'Message': 'OK', 'RequestId': '37423015-9E62-5726-903F-76A382D3BB8B'}}
            print(f"send_sms 5555")
            # 解析结果判断是否成功
            if hasattr(result, 'status_code') and result.status_code == 200:
                if hasattr(result, 'body') and hasattr(result.body, 'code') and result.body.code == 'OK':
                    print(f"短信发送成功")
                    return True, ""
                else:
                    print(f"短信发送失败，错误代码: {result.body.code}, 错误消息: {result.body.message}")
                    return False, result.body.message
            else:
                print(f"请求失败，状态码: {result.status_code}")
                return False, f"请求失败，状态码: {result.status_code}"
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            return False, error.message

    @staticmethod
    async def send_sms_async(phone_num, verification_code) -> None:
        client = PhoneSmsOptAliyun.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='哈希流光',
            template_code='SMS_495955218',
            phone_numbers=phone_num,
            template_param=f'{{"code":"{verification_code}"}}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            result = await client.send_sms_with_options_async(send_sms_request, runtime)
            print(f"异步发送短信结果: {result}")
            
            # 解析结果判断是否成功
            if hasattr(result, 'status_code') and result.status_code == 200:
                if hasattr(result, 'body') and hasattr(result.body, 'code') and result.body.code == 'OK':
                    print(f"短信异步发送成功")
                    return True, ""
                else:
                    print(f"短信异步发送失败，错误代码: {result.body.code}, 错误消息: {result.body.message}")
                    return False, result.body.message
            else:
                print(f"异步请求失败，状态码: {result.status_code}")
                return False
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            return False, error.message


if __name__ == '__main__':
    b_sucess, msg = PhoneSmsOptAliyun.send_sms("15280006510", "1234")
    if b_sucess == False:
        print(msg)
    else:
        print("短信发送成功")
