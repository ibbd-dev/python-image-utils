# -*- coding: utf-8 -*-
#
# 表格聚类: 将有关联的线段聚合在一起
# Author: alex
# Created Time: 2020年05月25日
import numpy as np
from sklearn.cluster import DBSCAN

# 线段a，b参数的最大值
A_MAX = 1e8
B_MAX = 1e8
# 斜率最小值
A_MIN = 1e-8
# 距离最大值
D_MAX = 1e8


def table_lines_cluster(lines, eps=3, min_samples=2):
    """表格线段聚类
    将有关联的线段聚合在一起
    线段：(a, b, x1, y1, x2, y2)
    其中：y = a*x+b，(x1, y1)和(x2, y2)是其两个端点
    :params lines list 线段列表
    :params eps, min_samples: DBSCAN聚类所使用的参数
    :return labels np.array 聚类结果
    """
    new_lines = []
    for a, b, x1, y1, x2, y2 in lines:
        a = max(min(a, A_MAX), -A_MAX)
        b = max(min(b, B_MAX), -B_MAX)
        if abs(a) < A_MIN:
            a = A_MIN

        new_lines.append([a, b, x1, y1, x2, y2])

    db = DBSCAN(eps=eps, min_samples=min_samples, metric=distance).fit(lines)
    return db.labels_


def distance(line1, line2):
    """计算两个线段的距离
    a, b: 线段直线参数，y=ax+b或者x=ay+b，具体看line_type的值
    x1, y1, x2, y2: 线段的两个端点
    :param line1, line2: [a, b, x1, y1, x2, y2]
    """
    a1, b1, x11, y11, x12, y12 = line1
    a2, b2, x21, y21, x22, y22 = line2

    # 计算交点
    if abs(a1-a2) < 0.01:
        return D_MAX
    x0 = (b2-b1)/(a1-a2)
    y0 = a1 * x0 + b1

    def point_line_dist(x1, y1, x2, y2):
        """计算点到线的距离"""
        v1 = [x1-x0, y1-y0]
        v2 = [x2-x0, y2-y0]
        return min(np.linalg.norm(v1), np.linalg.norm(v2))

    # 计算到线1的距离
    dist1 = point_line_dist(x11, y11, x12, y12)
    # 计算到线2的距离
    dist2 = point_line_dist(x21, y21, x22, y22)
    print(line1[2:])
    print(line2[2:])
    print(dist1+dist2)
    return dist1 + dist2


if __name__ == '__main__':
    def create_line(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        a = (y2-y1)/(x2-x1)
        b = y1 - a*x1
        return (a, b, x1, y1, x2, y2)

    points1 = [(1, 9), (2, 1), (7, 1.5), (10, 10)]
    points2 = [(4, 2), (5, 2), (6, 4), (3, 5)]
    lines = [create_line(points1[i], points1[i+1])
             for i in range(len(points1)-1)]
    for i in range(len(points2)-1):
        lines.append(create_line(points2[i], points2[i+1]))

    lines.append(create_line(points2[0], points2[len(points2)-1]))
    labels = table_lines_cluster(lines, eps=2.5)
    print(labels)
