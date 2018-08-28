---
title: python linecache
toc: true
date: 2018-08-28
---

# Python linecache 模块

本节主要内容：
**python linecache模块读取文件**

在python中，有个好用的模块linecache，该模块允许从任何文件里得到任何的行，并且使用缓存进行优化，常见的情况是从单个文件读取多行。

**linecache.getlines(filename)**从名为filename的文件中得到全部内容，输出为列表格式，以文件每行为列表中的一个元素,并以linenum-1为元素在列表中的位置存储

**linecache.getline(filename,lineno)**从名为filename的文件中得到第lineno行。这个函数从不会抛出一个异常–产生错误时它将返回”（换行符将包含在找到的行里）。
如果文件没有找到，这个函数将会在sys.path搜索。

**linecache.clearcache()**清除缓存。如果你不再需要先前从getline()中得到的行

**linecache.checkcache(filename)**检查缓存的有效性。如果在缓存中的文件在硬盘上发生了变化，并且你需要更新版本，使用这个函数。如果省略filename，将检查缓存里的所有条目。

**linecache.updatecache(filename)**更新文件名为filename的缓存。如果filename文件更新了，使用这个函数可以更新linecache.getlines(filename)返回的列表。



代码示例:

\# cat a.txt
1a
2b
3c
4d
5e
6f
7g



1、获取a.txt文件的内容



代码示例:



\>>> a=linecache.getlines('a.txt')

\>>> a

['1a\n', '2b\n', '3c\n', '4d\n', '5e\n', '6f\n', '7g\n']

2、获取a.txt文件中第1-4行的内容

代码示例:

\>>> a=linecache.getlines('a.txt')[0:4]

\>>> a

['1a\n', '2b\n', '3c\n', '4d\n']

3、获取a.txt文件中第4行的内容

代码示例:

\>>> a=linecache.getline('a.txt',4)
\>>> a
'4d\n'

注意：使用linecache.getlines('a.txt')打开文件的内容之后，如果a.txt文件发生了改变，如果要再次用linecache.getlines获取的内容，不是文件的最新内容，还是之前的内容，此时有两种方法：
1、使用linecache.checkcache(filename)来更新文件在硬盘上的缓存，然后在执行linecache.getlines('a.txt')就可以获取到a.txt的最新内容；
2、直接使用linecache.updatecache('a.txt')，即可获取最新的a.txt的罪行内容

另外：
1）、读取文件之后，不需要使用文件的缓存时，需要在最后清理一下缓存，使linecache.clearcache()清理缓存，释放缓存。
2）、此模块使用内存来缓存文件内容，所以需要耗费内存，打开文件的大小和打开速度和你的内存大小有关系。



## 相关资料

- [详解python linecache模块读取文件的方法](https://blog.csdn.net/my2010Sam/article/details/38022041)
