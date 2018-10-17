---
title: 53 图像 ROI
toc: true
date: 2018-10-17
---
# 需要补充的

- 感觉对于 ROI 还是有很多可以补充的
- 应该是有一些对于 ROI 的使用的例子吧？找一下。总结一下。


# 图像 ROI


有时你需要对一幅图像的特定区域进行操作。例如我们要检测一副图像中眼睛的位置，我们首先应该在图像中找到脸，再在脸的区域中找眼睛，而不是直接在一幅图像中搜索。这样会提高程序的准确性和性能。 <span style="color:red;">是的，的确是这样的。先检测到脸，然后在脸中检测到眼睛。</span>

ROI 也是使用 Numpy 索引来获得的。现在我们选择球的部分并把他拷贝到图像的其他区域。

```python
import cv2
import numpy as np

img = cv2.imread('./1.jpg')
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball
```

看看结果吧：


![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181017/9JCkgcjH69.png?imageslim)




# 相关资料

- 《OpenCV-Python 中文教程》
