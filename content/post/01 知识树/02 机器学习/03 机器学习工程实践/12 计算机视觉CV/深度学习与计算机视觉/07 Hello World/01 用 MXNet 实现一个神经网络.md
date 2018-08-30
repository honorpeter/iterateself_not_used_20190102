---
title: 01 用 MXNet 实现一个神经网络
toc: true
date: 2018-08-29
---
# 第 7 章 Hello World!

从第7章开始就进入到了实战阶段，将通过一系列基础例子了解基于深度学习计算机 视觉的有趣应用和实施方法。本章作为实战阶段的第一章，用一个Hello World级别的神 经网络小例子带大家一起入门最基本的训练（Training）-预测（Inference）流程，以及 MXNet 和 Caffe 这两种框架的基本使用。

对于 MXNet 和 Caffe 这两种框架，本书会基于实例对其用法进行最基本的介绍。不过作为一本入门书，本书不会涉及分布式使用、代码细节和架 构等方面，而只会专注于基本算法的实现方法。深度学习框架多种多样，但框架终究是工具，重点是通过了解每个例子和背后对应的思想来入门深度学习/计算机视觉这个有用又有趣的领域。<span style="color:red;">嗯。</span>


## 用MXNet实现一个神经网络

MXNet 的起源已经在第 1 章大概介绍过，本节主要介绍 MXNet 的安装和基本概念，并通过实现一个最简单的神经网络来了解 MXNet 的使用。

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

## 安装 MXNet

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

### MXNet 基本使用

在第 3 章已经提到过，当描述一个神经网络或者一些计算公式及函数的时候，实质上 是在描述一种可以用图表示的计算关系。在MXNet中，这种计算关系可以有两种方式表 达和计算，即命令式(Imperative)和符号式(Symbolic)。比如(a+b)*c,命令式计算的代 码如下：

import mxnet as mx #申请内存并赋值，默认利用CPU

a = mx.nd b = mx.nd c = mx.nd #执行计算 d = (a +

array([1]) array([2]) array([3])

b) * c

\#将结果以NumPy的array的形式表示， print(d.asnumpy())

[9.]

\#将结果以标量的形式表示，9.0 print(d.asscalar (>)

和NumPy的array很像，其实ND Array里很多的操作和方法确实和NumPy是一样的。

回到正题，相应的符号式计算的代码如下： import mxnet as mx

\#定义3个符号变量，注意符号变量都需要一个显式指定的名字 a = mx.sym.Variable(* a') b = mx.sym.Variable(* b') c = mx.sym.Variable(•c*)

\#定义计算关系

d = (a + b) * c #指定每个输入符号对应的输入

| input args | ={      |                   |
| ---------- | ------- | ----------------- |
|            | 1 a':   | mx.nd.array([1]), |
|            | 'b':    | mx.nd.array([2]), |
| }          | * c * : | mx.nd.array([3])  |

\# a、b、c和d定义的只是计算关系，执行计算(包括申请相应内存等操作)需要Executor

\#用bind ()函数指定输入，d为输出，cpu ()指定计算在cpu上进行 executor = d.bind(ctx=mx.cpu(), args=input_args)

\#执行计算

executor.forward()

\#打印结果，[9.]

print(executor.outputs[0].asnumpy())

可以看到，命令式计算非常灵活直接，每个变量的内存分配是即时完成的，计算也是 即时完成。而符号式计算则是函数式编程的思路，计算也是延迟(lazy)的，符号变量只 能定义计算关系。这种计算关系在执行前需要通过bind()方法产生一个执行器(Executor), 用来把数据的NDArray和Symbol绑定起来，实际的计算发生在Executor调用时。符号式 计算很明显要麻烦一些，不过优点是延迟计算和对计算图的优化能得到更优的性能。另外， 在MXNet中通过符号式计算求导是非常方便的，继续接前面例子：

\#定义一个变量用来保存关于a的梯度，随便初始化一下

grad_a = mx. nd. empty (1)    ..

\#在bind ()函数中指定要求梯度的变量

executor = d.bind( ctx=mx.cpu(), args=input_args, args_grad={* a *: grad_a}

)

\#因为梯度是传播的，所以最后输出节点的梯度需要指定，这里用1 executor.backward(out_grads=mx.nd.ones(1))

\#计算出梯度为3.0，也、就ic的值，将自动刷新在grad_a中 print(grad_a.asscalar())

在MXNet中，第一段代码中，用于命令式计算的NDArray是一个非常基础的模块， 符号式计算的Symbolic模块结合NDArray 一起使用可以定义一些基础的计算关系并进行 计算。在这两个模块基础上可以搭建一些简单的计算关系，比如神经网络。但是如果每次 都像上面代码一样从底层搭建，并且自己指定计算梯度等操作，甚至更进一步比如在神经 网络中进行后向传播和梯度更新等，将是一件非常麻烦的事情。所以在NDArray和Symbolic 基础上，MXNet提供了一些接口进行封装来简化这些操作，包含通用性更好的Module模 块和更为简单的Model模块。

