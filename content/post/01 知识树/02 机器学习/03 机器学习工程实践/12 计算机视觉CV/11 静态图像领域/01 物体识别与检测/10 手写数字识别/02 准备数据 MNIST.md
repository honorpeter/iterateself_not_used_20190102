---
title: 02 准备数据 MNIST
toc: true
date: 2018-08-29
---
# 需要补充的

- 对于这个 MNIST 的数据集的处理，感觉还是有很多需要补充进来的。



# 准备数据 MNIST

在大多数框架的例子中，用 MNIST 训练 LeNet-5 的例子都被脚本高度封装了。只需要执行脚本就可以完成从下载数据到训练的过程。比如在 MXNet 中，直接到 mxnet/example 下执行 train mnist.py 就大功告成了，Caffe 中也有类似的 shell 脚本。<span style="color:red;">嗯，这两个脚本也要总结进来。</span>

其实这样是不利于初学者了解到底发生了什么的。所以本书把数据准备的部分剥离开来，把每个训练都具体到一张图片，然后从头开始完整地过一遍流程。了解了这个流程，基本上就了解了如何从图片数据开始到训练一个模型进行分类。<span style="color:red;">嗯。</span>

## 下载 MNIST

原版 MNIST 下载的很慢，本书中用的 MNIST 是 Bengio 组封装好的数据包，下载地 址为 http://deeplearning.net/data/mnist/mnist.pkl.gz 。

在Linux下直接用wget即可：

```
wget http://deeplearning.net/data/mnist/mnist.pkl.gz
```

或者写在一个 .sh 脚本里进行运行：

download_mnist.sh

```sh
#!/bin/sh
# wget http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz
wget http://deeplearning.net/data/mnist/mnist.pkl.gz
```

<span style="color:red;">对于 wget ，一直没有仔细看过是用来干什么的。</span>

本书的github仓库中第8章的文件夹下也有提供该文件的下载脚本。

## 生成 MNIST 的图片

mnist.pkl.gz 这个压缩包中其实是数据的训练集、验证集和测试集用 pickle 导出的文件被压缩为 gzip 格式，所以用 python 中的 gzip 模块当成文件就可以读取。

其中每个数据集是一个元组，第一个元素存储的是手写数字图片，表示每张图片是长度为28x28=784的一维浮点型 numpy 数组，这个数组就是单通道灰度图片按行展开得到，最大值为1，代表白色部分，最小值为0，代表黑色部分。元组中第二个元素是图片对应的标签，是一个一维的整型numpy数组，按照下标位置对应图片中的数字。基于以上将数据集转换成图片的代码如下：


```python
import os
import pickle, gzip
from matplotlib import pyplot

# 读取 MNIST 数据
print('Loading data from mnist.pkl.gz ...')
with gzip.open('mnist.pkl.gz', 'rb') as f:
    train_set, valid_set, test_set = pickle.load(f)

# 创建 mnist 文件夹
imgs_dir = 'mnist'
os.system('mkdir -p {}'.format(imgs_dir))
datasets = {'train': train_set, 'val': valid_set, 'test': test_set}

# 转换 train、val 和 test 数据集
for dataname, dataset in datasets.items():
    print('Converting {} dataset ...'.format(dataname))
    data_dir = os.sep.join([imgs_dir, dataname])

    # 在 mnist 文件夹下创建对应子文件夹
    os.system('mkdir -p {}'.format(data_dir))

    # i 代表数据的序号，用 zip() 函数读取对应位置的图片和标签
    for i, (img, label) in enumerate(zip(*dataset)):
        # 格式化生成文件的民资，第一个字段是序号，第二个字段是数字值
        filename = '{:0>6d}_{}.jpg'.format(i, label)
        filepath = os.sep.join([data_dir, filename])
        # 将展开的一维数组还原为 二维图像
        img = img.reshape((28, 28))
        # 用 pyplot 保存可以自动归一化生成像素值在 o~255 之间的灰度图片。
        pyplot.imsave(filepath, img, cmap='gray')
        if (i+1) % 10000 == 0:
            print('{} images converted!'.format(i+1))

```

说明：

1. <span style="color:red;">`with gzip.open('mnist.pkl.gz', 'rb') as f:` 这个真的是第一次见，没想到 对于 gzip 格式的文件，还可以这样解压，之前可能见过，但是没有注意过，不错。</span>
2. <span style="color:red;">`os.system('mkdir -p {}'.format(imgs_dir))` 和 `os.system('mkdir -p {}'.format(data_dir))` 和 `os.sep.join([data_dir, filename])` 竟然可以这样使用 os.system ，厉害了，对 os.system 进行总结一下，是可以执行所有的 shell 的命令吗？而且，`os.sep.join` 这个是推荐使用的路径拼接的方式吗？</span>
3. <span style="color:red;">对于 `enumerate(zip(*dataset))` 的使用再进行总结下。</span>
4. <span style="color:red;">之前不知道 `pyplot` 还可以用来保存图片， `pyplot.imsave(filepath, img, cmap='gray')` ，看来对 matplotlib 还是要好好总结下的。而且，这个数字不是只是 0 和 1 吗？怎么对应到一个 0~255 的灰度图像中的？</span>

这个脚本首先创建了一个叫 mnist 的文件夹，然后在 mnist 下创建3个子文件夹 train、 val和 test，分别用来保存对应的3个数据集转换后产生的图片。每个文件的命名规则为第一个字段是序号，第二个字段是数字的值，保存为 JPG 格式。一些图片的例子如图8-1所示。

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180901/2Gb5H8C48m.png?imageslim)





## 相关资料

- 《深度学习与计算机视觉》
