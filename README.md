# 微信私域精灵（Windows RPA 版）

基于 Python 的微信桌面客户端自动化助手（Windows RPA）。通过窗口嵌入、截图识别（OCR + 像素分析）、模拟输入等技术，把 PC 版微信接入私域运营工作流：自动回复、好友管理、朋友圈发布、智能话术等。

> 本项目仅供学习交流自动化与 RPA 技术使用，请遵守微信相关使用条款，勿用于违规用途。

## 功能特性

- **窗口嵌入**：将微信主窗口以子窗口形式嵌入程序右侧面板，统一托管
- **页面识别**：OCR 文本特征 + 导航栏像素颜色双通道识别当前页面（消息列表 / 聊天页 / 服务通知页等）
- **自动回复**：接入多家 LLM（Kimi、通义千问、DeepSeek、智谱 GLM、豆包、Gemini、讯飞星火等）生成智能话术
- **话术库**：支持本地自定义话术库（txt），按关键词匹配回复
- **好友管理**：待添加好友列表批量处理、通过好友请求
- **朋友圈**：自动发布朋友圈（文字 / 图片）
- **输入托管**：运行期间接管键鼠输入防止误操作，**物理 ESC 键为紧急停止**
- **客户端上报**：向服务端上报机器信息、拉取云端配置、登录校验
- **打包发布**：PyInstaller + Inno Setup 一键产出安装包

## 技术栈

| 类别 | 组件 |
|---|---|
| 语言 | Python 3.7（Anaconda 环境） |
| GUI | PyQt5 |
| 窗口自动化 | pywin32（win32gui/win32con）、pywinauto |
| 图像处理 | Pillow、OpenCV (opencv-python) |
| 文字识别 | 远程 OCR 服务（HTTP 接口） |
| LLM | openai / zhipuai / spark-ai-python 等多家 SDK |
| 网络通信 | requests、websocket-client |
| 其他 | cryptography（配置加解密）、openpyxl、qrcode |

## 目录结构（关键文件）

```
main.py                          # 程序入口：GUI、主工作线程、检测线程
yang_hao_opt.py                  # 核心自动化流程（页面判定、消息处理、好友/朋友圈操作）
yang_hao_opt_helper_of_windows.py# Windows 平台辅助（窗口查找/嵌入/置顶、截图）
llm_helper.py                    # 多家 LLM 接入封装
test_my_ocr.py                   # OCR 服务调用
server_http_opt.py               # 服务端 HTTP 通信（上报/配置/登录）
config_helper.py                 # 配置文件读写（加密存储）
windows_helper.py                # 键鼠钩子、输入屏蔽、紧急停止
phone_sms_opt_aliyun.py          # 阿里云短信
agent_helper.py                  # 讯飞星火智能体
pic_button.py                    # 自绘按钮控件
pack.py                          # 打包脚本（PyInstaller + Inno Setup）
location.cfg                     # 坐标/分辨率配置
```

## 快速开始

### 环境准备

1. Python 3.7.x（项目在 Anaconda base 环境下开发验证）
2. 安装依赖：

```bash
pip install PyQt5 pywinauto pywin32 Pillow opencv-python==4.5.5.64 \
    openpyxl requests websocket-client cryptography qrcode \
    openai==1.16.2 zhipuai==2.0.1 typing_extensions==4.7.1
```

3. PC 版微信（3.x / 4.x 均可，窗口标题「微信」）已安装并可登录

### 配置 API 密钥

代码中的 API 密钥**均已脱敏为占位符**（如 `YOUR_KIMI_API_KEY`），运行前请替换为真实密钥：

| 文件 | 说明 |
|---|---|
| `llm_helper.py` | 各 LLM 服务的 api_key（Kimi/Qwen/DeepSeek/GLM/豆包等） |
| `test_my_ocr.py` | OCR 服务 X-API-Key |
| `test_baidu_ocr.py` | 阿里云视觉智能（可选） |
| `agent_helper.py` | 讯飞星火（可选） |
| `phone_sms_opt_aliyun.py` | 阿里云短信（可选） |

### 运行

```bash
python main.py
```

启动后：登录微信 → 程序自动将微信窗口嵌入右侧面板 → 点击「开始」进入自动化工作流。

**运行期间注意**：
- 输入托管开启后键鼠被屏蔽，**按下物理 ESC 键可紧急停止并解除屏蔽**
- 请勿在运行中手动操作微信窗口（移动/最小化会导致窗口位置校验失败）

### 打包

```bash
python pack.py --compress 0   # 不压缩
python pack.py --compress 1   # UPX 压缩
```

产出：`dist\main\`（目录版）与 `wechatSiYuGenie_WindowsRPA_V1.0_Install.exe`（安装包，需 Inno Setup 6）。

## 数据目录

运行时数据（日志、截图、配置）存放于：

```
%APPDATA%\wechatSiYuGenie_WindowsRPA\
```

## 已知兼容性说明（Python 3.7）

项目在 Python 3.7 环境下做过大量兼容处理，迁移环境时注意：

- 源码使用 `from __future__ import annotations` 规避 PEP 585/604 注解语法
- 部分新版 SDK（spark-ai-python、websocket-client 等）的低版本已做 3.7 兼容修补
- `sitecustomize.py` 注入了 `typing.Literal/Protocol` 等新名称（Python 3.8+ 才进入标准库 typing）
- `QFontMetrics.horizontalAdvance()` 需 PyQt5 ≥ 5.11，代码中已做 `width()` 回退

## License

仅供学习交流，请自行承担使用风险。
