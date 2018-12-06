---
title: 06 MR-CNN
toc: true
date: 2018-09-22
---
# MR-CNN


2015年巴黎科技大学提出 MR-CNN 算法，结合样本区域本身的特征，利用样本区域周围采样的特征和图像分割的特征来提高识别率，可将检测问题分解为分类和定位问题。

![mark](http://images.iterate.site/blog/image/180922/0EfgDdLe1E.png?imageslim)



分类问题由Multi-Region CNN Model和Semantic Segmentation-Aware CNN Model组成。前者的候选框由Selective Search得到，对于每一个样本区域，取10个区域分别提取特征后拼接，这样可以强制网络捕捉物体的不同方面，同时可以增强网络对于定位不准确的敏感性，其中adaptive max pooling即ROI max pooling；后者使用FCN进行目标分割，将最后一层的feature map和前者产生的feature map拼接，作为最后的feature map。

为了精确定位，采用三种样本边框修正方法，分别为Bbox regression、Iterative localization以及Bounding box voting。Bbox regression：在Multi-Region CNN Model中整幅图经过网路的最后一层卷积层后，接一个Bbox regression layer，与RPN不同，此处的regression layer是两层FC以及一层prediction layer，为了防止Selective Search得到的框过于贴近物体而导致无法很好的框定物体，将候选框扩大为原来的1.3倍再做。Iterative localization：初始的框是Selective Search得到的框，然后用已有的分类模型对框做出估值，低于给定阈值的框被筛掉，剩下的框用Bbox regression的方法调整大小，并迭代筛选。Bounding box voting：首先对经过Iterative localization处理后的框应用NMS, IOU = 0.3，得到检测结果，然后对于每一个框，用每一个和其同一类的而且IOU >0.5的框加权坐标，得到最后的目标样本框。
