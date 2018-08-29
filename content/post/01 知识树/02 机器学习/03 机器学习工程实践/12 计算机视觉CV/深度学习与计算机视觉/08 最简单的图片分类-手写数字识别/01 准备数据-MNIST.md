---
title: 01 准备数据-MNIST
toc: true
date: 2018-08-29
---
##### 第8章最简单的图片分类_手写数字识别

在第4章已经提到过，卷积神经网络的第一代成功应用是在手写数字识别上，用的网 络是LeNet-5。如今在实际应用中已经很少看到LeNet-5的身影了，不过这个经典的结构成 了图片分类中的Hello Worldo几乎所有深度学习框架中都有用LeNet-5在MNIST数据集 上训练做手写数字识别的例子，甚至很多人测试一个框架是否安装好，用的就是训练 LeNet-5的脚本。

本章就一步步通过这个图片分类的Hello World来了解基于Caffe和MXNet做图片分

类的基本方法。

8.1准备数据——MNIST

在大多数框架的例子中，用MNIST训练LeNet-5的例子都被脚本高度封装了。只需要 执行脚本就可以完成从下载数据到训练的过程。比如在MXNet中，直接到mxnet/example 下执行train mnist.py就大功告成了，Caffe中也有类似的shell脚本。其实这样是不利于初 学者了解到底发生了什么的。所以本书把数据准备的部分剥离开来，把每个训练都具体到 -张图片，然后从头开始完整地过一遍流程。了解了这个流程，基本上就了解了如何从图

片数据开始到训练一个模型进行分类。

8.1.1 下载 MNIST

原版MNIST下载的很慢，本书中用的MNIST是Bengio组封装好的数据包，下载地 址为 [http://deeplearning.net/data/mnist/mnist.pkl.gz](http://deeplearning.net/data/mnist/mnist.pkl.gz%e3%80%82)[。](http://deeplearning.net/data/mnist/mnist.pkl.gz%e3%80%82)

在Linux下直接用wget即可：

\>> wget <http://deeplearning.net/data/mnist/mriist.pkl.gz>

本书的github仓库中第8章的文件夹下也有提供该文件的下载脚本。

8.1.2生成MNIST的图片

mnist.pkl.gz这个压缩包中其实是数据的训练集、验证集和测试集用pickle导出的文件 被压缩为gzip格式，所以用python中的gzip模块当成文件就可以读取。其中每个数据集 是一个元组，第一个元素存储的是手写数字图片，表示每张图片是长度为28x28=784的一 维浮点型munpy数组，这个数组就是单通道灰度图片按行展开得到，最大值为1,代表白 色部分，最小值为0,代表黑色部分。元组中第二个元素是图片对应的标签，是一个• -维 的整型numpy数组，按照下标位置对应图片中的数字。基于以上将数据集转换成图片的代 码如下：

import os

import pickle, gzip

from matplotlib import pyplot

林从原始文件读取MNIST数据

print(* Loading data from mnist.pkl.gz . . . * ) with gzip.open(*mnist.pkl.gz *,    'rb*) as f:

train_set, valid_set, test_set = pickle.load(f)

\# 创建mnist文件夹 imgs_dir =    *mnist *

os.system('mkdir -p {}*.format(imgs_dir))

datasets =    {'train': train_set, 1val*: valid_set, 'test': test_set}

\#转换train、val和test数据集_

for dataname, dataset in datasets.items():

print(* Converting { } dataset ...*.format(dataname)) data_dir = os.sep.join([imgs_dir, dataname])

\#在mnist文件夹下创建对应子文件夹

os.system(* mkdir -p {}*.format(data_dir))

\# i代表数据的序号，用zip ()函数读取对应位置的图片和标签 for i, (img, label) in enumerate(zip(*dataset)):

\#格式化生成文件的名字，第一个字段是序号，第二个字段是数字值

filename =    *{:0>6d}_{}.jpg *.format(i, label)

filepath = os.sep.j oin([data_dir, filename])

\#将展开的一维数组还原为二维图像

img = img.reshape((28,    28))

7    #用pyplot保存可以自动归一化生成像素值在0〜255之间的灰度图片

pyplot.imsave(filepath, img, cmap= * gray') if (i+1)    %    10000 == 0:

print (*{} images converted!*.format (i + 1))

这个脚本首先创建了一个叫mnist的文件夹，然后在mnist下创建3个子文件夹train、 val和test,分别用来保存对应的3个数据集转换后产生的图片。每个文件的命名规则为第一 个字段是序号，第二个字段是数字的值，保存为JPG格式。一些图片的例子如图8-1所示。

H    回    D    B    B    D

000000_7.jpg    000001_2jpg    000002_l.jpg    000003_0.jpg    000004_4.jpg    000005_l.jpg

##### B    □    B    B    B    BI

000006_4.jpg    000007_9.jpg    000008_5.jpg    000009_9.jpg    000010_0.jpg    000011_6.jpg

图8-1 MNIST图片例子

8.2基于Caffe的实现

本节讲解如何基于Caffe和LeNet-5训练一个用于手写数字识别的模型，并对模型进 行评估和测试。

8.2.1制作LMDB数据

LMDB是Caffe中最常用的一种数据库格式，全称Lightning Memory-Mapped Database,直译就是闪电般快速的内存映射型数据库。除了快，LMDB还支持多程序同时 对数据进行读取，这是相比Caffe更早支持的LevelDB的优点。现在LMDB差不多是Caffe 用来训练图片最常用的数据格式。

Caffe提供了专门为图像分类任务将图片转换为LMDB的官方工具，路径为 caffe/build/tools/convert_imageseto要使用这个工具，第一部是生成一个图片文件路径的列 表，每一行是文件路径和对应标签(的下标)，用space键或者制表符(Tab)分开，格式例 子如下：

mnist_images/val/000000_3.jpg 3 mnist_images/val/000001_8.jpg 8 mnist_images/val/000002_6.jpg 6

在8.1节中已经在mnist文件夹下生成了 3个文件夹，分别是train、val和test，分别 包含训练图片、验证图片和测试图片。接下来要把这些图片的路径和对应标签，也就是数 字的值转化为上面的格式，因为文件名字中下画线分开的第2个字段就是标签，所以用如 下代码可以实现。

import os import sys

\#输入路径，是包含mnist图片文件的路径 input_path = sys.argv[l].rstrip(os.sep)

\#输tS的文件名，内容就是图片路径-标签的列表 output_path = sys.argv[2]

\#列出論入路径下所有的文件名 filenames = os.listdir(input_path) with open (output_path, ' w *) as f:

for filename in filenames:

\#完整的图片文件路径

filepath = os.sep.j oin([input_pathf filename])

\#第2个字段的值就是标签

label = filename [: filename . rfind (*.*)]. split () [1]

\#生成路径-标签的格式并写入文件

line =    *{}    {}\nformat(filepath, label)

f.write(line)

把这个文件保存为gen_caffe_imglist.py,然后在控制台下依次执行下面命令：

\>> python gen_caffe_imglist.py mnist/train train.txt

» python gen_caffe_imglist.py mnist/val val.txt

» python gen_caffe_imglist.py mnist/test test.txt

这样就生成了 3个数据集的文件列表和对应标签。然后直接调用convert_imageset就 可以制作lmdb 了。

\>> /path/to/caffe/build/tools/convert_imageset . / train.txt train_lmdb

--gray ——shuffle

\>> /path/to/caffe/build/tools/convert_imageset . / val.txt val_lmdb

——gray ——shuffle

» /path/to/caffe/build/tools/convert_imageset ./ test.txt test一lmdb

——gray --shuffle

其中-gray是单通道读取灰度图的选项，--shuffle是个常用的选项，作用是打乱文件列 表顺序，但是在本例中其实是可有可无的，因为本来就是乱序的。执行这个工具其实就是 读取图片为OpenCV的Mat,然后保存到lmdb里。更多convert imageset的用法可以执行 下面命令或者参考源码：

» /path/to/caffe/built/tools/convert_imageset -h

8.2.2 训练 LeNet-5

本书采用的结构和Caffe官方例子的版本没有区别，只是输入的数据层变成了我们自

己制作的LMDB,用于描述数据源和网络结构的lenet train val.prototxt如下：

name: "LeNet" layer {

name: "mnist" type: "Data" top: "data" top: "label" include {

phase: TRAIN

}

\#数据层的参数，指定均值和缩放比例，数据会先减去mean_value然后乘上scale

\#具体到mnist图片，就是把0〜255之间的值缩放到-0.5〜0.5,帮助收敛 transform_param {

mean_value:    128

scale:    0.00390625

}

\#指定训练阶段的数据，每次迭代用50个样本 data_param {

source:    "../data/train_lmdb"

batch_size:    50

backend: LMDB

}

}

layer {

name: "mnist" type: "Data” top: "data" top: "label" include {

phase: TEST

}

transform_param { mean_value:    128

scale:    0.00390625

}

\#指定验证阶段的数据，每次计算100个 data_param {

source:    " . . /data/val_lmdt>"

batch_size:    100

backend: LMDB

}

}

