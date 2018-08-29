---
title: 01 用 MXNet 实现一个神经网络
toc: true
date: 2018-08-29
---
#### 第 7 章 Hello World!

从第7章开始就进入到了实战阶段，将通过一系列基础例子了解基于深度学习计算机 视觉的有趣应用和实施方法。本章作为实战阶段的第一章，用一个Hello World级别的神 经网络小例子带大家一起入门最基本的训练（Training）-预测（Inference）流程，以及MXNet 和Caffe这两种框架的基本使用。对于MXNet和Caffe这两种框架，本书会基于实例对其 用法进行最基本的介绍。不过作为一本入门书，本书不会涉及分布式使用、代码细节和架 构等方面，而只会专注于基本算法的实现方法。深度学习框架多种多样，但框架终究是工 具，重点是通过了解每个例子和背后对应的思想来入门深度学习/计算机视觉这个有用又有 趣的领域。

和第6章一样，本章中完整实例的代码都可以在下面地址找到，之后章节中的每个入 门实例的代码也将放在这个github的代码仓库中，不再强调，地址为https://github.com/ frombeijingwithlove/ dlcvforbeginners o

7.1用MXNet实现一个神经网络

MXNet的起源已经在第1章大概介绍过，本节主要介绍MXNet的安装和基本概念， 并通过实现一个最简单的神经网络来了解MXNet的使用。

7.1.1 基础工具、NVIDIA驱动和CUDA安装

首先是安装大部分开发工具需要的基础依赖工具包，比如git、用于矩阵计算的atlas, 和图可视化的graphviz等，以Ubuntu 16.04 LTS为例，执行下面命令安装包：

»    sudo    apt    update

»    sudo    apt    install    build-essential    git libatlas-base-dev

\>>    sudo    pip    install    graphviz

第5章和第6章讲过的pip、NumPy和OpenCV也是需要的，安装方法已经讲过在此 就不再介绍了。

对于当前的所有深度学习框架，如果要训练神经网络一定离不开（NVIDIA的）GPU, 以及配套的GPU编程工具包CUDA。所以接下来是安装NVIDIA的驱动和CUDA工具包。 安装NVIDIA驱动前需要先卸载系统自己的驱动：

» sudo apt ——purge remove xserver-xorg-video-nouveau

然后添加NVIDIA驱动的源：

» sudo add-apt-repository ppa:graphics-drivers/ppa

然后就可以安装驱动和CUDA工具包了。

\>> sudo apt install nvidia-361 nvidia-settings nvidia-prime » sudo apt install nvidia-cuda-toolkit

安装完成后，在控制台输入：

\>> nvidia-smi

如果安装成功则会显示显卡的信息，比如笔者的GTX980M笔记本显示信息如图7-1 所示。

心：:•、leaf醪Arreat-Top: ~

leaf@Arreat-Top:-$ nvtdta-snt Sat Apr 23 17:45:29 2016

NVIDIA-SMI 351.42

Driver Version: 361.42

| GPUFan    | NaneTemp    | Perf                      | ..............+ ■Pe「ststence-M\| Pwr:Usage/Cap\| | Bus-IdMenor | •........+..........Disp.A \| Volattle y-Usage \| GPU-Util | Uncorr, ECC Compute M. |
| --------- | ----------- | ------------------------- | ------------------------------------------------- | ----------- | ---------------------------------------------------------- | ---------------------- |
| 0         | GeForce GTX | 980H    Off \|            | 0000:01:00.0                                      | Off J       | N/A                                                        |                        |
| N/A       | 54C         | P8                        | 7W / N/A \|                                       | 322M1B /    | 8191M1B j    0%                                            | Default                |
|           |             |                           |                                                   |             |                                                            |                        |
| Processes |             |                           |                                                   |             | GPU Memory                                                 |                        |
| GPU       |             | PID                       | Type Process name                                 |             | Usage                                                      |                        |
| 0         |             | 9B6                       | G /usr/llb/xorg/Xorg                              |             | 207M1B                                                     |                        |
| 0         |             | 1470                      | G compiz                                          |             |                                                            | 92M1B                  |
| 0         | 26046       | G    unity-control-center |                                                   | IMiB        |                                                            |                        |

