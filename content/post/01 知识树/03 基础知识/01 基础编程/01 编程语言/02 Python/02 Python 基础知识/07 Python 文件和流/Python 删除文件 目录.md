---
title: Python 删除文件 目录
toc: true
date: 2018-10-17
---
本文讲述了python实现删除文件与目录的方法。分享给大家供大家参考。具体实现方法如下：
os.remove(path)
删除文件 path. 如果path是一个目录， 抛出 OSError错误。如果要删除目录，请使用rmdir().

remove() 同 unlink() 的功能是一样的
在Windows系统中，删除一个正在使用的文件，将抛出异常。在Unix中，目录表中的记录被删除，但文件的存储还在。

#使用os.unlink()和os.remove()来删除文件
#!/user/local/bin/python2.7
# -*- coding:utf-8 -*-
import os
my_file = 'D:/text.txt'
if os.path.exists(my_file):
​    #删除文件，可使用以下两种方法。
​    os.remove(my_file)
​    #os.unlink(my_file)
else:
​    print 'no such file:%s'%my_file
1
2
3
4
5
6
7
8
9
10
11
os.removedirs(path)
递归地删除目录。类似于rmdir(), 如果子目录被成功删除， removedirs() 将会删除父目录；但子目录没有成功删除，将抛出错误。
举个例子， os.removedirs(“foo/bar/baz”) 将首先删除 “foo/bar/ba”目录，然后再删除foo/bar 和 foo, 如果他们是空的话
如果子目录不能成功删除，将 抛出 OSError异常

os.rmdir(path)
删除目录 path，要求path必须是个空目录，否则抛出OSError错误

递归删除目录和文件（类似DOS命令DeleteTree）：
复制代码 代码如下:

import os
for root, dirs, files in os.walk(top, topdown=False):
​    for name in files:
​        os.remove(os.path.join(root, name))
​    for name in dirs:
​        os.rmdir(os.path.join(root, name))
1
2
3
4
5
6
方法2：
代码如下:

import shutil
shutil.rmtree()
---------------------




- [python 删除文件、目录](https://blog.csdn.net/MuWinter/article/details/77196261)