layer {

name: "convl"

type:    "Convolution"

bottom: "data"

top:    "convl"

\#卷积核的学习率为基础学习率乘以lr_nmlt param {

\# weight_filler用于初始化参数，xavier是一种初始化方法，源于Bengio组2010年论文 # 《Understanding the difficulty of training deep feedforward

neural networks》

weight_filler {

type:    "xavier"

}

bias_filler {

type: "constant"

}

}

}

layer {    <

\#在卷积层后接Pooling层，这种用法已经在第4章讲过

name: "pooll"

type: "Pooling"

bottom: "convl”

top: "pooll"

pooling_param {

pool: MAX kernel_size:    2

stride:    2

}

}

layer {

name: "conv2" type:    "Convolution"

bottom: "pooll" top: "conv2" param {

weight_filler {

type: "xavier"

}

bias_filler {

type: "constant"

}

}

layer {

name: "pool2" type: "Pooling" bottom: "conv2” top: "pool2'’ pooling_param {

pool: MAX kernel_size:    2

stride:    2

}

}

layer {

name: "ipl"

type: "InnerProduct”

bottom: "pool2"

top: "ipl"

param {

weight_filler {

type: "xavier"

}

bias_filler {

type: "constant**

}

}

}

layer {

\# ReLU单元比起原版的Sigmoid有更好的收敛效果

name: "relul"

type:    "ReLU"

bottom: "ipl"

top: "ipl"

}

layer {

weight_filler {

type: "xavier"

}

bias_filler {

type: "constant"

}

}

}

\# Accuracy层只用在验证/测试阶段，用于计算分类的准确率

layer {

name: "accuracy" type: "Accuracy" bottom: "ip2” bottom: "label" top: "accuracy" include {

phase: TEST

}

}

layer {

name: ’’loss"

type: "SoftmaxWithLoss"

bottom: "ip2n

bottom: "label"

top: "loss"

}

和第7章的例子比起来，本例中又增加了卷积层和池化层，每•层的参数意义已经写 在了洋释中。另外就是引入了 TEST的数据层，有专门用于验证的数据valjmdb。除了网 络结构和数据，还需要像第7章中的例子一样配置一个lenet solver.prototxt□

net:    '* lenet_train_val. prototxt"

\#    于指是test执行的时候的迭代次数

\#在我听的例子中，test的batch size是100,而val_lmdb中的数据总量是10000

林我们希望每次测试都能够遍历全部val_lmdb中的数据，所以test_it參r定为100

momentum: 0.9

weight_decay:    0.0005

\#    采用 inv 的学习策略，lr = base_lr *    (1    + gamma * iter) A (- power)

\#    每种策略的计算方法可以参考caf fe/src/caf fe/proto/caffe .proto lr_policy: "invn

gamma:    0.0001

power:    0.75

\#每迭代多少次显示一次当前训练的信息，主要是loss和学习率 display: 100 #指定最大迭代次数 max_iter:    36000

\#每迭代多少次保存一次模型的参数和训练状态

snapshot:    5000

snapshot_prefix: "mnist—lenet"

\#这个例手利用GPU求解 solver_mode: GPU

本例和Caffe的官方例子区别不大，除了迭代次数有所变化之外。更多Solver的详细 内容可以参考 Caffe 官网 <http://caffe.berkeleyvision.org/tutorial/solver.htmlo>

现在万事俱备，调用下面命令就可以进行训练了。

» /path/to/caffe/build/tools/caffe train -solver lenet_solver.prototxt

-gpu 0 -log_dir . /

或者双短线开头的参数命令：

» /path/to/caffe/build/tools/caffe train -solver=lenet_solver.prototxt

--gpu=0 --log_dir=./

不过因为第二种方式无法使用终端的自动补全，所以没有第一种方式方便。在这个训

练命令中，相比起第7章的例子又多了-gpu和-log_dir的选项，其中gpu参数是指定要用 哪块GPU训练（如果有多块的话，比如一台多卡GPU服务器），如果确实需要，可以用

