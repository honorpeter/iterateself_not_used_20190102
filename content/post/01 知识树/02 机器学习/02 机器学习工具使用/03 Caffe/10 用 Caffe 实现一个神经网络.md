---
title: 10 用 Caffe 实现一个神经网络
toc: true
date: 2018-08-30
---

# 用Caffe实现一个神经网络

Caffe 虽然从应用角度更针对于卷积神经网络，但是实现简单的神经网络的例子还是是不在话下的。

本节将通过实现两层的小网络来了解 Caffe 的基础概念和基本使用。<span style="color:red;">嗯。</span>



## 用Caffe实现一个两层神经网络

这一节我们用一个Hello World级别的神 经网络小例子带大家一起入门最基本的训练（Training）-预测（Inference）流程，以及 Caffe 这种框架的基本使用。

我们要用到的数据的二维可视化如下：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180831/7FFJ7AFIkm.png?imageslim)

我们将搭建一个两层神经网络，网络结构如下：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180831/2ba909hiCc.png?imageslim)


## 生成数据

首先，我们生成我们需要的数据：

gen_data.py：

```python
import pickle
import numpy as np
import matplotlib.pyplot as plt


# 划分类别的边界
def cos_curve(x):
    return 0.25 * np.sin(2 * x * np.pi + 0.5 * np.pi) + 0.5


# samples 保存二维点的坐标，labels 标明类别
np.random.seed(123)
samples = []
labels = []

# 单位样本空间内平均样本数为 50
sample_density = 50
for i in range(sample_density):
    x1, x2 = np.random.random(2)
    # 计算当前 x1 对应的分类边界
    bound = cos_curve(x1)
    # 为了方便可视化，舍弃太靠近边界的样本
    if bound - 0.1 < x2 <= bound + 0.1:
        continue
    else:
        samples.append((x1, x2))
        # 上半部分标签为1，下半部分标签为0
        if x2 > bound:
            labels.append(1)
        else:
            labels.append(0)

# 讲生成的样本和标签保存
with open('data.pkl', 'wb') as f:
    pickle.dump((samples, labels), f)

# 可视化
for i, sample in enumerate(samples):
    plt.plot(sample[0], sample[1],
             'o' if labels[i] else '^',
             mec='r' if labels[i] else 'b',
             mfc='none',
             markersize=10)

x1 = np.linspace(0, 1)
plt.plot(x1, cos_curve(x1), 'k--')
plt.show()
```

由于在 Caffe 中，非图像数据的支持并不是很好，因此这里我们用 HDF5 格式来存放上面生成的坐标数据和标签，具体代码如下：<span style="color:red;">为什么对非图像数据的支持不是很好？具体在哪里？</span>

gen_hdf5.py：

```python
import pickle
import numpy as np
import h5py

# 读取我们之前保存的数据
with open('../data.pkl', 'rb') as f:
    samples, labels = pickle.load(f)

sample_size = len(labels)

# 按照 HDF5 格式要求制作数据
samples = np.array(samples).reshape((sample_size, 2))
labels = np.array(labels).reshape((sample_size, 1))

# 生成 HDF5 格式数据
h5_filename = 'data.h5'
with h5py.File(h5_filename, 'w') as h:
    h.create_dataset('data', data=samples)
    h.create_dataset('label', data=labels)

# 生成 HDF5 数据列表
with open('data_h5.txt', 'w') as f:
    f.write(h5_filename)

```

<span style="color:red;">没明白，什么是HDF5格式的数据？想了解下这种格式，而且，为什么是创建了数据之后，又把文件名写到一个文本文件中？还是说一般我们创建 HDF5 文件的时候，可能会创建很多的 .h5 文件？</span>

需要提一点的是 Caffe 中 HDF5Data 层读取的并不是 HDF5 数据本身，而是一个 HDF5 文件的列表，所以我们除了生成 data.h5 外还生成了一个 data_h5.txt 作为 HDF5Data 层的数据源。

## 定义训练网络 train.prototxt

接下来开始定义网络和训练网络的 train.prototxt。

```
name: "SimpleMLP"
layer {
  name: "data"
  type: "HDF5Data"
  top: "data"
  top: "label"
  include {
    phase: TRAIN
  }
  hdf5_data_param {
    source: "data_h5.txt"
    batch_size: 41
  }
}
layer {
  name: "fc1"
  type: "InnerProduct"
  bottom: "data"
  top: "fc1"
  inner_product_param {
    num_output: 2
    weight_filler {
      type: "uniform"
    }
  }
}
layer {
  name: "sigmoid1"
  type: "Sigmoid"
  bottom: "fc1"
  top: "sigmoid1"
}
layer {
  name: "fc2"
  type: "InnerProduct"
  bottom: "sigmoid1"
  top: "fc2"
  inner_product_param {
    num_output: 2
    weight_filler {
      type: "uniform"
    }
  }
}
layer {
  name: "loss"
  type: "SoftmaxWithLoss"
  bottom: "fc2"
  bottom: "label"
  top: "loss"
}
```

