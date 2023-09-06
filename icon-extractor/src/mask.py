# coding: UTF-8

import sys, PIL
import os

from PIL import Image, ImageOps

qr = sys.argv[1]

# 打开图片
im = Image.open(qr)

#获取图片的宽w和高h
w, h = im.size


# 根据图片尺寸选择合适的遮罩图片
if w == 512 and h == 307:
    # 选择maskTV.png进行遮罩，并转为灰度图像
    mask = Image.open('maskTV.png').convert('L')
elif w == 512:
    mask = Image.open('mask512.png').convert('L')
else:
    mask = Image.open('mask.png').convert('L')


# 使用ImageOps.fit()方法根据遮罩图片的尺寸将QR码图片进行调整
# 使用centering=(0.5, 0.5)参数确保QR码图片被居中放置
output = ImageOps.fit(im, mask.size, centering=(0.5,0.5))
# output.putalpha()方法将遮罩图片应用到输出图片中，以设置透明度
output.putalpha(mask)
# output.save()方法将合成后的图片保存为原始文件名加上’.png’的后缀
output.save(qr + '.png')