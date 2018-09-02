---
title: 使用 MXNet 的 SSD 模型
toc: true
date: 2018-08-29
---
# 需要补充的

- 还是有很多东西需要拆分出来的。
- 这个 PASCAL VOC 是不是目标检测的官方数据集？如果是的话，要把所有的方法在这个数据集上进行实践。
- 是不是要把这个合并到 “经典网络理解” 文件夹里？如果是标准数据集的话看看是不是可以融过去。


## 基于 PASCAL VOC 数据集训练 SSD 模型

本节一起来了解 MXNet 下的训练/测试 SSD 的官方例子，并试试 SSD 的效果。

### MXNet 的 SSD 实现

MXNet 的 SSD 的实现其实就是把 SSD 作者 Wei Liu 基于 Caffe 的官方实现(网址为 <https://github.com/weiliu89/caffe/tree/ssd> )。在 MXNet 上的重新实现，原作者是 Missouri-Columbia 大学的博士生 Zhi (Joshua) Zhang。具体实现是在mxnet根目录中的 example\ssd目录下，如图11-8所示。<span style="color:red;">原作者的 Caffe 的实现也要总结进来。</span>

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/glc9h1kIgC.png?imageslim)

其中：

- config 下是训练相关的一些设置，如随机镜像和检测及每个 epoch 的随机设置等;
- data 是默认存放数据或者数据软链接的地方；
- dataset 是数据迭代的实现，默认是支持 PASCAL VOC的数据格式。另外，训练的物体类别定义也是在dataset/pascal_voc.py中实 现，所以如果需要训练自己的数据，就要在这个文件中做相应修改；
- detect 中包含执行目标检测的代码和接口；
- evaludate 是封装目标检测代码并评估模型指标的脚本；
- model 文件夹默认用来存储模型结构和参数值；
- operator 是个比较关键的文件夹，里面是对 MXNet 默认不包含的底层操作的实现，如 Faster R-CNN 中的 Region Proposal，SSD 中的默认物体框和标注框的匹配，正负样本的选取，还有 NMS 等操作的实现代码都是在 operator 中;
- symbol 里是默认网络结构的定义；
- tools 里定义了一些其他的常用基本操作如随机裁剪和随机补边的实现等；
- train 文件夹则是定义了训练网络的基本操作，由根目录下的 train.py 调用。
- 根目录下的其他文件后面再介绍。

<span style="color:red;">这个项目要仔细总结下。</span>

### 下载PASCAL VOC数据集

PASCAL VOC数据集已经简要介绍过了，下载地址如下。

- http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
- http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
- http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar

其中前两个分别是 2012 年和 2007 年的训练验证集下载地址，第 3 个是 2007 年版本的测试集下载地址，通常的用法是前两个数据作为训练验证数据，最后一个用来测试指标。

下载完毕后，分别对三个文件执行 `tar -xvf`，就可以得到一个 VOCdevkit 的文件夹。VOCdevkit 包含两个文件夹 VOC2007 和 VOC2012 ，这两个文件夹下的文件结构基本一致，一共是 5 个子文件夹，分别是 Annotations、ImageSets、JPEGImages、SegmentationClass 和 SegmentationObject。

对于目标检测任务，主要关心的是前 3 个文件夹：

- Annotations下是所有的标注信息， 格式为 XML，每个 XML 里的 `<object>` 就包含了标注物体的名称 `<name>` 和物体框的坐标 `<bndbox>` ;
- JPEGImages 文件夹下是和 Annotations 文件夹下的 XML 文件同名的 jpg 图片文件，与同名的 XML 的标注信息相对应；
- ImageSets/Main 下就包含了训练集、验证集和测试集的列表。

如果想要自己制作数据，如用本书第 6 章的小工具标注的数据来训练模型。最简单的方式是按照这里说的规则，把所有标注信息放到 Annotations 里，图片做成 JPG 格式放到 JPEGImages 中，然后训练/验证/测试集的列表放到 ImageSets/Main 下，再修改 dataset/pascal_voc.py 下的相应代码并另存，其他步骤与训练 PASCAL VOC 区别不大了。<span style="color:red;">嗯，数据标注的小工具是一定要会做的，对各种数据标注的工具还是要总结下的。</span>

执行本书 github 代码仓库中的 prepare_voc_data.sh 可以自动完成下载到解压的步骤。

