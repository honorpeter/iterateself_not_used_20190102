---
title: 获得python的list中含有重复值的index
toc: true
date: 2018-10-31
---

# 获得python的list中含有重复值的index

关于怎么获得，我想其实网上有很多答案。
list.index( )获得值的索引值，但是如果list中含有的值一样，例如含有两个11,22，这样每次获得的都是第一个值的位置。
那么怎么去解决这个问题呢？
下面的程序对这个问题做了一定的解答

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : SundayCoder-俊勇
# @File    : listlearn.py
# 怎么获得list中的相同值的索引值
# 请看下列程序
s = [11, 22, 33, 44, 22, 11]
print s.index(11)
# 此时输出0
print s.index(22)
# 此时输出1
# 那怎么才能得到11,22相同的值的索引值呢？
# 有人说用dict（字典），这个方法也可以
# 有人说用defaultdict
# 程序如下：
from collections import defaultdict
d = defaultdict(list)
for k,va in [(v,i) for i,v in enumerate(s)]:
​    d[k].append(va)
print d
# 输出的结果如下：defaultdict(<type 'list'>, {33: [2], 11: [0, 5], 44: [3], 22: [1, 4]})
# 但是有没有一个更加简单的方法呢？
# 有的，那就是”偷梁换柱“，用一个s1来复制s。
s1 = s
i = s1.index(11)
s1[i]=55
# 替换s1的11为55（不一定是55只要是列表中没有的数值就可以）
# 再打印s1
print s1
# 输出[55, 22, 33, 44, 22, 11]
# 下一步可以得到11的位置了
print  s1.index(11)
# 输出为：5

```



# 相关资料

- [获得python的list中含有重复值的index](https://blog.csdn.net/qq_33094993/article/details/53584379)
