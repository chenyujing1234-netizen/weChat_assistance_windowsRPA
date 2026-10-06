# coding: utf-8
# 将 C:\Users\admin\anaconda3\envs\chenyj\Scripts  添加到环境变量PATH中
import os
import sys
import shutil
import zipfile
import time
from log_helper import print_my
from app_info import *
import argparse
import glob
from pathlib import Path

DIST_DIR = ".\\dist\\main\\"
MODEL_DIR = ".\\dist\\main\\_internal\\"
TESSERACT_DIST_DIR = DIST_DIR + TESSERACT_DIR + "\\"
LEI_DIAN_DIST_DIR = DIST_DIR + LEI_DIAN_DIR + "\\"

# 方式一：不压缩
# python pack.py --compress 0
# 方式二：压缩
# python pack.py --compress 1

# 参数解析器
parser = argparse.ArgumentParser(description="示例脚本")
parser.add_argument('--compress', type=int, help='是否要压缩', default=1)
args = parser.parse_args()
print(f"是否要压缩: {args.compress}")

def ss(string):
    t = sys.getfilesystemencoding()
    return string.decode('utf-8').encode(t)

def my_exit(status):
    sys.exit(status)

# 拼接命令
upx_str = ""
if args.compress == 1:
    upx_str = "--upx-dir C:\\Users\\admin\\anaconda3\\envs\\chenyj\\Scripts"
#cmd_str = "pyinstaller --hidden-import=PyQt5.QtWidgets --exclude-module=mkl,yaml,h5py,dask,numba,yarl,selenium,xyzservices,scipy,greenlet,jedi,lxml,pandas,menuinst,IPython,numpy,pyarrow,docutils,bokeh,aiohttp,psutil,alabaster {} --noconsole --clean -y main.py".format(upx_str)
#cmd_str = "pyinstaller {} --noconsole --clean -i .\\logo.ico -y main.py".format(upx_str)
cmd_str = "pyinstaller {} --hidden-import=openpyxl.cell._writer --hidden-import=PIL --hidden-import=PIL.Image --collect-submodules=openpyxl --noconsole --clean -i .\\{}\\logo.ico -y main.py --exclude PyQt6".format(upx_str, APP_IMG_DIR)
 

print("要执行的打包命令是:{}".format(cmd_str))
#"""
status = os.system(cmd_str)

#status = os.system("pyinstaller --noconsole --clean -y -F main.py")
#status = os.system("pyinstaller --noconsole --clean -y -p C:\\Users\\admin\\anaconda3\\Lib\\site-packages main.py")
if status != 0:
    my_exit(status)
#"""

####################拷贝等后处理##################################
# 为保证删除成功，这里等待5秒
print("等待5秒")
time.sleep(5)

# 1.将文件重命名
old_name = DIST_DIR + "main.exe"
new_name = "{}\\{}.exe".format(DIST_DIR, APP_NAME)
if os.path.exists(old_name):
    try:
        os.rename(old_name, new_name)
        print(f"文件已从 {old_name} 重命名为 {new_name}")
    except OSError as e:
        print(f"重命名失败: {e}")

# 2.把特定的文件拷到dist目录下
"""
src_dir = ".\\LDPlayer9_wei_xin"
dst_dir = DIST_DIR + LEI_DIAN_DIR
if False == os.path.exists(dst_dir):
    try:
        shutil.copytree(src_dir, dst_dir)
        print("目录{}拷贝成功".format(src_dir))
    except Exception as e:
        print(f"!!!目录{src_dir}拷贝失败：{e}")
"""
# 3.把特定的文件拷到dist目录下
"""
src_dir = ".\\Tesseract-OCR"
dst_dir = TESSERACT_DIST_DIR
if False == os.path.exists(dst_dir):
    try:
        shutil.copytree(src_dir, dst_dir)
        print("目录{}拷贝成功".format(src_dir))
    except Exception as e:
        print(f"!!!目录{src_dir}拷贝失败：{e}")
"""
# 4.把特定的文件拷到dist目录下  
#       拷贝APP_IMG目录下的所有文件
def get_all_files(directory):
    """
    获取目录下所有文件（包括子目录）的完整路径列表
    :param directory: 目标目录路径（字符串或 Path 对象）
    :return: 文件路径字符串列表
    """
    return [str(p) for p in Path(directory).rglob('*') if p.is_file()]
