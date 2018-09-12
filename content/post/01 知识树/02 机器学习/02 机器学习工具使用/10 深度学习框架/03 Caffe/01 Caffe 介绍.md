---
title: 01 Caffe 介绍
toc: true
date: 2018-09-01
---


来源于Berkeley 的开源框架，高效 ， 一般的训练无需手写大量代码，有python 和mathlab 的接口，



### Caffe

Caffe 全称为 Convolutional Architecture for Fast Feature Embedding，由伯克利加州大 学(University of California, Berkeley)的博士生贾扬清开发，后来一直由伯克利视觉及学习中心(Berkeley Vision and Learning Center，BVLC)进行维护。Caffe 基于 C++和英伟达 (NVIDIA)公司的 GPU (Graphic Processing Unit)通用计算架构 CUDA (Compute Unified Device Architecture)开发，特点是高效、可配置化的输入、GPU和CPU的无缝切换。当 然还有非常重要的一点，Caffe拥有庞大的社区，无论是科研领域还是业界都有大量的用户。 每当一些最前沿的深度学习方法发表后，没多久就会有官方的预训练模型或是第三方基于Caffe的实现，所以Caffe是一个对初学者和有经验的人都非常适合的工具。

2013年，贾扬清得到了一块NVIDIA免费提供的K20加速卡。在这个契机下贾扬清 一边做毕业论文一边开始写一个用于深度学习的框架。经过了近半年的独立开发，Caffe 初具形态并且在伯克利的研究组内获得了良好的试用反响。后来在物体检测领域成为经典的 R-CNN (Regions with Convolutional Neural Network features)方法就是在这段时间内基于Caffe实现的。

2013年底，贾扬清将 Caffe 开源，成为了当时业内第一个较为完整的深度学习开源框 架，于是立刻获得了学术界和业界的好评及支持。后来在BLVC和NVIDIA为主的合力推广下，Caffe很快成为了深度学习领域，尤其是基于深度学习的计算机视觉领域最流行的框 架。本书使用Caffe作为实例的主要实现框架之一，后面会有更多关于Caffe的内容。
