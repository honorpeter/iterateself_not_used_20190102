---
title: Caffe
toc: true
date: 2018-09-01
---
## Caffe的基本概念

Caffe 从本质上来说和 MXNet 中 Symbolic 的使用方式差不多，都是先定义好一个计算关系，然后根据这个计算关系结合数据训练和使用模型。在 Caffe 中，最基本的计算节点是层(Layer)，所有的计算关系都是基于层的，无论是 Caffe 预定义好的层，还是用户自定义的层。这和 MXNet 中预定义层的使用方式也很像，如果直接基于 Python 写层的定义就更像了。不过这里我们要了解的是更常用的一种使用方式，即利用 protobuf 的格式而不是代码来定义网络的结构，然后再结合数据进行训练，也就是说用 Caffe 训练模型是不需要写代码的。这体现了 Caffe 设计哲学中利用表达式(expression)和模块化(Modularity)的特点。<span style="color:red;">为什么体现了利用表达式和模块化的特点？</span>

Caffe 中预定义的层覆盖了当前流行的网络结构中几乎所有的类型，比如卷积神经网络最常用到的全连接层(InnerProduct)、卷积层(Convolution)和池化层(Pooling)；各种各样的激活函数层(ReLU、Sigmoid、PReLU等)；以及数据交互的各种层(Data、HDF5Data、 ImageData 等)；输出及计算损失函数的层(Softmax、SoftmaxWithLoss、 Euclidean 等)。 除了 Caffe的接口文档，各种常用层的信息一览在 Caffe 官网也有列出地址为 http://caffe.berkeleyvision.org/tutorial/layers.html 。<span style="color:red;">嗯，需要好好总结下。</span>

基于各种层就可以构建成网络(Net)，然后定义好数据，就可以训练一个模型了。在 Caffe 中，数据的形式是一种叫 Blob 的类，其实就是空间连续的多维数组，比如存储图像的时候是个四维的数组，四个维度分别是批大小、通道数、图像高度、图像宽度。有了网络结构和数据之后，再定义一个利用梯度下降法做优化的 Solver 模块，就可以训练网络了。 具体总结如下。

- 层 (Layer)
- 网络 (Net)
- 数据 (Blob)
- 梯度下降 (Solver)

这 4 个部分就是入门学习最关键的内容。
