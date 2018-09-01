---
title: 02 Caffe 的安装
toc: true
date: 2018-09-01
---



# 需要补充的

- 下面这些也要融入总结进来
- Ubuntu 14.04+ ：https://www.zybuluo.com/hanxiaoyang/note/364737
- CentOS 7.0+ ：https://www.zybuluo.com/hanxiaoyang/note/364680
- Mac ：https://www.zybuluo.com/hanxiaoyang/note/370344
- windows :https://gaussic.github.io/2016/08/02/caffe-for-windows/


# Caffe 的安装

<span style="color:red;">**注意**：在安装之前，先看下 “00 基本环境” 文件夹中的系统基础要装的东西是否已经安装好了。</span>


Caffe是个依赖非常多的框架，除了在7.1.1节中我们已经安装好的基础依赖，还需要以下的依赖包。

```
sudo apt install libprotobuf-dev libleveldb-dev libsnappy-dev libboost-all-dev libhdf5-serial-dev protobuf-compiler gfortran libjpeg62 libfreeimage-dev libgoogle-glog-dev libbz2-dev libxml2-dev libxslt-dev libffi-dev libssl-dev libgflags-dev liblmdb-dev python-yaml
```

<span style="color:red;">为什么 Caffe 依赖了这么多东西？他是怎么使用这些的？</span>

然后可以开始安装Caffe 了，先到要安装Caffe的文件夹下：

```
git clone https://github.com/BVLC/caffe.git
```

然后到caffe文件夹下，找到 Makefile.config.example 文件复制一份：

```
cd caffe
cp Makefile.config.example Makefile.config
```

和 MXNet 类似，Makefile.config 是编译的配置文件，在这个文件里可以配置一些编译选项，一般来说主要配置 CUDA、cuDNN 和 bias 库。比如笔者的机器上，主要是下面两个选项：

- USE_CUDNN:=1
- BLAS:=mkl

默认情况下 CPU_ONLY:=1 是被注释掉的，所以不用管。除非是在没有 NVIDIA 的 GPU 机器上安装 Caffe，那么把注释取消即可。

还有一个选项是 WITH_PYTHON_LAYER:=1，意思是支持用 Python 定义神经网络中的层，和 MXNet 中定义层的方式有些相像。如果要使用一些 Python 的层或是一些特定功能的Caffe版本，比如 Ross Girshick 的 py-faster-rcnn ，那么就需要把这一项前的注释取消。<span style="color:red;">什么叫特定功能的 Caffe 版本？</span>

配置好 Makefile.config 后，就可以开始编译了，依次执行下面的命令：

```
make pycaffe - j
make all -j
make test - j
```

<span style="color:red;">这个 -j 是什么意思？</span>

因为 Caffe 的依赖过多，在安装过程中有可能找不到一些动态库，这个时候需要把相对的路径加入到 LD_LIBRARY_PATH 下即可，如果是头文件则可以把对应路径加入到 CPLUS_INCLUDE_PATH中。比如找不到 HDF5 的库，可在控制台下执行：<span style="color:red;">什么是 HDF5 的库？</span>

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/hdf5/serial
```

为了在 Python 中直接调用 Caffe，还需要把 Caffe 的 Python 路径加入到 PYTHONPATH。

```
export PYTHONPATH=$PYTHONPATH=:/path/to/caffe/python
```

<span style="color:red;">这个 export 是什么意思？</span>

有的版本的 Ubuntu 下如果是使用 apt 安装的 cuda，还需要添加下面两个路径：

- /usr/lib/nvidia-cuda-tookit
- /usr/lib/x86-linux-gnu




## 相关资料

- 《深度学习与计算机视觉》
- 七月在线 深度学习
