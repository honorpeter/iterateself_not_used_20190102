---
title: Ubuntu 上的基本环境
toc: true
date: 2018-09-01
---

# 需要补充的

- 这个要融入进去
- 这个只是最基础的一些东西，要不断的完善和细化
- 大部分深度学习的开发都是用 Ubuntu 的吗？别的 Linux 系统的？比如 Debian 或者 CentOS？
- 这里面的东西还要拆分，比如 graphviz 和 CUDA 什么的要分开。还需要补充。


# 在 Ubuntu 上做深度学习开发需要安装的


这个是作为最基本存在的，基本上所有的框架，在安装之前都需要把这个最基础需要安装的东西安装上。

这里只包括了非常基础的，就是无论哪个框架都需要安装的东西，但是各个框架自己还有自己的不同的依赖，在安装完这个基础的东西后，自己的依赖也要安装

### 基础工具、NVIDIA驱动和CUDA安装

首先是安装大部分开发工具需要的基础依赖工具包，比如 git、用于矩阵计算的 atlas, 和图可视化的 graphviz 等，以Ubuntu 16.04 LTS为例，执行下面命令安装包：<span style="color:red;">这个 atlas 是什么？</span>

```
sudo apt update
sudo apt install build-essential git libatlas-base-dev
sudo pip install graphviz
```

<span style="color:red;">现在的 linux 用来做机器学习的机器普遍都是装的 ubuntu 吗？</span>

第 5 章和第 6 章讲过的 pip、NumPy 和 OpenCV 也是需要的，安装方法已经讲过在此就不再介绍了。

对于当前的所有深度学习框架，如果要训练神经网络一定离不开（NVIDIA的）GPU, 以及配套的 GPU 编程工具包 CUDA。所以接下来是安装 NVIDIA 的驱动和 CUDA 工具包。安装 NVIDIA 驱动前需要先卸载系统自己的驱动：

```
sudo apt --purge remove xserver-xorg-video-nouveau
```

然后添加NVIDIA驱动的源：

```
sudo add-apt-repository ppa:graphics-drivers/ppa
```

然后就可以安装驱动和CUDA工具包了。

```
sudo apt install nvidia-361 nvidia-settings nvidia-prime
sudo apt install nvidia-cuda-toolkit
```

安装完成后，在控制台输入：

```
nvidia-smi
```

如果安装成功则会显示显卡的信息，比如笔者的 GTX980M 笔记本显示信息如图7-1 所示。

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180830/bKk4m1ab7H.png?imageslim)

如果是其他的Linux系统，步骤也很相似，首先卸载自带的显卡驱动，然后用系统自带软件包或者到 NVIDIA 官网下载驱动及 CUDA 按照说明进行安装，下载地址为 http://www.nvidia.com/Download/index.aspx 或  https://developer.nvidia.com/cuda-downloads。<span style="color:red;">还没有亲自安装过，一定要亲自实践并总结。</span>

cuDNN 是 CUDA 中专门为加速深度神经网络设计的库，是个可选的安装选项。下载 ±也址为 https://developer.nvidia.com/cudnn 。

找到对应的版本并填写需要的信息之后就可以下载了。下载之后是一个压缩包，这里 以 cuDNN 5.1 为例，执行以下命令将 cuDNN 中的库解压并添加到 CUDA 对应文件夹下。

```
tar -xvzf cudnn-8.0-linux-x64-v5.1-ga.tgz
sudo cp -P cuda/include/cudnn.h /usr/local/cuda/include
sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64
```

任何深度学习框架中，基于 CPU 的矩阵计算包也是基础的库之一，除了本节一开始安 装的 atlas, Intel 的 MKL (Math Kernel Library) 因为其优异的性能，往往是一个更佳的选项，MKL 的下载地址为 https://software.intel.com/en-us/intel-mkl/ 。<span style="color:red;">嗯。</span>

MKL 对于个人是免费的，需要一定的注册步骤获取一个许可证。其安装也不难，下载好安装包并解压后，执行 install.sh 或者 install_GUI.sh ，按照指示一步步安装即可。






# 相关资料

- 《深度学习与计算机视觉》
