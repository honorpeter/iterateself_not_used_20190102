---
title: Python 文本的读写
toc: true
date: 2018-08-28
---

# Python 文本的读写

Python中读取文件常用的三种方法：read(),readline(),readlines().

### 0.准备

假设`a.txt`的内容如下所示：

```
Hello
Welcome
What is the fuck...
```

### 1. read([size])方法

`read([size])`方法从文件当前位置起读取size个字节，若无参数`size`，则表示读取至文件结束为止，它范围为字符串对象

```
f = open("a.txt")
lines = f.read()
print lines
print(type(lines))
f.close()
```

输出结果：

```
Hello
Welcome
What is the fuck...
<type 'str'> #字符串类型
```

### 2.readline()方法

从字面意思可以看出，该方法每次读出一行内容，所以，读取时占用内存小，比较适合大文件，该方法返回一个字符串对象。

```
f = open("a.txt")
line = f.readline()
print(type(line))
while line:
    print line,
    line = f.readline()
f.close()
```

输出结果：

```
<type 'str'>
Hello
Welcome
What is the fuck...
```

### 3.readlines()方法读取整个文件所有行，保存在一个列表(list)变量中，每行作为一个元素，但读取大文件会比较占内存。

```
f = open("a.txt")
lines = f.readlines()
print(type(lines))
for line in lines:
    print line，
f.close()
```

输出结果：
 <type 'list'>
 Hello
 Welcome
 What is the fuck...

### 4.linecache模块

当然，有特殊需求还可以用linecache模块，比如你要输出某个文件的第n行：

```
# 输出第2行
text = linecache.getline(‘a.txt’,2)
print text,
```

对于大文件效率还可以。



## 相关资料

- [Python中的read(),readline(),readlines()区别与用法](https://www.jianshu.com/p/a672f39287c4) 作者：大阿拉伯人
