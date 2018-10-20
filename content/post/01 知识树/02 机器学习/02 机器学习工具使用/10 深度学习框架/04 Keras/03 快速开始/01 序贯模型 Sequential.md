---
title: 01 序贯模型 Sequential
toc: true
date: 2018-10-20
---
# 需要补充的

- 还是有很多东西不是很明白。

# 快速开始序贯（Sequential）模型

序贯模型是多个网络层的线性堆叠，也就是 “一条路走到黑”。

可以通过向 `Sequential` 模型传递一个 layer 的 list 来构造该模型：

```python
from keras.models import Sequential
from keras.layers import Dense, Activation

model = Sequential([
                    Dense(32, units=784),
                    Activation('relu'),
                    Dense(10),
                    Activation('softmax'),
                    ])
```

也可以通过 `.add()` 方法一个个的将layer加入模型中：

```python
model = Sequential()
model.add(Dense(32, input_shape=(784,)))
model.add(Activation('relu'))
```


## 指定输入数据的shape <span style="color:red;">这个地方没看懂</span>

模型需要知道输入数据的 shape，因此，`Sequential` 的第一层需要接受一个关于输入数据shape的参数，后面的各个层则可以自动的推导出中间数据的shape，因此不需要为每个层都指定这个参数。<span style="color:red;">嗯。</span>

有几种方法来为第一层指定输入数据的 shape：<span style="color:red;">没看懂。</span>

* 传递一个```input_shape```的关键字参数给第一层，```input_shape```是一个tuple类型的数据，其中也可以填入```None```，如果填入```None```则表示此位置可能是任何正整数。数据的 batch 大小不应包含在其中。
* 有些 2D 层，如```Dense```，支持通过指定其输入维度```input_dim```来隐含的指定输入数据 shape，是一个 Int 类型的数据。一些 3D 的时域层支持通过参数 ```input_dim``` 和 ```input_length``` 来指定输入shape。
* 如果你需要为输入指定一个固定大小的 batch_size（常用于stateful RNN网络），可以传递```batch_size```参数到一个层中，例如你想指定输入张量的batch大小是32，数据shape是（6，8），则你需要传递```batch_size=32```和```input_shape=(6,8)```。



```python
model = Sequential()
model.add(Dense(32, input_dim=784))
```

```python
model = Sequential()
model.add(Dense(32, input_shape=(784,)))
```


## 编译

在训练模型之前，我们需要通过```compile```来对学习过程进行配置。```compile```接收三个参数：

* 优化器 optimizer：该参数可指定为已预定义的优化器名，如```rmsprop```、```adagrad```，或一个```Optimizer```类的对象。
* 损失函数 loss：该参数为模型试图最小化的目标函数，它可为预定义的损失函数名，如```categorical_crossentropy```、```mse```，也可以为一个损失函数。
* 指标列表 metrics：对分类问题，我们一般将该列表设置为```metrics=['accuracy']```。指标可以是一个预定义指标的名字，也可以是一个用户定制的函数。指标函数应该返回单个张量，或一个完成 `metric_name - > metric_value` 映射的字典。<span style="color:red;">这个指标列表 metrics 是起到什么作用？</span>


```python
# For a multi-class classification problem
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# For a binary classification problem
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# For a mean squared error regression problem
model.compile(optimizer='rmsprop',
              loss='mse')

# For custom metrics
import keras.backend as K

def mean_pred(y_true, y_pred):
    return K.mean(y_pred)

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy', mean_pred])
```

<span style="color:red;">上面这个最后的 mean_pred 没明白，这个不是预测的数的均值吗？为什么作为 accuracy？</span>


## 训练

Keras 以 Numpy 数组作为输入数据和标签的数据类型。训练模型一般使用```fit```函数。

下面是一些例子:

一个二分类问题：

```python
# For a single-input model with 2 classes (binary classification):
from keras.models import Sequential
from keras.layers import Dense


model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Generate dummy data
import numpy as np
data = np.random.random((1000, 100))
labels = np.random.randint(2, size=(1000, 1))

# Train the model, iterating on the data in batches of 32 samples
print(model.fit(data, labels, epochs=1100, batch_size=32))
```

