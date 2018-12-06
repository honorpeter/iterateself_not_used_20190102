---
title: Python 中文编码
toc: true
date: 2018-07-27 17:16:47
---
## 需要补充的


# Python 中文编码

# Python2 中的中文编码

## 在 py 文件开头指定编码


Python2 中如果py文件中未指定编码，在涉及中文字符的时候，执行会报错：

```
#!/usr/bin/python
print "你好，世界";
```


输出：

```
  File "test.py", line 2
SyntaxError: Non-ASCII character '\xe4' in file test.py on line 2, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
```


以上出错信息显示了我们未指定编码。

解决方法为：在文件开头加入下面任意一个即可：

- `# -*- coding: UTF-8 -*-`
- `# coding=utf-8`


例子如下：

```py
#!/usr/bin/python
# coding=utf-8

print "你好，世界";
```

输出：

```
你好，世界
```




## 使用 Pycharm 的时候的中文对应

如果你使用编辑器，同时需要设置好编辑器的编码，如 Pycharm 设置步骤：

* 进入 **file > Settings**，在输入框搜索 **encoding**。
* 找到 **Editor > File encodings**，将 **IDE Encoding** 和 **Project Encoding** 设置为 utf-8。


![mark](http://images.iterate.site/blog/image/180727/aaJ4e3e2Be.png?imageslim)



# Python3 中的中文编码


Python3.X 的源码文件默认使用 utf-8 编码，所以可以正常解析中文，无需指定 UTF-8 编码。





# 相关资料

1. [python基础教程 w3cschool](https://www.w3cschool.cn/python/)
2. [Python 3 教程 菜鸟教程](http://www.runoob.com/python3/python3-tutorial.html)
