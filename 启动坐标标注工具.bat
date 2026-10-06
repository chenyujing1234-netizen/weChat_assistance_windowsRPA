@echo off
chcp 65001 >nul
title 微信坐标标注工具
echo.
echo ========================================
echo    微信坐标标注工具启动中...
echo ========================================
echo.

python location_annotation_tool.py

if errorlevel 1 (
    echo.
    echo [错误] 工具启动失败！
    echo.
    echo 可能原因：
    echo 1. Python未安装或未添加到PATH
    echo 2. PyQt5未安装 (运行: pip install PyQt5)
    echo 3. 其他依赖缺失
    echo.
    pause
)

