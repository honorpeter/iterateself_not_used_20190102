---
title: 02 MXNet 的安装
toc: true
date: 2018-09-01
---

## 安装 MXNet


<span style="color:red;">**注意**：在安装之前，先看下 “00 基本环境” 文件夹中的系统基础要装的东西是否已经安装好了。</span>

MXNet 的 github 页面是 https://github.com/dmlc/mxnet 。

在这里可以找到源代码的 git 地址，然后在要保存的控制台地址中输入下面命令:

```
git clone --recursive https://github.com/dmlc/mxnet
```

<span style="color:red;">为什么要写 recursive ？</span>

之后就会在执行命令的文件夹下得到一个 mxnet 的文件夹。第一步是配置安装的基础选项，打开 mxnet/make 文件夹下的 config.mk 文件，主要需要配置的是以下3个选项。

- USE_CUDA = 0；
- USE_CUDNN = 0；
- USEBLAS = atlas。

上面列出的都是默认选项，对于训练网络的需求，需要至少把 USE_CUDA 改成 1，如果需要 cuDNN 和 mkl 的话则需要把 USE_CUDNN 改成 1，USE_BLAS 改为 mkl。

配置好后就可以开始安装了。在Ubuntu下有个非常方便的方式，就是进入 mxnet/setup-utils 文件夹下，直接执行对应脚本：

```
cd mxnet/setup-utils
sh install-mxnet-ubuntu-python.sh
```

等待执行结束就大功告成了。当然如果不是 Ubuntu，那么一般的方式是回到 mxnet 目录下，执行：

```
cd mxnet
make - j
```

自动利用所有可用的 CPU 核对代码进行编译，如果在 -j 后面直接加上数字可以指定用的核数。然后配置 Python 接口：

```
cd python
sudo python setup.py install
```

<span style="color:red;">配置 Python 接口是什么意思？</span>

 万事俱备，接下来可以开始使用这个强大的框架了。





## 相关资料

- 《深度学习与计算机视觉》
