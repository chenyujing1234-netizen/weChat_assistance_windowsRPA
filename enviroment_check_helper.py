# -*- coding: utf-8 -*-
import subprocess
import psutil
import os
import re
import winreg
import ctypes
import sys
import wmi

def check_virtualization():
    result = subprocess.run(['systeminfo'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    output = result.stdout
    if 'Virtualization Enabled In Firmware: Yes' in output:
        return True
    elif "固件中已启用虚拟化: 是" in output:
        return True
    elif "将不显示 Hyper-V 所需的功能" in output or "将不显示Hyper-V所需的功能" in output:
        return True 
    else:
        return False

#virtualization_enabled = check_virtualization()
#print("Virtualization is enabled:", virtualization_enabled)

# 判断是不是有雷电应用程序在运行
def is_another_lei_dian_running(): 
    PROCESS_NAME_OF_LEIDIAN = 'dnplayer.exe'
    process_path = ""
    
    # 获得当前目录  
    current_directory = os.getcwd()
    
    # 获取所有进程信息
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        if proc.info['name'] == PROCESS_NAME_OF_LEIDIAN:
            process_path = proc.info['exe']
            break
    if len(process_path) <= 0:
        return False 

    if current_directory not in process_path:
        print("当前的进程是在:{},不在当前目录:{}".format(process_path, current_directory))
        return True 

    return False 

# 判断是否有360在运行
def is_360_running():
    PROCESS_NAME_LIST_OF_360 = [
        "360sd.exe",      # 360杀毒主程序
        "360tray.exe",    # 360托盘程序
        "360safe.exe",    # 360安全卫士主程序
        "360rp.exe",      # 360实时保护程序
        "360sp.exe",      # 360安全防护中心
        "360netmon.exe",  # 360网络监控
    ]
    process_path = ""
    
    # 获取所有进程信息
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        if proc.info['name'] in PROCESS_NAME_LIST_OF_360:
            process_path = proc.info['exe']
            break
    if len(process_path) > 0:
        return True 
    
    return False 

# 判断windows中的defender是否打开
def is_windows_defender_enabled():
    try:
        # 使用 PowerShell 命令检查 Defender 的状态
        command = "Get-MpComputerStatus"
        result = subprocess.run(
            ["powershell", "-Command", command],   # 用 -Command 更稳妥
            capture_output=True,
            text=True,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # 关键：无窗口
        )
        output = result.stdout
        # 检查输出中是否包含 Defender 的相关状态信息
        if "AMServiceEnabled" in output and "RealTimeProtectionEnabled" in output:
            # 使用正则表达式提取状态信息
            am_service_enabled = re.search(r"AMServiceEnabled\s+:\s+(\w+)", output)
            real_time_protection_enabled = re.search(r"RealTimeProtectionEnabled\s+:\s+(\w+)", output)
            if am_service_enabled and real_time_protection_enabled:
                return am_service_enabled.group(1).strip() == "True" and real_time_protection_enabled.group(1).strip() == "True"
    except Exception as e:
        print(f"发生错误：{e}")
    return False

# 打开windows中的defender面板
def open_windows_defender_panel():
    # 方法1：使用 windowsdefender:// URI
    subprocess.run(["start", "windowsdefender://"], 
                   shell=True)

    # 方法2：使用 ms-settings:windowsdefender URI（打开设置中的“Windows 安全”）
    # subprocess.run(["start", "ms-settings:windowsdefender"], shell=True)
    return 

def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def disable_defender_registry():
    """通过注册表禁用Windows Defender（需重启生效）"""
    if not is_admin():
        print("当前没有管理员权限，请以管理员权限运行此程序")
        # 重新以管理员权限运行
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        print("是获得了权限了？")
        return False
    try:
        # 定位到 Defender 的注册表路径
        key_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
        
        # 创建或打开注册表项（以管理员权限）
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            # 设置DisableAntiSpyware值为1（禁用Defender）
            winreg.SetValueEx(key, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
            print("注册表修改成功！重启后Windows Defender将被禁用。")
            return True
    
    except PermissionError:
        print("disable_defender_registry, 错误：需要管理员权限运行此脚本。")
        return False
    except Exception as e:
        print(f"disable_defender_registry, 操作失败: {str(e)}")
        return False
    return False

########################### 检查是否在虚拟机中运行###############################
# 1. WMI 检查主板、BIOS 厂商/型号 -----------------------------------------
def check_is_virtual_machine_by_wmi():
    try:
        c = wmi.WMI()
        clues = ["virtual", "vmware", "virtualbox", "qemu", "kvm", "hyper-v"]
        for board in c.Win32_BaseBoard():
            txt = (board.Manufacturer or "") + " " + (board.Product or "")
            if any(c in txt.lower() for c in clues):
                print("check_is_virtual_machine_by_wmi, 判断到是在虚拟机中运行1")
                return True
        for bios in c.Win32_BIOS():
            txt = (bios.Manufacturer or "") + " " + (bios.SMBIOSBIOSVersion or "")
            if any(c in txt.lower() for c in clues):
                print("check_is_virtual_machine_by_wmi, 判断到是在虚拟机中运行2")
                return True
    except Exception:
        pass
    return False

# 2. 进程名检查 -----------------------------------------------------------
def check_is_virtual_machine_by_processes():
    vm_procs = {
        "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe", "vmacthlp.exe",
        "vboxservice.exe", "vboxtray.exe",
        "vmsrvc.exe", "vmusrvc.exe", "vpcmap.exe"
    }
    try:
        for p in psutil.process_iter(['name']):
            name = (p.info['name'] or "").lower()
            if name in vm_procs:
                print("check_is_virtual_machine_by_processes, 判断到是在虚拟机中运行")
                return True
    except Exception:
        pass
    return False

# 4. CPUID（可选，需要 pip install pycpuid） -------------------------------
def check_is_virtual_machine_by_cpuid():
    try:
        import pycpuid
        if pycpuid.hypervisor_present():
            print("check_is_virtual_machine_by_cpuid, 判断到是在虚拟机中运行")
            return True
    except Exception:
        pass
    return False

# 判断是不是在虚拟机里运行
def is_virtual_machine():
    return any([
        check_is_virtual_machine_by_wmi(),
        check_is_virtual_machine_by_processes(),
        check_is_virtual_machine_by_cpuid()
    ])
"""
if is_virtual_machine():
    print("当前系统运行在虚拟机中")
else:
    print("当前系统未检测到虚拟化特征")
"""
