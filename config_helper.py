# -*- coding: utf-8 -*-
import json
import os
import json
from threading import Lock
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from log_helper import print_my 

#
user_dir = os.path.expanduser('~')
config_dir = user_dir + "\\ExportConf\\"
if False == os.path.exists(config_dir):
    os.mkdir(config_dir)
g_config_path = config_dir + "other.bin"
g_key = b"soi23fsdfwejsdfk"

g_lock_config = Lock()

# 加密函数
def encrypt_data(data, key):
    # 生成随机的IV（初始化向量）
    iv = os.urandom(16)
    # 创建AES加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data  # 将IV和加密数据一起返回

# 解密函数
def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]  # 提取IV
    encrypted_data = encrypted_data[16:]  # 提取加密数据
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode('utf-8')

def load_from_binary(file_path):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()  # 读取加密后的二进制数据
    return encrypted_data

def load_config_data(config_path):
    g_lock_config.acquire()
    
    if False == os.path.exists(config_path):
        g_lock_config.release()
        return {}
    # 版本1       
    """
    with open(config_path, "r", encoding='utf-8') as f_read:
        try: 
            config_json_data = json.load(f_read)
        except Exception as e:
            print_my("加载配置文件{}失败[{}]".format(config_path, e))
            return {}
    
    #print_my("成功从配置文件:{}加载数据".format(config_path))
    return config_json_data
    """
    # 版本2
    """
    with open(config_path, 'rb') as file:
        try:
            config_json_data = pickle.load(file)  # 使用pickle反序列化数据
        except Exception as e:
            print_my("加载配置文件{}失败[{}]".format(config_path, e))
            return {}
    #print_my("成功从配置文件:{}加载数据".format(config_path))
    return config_json_data
    """
    # 版本3
    #"""
    try:
        loaded_encrypted_data = load_from_binary(config_path)
        decrypted_data = decrypt_data(loaded_encrypted_data, g_key)
        config_json_data = json.loads(decrypted_data)
    except Exception as e:
        print_my("加载配置文件{}失败[{}]".format(config_path, e))
        g_lock_config.release()
        return {}
    g_lock_config.release()
    return config_json_data
    #"""

"""
def save_as_binary(data, output_file_path):
 with open(output_file_path, 'wb') as file:
        pickle.dump(data, file)  # 使用pickle序列化数据并保存为二进制文件
"""
def save_as_binary(encrypted_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        file.write(encrypted_data)  # 写入加密后的二进制数据
        
def save_config_data(config_json_data, config_path):  
    """
    with open(config_path, "w", encoding='utf-8') as f_write:
        json.dump(config_json_data, f_write, ensure_ascii=False, indent=4)
    """
    
    """
    save_as_binary(config_json_data, config_path)
    """
    g_lock_config.acquire()
    try:
        json_string = json.dumps(config_json_data)  
        encrypted_data = encrypt_data(json_string, g_key)
        save_as_binary(encrypted_data, config_path)
    except Exception as e:
        print_my("配置文件保存失败")
        print("异常:{}".format(e))
        g_lock_config.release()
        return
    #print_my("配置文件保存到:{}".format(config_path))
    g_lock_config.release()
    return 
# chenyj test   
#g_config_json_data = load_config_data(g_config_path)
#print(g_config_json_data)
#save_config_data(g_config_json_data, g_config_path)