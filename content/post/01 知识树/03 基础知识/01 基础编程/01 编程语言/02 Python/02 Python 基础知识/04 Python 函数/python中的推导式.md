---
title: python中的推导式
toc: true
date: 2018-06-11 08:14:29
---
# 需要补充的


# Python中的推导式

推导式感觉很酷，要掌握下：


## 简单的例子：



```py
# set与dict在python2里面是不支持的
li = [i * 2 for i in range(10)]
print(li)
s = {x for x in range(10) if x % 2 == 0}
print(s)
d = {x: x % 2 == 0 for x in range(10)}
print(d)
```

输出：

```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
{0, 2, 4, 6, 8}
{0: True, 1: False, 2: True, 3: False, 4: True, 5: False, 6: True, 7: False, 8: True, 9: False}
```


# 相关资料

**要更加系统的深入的了解**
