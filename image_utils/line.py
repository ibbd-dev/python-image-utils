# -*- coding: utf-8 -*-
#
# 直线检测与识别
# Author: alex
# Created Time: 2020年03月20日 星期五 16时41分48秒
import cv2
import numpy as np
from math import atan
from sklearn.cluster import DBSCAN


def intersection_points(line_img1, line_img2):
    """计算两个直线的交点图像"""
    points = cv2.bitwise_and(line_img1, line_img2)
    return points


def detect_lines_angle(gray, scale, line_type='row'):
    """检测直线的倾斜角度
    :param gray 灰度图
    :param scale 检测参数
    :param line_type 直线类型，值为row（横线）或者col（竖线）
    :return 倾斜弧度，如果需要转换为角度: math.degrees
    """
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, -10)
    if line_type == 'row':
        line_img = detect_row_line(binary, scale)
    elif line_type == 'col':
        line_img = detect_col_line(binary, scale)
    else:
        raise Exception('error line_type value')

    n, lines = cluster_fit_lines(line_img)
    if n < 3:
        return None
    angles = [line[0] for line in lines]
    return atan(sum(angles)/len(angles))


def detect_line(gray, scale):
    """检测横线和竖线"""
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, -10)
    row_img = detect_row_line(binary, scale)
    col_img = detect_col_line(binary, scale)
    return row_img, col_img


def detect_col_line(binary, scale):
    """检测竖线"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    return cv2.dilate(eroded, kernel, iterations=1)


def detect_row_line(binary, scale):
    """检测横线"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    return cv2.dilate(eroded, kernel, iterations=1)


def cluster_lines(data, eps=3, min_samples=2, metric='manhattan'):
    """线条聚类"""
    db = DBSCAN(eps=eps, min_samples=min_samples, metric=metric).fit(data)
    labels = db.labels_
    n_clusters_ = max(labels) + 1
    return n_clusters_, labels


def fit_line(points):
    """拟合直线
    :params points [[y, x]] 图像坐标：[y, x]
    :return [a, b] 直线参数：y=ax+b
    """
    X = points[:, 1]
    Y = points[:, 0]
    line = np.polyfit(X, Y, 1)
    return line


def cluster_fit_lines(lines_img):
    """直线聚合并拟合直线
    :param lines_img 直线的黑白图像
    :return n int 直线数量
    :return lines [[a, b]] 直线方程的参数
    """
    points_idx = np.argwhere(lines_img == 255)
    n, labels = cluster_lines(points_idx)
    lines = []
    for i in range(n):
        line_points_idx = points_idx[labels == i]
        line = fit_line(line_points_idx)
        lines.append(line)

    return n, lines