既然要训练模型，就不能避免与数据和机器打交道，所以MXNet也提供了数据读取 和处理的IO Data Loading模块和用来支持多GPU卡及分布式计算的KVStore模块。本书 作为一本入门书籍，将主要涉及6大模块中除了 KVStore以外的模块，神经网络模型的搭 建也主要基于Module和Model模块，而不需要从Symbolic开始进行复杂的底层编写。更 多关于这些模块的细节可以参考官方文档[http://mxnet.io/zh/api/python/](http://mxnet.io/zh/api/python/%e3%80%82)[。](http://mxnet.io/zh/api/python/%e3%80%82)

7.1.4用MXNet实现一个两层神经网络

本节将基于Model模块实现本书中第一个神经网络。数据和网络的模型结构就是第3

章中3.2.2中的例子，产生数据的代码如下： import pickle import numpy as np

\#划分类别的边界

def cos_curve(x):

for i in range(sample_density):

xl, x2 = np.random.random(2)

\#计算当前xl对应的分类边界 bound = cos_curve(xl)

\#为了方便可视 1 七，舍弃太靠近边界的样本 if bound -    0.1    < x2 <= bound. +    0.1:

continue

else :

samples.append((xl, x2))

\#上半部分标签为1,下半部分标签为2 if x2 > bound:

labels.append(1)

else:

labels.append(0)

\#将生成的样本和标签保存

with open (1 data. pkl *,    * wb *) as f:

pickle.dump((samples, labels), f)

\#可视化

import matplotlib.pyplot as pit for i, sample in enumerate(samples):

pit.plot(sample[0], sample[1],    * o * if labels[i] else ' A * ,

mec= * r * if labels[i] else *b *, mfc= * none *,

markersize=l0) xl = np.linspace(0,    1)

pit.plot(xl, cos_curve(xl) ,    'k--*)

pit.show()

数据的二维可视化参照第3章的图3-7所示。然后通过MXNet的model模块搭建一个

两层神经网络，网络结构参照第3章的图3-8所示，代码如下： import numpy as np import mxnet as mx

\#    定义data

data = mx.sym.Variable(* data *)

\#    data经过一个两输出的全连接层

f cl = mx.sym.FullyConnected(data=data, name=,fcl,, num_hidden=2)

\#再经过一个sigmoid激活层

sigmoidl = mx.sym.Activation(data=fclz name= * sigmoidl*, act_type=* sigmoid*)

\#然后再过一个全连接层

fc2 = mx.sym.FullyConnected(data=sigmoidl, name= * fc2 *, num_hidden=2)

\#最后经过Softmax输出，Sof tmaxOutput还自带NLL作为loss进行计算 mlp = mx.sym.SoftmaxOutput(data=fc2, name='softmax')

\#网络结构可视化，基于graphviz

shape = {'data': (2,)}

mlp_dot = mx.viz.plot_network(symbol=mlp, shape=shape) mlp_dot.render(* simple_mlp.gv', view=True)

程序执行后就定义好了计算关系，最后3行代码是网络结构的可视化，执行程序得到 如图7-2所示的结构图。



图7-2 MXNet可视化简单的二层神经网络

有了网络，接下来可以读取数据训练模型了。对于内存中生成的数据，可以用 mxnet.io.NDArraylter来生成一个用于遍历训练数据和对应标签的迭代器，然后用model进

行训练。代码如下： import pickle import logging #用pickle读取数据

with open (* data. pkl *,    ' rb *) as f:

samples, labels = pickle.load(f)

\#设置logging级别，显示训练时的信息

logging.getLogger().setLevel(logging.DEBUG)

\#对于这个简单例子，就用全量梯度下降法

batch_size = len(labels) samples = np.array(samples) labels = np.array(labels)

\#生成训练数据迭代器

train_iter = mx.io.NDArraylter(samples, labels, batch_size)

\# 利用 mxnet .model. FeedForward. create 训练一个网络 #迭代1000代，学习率0.1,冲量系数0.99

model = mx.model.FeedForward.create( symbol=mlp,

X=train_iter, num_epoch=l000, learning_rate=0.1, momentum=0.99)

\# mxnet也提供先设置好参数，然后通过fit ()方法进行训练的方式 model = mx.model.FeedForward(

symbol=mlpf num_epoch=1000, learning_rate=O.1, momentum=0.99)

model.fit(X=train_iter)

f V V

\#训练好的模型进行预测，正中央一点属于类别1

print(model.predict(mx.nd.array([[0.5,    0.5]])))

训练过程中可以看到实时输出的loss信息，每迭代完一代（epoch）就进行一次重 新设置：

INFO

INFO

INFO

INFO

INFO

root

root

root

root

root

Start training with [cpu (0)] Epoch[0] Resetting Data Iterator Epoch[0] Time cost=0.007

Epoch[1] Resetting Data Iterator Epoch[1] Time cost=0.002

接下来用训练好的模型对所有样本和取值范围的平面进行分类，并画出对应的概率可 视化的图，代码如下：

import matplotlib.pyplot as pit from mpl_toolkits.mplot3d import Axes3D #定义取if范围平面的采样格点，以0.05为间隔 X = np.arange(0, 1.05, 0.05)

Y = np.arange(0z 1.05, 0.05)

X, Y = np.meshgrid(X, Y)

\#按照模型可以接受的格式生成每个格点的坐标

grids = mx.nd.array([ [X [i] [j], Y[i] [j]] for i in range(X.shape [0]) for j in range(X.shape[1])])

\#获取模型预测的结果，以标签1为结果

grid_probs = model.predict(grids)[:,    1].reshape(X.shape)

\#定^图标

fig = pit.figure(* Sample Surface *) ax = fig.gca(projection= * 3d*)

\#画出整个结果的表面

ax.plot_surface(X, Y, grid_probs, alpha=0.15, color= * k'z rstride=2, cstride=2, lw=0.5)

\#按照标签选出对应样本

samplesO = samples[labels==0]

pit.show()

程序生成的三维可视化图如图7-3所示。

注意这只是最简单的例子，目的是帮助了解MXNet的基本使用，并没有设置验证/测 试集，训练迭代1000次也只是随便定的。7.2节将用Caffe实现这个例子，而更加实际的 例子会从第8章开始。



图7-3标签为1的概率在取值平面上的分布可视化