输出的一部分:

```
Epoch 883/1100

32/1000 [..............................] - ETA: 0s - loss: 2.8313e-06 - acc: 1.0000
1000/1000 [==============================] - 0s 31us/step - loss: 1.9177e-06 - acc: 1.0000
```

<span style="color:red;">这个输出有点没看懂。</span>

一个多分类问题：

```python
# For a single-input model with 10 classes (categorical classification):
from keras.models import Sequential
from keras.layers import Dense
import keras

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Generate dummy data
import numpy as np

data = np.random.random((1000, 100))
labels = np.random.randint(10, size=(1000, 1))

# Convert labels to categorical one-hot encoding
one_hot_labels = keras.utils.to_categorical(labels, num_classes=10)

# Train the model, iterating on the data in batches of 32 samples
print(model.fit(data, one_hot_labels, epochs=1000, batch_size=32))
```

这个输出好像有点问题：

之前用 1.2 版本的 tensorflow 有点问题：

```
TypeError: softmax() got an unexpected keyword argument 'axis'
```

因此使用了 1.8 版本的tensorflow ，好了，部分输出如下：

```
...
Epoch 528/1000

32/1000 [..............................] - ETA: 0s - loss: 0.1717 - acc: 1.0000
1000/1000 [==============================] - 0s 22us/step - loss: 0.1358 - acc: 0.9990
...
```

<span style="color:red;">嗯，不错，keras.utils.to_categorical 也不错。</span>


## 例子

这里是一些帮助你开始的例子

在 Keras 代码包的 examples 文件夹中，你将找到使用真实数据的示例模型：

* CIFAR10 小图片分类：使用CNN和实时数据提升
* IMDB 电影评论观点分类：使用LSTM处理成序列的词语
* Reuters（路透社）新闻主题分类：使用多层感知器（MLP）
* MNIST 手写数字识别：使用多层感知器和CNN
* 字符级文本生成：使用LSTM
...

<span style="color:red;">都要总结进来。</span>

### 基于多层感知器的 softmax 多分类：

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import keras

# Generate dummy data
import numpy as np

x_train = np.random.random((1000, 20))
y_train = keras.utils.to_categorical(np.random.randint(10, size=(1000, 1)), num_classes=10)
x_test = np.random.random((100, 20))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(64, activation='relu', input_dim=20))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01,
          decay=1e-6,
          momentum=0.9,
          nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=100,
          batch_size=128)


print("***")
score = model.evaluate(x_test,
                       y_test,
                       batch_size=128)
print(score)
```

部分输出：

```
Epoch 99/100

 128/1000 [==>...........................] - ETA: 0s - loss: 2.2526 - acc: 0.1484
1000/1000 [==============================] - 0s 14us/step - loss: 2.2779 - acc: 0.1530
Epoch 100/100

 128/1000 [==>...........................] - ETA: 0s - loss: 2.2465 - acc: 0.1562
1000/1000 [==============================] - 0s 14us/step - loss: 2.2755 - acc: 0.1450
***

100/100 [==============================] - 0s 350us/step
[2.3050098419189453, 0.11999999731779099]
```




### MLP的二分类：

```python
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout

# Generate dummy data
x_train = np.random.random((1000, 20))
y_train = np.random.randint(2, size=(1000, 1))
x_test = np.random.random((100, 20))
y_test = np.random.randint(2, size=(100, 1))

