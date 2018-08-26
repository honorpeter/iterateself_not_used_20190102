---
title: TL JDA例子1
toc: true
date: 2018-06-11 08:14:54
---




## 需要补充的

- 没有写，之前的册子上是Matlab代码的，




# 上手实践


在本部分，我们以迁移学习中最为流行的图像分类为实验对象，在流行的Office+Caltech10数据集上完成。

在众多的非深度迁移学习方法中，我们选择发表于ICCV-13的 JDA  方法进行实践。实验平台为普通机器上的Matlab软件。

1. 数据获取

由于我们要测试非深度方法，因此，选择 SURF 特征文件作为算法的输入。SURF 特征文件可以[这里](https://pan.baidu.com/s/1bp4g7Av)下载。

下载到的文件主要包含4个.mat文件：Caltech.mat, amazon.mat, webcam.mat, dslr.mat。它们恰巧对应4个不同的领域。彼此之间两两一组，就是一个迁移学习任务。

每个数据文件包含两个部分：fts 为800维的特征，labels 为对应的标注。在测试中，我们选择由Caltech.mat作为源域，由amazon.mat作为目标域。

Office+Caltech10  数据集的介绍可以在本手册的第~\ref{sec-dataset}部分找到。

我们对数据进行加载并做简单的归一化，将最后的数据存入 \(X_s,Y_s,X_t,Y_t\) 这四个变量中。这四个变量分别对应源域的特征和标注、以及目标域的特征和标注。



## 相关资料

- [迁移学习简明手册](https://github.com/jindongwang/transferlearning-tutorial) 
- [王晋东](https://zhuanlan.zhihu.com/p/35352154)
- [迁移学习代码实现 总结 王晋东](https://github.com/jindongwang/transferlearning/tree/master/code)
