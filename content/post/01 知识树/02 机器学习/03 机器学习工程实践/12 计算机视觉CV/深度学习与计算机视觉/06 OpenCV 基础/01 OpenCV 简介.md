---
title: 01 OpenCV 简介
toc: true
date: 2018-08-29
---

# 6章 OpenCV基础

## 需要补充的

- <span style="color:red;">这部分简单看了下pdf，还是非常有意思的，是围绕数据增强提供了一些实现的方法，还有就是打标的工具，很nice。</span>
- <span style="color:red;">这部分暂时还没有进行整理，对于 OpenCV 的使用我其实有一些了解，因此这部分在整合 OpenCV 相关的时候整理进去。</span>
- 相关代码在 github 上是有的 https://github.com/frombeijingwithlove/dlcv_for_beginners

在深度学习大行其道之前，提到计算机视觉的工具和框架，大多数人一定会最先想到 OpenCV。因为其丰富的接口，优秀的性能，商业友好的属性，OpenCV至今仍然是最流行 的计算机视觉库，并在各个计算机视觉领域发挥着巨大的作用。

本章将介绍OpenCV的基本知识，以及Python下OpenCV的基础使用，并完成4个有 趣且实用的小例子。

延时摄影小程序。

视频中截屏采样的小程序。

图片数据增加（dataaugmentation）的小工具。

物体检测框标注小工具。

其中，后两个例子的代码可以在 <https://github.com/frombeijingwithlove/dlcv_for_> beginners上直接下载。

6.1 OpenCV 简介

OpenCV的起源和发展历史已经在第1章中介绍过了，本节主要介绍OpenCV的常见 模块和结构。

6.1.1 OpenCV 的结构

和Python—样，当前的OpenCV也有两个大版本，即OpenCV 2和OpenCV 3。相比 OpenCV 2, OpenCV 3提供了更强的功能和更多方便的特性。不过考虑到和深度学习框架 的兼容性，以及上手安装的难度，本节先以OpenCV 2为主进行介绍。

根据功能和需求的不同，OpenCV中的函数接口大体可以分为如下几部分。

□    core：核心模块，主要包含了 OpenCV中最基本的结构（矩阵、点线和形状等）， 以及相关的基础运算/操作。

□    imgproc：图像处理模块，包含和图像相关的基础功能（滤波、梯度、改变大小等）， 以及一些衍生的高级功能（图像分割、直方图、形态分析和边缘/直线提取等）。

□    highgui：提供了用户界面和文件读取的基本函数，比如图像显示窗口的生成和控 制，图像/视频文件的IO等。

如果不考虑视频应用，以上3部分就是最核心和常用的模块了。针对视频和一些特别 的视觉应用，OpenCV也提供了如下强劲的支持。

□    video：用于视频分析的常用功能，比如光流法（Optical Flow）和目标跟踪等。

□    calib3d：三维重建、立体视觉和相机标定等相关功能。

□    features2d：二维特征相关的功能，主要是一些不受专利保护的、商业友好的特征 点检测和匹配等功能，比如ORB特征。

□    object：目标检测模块，包含级联分类和Latent SVM。

□    ml：机器学习算法模块，包含一些视觉中最常用的传统机器学习算法。

口 flann：最近邻算法库，Fast Library for Approximate Nearest Neighbors,用于在多维 空间进行聚类和检索，经常和关键点匹配搭配使用。

□    gpu:包含了一些gpu加速的接口，底层的加速是CUDA实现。

□    photo：计算摄像学(Computational Photography)相关的接口，当然这只是个名字， 其实只有图像修复和降噪而已。

□    stitching：图像拼接模块，有了它可以自己生成全景照片。

□    nonfree：受到专利保护的一些算法，其实就是SIFT和SURF。

□    contrib： 一些实验性质的算法，考虑在未来版本中加入。

□    legacy：字面是遗产，意思就是废弃的一些接口，将其保留下来是考虑到向下兼容。

□    ocl:利用OpenCL并行加速的一些接口。

□    superres:超分辨率模块，其实就是 BTV-L1 (Biliteral Total Variation - LI regularization)算法。

□    viz:基础的3D渲染模块，其实底层就是著名的3D工具包VTK (Visualization Toolkit)。

从使用的角度来看，和OpenCV2相比，OpenCV 3的主要变化是更多的功能和更细化 的模块划分。

6.1.2安装和使用OpenCV

作为最流行的视觉包，在Linux中安装OpenCV是非常方便的，大多数Linux的发行 版都支持包管理器的安装，比如在Ubuntu 16.04 LTS中，只需要在终端中输入：

» sudo apt install libopencv-dev python-opencv

当然也可以通过官网下载源码编译安装，首先安装各种依赖。

» sudo apt install build-essential

»    sudo apt install cmake    git libgtk2.0-dev    pkg-config

libavcodec-dev libavformat-dev libswscale-dev

»    sudo apt-get    install    python-dev    python-numpy libtbb2    libtbb-dev

libjpeg-dev libpng-dev libtiff-dev libj asper-dev libdcl3 94-22-dev

然后找一个clone压缩包的文件夹，将源码下载下来。

\>> git clone <https://github.com/opencv/opencv.git>

然后进入OpenCV文件夹。

» mkdir release » cd release

» cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREF工X=/usr/local.. 准备完毕，直接make并安装。

\>> make

» sudo make install

Windows 下的安装也很简单，直接去 OpenCV 官网 <http://opencv.org/downloads.html> 下 载即可。

执行exe文件安装后，会在＜安装目录〉\build\python/2.7下发现一个cv2.pyd的文件， 把该文件复制到＜?外11011目录〉\Lib\site-packages下就可以了。Windows下如果只想在Python 中体验OpenCV,有个更简单的方法是加州大学尔湾分校(University of California，Irvine) 的Christoph Gohlke制作的Windows下的Python科学计算包网页，下载对应版本的wheel 文件，然后通过 pip 安装即可，下载地址为 [http://www.lfd.uci.edU/~gohlke/pythonlibs/#opencvo](http://www.lfd.uci.edu/~gohlke/pythonlibs/%23opencvo)

本节只讲Python下的OpenCV基本用法，Python中导入OpenCV非常简单： import cv2 这样就导入成功了。

6.2 Python-OpenCV 基础

本节主要讲解在Python中利用OpenCV的图像存取，以及与深度学习中图像预处理阶 段相关的最基本使用。

6.2.1图像的表示

前面章节已经提到过了单通道的灰度图像在计算机中的表示，就是一个8位无符号整 形的矩阵。在OpenCV的C++代码中，表示图像有个专门的结构cv::Mat,不过在 Python-OpenCV中^因为已经有了 NumPy这种强大的基础工具，所以这个矩阵就用NumPy 的array表示。如果是多通道情况，最常见的就是红绿蓝(RGB)三通道，则第一个维度 是高度，第二个维度是高度，第三个维度是通道，如图6-la所示为一幅3x3图像在计算机 中表示的例子。



分通道表示

◄-

RBG表示

| 255,0,0     | 0,255,0     | 0,0,255   |
| ----------- | ----------- | --------- |
| 255,255,0   | 255,0,255   | 0,255,255 |
| 255,255,255 | 128,128,128 | 0,0,0     |

| BGR表示



a)

b)

图6-1 RGB图像在计算机中表示的例子

在图6-1中，右上角的矩阵里每个元素都是一个三维数组，分别代表这个像素上的三

个通道的值。最常见的RGB通道中，第一个元素就是红色(Red)的值，第二个元素是绿

色(Green)的值，第三个元素是蓝色(Blue)，最终得到的图像如图6-la所示。RGB是

最常见的情况，然而在OpenCV中，默认的图像表示却是反过来的，也就是BGR，得到的

图像如图6-lb所示。可以看到，前两行的颜色顺序都交换了，最后一行是三个通道等值的

灰度图，所以没有影响。至于OpenCV为什么不是大家喜闻乐见的RGB,则是历史遗留问

题。在OpenCV刚开始研发的年代，BGR是相机设备厂商的主流表示方法，虽然后来RGB

