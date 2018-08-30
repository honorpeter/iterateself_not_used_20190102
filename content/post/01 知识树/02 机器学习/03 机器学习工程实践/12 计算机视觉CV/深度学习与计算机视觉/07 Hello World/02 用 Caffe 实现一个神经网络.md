---
title: 02 用 Caffe 实现一个神经网络
toc: true
date: 2018-08-30
---

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
