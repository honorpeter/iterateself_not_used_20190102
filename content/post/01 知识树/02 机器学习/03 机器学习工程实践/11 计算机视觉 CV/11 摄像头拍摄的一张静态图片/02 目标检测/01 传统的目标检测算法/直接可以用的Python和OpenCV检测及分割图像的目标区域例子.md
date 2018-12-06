---
title: 直接可以用的Python和OpenCV检测及分割图像的目标区域例子
toc: true
date: 2018-11-10
---

# 直接可以用的Python和OpenCV检测及分割图像的目标区域例子


在用深度学习的时候，比如说面对一张图像，对某个区域感兴趣怎么办？切割出来啊，只需要训练感兴趣的部分就好啦。

用一个可爱的虫子做为一个示例，目标是把虫子区域抠出来：

![mark](http://images.iterate.site/blog/image/181106/hGhGh0Lhbk.png?imageslim)



具体思路如下：

1.获取图片，这个简单哈

```
img_path = r'C:\Users\aixin\Desktop\chongzi.png'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

看，这不就是你处理初始的样子？

![mark](http://images.iterate.site/blog/image/181106/4IC8gGBakb.png?imageslim)

2.转换灰度并去噪声

```
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9),0)
```

我们可以得到这两张图，第一张是灰度图，第二张是去噪之后的，另外说一下，去噪咱们有很多种方法，均值滤波器、高斯滤波器、中值滤波器、双边滤波器等。

这里取高斯是因为高斯去噪效果是最好的。

![mark](http://images.iterate.site/blog/image/181106/f04JK94IA4.png?imageslim)

3.提取图像的梯度

```
gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)
```

以Sobel算子计算x，y方向上的梯度，之后在x方向上减去y方向上的梯度，通过这个减法，我们留下具有高水平梯度和低垂直梯度的图像区域。

此时，我们会得到

![mark](http://images.iterate.site/blog/image/181106/Gi9jeHc0DJ.png?imageslim)

4.我们继续去噪声

考虑到图像的孔隙 首先使用低通滤泼器平滑图像, 这将有助于平滑图像中的高频噪声。 低通滤波器的目标是降低图像的变化率。
如将每个像素替换为该像素周围像素的均值， 这样就可以平滑并替代那些强度变化明显的区域。

对模糊图像二值化，顾名思义，就是把图像数值以某一边界分成两种数值，细节我会附在文章底部，如果还是不懂，去cao文档吧。

```
blurred = cv2.GaussianBlur(gradient, (9, 9),0)
(_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
```

此时，我们会得到

![mark](http://images.iterate.site/blog/image/181106/ELIC3DEhaE.png?imageslim)


其实就算手动分割我们也是需要找到一个边界吧，可以看到轮廓出来了，但是我们最终要的是整个轮廓，所以内部小区域就不要了

5.图像形态学（牛逼吧、唬人的）

在这里我们选取ELLIPSE核，采用CLOSE操作，具体细节你依旧可以参考我的附录文档，及拓展。

```
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
```

此时，我们会得到

![mark](http://images.iterate.site/blog/image/181106/ibhCc6Bac8.png?imageslim)

6.细节刻画

从上图我们可以发现和原图对比，发现有细节丢失，这会干扰之后的昆虫轮廓的检测，要把它们扩充，分别执行4次形态学腐蚀与膨胀（附录文档）

```

closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=4)
```

此时，我们会得到

![mark](http://images.iterate.site/blog/image/181106/IkBHb5khl2.png?imageslim)

7.找出昆虫区域的轮廓

此时用cv2.findContours()函数
第一个参数是要检索的图片，必须是为二值图，即黑白的（不是灰度图）

```

(_, cnts, _) = cv2.findContours(
​    参数一： 二值化图像
​    closed.copy(),
​    参数二：轮廓类型
​    # cv2.RETR_EXTERNAL,             #表示只检测外轮廓
​    # cv2.RETR_CCOMP,                #建立两个等级的轮廓,上一层是边界
​    # cv2.RETR_LIST,                 #检测的轮廓不建立等级关系
​    # cv2.RETR_TREE,                 #建立一个等级树结构的轮廓
​    # cv2.CHAIN_APPROX_NONE,         #存储所有的轮廓点，相邻的两个点的像素位置差不超过1
​    参数三：处理近似方法
​    # cv2.CHAIN_APPROX_SIMPLE,         #例如一个矩形轮廓只需4个点来保存轮廓信息
​    # cv2.CHAIN_APPROX_TC89_L1,
​    # cv2.CHAIN_APPROX_TC89_KCOS
​    )
```

8.画出轮廓

找到轮廓了，接下来，要画出来的，即用cv2.drawContours()函数。


```

