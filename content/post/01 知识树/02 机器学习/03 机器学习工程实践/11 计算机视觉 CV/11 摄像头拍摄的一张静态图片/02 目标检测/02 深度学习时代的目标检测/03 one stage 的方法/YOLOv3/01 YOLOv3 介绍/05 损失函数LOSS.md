# 第5篇，损失函数Loss

精巧地设计，中心点、宽高、框置信度和类别置信度等4个部分的损失值，这是训练过程的最后一篇。当然还有第6篇，至第n篇，毕竟，这是一个完整版 ：）。


## 1. 损失层

在模型的训练过程中，不断调整网络中的参数，优化损失函数 loss 的值达到最小，完成模型的训练。在YOLO v3中，损失函数yolo_loss封装自定义Lambda的损失层中，作为模型的最后一层，参于训练。损失层Lambda的输入是已有模型的输出 model_body.output 和真值 y_true，输出是 1 个值，即损失值。

损失层的核心逻辑位于 yolo_loss 中，yolo_loss 除了接收 Lambda 层的输入 model_body.output和 y_true，还接收锚框 anchors、类别数 num_classes 和过滤阈值 ignore_thresh 等3个参数。

实现：

```python
model_loss = Lambda(yolo_loss,
                    output_shape=(1,), name='yolo_loss',
                    arguments={'anchors': anchors,
                               'num_classes': num_classes,
                               'ignore_thresh': 0.5}
                    )(model_body.output + y_true)
```

其中，model_body.output是已有模型的预测值，y_true是真实值，两者的格式相同，如下：

```
model_body: [(?, 13, 13, 18), (?, 26, 26, 18), (?, 52, 52, 18)]
y_true: [(?, 13, 13, 18), (?, 26, 26, 18), (?, 52, 52, 18)]
```

接着，在yolo_loss方法中，参数是：

- args是Lambda层的输入，即model_body.output和y_true的组合；
- anchors是二维数组，结构是(9, 2)，即9个anchor box；
- num_classes是类别数；
- ignore_thresh是过滤阈值；
- print_loss是打印损失函数的开关；

即：

```python
def yolo_loss(args, anchors, num_classes, ignore_thresh=.5, print_loss=True):
```

------

## 2. 参数

在损失方法yolo_loss中，设置若干参数：

- num_layers：层的数量，是anchors数量的3分之1；
- yolo_outputs和y_true：分离args，前3个是yolo_outputs预测值，后3个是y_true真值；
- anchor_mask：anchor box的索引数组，3个1组倒序排序，678对应13x13，345对应26x26，123对应52x52；即[[6, 7, 8], [3, 4, 5], [0, 1, 2]]；
- input_shape：K.shape(yolo_outputs[0])[1:3]，第1个预测矩阵yolo_outputs[0]的结构（shape）的第1~2位，即(?, 13, 13, 18)中的(13, 13)。再x32，就是YOLO网络的输入尺寸，即(416, 416)，因为在网络中，含有5个步长为(2, 2)的卷积操作，降维32=5^2倍；
- grid_shapes：与input_shape类似，K.shape()[1:3]，以列表的形式，选择3个尺寸的预测图维度，即[(13, 13), (26, 26), (52, 52)]；
- m：第1个预测图的结构的第1位，即K.shape()[0]，输入模型的图片总量，即批次数；
- mf：m的float类型，即K.cast(m, K.dtype())
- loss：损失值为0；

即：

```python
num_layers = len(anchors) // 3  # default setting
yolo_outputs = args[:num_layers]
y_true = args[num_layers:]
anchor_mask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]] if num_layers == 3 else [[3, 4, 5], [1, 2, 3]]
# input_shape是输出的尺寸*32, 就是原始的输入尺寸，[1:3]是尺寸的位置，即416x416
input_shape = K.cast(K.shape(yolo_outputs[0])[1:3] * 32, K.dtype(y_true[0]))
# 每个网格的尺寸，组成列表
grid_shapes = [K.cast(K.shape(yolo_outputs[l])[1:3], K.dtype(y_true[0])) for l in range(num_layers)]

m = K.shape(yolo_outputs[0])[0]  # batch size, tensor
mf = K.cast(m, K.dtype(yolo_outputs[0]))

loss = 0
```

