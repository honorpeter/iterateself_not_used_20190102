---
title: python中的枚举
toc: true
date: 2018-08-03 15:17:04
---
# 需要补充的

- 说实话，Python 的枚举一直想用，但是之前没有怎么认真了解过，还是要认真掌握的。

# Python 中的枚举


视频里说到python中的enum的时候，感觉与其他的语言有很大的不同，因此，还是要总结下的


```py
# 感觉python里面的enum与其他语言的又很大的不同

from enum import Enum

# 为什么这个地方还有一个Month？
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr'))

# value为什么是从1开始的？
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

jan = Month.Jan
print(jan)
```

输出：

```
Jan => Month.Jan , 1
Feb => Month.Feb , 2
Mar => Month.Mar , 3
Apr => Month.Apr , 4
Month.Jan
```

<span style="color:red;">为什么 Enum 里面还有一个 Month？而且为什么会有name，member 和 member.value？</span>



# 相关资料
