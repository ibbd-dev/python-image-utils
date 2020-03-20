#!/bin/bash
# 
# 
# Author: alex
# Created Time: 2020年03月18日 星期三 21时12分01秒
cd ../
name="python-image-utils"
if [ ! -d "$name" ]; then
    echo "$PWD: 当前目录错误."
fi

date_str=`date -I`
filename="$name-${date_str//-/}".zip
if [ -f "$filename" ]; then
    rm -f "$filename"
fi

# 第一次打包时，记得把模型文件也打包在一起
# 正式发布时，记得过滤src目录中的内容
# -x "*/src/*" \
zip -r "$filename" "$name" \
    -x "*/.git/*" \
    -x "*/.*" \
    -x "*/*/*.swp" \
    -x "*/__pycache__/*" \
    -x "*/build/*" \
    -x "*/zip.sh" 

# scp "$filename" ibbd@192.168.80.242:~/ocr/ocr-v3/
mv "$filename" /var/www/src/git.ibbd.net/cv/

date
