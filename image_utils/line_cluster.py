# -*- coding: utf-8 -*-
#
# 线段聚类
# Author: alex
# Created Time: 2020年03月26日 星期四 15时18分41秒
import numpy as np
from ibbd_algo.optics import Optics


def line_cluster(lines, enpoints,
                 max_radius=3, min_samples=2, cluster_thr=2):
    """线段聚类
    :param lines list 线段方程，y=ax+b: [(a, b)]
    :param enpoints list 线段的端点，注意每个线段有两个端点: [[(y1, x1), (y2, x2)]]
    :param min_samples, max_radius: 聚类参数
    :return labels
    """
    data = [(a, b, x1, y1, x2, y2)
            for ((a, b), ((x1, y1), (x2, y2))) in zip(lines, enpoints)]
    optics = Optics(max_radius, min_samples, distance=distance)
    optics.fit(data)
    return optics.fit(cluster_thr)


def distance(line1, line2):
    """计算两个线段的距离
    :param line1,line2: [a, b, x1, y1, x2, y2]
    """
    a1, b1, x11, y11, x12, y12 = line1
    a2, b2, x21, y21, x22, y22 = line2
    if abs(a1-a2) < 0.001:     # 平行
        return Optics.inf
    # 计算直线交点
    x0 = (b2-b1) / (a1-a2)
    y0 = a1*x0 + b1

    # 计算到线1的距离
    if x11 <= x0 <= x12 and y11 <= y0 <= y12:
        dist1 = 0
    else:
        # 到两端点的最小距离
        dist1 = min(np.linalg.norm([x0-x11, y0-y11]),
                    np.linalg.norm([x0-x12, y0-y12]))

    # 计算到线2的距离
    if x21 <= x0 <= x22 and y21 <= y0 <= y22:
        dist2 = 0
    else:
        # 到两端点的最小距离
        dist2 = min(np.linalg.norm([x0-x21, y0-y21]),
                    np.linalg.norm([x0-x22, y0-y22]))

    return dist1 + dist2