dir_copy_list = [APP_IMG_DIR, APP_HTML_DIR]
for dir_copy in dir_copy_list:
    img_file_path_list = get_all_files(dir_copy)
    os.makedirs(DIST_DIR + dir_copy, exist_ok=True)
    for src_file in img_file_path_list:
        file_name = os.path.basename(src_file)
        dst_file = DIST_DIR + dir_copy + "\\" + file_name
        print(f"dst_file:{dst_file}")
        if False == os.path.exists(dst_file):
            try:
                shutil.copy(src_file, dst_file)
                print("文件{}拷贝成功".format(src_file))
            except Exception as e:
                print(f"!!!文件{src_file}拷贝失败：{e}")
#       拷贝其他指定文件指目录
src_file_list = [
    ".\\cacert.pem", ".\\示例_自定义本地话术库.txt", ".\\示例_自定义本地话术库_销售.txt", 
    ".\\示例_待添加好友微信号列表.txt", ".\\示例_产品文档.txt", ".\\loading.gif", 
    ".\\示例图片.JPG", ".\\location.cfg"]
for src_file in src_file_list:
    dst_file = DIST_DIR + src_file
    if False == os.path.exists(dst_file):
        try:
            shutil.copy(src_file, dst_file)
            print("文件{}拷贝成功".format(src_file))
        except Exception as e:
            print(f"!!!文件{src_file}拷贝失败：{e}")
        
# 4. 把没用的文件夹或文件删除
# "numpy"  "pandas" "psutil", "mkl"
# "PyQt5\\Qt5\\translations", "PyQt5\\Qt5\\resources",
# "pytz",  "tzdata"
dir_remove_list_dict = {
    MODEL_DIR:[
        "multidict", "yaml", "h5py", "dask", "numba", 
        "yarl", "selenium", "xyzservices", "scipy", 
        "greenlet", "jedi", "lxml", "menuinst", "IPython", 
        "pyarrow", "docutils", "bokeh", "bokeh-3.3.4.dist-info", 
        "_argon2_cffi_bindings", "aiohttp", "alabaster", "zstandard", 
        "cryptography-42.0.2.dist-info", "llvmlite", "snappy", "numexpr",
        "wheel-0.43.0.dist-info", "lmdb", "markupsafe", "attrs-23.2.0.dist-info", 
        "bcrypt", "botocore", "nbformat-5.9.2.dist-info", 
        "distributed-2023.11.0.dist-info", "importlib_metadata-7.0.1.dist-info", 
        "jsonschema-4.19.2.dist-info", "jsonschema_specifications", 
        "jsonschema", "rpds", "kiwisolver", "winpty", "lz4-4.3.2.dist-info", 
        "zope", "zmq", "frozenlist", "nbformat", "parso", "contourpy", 
        "tables", "sphinx", "nacl", "lz4", "sqlalchemy", "win32com", 
        "lib2to3", "babel", 
        "playwright", "pywt", "numpy-1.26.4", "gmpy2", "email_validator-2.3.0", "distributed",
        "dateutil", "erfa", "etc", "imagecodecs", "anaconda_catalogs-0.2.0", "APScheduler-3.11.0",
        "astor", "altair", "astropy", "astropy-5.3.4*", "black", "blib2to3", "plotly", "panel",
        "notebook", "tiktoken", "xarray-2023.6.0*", "share", "shapely", "Shapely.libs", "skimage",
        "regex", "sklearn", "nbconvert-7.10.0*", "nbconvert", "statsmodels", "tzdata-2023.3*",
        "jupyterlab", "matplotlib", "numpy-1.26.4*", 
        "websockets-13.0.dist-info"
        ], 
    TESSERACT_DIST_DIR:[
        "doc"], 
    LEI_DIAN_DIST_DIR:[
        "qrcode", "ldmutiplayer"
        ]
    }
