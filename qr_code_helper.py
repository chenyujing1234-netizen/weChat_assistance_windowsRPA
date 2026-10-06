# pip install qrcode
from __future__ import annotations
import qrcode
from pathlib import Path

def url_to_qr_image(url: str, save_path: str | None = None) -> "qrcode.image.pil.PilImage | None":
    """
    将 URL 生成二维码图片
    :param url: 要编码的网址
    :param save_path: 若为 None，则只返回 PIL.Image 对象；否则保存到该路径
    :return: PIL.Image 对象（save_path 为 None 时）；已保存文件时返回 None
    """
    qr = qrcode.QRCode(
        version=None,      # 自动选择最小尺寸
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,       # 每个小格像素数
        border=4,          # 边框格子数
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(save_path)
        print(f"二维码已保存 → {save_path}")
        return None
    return img


# ----------------- 用法示例 -----------------
if __name__ == "__main__":
    target_url = "https://github.com/sahq/qrcode"

    # 1. 直接保存为文件
    url_to_qr_image(target_url, "demo_url.png")

    # 2. 仅获取 PIL.Image 对象，可继续二次处理（显示、上传、转 base64…）
    pil_img = url_to_qr_image(target_url)
    pil_img.show()          # 弹出默认图片查看器