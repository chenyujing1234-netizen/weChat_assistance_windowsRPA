# coding: utf-8
import os
import sys
import shutil
import zipfile
import time
from app_info import *
import argparse
import glob

DIST_DIR = ".\\dist\\main\\"
MODEL_DIR = ".\\dist\\main\\_internal\\"
TESSERACT_DIST_DIR = DIST_DIR + TESSERACT_DIR + "\\"
LEI_DIAN_DIST_DIR = DIST_DIR + LEI_DIAN_DIR + "\\"
        
#"""
# 4. 把没用的文件夹或文件删除
# "numpy"  "pandas" "psutil", "mkl"
dir_remove_list_dict = {MODEL_DIR:["multidict", "yaml", "h5py", "dask", "numba", "yarl", "selenium", "xyzservices", "scipy", "greenlet", "jedi", "lxml", "menuinst", "IPython", "pyarrow", "docutils", "bokeh", "bokeh-3.3.4.dist-info", "_argon2_cffi_bindings", "aiohttp", "alabaster", "zstandard", "cryptography-42.0.2.dist-info", "llvmlite", "snappy", "numexpr", "wheel-0.43.0.dist-info", "lmdb", "markupsafe", "attrs-23.2.0.dist-info", "bcrypt", "botocore", "nbformat-5.9.2.dist-info", "distributed-2023.11.0.dist-info", "importlib_metadata-7.0.1.dist-info", "jsonschema-4.19.2.dist-info", "jsonschema_specifications", "jsonschema", "rpds", "kiwisolver", "winpty", "lz4-4.3.2.dist-info", "zope", "zmq", "frozenlist", "nbformat", "parso", "contourpy", "tables", "sphinx", "nacl", "lz4", "sqlalchemy", "win32com", "lib2to3", "babel", "pytz"], TESSERACT_DIST_DIR:["doc"], LEI_DIAN_DIST_DIR:["qrcode", "ldmutiplayer"]}
# "msvcp*.dll", "tk86t.dll",  "tcl86t.dll", "mkl_def*.dll", "api-ms*.dll", "libxslt.dll", "libexslt.dll", 
file_remove_list_dict = {MODEL_DIR:["mkl_vml_*.dll", "mkl_scalapack_*.dll", "mkl_tbb_*.dll", "mkl_sequen*.dll", "mkl_pgi_thread*.dll", "mkl_msg*.dll", "mkl_mc*.dll", "mkl_cdft_core*.dll", "mkl_blacs_*.dll", "yaml.dll", "hdf5*.dll", "snappy.dll", "opengl32sw.dll", "arrow*.dll", "arrow_flight.dll", "libmmd.dll", "libGLESv2.dll", "brotlienc.dll", "libprotobuf.dll", "winpty.dll", "libiomp5md.dll", "libifcoremd.dll", "orc.dll", "sqlite3.dll", "parquet.dll", "omptarget*.dll", "arrow_dataset.dll", "aws*.dll", "libxml2.dll", "thriftmd.dll", "libwebp.dll", "re2.dll", "ucrtbase.dll", "vccorlib140.dll", "concrt140.dll", "libcurl.dll", "_sqlite3.pyd", "libjpeg.dll", "win32\\mfc140u.dll", "_hashlib.pyd", "_uuid.pyd", "iconv.dll", "libblosc2.dll", "freetype.dll", "_decimal.pyd", "vcomp140.dll", "Qt5Qml_conda.dll", "Qt5VirtualKeyboard_conda.dll", "Qt5Pdf_conda.dll", "Qt5WebSockets_conda.dll", "Qt5Quick_conda.dll", "Qt5QmlModels_conda.dll", "Qt5Network_conda.dll", "Qt5Svg_conda.dll", "Qt5DBus_conda.dll", "_elementtree.pyd"], TESSERACT_DIST_DIR:["tessdata\\chi_tra.traineddata", "text2image.exe", "lstmtraining.exe", "lstmeval.exe", "set_unicharset_properties.exe", "mftraining.exe", "shapeclustering.exe", "classifier_tester.exe", "cntraining.exe", "unicharset_extractor.exe", "combine_lang_model.exe" "combine_tessdata.exe", "ambiguous_words.exe", "wordlist2dawg.exe", "dawg2wordlist.exe", "merge_unicharsets.exe", "combine_lang_model.exe", "icuin64.dll", "libeay32.dll", "icudt64.dll", "combine_tessdata.exe"], LEI_DIAN_DIST_DIR:["dnrepairer.exe", "dnmultiplayer.exe", "ldplayerhelper.exe", "aapt.exe" "ldplayerhelper.exe", "7za.exe", "vmware-vdiskmanager.exe", "dnconsole.exe", "ldconsole.exe", "ldrecord.exe", "libx264.dll", "avfilter-4.dll", "avdevice-55.dll", "ssleay32.dll", "node.dll", "zlibwapi.dll", "libgcc_s_dw2-1.dll", "zlib1.dll", "ldcam.exe", "data.vmdk", "data-3G.vmdk"]}
i_remove_dir_count = 0
i_remove_file_count = 0

print("TESSERACT_DIST_DIR:{}".format(TESSERACT_DIST_DIR))
print("LEI_DIAN_DIST_DIR:{}".format(LEI_DIAN_DIST_DIR))
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
print("共删除掉{}个文件夹".format(i_remove_dir_count))
print("共删除掉{}个文件".format(i_remove_file_count))
#"""
##############################################


####################压缩打包##################################
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
