---
title: 01 Keras 基于 Python 的深度学习库
toc: true
date: 2018-10-20
---
# 需要补充的

- 感觉一些东西可以拆分出去

# Keras:基于Python的深度学习库

## 这就是 Keras

Keras 是一个高层神经网络 API，Keras 由纯 Python 编写而成并基[Tensorflow](https://github.com/tensorflow/tensorflow)、[Theano](https://github.com/Theano/Theano)以及[CNTK](https://github.com/Microsoft/cntk)后端。<span style="color:red;">Tneano 和 CNTK 好像还没有用过，它们分别是在什么场景下使用的比较多？</span>

Keras 为支持快速实验而生，能够把你的 idea 迅速转换为结果，如果你有如下需求，请选择 Keras：

- 简易和快速的原型设计（keras具有高度模块化，极简，和可扩充特性）
- 支持 CNN 和 RNN，或二者的结合
- 无缝 CPU 和 GPU 切换。

<span style="color:red;">感觉上面这些特点 tensorflow 也有。</span>

Keras 适用的Python版本是：Python 2.7-3.6

Keras 的设计原则是

- 用户友好：Keras是为人类而不是天顶星人设计的API。用户的使用体验始终是我们考虑的首要和中心内容。Keras遵循减少认知困难的最佳实践：Keras 提供一致而简洁的 API， 能够极大减少一般应用下用户的工作量，同时，Keras提供清晰和具有实践意义的bug反馈。
- 模块性：模型可理解为一个层的序列或数据的运算图，完全可配置的模块可以用最少的代价自由组合在一起。具体而言，网络层、损失函数、优化器、初始化策略、激活函数、正则化方法都是独立的模块，你可以使用它们来构建自己的模型。<span style="color:red;">好东西，优化器是什么？</span>
- 易扩展性：添加新模块超级容易，只需要仿照现有的模块编写新的类或函数即可。创建新模块的便利性使得 Keras更适合于先进的研究工作。<span style="color:red;">怎样有易扩展性的？好想知道。</span>
- 与 Python 协作：Keras 没有单独的模型配置文件类型（作为对比，caffe有），模型由 python 代码描述，使其更紧凑和更易 debug，并提供了扩展的便利性。<span style="color:red;">是的，这个模型配置文件感觉是一个缺点吧，嗯，不知道，感觉这种模型配置文件给整个模型笼罩了一层迷雾。</span>


## 关于Keras-cn

本文档 包括[keras.io](http://keras.io/)的全部内容。


## 当前版本与更新

如果你发现本文档提供的信息有误，有两种可能：


## 快速开始：30s上手Keras

Keras 的核心数据结构是 “模型”，模型是一种组织网络层的方式。

Keras 中主要的模型是 Sequential 模型，Sequential 是一系列网络层按顺序构成的栈。你也可以查看[函数式模型](https://keras-cn.readthedocs.io/en/latest/getting_started/functional_API/)来学习建立更复杂的模型。<span style="color:red;">想看下，什么是函数式模型？怎么建立更复杂的模型的？什么是更复杂的模型？</span>

Sequential 模型如下

```python
from keras.models import Sequential
model = Sequential()
```

将一些网络层通过 `.add()` 堆叠起来，就构成了一个模型：

```python
from keras.layers import Dense, Activation

model.add(Dense(units=64, input_dim=100))
model.add(Activation("relu"))
model.add(Dense(units=10))
model.add(Activation("softmax"))
```

完成模型的搭建后，我们需要使用 `.compile()` 方法来编译模型：<span style="color:red;">模型的编译过程是在做什么？</span>

```python
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
```

编译模型时必须指明损失函数和优化器，如果你需要的话，也可以自己定制损失函数。<span style="color:red;">怎么定制损失函数？metrics 是什么？</span>

Keras 的一个核心理念就是简明易用，同时保证用户对 Keras 的绝对控制力度，用户可以根据自己的需要定制自己的模型、网络层，甚至修改源代码。

```python
from keras.optimizers import SGD
model.compile(loss='categorical_crossentropy',
              optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))
```

完成模型编译后，我们在训练数据上按 batch 进行一定次数的迭代来训练网络

```python
model.fit(x_train,
          y_train,
          epochs=5,
          batch_size=32)
```

<span style="color:red;">看起来真的很方便，很好。再明确下 epochs 和 batch_size 的意思。</span>

当然，我们也可以手动将一个个batch的数据送入网络中训练，这时候需要使用：<span style="color:red;">什么时候会要用到这个？</span>

```python
model.train_on_batch(x_batch,
                      y_batch)
```


随后，我们可以使用一行代码对我们的模型进行评估，看看模型的指标是否满足我们的要求：<span style="color:red;">嗯。</span>

```python
loss_and_metrics = model.evaluate(x_test,
                                  y_test,
                                  batch_size=128)
```


或者，我们可以使用我们的模型，对新的数据进行预测：

```python
classes = model.predict(x_test,
                        batch_size=128)
```

<span style="color:red;">predict 的时候，还有 batch_size 的吗？</span>

搭建一个问答系统、图像分类模型，或神经图灵机、word2vec 词嵌入器就是这么快。<span style="color:red;">真的吗？想知道到底是怎么搭建起来的。</span>

<span style="color:red;">Sequntial模型 和 函数式模型还是要好好学的。</span>

<span style="color:red;">Keras 自带的 examples 还是要系统的学习下的。有基于记忆网络的问答系统、基于LSTM的文本的文本生成等。嗯，都想知道。</span>


# 相关资料

- [Keras中文文档](https://keras-cn.readthedocs.io/en/latest/)