------

## 3. 预测数据

在yolo_head中，将预测图yolo_outputs[l]，拆分为边界框的起始点xy、宽高wh、置信度confidence和类别概率class_probs。输入参数：

- yolo_outputs[l]或feats：第l个预测图，如(?, 13, 13, 18)；
- anchors[anchor_mask[l]]或anchors：第l个anchor box，如[(116, 90), (156,198), (373,326)]；
- num_classes：类别数，如1个；
- input_shape：输入图片的尺寸，Tensor，值为(416, 416)；
- calc_loss：计算loss的开关，在计算损失值时，calc_loss打开，为True；

即：

```python
grid, raw_pred, pred_xy, pred_wh = \
    yolo_head(yolo_outputs[l], anchors[anchor_mask[l]], num_classes, input_shape, calc_loss=True)

def yolo_head(feats, anchors, num_classes, input_shape, calc_loss=False):
```

接着，统计anchors的数量num_anchors，即3个。将anchors转换为与预测图feats维度相同的Tensor，即anchors_tensor的结构是(1, 1, 1, 3, 2)，即：

```python
num_anchors = len(anchors)
# Reshape to batch, height, width, num_anchors, box_params.
anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])
```

下一步，创建网格grid：

- 获取网格的尺寸grid_shape，即预测图feats的第1~2位，如13x13；
- grid_y和grid_x用于生成网格grid，通过arange、reshape、tile的组合，创建y轴的0~12的组合grid_y，再创建x轴的0~12的组合grid_x，将两者拼接concatenate，就是grid；
- grid是遍历二元数值组合的数值，结构是(13, 13, 1, 2)；

即：

```python
grid_shape = K.shape(feats)[1:3]
grid_shape = K.shape(feats)[1:3]  # height, width
grid_y = K.tile(K.reshape(K.arange(0, stop=grid_shape[0]), [-1, 1, 1, 1]),
                [1, grid_shape[1], 1, 1])
grid_x = K.tile(K.reshape(K.arange(0, stop=grid_shape[1]), [1, -1, 1, 1]),
                [grid_shape[0], 1, 1, 1])
grid = K.concatenate([grid_x, grid_y])
grid = K.cast(grid, K.dtype(feats))
```

下一步，将feats的最后一维展开，将anchors与其他数据（类别数+4个框值+框置信度）分离

```python
feats = K.reshape(
    feats, [-1, grid_shape[0], grid_shape[1], num_anchors, num_classes + 5])
```

下一步，计算起始点xy、宽高wh、框置信度box_confidence和类别置信度box_class_probs：

- 起始点xy：将feats中xy的值，经过sigmoid归一化，再加上相应的grid的二元组，再除以网格边长，归一化；
- 宽高wh：将feats中wh的值，经过exp正值化，再乘以anchors_tensor的anchor box，再除以图片宽高，归一化；
- 框置信度box_confidence：将feats中confidence值，经过sigmoid归一化；
- 类别置信度box_class_probs：将feats中class_probs值，经过sigmoid归一化；

即：

```python
box_xy = (K.sigmoid(feats[..., :2]) + grid) / K.cast(grid_shape[::-1], K.dtype(feats))
box_wh = K.exp(feats[..., 2:4]) * anchors_tensor / K.cast(input_shape[::-1], K.dtype(feats))
box_confidence = K.sigmoid(feats[..., 4:5])
box_class_probs = K.sigmoid(feats[..., 5:])
```

其中，xywh的计算公式，tx、ty、tw和th是feats值，而bx、by、bw和bh是输出值，如下：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180925/E2Kgb34GCI.png?imageslim)

框的4个值

这4个值box_xy, box_wh, confidence, class_probs的范围均在0~1之间。

由于计算损失值，calc_loss为True，则返回：

