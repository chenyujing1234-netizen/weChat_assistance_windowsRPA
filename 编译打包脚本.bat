@echo off
echo ========================================
echo 编译Inno Setup打包脚本
echo ========================================
echo.

echo 正在编译打包脚本...
"E:\Program Files (x86)\Inno Setup 6\ISCC.exe" "个微私域精灵打包脚本.iss"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 编译成功！
    echo 安装包已生成：wechatSiYuGenie_WindowsRPA_V1.0_Install.exe
) else (
    echo.
    echo 编译失败，请检查脚本内容
)

echo.
pause