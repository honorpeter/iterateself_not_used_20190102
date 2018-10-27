# 在 IPython 中检测程序效率

##### 有时你需要比较两个相似操作的效率，这时你可以使用 IPython 为你提供

##### 的魔法命令％time。他会让代码运行好几次从而得到一个准确的(运行)时 间。它也可以被用来测试单行代码的。

例如，你知道下面这同一个数学运算用哪种行式的代码会执行的更快吗？ x = 5; y 二 x * *2 x 二5; y 二 x * x x 二 np.uint([5]); y 二 x * x y 二 np.squre(x)

##### 我们可以在IPython的Shell中使用魔法命令找到答案。

Created on Thu Jan 9 21:10:40 2014

@author: duan

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

##### 竟然是第一种写法，它居然比Nump快了 20倍。如果考虑到数组构建的 话，能达到 100 倍的差。

##### 注意： Python 的标量计算比 Nump 的标量计算要快。对于仅包含一两个 元素的操作Python标量比Numpy的数组要快。但是当数组稍微大一点时 Numpy 就会胜出了。

##### 我们来再看几个例子。 我们来比 较一 下 cv2.countNonZero() 和

np.count_nonzero()。

| # -*- coding: utf-8 -*-      |                         |
| ---------------------------- | ----------------------- |
| Created on Thu Jan           | 9 21:10:40 2014         |
| @author: duan                |                         |
| import cv2import numpy as np |                         |
| In [35]: %timeit z           | = cv2.countNonZero(img) |
| 100000 loops, best           | of 3: 15.8 us per loop  |
| In [36]: %timeit z           | = np.count_nonzero(img) |
| 1000 loops, best of          | 3: 370 us per loop      |

看见了吧，OpenCV的函数是Numpy函数的25倍。

注意：一般情况下OpenCV的函数要比Numpy函数快。所以对于相同的操 作最好使用OpenCV的函数。当然也有例外，尤其是当使用Numpy对视图 （而非复制）进行操作时。
