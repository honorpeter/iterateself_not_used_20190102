---
title: 10 基于 Caffe 实现 LeNet-5 网络
toc: true
date: 2018-09-01
---

# 需要补充的

- 要对这个项目进行重新的组织，该分离出去的要进行分离。
- 要对 Caffe 进行总结，之前看过简单的例子之后，以为 Caffe 就是这样的，现在看来 Caffe 还是有非常丰富的功能的，如果连认识都认识不到，那么根本没有办法恰当的使用
- 这个要自己跑一下。把结果总结到这里
- 这个是 LeNet-5 的 ，别的网络也要进行总结。并进行对比。



#  LeNet-5 基于 Caffe 实现对手写数字的识别

OK，数据我们已经准备好了，下面我们开始使用 Caffe 来搭建 LeNet-5 模型来对手写数字进行识别。我们会对模型进行评估和测试。


## 训练 LeNet-5

本书采用的结构和Caffe官方例子的版本没有区别，只是输入的数据层变成了我们自己制作的LMDB，用于描述数据源和网络结构的 lenet_train_val.prototxt 如下：

```prototxt
name: "LeNet"
layer {
  name: "mnist"
  type: "Data"
  top: "data"
  top: "label"
  include {
    phase: TRAIN
  }
  # 数据层的参数，指定均值和缩放比例，数据会先减去 mean_value 然后乘上 scale
  # 具体到 mnist 图片，就是把 0~255 之前的值缩放到 -0.5~0.5，帮助收敛
  transform_param {
    mean_value: 128
    scale: 0.00390625
  }
  # 指定训练阶段的数据，每次迭代用 50 个样本
  data_param {
    source: "../data/train_lmdb"
    batch_size: 50
    backend: LMDB
  }
}
layer {
  name: "mnist"
  type: "Data"
  top: "data"
  top: "label"
  include {
    phase: TEST
  }
  transform_param {
    mean_value: 128
    scale: 0.00390625
  }
  # 指定验证阶段的数据，每次计算 100 个。
  data_param {
    source: "../data/val_lmdb"
    batch_size: 100
    backend: LMDB
  }
}
layer {
  name: "conv1"
  type: "Convolution"
  bottom: "data"
  top: "conv1"
  # 卷积核的学习率为基础学习率乘以 lr_mult
  param {
    lr_mult: 1
  }
  # 偏置的学习率为基础学习率乘以 lr_mult
  param {
    lr_mult: 2
  }
  # 输出 20 个 feature map，卷积核大小为 5x5
  convolution_param {
    num_output: 20
    kernel_size: 5
    stride: 1
    # weight_filler 用于初始化参数，xavier 是一种初识化方法，源于 Bengio 组 2010 年论文
    # 《 Understanding the difficulty of training deep feedforward neural networks 》
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  # 在卷积层后接 Pooling 层
  name: "pool1"
  type: "Pooling"
  bottom: "conv1"
  top: "pool1"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "conv2"
  type: "Convolution"
  bottom: "pool1"
  top: "conv2"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  convolution_param {
    num_output: 50
    kernel_size: 5
    stride: 1
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "pool2"
  type: "Pooling"
  bottom: "conv2"
  top: "pool2"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "ip1"
  type: "InnerProduct"
  bottom: "pool2"
  top: "ip1"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  inner_product_param {
    num_output: 500
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  # ReLU 单元比原版的 Sigmoid 有更好的收敛效果
  name: "relu1"
  type: "ReLU"
  bottom: "ip1"
  top: "ip1"
}
layer {
  name: "ip2"
  type: "InnerProduct"
  bottom: "ip1"
  top: "ip2"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  inner_product_param {
    num_output: 10
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
# Accuracy 层值由于验证/测试阶段，用于计算分类的准确率。
layer {
  name: "accuracy"
  type: "Accuracy"
  bottom: "ip2"
  bottom: "label"
  top: "accuracy"
  include {
    phase: TEST
  }
}
layer {
  name: "loss"
  type: "SoftmaxWithLoss"
  bottom: "ip2"
  bottom: "label"
  top: "loss"
}
```

