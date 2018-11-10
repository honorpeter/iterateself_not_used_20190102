---
title: PIL 常用基础知识
toc: true
date: 2018-11-10
---
# PIL中设计的几个基本概念

1. 通道（bands）：即使图像的波段数，RGB图像，灰度图像

- 以RGB图像为例：

```text
from PIL import Image
im = Image.open('*.jpg')      # 打开一张RGB图像
im_bands = im.g
etbands()  # 获取RGB三个波段
len(im_bands)
print im_bands[0,1,2]          # 输出RGB三个值
```

2.模式（mode）：定义了图像的类型和像素的位宽。共计9种模式：

```text
im.mode
```

- 1：1位像素，表示黑和白，但是存储的时候每个像素存储为8bit。
- L：8位像素，表示黑和白。
- P：8位像素，使用调色板映射到其他模式。
- RGB：3x8位像素，为真彩色。
- RGBA：4x8位像素，有透明通道的真彩色。
- CMYK：4x8位像素，颜色分离。
- YCbCr：3x8位像素，彩色视频格式。
- I：32位整型像素。
- F：32位浮点型像素。

3.尺寸（size）：获取图像水平和垂直方向上的像素数

```text
im.size()
```

4.坐标系统（coordinate system）：

PIL使用笛卡尔像素坐标系统，坐标(0，0)位于左上角。

注意：坐标值表示像素的角；位于坐标（0，0）处的像素的中心实际上位于（0.5，0.5）。

5.调色板（palette）：

调色板模式（"P"）适用一个颜色调色板为每一个像素定义具体的颜色值。

6.信息（info）

```text
im.info() # 返回值为字典对象
```

7.滤波器（filters）：将多个输入像素映射为一个输出像素的几何操作

PIL提供了4种不同的采样滤波器：

- NEAREST：最近滤波。从输入图像中选取最近的像素作为输出像素。
- BILINEAR：双线性内插滤波。在输入图像的2*2矩阵上进行线性插值。
- BICUBIC：双立方滤波。在输入图像的4*4矩阵上进行立方插值。
- ANTIALIAS：平滑滤波。对所有可以影响输出像素的输入像素进行高质量的重采样滤波，以计算输出像素值。


im.resize()和im.thumbnail()用到了滤波器
方法一：resize(size,filter = None)

```text
from PIL import Image
im = Image.open('*.jpg')
im.size
im_resize = im.resize((256,256)) #default 情况下是NEAREST插值方法
im_resize0 = im.resize((256,256), Image.BILINEAR)
im_resize0.size
im_resize1 = im.resize((256,256), Image.BICUBIC)
im_resize2 = im.resize((256,256), Image.ANTIALIAS)
```

方法二：im.thumbnail(size,filter = None)



# 相关资料

- [Python—PIL基本概念介绍](https://zhuanlan.zhihu.com/p/27504020)
