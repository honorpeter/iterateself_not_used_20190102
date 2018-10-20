---
title: 03 Keras安装和配置指南 Linux
toc: true
date: 2018-10-20
---

# Keras 安装和配置

在 基本环境已经安装完之后。

一般通过conda 进行安装：

```
conda install keras
```

基本上就可以使用了。

可能 tensorflow 的版本会有问题，如果是 1.2 或者比较低的版本可以安装成比较高的版本：

```
conda install tensorflow=1.8
conda install tensorflow-gpu=1.8
```


测试，可以：


```shell
git clone https://github.com/fchollet/keras.git
cd keras/examples/
python mnist_mlp.py
```


但是这个例子的数据集可能要从 amazonaws 上进行下载，应该是下载不了的，翻墙好像也不行。

但是这些例子都是非常值得阅读的。






# 相关资料

- [Keras中文文档](https://keras-cn.readthedocs.io/en/latest/)
