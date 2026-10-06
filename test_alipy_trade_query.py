
#!/usr/bin/env python
# -* - coding: utf - 8 -* -
import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest

logging.basicConfig(
  level = logging.INFO,
  format = '%(asctime)s %(levelname)s %(message)s',
  filemode = 'a',)
logger = logging.getLogger('')

if __name__ == '__main__':
  """ 初始化 """
  alipay_client_config = AlipayClientConfig()

  """ 支付宝网关 """
  alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'

  """ 如何获取appid请参考：https://opensupport.alipay.com/support/helpcenter/190/201602493024 """
  alipay_client_config.app_id = '2021005199629241'

  """ 密钥格式为pkcs1，如何获取应用私钥请参考：https://opensupport.alipay.com/support/helpcenter/207/201602469554 """
  alipay_client_config.app_private_key = 'MIIEogIBAAKCAQEAjxpjwOhVv23pmPWAhlhKF48d8ew+iZ7kH1pCIL1+c37EgzT/tKwSnsmvN3MGcKs9kS+zRbb0oD+MKtzrA+2crbp7ApZi+ppZmSoqovdrW9x9+ZCAERJzBWcRyvvEDZjm4QRUFDsPUkkksnAwEy8hq20cpF5DtpBCfNIu1ZVNRznZkLcOTXh5hVXWepam6SFQWIqVEPKtRwZd423P279btq0UkAVIn3r8qJLu/ulKcVZecQuCZOURzWb91nL/lgR1P2pnAbGwTsGHYV9NR2IGgFQm/T+4U50rrjOUDvBCbxvPq8Y866CvvR8WdgCu3ZbLKkUo6gTaPND/zhqjXJKZxQIDAQABAoIBAFwr/zxtaW2XefKPjmz5yR9Li1obdFxn/z9Cf31fEGeLqz9nj5vriULFXRo1+FvxsAIn2yx4HzBoPfwNt0IcdeJgToLoInCPok5JHpVBD+FnL6zjKdnVLEi6jndTmn+3kF42z4EIWWICwqQ8Jnr0zJcB/ITSQoMAgBKtvoTLWa8Z1qeDaJaBsBUUjyAAkywmYrOibb8p8qY8gzJZdR+bLWDXHxPTIzIrJrsRmyK5aOaGQVo15bZ76WsXqxaP6Eqv0JpSfUk+VSTiaXzXRLaZoDmcr+mWo9ThovfGkTVcqR+Vp4ePqHhw+yRhuzqFTNXLtcWmI1XJma0Qoc8F7GBG2AECgYEA3Ssj+Rms0c9gmGGy1U2TFwsspoigXTBoSNF9JyKnAW1luCLz6zMmfBVwbHo2LyX/UwG48GNjJIXK8zrAtJF8hxCQPZUA0us3CykaymIPxmBVqbwMJMAj9ckbIuAHO076bEQKzMJC08dYzUmdSNvpTZ2Oc7UQmA40Yo15ypaGEYECgYEApaPh00fFTtXH/8xIi4twP05ay0Z2J+pHLf2PGDVrC0B+gElYi5p600IuoC87zjm1jnn6AMSVpk4tT/lXIvOAOHMYzLXO7k1ABYDR+jx9/uYCv+EGeKbrfkYSWOaiAhQIaExM/Sz47A83Z9WpMa+6qljNEXZfp3gsf4/oHzT84kUCgYBCVjM2/v13/NSDQCKMmfT5X2+oD6jR6rgMx1DbkSg4ZGCzJ0C0FiZ/50pOLyXbZHE9q3GWIKlXBg5GgCPWxSBtvokU/4E8wjJDVbPkah9DKBfpji6yQzNGAGj0P+/LWTgBizMWEVpL/SnkgST8+oDyt8RHblKo2PHbcYXLPvS9gQKBgCYkNZUEOs/rdFFXxgC0DBXXwhp60Cxiyx8w+ulVK5/8quR5fzUuTkglPj1OgxP6v+7d8Y6JtfgEmnSG8uSuc4EMJ9LDrrG7AhoCTtezZEP0zP9IHshbj3CVTBZCjV2zJTh3EWdfGraozlZPodU6JN6i8h2qR1510rFQ/t9owS6NAoGAURwhpt32HaY1FeKKQLdkbznEWwtRhhM9JfauiiU2XeGPeCy1GP6g56j7dLGsanALxA5LjaA5oscFDaaPd5PiZf9MbIY6x0iq42ovLx+sIw4DErZrmi3TMk1FjrQOqf2yzDoBAZ9J3Ct59Jb7B2bvv7ujp+rFsKvfvvNF/b9/7Xc='

  """ 如何获取支付宝公钥请查看：https://opensupport.alipay.com/support/helpcenter/207/201602487431 """
  alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr2ClAsdkOdZf8lpoJdZS7/+zXv4EnHnhFJ6RAib5QWu0v5mI0TlQm2PVLB0G0aomkaVTJ0K6bYVIK7ZklhwmjqEpLegYb5XCzhXcXvdddJfi1AxQwF7KqYdk1IYpDHaxMY/lrZd+a7fhPTsILZ7bspur4L94T88wtOIFkHpViZws4qXdpL6PQL/pKEScAydqyPBwN0BtSOu4IXVg2m4Bfyc1Nc+ZKHEyoBjmTQAIpKGF8BuPztcHAd9iMUZ4szSMhZxuX79IxEMp77clxmmZFH+JbB2q5Js6GO7vuvWfYrloZyhLsGkeXWluNnXO+oVUQS+8Ml/TKeztGn2xfGIOnQIDAQAB'

  """ 签名算法类型 """
  alipay_client_config._sign_type = 'RSA2'
  client = DefaultAlipayClient(alipay_client_config, logger)

  """ 构造请求参数对象,当前调用接口名称：alipay.trade.query(统一收单线下交易查询) """
  model = AlipayTradeQueryModel()

  """ 注：交易号（TradeNo）与订单号（OutTradeNo）二选一传入即可，如果2个同时传入，则以交易号为准 """ 
  """ 支付接口传入的商户订单号。如：2020061601290011200000140004 """ 
  model.out_trade_no = "234234242543543";

  """ 异步通知/查询接口返回的支付宝交易号，如：2020061622001473951448314322 """
  model.trade_no = "";

  request = AlipayTradeQueryRequest(biz_model = model)

  """ 第三方调用（服务商模式），传值app_auth_token后，会收款至授权token对应商家账号，如何获传值app_auth_token请参考文档：https://opensupport.alipay.com/support/helpcenter/79/201602494631 """
  #request.add_other_text_param('app_auth_token', '传入获取到的app_auth_token值')

  """ 执行API调用 """ 
  response = client.execute(request)

  """ 获取接口调用结果，如果调用失败，可根据返回错误信息到该文档寻找排查方案：https://opensupport.alipay.com/support/helpcenter/101 """
  print("get response body:" + response)