```sh
#!/bin/sh
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
tar -xvf VOCtrainval_11-May-2012.tar
tar -xvf VOCtrainval_06-Nov-2007.tar
tar -xvf VOCtest_06-Nov-2007.tar
```

### 训练SSD模型

第 7 章已经讲过如何安装和配置 MXNet，不过默认下载并编译好的 MXNet 无法直接训练 SSD，原因就是 SSD 中有些操作是默认不被 MXNet 支持的。这些操作定义在 `operator` 文件夹下，所以我们需要做的是，找到根目录下的 make 文件夹，打开里面的 config.mk， 找到 `EXTRA_OPERATORS =` 这一行，修改为 ssd 中 `operator` 的路径：

```
EXTRA_OPERATORS = example/ssd/operator
```

如果使用的 MXNet 已经加入了自定义的 operator，则用下面语句：

```
EXTRA_OPERATORS += example/ssd/operator
```

然后到 MXNet 的根目录下，输入 make 命令，就得到了支持 SSD 的 MXNet 版本。<span style="color:red;">这个自定义的 operator 是怎么写的？是不是用 Caffe 会方便些？make 的过程中会有什么问题吗？</span>

当然用 Python 调用前别忘了再到 `mxnet\python` 目录下执行以下语句来更新 python 接口。<span style="color:red;">什么叫更新 python 接口？</span>

```
python setup.py install
```

训练 SSD 并不是从头训起，而是从一个 ImageNet 数据集预训练好的简化版 VGG-16 模型开始，按照官网的说明，该模型可以从下面链接下载 https://dl.dropboxusercontent.eom/u/39265872/vggl6_reduced.zip ，国内的读者也可以选择到 链接：https://pan.baidu.com/s/1GCzJ1bqJza5CdpkmrCJ72g 密码：2nvs 下载。

下载后解压得到定义网络结构的文件 `vgg16_reduced-symbol.json` 和对应的参数文件  `vggl6_reduced-0001.params`。把这两个文件放到 `example\ssd\model` 下，基础模型就准备好了。

接下来把 11.2.2 节中准备好的 VOCdevkit 文件复制到 `example\ssd\data` 下，或者通过 `ln -s` 在 example | ssd | data下建立一个链接。

现在万事俱备，直接到 ssd 目录下执行 train.py 就可以开始训练了，考虑到硬件配置的不同及训练效果等，可以通过修改 train.py 的参数执行训练，如笔者修改了 batch-size 和 epoch:

```
python train.py --batch-size=24 --epoch=20
```

训练过程中会得到实时的训练精度和 loss 的输出，每个 epoch 结束会在验证集上测试模型，输出例子如下：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/F55jI59gFl.png?imageslim)
![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/I2DIGHGbHd.png?imageslim)

### 测试和评估模型效果

因为训练比较耗时，笔者象征性地训练了一个 epoch，此外官网也很贴心地提供了训练好的模型（从原作者提供的模型转换而来），在相关资料里有对应的下载地址。

下载后解压得到 `ssd_300-0000.params` 和 `ssd_300-symbol.json` 两个文件，放到 `example/ssd/model` 下。然后执行：

```
python evaluate.py
```

就会默认执行 vggl6_reduced, epoch 为 0 的模型在 VOC2007 测试集上的评估，输出每个类别的 AP
 和最后的 mAP。

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/3BbkDij5KB.png?imageslim)

如果要评估别的模型可以在输入参数中指定，如下面命令评估训练完 3 个 epoch 得到的模型，并且 batch-size 指定为24。<span style="color:red;">什么意思？不是说评估别的模型吗？这个参数是用来评估的时候用的还是用来标识之前训练得到的这个模型的？</span>

```
python evaluate.py --batch-size 24 --epoch 3
```

上段代码评估的模型文件实际上是用来训练和验证的模型，实际部署的时候，和训练相关的如 loss 等都是不需要的，对默认的 Vggl6 训练出的模型，可以用下面脚本生成用于部署的模型和参数文件。

```
python deploy --num-class 20
```

执行完该脚本，在 `model` 文件夹下生成的两个 `deploy_` 前缀的文件就是用来部署的模型结构和对应参数值，其中 `.params` 文件其实就复制了一遍而已。

<span style="color:red;">这个地方的部署还是有些不明白？还是要自己跑一遍</span>

### 物体检测结果可视化

