# OpenCV 中的默认优化

OpenCV 中的很多函数都被优化过(使用 SSE2， AVX 等)。<span style="color:red;">这些是什么？SSE2 和 AVX？ 之前在跑 tensorflow 的时候，开头总是有这题提示时候你的 CPU 不支持这个。确认下这个是什么</span>

如果我们的系统支持优化的话要尽量利用只一点。

实际上，OpenCV 的优化在编译时是被默认开启的，因此，实际上 OpenCV 运行的就是优化后的代码，如果你把优化关闭的话就只能执行低效的代码了。<span style="color:red;">下面的例子测了，好像没有什么优化效果。。</span>

你可以使用函数 `cv2.useOptimized()` 来查看优化是否被开启了，使用函数 `cv2.setUseOptimized()` 来开启优化 让我们来看一个简单的例子吧。


```python
# -*- coding: utf-8 -*-

import cv2


def get_run_time():
    img1 = cv2.imread('2.jpg')
    e1 = cv2.getTickCount()
    for i in range(5, 49, 2):
        img1 = cv2.medianBlur(img1, i)
    e2 = cv2.getTickCount()
    t = (e2 - e1) / cv2.getTickFrequency()
    return t

# 默认是开启优化的
print(cv2.useOptimized())
print(get_run_time())

# 关闭优化
cv2.setUseOptimized(False)
print(cv2.useOptimized())
print(get_run_time())
```

输出：

```
True
1.0253463
False
1.0433325
```

书上说，这个地方优化后中值滤波的速度是原来的两倍。然后说，如果你查看源代码的话，会发现中值滤波是被 SIMD 优化的。

<span style="color:red;">但是真的没发现优化比没有优化好。。而且，我在另外一台高配电脑上用相同的程序，相同的图片，试了下，优化后是 0.268887296 没有优化后是 0.260366168 。没有优化反而比 优化后快，按理说，这个高配的电脑肯迪肯定是什么都支持的吧？。。还是说这个高配的电脑不一定支持？</span>