model = Sequential()
model.add(Dense(64, input_dim=20, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model.fit(x_train,
          y_train,
          epochs=100,
          batch_size=128)
print("***")
score = model.evaluate(x_test,
                       y_test,
                       batch_size=128)
print(score)
```

部分输出：

```
Epoch 99/100

 128/1000 [==>...........................] - ETA: 0s - loss: 0.6388 - acc: 0.6406
1000/1000 [==============================] - 0s 13us/step - loss: 0.6555 - acc: 0.6130
Epoch 100/100

 128/1000 [==>...........................] - ETA: 0s - loss: 0.6563 - acc: 0.6250
1000/1000 [==============================] - 0s 13us/step - loss: 0.6582 - acc: 0.6120
***

100/100 [==============================] - 0s 360us/step
[0.70203381776809692, 0.52999997138977051]
```



### 类似VGG的卷积神经网络：

<span style="color:red;">这个例子还真的挺好的，信手拈来的感觉，有些厉害。</span>

```python
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD

# Generate dummy data
x_train = np.random.random((200, 100, 100, 3))
y_train = keras.utils.to_categorical(np.random.randint(10, size=(200, 1)), num_classes=10)
x_test = np.random.random((20, 100, 100, 3))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)

model = Sequential()
# input: 100x100 images with 3 channels -> (100, 100, 3) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01,
          decay=1e-6,
          momentum=0.9,
          nesterov=True)  # 这个 nesterov 是什么？

model.compile(loss='categorical_crossentropy',
              optimizer=sgd)  # 为什么没有 metrics ？

model.fit(x_train,
          y_train,
          batch_size=32,
          epochs=10)
print("***")
score = model.evaluate(x_test,
                       y_test,
                       batch_size=32)
print(score)

```

部分输出：

```
Epoch 9/10

 32/200 [===>..........................] - ETA: 6s - loss: 2.3001
 64/200 [========>.....................] - ETA: 5s - loss: 2.2850
 96/200 [=============>................] - ETA: 4s - loss: 2.2847
128/200 [==================>...........] - ETA: 3s - loss: 2.2686
160/200 [=======================>......] - ETA: 1s - loss: 2.2763
192/200 [===========================>..] - ETA: 0s - loss: 2.2823
200/200 [==============================] - 9s 43ms/step - loss: 2.2832
Epoch 10/10

 32/200 [===>..........................] - ETA: 7s - loss: 2.2554
 64/200 [========>.....................] - ETA: 5s - loss: 2.2685
 96/200 [=============>................] - ETA: 4s - loss: 2.2522
128/200 [==================>...........] - ETA: 3s - loss: 2.2682
160/200 [=======================>......] - ETA: 1s - loss: 2.2649
192/200 [===========================>..] - ETA: 0s - loss: 2.2829
200/200 [==============================] - 9s 43ms/step - loss: 2.2914
***

20/20 [==============================] - 0s 16ms/step
2.34389066696
```

感觉这个看的还是听清楚的，9s 一个 epoch，处理每张图片的时间大概是  44ms，因为是随机生成的图像数据，所以 loss 一直没怎么降。

最后预测的时候，20 张图片，用了不到 1s，每张图片大概用了 16ms。<span style="color:red;">不知道这个地方我理解的对不对。</span>




### 使用LSTM的序列分类

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM

model = Sequential()
model.add(Embedding(max_features, output_dim=256))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=16, epochs=10)
score = model.evaluate(x_test, y_test, batch_size=16)
```

<span style="color:red;">这个例子不完整，找一下完整的例子在哪里。可以提一个 issus 问一下。</span>

### 使用1D卷积的序列分类

```python
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D

model = Sequential()
model.add(Conv1D(64, 3, activation='relu', input_shape=(seq_length, 100)))
model.add(Conv1D(64, 3, activation='relu'))
model.add(MaxPooling1D(3))
model.add(Conv1D(128, 3, activation='relu'))
model.add(Conv1D(128, 3, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=16, epochs=10)
score = model.evaluate(x_test, y_test, batch_size=16)
```

<span style="color:red;">这个例子也不完整，这个 x_train 是什么？</span>
<span style="color:red;">以前好像还没有见到过 一维的卷积，嗯，这个一般在什么时候使用呢？</span>


### 用于序列分类的栈式LSTM

在该模型中，我们将三个 LSTM 堆叠在一起，是该模型能够学习更高层次的时域特征表示。<span style="color:red;">为什么堆叠的 LSTM 能够学习到更高层次的时域特征表示？</span>

开始的两层 LSTM 返回其全部输出序列，而第三层 LSTM 只返回其输出序列的最后一步结果，从而其时域维度降低（即将输入序列转换为单个向量）。<span style="color:red;">没明白？</span>

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181020/dd44K3GjAg.png?imageslim)

