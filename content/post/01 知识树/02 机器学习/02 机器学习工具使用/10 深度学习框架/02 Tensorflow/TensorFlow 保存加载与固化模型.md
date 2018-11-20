# 需要补充的



# Tensorflow 保存及加载模型的典型的3种方法




#### 1. 利用Saver

通常我们使用 TensorFlow保存模型时都使用ckpt格式的模型文件（实际上有4个文件）,模型的结构和数据是分离的。

##### 利用saver保存模型

``

```
#模型保存在.meta文件，变量保存在checkpoint文件
model_save_path = "./model/model_save"
saver = tf.train.Saver()
saver.save(sess, model_save_path)
利用saver加载模型try:
    # 恢复所有变量信息
    saver.restore(sess, tf.train.latest_checkpoint(model_save_path))
    print("成功加载模型参数")
except:
    # 如果是第一次运行，通过init加载并初始化变量
    print("未加载模型参数，第一次运行或者模型文件被删除")
    sess.run(tf.global_variables_initializer())
```

``

上面的方式在模型调试的时候可以使用，反正模型网络结构都已经定义在文件前面了，只是加载模型继续训练而已。如果需要另外new一个文件去加载模型，可以用下面的方式：

``

```
    sess = tf.Session()
    # 加载模型结构
    saver = tf.train.import_meta_graph("./model/model_save.meta")
    # 只需要指定目录就可以恢复所有变量信息
    saver.restore(sess, tf.train.latest_checkpoint(model_save_path))

    # 直接获取保存的变量
    print(sess.run("b:0"))

    # 获取placeholder变量
    input_x = sess.graph.get_tensor_by_name("input_x:0")
    input_y = sess.graph.get_tensor_by_name("input_y:0")
    # 获取需要进行计算的operator
    op = sess.graph.get_tensor_by_name("sum:0")

    # 加入新的操作
    add_on_op = tf.multiply(op, 2)

    print(sess.run(add_on_op, {input_x: 5, input_y: 5}))
```

``

#### 2.利用graph_util

谷歌推荐的保存模型的方式是固化模型参数并序列化为PB文件，它具有语言独立性，可独立运行，封闭的序列化格式，任何语言都可以解析它，它允许其他语言和深度学习框架读取、继续训练和迁移TensorFlow的模型。

它的主要使用场景是实现模型训练与模型预测的解耦。模型的参数和模型结构固化在一起，就可以迁移到需要的地方前向传播即可得到网络结果。

##### 保存 PB 文件


```
import tensorflow as tf
from tensorflow.python.framework import graph_util

with tf.Session(graph=tf.Graph()) as sess:
    x = tf.placeholder(tf.int32, name='input_x')
    y = tf.placeholder(tf.int32, name='input_y')
    b = tf.Variable(1, name='b')
    xy = tf.multiply(x, y)
    op = tf.add(xy, b, name='sum')
    # 初始化变量
    sess.run(tf.global_variables_initializer())

    # 测试 OP
    print(sess.run(op, feed_dict = {x: 10, y: 3}))

    # 固化需要用到的变量
    # 这里的输出需要加上name属性 需要指定output_node_names，可以多个
    constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ['sum'])

    # 写入序列化的PB文件
    with tf.gfile.FastGFile("./test/test.pb", mode='wb') as f:
        f.write(constant_graph.SerializeToString())

    # 输出
    # Converted 1 variables to const ops.
    # 31
```

``

##### 加载 PB 文件

``

```
with tf.Session() as sess:
    with tf.gfile.FastGFile("./test/test.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read()) #加载图
        # 从图上读取张量（第一种方法），同时把图设为默认图
        input_x,input_y,op=tf.import_graph_def(graph_def, return_elements=["input_x:0","input_y:0","sum:0"])

    # 需要有一个初始化的过程
    sess.run(tf.global_variables_initializer())

    print(sess.run(op,  feed_dict={input_x: 5, input_y: 5}))
    #26
```

#### 3. 利用builder

##### 利用builder保存模型


```
with tf.Session(graph=tf.Graph()) as sess:
    x = tf.placeholder(tf.int32, name='input_x')
    y = tf.placeholder(tf.int32, name='input_y')
    b = tf.Variable(1, name='b')
    xy = tf.multiply(x, y)
    op = tf.add(xy, b, name="sum")

    sess.run(tf.global_variables_initializer())

    constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ["sum"])

    # 测试 OP
    feed_dict = {x: 10, y: 3}
    print(sess.run(op, feed_dict))

    # 构造器，模型保存的路径
    builder = tf.saved_model.builder.SavedModelBuilder("./test/savemodel")

    # 保存sess，标签，输入输出映射
    builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING])
    # 保存为PB模型
    builder.save()
```


保存好以后到saved_model_dir目录下，会有一个saved_model.pb文件以及variables文件夹。顾名思义，variables保存所有变量，saved_model.pb用于保存模型结构等信息。

##### 利用builder加载模型


```
with tf.Session(graph=tf.Graph()) as sess:
    # 依标签加载模型
    tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], "./test/savemodel")
    # 初始化变量
    sess.run(tf.global_variables_initializer())
    # 查看图中的op
    for op in sess.graph.get_operations():
        print(op.name,op.values())
    # 获取张量的第二种方法
    input_x = sess.graph.get_tensor_by_name('input_x:0')
    input_y = sess.graph.get_tensor_by_name('input_y:0')
    op = sess.graph.get_tensor_by_name('sum:0')
    # 在模型中前向传播
    ret = sess.run(op,  feed_dict={input_x:5,input_y:5})
    print(ret)
```


只需要指定要恢复模型的session，模型的 tag，模型的保存路径即可,使用起来比第一种方法简单

#### 总结

- 如果需要迁移模型，例如使用opencv运行tensorflow模型，就需要将模型的参数和模型结构固化到一起并序列化为.pb文件，也就是使用第二种方式。
- 第一种和第三种方法都将模型结构和模型参数分离了，并且依赖于tensorflow框架。
- 总体建议日常还是将模型保存为pb文件。




# 相关资料

- [TensorFlow 保存模型为 PB 文件](https://zhuanlan.zhihu.com/p/32887066)
- [TensorFlow 保存加载与固化模型](https://me.aimao.co/2018/05/tensorflow-save-load-frezen-model/)
