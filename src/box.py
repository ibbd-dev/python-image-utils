# -*- coding: utf-8 -*-
#
# box相关函数
#
# Author: alex
# Created Time: 2020年03月10日 星期二


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


def iou(box1, box2):
    """计算两个矩形的交并比"""
    in_area = intersection_area(box1, box2)
    if in_area == 0:
        return 0.

    x1, y1, xb1, yb1 = box1
    x2, y2, xb2, yb2 = box2
    area1 = abs((xb1-x1) * (yb1-y1))
    area2 = abs((xb2-x2) * (yb2-y2))
    return in_area / (area1 + area2 - in_area)


def in_box_rate(box, container_box):
    """判断一个box在一个容器box里的占比"""
    in_area = intersection_area(box, container_box)
    if in_area == 0:
        return 0.
    x1, y1, xb1, yb1 = box
    area = abs((xb1-x1) * (yb1-y1))
    return in_area / area


def boxes_in_row(box1, box2):
    """判断两个box是否在同一行"""
    if iou(box1, box2) > 0:
        return False     # 不能有交集
    if box1[0] > box2[0]:
        box1, box2 = box2, box1

    _, y1, xb1, yb1 = box1
    x2, y2, _, yb2 = box2
    if xb1 > x2:
        return False    # box2必须在box1的右边

    # 垂直方向上交集
    min_yb, max_y = min(yb1, yb2), max(y1, y2)
    if min_yb <= max_y:
        return False    # 如果没有交集
    max_h = max(yb1, yb2) - min(y1, y2)
    min_h = min_yb - max_y

    # 高度差
    h1, h2 = yb1-y1, yb2-y2
    h1, h2 = min(h1, h2), max(h1, h2)
    print((h2-h1)/h1)

    # 水平方向需要相邻 & 重叠部分超过80% & 高度差不能超过20%
    # TODO 这里的参数可能不是最优的，可以经过测试调整
    return min_h/max_h > 0.8 and (x2-xb1) < 2*min_h and (h2-h1)/h1 < 0.2


if __name__ == '__main__':
    box1 = [325.8022766113281, 393.0766296386719, 592.3567504882812, 435.80364990234375]
    box2 = [620.7103881835938, 397.5979309082031, 660.7562255859375, 433.3531188964844]
    print(boxes_in_row(box1, box2))