leaf@Arreat-Top:-$ Q)

图7-1显卡信息

如果是其他的Linux系统，步骤也很相似，首先卸载自带的显卡驱动，然后用系统自 带软件包或者到NVIDIA官网下载驱动及CUDA按照说明进行安装，下载地址为 <http://www.nvidia.com/Download/index.aspx> 或 [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads%e3%80%82)[。](https://developer.nvidia.com/cuda-downloads%e3%80%82)

cuDNN是CUDA中专门为加速深度神经网络设计的库，是个可选的安装选项。下载 ±也址为 [https://developer.nvidia.com/cudnn](https://developer.nvidia.com/cudnn%e3%80%82)[。](https://developer.nvidia.com/cudnn%e3%80%82)

找到对应的版本并填写需要的信息之后就可以下载了。下载之后是一个压缩包，这里 以cuDNN 5.1为例，执行以下命令将cuDNN中的库解压并添加到CUDA对应文件夹下。

\>> tar -xvzf cudnn-8.0-linux-x64-v5.1-ga.tgz

» sudo cp -P cuda/include/cudnn.h /usr/local/cuda/include

» sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64

任何深度学习框架中，基于CPU的矩阵计算包也是基础的库之一，除了本节一开始安 装的atlas, Intel的MKL (Math Kernel Library)因为其优异的性能，往往是一个更佳的选 项，MKL 的下载地址为 [https://software.intel.com/en-us/intel-mkl/](https://software.intel.com/en-us/intel-mkl/%e3%80%82)[。](https://software.intel.com/en-us/intel-mkl/%e3%80%82)

MKL对于个人是免费的，需要一定的注册步骤获取一个许可证。其安装也不难，下载 好安装包并解压后，执行install.sh或者install_GUI.Sh，按照指示一步步安装即可。

7.1.2 安装 MXNet

MXNet 的 github 页面是 [https://github.com/dmlc/mxnet](https://github.com/dmlc/mxnet%e3%80%82)[。](https://github.com/dmlc/mxnet%e3%80%82)

在这里可以找到源代码的git地址，然后在要保存的控制台地址中输入下面命令:

» git clone --recursive <https://github.com/dmlc/mxnet>

之后就会在执行命令的文件夹下得到一个mxnet的文件夹。第一步是配置安装的基础

选项，打开mxnet/make文件夹下的config.mk文件，主要需要配置的是以下3个选项。

□    USE_CUDA = 0；

□    USECUDNN = 0；

□    USEBLAS = atlas。

上面列出的都是默认选项，对于训练网络的需求，需要至少把USE_CUDA改成1，如 果需要cuDNN和mkl的话则需要把USE_CUDNN改成1，USE_BLAS改为mkl。

配置好后就可以开始安装了。在Ubuntu下有个非常方便的方式，就是进入 mxnet/setup-utils文件夹下，直接执行对应脚本：

» cd mxnet/setup-utils » sh install-mxnet-ubuntu-python.sh

等待执行结束就大功告成了。当然一般的方式是回到mxnet目录下，执行：

» cd mxnet » make - j

自动利用所有可用的CPU核对代码进行编译，如果在-j后面直接加上数字可以指定用的核 数。然后配置Python接口：

» cd python

» sudo python setup.py install 万事俱备，接下来可以开始使用这个强大的框架了。

7.1.3 MXNet基本使用

在第3章已经'提到过，当描述一个神经网络或者一些计算公式及函数的时候，实质上 是在描述一种可以用图表示的计算关系。在MXNet中，这种计算关系可以有两种方式表 达和计算，即命令式(Imperative)和符号式(Symbolic)。比如(a+b)*c,命令式计算的代 码如下：

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

7.2用Caffe实现一个神经网络

Caffe虽然从应用角度更针对于卷积神经网络，但是实现7.1节的例'子当然是不在话下 的。本节将通过实现两层的小网络来了解Caffe的基础概念和基本使用。

7.2.1 安装 Caffe

Caffe是个依赖非常多的框架，除了在7.1.1节中我们已经安装好的基础依赖，还需要 以下的依赖包。

» sudo apt install libprotobuf-dev libleveldb-dev libsnappy-dev libboost-all-dev libhdf5-serial-dev protobuf-compiler gfortran libjpeg62 libfreeimage-dev libgoogle-glog-dev libbz2-dev libxml2-dev libxslt-dev libffi-dev libssl-dev libgflags-dev liblmdb-dev python-yaml

然后可以开始安装Caffe 了，先到要安装Caffe的文件夹下：

» git clone <https://github.com/BVLC/caffe.git>

然后到caffe文件夹下，找到Makefile.config.example文件复制一份：

» cd caffe

» cp Makefile.config.example Makefile.config

和MXNet类似，Makefile.config是编译的配置文件，在这个文件里可以配置一些编译 选项，-般来说主要配置CUDA、cuDNN和bias库。比如笔者的机器上，主要是下面两 个选项：

□    USE_CUDNN:=1；

□    BLAS:=mklo

默认情况下CPU_ONLY:=1是被注释掉的，所以不用管。除非是在没有NVIDIA的 GPU机器上安装Caffe,那么把注释取消即可。

还有一个选项是WITH_PYTHON_LAYER:=1,意思是支持用Python定义神经网络中 的层，和MXNet中定义层的方式有些相像。如果要使用一些Python的层或是一些特定 功能的Caffe版本，比如Ross Girshick的py-faster-rcnn,那么就需要把这一项前的注释 取消。

配置好Makefile.config后，就可以开始编译了，依次执行下面的命令：

» make pycaf fe - j

» make all -j

» make test - j

因为Caffe的依赖过多，在安装过程中有可能找不到一些动态库，这个时候需要把相 对的路径加入到LD_LIBRARY_PATH下即可，如果是头文件则可以把对应路径加入到 CPLUS_INCLUDE_PATH中。比如找不到HDF5的库，可在控制台下执行：

» export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/hdf5/serial

为了在Python中直接调用Caffe,还需要把Caffe的Python路径加入到PYTHONPATH0

» export PYTHONPATH=$PYTHONPATH=:/path/to/caffe/python

有的版本的Ubuntu下如果是使用apt安装的cuda,还需要添加下面两个路径：

□    /usr/lib/nvidia-cuda-tookit；

□    /usr/lib/x86-linux-gnu o

7.2.2 Caffe的基本概念

Caffe从本质上来说和MXNet中Symbolic的使用方式差不多，都是先定义好一个计算 关系，然后根据这个计算关系结合数据训练和使用模型。在Caffe中，最基本的计算节点 是层(Layer)，所有的计算关系都是基于层的，无论是Caffe预定义好的层，还是用户自 定义的层。这和MXNet中预定义层的使用方式也很像，如果直接基于Python写层的定义 就更像了。不过这里我们要了解的是更常用的一种使用方式，即利用protobuf的格式而不 是代码来定义网络的结构，然后再结合数据进行训练，也就是说用Caffe训练模型是不需 要写代码的。这体现了 Caffe设计哲学中利用表达式(expression)和模块化(Modularity) 的特点。

Caffe中预定义的层覆盖了当前流行的网络结构中几乎所有的类型，比如卷积神经网络 最常用到的全连接层(InnerProduct)、卷积层(Convolution)和池化层(Pooling)；各种 各样的激活函数层(ReLU、Sigmoid、PReLU等)；以及数据交互的各种层(Data、HDF5Data、 ImageData 等)；输出及计算损失函数的层(Softmax、SoftmaxWithLoss> Euclidean 等)。 除了 Caffe的接口文档，各种常用层的信息一览在Caffe官网也有列出地址为 <http://caffe.berkeleyvision.org/tutorial/layers.htmlo>

基于各种层就可以构建成网络(Net),然后定义好数据，就可以训练一个模型了。在 Caffe中，数据的形式是一种叫Blob的类，其实就是空间连续的多维数组，比如存储图像 的时候是个四维的数组，四个维度分别是批大小、通道数、图像高度、图像宽度。有了网 络结构和数据之后，再定义一个利用梯度下降法做优化的Solver模块，就可以训练网络了。 具体总结如下。

□层(Layer);

□网络(Net)；

□数据（Blob）;

□梯度下降（Solver）。

这4个部分就是入门学习最关键的内容。

7.2.3用Caffe实现一个两层神经网络

本节还是通过例子来了解Caffe的基本使用，比如7.1节中神经网络的小例子。第一步 是准备数据，在Caffe中，非图像数据的支持并不是很好，这里我们用HDF5格式来准备 7.1节中产生的坐标数据和对应标签，具体代码如下：

import pickle import numpy as np import h5py #读取先前保存好的数据

with open (* data .pkl1,    * rb *) as f:

samples, labels = pickle.load(f)

sample_size = len(labels)

\#按照HDF5格式要求制作数据

samples = np. array (samples) . reshape ( (sample_size, 2)) labels = np.array(labels).reshape((sample_sizeA 1))

\#生成HDF5 &式数据

h5_filename = * data.h5 *    )

with h5py. File (h5_filename, * w *) as h:

h.create_dataset(* data *, data=samples) h.create_dataset(* label *, data=labels)

\#生成HDF5数据刿表

with open(* data_h5.txt *,    * w *) as f:

f.write(h5_filename)

需要提一点的是Caffe中HDF5Data层读取的并不是HDF5数据本身，而是一个HDF5 文件的列表，所以我们除了生成data.h5外还生成了一个data_h5.txt作为HDF5Data层的数 据源。接下来开始定义网络和训练网络的train.prototxt。

name:    "SimpleMLP"

layer {

name: "data" type: "HDF5Data" top: "data" top: "label" include {

phase: TRAIN

}

hdf5_data_param {

source: "data_h5 . txt** batch_size:    41

}

}

layer {

name: "fcl" type: "InnerProduct" bottom:    "data"

top: "fcl"

inner_product_param {

| num_output:    2  |                   |
| ----------------- | ----------------- |
| weight filler {   |                   |
| }}}layer {        | type:    "uniform |
| name:             | "sigmoidl"        |
| type:             | "Sigmoid"         |
| bottom:           | :,'fcln           |
| top:    ”}layer { | sigmoidl"         |

name:    "fc2"

type:    "InnerProduct"

bottom: "sigmoidl" top:    "fc2"

inner_product_param { num_output:    2

weight_filler {

type: "uniform"

}

}

}

layer {

name: "loss"

type: "SoftmaxWithLoss"

bottom:    "fc2"

bottom: J* label*' t

top: "loss"

}

程序代码并不复杂，每一层的意思也比较明确，name是层的名字，type指定层的类型， bottom是输入blob的名字，top是输出blob的名字。最后根据类型的不同，每一层会有特 定的参数，比如InnterProduct，也就是全连接层中，num_output就是输出的数量，也就是 隐藏单元的个数。整体来看，这个prototxt文件中首先定义了 HDF5数据层，用于从HDF5 文件中读取数据。读取的数据按照顺序排列分别是data和label。因为在这个简单例子中， 我们把所有的数据用于训练,所以只有一个phase为TRAIN的HDF5数据层，并且batch^ize 就是所有样本的数量。在这个简单例子中只有全连接的InnerProduct层和激活函数的 Sigmoid层。在这里需要提的是weight_filler这个参数。在mxnet中，默认是用均匀分布的 随机数来初始化网络参数，所以没有专门指定。而在Caffe中，默认的初始化参数居然是0, 对于这个例子会很难收敛。所以我们专门把这个参数手动指定为uniform,这样会默认产生 0〜1之间的随机数用来初始化当前层，除了 weight_filler之外还有bias_filler用来初始化偏 置的值，不过因为默认值并不影响收敛，所以例子中略过了。最后用SoftmaxWithLoss层 来计算损失函数，这和7.1节MXNet的例子差不多。Caffe中自带专门用来可视化网络结 构的脚本，路径是caffe/python/draw_net.py,在控制台中执行如下指令：

» python /path/to/caffe/python/draw_net.py train.prototxt mlp_train.png

-rankdir BT

就可以得到Caffe可视化后的网络结构并保存在mlp_train.png中，如图7-4所示。



data (HDFSDala)

图7-4用Caffe自带的draw net.py可视化的训练阶段网络结构

和MXNet中可视化的底层实现一样，都是基于graphviz（graphviz是一个可视化图库）， 主要区别在于Caffe会把每个数据对应的blob都画出来。另外，默认情况下，网络结构的 绘制顺序是输入到输出从左至右绘制，为了方便排版，这里用一rankdir选项改成了从下向 上绘制。Caffe自带的draw_net.py效果并不是很美观，所以线上有一些开源的可视化Caffe 网络结构的工具，比较为人熟知的是github上的ethereon开发的netscope地址为： <http://ethereon.github.io/netscope/quickstart.htmlo>

在netscope基础上，github上的dgschwend又开发了可视化+分析网络参数、中间变量 等功能的加强版地址为：[https://dgschwend.github.io/netscope/quickstart.html](https://dgschwend.github.io/netscope/quickstart.html%ef%bc%8c%e6%af%94)[，比](https://dgschwend.github.io/netscope/quickstart.html%ef%bc%8c%e6%af%94) draw net.py 好用很多。

回到例子中，定义好网络结构后还需要定义用于梯度下降的solver.prototxt：

net: "train .prototxt’’

momentum: 0.95

snapshot_prefix: "simple_mlp" solver_mode: CPU

这个文件很容易看懂，第一个net参数指定了训练用train.prototxt。base_lr是学习率， 这里设置为0.15。Impolicy是学习率随训练进行改变的策略，这里设置为fixed,意思是不 做任何改变。display是指每迭代这么多次数就显示一次训练进行的信息，比如当前loss的 值。maxjter是最大训练次数，达到这个次数就停止，同时产生当前模型的参数和solver 状态的备份。Momentum顾名思义是冲量的系数，snapshot_prefix是保存模型和solver状态 文件的名字前缀。solver_mode指定用CPU还是GPU进行训练，例子中先用CPU。

现在数据和训练需要的配置文件都定义好了，接下来在控制台下执行下面命令：

» /path/to/caffe/build/tools/caffe train -solver solver.prototxt

就开始训练了，训练过程中会输出当前的迭代次数和对应的loss值，例如下面:

| 10102 | 15:40:52.076025 | 5821 |
| ----- | --------------- | ---- |
| 10102 | 15:40:52.076042 | 5821 |
| 10102 | 15:40:52.076056 | 5821 |
| fixed |                 |      |
| 10102 | 15:40:52.076231 | 5821 |

0.668031

| 10102    15:40:52.076267  | 5821   |
| ------------------------- | ------ |
| #0: loss = 0.668031       | (* 1 = |
| 10102    15:40:52.076275  | 5821   |
| 0.15    -                 |        |
| 10102    15:4(/:52.078455 | 5821   |
| 0.250734                  |        |
| 10102    15:40:52.078527  | 5821   |
| 林0: loss =    0.250734   | (* 1 = |
| 10102    15:40:52.078536  | 5821   |
| =0.15                     |        |
| 10102    15:40:52.080875  | 5821   |
| 0.24788                   |        |
| 10102    15:40:52.080978  | 5821   |

\#0:

loss = 0.24788

caffe.cpp:251] Starting Optimization solver.cpp:291] Solving SimpleMLP

| solver.cpp:292]                 | Learning Rate          | Policy: |
| ------------------------------- | ---------------------- | ------- |
| solver.cpp:240]                 | Iteration 0,           | loss =  |
| solver.cpp:256] 0.668031 loss)  | Train net              | output  |
| sgd solver.cpp:106] Iteration 0 | ,lr =                  |         |
| solver.cpp:240]                 | Iteration 100,         | loss =  |
| solver.cpp:256] 0.250734 loss)  | Train net              | output  |
| sgd_solver.cpp:                 | 106] Iteration 100, lr |         |
| solver.cpp:240]                 | Iteration 200,         | loss =  |
| solver.cpp:256]                 | Train net              | output  |

