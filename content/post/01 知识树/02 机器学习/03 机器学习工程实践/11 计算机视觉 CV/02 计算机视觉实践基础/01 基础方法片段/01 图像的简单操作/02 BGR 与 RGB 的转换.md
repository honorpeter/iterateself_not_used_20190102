---
title: 02 BGR 与 RGB 的转换
toc: true
date: 2018-10-14
---
# BGR 与 RGB 的转换


这个问题还是有可能遇到的，比如说你用 OpenCV 加载了一张图像，但是后面你要用 matplotlib 来进行处理或显示，那么这就有一个问题了，OpenCV 使用的是 BGR 模式，而 Matplotlib 使用的是 RGB 模式。

因此，当你用 Matplotib 显示一个通过 OpenCV 加载进来的图像的时候，你需要把它转到 RGB 形式下。

那么怎么转化呢？

有下面几种方法：


## 先 split ，再 merge

```py
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('messi4.jpg')
b,g,r = cv2.split(img)
img2 = cv2.merge([r,g,b])
plt.subplot(121);plt.imshow(img) # expects distorted color
plt.subplot(122);plt.imshow(img2) # expect true color
plt.show()

cv2.imshow('bgr image',img) # expects true color
cv2.imshow('rgb image',img2) # expects distorted color
cv2.waitKey(0)
cv2.destroyAllWindows()
```

上面的程序输出如下：

Matplotlib 输出如下：

![mark](http://images.iterate.site/blog/image/181014/ELeIIhFE7c.png?imageslim)

OpenCV 输出如下：

![mark](http://images.iterate.site/blog/image/181014/Blfcg8e1ch.png?imageslim)

<span style="color:red;">一直不知道 cv2 还有 split 和 merge 的功能。有些厉害，这个功能做出来是为了什么情况下使用的呢？就是为了这种情况的吗？</span>

## 直接：`img[:,:,::-1]`

```python
img2 = img[:,:,::-1]
```
<span style="color:red;">上面这个有点不是很明白</span>

## 直接：`img[..., ::-1]`


```python
img2 = img[..., ::-1]
```

<span style="color:red;">一直想知道这个 ... 是什么作用，一般什么时候使用？</span>

## 直接：`cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`


```python
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```



# 相关资料

- [Extracting a region from an image using slicing in Python, OpenCV](https://stackoverflow.com/questions/15072736/extracting-a-region-from-an-image-using-slicing-in-python-opencv)
