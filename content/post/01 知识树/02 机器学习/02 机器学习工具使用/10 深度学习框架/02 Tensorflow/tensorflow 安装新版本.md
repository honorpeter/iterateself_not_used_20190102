---
title: tensorflow 安装新版本
toc: true
date: 2018-10-04
---
# 需要补充的

# 用 anaconda 安装最新的 TensorFlow 版本

**存在问题：**

一般从anaconda官网下载的anaconda，查看tensorflow依然还是1.2的版本，现在用conda更新TensorFlow

**解决方法：**

1，打开anaconda-prompt

2，查看tensorflow各个版本：（查看会发现有一大堆TensorFlow源，但是不能随便选，选择可以用查找命令定位）

```
anaconda search -t conda tensorflow
```

4，找到自己安装环境对应的最新TensorFlow后（可以在终端搜索anaconda，定位到那一行），然后查看安装命令

```
anaconda show <USER/PACKAGE>
```

安装anaconda/tensorflow具体操作命令：

```
anaconda show anaconda/tensorflow
```

5，第4步会提供一个下载地址，使用下面命令就可安装新版本tensorflow

```
conda install --channel https://conda.anaconda.org/anaconda tensorflow
```


# 相关资料

- [已解决：用anaconda安装最新的TensorFlow版本](https://blog.csdn.net/qq_35203425/article/details/79965389)
