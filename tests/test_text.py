# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2020年05月24日 星期日 10时26分26秒
from PIL import Image
from image_utils import text

# 写入中文汉字
img = Image.open('test.png')
text.add_chinese_img(img, (20, 20), '中国人')
img.save('/tmp/test_out1.jpg')

# 设置字体大小
img = Image.open('test.png')
text.set_font(font_size=18)
text.add_chinese_img(img, (20, 20), '中国人')
img.save('/tmp/test_out2.jpg')
