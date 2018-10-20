---
title: 04 Keras 使用陷阱
toc: true
date: 2018-10-20
---
# 需要补充的

- 嗯，需要不断补充。总结。

# Keras使用陷阱

这里归纳了 Keras 使用过程中的一些常见陷阱和解决方法，如果你的模型怎么调都搞不对，可能需要注意下。



## TF卷积核与TH卷积核

Keras 提供了两套后端，Theano 和 Tensorflow，这是一件幸福的事，就像手中拿着馒头，想蘸红糖蘸红糖，想蘸白糖蘸白糖

如果你从无到有搭建自己的一套网络，则大可放心。但如果你想使用一个已有网络，或把一个用 th/tf 训练的网络以另一种后端应用，在载入的时候你就应该特别小心了。

卷积核与所使用的后端不匹配，不会报任何错误，因为它们的 shape 是完全一致的，没有方法能够检测出这种错误。

在使用预训练模型时，一个建议是首先找一些测试样本，看看模型的表现是否与预计的一致。

如需对卷积核进行转换，可以使用 utils.convert_all_kernels_in_model 对模型的所有卷积核进行转换。

<span style="color:red;">暂时还没遇到，不知道这是一种什么情况。</span>

## 向BN层中载入权重

如果你不知道从哪里淘来一个预训练好的 BN 层，想把它的权重载入到 Keras 中，要小心参数的载入顺序。

一个典型的例子是，将 caffe 的 BN 层参数载入 Keras 中，caffe 的 BN 由两部分构成，bn 层的参数是 mean，std，scale 层的参数是 gamma，beta

按照BN的文章顺序，似乎载入 Keras BN 层的参数应该是[mean, std, gamma, beta]

然而不是的，Keras 的 BN 层参数顺序应该是 [gamma, beta, mean, std]，这是因为 gamma 和 beta 是可训练的参数，而 mean 和 std 不是

Keras的可训练参数在前，不可训练参数在后。

错误的权重顺序不会引起任何报错，因为它们的 shape 完全相同。

<span style="color:red;">不知道，但是从 caffe 导入到 Keras 还是有可能的。</span>

## shuffle和validation_split的顺序

模型的 fit 函数有两个参数，shuffle 用于将数据打乱，validation_split 用于在没有提供验证集的时候，按一定比例从训练集中取出一部分作为验证集

这里有个陷阱是，程序是先执行validation_split，再执行shuffle的，所以会出现这种情况：

假如你的训练集是有序的，比方说正样本在前负样本在后，又设置了 validation_split，那么你的验证集中很可能将全部是负样本

同样的，这个东西不会有任何错误报出来，因为 Keras 不可能知道你的数据有没有经过 shuffle，保险起见如果你的数据是没shuffle过的，最好手动 shuffle 一下。

<span style="color:red;">嗯，还是要手动 shuffle 一下的。</span>

## Merge 层的层对象与函数方法

Keras 定义了一套用于融合张量的方法，位于 keras.layers.Merge，里面有两套工具，以大写字母开头的是 Keras Layer 类，使用这种工具是需要实例化一个 Layer 对象，然后再使用。以小写字母开头的是张量函数方法，本质上是对 Merge Layer 对象的一个包装，但使用更加方便一些。注意辨析。<span style="color:red;">这也可以，Merge 一般什么时候使用？</span>



# 相关资料

- [Keras中文文档](https://keras-cn.readthedocs.io/en/latest/)