-gpu all参数对所有卡进行训练。log_dir参数指定输出log文件的路径，前提是这个路径必 须提前存在。执行命令后，得到如下输出，并且同步在log中。

10107

10107

10107

inv

13:50:57.542906

13:50:57.542917

13:50:57.542935

131455 caffe.cpp:219] Starting Optimization 131455 solver.cpp:279] Solving LeNet 131455 solver.cpp:280] Learning Rate Policy:

10107    13:50:57.543421

net (#0)

10107    13:50:58.501360

\#0 : accuracy =    0.0915

10107    13:50:58.501461

\#1: loss = 2.34842 10107    13:50:58.512187

2.3351

131455 solver.cpp:337]

131455 solver.cpp:404]

131455 solver.cpp:404 ]

(*    1    = 2.34842 loss)

131455 solver.cpp:228]

| Iteration | 0,   | Testing |
| --------- | ---- | ------- |
| Test      | net  | output  |
| Test      | net  | output  |
| Iteration | 0,   | loss =  |

Train net output

10107    13

\#0: loss

50

58.512253 2.3351    (*

10107    13:50:58.512293

0.01

10107    13:50:59.664911

0.306985

10107    13:51:03.086341

0.125596

10107    13:51:03.086414

\#0: loss = 0.125596 10107    13:51:03.086434

=0.00971013 10107    13:51:04.223389

net (#0)    .

10107    13:51?05.157244

\#0: accuracy =    0.972

10107    13:51:05.157322

131455 solver.cpp:244] 1    =    2.3351 loss)

| 131455                | sgd_solver.cpp:                              |
| --------------------- | -------------------------------------------- |
| 131455                | solver.cpp:228]                              |
| 131455                | solver.cpp:228]                              |
| 131455 ：* 1 = 131455 | solver.cpp:244]0.125596 loss) sgd solver.cpp |
| 131455                | solver.cpp:337]                              |
| 131455                | solver.cpp:404]                              |
| 131455                | solver.cpp:404]                              |

16] Iteration 0, lr =

Iteration 100, loss =

Iteration 400, loss =

| Train net output       |         |
| ---------------------- | ------- |
| 106] Iteration 400, lr |         |
| Iteration 500,         | Testing |
| Test net               | output  |
| Test net               | output  |

\#1: loss = 0.0923853 10107 13:51:05.168064 0.0740159

10107 13:51:05.168099 #0: loss = 0.074016

(*    1    =    0.0923853 loss)

131455 solver.cpp:228] Iteration 500, loss =

131455 solver.cpp:244]    Train net output

(*    1    =    0.074016 loss)

注意因为指定了 TEST的数据层，所以输出里按照solver中指定的间隔会输出当前模 型在val lmdb上的准确率和loss。训练完毕就会生成几个以caffemodel和solverstate结尾 的文件，这个就是模型参数和solver状态在指定迭代次数以及训练结束时的存档，名字前 缀就是在lenet_solver.prototxt中指定的前缀。当然同时生成的还有log文件，命名是：

caffe.［主机名］.［域名］.［用户名］.log. INFO.［年月日］-［时分秒］.［微秒］

的形式，t匕如 caffe.localhost.localdomain.dlcv.log.INFO.20170107-144322.132282。Caffe 官 方也有提供可视化log文件的工具，在caffe\tools\extra下有个plot training log.py.example, 把这个文件复制一份命名为plot_training_log.py，就可以用来画图，这个脚本的输入参数分 别是：图的类型、生成图片的路径和log的路径。其中图片类型的输入和对应类型如下。

| □ 0: | 测试准确率vs.迭代次数； |             |                     |
| ---- | ----------------------- | ----------- | ------------------- |
| □    | 1:                      | 测试准确率  | vs.训练时间（秒）； |
| □    | 2:                      | 测试loss vs | 迭代次数；          |

□    3:测试loss vs.训练时间（秒）；

□    4:学习率vs.迭代次数；

□    5:学习率vs.训练时间（秒）；

□    6:训练loss vs.迭代次数；

□    7:训练loss vs.训练时间（秒）。

另外，这个脚本要求log文件必须以.log结尾。我们用mv命令把log文件名改成 mnist_train.log,比如想看看测试准确率和测试的loss随迭代次数的变化，依次执行：

» python plot_training_log.py 0 test_acc_vs_iters.png mnist_train.log » python plot_training一log.py 2 test_loss_vs_iters.png mnist_train.log 得到如图8-2所示的两个曲线，注意这里为了方便可视化，在窗口上做了局部放大。

Test loss vs. Iters



5000    10000    15000    20000    25000    30000    35000

Iters

Test accuracy vs. Iters

S* 0.98

2

M

2 0.97

0.96

|      |      |                |
| ---- | ---- | -------------- |
|      |      |                |
|      | /    | mnist train \| |

5000    10000    15000    20000    25000    30000    35000

Iters

图8-2 Caffe自带工具生成的log可视化曲线

8.2.3测试和评估

1.测试模型准确率

训练好模型之后，就需要对模型进行测试和评估了。其实在训练过程中，每迭代500 次，就已经在valjmdb上对模型进行了准确率的评估。不过MNIST除了验证集外还有 一个测试集，对于数据以测试集为准进行评估。在8.2.1节中，testjmdb已经建好，所以 只需要把lenet_train_val.prototxt中TEST对应的数据层中的路径，从val lmdb的路径换 成test_lmdb就可以；或者也可以新建一个lenet_test.prototxt，其中的数据层如下，其他 层不变。

name: "LeNet Test" layer {

name: "mnist" type: "Data" top: "data" top: "label" include {

phase: TEST

transform_param { mean_value:    128

scale:    0.00390625

}

data_param {

source:    *'. . /data/test_lmdbn

batch_size:    100

backend: LMDB

}

}

这个例子文件在本书的github仓库中也可以找到。接下来就可以进行测试了，比如想

测试一下最后一个mnist_lenet_iter_36000.caffemodel,可在终端输入下面命令：

» /path/to/caffe/build/tools/caffe test -model lenet_test.prototxt -weights mnist_aug_lenet_iter_36000.caffemodel -gpu 0 -iterations 100

和训练不同的是，第一个输入参数从train变成了 test,然后通过-model参数指定 lenet test.prototxt作为测试的模型和数据，-weights用来从一个caffemodel文件中读取参数 的值，-gpu用来指定测试GPU的序号，最后的参数-iterations和solver中的test iter意思 相似，iterations和batch size相乘是最终测试的样本量，这个值默认是50，所以这里要显 式地指定为100好遍历所有测试数据。执行后输出如下：

10107    16:34:48.991080    134063 caffe.cpp:252] Running for 100