现在万事倶备，可以使用训练好（或是下载好）的模型执行检测任务了。MXNet 的 SSD 自带 demo，首先到 `data/demo` 下运行：

```
python download_demo_images.py
```

这个脚本会下载几张用于演示的图片，其中包括根目录下 demo.py 的默认演示图片 dog.jpg。回到 ssd 目录下，执行：

```
python demo.py
```

得到图11-9所示的结果。

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/Ib8HEhaBB8.png?imageslim)

如果要指定图片就用-image选项，下面用前面也用过的照片来试试:

```
python demo.py --images beihong_village.jpg
```

得到结果如图11-10所示。

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/4gdk9l4L0e.png?imageslim)

下面来简单看一下demo.py到底做了什么，demo.py 中主要就是一个交互的总逻辑，通过 `get_detector()` 获取了一个定义在 `detect` 文件夹下的 `Detector` 对象。在 `detect/detector.py` 中，定义了 `Detector` 的类。

首先 `Detector` 的初始化阶段，和之前讲的 MXNet 做分类的代码没有什么不同，就是把一个 `symbol` 读进来，并进行 `bind` 用于后续计算。

成员函数中的 `detect()` 用于执行前向计算，用 mod.predict() 执行前向计算之后，得到的结果 `detections` 是一个三维 的张量。其中第一个维度和 batch 相关，因为 demo.py 中默认 `batch-size` 为 1，所以所有结果都在 `detections[0]` 里，这个结果如看做是一个二维矩阵的话，每行就是一个检测到的物体框。第一列是物体框的类别下标，如果为 -1 说明是背景。第 2 列是类别的分数，第 3~6 列分别是 xmin、ymin、xmax 和 ymax 相对于画面宽高的百分比，所以物体框在画面中左上角的坐标就是 $( xmin\times 宽度，ymin\times 高度)$，右下角坐标是 $( xmax\times 宽度，ymax\times 高度)$。 `im_detect()` 函数是调用 `detect` 对读取的数据进行前向计算。`detect_and_visualize()` 函数会调用 `im_detect()` 函数返回的结果，然后在 `visualize_detection()` 函数中进行可视化，可视化的规则是取类别得分大于给定阈值的框进行可视化，detector.py 中，相关部分代码和注释如下:

(代码中的省略号表示省略了部分代码)：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/39K094g3gE.png?imageslim)
![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/gKFmH7lKlg.png?imageslim)
![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/3j13ek0aK0.png?imageslim)

<span style="color:red;">还是要自己跑一下，并且把全部的代码都总结进来。</span>

### 制作自己的标注数据

本书第 6 章最后曾实现了一个简单的标注小工具，考虑到灵活性，该小工具是用自定义的格式保存了标注信息。但其实基本上现在的物体检测算法大都是默认支持 PASCAL VOC 的格式，本节提供一个进行转换的小脚本，可以把小工具标注好的数据转换为 PASCAL VOC 支持的 XML 格式，方便各种主流框架下训练自己标注的数据。<span style="color:red;">嗯。</span>

标注信息其实就是个 XML：对于目标检测而言，需要的最小信息是 `<filename>` 、 `<size>`  和 `<object>` 。

- `<filename>` 就是标注对应的图片文件的名字；
- `<size>` 中包含 `<width>` 、 `<height>`  和 `<depth>` 分别是图片像素的宽、高和通道数；
- `<object>` 就是物体和对应标注框，其中 `<name>`  是物体的名称， `<bndbox>` 中 `<xmin>` 、 `<ymin>`、`<xmax>`、`<ymax>` 分别是左上角和右下角的像素位置坐标。

使用 标注工具，以及转化成 PASCAL VOC 格式的数据代码在 “计算机视觉CV-> 计算机视觉基础-> 数据与数据标注-> 数据标注” 文件夹中看到。

其中 detection_anno_bbox2voc.py 会把小工具生成的信息转化为 XML 标注信息。

用 Python 执行时第一个参数是包含图片和标注信息的文件夹，就可以根据第 6 章定义的后缀为 bbox 的标注信息，生成相应的 XML 标注信息并保存在同一文件夹下。




## 相关资料

- 《深度学习与计算机视觉》
- 简化版 VGG-16 模型，和官方已经训练好的一个模型： https://pan.baidu.com/s/1GCzJ1bqJza5CdpkmrCJ72g 密码：2nvs
