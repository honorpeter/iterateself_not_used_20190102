---
title: 11 基于 MXNet 实现 LeNet-5 网络
toc: true
date: 2018-09-01
---

# 需要补充的

- 这个还没有进行整理。要进行整理。


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





## 相关资料

- 《深度学习与计算机视觉》