- 网格grid：结构是(13, 13, 1, 2)，数值为0~12的全遍历二元组；
- 预测值feats：经过reshape变换，将18维数据分离出3维anchors，结构是(?, 13, 13, 3, 6)
- box_xy和box_wh归一化的起始点xy和宽高wh，xy的结构是(?, 13, 13, 3, 2)，wh的结构是(?, 13, 13, 3, 2)；box_xy的范围是(0~1)，box_wh的范围是(0~1)；即bx、by、bw、bh计算完成之后，再进行归一化。

即：

```python
if calc_loss == True:
    return grid, feats, box_xy, box_wh
```


## 4. 损失函数

在计算损失值时，循环计算每1层的损失值，累加到一起，即

```python
for l in range(num_layers):
        // ...
        loss += xy_loss + wh_loss + confidence_loss + class_loss
```

在每个循环体中：

- 获取物体置信度object_mask，最后1个维度的第4位，第0~3位是框，第4位是物体置信度；
- 类别置信度true_class_probs，最后1个维度的第5位；

即：

```python
object_mask = y_true[l][..., 4:5]
true_class_probs = y_true[l][..., 5:]
```

接着，调用yolo_head重构预测图，输出：

- 网格grid：结构是(13, 13, 1, 2)，数值为0~12的全遍历二元组；
- 预测值raw_pred：经过reshape变换，将anchors分离，结构是(?, 13, 13, 3, 6)
- pred_xy和pred_wh归一化的起始点xy和宽高wh，xy的结构是(?, 13, 13, 3, 2)，wh的结构是(?, 13, 13, 3, 2)；

再将xy和wh组合成预测框pred_box，结构是(?, 13, 13, 3, 4)。

```python
grid, raw_pred, pred_xy, pred_wh = \
    yolo_head(yolo_outputs[l], anchors[anchor_mask[l]],
              num_classes, input_shape, calc_loss=True)
pred_box = K.concatenate([pred_xy, pred_wh])
```

接着，生成真值数据：

- raw_true_xy：在网格中的中心点xy，偏移数据，值的范围是0~1；y_true的第0和1位是中心点xy的相对位置，范围是0~1；
- raw_true_wh：在网络中的wh针对于anchors的比例，再转换为log形式，范围是有正有负；y_true的第2和3位是宽高wh的相对位置，范围是0~1；
- box_loss_scale：计算wh权重，取值范围(1~2)；

实现：

```python
# Darknet raw box to calculate loss.
raw_true_xy = y_true[l][..., :2] * grid_shapes[l][::-1] - grid
raw_true_wh = K.log(y_true[l][..., 2:4] / anchors[anchor_mask[l]] * input_shape[::-1])  # 1
raw_true_wh = K.switch(object_mask, raw_true_wh, K.zeros_like(raw_true_wh))  # avoid log(0)=-inf
box_loss_scale = 2 - y_true[l][..., 2:3] * y_true[l][..., 3:4]  # 2-w*h
```

接着，根据IoU忽略阈值生成ignore_mask，将预测框pred_box和真值框true_box计算IoU，抑制不需要的anchor框的值，即IoU小于最大阈值的anchor框。ignore_mask的shape是(?, ?, ?, 3, 1)，第0位是批次数，第1~2位是特征图尺寸。

实现：

```python
ignore_mask = tf.TensorArray(K.dtype(y_true[0]), size=1, dynamic_size=True)
object_mask_bool = K.cast(object_mask, 'bool')

def loop_body(b, ignore_mask):
    true_box = tf.boolean_mask(y_true[l][b, ..., 0:4], object_mask_bool[b, ..., 0])
    iou = box_iou(pred_box[b], true_box)
    best_iou = K.max(iou, axis=-1)
    ignore_mask = ignore_mask.write(b, K.cast(best_iou < ignore_thresh, K.dtype(true_box)))
    return b + 1, ignore_mask

_, ignore_mask = K.control_flow_ops.while_loop(lambda b, *args: b < m, loop_body, [0, ignore_mask])
ignore_mask = ignore_mask.stack()
ignore_mask = K.expand_dims(ignore_mask, -1)
```

损失函数：