(*    1    =    0.24788 loss)

如果不喜欢用控制台，也可以利用Python进行训练。

import sys

import numpy as np

\#将Caffe所在路径添加到sys .path以便导入 sys.path.append(*/opt/caffe/python') import caffe

\# 初始化一个SGDSolver

solver = caffe.SGDSolver(* solver.prototxt *) #开始训练 solver.solve()

\#获取训练好的网络

net = solver.net

\#指定一个输入数据，比如取值范围平面的中心

net.blobs[* data']    = np.array([[0.5,    0.5]])

\#执行前向计算

output = net.forward()

\#输出结果

print(output)

将这段代码保存为文件然后执行，和前面在控制台下的训练效果一样。不过这样训练 完后并不能立刻使用，比如上面代码最后一行的print会输出下面结果：

{•loss1: array(0.004321129061281681, dtype=float32)}

这是一个字典，键是最后一层的blob名字，值是loss的值，是因为train.prototxt网络中我

们定义的是训练用的网络，到了做推断(Inference)的阶段，还需要对这个结构做一些修

改才可以。修改的主要部分是输入和输出部分，同时初始化网络权重的部分可有可无，完

整的内容如下：

name: '’SimpleMLP" input: "data" input_shape {

dim: 1 dim: 2

}

layer {

name: "fcl" type:    "工 rmerProduct"

bottom: "data" top: "fcl"

inner_product_param {

num_output:    2    )

} ~ '

}