c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))

# draw a bounding box arounded the detected barcode and display the image
draw_img = cv2.drawContours(img.copy(), [box], -1, (0, 0, 255), 3)
cv2.imshow("draw_img", draw_img)
```

此时，我们会得到

![mark](http://images.iterate.site/blog/image/181106/k75DlGCaK8.png?imageslim)


9.裁剪出来就完成啦

方法嘛，这不就是么，找到这四个点切出来就好啦
我们放大一点看一下细节

![mark](http://images.iterate.site/blog/image/181106/iKJ6ga8bmE.png?imageslim)


```
Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = min(Xs)
x2 = max(Xs)
y1 = min(Ys)
y2 = max(Ys)
hight = y2 - y1
width = x2 - x1
crop_img= img[y1:y1+hight, x1:x1+width]
cv2.imshow('crop_img', crop_img)
```

其实，box里保存的是绿色矩形区域四个顶点的坐标。 我将按下图红色矩形所示裁剪昆虫图像。
找出四个顶点的x，y坐标的最大最小值。新图像的高=maxY-minY，宽=maxX-minX

![mark](http://images.iterate.site/blog/image/181106/0dCC856J07.png?imageslim)


终于我们得到了可爱的小虫子。
得到了目标区域，那么你想拿它干什么就干什么！我不管你哈。

考虑到现在的python教程一般都是一上来就是list、tuple什么的，而不是文件的读写和保存，包括批量读取等等，我特地加入了python版的文件批量读写和保存等附录文件。


完整代码如下：



```
#-*- coding: UTF-8 -*-

'''
Author: Steve Wang
Time: 2017/12/8 10:00
Environment: Python 3.6.2 |Anaconda 4.3.30 custom (64-bit) Opencv 3.3
'''

import cv2
import numpy as np


def get_image(path):
​    #获取图片
​    img=cv2.imread(path)
​    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    return img, gray

def Gaussian_Blur(gray):
​    # 高斯去噪
​    blurred = cv2.GaussianBlur(gray, (9, 9),0)

    return blurred

def Sobel_gradient(blurred):
​    # 索比尔算子来计算x、y方向梯度
​    gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
​    gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    return gradX, gradY, gradient

def Thresh_and_blur(gradient):

    blurred = cv2.GaussianBlur(gradient, (9, 9),0)
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)

    return thresh

def image_morphology(thresh):
​    # 建立一个椭圆核函数
​    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
​    # 执行图像形态学, 细节直接查文档，很简单
​    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
​    closed = cv2.erode(closed, None, iterations=4)
​    closed = cv2.dilate(closed, None, iterations=4)

    return closed

def findcnts_and_box_point(closed):
​    # 这里opencv3返回的是三个参数
​    (_, cnts, _) = cv2.findContours(closed.copy(),
​        cv2.RETR_LIST,
​        cv2.CHAIN_APPROX_SIMPLE)
​    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
​    # compute the rotated bounding box of the largest contour
​    rect = cv2.minAreaRect(c)
​    box = np.int0(cv2.boxPoints(rect))

    return box