iterations.

| 101070.99          | 16:34:49.021505 | 134063 | caffe.cpp:275] | Batch      | 0,                | accuracy = |
| ------------------ | --------------- | ------ | -------------- | ---------- | ----------------- | ---------- |
| 10107              | 16:34:49.034065 | 134063 | caffe.cpp:275] | Batch 1,   | accuracy =    1   |            |
| 工 0107            | 16:34:49.046600 | 134063 | caffe.cpp:275] | Batch      | 2,                | accuracy = |
| 0.98               | /               |        |                |            |                   |            |
| 101070.99          | 16:34:49.061431 | 134063 | caffe.cpp:275] | Batch      | 3,                | accuracy = |
| ...中间部分省略... |                 |        |                |            |                   |            |
| 101070.99          | 16:34:50.022043 | 134063 | caffe.cpp:275] | Batch      | 97,               | accuracy = |
| 101070.98          | 16:34:50.034638 | 134063 | caffe.cpp:275] | Batch      | 98,               | accuracy = |
| 10107              | 16:34:50.047296 | 134063 | caffe.cpp:275] | Batch 99   | , accuracy =    1 |            |
| 10107              | 16:34:50.047312 | 134063 | caffe.cpp:280] | Loss:    0 |                   |            |
| 10107              | 16:34:50.047440 | 134063 | caffe.cpp:292] | accuracy   | =                 | 0.9912     |

程序中的每个batch的准确率都进行了计算，最后得到一个总的准确率。对于本书的 例子，生成的模型存档数量不多，对照验证数据loss小、准确率高的区域，手动运行所有 模型就可以挑选一个最优的模型。如果是模型存档很多的情况下，利用测试集挑选模型， 最好自己写成脚本来比较所有模型中最好的一个。

在数据不是很充裕的情况下，很可能手头并没有一个专门的测试数据集，而是只有训 练和验证集，或者说验证集和测试集合二为一。这种情况下，挑选模型就是个经验活，一 般而言，数据越多，验证集loss最小的和准确率最高的就越有可能是一个，如果不是一个， 通常选loss最小的泛化性能会好一些。就像在第3章中讲到的，无论是训练集、验证集还 是测试集，其实都是对真实分布的采样，所以谁知道哪个模型才是真正最优的呢？只是在 大数据量上挑出的模型比小数据量上挑出的模型更有信心而已。

2.评估模型性能

评估模型性能一般来说主要是评估速度和内存占用。在Caffe中这件事情也很简单， 只要有描述模型网络结构的prototxt文件就可以，因为支持评估计算性能，所以不需要参 数。可以直接用caffe/example/mnist下lenet.prototxt作为评估的结构，在终端输入：

\>> /path/to/caffe/build/tools/caffe time -model lenet.prototxt -gpu 0

得到输出如下：

3631 caffe. cpp: 308 ] Use GPU with device ID

10108    00:53:53.281692

0

10108    00:53:53.456862

parameters: name: "LeNet” state {

phase: TRAIN

}

layer {

name: "data"

...中间部分省略...

top: "prob"

}

10108    00:53:53.456987

data 工 0108

3631 net.cpp:49] Initializing net from

3631 layer_factory.hpp:77] Creating layer

3631 net.cpp:91] Creating Layer data

00:53:53.457008

| 工 0108  | 00:          | 53:   | 53.584645   | 3631 net | .cpp:399] prob            | -> prob |           |          |      |
| -------- | ------------ | ----- | ----------- | -------- | ------------------------- | ------- | --------- | -------- | ---- |
| 10108    | 00:          | 53:   | 53.584926   | 3631 net | .cpp:141] Setting up prob |         |           |          |      |
| 10108    | 00:          | 53:   | 53.584935   | 3631 net | .cpp:148] Top             | shape   | :64    10 | (640)    |      |
| 10108    | 00:          | 53:   | 53.584949   | 3631 net | .cpp:156] Memory required | for     | data:     |          |      |
| 5172224  |              |       |             |          |                           |         |           |          |      |
| 10108    | 00           | :53   | :53.584951  | 3631     | net.cpp:219]              | prob    | does      | not      | need |
| backward | computation. |       |             |          |                           |         |           |          |      |
| 10108    | 00           | \|:53 | :53.584959  | 3631     | net.cpp:219]              | ip2     | does      | not      | need |
| backward | computation. |       |             |          |                           |         |           |          |      |
| 10108    | 00           | :53   | :53.584980  | 3631     | net.cpp:219]              | convl   | does      | not      | need |
| backward | computation. |       |             |          |                           |         |           |          |      |
| 10108    | 00           | :53   | .-53.584982 | 3631     | net.cpp:219]              | data    | does      | not      | need |
| backward | computation. |       |             |          |                           |         |           |          |      |
| 10108    | 00           | :53   | :53.584985  | 3631     | net.cpp:261]              | This    | network   | produces |      |

3631    net.cpp:274]    Network initialization

output prob

10108    00:53:53.584995

done.

10108 10108 10108 10108 ★ ★ ★

10108

00:53

00:53

00:53

53.585024

53.586663

53.586686

00:53:53.586691

3631

3631

3631

3631

caffe.cpp:320] caffe.cpp:325] caffe.cpp:326]

Performing Forward Initial loss:    0

Performing Backward

00:53:53.586695 iterations.

10108    00:53:53.588556

forward-backward time:    1.83546 ms

10108    00:53:53.589872    3631

forward-backward time:    1.29267 ms

caffe.cpp:334]    *** Benchmark begins

3631 caffe.cpp:335] Testing for 50

caffe.cpp:363]    Iteration:    1

caffe.cpp:363]    Iteration:    2

3631

10108    00:53:53.661034    3631    caffe.cpp:363]

forward-backward time:    1.27718 ms.

10108    00:53:53.661046    3631 caffe.cpp:366] Average

工teration:

time per layer:

