# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm


dst_filename = 'wechatAiAssistantV1.0-2024-08-29.zip'
dowload_url = 'http://110.40.133.216:8002/download/' + dst_filename
#TIME_OUT = 5
#TIME_OUT = 8
#TIME_OUT = 30
TIME_OUT = 120
def download_file(dowload_url, dst_filename, debug_process = False):
    i_recved_data_len = 0
    # 使用requests的Session来保持连接
    with requests.Session() as session:
        # 发送GET请求
        response = session.get(dowload_url, stream=True, timeout=TIME_OUT)
        
        # 总大小
        total_size = int(response.headers.get('content-length', 0))
        block_size = 256*1024  # 1 Kilobyte per chunk

        if debug_process == True:
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        # 打开文件准备写入
        with open(dst_filename, 'wb') as file:
            for data in response.iter_content(block_size):
                if debug_process == True:
                    progress_bar.update(len(data))
                file.write(data)
                i_recved_data_len += len(data)
                yield int(i_recved_data_len/total_size*100)
        if debug_process == True:
            progress_bar.close()
            
    return None

    
#for finish_count in download_file(dowload_url, dst_filename, True):
#    pass