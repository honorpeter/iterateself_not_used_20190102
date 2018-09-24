---
title: 05 Faster R-CNN
toc: true
date: 2018-09-22
---

# Faster R-CNN

论文地址：

https://arxiv.org/pdf/1506.01497.pdf


为了解决Fast R-CNN算法缺陷，使得算法实现 two stage 的全网络结构，2015年微软研究院的任少庆、何恺明以及Ross B Girshick等人又提出了 Faster R-CNN 算法。


设计辅助生成样本的 RPN（Region Proposal Networks）网络，将算法结构分为两个部分，先由 RPN 网络判断候选框是否为目标，再经分类定位的多任务损失判断目标类型，整个网络流程都能共享卷积神经网络提取的的特征信息，节约计算成本，且解决 Fast R-CNN 算法生成正负样本候选框速度慢的问题，同时避免候选框提取过多导致算法准确率下降。

但是由于 RPN 网络可在固定尺寸的卷积特征图中生成多尺寸的候选框，导致出现可变目标尺寸和固定感受野不一致的现象。<span style="color:red;">没明白。</span>




看到微信群里有人讨论 RPN，有人问大的图像能输入到 RPN 里面吗，然后有人说 YOLO 和 R-CNN 系列方法不一样，只要求图像的一个边是 32 倍，对图像的大小要求没有那么高。<span style="color:red;">对，我也想问，大的图像到底要怎么处理？直接缩到 227*227 不好吧？如果用大尺寸来输入，那么又没有足够的训练资源，别的网络拿过来又不能用了，怎么办？</span>


对于这块我理解的也不够，因此还是要好好总结下的。







## 需要消化的


- [faster-rcnn 之 RPN网络的结构解析](https://blog.csdn.net/sloanqin/article/details/51545125)
- [faster-rcnn中，对RPN的理解](https://blog.csdn.net/ying86615791/article/details/72788414)

- Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks http://papers.nips.cc/paper/5638-faster-r-cnn-towards-real-time-object-detection-with-region-proposal-networks.pdf

- []()
