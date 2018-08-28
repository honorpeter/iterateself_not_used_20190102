---
title: const
toc: true
date: 2018-08-28
---






#### [Q 12*](http://blog.csdn.net/heyabo/article/details/8745942) :

题目：

在C++中，

```
const int i = 0;
int *j = (int *) &i;
*j = 1;
printf("%d, %d", i, *j);
```

输出是多少？

答案:

0
1

解答:

考察C++常量折叠。

1. const 变量放在编译器的符号表中，计算时编译器直接从表中取值，省去了访问内存的时间，从而达到了优化。<span style="color:red;">编译器的符号表是什么？</span>
2. 结论，const 变量通过取地址方式可以修改该地址存储的数据值，但不能修改常量的值。<span style="color:red;">const 变量可以通过取地址的方式来修改它的地址存储的数据值吗？这个之前不知道？确认下，为什么修改了这个地发的值，但不能修改常量的值？还是说这个值在运行 const int i=0 的时候已经加入到符号表中了？后面改了也不是修改这个表中的值？</span>
