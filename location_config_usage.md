# 坐标配置系统使用说明

## 概述
本项目已将分散在`yang_hao_opt.py`中的硬编码坐标值统一整理到配置文件`location.cfg`中，并通过`location_config.py`模块提供统一的读取接口。

## 文件说明

### 1. location.cfg
配置文件，包含所有平台的坐标定义：
- `[Local_Emulator]` - 本地模拟器 (1080*1920)
- `[WiFi_Phone_Xiaomi_8_Pro]` - 小米8 Pro (1080*2340)
- `[Yun_Phone_720_1080]` - 云手机 (720*1080)
- `[Windows]` - Windows PC微信 (1080*1920)
- `[Windows_1366_768]` - Windows低分辨率版本

### 2. location_config.py
坐标配置管理模块，提供：
- 自动根据当前设备类型加载对应配置
- 属性方式访问所有坐标值
- Windows平台自动叠加G_X_PIAN_YI和G_Y_PIAN_YI偏移量
- 配置缺失时的兜底机制

### 3. yang_hao_opt.py
已修改为从配置文件读取坐标

## 使用方法

### 在代码中使用坐标配置

```python
# 导入全局配置实例
from location_config import g_location_config

# 使用屏幕尺寸
screen_width = g_location_config.W_SCREEN
screen_height = g_location_config.H_SCREEN

# 使用好友列表坐标（自动处理偏移量）
friend_list_x = g_location_config.FRIEND_CHAT_LIST_LT_X
friend_list_y = g_location_config.FRIEND_CHAT_LIST_LT_Y

# 使用聊天窗口坐标
chat_x = g_location_config.CHAT_LT_X
chat_y = g_location_config.CHAT_LT_Y

# 使用按钮坐标
btn_x = g_location_config.BTN_NAV_WEIXIN_X
btn_y = g_location_config.BTN_NAV_WEIXIN_Y

# 使用截图区域（返回元组）
friend_list_bbox = g_location_config.get_friend_list_bbox()  # (x1, y1, x2, y2)
chat_content_bbox = g_location_config.get_chat_content_bbox()
```

## 坐标分类

### 屏幕尺寸
- `W_SCREEN` - 屏幕宽度
- `H_SCREEN` - 屏幕高度

### 好友列表区域
- `FRIEND_CHAT_LIST_LT_X` - 好友列表左上角X坐标
- `FRIEND_CHAT_LIST_LT_Y` - 好友列表左上角Y坐标

### 聊天窗口区域
- `CHAT_LT_X` - 聊天窗口左上角X坐标
- `CHAT_LT_Y` - 聊天窗口左上角Y坐标
- `CHAT_LINE_HEIGHT` - 聊天记录行高
- `CHAT_LINE_HEIGHT_INTER` - 聊天记录行间距
- `CHAT_MIN_Y_FOR_OCR` - OCR识别最小Y坐标
- `CHAT_MAX_Y_FOR_OCR` - OCR识别最大Y坐标
- `CHAT_LT_X_SHOULD_MIN` - 聊天文本左边界最小X
- `CHAT_RB_X_SHOULD_MIN` - 聊天文本右边界最小X

### 好友资料页
- `NICKNAME_RB_X` - 好友昵称区域右下角X
- `NICKNAME_RB_Y` - 好友昵称区域右下角Y

### 按钮坐标
- `BTN_NAV_WEIXIN_X/Y` - 微信按钮
- `BTN_NAV_CONTACTS_X/Y` - 通讯录按钮
- `BTN_NAV_DISCOVER_X/Y` - 发现按钮
- `BTN_NAV_ME_X/Y` - 我按钮
- `ADD_FRIEND_BTN_X/Y` - 添加好友按钮
- `SEARCH_BTN_X/Y` - 搜索按钮
- `BACK_BTN_X/Y` - 返回按钮

### 截图区域方法
- `get_friend_list_bbox()` - 好友列表截图区域
- `get_friend_info_bbox()` - 好友信息页截图区域
- `get_chat_title_bbox()` - 聊天标题截图区域
- `get_chat_content_bbox()` - 聊天内容截图区域
- `get_tag_select_bbox()` - 标签选择页截图区域

## 修改坐标值

### 修改配置文件
直接编辑`location.cfg`文件，修改对应平台section下的坐标值：

```ini
[Windows]
# 修改好友列表坐标
FRIEND_CHAT_LIST_LT_X = 102
FRIEND_CHAT_LIST_LT_Y = 120

# 修改聊天窗口坐标
CHAT_LT_X = 413
CHAT_LT_Y = 106
```

### 注意事项
1. Windows平台的部分坐标会自动叠加`G_X_PIAN_YI`和`G_Y_PIAN_YI`偏移量
2. 需要叠加偏移的坐标在配置文件中已标注
3. 修改配置后需要重启程序
4. 建议先备份原配置再修改

## 添加新坐标

### 1. 在location.cfg中添加
在所有平台的section下添加新坐标：

```ini
[Windows]
NEW_BUTTON_X = 100
NEW_BUTTON_Y = 200
```

### 2. 在location_config.py中添加属性
```python
@property
def NEW_BUTTON_X(self):
    """新按钮X坐标"""
    return self.get_int('NEW_BUTTON_X', need_offset_x=True, default=100)

@property
def NEW_BUTTON_Y(self):
    """新按钮Y坐标"""
    return self.get_int('NEW_BUTTON_Y', need_offset_y=True, default=200)
```

### 3. 在代码中使用
```python
new_btn_x = g_location_config.NEW_BUTTON_X
new_btn_y = g_location_config.NEW_BUTTON_Y
```

## 调试
如果坐标配置加载失败，可以查看日志输出：
- 成功加载：`成功加载坐标配置文件: location.cfg, 设备类型: Windows`
- 加载失败：`!!!!! 坐标配置文件不存在: location.cfg`
- 配置项缺失：`警告: 配置项 [Windows]XXX 不存在或格式错误，使用默认值`

## 兜底机制
代码中保留了原有的硬编码逻辑作为兜底，当配置文件加载失败时会自动使用原有逻辑，确保程序正常运行。

## 迁移清单
✅ 已完成迁移的坐标配置：
- 屏幕尺寸 (W_SCREEN, H_SCREEN)
- 好友列表坐标 (FRIEND_CHAT_LIST_LT_X/Y)
- 聊天窗口坐标 (CHAT_LT_X/Y)
- 聊天相关参数 (行高、OCR范围、文本边界等)
- 好友资料页坐标 (NICKNAME_RB_X/Y)
- 权限申请页坐标 (QUXIAN_CANCEL_LT_X/Y)

🔄 部分迁移（主要配置已完成）：
- 底部导航栏按钮坐标
- 各类功能按钮坐标
- 截图区域坐标

⚠️ 待完成迁移：
- 代码中散落的其他特定按钮坐标（需要根据实际使用情况逐步迁移）

## 维护建议
1. 新增坐标时优先使用配置文件
2. 定期检查配置文件完整性
3. 修改坐标后进行充分测试
4. 保持配置文件注释的准确性