成了主流和默认，但是这个底层的顺序却保留了下来，事实上Windows下的最常见格式之

一 bmp的底层字节的存储顺序还是BGR。OpenCV的这个特殊之处还是需要注意的，比如

在Python中，图像都是用NumPy的array表示，但是同样的array在OpenCV中的显示

效果和matplotlib中的显示效果就会不一样。下面的简单代码就可以生成两种表示方式下

图6-1中矩阵对应的图像，生成图像后，放大看就能体会到二者的区别。

import numpy as np import cv2

import matplotlib.pyplot as pit

\#图6-1中的矩阵 img = np.array ([

[[255, 0, 0],队 255, 0], [0, 0, 255]],

[[255,    255,    0],    [255, 0r 255],    [0,    255,    255]],

[[255, 255, 255], [128, 128, 128], [0, 0, 0/j <

], dtype=np.uint8)

\# 用 matplotlib 存储

pit.imsave(* img_pyplot.jpg *, img)

\#用OpenCV存储

cv2 . imwrite (' img_cv2 .jpg', img)

不管是RGB还是BGR,都是高度x宽度x通道数，HxWxC的表达方式，而在深度学 习中，因为要对不同通道应用卷积，所以用的是另一种方式：CxHxW,就是把每个通道都 单独表达成一个二维矩阵，如图6-lc所示。

6.2.2基本图像处理

1.存取图像

读图像用CV2.imread()函数，可以按照不同模式读取，一般最常用到的是读取单通道灰 度图，或者直接默认读取多通道。保存图像用cv2.imwrite()函数，注意保存的时候是没有 单通道这一说的，根据保存文件名的后缀和当前的array维度，OpenCV自动判断存储的通 道。另外，压缩格式还可以指定存储质量，下面来看代码例子。

import cv2

\#读取一张400x600分辨率的图像

color_img = cv2.imread(* test_400x600.jpg *)

print(color_img.shape)

\#直接读取单i道

gray_img = cv2.imread(* test_4 00x600.jpg', cv2.工MREAD—GRAYSCALE) print(gray_img.shape)

\#把单通道菌片保存后，再读取，仍然是3通道，相当于把单通道值复制到3个通道保存 cv2.imwrite('test_grayscale.jpg', gray_img)

reload_grayscale = cv2.imread(* test_grayscale.jpg *) print(reload—grayscale.shape)

\#    cv2.IMWRITE_JPEG_QUALITY指定jpg质量，范围为0〜100,默认95,越高画质越好，文

件越大

cv2.imwrite('test_imwrite.jpg', color_img,    (cv2.工MWRITE一JPEG_QUALITY,

80))

\#    cv2.IMWRITE_PNG_COMPRESSION指定png质量，范围为0〜9:默认3，越高文件越小，画

质越差

cv2 . imwrite (* test_imwrite .png *, color_img, (cv2 .工MWR工TE—PNG—COMPRESS工ON, 5))

\2.    缩放、裁剪和补边

缩放通过cv2.resize()函数实现，裁剪则是利用array自身的下标截取实现，此外OpenCV 还可以给图像补边，这样能对一幅图像的形状和感兴趣区域实现各种操作。下例中读取一 幅400x600分辨率的图片，并执行一些基础的操作。

import cv2

\#读取一张四川大录古藏寨的照片

img = cv2.imread(* tiger_tibet_village.jpg')

\#缩放成200x200的方形图像

img_200x200    = cv2.resize(imgz (200,    200))

\#示直接指定缩放后大小，通过fx和fy指定缩放比例，0.5则长宽都为原来一半

\#等效于img_200x300    = cv2 .resize (img, (300,    200))，注意指定大小的格式是(宽

度，局度)

\#插值方法默认是cv2.INTER_LINEAR，这里指定为最近邻插值 img_200x300    = cv2.resize(img, (0,    0), fx=0.5, fy=0.5Z

interpolation=cv2.工NTER_NEAREST)

\#在上张图片的基础上，上下吝贴50像素的黑边，生成300x300的图像 img_300x300    = cv2.copyMakeBorder(imgf 50,    50,    0,    0,

cv2 .BORDER_C(^NSTANT,

value=(0,    0,    0))

\#对照片中树的部分进行剪裁

patch_tree = img[20:150,    -180:-50]

cv2.imwrite('cropped_tree.jpg *, patch_tree)

cv2.imwrite('resized_200x200.jpg', img_200x200)

cv2.imwrite(* resized_200x300.jpg', img_200x300)

cv2.imwrite(*bordered_300x300.jpg *,    img_300x300)

处理的效果如图6-2所示。

\3.    色调、明暗、直方图和Gamma曲线

除了区域，图像本身的属性操作也非常多，比如可以通过HSV空间对色调和明暗进行

调节。HSV空间是由美国的图形学专家A. R. Smith提出的一种颜色空间，HSV分别是色

调(Hue),饱和度(Saturation)和明度(Value)。在HSV空间中进行调节就避免了直

接在RGB空间中调节时还需要考虑3个通道的相关性。OpenCV中H的取值是[0, 180),

其他两个通道的取值都是[0,256),下面接着上例代码，通过HSV空间对图像进行调整。

\#通过cv2 . cvtColor把图像从BGR转换到HSV img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

\#    tF空间中，绿色比黄色的值高一点，所以给每个像壽+15,黄色的树叶就会变绿 turn_green_hsv = img_hsv.copy()

turn_green_hsv [:,    :,    0]    =    (turn_green_hsv [:,    :,    0] +15)    %    180

turn_green_img = cv2 . cvtColor (turn_green_hsv/. cv2 . COLOR—HSV2BGR)

cv2.imwrite(1turn_green.jpg’， turn_green_img)

\#减小饱和度会让图损失鲜艳变得更灰

colorless_hsv = img_hsv.copy()

colorless_hsv [:,    :,    1]    =    0.5    * colorless_hsv [:,    :,    1 ]

coloriess_img = cv2.cvtColor(colorless_hsv, cv2.COLOR_HSV2BGR) cv2.imwrite(1 colorless.jpg1, colorless_img)

\#减小明度为原来一半 darker_hsv = img_hsv.copy()

darker_hsv [:,    :,    2]    =    0.5    * darker_hsv [:,    :,    2]

darker_img = cv2.cvtColor(darker_hsvf cv2.COLOR_HSV2BGR) cv2.imwrite(’ darker.jpg’， darker_img)

无论是HSV还是RGB,都较难一眼就对像素中值的分布有细致的了解，这时候就需 要直方图。如果直方图中的成分过于靠近0或者255,可能就出现了暗部细节不足或者亮 部细节丢失的情况。比如图6-2中，背景里的暗部细节是非常弱的，这个时候，一个常用 方法是考虑用Gamma变换来提升暗部细节。Gamma变换是矫正相机直接成像和人眼感受 图像差别的一种常用手段，简单来说就是通过非线性变换，让图像从对曝光强度的线性响 应变得更接近人眼感受到的响应。具体的定义和实现还是接着上面代码中读取的图片，执 行计算直方图和Gamma变换的代码如下：

import numpy as np

\#分通道计算每个通道的直方图

| hist_b = | cv2.calcHist([img], | [0], | None, | [256], | [o,  | 256])  |
| -------- | ------------------- | ---- | ----- | ------ | ---- | ------ |
| hist_g = | cv2.calcHist([img], | [1], | None, | [256], | [0,  | <256]) |
| hist r = | cv2.calcHist([img], | [2], | None, | [256], | [0,  | 256])  |

\#定义Gamma矫正的函数

def gamma_trans(img, gamma):

\#真体做法是先归一化到1,然后gamma作为指数值求出新的像素值再还原 gamma_table = [np.power(x/255.0z gamma)*255.0 for x in

range (256)]

gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)

\#实现映射用的是OpenCV的查表函数 return cv2.LUT(img, gamma_table)

\#执行Gamma矫正，小于1的值让暗部细<大量提升，同时亮部细节少量提升

img_corrected = gamma_trans(img, 0.5)

cv2.imwrite('gamma_corrected.jpg' , img_corrected)

