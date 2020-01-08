# -*- coding: utf-8 -*-
#
# 图像格式转换相关函数
# Author: alex
# Created Time: 2019年09月04日 星期三 09时31分18秒
"""
from PIL import Image
img = Image.open(path)

img.mode模式:
1             1位像素，黑和白，存成8位的像素
L             8位像素，黑白
P             8位像素，使用调色板映射到任何其他模式
RGB           3×8位像素，真彩
RGBA          4×8位像素，真彩+透明通道
CMYK          4×8位像素，颜色隔离
YCbCr         3×8位像素，彩色视频格式
I             32位整型像素
F             32位浮点型像素

img.format: 这和文件后缀对应

注意P模式的图片，对应的format格式可能是GIF
"""
import re
import cv2
import base64
import numpy as np
from PIL import Image
from io import BytesIO


def base64_cv2(b64):
    """将base64格式的图片转换为cv2格式"""
    b64 = base64.b64decode(b64)
    nparr = np.fromstring(b64, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    """
    tmp = b64.split(',')[0]
    b64 = b64[len(tmp)+1:]
    b64 = base64.b64decode(b64)
    img = Image.open(BytesIO(b64))
    if 'png' in tmp:   # 先转化为jpg
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, img)
        img = bg

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    """


def cv2_base64(img, format='JPEG'):
    """将cv2格式的图像转换为base64格式"""
    out_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    output_buffer = BytesIO()
    out_img.save(output_buffer, format=format)
    binary_data = output_buffer.getvalue()
    return str(base64.b64encode(binary_data), encoding='utf8')


def base64_pil(b64):
    """将图片从base64格式转换为PIL格式"""
    base64_data = re.sub('^data:image/.+;base64,', '', b64)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    return Image.open(image_data)


def pil_base64(img, format='JPEG'):
    """将PIL图片转换为base64格式"""
    buf = BytesIO()
    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.save(buf, format=format)
    binary_data = buf.getvalue()
    return str(base64.b64encode(binary_data), encoding='utf8')


def cv2_pil(img):
    """将图片从cv2转换为PIL格式"""
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def pil_cv2(img):
    """将图片从PIL转换为cv2格式"""
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def gif_jpg(img):
    """GIF格式图片转化为jpg"""
    palette = img.getpalette()
    img.putpalette(palette)
    new_img = Image.new("RGB", img.size)
    new_img.paste(img)
    return new_img


def rotate(image, angle, center=None, scale=1.0, borderValue=(255, 255, 255)):
    """cv2旋转图像
    效果比Image.rotate效果要好
    :param borderValue 填充颜色，默认为白色
    """
    # 获取图像尺寸
    (h, w) = image.shape[:2]

    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)

    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=borderValue)

    # 返回旋转后的图像
    return rotated


def rotate_pil(image, angle, center=None, scale=1.0):
    """PIL旋转图像
    效果比Image.rotate效果要好
    """
    image = np.asarray(image)
    rotated = rotate(image)
    return Image.fromarray(rotated)


def intersection_area(box1, box2):
    """计算两个矩形的重叠面积"""
    x1, y1, xb1, yb1 = box1
    x2, y2, xb2, yb2 = box2

    # 相交矩形
    ax, ay, bx, by = max(x1, x2), max(y1, y2), min(xb1, xb2), min(yb1, yb2)
    if ax >= bx or ay >= by:
        return 0

    # 重叠面积
    in_area = (bx-ax) * (by-ay)
    # print((ax, ay, bx, by))
    # print('相交面积：%d' % in_area)
    return in_area
