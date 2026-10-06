from PIL import Image
import argparse
import os

# 使用示例
# python img_to_png_Tou_ming.py -i weichat_logo.jpeg -o weichat_logo.png -t 245 -tol 15

def white_to_transparent(input_path, output_path, threshold=240, tolerance=10):
    """
    将PNG图片中的白色像素转为透明
    
    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径
        threshold: RGB值的阈值，超过此值的像素被视为白色
        tolerance: 容差值，用于处理接近白色的像素
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGBA模式（如果不是的话）
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            width, height = img.size
            pixels = img.load()
            
            # 遍历所有像素
            for y in range(height):
                for x in range(width):
                    # 获取像素值
                    r, g, b, a = pixels[x, y]
                    
                    # 判断是否为白色或接近白色
                    if (r > threshold and g > threshold and b > threshold) and \
                       (max(r, g, b) - min(r, g, b) < tolerance):
                        # 设置为透明
                        pixels[x, y] = (r, g, b, 0)
            
            # 保存修改后的图片
            img.save(output_path, 'PNG')
            print(f"成功处理图片并保存至: {output_path}")
    
    except Exception as e:
        print(f"处理图片时出错: {e}")

def main():
    parser = argparse.ArgumentParser(description='将PNG图片中的白色像素转为透明')
    parser.add_argument('-i', '--input', required=True, help='输入图片路径')
    parser.add_argument('-o', '--output', help='输出图片路径，默认为input_transparent.png')
    parser.add_argument('-t', '--threshold', type=int, default=240, help='RGB阈值，默认240')
    parser.add_argument('-tol', '--tolerance', type=int, default=10, help='容差值，默认10')
    
    args = parser.parse_args()
    
    # 如果没有指定输出路径，在输入文件名后添加_transparent
    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_transparent.png"
    
    white_to_transparent(args.input, args.output, args.threshold, args.tolerance)

if __name__ == "__main__":
    main()    