def drawcnts_and_cut(original_img, box):
​    # 因为这个函数有极强的破坏性，所有需要在img.copy()上画
​    # draw a bounding box arounded the detected barcode and display the image
​    draw_img = cv2.drawContours(original_img.copy(), [box], -1, (0, 0, 255), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    crop_img = original_img[y1:y1+hight, x1:x1+width]

    return draw_img, crop_img

def walk():

    img_path = r'C:\Users\aixin\Desktop\chongzi.png'
    save_path = r'C:\Users\aixin\Desktop\chongzi_save.png'
    original_img, gray = get_image(img_path)
    blurred = Gaussian_Blur(gray)
    gradX, gradY, gradient = Sobel_gradient(blurred)
    thresh = Thresh_and_blur(gradient)
    closed = image_morphology(thresh)
    box = findcnts_and_box_point(closed)
    draw_img, crop_img = drawcnts_and_cut(original_img,box)

    # 暴力一点，把它们都显示出来看看

    cv2.imshow('original_img', original_img)
    cv2.imshow('blurred', blurred)
    cv2.imshow('gradX', gradX)
    cv2.imshow('gradY', gradY)
    cv2.imshow('final', gradient)
    cv2.imshow('thresh', thresh)
    cv2.imshow('closed', closed)
    cv2.imshow('draw_img', draw_img)
    cv2.imshow('crop_img', crop_img)
    cv2.waitKey(20171219)
    cv2.imwrite(save_path, crop_img)

walk()
```

附录2.本篇文章精华函数说明


```

# 用来转化图像格式的
img = cv2.cvtColor(src,
​    COLOR_BGR2HSV # BGR---->HSV
​    COLOR_HSV2BGR # HSV---->BGR
​    ...)
# For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]


# 返回一个阈值，和二值化图像，第一个阈值是用来otsu方法时候用的
# 不过现在不用了，因为可以通过mahotas直接实现
T = ret = mahotas.threshold(blurred)
ret, thresh_img = cv2.threshold(src, # 一般是灰度图像
​    num1, # 图像阈值
​    num2, # 如果大于或者num1, 像素值将会变成 num2
# 最后一个二值化参数
    cv2.THRESH_BINARY      # 将大于阈值的灰度值设为最大灰度值，小于阈值的值设为0
    cv2.THRESH_BINARY_INV  # 将大于阈值的灰度值设为0，大于阈值的值设为最大灰度值
    cv2.THRESH_TRUNC       # 将大于阈值的灰度值设为阈值，小于阈值的值保持不变
    cv2.THRESH_TOZERO      # 将小于阈值的灰度值设为0，大于阈值的值保持不变
    cv2.THRESH_TOZERO_INV  # 将大于阈值的灰度值设为0，小于阈值的值保持不变
)
thresh = cv2.AdaptiveThreshold(src,
​    dst,
​    maxValue,
​    # adaptive_method
​    ADAPTIVE_THRESH_MEAN_C,      
​    ADAPTIVE_THRESH_GAUSSIAN_C,      
​    # thresholdType
​    THRESH_BINARY,
​    THRESH_BINARY_INV,
​    blockSize=3,
​    param1=5
)


# 一般是在黑色背景中找白色物体，所以原始图像背景最好是黑色
# 在执行找边缘的时候，一般是threshold 或者是canny 边缘检测后进行的。
# warning:此函数会修改原始图像、
# 返回：坐标位置（x,y）,
(_, cnts, _) = cv2.findContours(mask.copy(),
​    # cv2.RETR_EXTERNAL,             #表示只检测外轮廓
​    # cv2.RETR_CCOMP,                #建立两个等级的轮廓,上一层是边界
​    cv2.RETR_LIST,                 #检测的轮廓不建立等级关系
​    # cv2.RETR_TREE,                   #建立一个等级树结构的轮廓
​    # cv2.CHAIN_APPROX_NONE,           #存储所有的轮廓点，相邻的两个点的像素位置差不超过1
​    cv2.CHAIN_APPROX_SIMPLE,       #例如一个矩形轮廓只需4个点来保存轮廓信息
​    # cv2.CHAIN_APPROX_TC89_L1,
​    # cv2.CHAIN_APPROX_TC89_KCOS
   )
img = cv2.drawContours(src, cnts, whichToDraw(-1), color, line)


img = cv2.imwrite(filename, dst,  # 文件路径，和目标图像文件矩阵

    # 对于JPEG，其表示的是图像的质量，用0-100的整数表示，默认为95
    # 注意，cv2.IMWRITE_JPEG_QUALITY类型为Long，必须转换成int
    [int(cv2.IMWRITE_JPEG_QUALITY), 5]
    [int(cv2.IMWRITE_JPEG_QUALITY), 95]
    # 从0到9,压缩级别越高，图像尺寸越小。默认级别为3
    [int(cv2.IMWRITE_PNG_COMPRESSION), 5])
    [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

# 如果你不知道用哪个flags，毕竟太多了哪能全记住，直接找找。
寻找某个函数或者变量
events = [i for i in dir(cv2) if 'PNG' in i]
print( events )

寻找某个变量开头的flags
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print flags

批量读取文件名字
import os
filename_rgb = r'C:\Users\aixin\Desktop\all_my_learning\colony\20170629'
for filename in os.listdir(filename_rgb):              #listdir的参数是文件夹的路径
    print (filename)
```








# 相关资料

- [直接可以用的Python和OpenCV检测及分割图像的目标区域例子](https://blog.csdn.net/sinat_36458870/article/details/78825571)
