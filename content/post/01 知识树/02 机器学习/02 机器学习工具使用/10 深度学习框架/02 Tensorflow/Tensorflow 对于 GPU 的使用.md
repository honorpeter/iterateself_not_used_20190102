---
title: Tensorflow 对于 GPU 的使用
toc: true
date: 2018-10-13
---
# 需要补充的

# Tensorflow 对于 GPU 的使用

## 使用指定的 GPU 及 GPU 显存

这个还是经常要用到的。

指定 GPU 的地方有两种：

- 在终端程序执行的时候指定
- 在 Python 代码中指定

### 终端执行程序时设置使用的GPU

如果电脑有多个 GPU，Tensorflow 默认全部使用。如果想只使用部分 GPU，可以设置 CUDA_VISIBLE_DEVICES。


在调用python程序时，可以使用：<span style="color:red;">这个还没用过。</span>

```
CUDA_VISIBLE_DEVICES=1 python my_script.py
```


CUDA_VISIBLE_DEVICES 参数说明：

```
Environment Variable Syntax      Results

CUDA_VISIBLE_DEVICES=1           Only device 1 will be seen
CUDA_VISIBLE_DEVICES=0,1         Devices 0 and 1 will be visible
CUDA_VISIBLE_DEVICES="0,1"       Same as above, quotation marks are optional
CUDA_VISIBLE_DEVICES=0,2,3       Devices 0, 2, 3 will be visible; device 1 is masked
CUDA_VISIBLE_DEVICES=""          No GPU will be visible
```

### python代码中设置使用的GPU

如果要在 Python 代码中设置使用的 GPU（如使用 Pycharm 进行调试时），可以使用下面的代码：

```python
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
```





## 设置 Tensorflow 使用的显存的大小

有两种方式：

- 定量设置显存
- 按需设置显存


### 定量设置显存

默认 Tensorflow 是使用 GPU 尽可能多的显存。可以通过下面的方式，来设置使用的 GPU 显存：<span style="color:red;">想知道这个定量设置显存一般是在什么时候使用？</span>

```python
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
```

上面分配给 Tensorflow 的 GPU 显存大小为：`GPU 实际显存 * 0.7`。

可以按照需要，设置不同的值，来分配显存。


### 按需设置显存

上面的只能设置固定的大小。如果想按需分配，可以使用 `allow_growth` 参数：

```python
gpu_options = tf.GPUOptions(allow_growth=True)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
```




## 检测 Tensorflow 是不是在使用 GPU 进行计算

对 conda 里面环境进行安装的时候，可能是把 原来的 GPU 的tensorflow 替换成了 CPU 的 tensorflow ，因为感觉模型跑的速度与正常的 CPU 跑的时候差的不是很多。

而一般来说，GPU 与 CPU 在跑模型的时候速度差别大概是 30 倍以上。

因此，就想验证下，到底现在用的是 CPU 还是 GPU。

可以用这个脚本进行验证：



```python
import numpy
import tensorflow as tf
a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
c = tf.matmul(a, b)
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
print(sess.run(c))
```

之后就会出现详细信息：

```
Device mapping:
/job:localhost/replica:0/task:0/device:GPU:0 -> device: 0, name: Tesla K40c, pci bus
id: 0000:05:00.0
b: /job:localhost/replica:0/task:0/device:GPU:0
a: /job:localhost/replica:0/task:0/device:GPU:0
MatMul: /job:localhost/replica:0/task:0/device:GPU:0
[[ 22.  28.]
 [ 49.  64.]]
```

可以看到，使用的是 GPU ，名字是 Tesla K40c 。

其实关键的就是这个：

```
import tensorflow as tf
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
```


日志信息若包含 GPU 信息，就是使用了 GPU。

当然，我们也可以在跑模型的时候通过 `nvidia-smi` 命令来查看 GPU 的内存使用量。





# 相关资料

- [（原）tensorflow中使用指定的GPU及GPU显存](https://www.cnblogs.com/darkknightzh/p/6591923.html)
- [确定自己的TensorFlow是CPU还是GPU的版本](https://blog.csdn.net/Zlase/article/details/79261348)
- [检测tensorflow是否使用gpu进行计算](https://blog.csdn.net/castle_cc/article/details/78389082)