| 10108    00:53:53.661048               | 3631 caffe.cpp:369] | data                      | forward:  |
| -------------------------------------- | ------------------- | ------------------------- | --------- |
| 0.0012032 ms.10108    00:53:53.661052  | 3631 caffe.cpp:372] | data                      | backward: |
| 0.00122112 ms.10108    00:53:53.661056 | 3631 caffe.cpp:369] | convl                     | forward:  |
| 0.14328 ms.10108    00:53:53.661062    | 3631 caffe.cpp:372] | convl                     | backward: |
| 0.285845 ms.10108    00:53:53.661065   | 3631 caffe.cpp:369] | pooll                     | forward:  |
| 0.0450701 ms.10108    00:53:53.661069  | 3631 caffe.cpp:372] | pooll                     | backward: |
| 0.00120576 ms.10108    00:53:53.661073 | 3631 caffe.cpp:369] | conv2                     | forward:  |
| 0.180986 ms.10108    00:53:53.661077   | 3631 caffe.cpp:372] | conv2                     | backward: |
| 0.178819 ms.10108    00:53:53.661080   | 3631 caffe.cpp:369] | pool2                     | forward:  |
| 0.0197043 ms.10108    00:53:53.661097  | 3631 caffe.cpp:372] | pool2                     | backward: |
| 0.0011904 ms.10108    00:53:53.661100  | 3631 caffe.cpp:369] | ipl                       | forward:  |
| 0.160433 ms.10108    00:53:53.661103   | 3631 caffe.cpp:372] | ipl                       | backward: |
| 0.0768755 ms.10108    00:53:53.661105  | 3631 caffe.cpp:369] | relul                     | forward:  |
| 0.0115635 ms.10108    00:53:53.661108  | 3631 caffe.cpp:372] | relul                     | backward: |
| 0.0011808 ms.10108    00:53:53.661111  | 3631 caffe.cpp:369] | ip2                       | forward:  |
| 0.0770592 ms.10108    00:53:53.661115  | 3631 caffe.cpp:372] | ip2                       | backward: |
| 0.0231827 ms.10108    00:53:53.661118  | 3631 caffe.cpp:369] | prob                      | forward:  |
| 0.014775 ms)10108    00:53:53.661123   | 3631 caffe.cpp:372] | prob                      | backward: |
| 0.00119104 ms.10108    00:53:53.661134 | 3631 caffe.cpp:377] | Average Forward pass:     |           |
| 0.765267 ms.10108    00:53:53.661139   | 3631 caffe.cpp:379] | Average Backward pass:    |           |
| 0.67 9705 ms.10108    00:53:53.661144  | 3631 caffe.cpp:381] | Average Forward-Backward: |           |
| 1.48855 ms.10108    00:53:53.661149    | 3631 caffe.cpp:383] | Total Time:    74         | .4273 ms. |
| 10108    00:53:53.661154               | 3631 caffe.cpp:384] | *** Benchmark             | ends ★★★  |

可以看到笔者的GTX980M运行一次前向计算不到1毫秒。另外这里也统计了批数量 为64的时候数据需要的内存，不过需要注意的是，这里只是对数据部分的估算，部署的时 候以此为准是不靠谱的，还是需要实际做过压力测试才知道。如果在执行命令的时候去掉 -gpu选项：

» /path/to/caffe/build/tools/caffe time -model lenet.prototxt 则会测试CPU下的执行效率，比如笔者计算机的CPU是i7-5500U,底层矩阵运算库是atlas, 运行一次前向计算需要26毫秒。有人也许会问为什么还要关注CPU,明明是GPU快了一 个量级还多啊？事实上虽然训练模型阶段几乎已经被NVIDIA的GPU统治了，但是部署 一个应用的时候GPU除了快，还有不灵活的数据交换和过高的功耗等特点。另外再加上基 于CPU架构下的程序部署已经非常成熟并且灵活，所以在很多大型公司里，训练用GPU, 预测阶段用CPU是很常见的。甚至为了更好的能耗比，在部署阶段可考虑用可编程逻辑阵

列芯片(FPGA)以及专用集成电路芯片(ASIC)。



8.2.4识别手写数字

有了训练好的模型，就可以用来识别手写数字了。我们测试用的是test数据集的图片 和之前生成的列表，基于Python接口来实现：

import sys

sys.path.append(*/opt/caffe/python*) import numpy as np import cv2 import caffe

\#均值和缩放系数

MEAN =    128

SCALE =    0.00390625

\#文件列表作为输入的参数

imglist = sys.argv[1]

\#设置GPU模式运行 caffe.set_mode_gpu()

\#使用第一知GPU_ caffe.set_device(0)

net = caffe.Net('lenet.prototxt',    *mnist_lenet_iter_36000.caffemodel',

caffe.TEST)

net.blobs[* data *].reshape(1,    1,    28,    28)

with open (imglist, * r1) as f:

line = f.readline() while line:

imgpath = line.split()[0] line = f.readline()

\#读取图片并减去均值128

image = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE) image = image.astype(np.float) - MEAN # 和 lenet_train_val .prototxt 保持一致，乘以 0.0390625 image *= SCALE

