from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from phone_sms_opt_aliyun import PhoneSmsOptAliyun
import random
import time
import json
import os
from log_helper import print_my
from server_http_opt import *
from qr_code_helper import url_to_qr_image
import app_info

# Html事件处理
class HtmlBackend(QObject):
    # 提供给原生main程序的信号 
    _signal = pyqtSignal(str)

    """后端接口，提供给JavaScript调用"""
    # 信号：用于向JavaScript发送消息
    messageChanged = pyqtSignal(str)
    verificationCodeSent = pyqtSignal(bool, str)  # 发送验证码结果
    loginResult = pyqtSignal(bool, str)  # 登录结果
    userInfoLoaded = pyqtSignal(bool, str)  # 用户信息加载结果 - 修改为字符串类型
    rechargeHistoryLoaded = pyqtSignal(bool, str)  # 充值记录加载结果 - 修改为字符串类型
    activationResult = pyqtSignal(bool, str)  # 激活码验证结果
    
    def __init__(self, config_json_data):
        super().__init__()
        self.config_json_data = config_json_data
        self.verification_code = ""
        self.valid_until = 0  # 验证码有效期时间戳
        
    @pyqtSlot(str, str, str, result=str)
    def get_payment_qr_code(self, phone, subject, total_amount):
        """获取支付二维码"""
        print(f"获取支付二维码：手机号 {phone}，商品 {subject}，金额 {total_amount}")
        
        # chenyj test
        #total_amount = "0.01"

        try:
            # 调用http_get_trade接口获取订单信息
            success, trade_return = http_get_trade(phone, subject, total_amount)
            
            if success and trade_return:
                # 检查是否包含qr_code字段
                if "qr_code" in trade_return:
                    print(f"获取二维码成功: {trade_return['qr_code']}")
                    # 生成二维码图片，保存到USER_DATA_DIR
                    qr_image_path = os.path.join(app_info.USER_DATA_DIR, "payment_qr.png")
                    url_to_qr_image(trade_return["qr_code"], qr_image_path)
                    return json.dumps({
                        "success": True,
                        "qr_code": qr_image_path  # 使用绝对路径
                    })
                else:
                    print("获取二维码失败：返回数据中不包含qr_code字段")
                    return json.dumps({
                        "success": False,
                        "message": "返回数据中不包含qr_code字段"
                    })
            else:
                print("获取二维码失败：调用http_get_trade接口失败")
                return json.dumps({
                    "success": False,
                    "message": "获取订单信息失败"
                })
        except Exception as e:
            print(f"获取二维码异常：{str(e)}")
            return json.dumps({
                "success": False,
                "message": f"获取二维码异常：{str(e)}"
            })

    @pyqtSlot(str)
    def test_message(self, message):
        print(f"收到来自前端的测试消息: {message}")
        # 简单地回复消息，验证通信是否双向
        return f"后端已收到消息: {message}"
        
    @pyqtSlot(str)
    def send_verification_code(self, phone):
        """发送验证码（实际项目中这里会调用短信接口）"""
        print(f"准备向手机号 {phone} 发送验证码")
        
        # 模拟发送验证码过程
        try:
            # 生成4位随机验证码
            self.verification_code = str(random.randint(1000, 9999))
            # 有效期1分钟
            self.valid_until = time.time() + 60
            
            # 模拟API调用延迟
            #time.sleep(1)
            b_sucess, message = PhoneSmsOptAliyun.send_sms(phone, self.verification_code)
            if b_sucess == False:
                #self.verificationCodeSent.emit(False, "发送失败，请检查手机号")
                self.verificationCodeSent.emit(False, f"发送失败：{message}")
                print_my(f"!!!!!! 短信发送失败：{message}")
                return
            
            print(f"验证码已发送")
            # 通知前端发送成功
            self.verificationCodeSent.emit(True, "验证码已发送，请注意查收")
        except Exception as e:
            print(f"发送失败：{str(e)}")
            print_my(f"发送失败：{str(e)}")
            self.verificationCodeSent.emit(False, f"发送失败：{str(e)}")
    
    @pyqtSlot(str, str)
    def verify_login(self, phone, code):
        """验证登录信息"""
        print(f"验证登录：手机号 {phone}，验证码 {code}")

        # chenyj test
        """
        # 验证成功
        self.loginResult.emit(True, f"登录成功，欢迎回来！")
        self._signal.emit("login_sucess_{}".format("15280006511"))
        return 
        """

        # 验证验证码
        if time.time() > self.valid_until:
            self.loginResult.emit(False, "验证码已过期，请重新获取")
            return
            
        if code != self.verification_code:
            self.loginResult.emit(False, "验证码不正确")
            return
            
        # 验证成功
        self.loginResult.emit(True, f"登录成功，欢迎回来！")
        self._signal.emit("login_sucess_{}".format(phone))
    
    @pyqtSlot()
    def load_user_info(self):
        """加载用户信息"""
        print("加载用户信息")
        print(f"当前config_json_data: {self.config_json_data}")
        if 'BIND_PHONE' in self.config_json_data and len(self.config_json_data["BIND_PHONE"]) > 0:
            print(f"BIND_PHONE存在: {self.config_json_data['BIND_PHONE']}")
        else:
            print(f"BIND_PHONE不存在")
        
        # 模拟用户信息数据
        # 实际项目中，这里应该从数据库或API获取真实用户信息
        try:
            # 确保BIND_PHONE字段存在
            if 'BIND_PHONE' not in self.config_json_data:
                self.config_json_data['BIND_PHONE'] = ''  # 默认手机号
                print("BIND_PHONE不存在，已设置默认值")
            """
            user_info = {
                "phone_number": self.config_json_data["BIND_PHONE"],
                "multi_open_expire": "2025-10-21 13:57:48",
                "multi_open_remaining": "24",
                "ai_expire": "-"
            }
            """
            user_info = {
                "phone_number": self.config_json_data["BIND_PHONE"],
                "multi_open_expire": "",
                "multi_open_remaining": "",
                "ai_expire": "-"
            }
            
            print(f"生成的用户信息: {user_info}")
            print("准备发出userInfoLoaded信号")
            # 将dict转换为JSON字符串
            user_info_json = json.dumps(user_info)
            print(f"转换后的JSON字符串: {user_info_json}")
            self.userInfoLoaded.emit(True, user_info_json)
        except Exception as e:
            print(f"加载用户信息失败：{str(e)}")
            print(f"异常类型: {type(e).__name__}")
            # 即使出错也发送一个有效的信号，避免前端接收不到数据
            fallback_user_info = {
                "phone_number": "15280006511",
                "multi_open_expire": "2025-10-21 13:57:48",
                "multi_open_remaining": "24",
                "ai_expire": "-"
            }
            # 将fallback_user_info转换为JSON字符串
            fallback_user_info_json = json.dumps(fallback_user_info)
            print(f"使用fallback用户信息: {fallback_user_info_json}")
            self.userInfoLoaded.emit(True, fallback_user_info_json)
    
    @pyqtSlot()
    def load_recharge_history(self):
        """加载充值记录"""
        print("加载充值记录")
        
        # 模拟充值记录数据
        # 实际项目中，这里应该从数据库或API获取真实的充值记录
        try:
            recharge_history = []
            """
            recharge_history = [
                {
                    "time": "2025-09-21 13:57:48",
                    "duration": "30天",
                    "description": "【Rpa|自助充值】微一个月"
                }
            ]
            """
            if 'BIND_PHONE'  in self.config_json_data:
                b_sucess, trades_return = http_get_payment(self.config_json_data["BIND_PHONE"])
                if b_sucess == True:
                    for trade in trades_return:
                        recharge = {"time":trade["trade_payment_time"], "duration":trade["trade_subject"], "description":trade["trade_subject"]}
                        recharge_history.append(recharge)
            
            # 将list转换为JSON字符串
            recharge_history_json = json.dumps(recharge_history)
            print(f"转换后的充值记录JSON字符串: {recharge_history_json}")
            self.rechargeHistoryLoaded.emit(True, recharge_history_json)
        except Exception as e:
            print(f"加载充值记录失败：{str(e)}")
            # 即使失败也发送空的JSON字符串
            self.rechargeHistoryLoaded.emit(False, "[]")
    
    @pyqtSlot()
    def lock_screen(self):
        """锁屏操作"""
        print("执行锁屏操作")
        self._signal.emit("lock_screen")
    
    @pyqtSlot()
    def switch_account(self):
        """切换账号"""
        print("执行切换账号操作")
        self._signal.emit("switch_account")
    
    @pyqtSlot()
    def renew_service(self):
        """续费操作"""
        print("执行续费操作")
        self._signal.emit("renew_service")
    
    @pyqtSlot(str)
    def switch_menu(self, menu_name):
        """切换菜单"""
        print(f"切换到菜单：{menu_name}")
        self._signal.emit(f"menu_switch_{menu_name}")
    
    @pyqtSlot(str)
    def switch_product(self, product_name):
        """切换产品"""
        print(f"切换产品：{product_name}")
        self._signal.emit(f"switch_product_{product_name}")
    
    @pyqtSlot(str)
    def select_wechat_number(self, number):
        """选择微信数量"""
        print(f"选择微信数量：{number}")
        self._signal.emit(f"select_wechat_number_{number}")
    
    @pyqtSlot(str, str)
    def select_subscription_plan(self, plan_name, plan_price):
        """选择订阅计划"""
        print(f"选择订阅计划：{plan_name}, 价格：{plan_price}")
        self._signal.emit(f"select_subscription_plan_{plan_name}_{plan_price}")
    
    @pyqtSlot(str)
    def switch_payment_method(self, method_name):
        """切换支付方式"""
        print(f"切换支付方式：{method_name}")
        self._signal.emit(f"switch_payment_method_{method_name}")
    
    @pyqtSlot(str)
    def verify_activation_code(self, code):
        """验证激活码"""
        print(f"验证激活码：{code}")
        
        # 模拟激活码验证过程
        # 实际项目中，这里应该连接到后端API或数据库进行验证
        try:
            # 简单的模拟逻辑：假设特定的激活码格式是有效的
            # 在实际应用中，应该有更复杂的验证逻辑
            if code and code.strip():  # 这里只是简单检查是否非空
                # 模拟验证成功
                print("激活码验证成功")
                self.activationResult.emit(True, "激活成功！感谢您的支持。")
            else:
                # 模拟验证失败
                print("激活码验证失败")
                self.activationResult.emit(False, "激活码无效，请重新输入。")
        except Exception as e:
            print(f"激活码验证过程中发生错误：{str(e)}")
            self.activationResult.emit(False, f"验证过程中发生错误：{str(e)}")
    
    @pyqtSlot(result=str)
    def get_bind_phone(self):
        """获取绑定的手机号"""
        if 'BIND_PHONE' in self.config_json_data and self.config_json_data['BIND_PHONE']:
            print(f"配置文件里找到绑定手机号：{self.config_json_data['BIND_PHONE']}")
            return self.config_json_data['BIND_PHONE']
        print(f"配置文件里没有找到绑定手机号，使用默认手机号")
        return '15280006510'  # 默认手机号
    
    @pyqtSlot()
    def close_payment(self):
        """关闭支付窗口"""
        print("关闭支付窗口")
        self._signal.emit("close_payment")