<span style="color:red;">
有很多想知道的：
</span>
<span style="color:red;">
1. 每个 layer 有多少种 type？
2. 而且，为什么第一个 layer 有两个top？top 和bottom 是什么意思？
3. name 是用来做什么的？
4. include { phase: TRAIN} 是什么意思？不同的 phase 有什么不同吗？
5. 为什么 验证阶段也放在里面了？验证阶段的 layer 在整个 网络中是出于什么位置？
6. 每个卷积层的两个 param 的 lr_mult 是什么意思？为什么偏置还有学习率？卷积核的学习率又要怎么定？
7. weight_filler 有多少种方式？ xavier 是现在普遍使用的方式吗？要总结下。
8. InnerProduct 是什么层？
9. Accuracy 是什么层？
10. SoftmaxWithLoss 这个层可以自定义吗？
11. 对整个这些层的连接和运转还是有些不清楚。
</span>

每一层的参数意义已经写在了注释中。另外就是引入了 TEST 的数据层，有专门用于验证的数据 val_lmdb。

OK，除了网络结构和数据，我们还需要配置一个 lenet_solver.prototxt：

```prototxt
# The train/validate net protocol buffer definition
net: "lenet_train_val.prototxt"

# test_iter 用于指定 test 执行的时候的迭代次数
# 在我们的例子中，test 的batch size 是 100，而 val_lmdb 中的数据总量是 10000
# 我们希望每次测试都能够遍历全部 val_lmdb 中的数据，所以 test_iter 定为 100
test_iter: 100

# 指定每训练多少次执行一次 test
test_interval: 500

# The base learning rate, momentum and the weight decay of the network.
base_lr: 0.01
momentum: 0.9
weight_decay: 0.0005

# 采用 inv 的学习策略，lr=base_lr*(1+gamma*iter)^(-power)
lr_policy: "inv"
gamma: 0.0001
power: 0.75

# 每迭代多少次显示一次当前训练的信息，主要是 loss 和学习率。
display: 100

# 指定最大的迭代次数
max_iter: 36000

# 每迭代多少次保存一次模型的参数和训练状态
snapshot: 5000
snapshot_prefix: "mnist_lenet"

# 使用 GPU 还是 CPU 求解
solver_mode: GPU
```

<span style="color:red;">
想要知道的：
</span>
<span style="color:red;">
1. `weight_decay` 这个是什么？
2. 什么是 `inv` 的学习策略？`lr=base_lr*(1+gamma*iter)^(-power)` 是什么？
3. 为什么要保存模型的参数和训练状态？这个之前就有这个疑问。
4. 对于这种 solver.prototxt ，想要知道更多可以配置的选项，要好好总结下。
</span>


本例和Caffe的官方例子区别不大，除了迭代次数有所变化之外。更多 Solver 的详细内容可以参考 Caffe 官网 http://caffe.berkeleyvision.org/tutorial/solver.html 。<span style="color:red;">嗯。</span>

OK，现在万事俱备，调用下面命令就可以进行训练了。

```
/path/to/caffe/build/tools/caffe train -solver lenet_solver.prototxt -gpu 0 -log_dir ./
```

或者双短线开头的参数命令：

```
/path/to/caffe/build/tools/caffe train -solver=lenet_solver.prototxt --gpu=0 --log_dir=./
```

不过因为第二种方式无法使用终端的自动补全，所以没有第一种方式方便。<span style="color:red;">柑橘二用这种双短线的参数命令更清晰一些，不知道普遍使用的是什么？无法使用终端的自动补全是什么意思？</span>

上面的额 `gpu` 参数是指定要用哪块 GPU 训练（如果有多块的话，比如一台多卡GPU服务器），如果确实需要，可以用 `-gpu all` 参数对所有卡进行训练。`log_dir` 参数指定输出 log 文件的路径，前提是这个路径必须提前存在。<span style="color:red;">嗯，这个 log 的路径必须提前存在。</span>

执行命令后，得到如下输出，并且同步在log中。