net.blobs[* data'].data[.. . ]    = image

output = net.forward()

pred_label = np.argmax(output[* prob1] [0])

print(* Predicted digit for {} is {}1.format(imgpath,

pred_label))

需要提一下的是lenetprototxt^,开头几行和第7章中讲的对数据形状的定义不一样。

name: "LeNet" layer {

name: "data" type: "Input"

| top: "data" |      |
| ----------- | ---- |
| input param | {    |
| shape:    { |      |
| dim:        | 64   |
| dim:        | 1    |
| dim:        | 28   |
| dim:        | 28   |

}

layer {

name:    "convl

从一个单纯的形状定义变成了一个简单的Input层。这是后来在Caffe中加入的方式， 应该说这才是比较推崇的方式，因为数据也抽象成了一个层，而不是一种特殊的定义。另 外注意和第7章的脚本不同，这次用的是GPU,并指定序号为0的GPU。把这段代码保存 为 recognize digit.py,并运行脚本：

» python recognize_digit.py test.txt

得到如下的输出，对于前几行而言，结果还是很准的：

| Predicted | digit | for  | mnist/test/000000  | _7.jpg | is   | 7    |
| --------- | ----- | ---- | ------------------ | ------ | ---- | ---- |
| Predicted | digit | for  | mnist/test/000001  | _2.jpg | is   | 2    |
| Predicted | digit | for  | mnist/test/000002_ | _l.jpg | is   | 1    |
| Predicted | digit | for  | mnist/test/000003  | _0.jpg | is   | 0    |
| Predicted | digit | for  | mnist/test/000004  | _4.jpg | is   | 4    |
| Predicted | digit | for  | mnist/test/000005  | _l.jpg | is   | 1    |
| Predicted | digit | for  | mnist/test/000006  | _4.jpg | is   | 4    |
| Predicted | digit | for  | mnist/test/000007  | _9.jpg | is   | 9    |
| Predicted | digit | for  | mnist/test/000008  | _5.jpg | is   | 5    |
| Predicted | digit | for  | mnist/test/000009_ | _9.jpg | is   | 9    |
| Predicted | digit | for  | mnist/test/000010  | _0.jpg | is   | 0    |

8.2.5增加平移和旋转扰动

在第6章中已经实现过一个简单的利用扰动增加数据的小工具，这个工具对MNIST是 否有用呢？本节一起来试一下。MNIST的特点是单通道灰度图，同时每个数字都是已经经 过了对齐在画面中心的处理。然而每个人写字都是没有固定规则的，什么样算是在中心很 难定义，并且字体的歪斜和“胖瘦”程度也是难以界定的，所以考虑利用平移和旋转对数 据进行增加。用第章实现过的小工具，关闭除了裁剪和旋转以外的一切选项，旋转范围 设定为正负15°之间。把训练集增加为原来的6倍，在控制台执行如下命令：

» pythona run_augmentation.py mnist/train/ mnist/augmented 250000

——rotate_angle_vari=15 ——p_mirror=0 --p_hsv=0    ——p_gamma=0

这样会在mnist下生成一个augmented的文件夹，包含25万张扰动后的图片，并且这 些图片的命名规则也符合gen_caffe_imglist.py的解析规则。所以接下来执行生成图片列表 文件的命令：

» python gen_caffe_imglist.py mnist/augmented augmented.txt

然后把原始训练集和新增加的文件列表合并：

» cat train.txt augmented.txt > train_aug.txt

就得到了包含30万张图片列表的文件，然后为这个文件单独建立一个lmdb：

»    /path/to/caffe/built/tools/convert_imageset    ./ train_aug.txt

train_aug_lmdb --resize_width=28 --resize_height=28 --gray --shuffle

注意，因为扰动后的图片分辨率不一定是28x28 了，所以必须在这里用resize width 和resize_height的选项把写入lmdb的图像大小固定，另外因为用cat合并的文件前5万张 是原始文件，后面都是增加的，所以shuffle选项也变成了必须项。接下来把 lenet solver.prototxt 中的 net 改成 lenet train val aug.prototxt, snapshot_prefix 改为 mnist aug lenet,然后其他参数维持不变就可以训练了。训练结束后把log文件命名为

mnist_with_augmentation.log,然后用 plot training log.py 画出两个训练的对比如下：

» python plot_training_log.py 0 test_acc_vs_iters.png mnist_train. log mnist_train_with_augmentation.log

» python plot_training_log.py 2 test_loss_vs_iters.png mnist_train. log mnist_train_with_augmentation.log

输出结果如图8-3所不。

Test loss vs. Iters

Test accuracy vs. Iters

0.12

0.10

0.08

S 0.06

0.04

0.02

*~■ mnisttrain

mnisttrainwithaugmentation

0.99

Auejnuuettai

0.98

0.97

0.96

mnist_train

mnist_train_with_augmentation

0    5000    10000    15000    20000    25000    30000    35000    0    5000    10000    15000    20000    25000    30000    35000

Iters    Iters

图8-3对比数据扰动前后的验证集指标

从验证集来看，增加扰动数据后的指标还是有提升的，loss在训练后期明显比原始数 据集低，准确率最高达到了 99.27%,提高了约0.3%。不过收敛速度比原始数据要慢，并 且到了 36000次迭代的时候仍然很不稳定。这是因为原始训练数据只有5万张，每个batch 里50个数据的情况下，迭代1000次就是一代（epoch）,从图8-3中看，超过20代之后 就已经比较稳定了。而增加后的数据总量是30万，迭代6000次才是一代，到了 36000次 结束时，才迭代了 6代。那么如果希望接着36000次的状态继续训练呢？比如继续训练到 20代，也就是12万次的时候，那么需要到solver文件中将max iter的值改为120000，然 后执行如下命令就能接着36000次的状态存档继续训练。

» /path/to/caffe/build/tools/caffe train -solver lenet_solver.prototxt

-snapshot mnist_aug_lenet_iter_36000.solverstate -gpu 0

最后得到的loss和准确率随训练的曲线如图8-4所示，可以看到loss还在缓慢下降， 最高的验证集准确率超过了 93%。

0.030

0.028

爰 0.026

0.024



Test loss vs. Iters



)00 40000 50000 60000 70000 80000 90000 100000 110000 120000 Rers

0.9940

0.9935

0.9930

2

9

9

o.

\>»ueJ3um^(vi

Test accuracy vs. Iters

mnist_train_resumed

)0 40000 50000 60000 70000 80000 90000 100000 110000 120000 Iters

I'fl 8-4继续玷于扰动后数据训练到12万次迭代的曲线

最后还要提一下的是，直接在样本基础上做扰动增加数据只是数据增加的方法之一， 并且不是一个好的方案，因为增加的数据量有限，并且还要占用原有样本额外的硬盘空间。 最好的办法是训练的时候实时对数据进行扰动，这样等效于无限多的随机扰动。其实Caffe 的数据层已经自带了最基础的数据扰动功能，不过只限于随机裁剪和随机镜像，并不是很 好用。Github上有一些开源的第三方实现的实时扰动的Caffe层，会包含各种常见的数据 扰动方式，只需要到github的搜索框里搜caffe augmentation就能找到很多，这里就不展开 讲了。

8.3基于MXNet的实现

本节基于和8.2节一样的网络结构和数据源，在MXNet上实现手写数字识别，进而了 解用MXNet进行图片分类任务的基本步骤。

8.3.1 制作 Image Record io 数据

和Caffe中用LMDB保存大量数据相对应，MXNet中对于大量数据10的实现采用的 是Image Recordio,这是DMLC自己研发的一种高效且易于分布式访问的数据存储方式， 和LMDB —样也是基于内存映射(Memory Map)。因为在硬盘上的存储编码可以是JPG 等压缩格式，所以空间占用上和Caffe中用LMDB类存储cv::Mat的方式比起来优势很大， 并且转换时的速度也不慢，这一点又胜过Caffe中直接读取图片的ImageDataLayer。和Caffe 类似，要制作这种格式，第一步也是要制作一个文件路径和标签的列表，格式如下：

0    5    mnist/train/000000_5.jpg

1    0    mnist/train/000001_0.jpg

2    4    mnist/train/000002_4.jpg

3    1    mnist/train/000003_l.jpg

每一行都是用制表符分隔开的3个字段，第一个字段是一个整数编号，第二个字段是 标签，第三个字段是文件名或者文件路径。注意虽然例子中的编号是按顺序的，其实不重 要。从产生的MNIST图片生成列表的代码如下：

import os

import sys

\#第一个参数是输入路径

input_path = sys.argv[l].rstrip(os.sep)

\#第£个参数是输出路径’ output_path = sys.argv[2]

\#列出Sj入文件夹下所有文件名 filenames = os . listdir(input_path) with open (output_path, * w') as f:

for i, filename in enumerate(filenames):

filepath = os.sep.j oin([input_pathz filename]) label = filename[:filename.rfind(*.*)].split(*_*)[1]

\#格式化为序号\t标签\t文件路径

line =    ’{}\t{}\t{}\n*.format(i, label, filepath)

f.write(line)

把这段代码保存为gen mxnet imglist.py,然后依次执行下面命令：

» python gen_mxnet_imglist.py mnist/train train.1st

\>> python gen_mxnet_imglist.py mnist/val val.lst

» python gen_mxnet_imglist.py mnist/test test.1st

接下来第二步就可以利用MXNet的官方工具mxnet/bin/im2rec进行数据转换了，执行 下面命令：

» /path/to/mxnet/bin/im2rec train.1st . / train.rec color=0

» /path/to/mxnet/bin/im2rec val.lst . / val.rec color=0

» /path/to/mxnet/bin/im2rec test.1st . / test.rec color=0

需要提一下的是，列表文件中，第二个字段可以是多个标签的，如果是这种情况，就 需要在执行im2rec时指定label_width参数为标签的个数。更多参数的含义可以参考 [http://mxnet](http://mxnet/). io/zh/api/python/io. html。

截止作者完稿时，在最新正在开发的0.9版的MXNet中推出了 image模块，提供了 Python实现的更灵活的接口 Imagelter,有兴趣的读者可以到MXNet的github主页进行

了解。

8.3.2 用 Module 模块训练 LeNet-5

第7章中已经大概了解了 MXNet中接口最简单的Model模块的使角，本节将进一步 了解更灵活的Module模块。按照Caffe中LeNet-5版本的结构，定义网络并用Module模 块封装的代码如下：

import mxnet as mx

\#定义数据Symbol

data = mx.symbol.Variable(* data1)

\#第一层卷积和池化

convl = mx.symbol.Convolution(data=dataz kernel=(5, 5), num_filter=20) pooll = mx.symbol.Pooling(data=convl, pool_type="max",

kernel=(2,    2), stride=(2, 2))

\#第二层卷积和池化

conv2 = mx.symbol.Convolution(data=pooll, kernel=(5, 5), num_filter=50) pool2 = mx.symbol.Pooling(data=convl, pool_type="max",

kernel=(2, 2), stride=(2,    2))

\#第一层全连接，输入到全连接前先将二维数据展开

flatten = mx.symbol.Flatten(data=pool2)

fcl = mx.symbol.FullyConnected(data=flatten, num_hidden=500) relul = mx.symbol.Activation(data=fcl, act_type="relu")

\#第二层全连接

f c2 = mx.symbol.FullyConnected(data=relul, num_hidden=l0)

\# Softmax+loss

lenet5 = mx.symbol.SoftmaxOutput(data=fc2, name=1softmax *)

\#用Module封装，这次使用GPU来进行训练

mod = mx.mod.Module(lenet5, context=mx.gpu(0))

有了模型，接下来定义数据。在MXNet中，数据迭代器比Caffe的Data Layer强大不 少，提供了更丰富的数据扰动方式，这里用随机裁剪和随机旋转。需要注意的是，MXNet 内置的随机裁剪是正方形裁剪，随机旋转是原大小旋转，也就是说会出现没有图像的区域， 我们用黑色进行了填充，相应代码如下：

train_dataiter = mx.io.ImageRecordlter(

~ #训练数据源

path_imgrec="../data/train.rec”，

\#数维度

data_shape=(1,    28,    28),

\#批_的样本数量

batch_size=50,

\#减i均值，因为是单通道，所以定义红色通道均值即可 mean_r=128,

\#减均值后归一化到［0.5,    0.5)之间

scale=0.00390625,

\#数据增加-随机裁剪

rand_crop=True,

\#裁 &的最小边长

min_crop_size=24,

\#暴剪的*大边长

max_crop_size=28,

\# i据增沅-随机旋转，范围为-15°〜15°之间 max_rotate_angle=15z

林i转后的圣白部分值填充为◦，也就是黑色 fill_value=0

)

val_dataiter = mx.io.ImageRecordlter( path_imgrec="../data/val.rec", data_shape=(1,    28,    28),

batch_size=100,

mean_r=128, scale=0.00390625,

)

模型和数据两大要素已备齐，下面可以开始训练模型了。

import logging

\#把log输出至G文件

logging.getLogger().setLevel(logging.DEBUG)

fh = logging.FileHandler(* train_mnist_lenet.log *)

logging.getLogger().addHandler(fh)

\#用来随着训练进程改变学习率

\#    MXNet默认的学习率策略较少，这里用FactorSecheduler，

\#相当于Caf fe中lr_policy的step，如果希望实现其他类型

\#需要自己到lr_scheduler. py中添加代码

*wd':    0.0005,

1lr_scheduler1: lr_scheduler

}

\#    checkpoint是个回调函数，用来保存模型，period是每多少个epoch保存一次 checkpoint = mx.callback.do_checkpoint('mnist_lenet', period=5)

\#和8.31中例子保持一致训练到3.6万次，也就是36个epoch

mod.fit(train_dataiter,

eval_data=val_dataiter, optirnizer_params=optimizer_params, num_epoch=3 6,

epoch_end_callback=checkpoint)

把上面所有代码合在一起，保存在train_lenet5.py中，然后执行：

» python train_lenet5.py

这样就开始训练了，训练完毕会输出一个mnist_lenet-symbol.json文件，这个是模型结 构的描述文件，按照设定，每迭代5代保存一次的模型参数存档，命名形式为mnist_lenet-[i)l| 练的代数].pamms。当然还有输出的log,例子如下，主要包含训练的精度、验证集的精度、 学习率的变化和保存模型的信息。

Epoch[0] Train-accuracy=O.710640

Epoch[0] Time cost=3.347

Epoch[0] Validation-accuracy=0.955000

Update[1001]: Change learning rate to 9.50000e-03

Epoch[1] Train-accuracy=0.925640

Epoch[1] Time cost=3.453

...中间部分省略...

Update[4001] : Change learning rate to 8.14506e-03

Epoch[4] Train-accuracy=0.959400

Epoch[4] Time cost=3.451

Saved checkpoint to nmnist_lenet-0005.params"

Epoch[4] Validation-accuracy=0.982800

Update[5001] : Change learning rate to 7.73781e-03

MXNet中没有Caffe里专门画训练曲线的工具，不过在自带例子中有个 mxnet/example/kaggle-ndsbl/training_curves.py 对只输出准确率的训练 log 文件都管用：

» python /path/to/mxnet/example/kaggle-ndsbl/training_curves.py --log-file=train_mnist_lenet.log    }

运行程序得到如图8-5所示的可视化结果。

.8



0    5    10    15    20    25    30    35

Epoch

图8-5 MXNet训练集和验证集准确率随训练变化

8.3.3测试和评估

1.测试模型准确率

MXNet在测试集上评估非常简单，把训练好的模型读取到一个Module中，把测试数

据装载到一个ImageRecordlter中，然后调用Module的score ()函数就可以了。

import mxnet as mx #测试数据的迭代器方法和验证数据一致 test_dataiter = mx.io.ImageRecordlter(

path_imgrec=n../data/test.rec", data_shape=(1,    28,    28),

batch_size=100 r mean_r=128,

scale=0.00390625,

)

