---
title: Python 对应元素求和
toc: true
date: 2018-10-27
---


# Python 中对多个 list 的对应元素求和

这个是之前的遇到的一个问题，是想把两个list 里面的坐标值进行相加。<span style="color:red;">嗯，说明还没有习惯使用 numpy ，不然也不会出现这个问题。</span>


Python 中对多个 list 的对应元素求和，前提是每个 list 的长度一样。


比如：a=[1,2,3], b=[2,3,4], c=[3,4,5], 对 a,b,c 的对应元素求和，输出应为 [6,9,12].
　　
## 方法一 直接求解


直接求解，按照对应元素相加的原则，可先定义一个函数。


```
def list_add(a,b):
​    c = []
​    for i in range(len(a)):
​        c.append(a[i]+b[i])
​    return c

if __name__ == '__main__':
​    a = [1,2,3]
​    b = [2,3,4]
​    c = [3,4,5]
​    print(list_add(list_add(a,b),c))
```


## 方法二 利用numpy模块求解。

```
import numpy as np
a = np.array([1,2,3])
b = np.array([2,3,4])
c = np.array([3,4,5])
print(a+b+c)
```


需要注意的是，a+b+c后的类型为numpy.ndarray.



## 方法三 利用numpy模块的sum()函数进行求解


```
import numpy as np
a = [1,2,3]
b = [2,3,4]
c = [3,4,5]
print(np.sum([a,b,c], axis = 0))
```

其中的 `axis` 参数表示纵向求和。



# 相关资料

- [Python之list对应元素求和](https://blog.csdn.net/jclian91/article/details/78118805)