程序代码并不复杂，每一层的意思也比较明确，name 是层的名字，type 指定层的类型， bottom 是输入 blob 的名字，top 是输出 blob 的名字。最后根据类型的不同，每一层会有特 定的参数，比如 InnterProduct，也就是全连接层中，num_output 就是输出的数量，也就是隐藏单元的个数。

整体来看，这个 prototxt 文件中首先定义了 HDF5 数据层，用于从 HDF5 文件中读取数据。读取的数据按照顺序排列分别是 data 和 label。因为在这个简单例子中，我们把所有的数据用于训练，所以只有一个 phase 为 TRAIN 的 HDF5 数据层，并且 batchsize 就是所有样本的数量。

在这个简单例子中只有全连接的 InnerProduct 层和激活函数的 Sigmoid 层。在这里需要提的是 weight_filler 这个参数。在 mxnet 中，默认是用均匀分布的随机数来初始化网络参数，所以没有专门指定。而在 Caffe 中，默认的初始化参数居然是 0, 对于这个例子会很难收敛。所以我们专门把这个参数手动指定为 uniform ，这样会默认产生 0~1 之间的随机数用来初始化当前层，除了 weight_filler 之外还有 bias_filler 用来初始化偏置的值，不过因为默认值并不影响收敛，所以例子中略过了。

最后用 SoftmaxWithLoss 层来计算损失函数，这和 7.1 节 MXNet的例子差不多。

Caffe 中自带专门用来可视化网络结构的脚本，路径是 caffe/python/draw_net.py，在控制台中执行如下指令：

```
python /path/to/caffe/python/draw_net.py train.prototxt mlp_train.png -rankdir BT
```

就可以得到Caffe可视化后的网络结构并保存在 mlp_train.png 中，如图7-4所示。


![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180831/gFakl4Gm2g.png?imageslim)


和 MXNet 中可视化的底层实现一样，都是基于 graphviz（graphviz是一个可视化图库）， 主要区别在于 Caffe 会把每个数据对应的 blob 都画出来。另外，默认情况下，网络结构的绘制顺序是输入到输出从左至右绘制，为了方便排版，这里用一 rankdir 选项改成了从下向上绘制。<span style="color:red;">还可以这样。</span>

Caffe 自带的 draw_net.py 效果并不是很美观，所以线上有一些开源的可视化 Caffe 网络结构的工具，比较为人熟知的是 github 上的 ethereon 开发的 netscope 地址为：  http://ethereon.github.io/netscope/quickstart.html 。

在netscope基础上，github 上的 dgschwend 又开发了可视化+分析网络参数、中间变量等功能的加强版地址为：[https://dgschwend.github.io/netscope/quickstart.html，比 draw _net.py 好用很多。<span style="color:red;">嗯，这两个都要总结下。</span>

## 定义用于梯度下降的 solver.prototxt

回到例子中，定义好网络结构后还需要定义用于梯度下降的 solver.prototxt：

```
net: "train.prototxt"
base_lr: 0.15
lr_policy: "fixed"
display: 100
max_iter: 2000
momentum: 0.95
snapshot_prefix: "simple_mlp"
solver_mode: CPU
```

这个文件很容易看懂，

- 第一个 net 参数指定了训练用 train.prototxt。
- base_lr 是学习率， 这里设置为 0.15。
- lr_policy 是学习率随训练进行改变的策略，这里设置为 fixed,意思是不做任何改变。
- display 是指每迭代这么多次数就显示一次训练进行的信息，比如当前 loss 的值。
- max_iter 是最大训练次数，达到这个次数就停止，同时产生当前模型的参数和 solver 状态的备份。<span style="color:red;">什么叫solver 状态的备份？</span>
- Momentum 顾名思义是冲量的系数。<span style="color:red;">什么是冲量的系数？</span>
- snapshot_prefix 是保存模型和 solver 状态文件的名字前缀。
- solver_mode 指定用 CPU 还是 GPU 进行训练，例子中先用CPU。

## 开始训练

现在数据和训练需要的配置文件都定义好了，接下来在控制台下执行下面命令：

```
/path/to/caffe/build/tools/caffe train -solver solver.prototxt
```

就开始训练了，训练过程中会输出当前的迭代次数和对应的loss值，例如下面:

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180831/96mG751JFI.png?imageslim)

<span style="color:red;">后面要自己跑一下，自己安装 GPU 跑</span>

如果不喜欢用控制台，也可以利用Python进行训练。

simple_mlp_train.py：

