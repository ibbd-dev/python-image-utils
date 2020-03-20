# -*- coding: utf-8 -*-
#
# 安装程序
# Author: alex
# Created Time: 2018年04月02日 星期一 17时29分45秒
from distutils.core import setup


LONG_DESCRIPTION = """
常用图像处理工具库
""".strip()

SHORT_DESCRIPTION = """
常用图像处理工具库""".strip()

DEPENDENCIES = [
    'pillow',
    'opencv-python',
    'numpy',
]

VERSION = '0.1.1'
URL = 'https://github.com/cyy0523xc/python-image-utils'

setup(
    name='image_utils',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Alex Cai',
    author_email='cyy0523xc@gmail.com',
    license='Apache Software License',

    keywords='image utils',

    packages=['image_utils'],
)