\#分通道计算Gamma f正后的直方图

| hist b corrected =           | cv2.calcHist([img_corrected], | [0], | None, | [256], |
| ---------------------------- | ----------------------------- | ---- | ----- | ------ |
| [0, _256])hist g corrected = | cv2.calcHist([img corrected], | [1], | None, | [256], |
| [0, _256])hist r corrected = | cv2.calcHist([img_corrected], | [2], | None, | [256], |
| [0, _256])                   |                               |      |       |        |

\#将直方图进行可视化

import matplotlib.pyplot as pit

from mpl_toolkits.mplot3d import Axes3D

fig = pit.figure()

pix_hists =    [

[hist_b, hist_g, hist_r],

[hist_b_corrected, hist_g_corrected, hist_r_corrected]

]

pix_vals = range(256)

for sub_plt, pix_hist in zip([121,    122], pix_hists):

ax = fig.add_subplot(sub_pltz projection^3d*)

for c, z, channel_hist in zip([1b1,    1g'z 'r'],    [20,    10,

0] , pix_hist):

cs =    [c]    *    256

color=csz

ax.bar(pix_vals, channel一hist, zs=z, zdir=1y*, alpha=0.618, edgecolor='none *, lw=0)

ax.set_xlabel(* Pixel Values *) ax.set_xlim([0z 256]) ax.set_ylabel(丨 Counts’) ax.set_zlabel('Channels')

pit.show()

上面三段代码的结果统•放在图6-2中。



缩放->200x300

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-240.jpg)

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-241.jpg)

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-242.jpg)

缩放 ^200x200

缩放并补边一＞300x300区域剪裁



原图:400x600



![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-245.jpg)

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-246.jpg)

色调变绿    饱和度降低    明暗度降低





通过Gamma变换提升暗部细节

图6-2

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-249.jpg)

Jwooo

1, J



对应的各通道直方图 左为原图，右为Gamma变换后

图像基本处理的例子

可以看到，Gamma变换后的暗部细节比原图清楚了很多，并且从直方图来看，像素值 也从集中在0附近变得散开了一些。

6.2.3图像的仿射变换

图像的仿射变换涉及图像的形状位置角度的变化，是深度学习预处理中常用的功能。 仿射变换的概念前面已经提到，在此简单回顾一下。仿射变换具体到图像中的应用，主要

第6章OpenCV基础

:    ■■■ ■■ ■. 二.， ..... ........ =

是对图像的缩放、旋转、剪切、翻转和平移的组合。在OpenCV中，仿射变换的矩阵是一 个2x3的矩阵，其中左边的2x2子矩阵是线性变换矩阵，右边的2x1的两项是平移项。

“00 “01 “10 a\\

(公式6-1)

Moo

a\Q

aQ\ ^0 a\\ ^1

对于图像上的任一位置仿射变换执行的是如下的操作

Taffine

(公式6-2)

需要注意的是，对于图像而言，宽度方向是x,高度方向是y,坐标的顺序和图像像素 对应下标一致。所以原点的位置不是左下角而是右上角，的方向也不是向上而是向下。 在OpenCV中实现仿射变换是通过仿射变换矩阵和cv2. warp Affine函数。下面还是通过代 码来理解一下，例子中图片的分辨率为600x400。    /

import cv2

import numpy as np

\#读取一张斯里兰卡拍摄的大象照片

img = cv2.imread(*lanka_safari.jpg *)

\#沿着横纵轴放大1.6倍，然后"平移(-150,-240)，最后沿原图大小截取，等效于裁剪并放大

M_crop_elephant 一 [1.6, 0,

=np.array([ -150],

-240]

[0, 1.6,

], dtype=np.float32)

cv2.imwrite('lanka_safari_rotated.jpg*, img_rotated)

\#某种变换，具体几何S义可以过SVD分解理解

M = np.array([

[1,    1.5,    -400],

[0.5,    2,    -100]

], dtype=np.float32)

img_transformed = cv2.warpAffine(img, M, (400，    600))

cv2•imwrite('lanka_safari_transformed.jpg', img_transformed)

代码实现的操作示意如图6-3所示。



图6-3仿射变换的例子

6.2.4基本绘图

OpenCV癍供各种绘图的函数，可以在画面上绘制线段、圆、矩形和多边形等，还 可以在图像上指定位置打印文字，比如下面例子：

import numpy as np

import cv2

\#定义一块宽600、高400的画布，初始化为白色

| cv2.line(canvas, (300,    149),    (599, | 149),  | (0, 0, | 0),  | 2)    |      |      |
| ---------------------------------------- | ------ | ------ | ---- | ----- | ---- | ---- |
| #左半部分的右下角画个红色的圆            |        |        |      |       |      |      |
| cv2.circle(canvas, (200,    300),    75, | (0, 0, | 255),  | 5)   |       |      |      |
| #左半部分的左下角画个蓝色的矩形          |        |        |      |       |      |      |
| cv2.rectangle(canvas,    (20,    240),   | (100,  | 360),  |      | (255, | 0,   | 0),  |

\#定义两个三角形，并执行内部绿色填充

(255,    333)],

(100,    237)]])

(0,    255,    0))

rotations =    [[[np.cos (i *

phi), -np.sin (i for i in range (1,

phi)], 5)]

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-252.jpg)

np.sin(phi), np.cos (i * phi)]]

pentagram = np.array([[[[ 0,    -1]]    + [np.dot(m,    (0,    -1)) for m in

rotations]]], dtype=np.float)

\#定义缩放倍数和平移向量，把五角星画在左半部分画面的上方

pentagram = np.round(pentagram *    80    + np.array([160,    120])).astype

(np.int)

\#将5个顶点作为多边形顶点连线，得到五角星

255]]], dtype=np.uint8)

line_color =    [int(c) for c in cv2.cvtColor(color_pixelz

cv2.COLOR_HSV2BGR)[0][0]]

cv2.line(canvas, (x,    0),    (x,    147), line_color)

\#如果定义圆的线宽大于半斤，则等效于画圆点，随机在画面右卞為的框内生成坐标

np.random.seed(42)

n_pts = 30

pts_x = np.random.randint (310, 590, n_pts) pts_y = np.random.randint (160, 390, n_pts) pts = zip (pts_x, pts_y)

\#画出每个点，颜色随机

for pt in pts:

pt_color =    [ int(c) for c in np.random.randint(0,

255,

3)]

cv2.circle(canvas, pt, 3, pt_color, 5)

\#在左半部分最上方打印文字    _    /

cv2.putText(canvas,

'Python-OpenCV Drawing Example 1,

(5,    15),

cv2.FONT HERSHEY SIMPLEX,

0.5,

(0, 0, 0),

1)

