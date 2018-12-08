---
title: python 获得列表(list)中每个元素(重复项)出现次数的最快解决方法
toc: true
date: 2018-10-31
---
# python 获得列表(list)中每个元素(重复项)出现次数的最快解决方法

这个如果是把近似的一些元素找出来要怎么办？用聚类吗？



何使用python快读统计列表中重复项出现的次数？

这个问题在实际应用场景中使用频率比较广泛。本文讲解一下常用的方法：

第一种使用标准库提供的collections：

```
from collections import Counter
import numpy
num=1000000
lst = np.random.randint(num / 10, size=num)
# 返回的值是字典格式如{'xx':8,'xxx':9}
res = Counter(lst)    
# 输出的是出现次数最后的数据如[('xxx', 8), ('xxx', 5),]
Counter(words).most_common(4)    
```

第二种使用numpy模块(更快)

```
import numpy

num=1000000
lst = np.random.randint(num / 10, size=num)
dict(zip(*np.unique(lst, return_counts=True)))
```

第三种使用list.count()方法（最慢）

```
import numpy

num=1000000
lst = np.random.randint(num / 10, size=num)
dic = {}
for i in lst:
    dic[i] = lst.count(i)
```

原文网址：
[http://www.chenxm.cc/post/333...](http://www.chenxm.cc/post/333.html?segmentfault)





# 相关资料

- [python 获得列表(list)中每个元素(重复项)出现次数的最快解决方法](https://segmentfault.com/a/1190000011544079)