![mark](http://images.iterate.site/blog/image/180901/1c8m2kmDja.png?imageslim)

注意因为指定了 TEST的数据层，所以输出里按照 solver 中指定的间隔会输出当前模型在 val_lmdb 上的准确率和 loss。

训练完毕就会生成几个以 caffemodel 和 solverstate 结尾的文件，这个就是模型参数和 solver 状态在指定迭代次数以及训练结束时的存档，名字前缀就是在lenet_solver.prototxt中指定的前缀。<span style="color:red;">为什么要进行存档？是有什么用处吗？</span>

当然同时生成的还有 log 文件，命名是：

```
caffe.［主机名］.［域名］.［用户名］.log. INFO.［年月日］-［时分秒］.［微秒］
```

的形式，比如 `caffe.localhost.localdomain.dlcv.log.INFO.20170107-144322.132282`。<span style="color:red;">看起来这个 log 可以存在一个指定的 server 上吗？怎么做？而且，这种训练的 log 一般都是怎么处理的？一般存放在哪里？</span>Caffe 官方也有提供可视化 log 文件的工具，在 `caffe\tools\extra` 下有个 `plot_training_log.py.example`, 把这个文件复制一份命名为 `plot_training_log.py`，就可以用来画图，这个脚本的输入参数分别是：图的类型、生成图片的路径和 log 的路径。其中图片类型的输入和对应类型如下。


- 0:测试准确率 vs. 迭代次数
- 1:测试准确率 vs. 训练时间（秒）
- 2:测试loss vs. 迭代次数
- 3:测试loss vs. 训练时间（秒）
- 4:学习率 vs.迭代次数
- 5:学习率 vs.训练时间（秒）
- 6:训练loss vs.迭代次数
- 7:训练loss vs.训练时间（秒）

另外，这个脚本要求 `log` 文件必须以 `.log` 结尾。我们用 `mv` 命令把 `log` 文件名改成 `mnist_train.log`，比如想看看测试准确率和测试的 loss 随迭代次数的变化，依次执行：

```
python plot_training_log.py 0 test_acc_vs_iters.png mnist_train.log
python plot_training_log.py 2 test_loss_vs_iters.png mnist_train.log
```

<span style="color:red;">感觉这种用法还很新奇的，但是想想有很合理，从 log 中拿到训练阶段的信息，进行画图，来描述整个的训练过程，感觉还是挺合理的。不知道 Tensorflow 和 MXNet 是怎么对训练的过程进行图像描述的，不知道是不是也是使用的 log 。</span>

得到如图 8-2 所示的两个曲线，注意这里为了方便可视化，在窗口上做了局部放大。

![mark](http://images.iterate.site/blog/image/180901/ddC5l8K189.png?imageslim)

<span style="color:red;">不知道还有没有别的工具可以来处理 Caffe 的 log 的。</span>



## 测试和评估

### 测试模型准确率

训练好模型之后，就需要对模型进行测试和评估了。其实在训练过程中，每迭代 500 次，就已经在 val_lmdb 上对模型进行了准确率的评估。不过 MNIST 除了验证集外还有一个测试集，对于数据以测试集为准进行评估。

之前，我们的 test_lmdb 已经建好了，所以，只需要把 lenet_train_val.prototxt 中 TEST 对应的数据层中的路径，从 val_lmdb 的路径换成 test_lmdb 就可以；或者也可以新建个 lenet_test.prototxt，其中的数据层如下，其他层不变。

```prototxt
name: "LeNet Test"
layer {
  name: "mnist"
  type: "Data"
  top: "data"
  top: "label"
  include {
    phase: TEST
  }
  transform_param {
    mean_value: 128
    scale: 0.00390625
  }
  data_param {
    source: "../data/test_lmdb"
    batch_size: 100
    backend: LMDB
  }
}
layer {
  name: "conv1"
  type: "Convolution"
  bottom: "data"
  top: "conv1"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  convolution_param {
    num_output: 20
    kernel_size: 5
    stride: 1
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "pool1"
  type: "Pooling"
  bottom: "conv1"
  top: "pool1"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "conv2"
  type: "Convolution"
  bottom: "pool1"
  top: "conv2"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  convolution_param {
    num_output: 50
    kernel_size: 5
    stride: 1
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "pool2"
  type: "Pooling"
  bottom: "conv2"
  top: "pool2"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "ip1"
  type: "InnerProduct"
  bottom: "pool2"
  top: "ip1"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  inner_product_param {
    num_output: 500
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "relu1"
  type: "ReLU"
  bottom: "ip1"
  top: "ip1"
}
layer {
  name: "ip2"
  type: "InnerProduct"
  bottom: "ip1"
  top: "ip2"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  inner_product_param {
    num_output: 10
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "accuracy"
  type: "Accuracy"
  bottom: "ip2"
  bottom: "label"
  top: "accuracy"
  include {
    phase: TEST
  }
}
```

OK，接下来就可以进行测试了，比如想测试一下最后一个 mnist_lenet_iter_36000.caffemodel，可在终端输入下面命令：<span style="color:blue;">OKOK，看到了这个，我才知道他为什么中间要保存一些模型，因为，并不是最后的模型是最好的，可能中间已经过拟合了，因此，我们可以通过上面的 log 的曲线找到我们认为的最好的一个模型。嗯，不错。</span>

```
/path/to/caffe/build/tools/caffe test -model lenet_test.prototxt -weights mnist_aug_lenet_iter_36000.caffemodel -gpu 0 -iterations 100
```

和训练不同的是，第一个输入参数从 `train` 变成了 `test`，然后通过 `-model` 参数指定 `lenet_test.prototxt` 作为测试的模型和数据，`-weights` 用来从一个 `caffemodel` 文件中读取参数 的值，`-gpu` 用来指定测试 GPU 的序号，最后的参数 `-iterations` 和 solver 中的 `test_iter` 意思相似，`iterations` 和 `batch_size` 相乘是最终测试的样本量，这个值默认是 50，所以这里要显式地指定为 100 好遍历所有测试数据。执行后输出如下：

![mark](http://images.iterate.site/blog/image/180901/LDhAm5IFCK.png?imageslim)

程序中的每个 batch 的准确率都进行了计算，最后得到一个总的准确率。对于本书的例子，生成的模型存档数量不多，对照验证数据 loss 小、准确率高的区域，手动运行所有模型就可以挑选一个最优的模型。如果是模型存档很多的情况下，利用测试集挑选模型，最好自己写成脚本来比较所有模型中最好的一个。<span style="color:red;">嗯，也是哦，即使验证集能说明某几个模型是好的，但是测试集还是有必要把所有的模型都测试一遍的，然后总结进行选择。这种脚本要怎么写？ `os.system` 可不可以？</span>

在数据不是很充裕的情况下，很可能手头并没有一个专门的测试数据集，而是只有训练和验证集，或者说验证集和测试集合二为一。这种情况下，挑选模型就是个经验活，一般而言，数据越多，验证集 loss 最小的和准确率最高的就越有可能是一个，如果不是一个， 通常选 loss 最小的泛化性能会好一些。<span style="color:red;">对于这个地方的模型挑选，再详细一些，要自己尝试一些，在补充一些。</span>

其实，无论是训练集、验证集还是测试集，其实都是对真实分布的采样，所以谁知道哪个模型才是真正最优的呢？只是在大数据量上挑出的模型比小数据量上挑出的模型更有信心而已。<span style="color:red;">嗯，可以说大数据量上的模型比小数据量上的模型好的概率更大吧。</span>

### 评估模型性能

<span style="color:red;">模型的性能还要评估吗？</span>

评估模型性能一般来说主要是评估速度和内存占用。在 Caffe 中这件事情也很简单，只要有描述模型网络结构的 prototxt 文件就可以，因为支持评估计算性能，所以不需要参数。可以直接用 `caffe/example/mnist` 下 `lenet.prototxt` 作为评估的结构，在终端输入：


```
/path/to/caffe/build/tools/caffe time -model lenet.prototxt -gpu 0
```

得到输出如下：


![mark](http://images.iterate.site/blog/image/180901/l922BfdeKI.png?imageslim)
![mark](http://images.iterate.site/blog/image/180901/Cmeh7CcDEE.png?imageslim)
![mark](http://images.iterate.site/blog/image/180901/63kh6cEB8H.png?imageslim)
![mark](http://images.iterate.site/blog/image/180901/lFgeGf6J2H.png?imageslim)

<span style="color:red;">要自己跑一下看看。</span>

可以看到笔者的 GTX980M 运行一次前向计算不到 1 毫秒。另外这里也统计了批数量为 64 的时候数据需要的内存，不过需要注意的是，这里只是对数据部分的估算，部署的时候以此为准是不靠谱的，还是需要实际做过压力测试才知道。<span style="color:red;">为什么这样的是不靠谱的？主要关注那些指标？实际的压力测试要怎么做？如果压力测试不达标要怎么做？这个测试与什么有关系？硬件？底层运算库有关系吗？</span>

如果在执行命令的时候去掉 `-gpu` 选项：

```
/path/to/caffe/build/tools/caffe time -model lenet.prototxt
```

则会测试 CPU 下的执行效率，比如笔者计算机的 CPU 是 i7-5500U，底层矩阵运算库是 atlas , 运行一次前向计算需要 26 毫秒。

有人也许会问为什么还要关注 CPU，明明是 GPU 快了一个量级还多啊？事实上虽然训练模型阶段几乎已经被 NVIDIA 的 GPU 统治了，但是部署一个应用的时候 GPU 除了快，还有不灵活的数据交换和过高的功耗等特点。另外再加上基于 CPU 架构下的程序部署已经非常成熟并且灵活，所以在很多大型公司里，训练用 GPU, 预测阶段用 CPU 是很常见的。甚至为了更好的能耗比，在部署阶段可考虑用可编程逻辑阵列芯片(FPGA)以及专用集成电路芯片(ASIC)。<span style="color:red;">是这样吗？这个真的是新的信息，我现在才知道原来预测的时候并不是都使用的 GPU 。首先，我想知道，什么是不灵活的数据交换？过高的功耗要考虑吗对于普通的公司？基于 GPU 的程序部署与基于 CPU 的程序部署有什么区别吗？难道从软件上有区别？我之前一直认为是没有什么区别的，感觉只是一个参数的问题。而且，我想知道怎么部署到 FPGA 和 ASIC 上面？这还是要总结下的。现在普遍是部署到什么上面的？而且服务器的维护是自己的服务器呢还是云服务器？</span>


## 识别手写数字

有了训练好的模型，就可以用来识别手写数字了。我们测试用的是 test 数据集的图片和之前生成的列表，基于 Python 接口来实现：

recognize_digit.py：

```python
import sys
sys.path.append('/path/to/caffe/python')
import numpy as np
import cv2
import caffe

# 均值和缩放系数
MEAN = 128
SCALE = 0.00390625

# 文件列表作为输入的参数
imglist = sys.argv[1]

# 设置 GPU 模式运行
caffe.set_mode_gpu()
# 使用第一块 GPU
caffe.set_device(0)

# 创建 net
net = caffe.Net('lenet.prototxt', 'mnist_lenet_iter_36000.caffemodel', caffe.TEST)
net.blobs['data'].reshape(1, 1, 28, 28)

with open(imglist, 'r') as f:
    line = f.readline()
    while line:
        imgpath, label = line.split()
        line = f.readline()
        # 读取图片并减去均值 128
        image = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE).astype(np.float) - MEAN
        image *= SCALE
        # 和 lenet_train_val.prototxt 保持一致，乘以 0.0390625
        net.blobs['data'].data[...] = image
        output = net.forward()
        pred_label = np.argmax(output['prob'][0])
        print('Predicted digit for {} is {}'.format(imgpath, pred_label))

```

<span style="color:red;">
想要知道的：
</span>
<span style="color:red;">
1. `net = caffe.Net('lenet.prototxt', 'mnist_lenet_iter_36000.caffemodel', caffe.TEST)` 还是要好好总结下的。
2. `net.blobs['data'].reshape(1, 1, 28, 28)` 看来关于 caffe.Net 还是要好好总结下的，如果不是真的理解，那么根本不知道这里该怎么写，该写什么。
3. `image = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE).astype(np.float) - MEAN` 看来对 python 的 OpenCV 还是要好好整理的，要明确每一步得到的数据类型，以及数据内容，以及可以进行什么操作，可以转化成什么类型。这样你才能有底气对这个数据进行处理。
4. `net.blobs['data'].data[...] = image` 这个 `...` 一直没有怎么总结，一直都不是很明白这个指的是什么。
5. `pred_label = np.argmax(output['prob'][0])` 这个 `np.argmax` 还是有点不是很熟悉的，虽然我知道他是用来获得最大的数的 index 的。不过还是要更详细的理解。
</span>

需要提一下的是 lenet.prototxt，开头几行和第7章中讲的对数据形状的定义不一样。

```prototxt
name: "LeNet"
layer {
  name: "data"
  type: "Input"
  top: "data"
  input_param {
    shape: {
      dim: 64
      dim: 1
      dim: 28
      dim: 28
    }
  }
}
layer {
  name: "conv1"
  type: "Convolution"
  bottom: "data"
  top: "conv1"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  convolution_param {
    num_output: 20
    kernel_size: 5
    stride: 1
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "pool1"
  type: "Pooling"
  bottom: "conv1"
  top: "pool1"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "conv2"
  type: "Convolution"
  bottom: "pool1"
  top: "conv2"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  convolution_param {
    num_output: 50
    kernel_size: 5
    stride: 1
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "pool2"
  type: "Pooling"
  bottom: "conv2"
  top: "pool2"
  pooling_param {
    pool: MAX
    kernel_size: 2
    stride: 2
  }
}
layer {
  name: "ip1"
  type: "InnerProduct"
  bottom: "pool2"
  top: "ip1"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  inner_product_param {
    num_output: 500
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "relu1"
  type: "ReLU"
  bottom: "ip1"
  top: "ip1"
}
layer {
  name: "ip2"
  type: "InnerProduct"
  bottom: "ip1"
  top: "ip2"
  param {
    lr_mult: 1
  }
  param {
    lr_mult: 2
  }
  inner_product_param {
    num_output: 10
    weight_filler {
      type: "xavier"
    }
    bias_filler {
      type: "constant"
    }
  }
}
layer {
  name: "prob"
  type: "Softmax"
  bottom: "ip2"
  top: "prob"
}
```

从一个单纯的形状定义变成了一个简单的 Input 层。这是后来在 Caffe 中加入的方式， 应该说这才是比较推崇的方式，因为数据也抽象成了一个层，而不是一种特殊的定义。<span style="color:red;">Input 层也要总结下。</span>

OK，我们运行脚本：

```
python recognize_digit.py test.txt
```

得到如下的输出，对于前几行而言，结果还是很准的：

![mark](http://images.iterate.site/blog/image/180901/B6eCJ98bm5.png?imageslim)




## 进行数据增强。

我们使用前面准备好的数据增强后混合的数据进行训练。

我们要把 lenet_solver.prototxt 中的 net 改成 lenet_train_val_aug.prototxt， snapshot_prefix 改为 mnist_aug_lenet，然后其他参数维持不变就可以训练了。训练结束后把 log 文件命名为 mnist_with_augmentation.log，然后用 plot_training_log.py 画出两个训练的对比如下：

```
python plot_training_log.py 0 test_acc_vs_iters.png mnist_train.log mnist_train_with_augmentation.log
python plot_training_log.py 2 test_loss_vs_iters.png mnist_train.log mnist_train_with_augmentation.log
```

<span style="color:red;">没想到还可以这样对比，样本的数量不同呀，怎么对比的？</span>

输出结果如图8-3所示。


![mark](http://images.iterate.site/blog/image/180901/96c4jh9LJK.png?imageslim)

从验证集来看，增加扰动数据后的指标还是有提升的，loss 在训练后期明显比原始数据集低，准确率最高达到了 99.27%，提高了约 0.3%。不过收敛速度比原始数据要慢，并且到了 36000 次迭代的时候仍然很不稳定。这是因为原始训练数据只有 5 万张，每个 batch 里 50 个数据的情况下，迭代 1000 次就是一代（epoch），从图8-3中看，超过20代之后 就已经比较稳定了。而增加后的数据总量是 30 万，迭代 6000 次才是一代，到了 36000 次 结束时，才迭代了 6 代。那么如果希望接着 36000 次的状态继续训练呢？比如继续训练到 20 代，也就是 12 万次的时候，那么需要到 solver 文件中将 `max_iter` 的值改为 120000，然后执行如下命令就能接着 36000 次的状态存档继续训练。<span style="color:red;">嗯，是的，不过已经可以感觉到这个增加扰动数据之后，效果的确提升了比较多。</span>

```
/path/to/caffe/build/tools/caffe train -solver lenet_solver.prototxt -snapshot mnist_aug_lenet_iter_36000.solverstate -gpu 0
```

最后得到的loss和准确率随训练的曲线如图8-4所示，可以看到 loss 还在缓慢下降， 最高的验证集准确率超过了 93%。

![mark](http://images.iterate.site/blog/image/180901/Cem0aicC6D.png?imageslim)

最后还要提一下的是，直接在样本基础上做扰动增加数据只是数据增加的方法之一，并且不是一个好的方案，因为增加的数据量有限，并且还要占用原有样本额外的硬盘空间。最好的办法是训练的时候实时对数据进行扰动，这样等效于无限多的随机扰动。<span style="color:red;">哇，厉害！这个要怎么做？</span>

其实 Caffe 的数据层已经自带了最基础的数据扰动功能，不过只限于随机裁剪和随机镜像，并不是很好用。Github 上有一些开源的第三方实现的实时扰动的 Caffe 层，会包含各种常见的数据扰动方式，只需要到 github 的搜索框里搜 caffe augmentation 就能找到很多，这里就不展开讲了。<span style="color:red;">嗯，要总结下。</span>






## 相关资料

- 《深度学习与计算机视觉》
