# -*- coding: utf-8 -*-
#
# 表格相关基础函数
# Author: alex
# Created Time: 2020年03月20日 星期五 16时41分48秒
import cv2
import numpy as np
from sklearn.cluster import DBSCAN


def detect_line(gray, scale):
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, -10)
    row_img = detect_row_line(binary, scale)
    col_img = detect_col_line(binary, scale)
    return row_img, col_img


def detect_col_line(binary, scale):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    return cv2.dilate(eroded, kernel, iterations=1)


def detect_row_line(binary, scale):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    return cv2.dilate(eroded, kernel, iterations=1)


def cluster_lines(data):
    db = DBSCAN(eps=3, min_samples=2, metric='manhattan', algorithm='auto').\
        fit(data)
    labels = db.labels_
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_clusters_ = max(labels) + 1
    return n_clusters_, labels


def fit_line(points):
    X = points[:, 1]
    Y = points[:, 0]
    params = np.polyfit(X, Y, 1)
    return params


def cluster_fit_lines(row_img):
    idx_row = np.argwhere(row_img == 255)
    n, labels = cluster_lines(idx_row)
    lines = []
    for i in range(n):
        points = idx_row[labels == i]
        line = fit_line(points)
        lines.append(line)

    return n, lines
