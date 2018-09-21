---
title: 02 R-CNN
toc: true
date: 2018-09-22
---
# R-CNN

论文地址：

http://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Girshick_Rich_Feature_Hierarchies_2014_CVPR_paper.pdf



2014年加州大学伯克利分校的Ross B. Girshick 提出 R-CNN 算法，其在效果上超越同期的 Yann Lecun 提出的端到端方法 OverFeat 算法，其算法结构也成为后续 two stage 的经典结构。

R-CNN 算法利用选择性搜索（Selective Search）算法评测相邻图像子块的特征相似度，通过对合并后的相似图像区域打分，选择出感兴趣区域的候选框作为样本输入到卷积神经网络结构内部，由网络学习候选框和标定框组成的正负样本特征，形成对应的特征向量，再由支持向量机设计分类器对特征向量分类，最后对候选框以及标定框完成边框回归操作达到目标检测的定位目的。


虽然R-CNN算法相较于传统目标检测算法取得了 50% 的性能提升，但其也有缺陷存在：训练网络的正负样本候选区域由传统算法生成，使得算法速度受到限制；卷积神经网络需要分别对每一个生成的候选区域进行一次特征提取，实际存在大量的重复运算，制约了算法性能。
