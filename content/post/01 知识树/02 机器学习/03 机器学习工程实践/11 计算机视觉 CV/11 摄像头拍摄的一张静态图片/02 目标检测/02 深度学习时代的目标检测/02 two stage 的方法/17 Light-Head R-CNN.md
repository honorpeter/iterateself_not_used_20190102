---
title: 17 Light-Head R-CNN
toc: true
date: 2018-09-22
---
# Light-Head R-CNN

2017年12月Face++提出了一种为了使 two stage 的检测算法 Light-Head R-CNN，主要探讨了 R-CNN 如何在物体检测中平衡精确度和速度。

Light-Head R-CNN 提出了一种更好的 two-stage detector 设计结构，使用一个大内核可分卷积和少量通道生成稀疏的特征图。该设计的计算量使随后的ROI子网络计算量大幅降低，检测系统所需内存减少。将一个廉价的全连接层附加到池化层上，充分利用分类和回归的特征表示。因其轻量级头部结构，该检测器能够实现速度和准确率之间的最优权衡，不管使用的是大主干网络还是小主干网络。

基于 ResNet101 网络达到了新的 state-of-the-art 的结果40.6，超过了 Mask R-CNN 和 RetinaNet。同时如果是用一个更小的网络，比如类似 Xception的小模型，达到了 100+FPS，30.7mmap，效率上超过了 SSD 和 YOLO。
