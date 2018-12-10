---
title: 73 在 IPython 中检测程序效率
toc: true
date: 2018-10-27
---
# 需要补充的

- 这个要拆分到 IPython 的里面去，但是，关于 opencv 和 numpy 的类似函数的效率对比还是要总结下的。

# 在 IPython 中检测程序效率

有时你需要比较两个相似操作的效率，这时你可以使用 IPython 为你提供的魔法命令 `％time`。他会让代码运行好几次从而得到一个准确的(运行)时间。它也可以被用来测试单行代码的。<span style="color:red;">一定要在 IPython 里面才能用吗？普通的时候怎么用？还是只能用 time.time() 这样得到两个值，然后再循环里进行统计？</span>

例如，你知道下面这同一个数学运算用哪种行式的代码会执行的更快吗？

```py
x = 5; y = x ∗ ∗2
x = 5; y = x ∗ x
x = np.uint([5]); y = x ∗ x
y = np.squre(x)
```

我们可以在IPython的Shell中使用魔法命令找到答案。

书上的结果是这样的：

```py
import cv2
import numpy as np
In [10]: x = 5
In [11]: %timeit y=x**2
10000000 loops, best of 3: 73 ns per loop
In [12]: %timeit y=x*x
10000000 loops, best of 3: 58.3 ns per loop
In [15]: z = np.uint8([5])
In [17]: %timeit y=z*z
1000000 loops, best of 3: 1.25 us per loop
In [19]: %timeit y=np.square(z)
1000000 loops, best of 3: 1.16 us per loop
```

竟然是第一种写法，它居然比Nump快了 20倍。如果考虑到数组构建的话，能达到 100 倍的差。

> 注意： Python 的标量计算比 Numpy 的标量计算要快。对于仅包含一两个元素的操作 Python 标量比 Numpy 的数组要快。但是当数组稍微大一点时 Numpy 就会胜出了。<span style="color:red;">真的是这样的吗？</span>

<span style="color:red;">为什么我在我的电脑上运行，结果是这样的：</span>

```py
import cv2
import numpy as np
In [10]: x = 5
In [11]: %timeit y=x**2
296 ns ± 0.94 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
In [12]: %timeit y=x*x
62.7 ns ± 0.299 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
In [15]: z = np.uint8([5])
In [17]: %timeit y=z*z
518 ns ± 11.4 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
In [19]: %timeit y=np.square(z)
509 ns ± 3.25 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

<span style="color:red;">感觉差不多呀。其实我想知道为什么 `x*x` 比 `x**2` 快了这么多？</span>




我们来再看几个例子。 我们来比 较一 下 cv2.countNonZero() 和 np.count_nonzero()。

我的电脑跑出来是：

```
import cv2
import numpy as np
In [35]: %timeit z = cv2.countNonZero(img)
15.5 µs ± 182 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
In [36]: %timeit z = np.count_nonzero(img)
729 µs ± 2.66 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```

看见了吧，OpenCV 的函数是 Numpy 函数的 50 倍。<span style="color:red;">在我的电脑上跑的的确是 50 倍，但是为什么会差别这么大？</span>

> 注意：一般情况下 OpenCV 的函数要比 Numpy 函数快。所以对于相同的操作最好使用OpenCV的函数。当然也有例外，尤其是当使用 Numpy 对视图 （而非复制）进行操作时。<span style="color:red;">什么叫对视图进行操作？到底什么时候用 opencv 的函数？而且，怎么知道 opencv 的函数与 numpy 的函数效果是不是相同的？嗯，这个地方再补充一下。</span>






# 相关资料

- 《OpenCV-Python 中文教程》
