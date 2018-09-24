---
title: 06 SSD
toc: true
date: 2018-09-22
---
# SSD

针对YOLO类算法的定位精度问题，2016年12月北卡大学教堂山分校的 Wei Liu 等提出 SSD 算法，将 YOLO 的回归思想和 Faster R-CNN 的 anchor box 机制结合。通过在不同卷积层的特征图上预测物体区域，输出离散化的多尺度、多比例的 default boxes 坐标，同时利用小卷积核预测一系列候选框的边框坐标补偿和每个类别的置信度。在整幅图像上各个位置用多尺度区域的局部特征图边框回归，保持YOLO算法快速特性的同时，也保证了边框定位效果和Faster R-CNN类似。但因其利用多层次特征分类，导致其对于小目标检测困难，最后一个卷积层的感受野范围很大，使得小目标特征不明显。






## 需要消化的


- 相关资料：[论文阅读：SSD: Single Shot MultiBox Detector](https://blog.csdn.net/u010167269/article/details/52563573)

- 实现：[ssd_keras github](https://github.com/pierluigiferrari/ssd_keras)

- SSD: Single Shot MultiBox Detector  https://arxiv.org/pdf/1512.02325v5.pdf