layer {

name: "sigmoidl" type: "Sigmoid" bottom: "fcl" top: "sigmoidl"

}

layer {

}

}

layer {

name: "softmax" type:    "Softmax"

bottom: nfc2" top: "prob"

}

HDF5Data层没有了，取代的是i叩ut用来指定输入blob的名字，还有i叩ut_shape中

指定输入数据的形状。最后一层也变成了 Softmax,最顶层输出取名为prob,表示属于某

个类的概率。把这个用于推断的网络结构保存为testprototxt,然后用如下Python代码可以

执行训练好的模型用于推断(Inference),最后生成-个和图7-3所示相似的可视化结果。

import sys

import pickle

import numpy as np

import matplotlib.pyplot as pit

from mpl_toolkits.mplot3d import Axes3D

sys.path.append('/opt/caffe/python')

import caffe

\#构建一个网络用于Inference

\# 网络结构是 test .prototxt，权重从训练好的 simple mlp iter 2000 . caf femodel 中 获取

net = caffe.Net(1 test.prototxt *,    1simple_mlp_iter_2000.caffemodel*,

caffe.TEST)

\#读取二维样本及标签

with open (' data. pkl',    * rb1) as f:

samples, labels = pickle.load(f)

samples = np.array(samples)

labels = np.array(labels)

