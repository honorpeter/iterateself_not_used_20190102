---
title: 13 Mask R-CNN
toc: true
date: 2018-09-22
---
# Mask R-CNN

为了解决 R-CNN 算法为代表的 two stage 的方法问题，2017 年 Facebook 的何恺明等提出了 Mask R-CNN 算法，取得了很好的识别效果。Mask R-CNN 算法将 ROI_Pooling 层替换成了 ROI_Align，并且在边框识别的基础上添加分支 FCN 层（mask层），用于语义 Mask 识别，通过 RPN 网络生成目标候选框，再对每个目标候选框分类判断和边框回归，同时利用全卷积网络对每个目标候选框预测分割掩膜。

加入的掩膜预测结构解决了特征图像和原始图像上的ROI不对准问题，避免对ROI边界做任何量化，而用双线性插值到对准特征，再用池化操作融合。掩膜编码了输入图像的空间布局，用全卷积网络预测每个目标候选框的掩膜能完整的保留空间结构信息，实现目标像素级分割定位。



## 需要消化的

- [Mask-RCNN技术解析](https://blog.csdn.net/linolzhang/article/details/71774168)
- 实现：[Mask_RCNN github](https://github.com/matterport/Mask_RCNN) 大概看了这个 README，震惊了，效果也太厉害了。

- [Mask-RCNN技术解析]
