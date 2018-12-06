---
title: 10 用 MXNet 实现一个神经网络
toc: true
date: 2018-08-29
---

## 需要补充的

- 这部分安装的内容要放到工程实践流程里面。
- 对于 mxnet 的安装也要放到 mxnet 里面
- 对于 mxnet 的例子放到 mxnet 里面。



# 使用 MXNet 实现一个简单的神经网络

## 用MXNet实现一个两层神经网络


这一节我们用一个Hello World级别的神 经网络小例子带大家一起入门最基本的训练（Training）-预测（Inference）流程，以及 MXNet 这种框架的基本使用。

我们要用到的数据的二维可视化如下：

![mark](http://images.iterate.site/blog/image/180831/7FFJ7AFIkm.png?imageslim)

我们将通过 MXNet 的 model 模块搭建一个两层神经网络，网络结构如下：

![mark](http://images.iterate.site/blog/image/180831/2ba909hiCc.png?imageslim)


## 生成我们需要的数据

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

## 构建网络、训练、对某个值进行预测

完整代码如下：

```python
import pickle
import logging
import numpy as np
import mxnet as mx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the network
# 定义 data
data = mx.sym.Variable('data')
# data 经过一个两输出的全连接层
fc1 = mx.sym.FullyConnected(data=data, name='fc1', num_hidden=2)
# 再经过一个 sigmoid 激活层
sigmoid1 = mx.sym.Activation(data=fc1, name='sigmoid1', act_type='sigmoid')
# 然后再经过一个全连接层
fc2 = mx.sym.FullyConnected(data=sigmoid1, name='fc2', num_hidden=2)
# 最后经过 Softmax 输出，SoftmaxOutput 还自带 NLL 作为loss 进行计算
mlp = mx.sym.SoftmaxOutput(data=fc2, name='softmax')


# 网络结构可视化，基于 graphviz
shape = {'data': (2,)}
mlp_dot = mx.viz.plot_network(symbol=mlp, shape=shape)
mlp_dot.render('simple_mlp.gv', view=True)


# 接着，我们就开始读取数据来训练这个模型
# 用 pickle 读取数据
with open('../data.pkl', 'rb') as f:
    samples, labels = pickle.load(f)

# 设置 logging 级别，显示训练时候的信息
logging.getLogger().setLevel(logging.DEBUG)

# 对于这个简单例子，就用全量梯度下降法，整个数据集作为一个 batch
batch_size = len(labels)
samples = np.array(samples)
labels = np.array(labels)

# 生成训练数据迭代器
train_iter = mx.io.NDArrayIter(samples, labels, batch_size)

# 利用 mxnet.model.FeedForward.create 训练一个网络
# 迭代 1000 代，学习率 0.1，冲量系数 0.99
model = mx.model.FeedForward.create(
    symbol=mlp,
    X=train_iter,
    num_epoch=1000,
    learning_rate=0.1,
    momentum=0.99)

'''
# mxnet 也提供先设置好参数，然后通过 fit() 方法进行训练的方式。
model = mx.model.FeedForward(
    symbol=mlp,
    num_epoch=1000,
    learning_rate=0.1,
    momentum=0.99)
model.fit(X=train_iter)
'''

# 使用训练好的模型对一个点进行预测
print(model.predict(mx.nd.array([[0.5, 0.5]])))

# 接下来对所有样本和取值范围的平面进行分类，并画出对应的概率可视化的图

# 定义取值范围平面的采样格点，以 0.05 为间隔
X = np.arange(0, 1.05, 0.05)
Y = np.arange(0, 1.05, 0.05)
X, Y = np.meshgrid(X, Y)

# 按照模型可以接受的格式生成每个格点的坐标
grids = mx.nd.array([[X[i][j], Y[i][j]] for i in range(X.shape[0]) for j in range(X.shape[1])])
# 获取模型预测的结果，以标签 1 为结果
grid_probs = model.predict(grids)[:, 1].reshape(X.shape)

# 定义图标
fig = plt.figure('Sample Surface')
ax = fig.gca(projection='3d')

# 画出整个结果的表面
ax.plot_surface(X, Y, grid_probs, alpha=0.15, color='k', rstride=2, cstride=2, lw=0.5)

# 按照标签选出对应的样本
samples0 = samples[labels==0]
samples0_probs = model.predict(samples0)[:, 1]
samples1 = samples[labels==1]
samples1_probs = model.predict(samples1)[:, 1]

# 按照标签画出散点图，标签为 0 的是红色圆，标签为 1 的是蓝色三角
ax.scatter(samples0[:, 0], samples0[:, 1], samples0_probs, c='b', marker='^', s=50)
ax.scatter(samples1[:, 0], samples1[:, 1], samples1_probs, c='r', marker='o', s=50)

plt.show()
```

说明：

1. 在执行程序的时候，我们会得到如图7-2所示的结构图。
  ![mark](http://images.iterate.site/blog/image/180831/g95g1gk0BC.png?imageslim)

2. 我们用的是 mxnet.io.NDArrayIter 来生成一个用于遍历训练数据和对应标签的迭代器，然后用model进行训练。<span style="color:red;">是不是一定要用这个？</span>

3. 训练过程中可以看到实时输出的loss信息，每迭代完一代（epoch）就进行一次重 新设置：
```
INFO:root:Start training with [cpu (0)]
INFO:root:Epoch[0] Resetting Data Iterator
INFO:root:Epoch[0] Time cost=0.007
INFO:root:Epoch[1] Resetting Data Iterator
INFO:root:Epoch[1] Time cost=0.002
```

4. 我们会用训练好的模型对所有样本和取值范围的平面进行分类，并画出对应的三维的概率可视化的图如下：
  ![mark](http://images.iterate.site/blog/image/180831/AcJGk9GCl5.png?imageslim)

对于上面的程序有两个地方想知道：<span style="color:red;">SoftmaxOutput 还自带 NLL 作为loss 是什么意思？冲量系数是什么？了解下。</span>


注：这只是最简单的例子，目的是帮助了解 MXNet 的基本使用，并没有设置验证/测试集，训练迭代1000次也只是随便定的。7.2 节将用 Caffe 实现这个例子，而更加实际的例子会从第8章开始。<span style="color:red;">嗯。</span>
