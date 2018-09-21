---
title: 03 SPP-Net
toc: true
date: 2018-09-22
---
# SPP-Net

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180922/3kHB0m7kdB.png?imageslim)


针对 R-CNN 中卷积神经网络重复运算问题，2015年微软研究院的何恺明等提出一种 SPP-Net 算法，通过在卷积层和全连接层之间加入空间金字塔池化结构（Spatial Pyramid Pooling）代替R-CNN算法在输入卷积神经网络前对各个候选区域进行剪裁、缩放操作使其图像子块尺寸一致的做法。


利用空间金字塔池化结构有效避免了 R-CNN 算法对图像区域剪裁、缩放操作导致的图像物体剪裁不全以及形状扭曲等问题，更重要的是解决了卷积神经网络对图像重复特征提取的问题，大大提高了产生候选框的速度，且节省了计算成本。

但是和 R-CNN 算法一样，训练数据的图像尺寸大小不一致，导致候选框的 ROI 感受野大，不能利用 BP 高效更新权重。<span style="color:red;">没看懂。</span>
