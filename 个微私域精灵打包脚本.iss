[Setup]
AppName=个微私域精灵WindowsRPA版
AppVersion=1.0
DefaultDirName={pf}\wechatSiYuGenie_WindowsRPA
DefaultGroupName=个微私域精灵WindowsRPA版
OutputDir=D:\weChat_assistance
OutputBaseFilename=wechatSiYuGenie_WindowsRPA_V1.0_Install
Compression=lzma
SolidCompression=yes
SetupIconFile=D:\weChat_assistance\img\logo.ico
UninstallDisplayIcon={app}\个微私域精灵V1.0_WindowsRPA版.exe
PrivilegesRequired=admin
; 禁用修改安装目录的选项，使安装路径固定
UsePreviousAppDir=no
DisableDirPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加图标:"

[Dirs]
; 在用户数据目录创建程序需要的文件夹
Name: "{userappdata}\wechatSiYuGenie_WindowsRPA"
Name: "{userappdata}\wechatSiYuGenie_WindowsRPA\message_sessions"
Name: "{userappdata}\wechatSiYuGenie_WindowsRPA\screenshot_img"
Name: "{userappdata}\wechatSiYuGenie_WindowsRPA\ai_generate_img"
Name: "{userappdata}\wechatSiYuGenie_WindowsRPA\Tesseract-OCR"
Name: "{userappdata}\wechatSiYuGenie_WindowsRPA\TuoGuanContainer"

[Files]
Source: "D:\weChat_assistance\dist\main\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\个微私域精灵WindowsRPA版"; Filename: "{app}\个微私域精灵V1.0_WindowsRPA版.exe"
Name: "{commondesktop}\个微私域精灵WindowsRPA版"; Filename: "{app}\个微私域精灵V1.0_WindowsRPA版.exe"; Tasks: desktopicon

[INI]
Filename: "{app}\config.ini"; Section: "Paths"; Key: "UserDataDir"; String: "{userappdata}\wechatSiYuGenie_WindowsRPA"

[Run]
Filename: "{app}\个微私域精灵V1.0_WindowsRPA版.exe"; Description: "启动个微私域精灵WindowsRPA版"; Flags: nowait postinstall skipifsilent