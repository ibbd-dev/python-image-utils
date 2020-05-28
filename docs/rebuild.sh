#!/bin/bash
# 
# 
# Author: alex
# Created Time: 2020年05月28日 星期四 18时26分17秒
# 复制配置文件
cp conf.py source/
cp index.rst source/

# 重新编译
make clean
pandoc -f markdown -t rst -o source/readme.rst ../README.md
sphinx-build -b html source build
make html

# 换行
echo "" >> build/_static/pygments.css
echo "" >> build/_static/pygments.css
echo "/* Added by rebuild.sh */" >> build/_static/pygments.css
echo "dl.function {white-space: pre}" >> build/_static/pygments.css