cv2.imshow(1 Example of basic drawing functions *, canvas cv2.waitKey()

执行代码效果如图6-4所示。



图6-4基本绘图的例子

6.2.5视频功能

视频中最常用的就是从视频设备采集图片或者视频，或读取视频文件并从中采样。所 以比较重要的也是两个模块，一个是VideoCapture,用于获取相机设备并捕获图像和视频， 或是从文件中捕获；还有一个是VideoWriter,用于生成视频。下面来看例子理解这两个功

能的用法，首先是一个制作延时摄影视频的小例子。 import cv2 import time

interval = 60    #捕获图像的间隔，单位：秒

num_frames =    500    #捕获图像的总巾贞数

out_fps =    24    #输出文件的巾贞率

林VideoCapture (0)表示打开默认的相机 cap = cv2.VideoCapture (0)

\#获取捕获的分辨率

size =(int (cap.get (cv2.CAP_PROP_FRAME一WIDTH)),

int (cap.get (cvSTcapJrOP-FSamE—HEIGHT)))

\#设置要保存视频的编码，分辨率和帧率

video = cv2.VideoWriter(

"time_lapse.avi",

cv2.VideoWriter_fourcc('M*,'P1,'4 *,'2’)，

out_fps,

size

)

\#对于一些低画质的摄像头，前面的帧可能不稳定，略过

for i in range(42):

cap.read()

\#开始捕获，通过read函数获取捕获的帧 try:

for i in range(num_frames):

frame = cap.read()

video.write(frame)

\#如果希望每一帧也存成文件，比如制作GIF,则取消下面的注释

\#    filename =    1{:0>6d}.png1.format(i)

\#    cv2.imwrite(filename, frame)

print('Frame {} is captured.1.format(i)) time.sleep(interval)

except Keyboardlnterrupt:

\#提前停止捕获

print(* Stopped!    {}/{} frames captured!*.format(i, num_frames))

\#释放资源并写入视频文件 video.release() cap.release()

该例实现了延时摄影的功能，把程序打开并将摄像头对准一些缓慢变化的画面，比如 桌上缓慢蒸发的水，或者正在生长的小草，就能制作出有趣的延时摄影作品。

程序的结构非常清晰简单，注释里也写清楚了每一步，所以程序流程就不多解释了。 需要提一下的有两点：一个是VideoWriter中的函数cv2.VideoWriter fourcco该函数指定 了视频编码的格式，比如例子中用的是MP42,也就是MPEG-4,更多编码方式可以在下 面的地址查询 <http://www.fourcc.org/codecs.phpo>

还有一个是Keyboardlnterrupt,这是一个常用的异常，用来获取用户Ctrl+C的中止， 捕获这个异常后直接结束循环并释放VideoCapture和VideoWriter的资源，使已经捕获好 的部分视频可以顺利生成。

从视频中截取帧也是处理视频时常见的任务，下面代码实现的是遍历一个指定文件夹 下的所有视频，并按照指定的间隔进行截屏保存。

import cv2 import os import sys

\#第一个输入参数是包含视频片段的路径

input_path = sys.argv[1]

\#第三个输入参数是设定每隔多少帧截取一帧

frame_interval = int(sys.argv[2])

\#列tS文件夹下所有的视频文件 filenames = os . listdir(input_path)

\#获取文件夹名称

video_prefix = input_path.split(os.sep) [-1]

\#建立一个新的文件夹，名称为原文件夹名称后加上_frames frame一path =    1{}_frames'.format(input_path)

if not os.path.exists(frame_path):

os.mkdir(frame_path)

\# 初始化一个VideoCapture对象 cap = cv2.VideoCapture()

\#遍历所有文件

for filename in filenames:    /

filepath = os.sep.join([input_path, filename])

\# VideoCapture::open函数可以从文件获取视频 cap.open(filepath)

\#获取视频帧数

n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

同样为了避免视频头几帧质量低下，黑i或者免关等_

for i in range(42): cap.read()

for i in range(n_frames):

ret, frame = cap.read()

\#每隔frame_interval巾贞进行一次截屏操作 if i % f rame_interval ==    0:

imagename =    •{}_{}_{:0>6d}•jpg’•format(video_prefix,

filename.split(1.*) [0]f i)

imagepath = os.sep.join([frame_path, imagename]) print(* exported {}!*.format(imagepath)) cv2.imwrite(imagepath, frame)

\#执行结束释放资源

cap.release()

6.3用OpenCV实现数据增加小工具

到目前我们已经熟悉了 NumPy中的随机模块、多进程调用和OpenCV的基本操作， 基于这些基础，本节将从思路到代码一步步实现一个最基本的数据增加小工具。

第3章和第4章都提到过数据增加(data augmentation),作为一种深度学习中的常用

手段，数据增加对模型的泛化性和准确性都有帮助。数据增加的具体使用方式一般有两 种，一种是实时增加，比如在Caffe中加入数据扰动层，每次图像都先经过扰动操作，再 去训练，这样训练经过几代（epoch）之后，就等效于数据增加。还有一种方式是更加直 接简单一些的，就是在训练之前通过图像处理手段对数据样本进行扰动和增加，也是本 节要实现的。

本节的例子中将包含3种基本类型的扰动：随机裁剪、随机旋转和随机颜色/明暗。

6.3.1随机裁剪

在AlexNet中已经讲过了随机裁剪的基本思路，本节的小例子中打算更进一步：在裁 剪的时候考虑图像宽高比的扰动。在绝大多数用于分类的图片中，样本进入网络前都是要 统一大小，所以宽高比扰动相当于对物体的横向和纵向进行了缩放，这样除了物体的位置 扰动，又多出了一项扰动。只要变化范围控制合适，目标物体始终在画面内，这种扰动是 有助于提升泛化性能的。实现这种裁剪的思路如图6-5所示。



图6-5中最左边是一幅需要剪裁的画面，首先根据这幅画面可以算出一个宽高比w/h. 然后设定一个小的扰动范围3和要裁剪的画面占原画面的比例々，从-<5到3之间按均匀采 样，获取一个随机数》作为裁剪后画面的宽高比扰动的比例，则裁剪后画面的宽和高分 别为：



如果先把这个宽为高为A’的区域置于原画面的右下角，则这个区域的左上角和原 画面的左上角框出的小区域，如图6-5b中的虚线框所示，就是裁剪后区域左上角可以取值 的范围。所以在这个区域内随机采一点作为裁剪区域的左上角，就实现了如图6-5c中，位 置随机且宽高比也随机的裁剪。

6.3.2随机旋转

与前面讲到过的旋转比起来，做数据增加时，一般希望旋转是沿着画面的中心。这样

除了要知道旋转角度，还要计算平移的量才能让仿射变换的效果等效于旋转轴在画面中心， 好在OpenCV中有现成的函数cv2.getRotationMatrix2D()可以使用。该函数的第1个参数是 旋转中心，第2个参数是逆时针旋转角度，第3个参数是缩放倍数，对于只是旋转的情况 参数值是1,返回值就是做仿射变换的矩阵。

直接用cv2.getRotationMatrix2D()函数并接着使用 cv2.warpAffine()函数会有一个潜在的问题，就是旋转之后 会出现黑边。如果要旋转后的画面不包含黑边，则需沿着 原来画面的轮廓做内接矩形，该矩形的宽高比和原画面相 同，如图6-6所示。

| iAP' |      |      |             |
| ---- | ---- | ---- | ----------- |
| //   |      |      | 、、1///•!/ |
| 丄   |      |      | :t//1!1/    |

在图6-6中可以看到，限制内接矩形大小的主要是原 画面更靠近中心的那条边，也就是图6-6中比较长的一条 边因此只要沿着中心O和内接矩形的顶点方向的直 线，求出和」5的交点P，就得到了内接矩形的大小。下 面先来看长边的方程，考虑之前画面和横轴相交的点，经 过角度旋转后，到了图6-5中的0点所在。

图6-6随机旋转，不含黑边裁剪

os（-0） -sin（-0） in（-0） cos （-沒）

|      |      | 子OS⑻   |
| ---- | ---- | ------- |
| 2    | =    |         |
| 0 _  |      | \|sin ⑻ |

因为长边所在直线过0点，且斜率为l/tan(0，所以有:

sin

（公式6-4）

x + ^cos（^）

这时候考虑OP这条直线:

（公式6-5）

把公式6-5带入公式6-4,求解可以得到：

w cos(0) + sin (0)tan (0)

（公式6-6）

h

—tan （汐）+ 1

w

注意，在这个问题中，每个象限和相邻象限都是轴对称的，而且旋转角度对剪裁宽度 和长度的影响是周期(7Mr)变化。再加上我们关心的其实并不是4个点的位置，而是旋 转后要截取的矩形的宽W和高A',所以复杂的分区间情况也简化了。首先对于旋转角度， 因为周期为K，所以都可以化到0到7T之间。因为相邻象限的对称性，进一步有：

0，6^k/2 Tl-d,其他

（公式6-7）

###### 于是对于0到7T/2之间的0，有:



9 h>w ，其他

cos （沒）+ sin （汐）tan （汐）

r tan （权）+ 1

（公式6-8）

当然需要注意的是，对于宽高比非常大或者非常小的图片，旋转后如果裁剪往往得到 的画面是非常小的一部分，甚至不包含目标物体。所以是否需要旋转，以及是否需要裁剪， 裁剪角度多少合适，都要视情况而定。

6.3.3随机颜色和明暗

比起AlexNet论文里在PCA之后的主成分上做扰动的方法，本节用来实现随机的颜色 以及明暗的方法相对简单很多，就是给HSV空间的每个通道分别加上一个微小的扰动。其 中对于色调，从到<5之间按均匀采样，获取一个随机数S作为要扰动的值，然后新的像 素值X’为原始像素值;v+J;对于其他两个空间则是新像素值/为原始像素值*的(1 + J)倍， 从而实现色调、饱和度和明暗度的扰动。

因为明暗度并不会对图像的直方图相对分布产生大的影响，所以在HSV扰动基础上， 考虑再加入一个Gamma扰动，方法是设定一个大于1的Gamma值的上限y,因为这个值 通常和1是一个量级，再用均匀采样的近似未必合适，所以从-logy到logy之间均匀采样一 个值a，然后用ea7作为Gamma值进行变换。

6.3.4多进程调用加速处理

做数据增加时如果样本量本身就不小，则处理起来可能会很耗费时间，所以可以考虑 利用多进程并行处理。比如我们的例子中，设定使用场景是输入一个文件夹路径，该文件 夹下包含了所有原始的数据样本。用户指定输出的文件夹和打算增加图片的总量。执行程 序的时候，通过os.listdirO函数获取所有文件的路径，然后按照第5章讲过的多进程平均划 分样本的办法，把文件尽可能均匀地分给不同进程，进行处理。

6.3.5代码：图片数据增加小工具

按照前面4个部分的思路和方法，本节来实现一个图片数据增加小工具，首先对于一 些基础的操作定义在一个image augmentation.py的文件里。

import numpy as np import cv2

定义裁剪函数，四个参数分别是: 左上角横坐标xO 左上角纵坐标yO

裁剪宽度w

裁剪高度h

I »曹

crop_image = lambda img, xO, yO, w, h: img[yO:yO+hz xO:xO+w]

V    I V

随机裁剪

area_ratio为裁剪画面占原画面的比例

hw_vari是扰动占原高宽比的比例范围

V    V I

def random_crop(img, area_ratio, hw_vari): h, w = img.shape[:2]

hw_delta = np.random.uniform(-hw_vari, hw_vari) hw_mult =    1    + hw_delta

\#下标进行裁剪，宽高必须是正整数

w_crop = int(round(w*np.sqrt(area_ratio*hw_mult)))

\#裁剪宽度不可超过原图可裁剪宽度

if w_crop > w:

w_crop = w

h_crop = int(round(h*np.sqrt(area_ratio/hw_mult))) if h_crop > h:

h_crop = h

\#随机生成左上角的位置    <

xO = np.random.randint(0, w-w_crop+l) yO = np.random.randint(0, h-h_crop+l) return crop_image(img, xO, yO, w_crop, h_crop)

V V V

定义旋转函数：

angle是逆时针旋转的角度

crop是个布尔值，表明是否要裁剪去除黑边

I I I

def rotate_image(img, angle, crop): h, w = img.shape[:2]

\#旋转角度的周期是360° angle %= 360

\#用OpenCV内置函数计算仿射矩阵

M_rotate = cv2•getRotationMatrix2D((w/2,    h/2), angle, 1)

\#得到旋转后的图像

img_rotated = cv2.warpAffine(img, M_rotate, (w, h))

\#远果需要裁剪去除黑边

if crop:

\#计算高宽比

hw_ratio = float(h)    / float(w)

\#计算裁剪边长系数的分子项

tan_theta = np.tan(theta)

numerator = np.cos(theta) + np.sin(theta) * tan_theta

\#计算分母项中和宽高比相关的项

r = hw_ratio if h > w else 1    / hw_ratio

\#计算分母项

denominator = r * tan_theta +    1

\#计算最终的边长系数

crop_mult = numerator / denominator

\#得到裁剪区域

w_crop = int(round(crop_mult*w)) h_crop = int(round(crop_mult*h)) xO = int((w-w_crop)/2)

yO = int((h-h_crop)/2)

img_rotated = crop_image(img_rotatedz xO, yO, w_crop,

h_crop)

return img_rotated

随机旋转

angle_vari是旋转角度的范围[-angle_ vari, angle_vari)

p_crop是要进行去黑边裁剪的比例

I V I

def random_rotate(img, angle_variz p_crop):

angle = np.random.uniform(-angle一vari, angle_vari) crop = False if np. random. random ()    > p_crop else True

returh rotate_image(img, angle, crop)

定义hsv变换函数： hue_delta是色调变化比例 saCdelta是饱和度变化比例 val^delta是明度变化比例

def hsv transform(img, hue delta, sat mult, val mult):

img hsv

cv2

img_hsv[:, img_hsv[:, img_hsv[:, img_hsv[img_hsv return

COLOR HSV2BGR)

cv2.cvtColor(img, cv2.COLOR BGR2HSV).astype(np.float)

0]    = (img_hsv[:,    :,    0]    +    hue_delta)    %    180

1]    *= sat_mult

2]    ★= val_mult

\>    255]    =— 255

cv2.cvtColor(np.round(img_hsv).astype(np.uint8)

随机hsv变换

hue_vari是色调变化比例的范围

sat^vari是饱和度变化比例的范围

val_vari是明度变化比例的范围

V曹V

def random_hsv_transform(img, hue_vari, sat_vari, val_vari): hue_delta = np.random.randint(-hue_vari, hue_vari) sat_inult = 1 + np. random.uniform (-sat_vari, sat_vari) val_mult = 1 + np.random.uniform(-val_vari, val_vari) return hsv_transform(img, hue_delta, sat_mult, val_mult)

定义gamma变换函数： gamma 就是 Gamma

I I I

def gamma_transform(img, gamma):

gamma_table = [np.power(x /    255.0, gamma) *    255.0 for x in

range(256)]

gamma_table = np.round(np.array(gamma_table)).astype(np.uint8) return cv2.LUT(img, gamma_table)

I I I

随机gamma变换

gamma_vari 是 Gamma 变化的范围[l/garmna_vari, gamma_vari)

I V I

def random_garmna_transform(img, gamma_vari): log_gamma_vari = np.log(gamma_vari)

alpha = np.random.uniform(-log_gamma_vari, log_gamma_vari)

gamma = np.exp(alpha)

return gamma_transform(imgz gamma)

调用这些函数需要通过一个主程序。主程序里首先定义3个子模块，定义一个函数

parse_arg()通过Python的argparse模块定义各种输入参数和默认值。需要注意的是这里用

argparse来输入所有参数，是因为参数总量并不是特别多，如果增加了更多的扰动方法，

更合适的参数输入方式可能是通过-•个配置文件。然后定义一个生成待处理图像列表的函

数generatejmageJistO,根据输入屮要增加图片的数量和并行进程的数目，尽可能均匀地

为每个进程生成了需要处理的任务列表。执行随机扰动的代码定义在augmentJmagesO中，

这个函数是每个进程内进行实际处理的函数，执行顺序是镜像一裁剪一旋转一HSV —

Gamma。需要注意的是镜像一裁剪，因为只是个演示例子，因此未必是一个合适的顺序。

最后定义一个mainO函数进行调用，代码如下：

import os import argparse import random import math

from multiprocessing import Process from multiprocessing import cpu_count import cv2

\# 导入image_augmentation.py为一个可调用模块 import image_augmentation as ia #利用Python的argparse模块读取输入输出和各种扰动参数 def parse_atgs():

parser = argparse.ArgumentParser(

description;'A Simple Image Data Augmentation Tool *, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('input_dir *,

help:'Directory containing images')

parser.add_argument(* output_dir',

help='Directory for augmented

images *)

parser.add_argument('num *,

help=,Number of images to be

augmented*,

type=int)

parser.add_argument(* ——num_procs1,

help='Number of processes for

paralleled augmentation *,

type=int, default=cpu_count())

parser.add_argument(*--p_mirror',

help=,Ratio to mirror an image',

type=float, default=O.5)

parser.add_argument(* ——p_crop',

help=1 Ratio to randomly crop

an image *,

type=float, default=l.0) parser.add_argument(丨——crop_size *,

help='The ratio of cropped image size to original image size, in area *,

type=float, default=0.8) parser.add_argument(1——crop_hw_vari1,

help='Variation of h/w ratio*, type=float, default=0.1)

parser.add一argument('--p_rotate',

help='Ratio

an image',

type=float,

parser.add_argument(* ——p_rotate_crop *,

help= * Ratio

empty part in a rotated image *,

type=float, parser.add_argument('--rotate_angle_vari',

to randomly rotate

default=l.0)

to crop out the

default=l.0)

help:1Variation range of rotate

angle *,

parser.add_argument(* ——p_hsv',

gamma of an image *,

parser.add_argument(1——hue_vari1

parser.add_argument(* ——sat_vari *

7

parser.add_argument(*--val_vari *

parser.add_argument('——p_gamma ’，

gamma of an image *,

type=float,

help=,Ratio

type=float,

default=10.0)

to randomly change

default=l.0)

help= * Variation of hue', type=int, default=10)

help= * Variation of saturation1, type=float, default=0.1)

help='Variation of value', type=float, default=0.1)

help= * Ratio

to randomly change

default=l.0)

type=float, parser.add_argument(* ——gamma_vari *,

help='Variation of gamma', type=float, default=2.0)

args = parser.parse_args()

args.input_dir = args.input_dir.rstrip(*/*) args.output_dir = args.output_dir.rstrip(*/*) return args

根据进程数和要增加的目标图片数，

生成每个进程要处理的文件列表和每个文件要增加的数目

V I I

def generate—image一list(args):

\#获取承有文#名和文件总数

filenames = os.listdir(args.input_dir) num_imgs = len(filenames)

\#译算平均处理的数目并向下取整

num_ave_aug = int(math.floor(args.num/num_imgs))

\#剩下的部分不足平均分配到每一个文件，所以做成一个随机幸运列表

\#对于幸运的文件就多增加一个，凑够指定的数目 rem = args.num - num_ave_aug*num_imgs lucky_seq = [True]*rem + [False]*(num_imgs-rem) random.shuffle(lucky_seq)

林根据平均分配和幸运表桌略

\#生成每个文件的全路径和对应要增加的数目并放到一个list里 img_list =    [

(os.sep.join([args.input_dir, filename]),    num_ave_aug十1

if lucky else num_ave_aug)

for filename, lucky in zip(filenames, lucky_seq)

] ,

\#文件可能大小不一，处理时间也不一样 #所以随机打乱，尽可能保证处理时间均匀 random.shuffle(img一list)

\#生成每个进程的文件列表

\#尽可能均匀地划分每个进程要处理的数目

length = float(num_imgs) / float(args.num_procs)

indices = [int(round(i * length)) for i in range

(args.num_procs +    1)]

return [img_list[indices[i]:indices[i +    1]] for i in range

(args.num_procs)]

\#每个进程_内调用图像处理函数进行扰动的函数

def augment—images(filelist, args):

\#遍岳所有列表内的文件

for filepath, n in filelist:

img = cv2.imread(filepath) filename = filepath.split(os.sep)[-1] dot_pos = filename.rfind(1.1)

\#获取文件名和后缀名

imgname = filename[:dot_pos]

ext = filename[dot一pos:]

print('Augmenting { }    ... 1.format(filename))

for i in range (n):

img_varied = img.copy()

\#扰动后文件名的前缀

varied_imgname =    '{}_{：0>3d}_*.format(imgname, i)

\#按照比例随机对图像进行镜像

if random.random()    < args.p_mirror:

\# 利用 numpy. fliplr (img_varied)也能实现 img_varied = cv2.flip(img一varied, 1) varied—imgname +=    *m'

\#按照比例随机对图像进行裁剪

if random.random()    < args.p_crop:

img_varied = ia.random一crop( img_variedf args.crop_size, args.crop_hw_vari)

varied—imgname +=    * c *

\#按照比例随机对图像进行旋转

if random.random()    < args.p_rotate:

img_varied = ia.random_rotate( img_varied,

args.rotate_angle_vari,

args.p_rotate_crop) varied_imgname +=    * r *

\#按照比例随机对图像进行HSV扰动 if random.random()    < args.p_hsv:

img_varied = ia.random_hsv_transform( img_varied, args.hue_vari, args.sat_vari, args.val_vari)

varied_imgname +=    * h *

\#按照比例随机对图像进行Gamma扰动 if random.random()    < args.p_gamma:

img_varied = ia.random_gamma_transform( img_varied, args.gamma_vari)

varied_imgname +=    ' g'

\#生成扰动后的文件名并保存在指定的路径

output_filepath = os.sep.j oin([

args.output_dir,

'{}{}*•format(varied_imgname, ext)]) cv2.imwrite(output_filepath, img_varied)

\#主函数

def main():

\#获取输入输出和变换选项 args = parse_args() params_str = str (args) [10:-1]

\#如果論出文件夹不存在，则建立文件夹

if not os.path.exists(args.output_dir):

os.mkdir(args.output_dir)

print(7 Starting image data augmentation for {} \n *

'with\n{}\n ’.format(args.input_dir, params_str))

\#生成每个进程要处理的列表

sublists = generate_image_list(args)

\#创建进程

processes = [Process(target=augment_images, args=(x, args, )) for x in sublists]

\#并行多进程处理

for p in processes:

p.start ()

for p in processes: p. join ()

print(*\nDone!*) if _name_ ==    *_main_* :

main ()

注意，程序中除了前面提的3种类型的变化，还增加了镜像变化，但是因为这种变换 太简单了。另外，默认进程数用的是cpu_Cmmt()函数，以获取CPU的核数。把该段代码 保存为run augmentation.py,然后在命令行输入：

» python run_augmentation.py -h

或者

» python run_augmentation.py ——help

就能看到脚本的使用方法、每个参数的含义及默认值。接下来执行一个图片增加任务:

» python run_augmentation.py    imagenet_samples more_samples 1000

——rotate_angle_vari=180 ——p_rotate_crop=0.5

参数的赋值也可以不用等号而是直接用空格接值，这样在参数是文件名的情况下很方 便，但本例中看不出：

\>> python run_augmentation.py    imagenet_samples more_samples 1000

--rotate_angle_vari 180    ——p_rotate_crop 0.5

其中imagenetsamples为一些从imagenet图片url中随机下载的一些图片， -rotate angle vari设为180，方便测试全方向的旋转，-p rotate crop设置为0.5，让旋转 裁剪对一半图片生效。扰动增加后的1000张图片在more_samples文件夹下，得到的部分 结果如图6-7所示。



图6-7扰动增加后的部分样本

6.4用OpenCV实现物体标注小工具

除了对图像的处理，OpenCV的图形用户界面(Graphical User Interface, GUI)和绘 图等相关功能也是很有用的功能，无论是可视化，图像调试还是本节要实现的标注任务， 都可以有所帮助。本节先介绍OpenCV窗口的最基本的使用和交互，然后基于这些基础和 之前的知识实现一个用于物体检测任务标注的小工具。

6.4.1窗口循环

OpenCV显示一幅图片的函数是cv2.imshow(),第一个参数是显示图片的窗口名称， 第二个参数是图片的array。如果直接执行该函数的话，什么都不会发生，因为该函数需配 合cv2.waitKeyO函数一起使用。cv2.waitKey()函数指定当前的窗口显示要持续的毫秒数， 比如cv2.waitKey(1000)就是显示一秒，然后窗口就关闭了。比较特殊的是cv2.waitKey(0)

函数，并不是显示0毫秒的意思，而是一直显示，直到键盘上的按键被按下，或者鼠标单 击了窗口的关闭按钮才关闭。cv2.waitKeyO函数的默认参数就是0,所以对于图像展示的场 景，cv2.waitKey()或者 cv2.waitKey(0)是最常用的。

import cv2

img = cv2.imread(* Aitutaki.png1) cv2.imshow(* Honeymoon Island*, img) cv2.waitKey()

执行代码得到如图6-8所示的窗口。



. 图6-8利用OpenCV进行最基本的图像显示 /

cv2.waitKey()函数的参数不为0的时候可以和循环结合产生动态画面，比如在6.2.4节 的延时小例子中，把延时摄影保存下来的所有图像放到一个叫做frames的文件夹下。下面 代码从frames的文件夹下读取所有图片并以24的帧率在窗口中显示成动画。

import os

from itertools import cycle import cv2

\#列出frames文件夹下的所有图片 filenames = os.listdir(1 frames *)

\#通过itertools.cycle生成一个无限循环的迭代器，每次迭代都输出下一张图像对象 img_iter = cycle([cv2.imread(os.sep.join(['frames', x])) for x in filenames])

key =    0

while key ! =    27:

cv2.imshow(* Animation *, next(img_iter)) key = cv2.waitKey(42)

在这个例子中采用了 Python的itertools模块中的cycle()函数，该函数可以把一个可遍 历结构编程一个无限循环的迭代器。另外从例子中还发现，cv2.waitKey()函数返回的就是 键盘上按下的按键。对于字母就是ASCII码，特殊按键如上下左右等，则对应特殊的值， 其实这就是键盘事件的最基本用法。

6.4.2鼠标和键盘事件

因为GUI总是交互的，所以鼠标和键盘事件基本使用必不可少，6.4.1节已经提到了 Cv2.waitKey()函数就是获取键盘消息的最基本方法。比如下面的循环代码就能够获取键盘 上按下的按键，并在终端输出：

while key ! =    27:

cv2.imshow(* Honeymoon Island *, img) key = cv2.waitKey()

\#如果获取的键值小于256则作为ASCII码输出对应字符，否则直接输出值

msg =    * { } is pressed* . format (chr (key) if key <    256 else

key)

print(msg)

通过这个程序能获取一些常用特殊按键的值，比如在笔者用的机器上，4个方向的按 键和删除键对应的值如下。

□上(T) : 65362；

□下(i) : 65364；

□左(一)：65361；

□右65363；

□删除(Delete) : 65535。

需要注意的是，在不同的操作系统里这些值可能是不一样的。鼠标事件比键盘事件稍 微复杂一点，需要定义一个回调函数，然后把回调函数和一个指定名称的窗口绑定，这样 只要鼠标位于画面区域内的事件就都能捕捉到。把下面这段代码插入到上段代码的while 之前，就能获取当前鼠标的位置和动作并输出。

\#定义鼠标事件回调函数

def on一mouse(event, x, y, flags, param):

\#鼠标左键按下，抬起，双击

if event == cv2.EVENT_LBUTTONDOWN:

print(* Left button down at ({},    {})’.format(x, y))

elif event == cv2.EVENT_LBUTTONUP:

print(* Left button up at ({},    {})’.format(x, y))

elif event == cv2.EVENT_LBUTTONDBLCLK:

print (' Left button double clicked at ⑴，    { }) * .

format(x, y))

\#鼠标右键按下，抬起，双击

elif event

cv2.EVENT RBUTTONDOWN:

print(* Right button down at ({},    { }) *.format(x, y))

elif event

cv2.EVENT RBUTTONUP:

{})，.format(x, y))

elif

print(* Right button up at ({}, event == cv2.EVENT RBUTTONDBLCLK:

print('Right button double clicked at ({},    {})

format(x, y))

\#鼠标中/滚轮键(如果有的话)按下，抬起，双击

elif event == cv2.EVENT_MBUTTONDOWN:

print('Middle button down at ({},    {})*.format(x, y))

elif event == cv2.EVENT_MBUTTONUP:

print('Middle button up at ({},    {}) '.format(x, y))

elif event == cv2.EVENT_MBUTTONDBLCLK:

print('Middle button double clicked at ({},    {})’.

format(x, y))

\#鼠标移动

elif event == cv2.EVENT_MOUSEMOVE:

print ('Moving at ({},    ⑴，• format (x, y))

\#为指定的窗口绑定自定义的回调函数

cv2.namedWindow(* Honeymoon 工sland')

cv2.setMouseCallback('Honeymoon Island1, on_mouse)

6.4.3代码：物体检测标注的小工具

基于6.4.1和6.4.2两小节的基本使用，就能和OpenCV的基本绘图功能实现一个超级 简单的物体框标注小工具了。基本思路是对要标注的图像建立一个窗口循环，然后每次循 环的时候对图像进行一次复制。鼠标在画面上画框的操作，以及已经画好的框的相关信息 在全局变量中保存，并且在每个循环中根据这些信息，在复制的图像上再画一遍，然后显 示这份复制的图像。

基于这种实现思路，使用上采用一个尽量简化的设计如下。

□输入是一个文件夹的路径，下面包含了所有要标注物体框的图片。如果图片中标 注了物体，则生成一个相同名称加额外后缀名的文件保存标注信息。

□标注的方式是按下鼠标左键选择物体框的左上角，松开鼠标左键选择物体框的右 下角，按下鼠标右键删除上一个标注好的物体框。所有待标注物体的类别和标注 框颜色由用户自定义，如果没有定义则默认只标注一种物体，定义该物体名称为 Object。

□方向键一和一键用来遍历图片，t和I键用来选择当前要标注的物体，Delete键删 除一张图片和对应的标注信息。

每张图片的标注信息，以及自定义标注物体和颜色的信息用一个元组表示，第一个元 素是物体名字，第二个元素是代表BGR颜色的tuple或者代表标注框坐标的元组。对于这 种并不复杂的数据结构，直接利用Python的reprO函数，把数据结构保存成机器可读的字 符串放到文件里，读取的时候用eval()函数就能直接获得数据。这样的方便之处在于不需 要单独写格式解析器。如果需要，可以在此基础上再编写一个转换工具，这样就能够转换 成常见的Pascal VOC的标注格式或其他的自定义格式。

在这些思路和设计下，定义标注信息文件格式的例子如下：

('Hili'f ((221,    163),    (741,    291)))

(’Horse', ((465,    430),    (613,    570)))

元组中第一项是物体名称，第二项是标注框左上角和右下角的坐标。这里之所以不把 标注信息的数据直接用pickle保存，是因为数据本身不会很复杂，直接保存还有更好的可 读性。自定义标注物体和对应标注框颜色的格式也类似，不过更简单些，因为括号可以不 写，具体如下：

第一项是物体名称，第二项是物体框的颜色。使用的时候把自己定义好的内容放到一 个文本里，然后保存成和待标注文件夹同名，后缀名为labels的文件。比如在一个samples 的文件夹下放上一些草原的照片，然后自定义一个和文件夹同名的samples.labels的文本文

件。把上段代码的内容放进去，就定义了小山头的框为黄色，骏马的框为青色，以及红色

的男青年。具体的标注小工具的代码如下：

import os import cv2

\# tkinter是Python内置的简单GUI库，实现一些比如打开文件夹、确认删除等操作十分方便 from tkFileDialog import askdirectory from tkMessageBox import askyesno #定义标注窗口的默认名称

WINDOW_NAME =    * Simple Bounding Box Labeling Tool *

\#定义面刷新的大概帧率(是否能达到取决于计算机性能)

get_bbox_name =    *{}.bbox *.format

\#是义物译框标注工具类

class SimpleBBoxLabeling:

def  init_(self, data_dir, fps=FPS, window_name=None):

| self. data dir = data dir self.fps = fps |               |      |             |      |
| ---------------------------------------- | ------------- | ---- | ----------- | ---- |
| self.window name                         | = window name | if   | window name | else |

WINDOW_NAME

\#pt0是正在画的左上角坐标，ptl是鼠标所在坐标

self ,_ptO = None

self.一ptl = None

\#表弭当前是否正在画框的状态标记

self._drawing = False

\#当俞标注物体的名称

self._cur_label = None

\#当i图像 1 寸应的所有已标注框

self._bboxes =    []

\#如＜有用户自定义的标注信息则读取，否则用默认的物体和颜色

label_path =    *{}.labels *.format(self._data_dir)

self.label一colors = DEFAULT_COLOR if not os.path.exists

(label_path) else self.load_labels(label_path)

\#获取已经标注的f件列表和还未标S的文件列表

|        | imagefiles                       | =[X      | for  | X                          | in os.listdir(self. data dir) |
| ------ | -------------------------------- | -------- | ---- | -------------------------- | ----------------------------- |
| if x   | [x.rfind('.1)    +    1:]        | .lower() | in   | SUPPOTED FORMATS]          |                               |
|        | labeled =                        | [x for   | X    | in                         | imagefiles if os.path.exists  |
| (get一 | bbox_name(x))]to be labeled = [x | for      | X    | in imagef iles if x not in |                               |

labeled]

\#每次打开一个文件夹，都自动从还未标注的第一张开始 self._filelist = labeled + to_be_labeled self.—index = len(labeled)

if self._index > len(self._filelist) -    1:

self._index = len(self._filelist) -    1

\#鼠标回调函数

def _mouse_ops(self, event, x, y, flags, param):

\#按下左键时，坐标为左上角，同时表明开始画框，改变drawing标记为True if event == cv2.EVENT_LBUTTONDOWN:

self.—drawing = True self._ptO =    (x, y)

\#松开左键，秦明当前框画完了，坐标记为右下角并保存，同时改变drawing

标记为False

elif event == cv2.EVENT LBUTTONUP:

self.—drawing = False self._ptl =    (x, y)

self._bboxes.append((self._cur_label, (self,_ptOz

self._ptl)))

\#实时更新右下角坐标方便画框

elif event == cv2.EVENT MOUSEMOVE:

self,_ptl =    (x, y)

\#按下鼠标右逼删除最近画好的框

elif event == cv2.EVENT_RBUTTONUP:

if self. bboxes:

self._bboxes.pop()

\#清除所有标注框和当前状态

def _clean_bbox(self):

self ._ptO = None self ._ptl = None self._drawing = False self.—bboxes =    []

\#画時注框和当前信息的函数

def _draw_bbox(self, img):

\#吞图像下方多出BAR_HEIGHT这么多像素的区域，用于显示文件名和当前标

注物体等信息

h, w = img.shape[:2]

canvas = cv2.copyMakeBorder(img, 0, BAR—HEIGHT, 0,    0,

cv2.BORDER一CONSTANT, value=COLOR_GRAY)

\#正在标注的物体信息，i卩果鼠标左键已经按下，则显示两个点坐标，否则显示 当前待标注物体的名称

label_msg =    *{} :    {},    {}'.format(self._cur_label, self

ptO, self._ptl) \

if self.—drawing \

else * Current label:    {}*.format(self._cur_label)

\#显示当前文件名，文件个数信息

msg =    *{}/{}:    {} I {}'.format(self._index +    1, len

(self._filelist), self._filelist[self,_index], label_msg)

cv2.putText(canvasf msg, (1,    h+12),

cv2.FONT_HERS HEY_SIMPLEX z 0.5,    (0,— 0,    0)7 1)

\#画出已经标好的框和对应名字

for label, (bptO, bptl) in self.—bboxes:

label—color = self.label_colors[label] if label

in self.label colors else COLOR GRAY

cv2.rectangle(canvas, bptO, bptl, label_color,

thickness=2)

cv2.putText(canvas, label, (bptO[0]+3, bptO[1]+15), cv2.FONT_HERSHEY_SIMPLEX,

0.5, label—color, 2)

\#画正在标注的框和对应名字

if self,_drawing:

label_color = self.label_colors[self._cur_label] if self._cur_label in self.label—colors else COLOR_GRAY

if self._ptl[0]    >= self._ptO[0] and self._ptl[1]

\>=self,_ptO[1]:

cv2.rectangle(canvas, self._ptO, self._ptl,

label_color, thickness=2)

cv2.putText(canvas, self,_cur_label, (self,_ptO[0] +    3, self._pt0[1]    +    15),

cv2.FONT_HERSHEY_SIMPLEX z 0.5, label_color, 2)

return canvas

\#利用repr ()函数导出标注框数据到文件 @staticmethod

def export_bbox(filepath, bboxes): if bboxes:

with open (filepath, * w *) as f: for bbox in bboxes:

line = repr(bbox) +    '\n *

f.write(line)

elif os.path.exists(filepath): os.remove(filepath)

\#利用eval()函数读取标注框字符串到数据 @staticmethod

def load_bbox(filepath):    ,

bboxes =    []

with open (filepath, * r *) as f:

line = f.readline().rstrip() while line:

bboxes.append(eval(line)) line = f.readline() .rstrip ()

return bboxes

\#利用eval()函数读取物体及对应颜色信息到数据 Qstaticmethod

def load_labels(filepath): label_colors =    {}

with open (filepath, * r *) as f:

line = f.readline().rstrip() while line:

label, color = eval(line) label_colors[label] = color line = f.readline() .rstrip ()

return label—colors

\#读取图像文件和对应标运框信息(如果有的话)

@staticmethod

def load_sample(filepath):

img = cv2.imread(filepath)

bbox_filepath = get_bbox_name(filepath)

bboxes =    []

if os.path.exists(bbox_filepath):

bboxes = SimpleBBoxLabeling.load_bbox(bbox_filepath)

return img, bboxes

\#导出当前标注框信息并清空

def _export_n_clean_bbox(self):

bbox_filepath = os.sep.join([self._data_dir, get_bbox_ name(self._filelist[self._index])])

self.export_bbox(bbox_filepath, self._bboxes) self._clean_bbox()

\#删除当前样i和对应丑标注框信息

def _delete_current_sample(self):

filename = self._f ilelist[self,_index] filepath = os.sep.join([self._data_dir, filename]) if os.path.exists(filepath):

os.remove(filepath) filepath = get_bbox_name(filepath) if os.path.exists(filepath):

os.remove(filepath) self._filelist.pop(self._index) print(*{} is deleted!1.format(filename))

\#开始OpenCV窗口循环的方法，定义了程序的主逻辑

def start(self):

\#之前标注的文件名，用于程序判断是否需要执行一次图像读取

last_filename =    "

\#标注物体在列表中的下标

label_index =    0

\#所有标注物体名称的列表

labels = self.label_colors.keys()

\#待标注物体的种类数

n_labels = len(labels)

定义窗口和鼠标回调

cv2.namedWindow(self.window_name)

cv2.setMouseCallback(self.window_name, self,_mouse_ops) key = KEY_EMPTY #定义每次环的持续时间 delay = int (1000    / FPS)

\#只要没有按下Esc键，就持续循环 while key ! = KEY_ESC:

\#上下方向键角于选择当前标注物体 if key == KEY_UP:

\#删除当前图片和对应忌注信息

elif key == KEY_DELETE:

if askyesno(丨Delete Sample *, 'Are you sure? *): self._delete_current_sample() key : KEY_EMPTY

continue

\#如果键盘操作执行了换图片，则重新读取，更新图片

filename = self.—filelist[self.—index]

if filename ! = last_filename:

filepath = os.sep.join([self._data_dir,

filename])

img, self,_bboxes = self.load_sainple(filepath)

\#更新当前标注物体羞称

self,_cur_label = labels[label_index]

\#把禄注和关信息画在图片上并显示指i的时间

canvas = self._draw_bbox(img)

cv2.imshow(self•window_name, canvas)

key = cv2.waitKey(delay)

\#当前文件名就是下次循环的老文件名

last filename = filename

print(* Finished!') cv2.destroyAllWindows()

\#如果退出程序，需要对当前文件进行保存

self.export_bbox(os.sep.join([self._data_dir,

g e t_bb o x_n ame(filename)]), self._bboxes) print('Labels updated!')

if _name_ ==    1_main_* :

dir_with_images = askdirectory(title='Where are y the images? *) labeling_task = SimpleBBoxLabeling(dir_with_images) labeling_task.start()

需要注意的是，程序中几个比较通用且独立的方法前加上了一句@staticmethod,表明 是个静态方法。执行程序并选择samples文件夹，就可以在文件夹下生成和图片同名、后 缀为bbox的标注信息文件了。标注时的画面如图6-9所示。



图6-9标注小工具使用界面
