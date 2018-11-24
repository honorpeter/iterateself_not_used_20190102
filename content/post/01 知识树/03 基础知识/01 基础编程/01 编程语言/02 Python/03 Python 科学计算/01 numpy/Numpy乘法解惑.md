---
title: Numpy乘法解惑
toc: true
date: 2018-11-23
---
# 需要补充的


# Numpy乘法解惑


numpy 中数据格式有**array**和**mat**，乘法有普通乘号**x**和**dot**，对于初学者（本人也是初学者）来说太容易迷糊了。下面记录一点心得。

#### 先说结论：**dot** 是遵循矩阵乘法的法则；普通乘号 **x** 遵循的法则既有矩阵乘法法则，也有逐元素相乘的法则，具体看相乘的两个数组的数据类型。

------

#### 普通乘号X

1.array相乘
 当两个**array**格式的数组相乘时，结果实际上是逐元素相乘。

```
In [60]: a = np.array([1, 2, 3, 4])

In [61]: b = np.array([2, 2, 3, 3])

In [62]: a * b
Out[62]: array([ 2,  4,  9, 12])

-----------------------------
In [63]: b = np.array([2])

In [64]: a * b
Out[64]: array([2, 4, 6, 8])
-----------------------------------
In [70]: b = np.array([2, 3])

In [71]: b
Out[71]: array([2, 3])

In [72]: a
Out[72]:
array([[1, 2],
       [3, 4]])

In [73]: a * b # 此时相当于将b扩展成array([[2, 3],[2, 3]])
Out[73]:
array([[ 2,  6],
       [ 6, 12]])
--------------------------------
In [74]: b.shape = (2, 1)

In [75]: b
Out[75]:
array([[2],
       [3]])

In [76]: b * a # 此时相当于将b扩展成array([[2, 2], [3, 3]])
Out[76]:
array([[ 2,  4],
       [ 9, 12]])

In [77]: a * b
Out[77]:
array([[ 2,  4],
       [ 9, 12]])
```

2.mat相乘
 当两个**mat**格式的数组相乘时，结果遵循矩阵相乘法则。

3.array与mat相乘
 当**array**与**mat**格式的数组相乘时，结果遵循矩阵相乘法则。

```
In [83]: a
Out[83]:
array([[1, 2],
       [3, 4]])

In [84]: b = np.mat('[2 2];[3 3]')

In [85]: b
Out[85]:
matrix([[2, 2],
        [3, 3]])

In [86]: a * b # 注意a * b的结果与b * a的结果不一致
Out[86]:
matrix([[ 8,  8],
        [18, 18]])

In [87]: b * a
Out[87]:
matrix([[ 8, 12],
        [12, 18]])

---------------------------------
In [90]: a
Out[90]:
matrix([[1, 2],
        [3, 4]])

In [91]: b = np.array([2, 3])

In [92]: b
Out[92]: array([2, 3])

In [93]: a * b # 注意此时出错了，因为不符合矩阵相乘法则
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-93-50927f39610b> in <module>()
----> 1 a * b

/usr/local/lib/python3.6/site-packages/numpy/matrixlib/defmatrix.py in __mul__(self, other)
    341         if isinstance(other, (N.ndarray, list, tuple)) :
    342             # This promotes 1-D vectors to row vectors
--> 343             return N.dot(self, asmatrix(other))
    344         if isscalar(other) or not hasattr(other, '__rmul__') :
    345             return N.dot(self, other)

ValueError: shapes (2,2) and (1,2) not aligned: 2 (dim 1) != 1 (dim 0)

In [94]: b * a
Out[94]: matrix([[11, 16]])
```

------

#### dot

**dot** 实际上采用的就是矩阵的乘法规则，不管是什么数据格式。如下示例：
 1.array相乘

```
In [2]: a = np.array([[1, 2], [3, 4]])

In [3]: a
Out[3]:
array([[1, 2],
       [3, 4]])

In [4]: b = np.array([[2, 3], [2, 3]])

In [5]: b
Out[5]:
array([[2, 3],
       [2, 3]])

In [6]: a.dot(b) # 此时就是矩阵a x 矩阵b的结果
Out[6]:
array([[ 6,  9],
       [14, 21]])
```

下面再举一个反常的例子:

```
In [7]: b = np.array([2, 3])

In [8]: a.dot(b)
Out[8]: array([ 8, 18])
```

如何理解这个例子呢？若按照矩阵的乘法法则，则a x b 应该会报错啊。实际上，此时的`a.dot(b)`可以理解为**a x b.T**的结果，再转置回来，如下所示：

```
In [9]: c = b.reshape((2, 1))

In [10]: c
Out[10]:
array([[2],
       [3]])

In [11]: a.dot(c)
Out[11]:
array([[ 8],
       [18]])

In [12]: np.mat(a) * c
Out[12]:
matrix([[ 8],
        [18]])
```

2.其余mat相乘及mat与array相乘，都是遵循矩阵的乘法法则。




# 相关资料

- [Numpy乘法解惑](https://www.jianshu.com/p/fd2999f41d84)
