---
title: 07 HyperNet
toc: true
date: 2018-09-22
---
# HyperNet


2016年清华大学提出HyperNet算法，其利用网络多个层级提取的特征，且从较前层获取的精细特征可以减少对于小物体检测的缺陷。将提取到的不同层级feature map通过最大池化降维或逆卷积扩增操作使得所有feature map尺寸一致，并利用LRN正则化堆叠，形成Hyper
Feature maps，其具有多层次抽象、合适分辨率以及计算时效性的优点。接着通过region proposal generation module结构进行预测和定位，仅保留置信度最高的N个样本框进行判断。

![mark](http://images.iterate.site/blog/image/180922/Kecbh2JeCI.png?imageslim)