```python
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

data_dim = 16
timesteps = 8
num_classes = 10

# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
model.add(LSTM(32,
               return_sequences=True,
               input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32,
               return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32))  # return a single vector of dimension 32
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Generate dummy training data
x_train = np.random.random((1000, timesteps, data_dim))
y_train = np.random.random((1000, num_classes))

# Generate dummy validation data
x_val = np.random.random((100, timesteps, data_dim))
y_val = np.random.random((100, num_classes))

model.fit(x_train,
          y_train,
          batch_size=64,
          epochs=5,
          validation_data=(x_val, y_val))
```

部分输出：

```
Epoch 5/5

  64/1000 [>.............................] - ETA: 0s - loss: 11.5359 - acc: 0.0781
 448/1000 [============>.................] - ETA: 0s - loss: 11.5902 - acc: 0.1183
 832/1000 [=======================>......] - ETA: 0s - loss: 11.6615 - acc: 0.1142
1000/1000 [==============================] - 0s 146us/step - loss: 11.6525 - acc: 0.1170 - val_loss: 11.5541 - val_acc: 0.0500
```

<span style="color:red;">嗯，对于验证集的使用，还是不错的，可以方便的看出当前模型是否过拟合。</span>

### 采用 stateful LSTM 的相同模型

stateful LSTM的特点是，在处理过一个 batch 的训练数据后，其内部状态（记忆）会被作为下一个 batch 的训练数据的初始状态。

<span style="color:red;">还是有点没理解，普通的模型也会在 一个 batch 之后更新权重，那么内部状态是什么意思？对于上面那个程序来说，它在训练一个 新的 batch 的时候，内部的状态是清零的，而这个 stateful LSTM ，内部的状态却是不清零的，是吗？</span>

状态 LSTM 使得我们可以在合理的计算复杂度内处理较长序列。<span style="color:red;">为什么能够在合理的计算复杂度内处理较长序列？上面的LSTM 的方法处理较长序列复杂度会很高吗？</span>


```python
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

data_dim = 16
timesteps = 8
num_classes = 10
batch_size = 32

# Expected input batch shape: (batch_size, timesteps, data_dim)
# Note that we have to provide the full batch_input_shape since the network is stateful.
# the sample of index i in batch k is the follow-up for the sample i in batch k-1.
model = Sequential()
model.add(LSTM(32,
               return_sequences=True,
               stateful=True,
               batch_input_shape=(batch_size, timesteps, data_dim)))
model.add(LSTM(32,
               return_sequences=True,
               stateful=True))
model.add(LSTM(32,
               stateful=True))
model.add(Dense(10,
                activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Generate dummy training data
x_train = np.random.random((batch_size * 10, timesteps, data_dim))
y_train = np.random.random((batch_size * 10, num_classes))

# Generate dummy validation data
x_val = np.random.random((batch_size * 3, timesteps, data_dim))
y_val = np.random.random((batch_size * 3, num_classes))

model.fit(x_train,
          y_train,
          batch_size=batch_size,
          epochs=5,
          shuffle=False,
          validation_data=(x_val, y_val))
```


部分输出：

```
Epoch 4/5

 32/320 [==>...........................] - ETA: 0s - loss: 11.8298 - acc: 0.0312
320/320 [==============================] - 0s 175us/step - loss: 11.5966 - acc: 0.1000 - val_loss: 11.6352 - val_acc: 0.1458
Epoch 5/5

 32/320 [==>...........................] - ETA: 0s - loss: 11.8293 - acc: 0.0625
320/320 [==============================] - 0s 187us/step - loss: 11.5959 - acc: 0.1031 - val_loss: 11.6354 - val_acc: 0.1250
```

<span style="color:red;">为什么这个地方 shuffle 设定为 False？ </span>

<span style="color:red;">对这个 stateful LSTM 还是不是很理解。</span>



# 相关资料

- [Keras中文文档](https://keras-cn.readthedocs.io/en/latest/)
