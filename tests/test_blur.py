'''
图像模糊检测测试

Author: alex
Created Time: 2020年11月03日 星期二 10时03分21秒
'''
import shutil
import cv2
from image_utils.cv2_utils import lapulase


def video_blur(video_path):
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    # video_FourCC = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_FourCC = cv2.VideoWriter_fourcc(*'mp4v')
    video_fps    = vid.get(cv2.CAP_PROP_FPS)
    video_size   = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    output_path = 'out_%s' % video_path.split('/')[-1]
    print("!!! :", output_path, video_FourCC, video_fps, video_size)
    out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
    blur_scores = []
    max_score, max_img = 0, None
    while True:
        return_value, frame = vid.read()
        if not return_value:
            break
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