# "msvcp*.dll", "tk86t.dll",  "tcl86t.dll", "mkl_def*.dll", "api-ms*.dll", "libxslt.dll", "libexslt.dll", 
# , "Qt5DBus_conda.dll", "Qt5Qml_conda.dll", "Qt5Quick_conda.dll", "Qt5QmlModels_conda.dll", 
# "mkl_def.2.dll", 
file_remove_list_dict = {
    MODEL_DIR:[
        "mkl_vml_*.dll", "mkl_scalapack_*.dll", "mkl_tbb_*.dll", 
        "mkl_sequen*.dll", "mkl_pgi_thread*.dll", "mkl_msg*.dll", 
        "mkl_mc*.dll", "mkl_cdft_core*.dll", "mkl_blacs_*.dll", 
        "yaml.dll", "hdf5*.dll", "snappy.dll", 
        "opengl32sw.dll", "arrow*.dll", "arrow_flight.dll", 
        "libmmd.dll", "libGLESv2.dll", "brotlienc.dll", 
        "libprotobuf.dll", "winpty.dll", "libiomp5md.dll", 
        "libifcoremd.dll", "orc.dll",
        "parquet.dll", "omptarget*.dll", "arrow_dataset.dll", 
        "aws*.dll", "libxml2.dll", "thriftmd.dll", 
        "libwebp.dll", "re2.dll", "ucrtbase.dll", 
        "vccorlib140.dll", "concrt140.dll", "libcurl.dll", 
        "libjpeg.dll", "win32\\mfc140u.dll",
        "_hashlib.pyd", "_uuid.pyd", "iconv.dll", 
        "libblosc2.dll", "freetype.dll", "_decimal.pyd", 
        "vcomp140.dll", "Qt5VirtualKeyboard_conda.dll", 
        "Qt5Pdf_conda.dll", "Qt5WebSockets_conda.dll", 
        "Qt5Svg_conda.dll", "_elementtree.pyd",
        "mkl_avx512.2.dll", "mkl_avx.2.dll", "Qt5Multimedia_conda.dll", "Qt5Quick3DRuntimeRender_conda.dll", 
        "Qt5QuickTemplates2_conda.dll", "Qt5DataVisualization_conda.dll", "Qt5Charts_conda.dll", "Qt5Quick3D_conda.dll",
        "Qt53DRender_conda.dll", "Qt5Location_conda.dll", "Qt5XmlPatterns_conda.dll", 
        "api-ms-win-core-handle-l1-1-0.dll", "api-ms-win-core-profile-l1-1-0.dll", 
        "api-ms-win-core-util-l1-1-0.dll", "api-ms-win-core-string-l1-1-0.dll", "api-ms-win-core-namedpipe-l1-1-0.dll",
        "api-ms-win-core-interlocked-l1-1-0.dll", "archive.dll"
        ], 
    TESSERACT_DIST_DIR:[
        "tessdata\\chi_tra.traineddata", "text2image.exe", "lstmtraining.exe", 
        "lstmeval.exe", "set_unicharset_properties.exe", "mftraining.exe", 
        "shapeclustering.exe", "classifier_tester.exe", "cntraining.exe", 
        "unicharset_extractor.exe", "combine_lang_model.exe" "combine_tessdata.exe", 
        "ambiguous_words.exe", "wordlist2dawg.exe", "dawg2wordlist.exe", 
        "merge_unicharsets.exe", "combine_lang_model.exe", "icuin64.dll", 
        "libeay32.dll", "icudt64.dll", "combine_tessdata.exe"
        ], 
    LEI_DIAN_DIST_DIR:[
        "dnrepairer.exe", "dnmultiplayer.exe", "ldplayerhelper.exe", 
        "aapt.exe" "ldplayerhelper.exe", "7za.exe", 
        "vmware-vdiskmanager.exe", "dnconsole.exe", "ldconsole.exe", 
        "ldrecord.exe", "libx264.dll", "avfilter-4.dll", 
        "avdevice-55.dll", "ssleay32.dll", "node.dll", 
        "zlibwapi.dll", "libgcc_s_dw2-1.dll", "zlib1.dll", 
        "ldcam.exe", "data.vmdk", "data-3G.vmdk"
        ]
    }