\#从前缀为nrniSt_lenet的存档中读取第35代的存档

\#    for_training 要指定为 False

mod = mx.mod.Module.load(*mnist_lenet',    35, context=mx.gpu(0))

V    f I

\#如果是想接着之前的结果继续训练把begin_epoch设置为35即可 mod.fit(...,

begin_epoch=35)

V    V •

\#    load只管读取模型文件(.j son)和参数(.params)

\#要想用起来还需要bind—遍

mod.bind(

data_shapes=test_dataiter.provide_data, label_shapes=test_dataiter.provide_label, for_training=False)

\#定义一个评估模型的metric，这里使用准确率(acc: accuracy) metric = mx .metric.create('acc1)

\#调用score ()函数，结果更新在metric里 mod.score(test_dataiter, metric)

\#准确率的metric里保存准确率和对应值

for name, val in metric.get_name_value():

print^( * {} = { : . 2f} % * . format (name, val* 100) >

把上面代码保存并执行，就能得到在测试集上的评估结果，如笔者训练的模型结果输 出如下：

accuracy=99.09%

2.评估模型性能

这里用一个比较粗略的方法来评估前向计算性能，就是用python的time模块，迭代

一定次数计算总时间，然后求得每次前向计算的消耗时间。

import time import mxnet as mx

\#和Caffe中的用例保持一致，用64作为batch size benchmark—dataiter = mx.io.ImageRecordlter(

path_imgrec="../data/test.rec", data_shape=(1,    28,    28),

batch_size=64,

mean_r=128, scale=0.00390625,

)

