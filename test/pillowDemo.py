#c:/python36/

#-*- coding: utf-8 -*-

from PIL import Image
'''
Pillow库不会直接解码或者加载图像栅格数据。
当你打开一个文件，只会读取文件头信息用来确定格式，
颜色模式，大小等等，文件的剩余部分不会主动处理。
这意味着打开一个图像文件的操作十分快速，
跟图片大小和压缩方式无关。
'''
im = Image.open("../image/zq123.jpg")

#print(im.format, im.size, im.mode) # 打印图片的格式，大小， 像素类型

#im.show() 显示图片

# 加载图片， 并转化为png格式

import os
import  sys
import glob #智能化的批图像处理技术
'''
#for infile in sys.argv[1:]:
for infile in glob.glob("../image/zq123.jpg"):
    f, e = os.path.splitext(infile)
    outfile = f + '.png'
    if infile != outfile:
        try:
            print("Success")
            Image.open(infile).save(outfile)
        except IOError:
            print("Connot convert", infile)
'''

#create thumbnail 略缩图

size = (128, 128)
for infile in glob.glob("../image/zq123.jpg"):
    f, ext = os.path.splitext(infile)
    img = Image.open(infile)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(f + ".thumbnail",'JPEG')




