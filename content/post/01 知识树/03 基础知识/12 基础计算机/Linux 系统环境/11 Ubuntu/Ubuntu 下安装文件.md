---
title: Ubuntu 下安装文件
toc: true
date: 2018-10-04
---

# 需要补充的

- 要按照书来，系统的进行掌握，这样是不行的。

# Ubuntu 下安装文件

一般情况下，多看看目录下的readme和INSTALL文件，里面会告诉你怎么安装软件。

这里我目前知道可能有两种情况：

1、目录下没有configure，但有configure.am或configure.in时，需要用autoconf命令来生成configure。代码如下：

$cd (软件名)-(版本号)
$autoconf
2、此软件或库安装方式不是按以下套路来安装,

$cd (软件名)-(版本号)
$./configure
$make
$sudo make install
就需要认真阅读文件夹下的相关文件readme等等，按里面写的方式来安装！




# 相关资料

- [如何在Ubuntu下安装”.deb“、”.bin“、”.tar.gz“、”.tar.bz2“格式的软件包！](https://blog.csdn.net/zyz511919766/article/details/7574040)
- [./configure: No such file or directory](https://www.cnblogs.com/niocai/archive/2011/07/14/2106088.html)