```python
import sys
import numpy as np

# 将 Caffe 所在路径添加到 sys.path 以便导入
sys.path.append('/path/to/caffe/python')
import caffe

# 初始化一个 SGDSolver
solver = caffe.SGDSolver('solver.prototxt')
# 开始训练
solver.solve()
# 获取训练好的网络
net = solver.net

# 指定一个输入数据，比如取值范围平面的中心
net.blobs['data'] = np.array([[0.5, 0.5]])
# 执行前向计算
output = net.forward()
print(output)

```

<span style="color:red;">上面这个 sys.path.append() 的作用具体是什么？什么时候使用这个？</span>

<span style="color:red;">感觉还是把操作写在 python 里面好，这样方便调试，而且重新运行的时候直接运行这个脚本就行。</span>

将这段代码保存为文件然后执行，和前面在控制台下的训练效果一样。

## 进行测试

在训练完我们并不能直接把 train.prototxt 拿过来用于测试，比如上面代码最后一行的 print 会输出下面结果：

```
{'loss': array(0.004321129061281681, dtype=float32)}
```

这是一个字典，键是最后一层的 blob 名字，值是 loss 的值，是因为 train.prototxt 网络中我们定义的是训练用的网络，到了做推断(Inference)的阶段，还需要对这个结构做一些修改才可以。

修改的主要部分是输入和输出部分，同时初始化网络权重的部分可有可无，完整的内容如下：

test.prototxt：

```
name: "SimpleMLP"
input: "data"
input_shape {
  dim: 1
  dim: 2
}
layer {
  name: "fc1"
  type: "InnerProduct"
  bottom: "data"
  top: "fc1"
  inner_product_param {
    num_output: 2
  }
}
layer {
  name: "sigmoid1"
  type: "Sigmoid"
  bottom: "fc1"
  top: "sigmoid1"
}
layer {
  name: "fc2"
  type: "InnerProduct"
  bottom: "sigmoid1"
  top: "fc2"
  inner_product_param {
    num_output: 2
  }
}
layer {
  name: "softmax"
  type: "Softmax"
  bottom: "fc2"
  top: "prob"
}

```

HDF5Data 层没有了，取代的是 input 用来指定输入 blob 的名字，还有 input_shape 中指定输入数据的形状。最后一层也变成了 Softmax，最顶层输出取名为 prob ，表示属于某个类的概率。把这个用于推断的网络结构保存为 test.prototxt，然后用如下 Python 代码可以执行训练好的模型用于推断(Inference)，最后生成一个和图7-3所示相似的可视化结果。

simple_mlp_test.py：

```python
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
sys.path.append('/path/to/caffe/python')
import caffe

# 构建一个网络用于 Inference
# 网络结构是 test.protootxt，权重从训练好的 simple_mlp_iter_2000.caffemodel 中获取
net = caffe.Net('test.prototxt', 'simple_mlp_iter_2000.caffemodel', caffe.TEST)

# 读取二维样本及标签
with open('../data.pkl', 'rb') as f:
    samples, labels = pickle.load(f)
samples = np.array(samples)
labels = np.array(labels)

# 可视化，第一步可视化概率值平面
X = np.arange(0, 1.05, 0.05)
Y = np.arange(0, 1.05, 0.05)
X, Y = np.meshgrid(X, Y)

# Plot the surface of probability
grids = np.array([[X[i][j], Y[i][j]] for i in range(X.shape[0]) for j in range(X.shape[1])])
grid_probs = []
for grid in grids:
    net.blobs['data'].data[...] = grid.reshape((1, 2))[...]
    output = net.forward()
    grid_probs.append(output['prob'][0][1])

grid_probs = np.array(grid_probs).reshape(X.shape)

fig = plt.figure('Sample Surface')
ax = fig.gca(projection='3d')

ax.plot_surface(X, Y, grid_probs, alpha=0.15, color='k', rstride=2, cstride=2, lw=0.5)

# 对所有样本及对应概率进行可视化
samples0 = samples[labels==0]
samples0_probs = []
for sample in samples0:
    net.blobs['data'].data[...] = sample.reshape((1, 2))[...]
    output = net.forward()
    samples0_probs.append(output['prob'][0][1])

samples1 = samples[labels==1]
samples1_probs = []
for sample in samples1:
    net.blobs['data'].data[...] = sample.reshape((1, 2))[...]
    output = net.forward()
    samples1_probs.append(output['prob'][0][1])

ax.scatter(samples0[:, 0], samples0[:, 1], samples0_probs, c='b', marker='^', s=50)
ax.scatter(samples1[:, 0], samples1[:, 1], samples1_probs, c='r', marker='o', s=50)

plt.show()
```



<span style="color:red;">什么时候，我能自己把这个项目完整手写出来，差不多就对这个有比较基础的认识了。</span>





## 相关资料

- 《深度学习与计算机视觉》
