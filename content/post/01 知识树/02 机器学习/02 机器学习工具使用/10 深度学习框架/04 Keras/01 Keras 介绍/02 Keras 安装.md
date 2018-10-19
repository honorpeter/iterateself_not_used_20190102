---
title: 02 Keras 安装
toc: true
date: 2018-10-20
---
# 需要补充的

- 安装的过程还是需要补充的。


# Keras 安装

Keras 使用了下面的依赖包，三种后端必须至少选择一种，我们建议选择 tensorflow。

- numpy，scipy
- pyyaml
- HDF5, h5py（可选，仅在模型的save/load函数中使用）
- 如果使用 CNN 的推荐安装 cuDNN

<span style="color:red;">pyyaml 是干什么的？</span>


“后端” 翻译自backend，指的是 Keras 依赖于完成底层的张量运算的软件包。


## 在Theano、CNTK、TensorFlow间切换

Keras 默认使用 TensorFlow 作为后端来进行张量操作，如需切换到 Theano，请查看[这里](https://keras-cn.readthedocs.io/en/latest/backend)

<span style="color:red;">嗯，虽然不一定使用到，但是还是想知道怎么切换的。</span>


# 相关资料

- [Keras中文文档](https://keras-cn.readthedocs.io/en/latest/)