i_remove_dir_count = 0
i_remove_file_count = 0

print("TESSERACT_DIST_DIR:{}".format(TESSERACT_DIST_DIR))
print("LEI_DIAN_DIST_DIR:{}".format(LEI_DIAN_DIST_DIR))
#"""
for model_dir_key in dir_remove_list_dict:
    dir_remove_list = dir_remove_list_dict[model_dir_key]
    for dir_remove in dir_remove_list:
        dir_remove = model_dir_key + dir_remove
        if os.path.exists(dir_remove):
            try:
                shutil.rmtree(dir_remove)
                i_remove_dir_count += 1
            except Exception as e:
                print(f"删除文件夹{dir_remove}时出错: {e}")
#"""
#"""
for model_dir_key in file_remove_list_dict:
    file_remove_list = file_remove_list_dict[model_dir_key]
    for file_remove in file_remove_list:
        file_remove_list_ = []
        
        file_remove = model_dir_key + file_remove
        file_remove_list_.append(file_remove)
        if "*" in file_remove:
            file_remove_list_ = []
            files_to_remove = glob.glob(file_remove)
            for file_path in files_to_remove:
                if os.path.isfile(file_path):
                    file_remove_list_.append(file_path)
        for file_remove_ in file_remove_list_:
            if os.path.isfile(file_remove_):
                try:
                    os.remove(file_remove_)
                    i_remove_file_count += 1
                except Exception as e:
                    print(f"删除文件{file_remove_}时出错: {e}")
#"""
print("共删除掉{}个文件夹".format(i_remove_dir_count))
print("共删除掉{}个文件".format(i_remove_file_count))

##############################################


####################压缩打包##################################
"""
ROOT_FOLDER = APP_NAME  # 根目录名称
strTime = time.strftime("%Y-%m-%d")
DEST_NAME = "{}-".format(APP_NAME) + strTime + '.zip'
z = zipfile.ZipFile(DEST_NAME,'w', compression=zipfile.ZIP_DEFLATED) 
os.chdir(DIST_DIR)
for dirpath, dirnames, filenames in os.walk('.',True):  
    for item in filenames:  
        # 构建文件的完整路径
        file_path = os.path.join(dirpath, item)
        # 构建目标路径，添加根目录名称
        arcname = os.path.join(ROOT_FOLDER, file_path)
        z.write(file_path, arcname=arcname)
        
        #z.write(os.path.join(dirpath,item))  
        #print(os.path.join(dirpath,item))  
z.close()
print("打包成功：打包文件存放在 {}".format(DEST_NAME))
my_exit(0)
"""

####################INNO打包##################################
print("开始使用Inno Setup打包...")
# 检查Inno Setup编译器是否存在
innosetup_path = r"E:\Program Files (x86)\Inno Setup 6\ISCC.exe"
iss_script_path = r"D:\weChat_assistance\个微私域精灵打包脚本.iss"

if not os.path.exists(innosetup_path):
    print(f"错误: Inno Setup编译器不存在于 {innosetup_path}")
    print("请确保已安装Inno Setup 6并检查路径是否正确")
    sys.exit(1)

if not os.path.exists(iss_script_path):
    print(f"错误: Inno Setup脚本文件不存在于 {iss_script_path}")
    sys.exit(1)

# 执行Inno Setup打包命令
# 使用subprocess模块替代os.system，更好地处理包含空格的路径
import subprocess
innosetup_cmd = [innosetup_path, iss_script_path]
print(f"执行命令: {' '.join(innosetup_cmd)}")

try:
    status = subprocess.run(innosetup_cmd, check=True, shell=False)
    print("Inno Setup打包成功!")
    print("安装包已生成在 D:\\weChat_assistance\\wechatSiYuGenie_WindowsRPA_V1.0_Install.exe")
except subprocess.CalledProcessError as e:
    print(f"Inno Setup打包失败，退出代码: {e.returncode}")
    sys.exit(e.returncode)
except Exception as e:
    print(f"执行Inno Setup时出错: {e}")
    sys.exit(1)