\#测试GPU下的执行效率

mod = mx.mod.Module.load('mnist_lenet1,    35, context=mx.gpu(0))

mod.bind(

data_shapes=benchmark_dataiter.provide_data, label_shapes=benchmark_dataiter.provide_label, for_training=False)

\#获取测试开始时的时间

start = time.time()

\#迭代并计次

for i, batch in enumerate(benchmark_dataiter): mod.forward(batch)

\#获取消耗的总时间并输出

time_elapsed = time.time()    - start

msg =    ' { } batches iterated!\nAverage forward time per batch:

{:.6f} ms *

print(msg.format(i+1, 1000*time_elapsed/float(i)))

在笔者的笔记本电脑上得到如下结果：

157 batches iterated!

Average forward, time per batch:    0.754967 ms

和Caffe的结果差不多，但是笔者用的毕竟是带桌面的笔记本电脑，结果可能不具参

考性。

8.3.4识别手写数字

用训练好的MXNet模型预测图片略微有些复杂，因为mxnet的Module模块中，没

有直接接受NDArray作为输入的方法，需要把输入做成一个带名字的值的形式，具体代

码如下：    <

import sys import os import cv2

\# 从 Python 的 collections 库中导入 namedtuple from collections import namedtuple

\#建立一个namedtuple，Batch为名称，只有一个字段，字段名字是data

Batch = namedtuple('Batch *,    ['data*])

import numpy as np import mxnet as mx

\#输入路径，在例子中是包含所有测试文件图片的nmist/test input_path = sys.argv[l].rstrip(os.sep)

mod = mx.mod.Module. load (*mnist_lenet' ,    35, context=mx.gpu (2))

\#没有数据迭代器的情况下，手动指定输入_的维度

mod.bind(

data_shapes=[(* data *,    (1,    1,    28,    28))],

for_training=False)

filenames = os.listdir(input_path) for filename in filenames:

filepath = os.sep.j oin([input_path, filename])

\#读取灰度图片

img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

\#数据预处理，减均值和缩放

img = (img. astype(np.float)-128)    ★    0.00390625

\# reshape成mod接受的形状

img = img.reshape((1,    1)+img.shape)

\#用Batch封装后传入做前向运算

mod.forward(Batch([mx.nd.array(img)]))

\#得到二维的概率

prob = mod.get_outputs()[0].asnumpyO

\#变成一维数组

prob = np.squeeze(prob)

\#获取预测的标签

pred_label = np.argmax(prob)

print(* Predicted digit for {} is {}'.format(filepath pred_label))

把这段代码同样保存为recognize_digit.py,并执行下面命令：

» python recognize_digit.py mnist/test

得到如下输出，对于前几行而言，结果和8.3.3基于Caffe的结果一致。

| PredictedPredicted | digitdigit         | for mnist/test/000000 7.jpg | isis               | 72     |      |      |
| ------------------ | ------------------ | --------------------------- | ------------------ | ------ | ---- | ---- |
| for                | mnist/test/000001_ | _2.jpg                      |                    |        |      |      |
| Predicted          | digit              | for                         | mnist/test/000002  | _l.jpg | is   | 1    |
| Predicted          | digit              | for                         | mnist/test/000003_ | _0.jpg | is   | 0    |
| Predicted          | digit              | for                         | mnist/test/000004  | _4.jpg | is   | 4    |
| Predicted          | digit              | for                         | mnist/test/000005  | _l.jpg | is   | 1    |
| Predicted          | digit              | for                         | mnist/test/000006_ | _4.jpg | is   | 4    |
| Predicted          | digit              | for                         | mnist/test/000007_ | _9.jpg | is   | 9    |
| Predicted          | digit              | for                         | mnist/test/000008  | _5.jpg | is   | 5    |
| Predicted          | digit              | for                         | mnist/test/000009  | _9.jpg | is   | 9    |
| Predicted          | digit              | for                         | mnist/test/000010  | _0.jpg | is   | 0    |