\#可视化，第一步可视化概率值平面

X = np.arange (0z 1.05, 0.05)

Y = np.arange(0, 1.05, 0.05)

X, Y = np .meshgrid (X, Y)

grids = np. array ([ [X [i] [j ] , Y [i] [ j ] ] for i in range (X. shape [0]) for j in range(X.shape[1])]) grid_probs =    []

for grid in grids:

net.blobs[* data *].data[...]    = grid.reshape((1,    2))[...]

output = net.forward()

grid一probs.append(output[* prob’] [0] [1])

grid_probs = np.array(grid_probs).reshape(X.shape)

fig = pit.figure(1 Sample Surface *)

ax = fig.gca(projection=1 3d*)

ax.plot_surface(X, Y, grid_probs, alpha=0.15, color= * k * A rstride=2, cstride=2, lw=0.5)

\#对所有样本及对应概率进行可视化

samplesO = samples[labels==0]

samples0_probs =    []

for sample in samplesO :

net.blobs[1 data *].data[...]    = sample.reshape( (1,    2))[...]

output = net.forward()

samples0_probs.append(output['prob1] [0] [1]) samples1    = samples[labels==l]

samplesl_probs =    []

for sample in samplesl:

net.blobs[* data *].data[. . . ]    = sample.reshape((1,    2))[...]

output = net.forward()

samplesl_probs.append(output['prob *] [0] [1]) ax.scatter(samplesO[:,    0],    samplesO[:,    1],    samples0_probs,    c=1b1z

marker=’八，，    s=50)

ax.scatter(samplesl[:,    0],    samplesl[:,    1],    samplesl_probs,    c= * r * z

marker= * o *,    s=50)

pit.show()
