---
title: 09  R-FCN
toc: true
date: 2018-09-22
---

# R-FCN

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180922/dmK3lb8A3h.png?imageslim)



随着全卷积网络的出现，2016年微软研究院的 Jifeng Dai 等提出 R-FCN 算法。相较于 Faster R-CNN 算法只能计算 ROI pooling 层之前的卷积网络特征参数，R-FCN 算法提出一种位置敏感分布的卷积网络代替 ROI pooling 层之后的全连接网络，解决了 Faster R-CNN 由于 ROI
Pooling 层后面的结构需要对每一个样本区域跑一次而耗时比较大的问题，使得特征共享在整个网络内得以实现，解决物体分类要求有平移不变性和物体检测要求有平移变化的矛盾，但是没有考虑到 region proposal 的全局信息和语义信息。