- xy_loss：中心点的损失值。object_mask是y_true的第4位，即是否含有物体，含有是1，不含是0。box_loss_scale的值，与物体框的大小有关，2减去相对面积，值得范围是(1~2)。binary_crossentropy是二值交叉熵。
- wh_loss：宽高的损失值。除此之外，额外乘以系数0.5，平方K.square()。
- confidence_loss：框的损失值。两部分组成，第1部分是存在物体的损失值，第2部分是不存在物体的损失值，其中乘以忽略掩码ignore_mask，忽略预测框中IoU大于阈值的框。
- class_loss：类别损失值。
- 将各部分损失值的和，除以均值，累加，作为最终的图片损失值。

细节实现：

```python
object_mask = y_true[l][..., 4:5]  # 物体掩码
box_loss_scale = 2 - y_true[l][..., 2:3] * y_true[l][..., 3:4]  # 框损失比例
z * -log(sigmoid(x)) + (1 - z) * -log(1 - sigmoid(x))  # 二值交叉熵函数
iou = box_iou(pred_box[b], true_box)  # 预测框与真正框的IoU
```

损失函数实现：

```python
xy_loss = object_mask * box_loss_scale * K.binary_crossentropy(raw_true_xy, raw_pred[..., 0:2],
                                                               from_logits=True)
wh_loss = object_mask * box_loss_scale * 0.5 * K.square(raw_true_wh - raw_pred[..., 2:4])
confidence_loss = object_mask * K.binary_crossentropy(object_mask, raw_pred[..., 4:5], from_logits=True) + \
                  (1 - object_mask) * K.binary_crossentropy(object_mask, raw_pred[..., 4:5],
                                                            from_logits=True) * ignore_mask
class_loss = object_mask * K.binary_crossentropy(true_class_probs, raw_pred[..., 5:], from_logits=True)

xy_loss = K.sum(xy_loss) / mf
wh_loss = K.sum(wh_loss) / mf
confidence_loss = K.sum(confidence_loss) / mf
class_loss = K.sum(class_loss) / mf
loss += xy_loss + wh_loss + confidence_loss + class_loss
```

YOLO v1的损失函数公式，与v3略有不同，作为参考：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180925/J8K5ijBI3D.png?imageslim)

Loss

------

## 补充

## 1. “...”操作符

在Python中，“...”(ellipsis)操作符，表示其他维度不变，只操作最前或最后1维；

```python
import numpy as np

x = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
"""[[ 1  2  3  4] [ 5  6  7  8] [ 9 10 11 12]]"""
print(x.shape)  # (3, 4)
y = x[1:2, ...]
"""[[5 6 7 8]]"""
print(y)
```

## 2. 遍历数值组合

在YOLO v3中，当计算网格值时，需要由相对位置，转换为绝对位置，就是相对值，加上网格的左上角的值，如相对值(0.2, 0.3)在第(1, 1)网格中的绝对值是(1.2, 1.3)。当转换坐标值时，根据坐标点的位置，添加相应的初始值即可。这样，就需要遍历两两的数值组合，如生成0至12的网格矩阵。

通过arange -> reshape -> tile -> concatenate的组合，即可快速完成。

源码：

```python
from keras import backend as K

grid_y = K.tile(K.reshape(K.arange(0, stop=3), [-1, 1, 1]), [1, 3, 1])
grid_x = K.tile(K.reshape(K.arange(0, stop=3), [1, -1, 1]), [3, 1, 1])
sess = K.get_session()

print(grid_x.shape)  # (3, 3, 1)
print(grid_y.shape)  # (3, 3, 1)

z = K.concatenate([grid_x, grid_y])

print(z.shape)  # (3, 3, 2)
print(sess.run(z))
"""创建3x3的二维矩阵，遍历全部数组0~2"""
```

## 3. ::-1

“::-1”是颠倒数组的值，例如：

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
print a[::-1]
"""[5 4 3 2 1]"""
```

## 4. Session

在Keras中，使用Session测试验证数据，实现：

```python
from keras import backend as K

sess = K.get_session()
a = K.constant([2, 4])
b = K.constant([3, 2])
c = K.square(a - b)

print(sess.run(c))
```


# 相关资料

- [探索 YOLO v3 实现细节 - 第5篇 Loss](https://mp.weixin.qq.com/s/4L9E4WGSh0hzlD303036bQ)
