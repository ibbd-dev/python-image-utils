# -*- coding: utf-8 -*-
#
# 文字角度相关函数
# Author: alex
# Created Time: 2020年01月03日 星期五 18时36分08秒
import cv2
import math
import numpy as np
from scipy.ndimage import filters, interpolation


def estimate_skew_angle(raw, fine_tune_num=3, step_start=1.5):
    """
    估计图像文字角度
    :param raw 待纠正的图像
    :param fine_tune_num 微调的次数, 界定了微调的精度
        当该值为n时，表示微调角度精确到step_start乘以10的-(n-1)次方
    :param step_start 步长的初始值
        当该值为a时，其纠正的角度范围是[-10*a, 10*a]。该值不应该大于4.5
    :return angle 需要纠正的角度
    """
    def resize_im(im, scale, max_scale=None):
        f = float(scale)/min(im.shape[0], im.shape[1])
        if max_scale is not None and \
                f*max(im.shape[0], im.shape[1]) > max_scale:
            f = float(max_scale)/max(im.shape[0], im.shape[1])
        return cv2.resize(im, (0, 0), fx=f, fy=f)

    raw = resize_im(raw, scale=600, max_scale=900)
    image = raw-np.amin(raw)
    image = image/np.amax(image)
    m = interpolation.zoom(image, 0.5)
    m = filters.percentile_filter(m, 80, size=(20, 2))
    m = filters.percentile_filter(m, 80, size=(2, 20))
    m = interpolation.zoom(m, 1.0/0.5)

    w, h = min(image.shape[1], m.shape[1]), min(image.shape[0], m.shape[0])
    flat = np.clip(image[:h, :w]-m[:h, :w]+1, 0, 1)
    d0, d1 = flat.shape
    o0, o1 = int(0.1*d0), int(0.1*d1)
    flat = np.amax(flat)-flat
    flat -= np.amin(flat)
    est = flat[o0:d0-o0, o1:d1-o1]

    angle, step = 0, step_start   # 纠正角度的初始值和步长
    for _ in range(fine_tune_num):
        angle = fine_tune_angle(est, step, start=angle)
        step /= 10

    return angle


def fine_tune_angle(image, step, start=0):
    """微调纠正
    在某个角度start的周围进行微调
    """
    estimates = []
    for a in range(-10, 11):
        a = start + step*a
        roest = interpolation.rotate(image, a, order=0, mode='constant')
        v = np.mean(roest, axis=1)
        v = np.var(v)
        estimates.append((v, a))

    _, angle = max(estimates)
    return angle


def estimate_skew_angle2(srcImage):
    """利用直线了纠正角度"""
    midImage = cv2.cvtColor(srcImage, cv2.COLOR_BGR2GRAY)
    dstImage = cv2.Canny(midImage, 50, 200, 3)

    # 通过霍夫变换检测直线
    # 第4个参数就是阈值，阈值越大，检测精度越高
    # 由于图像不同，阈值不好设定，因为阈值设定过高导致无法检测直线，阈值过低直线太多，速度很慢
    # 霍夫变换
    lines = cv2.HoughLines(dstImage, 1, np.pi / 180, 0)
    rotate_angle = 0
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        if x1 == x2 or y1 == y2:
            continue
        t = float(y2 - y1) / (x2 - x1)
        rotate_angle = math.degrees(math.atan(t))
        if rotate_angle > 45:
            rotate_angle = -90 + rotate_angle
        elif rotate_angle < -45:
            rotate_angle = 90 + rotate_angle

    return math.radians(rotate_angle)
    # return rotate_angle


if __name__ == '__main__':
    import sys
    from convert import rotate
    img = cv2.imread(sys.argv[1])
    angle = estimate_skew_angle2(img)
    print(angle)
    new_img = rotate(img, angle)
    cv2.imwrite(sys.argv[2], new_img)
