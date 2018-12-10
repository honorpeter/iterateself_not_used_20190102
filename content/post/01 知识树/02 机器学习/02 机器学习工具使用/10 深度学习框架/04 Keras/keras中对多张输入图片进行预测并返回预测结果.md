---
title: keras中对多张输入图片进行预测并返回预测结果
toc: true
date: 2018-12-10
---
# 需要补充的

- 这个的确是需要的，因为一张一张进行预测，比较耗费时间，但是我进行批量预测之后，时间减少了一些，但是没有很多，大概有原来一张一张的时间的 3/4 ，是什么原因呢？

# keras中对多张输入图片进行预测并返回预测结果

前面讨论过单张图片的输入和和预测，下面讨论一下多张图片同时输入模型的方法。

对于多张图片的输入，将多张图片读入到一个列表中，然后 concatenate 起来，concatenate的作用是把shape为（0,224,224,3）的每张图片tensor，打包成shape为（batch，224,224,3）的tensor，实现批量的预测或者批量训练了。



代码如下：


```py
import numpy as np
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
from keras.applications import *
import glob

import os

# 忽略硬件加速的警告信息
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

file_path = 'Data/'
f_names = glob.glob(file_path + '*.jpg')

img = []
# 把图片读取出来放到列表中
for i in range(len(f_names)):
    images = image.load_img(f_names[i], target_size=(224, 224))
    x = image.img_to_array(images)
    x = np.expand_dims(x, axis=0)
    img.append(x)
    print('loading no.%s image' % i)

# 把图片数组联合在一起
x = np.concatenate([x for x in img])

model = ResNet50(weights='imagenet')
y = model.predict(x)
print('Predicted:', decode_predictions(y, top=3))
```

注意： decode_predictions 返回的是一个预测的列表值。


整体如下：


```py
def predict_with_batch(model, img_gray_list):
    # 进行图像缩放
    x_list=[]
    for img_gray in img_gray_list:
        img_resized = resize_img(img_gray)
        # 作为 X
        img_data = np.array(img_resized).astype(np.float32) / 255.0 - 0.5
        w, h = img_resized.size[0], img_resized.size[1]
        img_data_reshaped = img_data.reshape((h, w, 1))
        X = np.expand_dims(img_data_reshaped, axis=0)
        x_list.append(X)

    X = np.concatenate([x for x in x_list])

    # 进行预测
    timer_predict.tic()
    y_pred = model.predict(X)
    timer_predict.toc()
    print("times: ", timer_predict.diff)
    argmax = np.argmax(y_pred, axis=2)[0]

    y_pred = y_pred[:, :, :]
    out = K.get_value(K.ctc_decode(y_pred,
                                   input_length=np.ones(y_pred.shape[0]) * y_pred.shape[1], )[0][0])[:, :]
    word_list=[]
    for data in out:
        word = u''.join([g_generator.get_char_according_with_id(x) for x in data])
        word_list.append(word)

    return word_list
```



# 相关资料

- [keras中对多张输入图片进行预测并返回预测结果](https://blog.csdn.net/u012193416/article/details/79376345)
