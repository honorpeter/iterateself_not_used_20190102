---
title: 03 准备 Caffe 要用的数据
toc: true
date: 2018-09-01
---


# 准备 Caffe 要用到的数据


# 制作 LMDB 数据

LMDB 是 Caffe 中最常用的一种数据库格式，全称 Lightning Memory-Mapped Database，直译就是闪电般快速的内存映射型数据库。除了快，LMDB 还支持多程序同时对数据进行读取，这是相比 Caffe 更早支持的 LevelDB 的优点。现在 LMDB 差不多是 Caffe 用来训练图片最常用的数据格式。<span style="color:red;">嗯，这个 LMDB 之前从来没听说过。</span>

Caffe 提供了专门为图像分类任务将图片转换为 LMDB 的官方工具，路径为 caffe/build/tools/convert_imageset。要使用这个工具，第一部是生成一个图片文件路径的列表，每一行是文件路径和对应标签(的下标)，用 space 键或者制表符(Tab)分开，格式例子如下：<span style="color:red;">对应的标签是什么意思？嗯，就是 label 的意思。好吧</span>

```
mnist_images/val/000000_3.jpg 3
mnist_images/val/000001_8.jpg 8
mnist_images/val/000002_6.jpg 6
...
```

在8.1节中已经在 mnist 文件夹下生成了 3个文件夹，分别是 train、val 和 test，分别包含训练图片、验证图片和测试图片。接下来要把这些图片的路径和对应标签，也就是数字的值转化为上面的格式，因为文件名字中下画线分开的第 2 个字段就是标签，所以用如下代码可以实现。

gen_caffe_imglist.py：

```python
import os
import sys

# 输入路径，是包含 mnist 图片文件的路径
input_path = sys.argv[1].rstrip(os.sep)
# 输出的文件名，内容就是图片路径-标签的列表
output_path = sys.argv[2]
# 列出输入路径下所有的文件名
filenames = os.listdir(input_path)

with open(output_path, 'w') as f:
    for filename in filenames:
        # 完整的图片文件路径
        filepath = os.sep.join([input_path, filename])
        # 第 2 个字段的值就是标签
        label = filename[:filename.rfind('.')].split('_')[1]
        # 生成 路径-标签 的格式并写入文件
        line = '{} {}\n'.format(filepath, label)
        f.write(line)

```

说明：

1. <span style="color:red;">`sys.argv[1]` 没想到这么方便就使用了传参，厉害。嗯，</span>
2. <span style="color:red;">`rstrip(os.sep)` 考虑的非常周到，把多余的 sep 去掉。</span>
3. <span style="color:red;">`label = filename[:filename.rfind('.')].split('_')[1]` 细腻的把想要的标签号从名称中截取了出来。非常好，对于路径的各种处理方式还是要详细的总结下的，因为这个一般会经常的使用。无论是从文本名中提取某种信息，还是提取文本的某种属性信息比如修改时间什么的。</span>


OK，这样我们在控制台下依次执行下面命令就能生成我们要的文本了：

```
python gen_caffe_imglist.py mnist/train train.txt
python gen_caffe_imglist.py mnist/val val.txt
python gen_caffe_imglist.py mnist/test test.txt
```

这样，我们就生成了 3 个数据集的文件列表和对应标签。然后直接调用 convert_imageset 就 可以制作 lmdb 了。

```
/path/to/caffe/build/tools/convert_imageset ./ train.txt train_lmdb --gray --shuffle
/path/to/caffe/build/tools/convert_imageset ./ val.txt val_lmdb --gray --shuffle
/path/to/caffe/build/tools/convert_imageset ./ test.txt test_lmdb --gray --shuffle
```

<span style="color:red;">对这个 `convert_imageset` 也要总结下，比如他的参数什么的。</span>

其中 `--gray` 是单通道读取灰度图的选项，`--shuffle` 是个常用的选项，作用是打乱文件列表顺序，但是在本例中其实是可有可无的，因为本来就是乱序的。<span style="color:red;">嗯。</span>

执行这个工具其实就是读取图片为 OpenCV 的 Mat，然后保存到lmdb里。更多convert imageset的用法可以执行下面命令或者参考源码：

```
/path/to/caffe/built/tools/convert_imageset -h
```

<span style="color:red;">嗯，要总结下 `convert_imageset`</span>


## 对数据进行增强

关于数据增强的方式，见 计算机视觉CV-计算机视觉基础-视觉项目优化 文件夹里有。

### 增加平移和旋转扰动

在第 6 章中已经实现过一个简单的利用扰动增加数据的小工具，这个工具对 MNIST 是否有用呢？本节一起来试一下。MNIST 的特点是单通道灰度图，同时每个数字都是已经经过了对齐在画面中心的处理。然而每个人写字都是没有固定规则的，什么样算是在中心很难定义，并且字体的歪斜和“胖瘦”程度也是难以界定的，所以考虑利用平移和旋转对数据进行增加。<span style="color:red;">嗯，看来数据增加是经常要做的。</span>

用第 6 章实现过的小工具，关闭除了裁剪和旋转以外的一切选项，旋转范围设定为正负 15° 之间。把训练集增加为原来的 6 倍，在控制台执行如下命令：

```
pythona run_augmentation.py mnist/train/ mnist/augmented 250000 --rotate_angle_vari=15 --p_mirror=0 --p_hsv=0 --p_gamma=0
```

注：`run_augmentation.py` 在 计算机视觉CV-计算机视觉基础-视觉项目优化 文件夹里有写到。

这样会在 mnist 下生成一个 augmented 的文件夹，包含 25 万张扰动后的图片，并且这些图片的命名规则也符合 gen_caffe_imglist.py 的解析规则。所以接下来执行生成图片列表文件的命令：

```
python gen_caffe_imglist.py mnist/augmented augmented.txt
```

然后把原始训练集和新增加的文件列表合并：

```
cat train.txt augmented.txt > train_aug.txt
```

<span style="color:red;">嗯，这就是大家都喜欢用 Linux 的原因吧，因为有一些工具和指令可以比较方便的对一些东西进行操作。这个在 windows 下不知道该怎么做？写一个 py 脚本还是也可以这么写？</span>

就得到了包含 30 万张图片列表的文件，然后为这个文件单独建立一个 lmdb：

```
/path/to/caffe/built/tools/convert_imageset  ./  train_aug.txt  train_aug_lmdb --resize_width=28 --resize_height=28 --gray --shuffle
```

注意，因为扰动后的图片分辨率不一定是 28x28 了，所以必须在这里用 `resize_width` 和 `resize_height` 的选项把写入 lmdb 的图像大小固定，另外因为用 cat 合并的文件前 5 万张是原始文件，后面都是增加的，所以 `shuffle` 选项也变成了必须项。




## 相关资料

- 《深度学习与计算机视觉》
