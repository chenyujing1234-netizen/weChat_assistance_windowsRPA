# -*- coding: utf-8 -*-
"""
坐标配置管理模块
读取location.cfg文件中的坐标配置，并根据当前设备类型提供对应的坐标值
"""

import configparser
import os
from app_info import DEVICE_MODEL_TYPE, g_deivce_MODEL, G_X_PIAN_YI, G_Y_PIAN_YI
from log_helper import print_my


class LocationConfig:
    """坐标配置管理类"""
    
    def __init__(self, config_file='location.cfg'):
        """
        初始化坐标配置
        :param config_file: 配置文件路径
        """
        self.config_file = config_file
        # 创建ConfigParser时支持行内注释（#和;开头的行内注释）
        self.config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        self.device_section = self._get_device_section()
        self._load_config()
        
    def _get_device_section(self):
        """根据当前设备类型获取配置文件section名称"""
        device_map = {
            DEVICE_MODEL_TYPE.Local_Emulator: 'Local_Emulator',
            DEVICE_MODEL_TYPE.WiFi_Phone_Xiaomi_8_Pro: 'WiFi_Phone_Xiaomi_8_Pro',
            DEVICE_MODEL_TYPE.Yun_Phone_720_1080: 'Yun_Phone_720_1080',
            DEVICE_MODEL_TYPE.Windows: 'Windows',
            DEVICE_MODEL_TYPE.Windows_1366_768: 'Windows_1366_768',
        }
        return device_map.get(g_deivce_MODEL, 'Windows')
    
    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            print_my(f"!!!!! 坐标配置文件不存在: {self.config_file}")
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        
        try:
            self.config.read(self.config_file, encoding='utf-8')
            print_my(f"成功加载坐标配置文件: {self.config_file}, 设备类型: {self.device_section}")
        except Exception as e:
            print_my(f"!!!!! 加载配置文件失败: {e}")
            raise
    
    def get_int(self, key, need_offset_x=False, need_offset_y=False, default=None):
        """
        获取整数类型的坐标值
        :param key: 配置项key
        :param need_offset_x: 是否需要叠加X轴偏移量(G_X_PIAN_YI)
        :param need_offset_y: 是否需要叠加Y轴偏移量(G_Y_PIAN_YI)
        :param default: 默认值
        :return: 坐标值
        """
        try:
            value = self.config.getint(self.device_section, key)
            
            # Windows平台部分坐标需要叠加偏移量
            if g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows or g_deivce_MODEL == DEVICE_MODEL_TYPE.Windows_1366_768:
                if need_offset_x:
                    value += G_X_PIAN_YI
                elif need_offset_y:
                    value += G_Y_PIAN_YI
            
            return value
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            if default is not None:
                print_my(f"警告: 配置项 [{self.device_section}]{key} 不存在或格式错误，使用默认值: {default}")
                return default
            else:
                print_my(f"!!!!! 配置项 [{self.device_section}]{key} 不存在: {e}")
                raise
    
    def get_string(self, key, default=None):
        """
        获取字符串类型的配置值
        :param key: 配置项key
        :param default: 默认值
        :return: 配置值
        """
        try:
            return self.config.get(self.device_section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            if default is not None:
                return default
            else:
                print_my(f"!!!!! 配置项 [{self.device_section}]{key} 不存在: {e}")
                raise
    
    # ===== 屏幕尺寸相关 =====
    
    @property
    def W_SCREEN(self):
        """屏幕宽度"""
        return self.get_int('W_SCREEN', default=1080)
    
    @property
    def H_SCREEN(self):
        """屏幕高度"""
        return self.get_int('H_SCREEN', default=1920)
    
    # ===== 好友聊天列表区域 =====
    
    @property
    def FRIEND_CHAT_LIST_LT_X(self):
        """好友列表左上角X坐标"""
        return self.get_int('FRIEND_CHAT_LIST_LT_X', need_offset_x=True)
    
    @property
    def FRIEND_CHAT_LIST_LT_Y(self):
        """好友列表左上角Y坐标"""
        return self.get_int('FRIEND_CHAT_LIST_LT_Y', need_offset_y=True)
    
    # ===== 聊天窗口区域 =====
    
    @property
    def CHAT_LT_X(self):
        """聊天窗口左上角X坐标"""
        return self.get_int('CHAT_LT_X', need_offset_x=True)
    
    @property
    def CHAT_LT_Y(self):
        """聊天窗口左上角Y坐标"""
        return self.get_int('CHAT_LT_Y', need_offset_y=True)
    
    @property
    def CHAT_LINE_HEIGHT(self):
        """聊天记录行高"""
        return self.get_int('CHAT_LINE_HEIGHT', default=46)
    
    @property
    def CHAT_LINE_HEIGHT_INTER(self):
        """聊天记录行间距"""
        return self.get_int('CHAT_LINE_HEIGHT_INTER', default=40)
    
    @property
    def CHAT_MIN_Y_FOR_OCR(self):
        """OCR识别最小Y坐标"""
        return self.get_int('CHAT_MIN_Y_FOR_OCR', default=5)
    
    @property
    def CHAT_MAX_Y_FOR_OCR(self):
        """OCR识别最大Y坐标"""
        return self.get_int('CHAT_MAX_Y_FOR_OCR', default=1841)
    
    @property
    def CHAT_LT_X_SHOULD_MIN(self):
        """聊天文本左边界最小X"""
        return self.get_int('CHAT_LT_X_SHOULD_MIN')
    
    @property
    def CHAT_LT_X_SHOULD_MIN_INTER(self):
        """聊天文本左边界容差"""
        return self.get_int('CHAT_LT_X_SHOULD_MIN_INTER', default=15)
    
    @property
    def CHAT_RB_X_SHOULD_MIN(self):
        """聊天文本右边界最小X"""
        return self.get_int('CHAT_RB_X_SHOULD_MIN')
    
    @property
    def CHAT_RB_X_SHOULD_MIN_INTER(self):
        """聊天文本右边界容差"""
        return self.get_int('CHAT_RB_X_SHOULD_MIN_INTER', default=20)
    
    # ===== 好友资料页 =====
    
    @property
    def NICKNAME_RB_X(self):
        """好友昵称区域右下角X"""
        return self.get_int('NICKNAME_RB_X')
    
    @property
    def NICKNAME_RB_Y(self):
        """好友昵称区域右下角Y"""
        return self.get_int('NICKNAME_RB_Y')
    
    # ===== 权限申请页面 =====
    
    @property
    def QUXIAN_CANCEL_LT_X(self):
        """权限申请页取消按钮X"""
        return self.get_int('QUXIAN_CANCEL_LT_X')
    
    @property
    def QUXIAN_CANCEL_LT_Y(self):
        """权限申请页取消按钮Y"""
        return self.get_int('QUXIAN_CANCEL_LT_Y')
    
    # ===== 隐私设置提示页 =====
    
    @property
    def MSG_BECAUSE_PRIVACY_X(self):
        """隐私提示确定按钮X"""
        return self.get_int('MSG_BECAUSE_PRIVACY_X')
    
    @property
    def MSG_BECAUSE_PRIVACY_Y(self):
        """隐私提示确定按钮Y"""
        return self.get_int('MSG_BECAUSE_PRIVACY_Y')
    
    # ===== 安全登录页面 =====
    
    @property
    def SAFE_RE_LOGIN_CANCEL_LT_X(self):
        """安全登录取消按钮X"""
        return self.get_int('SAFE_RE_LOGIN_CANCEL_LT_X')
    
    @property
    def SAFE_RE_LOGIN_CANCEL_LT_Y(self):
        """安全登录取消按钮Y"""
        return self.get_int('SAFE_RE_LOGIN_CANCEL_LT_Y')
    
    # ===== 访问剪贴板提示 =====
    
    @property
    def WEI_XIN_APPLY_VISIT_AMBLE_X(self):
        """访问剪贴板允许按钮X"""
        return self.get_int('WEI_XIN_APPLY_VISIT_AMBLE_X')
    
    @property
    def WEI_XIN_APPLY_VISIT_AMBLE_Y(self):
        """访问剪贴板允许按钮Y"""
        return self.get_int('WEI_XIN_APPLY_VISIT_AMBLE_Y')
    
    # ===== 继续编辑按钮 =====
    
    @property
    def KEEP_EDIT_X(self):
        """继续编辑X坐标"""
        return self.get_int('KEEP_EDIT_X')
    
    @property
    def KEEP_EDIT_Y(self):
        """继续编辑Y坐标"""
        return self.get_int('KEEP_EDIT_Y')
    
    # ===== 底部导航栏按钮 =====
    
    @property
    def BTN_NAV_WEIXIN_X(self):
        """微信按钮X坐标"""
        return self.get_int('BTN_NAV_WEIXIN_X', need_offset_x=True)
    
    @property
    def BTN_NAV_WEIXIN_Y(self):
        """微信按钮Y坐标"""
        return self.get_int('BTN_NAV_WEIXIN_Y', need_offset_y=True)
    
    @property
    def BTN_NAV_CONTACTS_X(self):
        """通讯录按钮X坐标"""
        return self.get_int('BTN_NAV_CONTACTS_X', need_offset_x=True)
    
    @property
    def BTN_NAV_CONTACTS_Y(self):
        """通讯录按钮Y坐标"""
        return self.get_int('BTN_NAV_CONTACTS_Y', need_offset_y=True)
    
    @property
    def BTN_NAV_DISCOVER_X(self):
        """发现按钮X坐标"""
        return self.get_int('BTN_NAV_DISCOVER_X')
    
    @property
    def BTN_NAV_DISCOVER_Y(self):
        """发现按钮Y坐标"""
        return self.get_int('BTN_NAV_DISCOVER_Y')
    
    @property
    def BTN_NAV_ME_X(self):
        """我按钮X坐标"""
        return self.get_int('BTN_NAV_ME_X', need_offset_x=True)
    
    @property
    def BTN_NAV_ME_Y(self):
        """我按钮Y坐标"""
        return self.get_int('BTN_NAV_ME_Y', need_offset_y=True)
    
    # ===== 其他常用按钮 =====
    
    @property
    def ADD_FRIEND_BTN_X(self):
        """添加好友按钮X"""
        return self.get_int('ADD_FRIEND_BTN_X')
    
    @property
    def ADD_FRIEND_BTN_Y(self):
        """添加好友按钮Y"""
        return self.get_int('ADD_FRIEND_BTN_Y')
    
    @property
    def SEARCH_BTN_X(self):
        """搜索按钮X"""
        return self.get_int('SEARCH_BTN_X')
    
    @property
    def SEARCH_BTN_Y(self):
        """搜索按钮Y"""
        return self.get_int('SEARCH_BTN_Y')
    
    @property
    def BACK_BTN_X(self):
        """返回按钮X"""
        return self.get_int('BACK_BTN_X')
    
    @property
    def BACK_BTN_Y(self):
        """返回按钮Y"""
        return self.get_int('BACK_BTN_Y')
    
    @property
    def SEND_MOMENT_BTN_X(self):
        """发送朋友圈按钮X"""
        return self.get_int('SEND_MOMENT_BTN_X', default=608)
    
    @property
    def SEND_MOMENT_BTN_Y(self):
        """发送朋友圈按钮Y"""
        return self.get_int('SEND_MOMENT_BTN_Y', default=875)
    
    # ===== 朋友圈相关按钮 =====
    
    @property
    def BTN_FRIEND_CIRCLE_X(self):
        """朋友圈按钮X（发现tab页中）"""
        return self.get_int('BTN_FRIEND_CIRCLE_X')
    
    @property
    def BTN_FRIEND_CIRCLE_Y(self):
        """朋友圈按钮Y（发现tab页中）"""
        return self.get_int('BTN_FRIEND_CIRCLE_Y')
    
    @property
    def BTN_WHO_CAN_SEE_TEXT_X(self):
        """文字模式"谁可以看"按钮X"""
        return self.get_int('BTN_WHO_CAN_SEE_TEXT_X')
    
    @property
    def BTN_WHO_CAN_SEE_TEXT_Y(self):
        """文字模式"谁可以看"按钮Y"""
        return self.get_int('BTN_WHO_CAN_SEE_TEXT_Y')
    
    @property
    def BTN_WHO_CAN_SEE_IMG_X(self):
        """图片模式"谁可以看"按钮X"""
        return self.get_int('BTN_WHO_CAN_SEE_IMG_X')
    
    @property
    def BTN_WHO_CAN_SEE_IMG_Y(self):
        """图片模式"谁可以看"按钮Y"""
        return self.get_int('BTN_WHO_CAN_SEE_IMG_Y')
    
    @property
    def BTN_SEND_CIRCLE_TOP_RIGHT_X(self):
        """右上角发送朋友圈按钮X"""
        return self.get_int('BTN_SEND_CIRCLE_TOP_RIGHT_X')
    
    @property
    def BTN_SEND_CIRCLE_TOP_RIGHT_Y(self):
        """右上角发送朋友圈按钮Y"""
        return self.get_int('BTN_SEND_CIRCLE_TOP_RIGHT_Y')
    
    @property
    def BTN_SELECT_FROM_ALBUM_CIRCLE_X(self):
        """朋友圈页的从相册选择按钮X"""
        return self.get_int('BTN_SELECT_FROM_ALBUM_CIRCLE_X')
    
    @property
    def BTN_SELECT_FROM_ALBUM_CIRCLE_Y(self):
        """朋友圈页的从相册选择按钮Y"""
        return self.get_int('BTN_SELECT_FROM_ALBUM_CIRCLE_Y')
    
    @property
    def BTN_SEND_CIRCLE_X(self):
        """发送朋友圈的发送按钮X"""
        return self.get_int('BTN_SEND_CIRCLE_X')
    
    @property
    def BTN_SEND_CIRCLE_Y(self):
        """发送朋友圈的发送按钮Y"""
        return self.get_int('BTN_SEND_CIRCLE_Y')
    
    @property
    def BTN_EXIT_SEND_CIRCLE_EDIT_X(self):
        """发送朋友圈编辑的退出确认按钮X"""
        return self.get_int('BTN_EXIT_SEND_CIRCLE_EDIT_X')
    
    @property
    def BTN_EXIT_SEND_CIRCLE_EDIT_Y(self):
        """发送朋友圈编辑的退出确认按钮Y"""
        return self.get_int('BTN_EXIT_SEND_CIRCLE_EDIT_Y')
    
    # ===== 编辑框坐标 =====
    
    @property
    def EDIT_CHAT_FOR_SEND_X(self):
        """消息编辑框X"""
        return self.get_int('EDIT_CHAT_FOR_SEND_X')
    
    @property
    def EDIT_CHAT_FOR_SEND_Y(self):
        """消息编辑框Y"""
        return self.get_int('EDIT_CHAT_FOR_SEND_Y')
    
    @property
    def EDIT_ADD_FRIEND_X(self):
        """添加好友编辑框X"""
        return self.get_int('EDIT_ADD_FRIEND_X', need_offset_x=True)
    
    @property
    def EDIT_ADD_FRIEND_Y(self):
        """添加好友编辑框Y"""
        return self.get_int('EDIT_ADD_FRIEND_Y', need_offset_y=True)
    
    @property
    def EDIT_REMARK_APPLY_ADD_X(self):
        """申请添加好友页面备注编辑框X"""
        return self.get_int('EDIT_REMARK_APPLY_ADD_X')
    
    @property
    def EDIT_REMARK_APPLY_ADD_Y(self):
        """申请添加好友页面备注编辑框Y"""
        return self.get_int('EDIT_REMARK_APPLY_ADD_Y')
    
    @property
    def EDIT_WENAN_SEND_CIRCLE_X(self):
        """发送朋友圈文案编辑框X"""
        return self.get_int('EDIT_WENAN_SEND_CIRCLE_X')
    
    @property
    def EDIT_WENAN_SEND_CIRCLE_Y(self):
        """发送朋友圈文案编辑框Y"""
        return self.get_int('EDIT_WENAN_SEND_CIRCLE_Y')
    
    @property
    def EDIT_SEARCH_CAN_SEE_X(self):
        """搜索可见好友栏编辑框X"""
        return self.get_int('EDIT_SEARCH_CAN_SEE_X')
    
    @property
    def EDIT_SEARCH_CAN_SEE_Y(self):
        """搜索可见好友栏编辑框Y"""
        return self.get_int('EDIT_SEARCH_CAN_SEE_Y')
    
    # ===== 关闭/完成类按钮 =====
    
    @property
    def BTN_CLOSE_SETTING_X(self):
        """设置页面关闭按钮X"""
        return self.get_int('BTN_CLOSE_SETTING_X')
    
    @property
    def BTN_CLOSE_SETTING_Y(self):
        """设置页面关闭按钮Y"""
        return self.get_int('BTN_CLOSE_SETTING_Y')
    
    @property
    def BTN_CLOSE_ADD_TO_FRIENDBOOK_X(self):
        """添加到通讯录页面关闭按钮X"""
        return self.get_int('BTN_CLOSE_ADD_TO_FRIENDBOOK_X')
    
    @property
    def BTN_CLOSE_ADD_TO_FRIENDBOOK_Y(self):
        """添加到通讯录页面关闭按钮Y"""
        return self.get_int('BTN_CLOSE_ADD_TO_FRIENDBOOK_Y')
    
    @property
    def BTN_CLOSE_ADD_TO_FRIENDBOOK_NO_EXIST_X(self):
        """添加到通讯录页面(好友不存在)关闭按钮X"""
        return self.get_int('BTN_CLOSE_ADD_TO_FRIENDBOOK_NO_EXIST_X')
    
    @property
    def BTN_CLOSE_ADD_TO_FRIENDBOOK_NO_EXIST_Y(self):
        """添加到通讯录页面(好友不存在)关闭按钮Y"""
        return self.get_int('BTN_CLOSE_ADD_TO_FRIENDBOOK_NO_EXIST_Y')
    
    @property
    def BTN_FINISH_WHO_CAN_SEE_X(self):
        """"谁可以看"页面的完成按钮X"""
        return self.get_int('BTN_FINISH_WHO_CAN_SEE_X')
    
    @property
    def BTN_FINISH_WHO_CAN_SEE_Y(self):
        """"谁可以看"页面的完成按钮Y"""
        return self.get_int('BTN_FINISH_WHO_CAN_SEE_Y')
    
    # ===== 聊天页按钮 =====
    
    @property
    def BTN_CHAT_ADD_X(self):
        """聊天页加号按钮X"""
        return self.get_int('BTN_CHAT_ADD_X')
    
    @property
    def BTN_CHAT_ADD_Y(self):
        """聊天页加号按钮Y"""
        return self.get_int('BTN_CHAT_ADD_Y')
    
    @property
    def BTN_CHAT_ALBUM_X(self):
        """聊天页相册按钮X"""
        return self.get_int('BTN_CHAT_ALBUM_X')
    
    @property
    def BTN_CHAT_ALBUM_Y(self):
        """聊天页相册按钮Y"""
        return self.get_int('BTN_CHAT_ALBUM_Y')
    
    @property
    def BTN_SEND_IMG_X(self):
        """发送图片按钮X"""
        return self.get_int('BTN_SEND_IMG_X')
    
    @property
    def BTN_SEND_IMG_Y(self):
        """发送图片按钮Y"""
        return self.get_int('BTN_SEND_IMG_Y')
    
    @property
    def BTN_SEND_X(self):
        """发送按钮X"""
        return self.get_int('BTN_SEND_X', need_offset_x=True)
    
    @property
    def BTN_SEND_Y(self):
        """发送按钮Y"""
        return self.get_int('BTN_SEND_Y', need_offset_y=True)
    
    # ===== 选择/点击类按钮 =====
    
    @property
    def BTN_PART_CAN_SEE_X(self):
        """部分可见按钮X"""
        return self.get_int('BTN_PART_CAN_SEE_X')
    
    @property
    def BTN_PART_CAN_SEE_Y(self):
        """部分可见按钮Y"""
        return self.get_int('BTN_PART_CAN_SEE_Y')
    
    @property
    def BTN_SELECT_FRIEND_X(self):
        """选择朋友按钮X"""
        return self.get_int('BTN_SELECT_FRIEND_X')
    
    @property
    def BTN_SELECT_FRIEND_Y(self):
        """选择朋友按钮Y"""
        return self.get_int('BTN_SELECT_FRIEND_Y')
    
    @property
    def BTN_SELECT_OF_SELECT_FRIEND_PAGE_X(self):
        """选择朋友页面的选择按钮X"""
        return self.get_int('BTN_SELECT_OF_SELECT_FRIEND_PAGE_X')
    
    @property
    def BTN_SELECT_OF_SELECT_FRIEND_PAGE_Y(self):
        """选择朋友页面的选择按钮Y"""
        return self.get_int('BTN_SELECT_OF_SELECT_FRIEND_PAGE_Y')
    
    @property
    def BTN_IGNORE_SAVE_LABEL_X(self):
        """"保存为标签"页面的忽略按钮X"""
        return self.get_int('BTN_IGNORE_SAVE_LABEL_X')
    
    @property
    def BTN_IGNORE_SAVE_LABEL_Y(self):
        """"保存为标签"页面的忽略按钮Y"""
        return self.get_int('BTN_IGNORE_SAVE_LABEL_Y')
    
    @property
    def BTN_I_KNOW_CIRCLE_PHOTO_X(self):
        """"拍照记录生活"页面的我知道按钮X"""
        return self.get_int('BTN_I_KNOW_CIRCLE_PHOTO_X')
    
    @property
    def BTN_I_KNOW_CIRCLE_PHOTO_Y(self):
        """"拍照记录生活"页面的我知道按钮Y"""
        return self.get_int('BTN_I_KNOW_CIRCLE_PHOTO_Y')
    
    @property
    def BTN_SELECT_FRIEND_SEARCHED_X(self):
        """选择搜索到的用户X"""
        return self.get_int('BTN_SELECT_FRIEND_SEARCHED_X')
    
    @property
    def BTN_SELECT_FRIEND_SEARCHED_Y(self):
        """选择搜索到的用户Y"""
        return self.get_int('BTN_SELECT_FRIEND_SEARCHED_Y')
    
    @property
    def BTN_ALBUM_FIRST_IMG_X(self):
        """相册第一张图片按钮X"""
        return self.get_int('BTN_ALBUM_FIRST_IMG_X')
    
    @property
    def BTN_ALBUM_FIRST_IMG_Y(self):
        """相册第一张图片按钮Y"""
        return self.get_int('BTN_ALBUM_FIRST_IMG_Y')
    
    # ===== 长按发送朋友圈按钮范围 =====
    
    @property
    def BTN_LONGPRESS_SEND_CIRCLE_BOT_X(self):
        """长按起始X"""
        return self.get_int('BTN_LONGPRESS_SEND_CIRCLE_BOT_X')
    
    @property
    def BTN_LONGPRESS_SEND_CIRCLE_BOT_Y(self):
        """长按起始Y"""
        return self.get_int('BTN_LONGPRESS_SEND_CIRCLE_BOT_Y')
    
    @property
    def BTN_LONGPRESS_SEND_CIRCLE_TOP_X(self):
        """长按结束X"""
        return self.get_int('BTN_LONGPRESS_SEND_CIRCLE_TOP_X')
    
    @property
    def BTN_LONGPRESS_SEND_CIRCLE_TOP_Y(self):
        """长按结束Y"""
        return self.get_int('BTN_LONGPRESS_SEND_CIRCLE_TOP_Y')
    
    # ===== 截图区域相关 (返回元组) =====
    
    def get_friend_list_bbox(self):
        """获取好友列表截图区域 (x1, y1, x2, y2)"""
        try:
            x1 = self.get_int('FRIEND_LIST_BBOX_X1', need_offset_x=True)
            y1 = self.get_int('FRIEND_LIST_BBOX_Y1', need_offset_y=True)
            x2 = self.get_int('FRIEND_LIST_BBOX_X2')
            y2 = self.get_int('FRIEND_LIST_BBOX_Y2')
            return (x1, y1, x2, y2)
        except:
            # 如果配置不存在，返回基于好友列表坐标计算的默认值
            return (self.FRIEND_CHAT_LIST_LT_X, self.FRIEND_CHAT_LIST_LT_Y, 399, 984)
    
    def get_friend_info_bbox(self):
        """获取好友信息页截图区域 (x1, y1, x2, y2)"""
        try:
            x1 = self.get_int('FRIEND_INFO_BBOX_X1', need_offset_x=True)
            y1 = self.get_int('FRIEND_INFO_BBOX_Y1', need_offset_y=True)
            x2 = self.get_int('FRIEND_INFO_BBOX_X2', need_offset_x=True)
            y2 = self.get_int('FRIEND_INFO_BBOX_Y2', need_offset_y=True)
            return (x1, y1, x2, y2)
        except:
            # 返回基于昵称坐标的默认值
            return (self.NICKNAME_RB_X + G_X_PIAN_YI, self.NICKNAME_RB_Y + G_Y_PIAN_YI, 
                    399 + G_X_PIAN_YI, 986 + G_Y_PIAN_YI)
    
    def get_chat_title_bbox(self):
        """获取聊天窗口标题截图区域 (x1, y1, x2, y2)"""
        try:
            x1 = self.get_int('CHAT_TITLE_BBOX_X1', need_offset_x=True)
            y1 = self.get_int('CHAT_TITLE_BBOX_Y1', need_offset_y=True)
            x2 = self.get_int('CHAT_TITLE_BBOX_X2', need_offset_x=True)
            y2 = self.get_int('CHAT_TITLE_BBOX_Y2', need_offset_y=True)
            return (x1, y1, x2, y2)
        except:
            return (421 + G_X_PIAN_YI, 41 + G_Y_PIAN_YI, 866 + G_X_PIAN_YI, 85 + G_Y_PIAN_YI)
    
    def get_chat_content_bbox(self):
        """获取聊天内容截图区域 (x1, y1, x2, y2)"""
        try:
            x1 = self.get_int('CHAT_CONTENT_BBOX_X1', need_offset_x=True)
            y1 = self.get_int('CHAT_CONTENT_BBOX_Y1', need_offset_y=True)
            x2 = self.get_int('CHAT_CONTENT_BBOX_X2', need_offset_x=True)
            y2 = self.get_int('CHAT_CONTENT_BBOX_Y2', need_offset_y=True)
            return (x1, y1, x2, y2)
        except:
            # 使用聊天窗口左上角坐标
            return (self.CHAT_LT_X, self.CHAT_LT_Y, 1044 + G_X_PIAN_YI, 761 + G_Y_PIAN_YI)
    
    def get_tag_select_bbox(self):
        """获取标签选择页截图区域 (x1, y1, x2, y2)"""
        try:
            x1 = self.get_int('TAG_SELECT_BBOX_X1', need_offset_x=True)
            y1 = self.get_int('TAG_SELECT_BBOX_Y1', need_offset_y=True)
            x2 = self.get_int('TAG_SELECT_BBOX_X2', need_offset_x=True)
            y2 = self.get_int('TAG_SELECT_BBOX_Y2', need_offset_y=True)
            return (x1, y1, x2, y2)
        except:
            return (198 + G_X_PIAN_YI, 155 + G_Y_PIAN_YI, 404 + G_X_PIAN_YI, 986 + G_Y_PIAN_YI)
    
    # ===== Windows特有坐标 =====
    
    @property
    def SEARCH_INPUT_X(self):
        """搜索输入框X坐标"""
        return self.get_int('SEARCH_INPUT_X', need_offset_x=True, default=157)
    
    @property
    def SEARCH_INPUT_Y(self):
        """搜索输入框Y坐标"""
        return self.get_int('SEARCH_INPUT_Y', need_offset_y=True, default=63)
    
    @property
    def REMARK_EDIT_BTN_X(self):
        """备注编辑按钮X"""
        return self.get_int('REMARK_EDIT_BTN_X', default=50)
    
    @property
    def REMARK_EDIT_BTN_Y(self):
        """备注编辑按钮Y"""
        return self.get_int('REMARK_EDIT_BTN_Y', default=325)
    
    @property
    def SEND_MSG_BTN_X(self):
        """发送消息按钮X"""
        return self.get_int('SEND_MSG_BTN_X', need_offset_x=True, default=983)
    
    @property
    def SEND_MSG_BTN_Y(self):
        """发送消息按钮Y"""
        return self.get_int('SEND_MSG_BTN_Y', need_offset_y=True, default=939)


# 创建全局配置实例
try:
    g_location_config = LocationConfig()
    print_my("全局坐标配置实例创建成功")
except Exception as e:
    print_my(f"!!!!! 创建全局坐标配置实例失败: {e}")
    g_location_config = None

