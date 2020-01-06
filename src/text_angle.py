# -*- coding: utf-8 -*-
#
# 文字角度相关函数
# Author: alex
# Created Time: 2020年01月03日 星期五 18时36分08秒
import cv2
import numpy as np
from scipy.ndimage import filters, interpolation


def estimate_skew_angle(raw, min_angle=-15, max_angle=15):
    """
    估计图像文字角度
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
    estimates = []
    for a in range(min_angle, max_angle):
        roest = interpolation.rotate(est, a, order=0, mode='constant')
        v = np.mean(roest, axis=1)
        v = np.var(v)
        estimates.append((v, a))

    _, angle = max(estimates)
    return angle
