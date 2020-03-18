# -*- coding: utf-8 -*-
#
# 其他图像工具函数
# Author: alex
# Created Time: 2020年03月18日 星期三 17时38分00秒
import cv2
import numpy as np
from copy import deepcopy


def find_empty_size_all(gray, size, std_thr=15, mean_thr=200):
    """查找图像中所有特定size的空白区域
    :param gray cv2格式的灰度图
    :param size 指定size，值如：(100, 100)
    :param std_thr int 区域内标准差
    :param mean_thr int 区域内均值
    :return [box1, box2, ...]  返回所有满足条件的box，每个box的格式(x1, y1, x2, y2)
    """
    boxes = []   # 返回值
    cw, ch = size
    h, w = gray.shape[:2]
    gray = deepcopy(gray)
    for row in range(0, h, ch):
        for col in range(0, w, cw):
            roi = gray[row:row+ch, col:col+cw]   # 获取分块
            dev = np.std(roi)
            avg = np.mean(roi)
            if dev < std_thr and avg > mean_thr:
                # 满足条件，接近空白区域，让他变黑
                boxes.append((col, col+cw, row, row+ch))
                gray[row:row+ch, col:col+cw] = 0    # 全部都赋值为0

    return boxes


def find_empty_size(gray, size, std_thr=15, mean_thr=200):
    """查找图像中特定size的空白区域
    :param gray cv2格式的灰度图
    :param size 指定size，值如：(100, 100)
    :param std_thr int 区域内标准差
    :param mean_thr int 区域内均值
    :return (x1, y1, x2, y2)  返回满足条件的第一个box
    """
    cw, ch = size
    h, w = gray.shape[:2]
    for row in range(0, h, ch):
        for col in range(0, w, cw):
            roi = gray[row:row+ch, col:col+cw]   # 获取分块
            dev = np.std(roi)
            avg = np.mean(roi)
            if dev < std_thr and avg > mean_thr:
                # 满足条件，接近空白区域，让他变黑
                return (col, col+cw, row, row+ch)

    return None


def count_black_points(img):
    """计算黑点的个数，通常用于文档图像
    :param img cv2格式的图像
    """
    _, binary = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)
    h, w = binary.shape[:2]
    # 计算黑点的个数
    total = h*w - sum(sum(binary/255))
    return total
