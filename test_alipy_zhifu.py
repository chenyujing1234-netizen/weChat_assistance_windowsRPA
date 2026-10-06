#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
# pip install alipay-sdk-python
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')
if __name__ == '__main__':
    # 实例化客户端
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2021005199629241'
    alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAjxpjwOhVv23pmPWAhlhKF48d8ew+iZ7kH1pCIL1+c37EgzT/tKwSnsmvN3MGcKs9kS+zRbb0oD+MKtzrA+2crbp7ApZi+ppZmSoqovdrW9x9+ZCAERJzBWcRyvvEDZjm4QRUFDsPUkkksnAwEy8hq20cpF5DtpBCfNIu1ZVNRznZkLcOTXh5hVXWepam6SFQWIqVEPKtRwZd423P279btq0UkAVIn3r8qJLu/ulKcVZecQuCZOURzWb91nL/lgR1P2pnAbGwTsGHYV9NR2IGgFQm/T+4U50rrjOUDvBCbxvPq8Y866CvvR8WdgCu3ZbLKkUo6gTaPND/zhqjXJKZxQIDAQABAoIBAFwr/zxtaW2XefKPjmz5yR9Li1obdFxn/z9Cf31fEGeLqz9nj5vriULFXRo1+FvxsAIn2yx4HzBoPfwNt0IcdeJgToLoInCPok5JHpVBD+FnL6zjKdnVLEi6jndTmn+3kF42z4EIWWICwqQ8Jnr0zJcB/ITSQoMAgBKtvoTLWa8Z1qeDaJaBsBUUjyAAkywmYrOibb8p8qY8gzJZdR+bLWDXHxPTIzIrJrsRmyK5aOaGQVo15bZ76WsXqxaP6Eqv0JpSfUk+VSTiaXzXRLaZoDmcr+mWo9ThovfGkTVcqR+Vp4ePqHhw+yRhuzqFTNXLtcWmI1XJma0Qoc8F7GBG2AECgYEA3Ssj+Rms0c9gmGGy1U2TFwsspoigXTBoSNF9JyKnAW1luCLz6zMmfBVwbHo2LyX/UwG48GNjJIXK8zrAtJF8hxCQPZUA0us3CykaymIPxmBVqbwMJMAj9ckbIuAHO076bEQKzMJC08dYzUmdSNvpTZ2Oc7UQmA40Yo15ypaGEYECgYEApaPh00fFTtXH/8xIi4twP05ay0Z2J+pHLf2PGDVrC0B+gElYi5p600IuoC87zjm1jnn6AMSVpk4tT/lXIvOAOHMYzLXO7k1ABYDR+jx9/uYCv+EGeKbrfkYSWOaiAhQIaExM/Sz47A83Z9WpMa+6qljNEXZfp3gsf4/oHzT84kUCgYBCVjM2/v13/NSDQCKMmfT5X2+oD6jR6rgMx1DbkSg4ZGCzJ0C0FiZ/50pOLyXbZHE9q3GWIKlXBg5GgCPWxSBtvokU/4E8wjJDVbPkah9DKBfpji6yQzNGAGj0P+/LWTgBizMWEVpL/SnkgST8+oDyt8RHblKo2PHbcYXLPvS9gQKBgCYkNZUEOs/rdFFXxgC0DBXXwhp60Cxiyx8w+ulVK5/8quR5fzUuTkglPj1OgxP6v+7d8Y6JtfgEmnSG8uSuc4EMJ9LDrrG7AhoCTtezZEP0zP9IHshbj3CVTBZCjV2zJTh3EWdfGraozlZPodU6JN6i8h2qR1510rFQ/t9owS6NAoGAURwhpt32HaY1FeKKQLdkbznEWwtRhhM9JfauiiU2XeGPeCy1GP6g56j7dLGsanALxA5LjaA5oscFDaaPd5PiZf9MbIY6x0iq42ovLx+sIw4DErZrmi3TMk1FjrQOqf2yzDoBAZ9J3Ct59Jb7B2bvv7ujp+rFsKvfvvNF/b9/7Xc='
    alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr2ClAsdkOdZf8lpoJdZS7/+zXv4EnHnhFJ6RAib5QWu0v5mI0TlQm2PVLB0G0aomkaVTJ0K6bYVIK7ZklhwmjqEpLegYb5XCzhXcXvdddJfi1AxQwF7KqYdk1IYpDHaxMY/lrZd+a7fhPTsILZ7bspur4L94T88wtOIFkHpViZws4qXdpL6PQL/pKEScAydqyPBwN0BtSOu4IXVg2m4Bfyc1Nc+ZKHEyoBjmTQAIpKGF8BuPztcHAd9iMUZ4szSMhZxuX79IxEMp77clxmmZFH+JbB2q5Js6GO7vuvWfYrloZyhLsGkeXWluNnXO+oVUQS+8Ml/TKeztGn2xfGIOnQIDAQAB'
    client = DefaultAlipayClient(alipay_client_config, logger)
    # 构造请求参数对象
    model = AlipayTradeCreateModel()
    model.out_trade_no = "20150320010101001";
    model.total_amount = "88.88";
    model.subject = "Iphone6 16G";
    model.buyer_id = "2088******846880";
    request = AlipayTradeCreateRequest(biz_model=model)
    # 执行API调用
    response_content = False
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        # 解析响应结果
        response = AlipayTradeCreateResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)