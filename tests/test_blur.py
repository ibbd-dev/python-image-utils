'''
图像模糊检测测试

Author: alex
Created Time: 2020年11月03日 星期二 10时03分21秒
'''
import shutil
import imutils
import cv2
import skvideo.io
import numpy as np
from PIL import Image
from image_utils.cv2_utils import lapulase
from image_utils.convert import pil_cv2, cv2_pil


def get_video_rotate(video_path):
    """"""""
    # video表示视频路径，字符串形式，eg：‘E:/project/blink-detection/3.mp4’
    metadata = skvideo.io.ffprobe(video_path)
    d = metadata['video'].get('tag')[0]
    if d.setdefault('@key') == 'rotate': #获取视频自选择角度
        return 360-int(d.setdefault('@value'))
    return 0


def rot90(img):
    return img.swapaxes(0,1)[...,::-1]


def rotate(img, angle):
    img = cv2_pil(img)
    if angle == 90:
        img = img.transpose(Image.ROTATE_90)
    elif angle == 270: 
        img = img.transpose(Image.ROTATE_270)
    elif angle == 180:
        img = img.transpose(Image.ROTATE_180)
    else:
        raise Exception('Error')
    return pil_cv2(img)


def video_blur(video_path):
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    # 获取旋转角度
    angle = get_video_rotate(video_path)
    print('Angle: ', angle)
    # video_FourCC = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_FourCC = cv2.VideoWriter_fourcc(*'mp4v')
    video_fps    = vid.get(cv2.CAP_PROP_FPS)
    video_size   = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    output_path = 'out_%s' % video_path.split('/')[-1]
    if angle in {90, 270}:
        video_size = video_size[::-1]

    print("!!! :", output_path, video_FourCC, video_fps, video_size)
    out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
    blur_scores = []
    max_score, max_img = 0, None
    while True:
        return_value, frame = vid.read()
        if not return_value:
            break
        if angle != 0:
            # print(frame.shape, angle)
            frame = rotate(frame, angle)
            # print(frame.shape, angle)

        result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        score = lapulase(result)
        text = 'Blur: %.2f' % score
        blur_scores.append(score)
        cv2.putText(frame, text=text, org=(3, 15),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.50, color=(255, 0, 0), thickness=2)
        out.write(frame)
        if score > max_score:
            max_score = score
            max_img = frame

    out.release()
    vid.release()

    # 计算平均得分
    score = sum(blur_scores) / len(blur_scores)
    save_path = 'out_%.1f_%s' % (score, video_path.split('/')[-1])
    shutil.move(output_path, save_path)
    # save image
    save_path = 'out_%s.jpg' % (video_path.split('/')[-1])
    cv2.imwrite(save_path, max_img)
    return score


if __name__ == '__main__':
    import os
    import sys
    for path in os.listdir(sys.argv[1]):
        if not path.endswith('mp4'):
            continue
        path = os.path.join(sys.argv[1], path)
        score = video_blur(path)
        print('%s: %.1f' % (path, score))
