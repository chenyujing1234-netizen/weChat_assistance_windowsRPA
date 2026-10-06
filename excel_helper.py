import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.drawing.image import Image
import tkinter as tk
from tkinter import filedialog
from PIL import Image as PILImage
import os
import tempfile
from pathlib import Path
from openpyxl.drawing.image import Image as OpenpyxlImage

def save_content_to_excel(content_data_list, excel_file_path):
    """
    将包含文案信息的列表写入Excel表格，并设置自动换行、列宽、表头字体等
    
    参数:
    content_data_list: 包含文案信息的列表
    excel_file_path: Excel文件保存路径
    
    返回:
    无
    """
    try:
        # 创建一个新的工作簿
        wb = Workbook()
        # 选择默认的工作表
        ws = wb.active
        # 设置表头
        ws.append(["文案文本", "文案图片"])
        
        # 遍历内容列表，将数据写入表格
        for content_info in content_data_list:
            # 提取文案文本
            text_content = content_info.get("content", "")
            # 提取图片列表
            image_paths = content_info.get("image_list", [])
            
            # 将数据写入表格
            ws.append([text_content, ""])
        
        # 设置自动换行
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=1):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True)
        
        # 获取屏幕宽度
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        screen_width = root.winfo_screenwidth()
        
        # 设置列宽为屏幕宽度的一半（这里需要根据实际情况调整换算比例）
        column_width = screen_width / 2 / 10  # 10 是一个换算比例，可能需要根据实际情况调整
        
        #列宽
        for col in ws.columns:
            column_letter = col[0].column_letter
            ws.column_dimensions[column_letter].width = column_width
        
        # 设置表头字体
        header_font = Font(size=20, bold=True)
        for cell in ws[1]:
            cell.font = header_font
        
        # 插入图片并保存临时文件路径
        temp_files = []  # 用于保存所有临时图片文件路径
        for i, content_info in enumerate(content_data_list, start=2):  # 从第二行开始（第一行是表头）
            image_paths = content_info.get("image_list", [])
            for j, image_path in enumerate(image_paths):
                if os.path.exists(image_path):
                    try:
                        # 读取并调整图片大小
                        img = PILImage.open(image_path)
                        img.thumbnail((100, 100))
                        
                        # 创建临时文件并保存调整后的图片
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                            temp_filename = temp_file.name
                            img.save(temp_filename)
                            temp_files.append(temp_filename)  # 记录临时文件路径
                        
                        # 插入图片到Excel
                        excel_image = Image(temp_filename)
                        ws.add_image(excel_image, f"B{i}")
                    except Exception as e:
                        print(f"插入图片失败: {e}")
        
        # 保存工作簿
        wb.save(excel_file_path)
        print(f"Excel文件已保存到: {excel_file_path}")
        
        # 删除所有临时图片文件
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"save_content_to_excel, 删除临时文件失败: {e}")
        return True
    except Exception as e:
        print(f"save_content_to_excel, 保存Excel文件失败: {e}")
        return False 
    return False
          
def load_content_from_excel(excel_file_path, image_output_folder=None):
    """
    从Excel文件导入文案数据及关联图片
    
    参数:
    excel_file_path: Excel文件路径
    image_output_folder: 图片保存目录（默认在Excel所在目录创建`imported_images`）
    
    返回:
    content_data_list: 包含文案信息的列表，结构为 [{"content": str, "image_list": [图片路径,...]}, ...]
    """
    # 创建图片保存目录
    if image_output_folder is None:
        excel_dir = os.path.dirname(excel_file_path)
        image_output_folder = os.path.join(excel_dir, "imported_images")
    
    Path(image_output_folder).mkdir(parents=True, exist_ok=True)

    # 加载工作簿
    wb = openpyxl.load_workbook(excel_file_path)
    ws = wb.active

    content_data_list = []
    image_mapping = {}

    # 预解析所有图片的位置信息（行号从1开始）
    for img in ws._images:
        if isinstance(img, OpenpyxlImage):
            
            # 获取图片锚定的单元格位置
            anchor = img.anchor
            #print("img:=======({}, {})".format(anchor.from_obj.row, anchor.from_obj.col))
            if isinstance(anchor, openpyxl.drawing.spreadsheet_drawing.TwoCellAnchor):
                row = anchor.from_obj.row + 1  # 调整为Excel行号（从1开始）
                col = anchor.from_obj.col + 1  # 调整为Excel列号（从1开始）
                if (row, col) not in image_mapping:
                    image_mapping[(row, col)] = []
                image_mapping[(row, col)].append(img)
    print("image_mapping:{}".format(image_mapping))
    # 遍历数据行（从第二行开始）
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        # 提取文案文本（A列）
        text_content = row[0].value or ""

        # 提取关联图片（B列）
        image_list = []
        if (row_idx, 2) in image_mapping:  # B列是第2列
            for idx, img in enumerate(image_mapping[(row_idx, 2)], 1):
                try:
                    # 生成唯一文件名
                    filename = f"row_{row_idx}_img_{idx}.png"
                    output_path = os.path.join(image_output_folder, filename)
                    
                    # 保存图片文件
                    with open(output_path, "wb") as f:
                        f.write(img._data())
                    
                    image_list.append(output_path)
                except Exception as e:
                    print(f"保存图片失败（行{row_idx}）: {str(e)}")

        content_data_list.append({
            "content": text_content,
            "image_list": image_list
        })

    return content_data_list
  
  
def save_friend_list_to_excel(friend_data_list, excel_file_path):
    """
    将好友列表写入Excel表格
    
    参数:
    friend_data_list: 包含好友信息的列表
    excel_file_path: Excel文件保存路径
    
    返回:
    无
    """
    try:
        # 创建一个新的工作簿
        wb = Workbook()
        # 选择默认的工作表
        ws = wb.active
        # 设置表头
        ws.append(["好友昵称", "添加时间", "好友近况说明"])
        
        # 遍历内容列表，将数据写入表格
        for friend_data in friend_data_list:
            friend_name = friend_data.get("friend_name", "")
            add_date = friend_data.get("add_date", "")
            friend_remark = friend_data.get("friend_remark", "")
            
            # 将数据写入表格
            ws.append([friend_name, add_date, friend_remark])
        
        # 设置自动换行
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=1):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True)
        
        # 获取屏幕宽度
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        screen_width = root.winfo_screenwidth()
        
        # 设置列宽为屏幕宽度的一半（这里需要根据实际情况调整换算比例）
        column_width = screen_width / 2 / 10  # 10 是一个换算比例，可能需要根据实际情况调整
        
        #列宽
        for col in ws.columns:
            column_letter = col[0].column_letter
            ws.column_dimensions[column_letter].width = column_width
        
        # 设置表头字体
        header_font = Font(size=20, bold=True)
        for cell in ws[1]:
            cell.font = header_font
        
        # 保存工作簿
        wb.save(excel_file_path)
        print(f"Excel文件已保存到: {excel_file_path}")
        
        return True
    except Exception as e:
        print(f"save_friend_list_to_excel, 保存Excel文件失败: {e}")
        return False 
    return False