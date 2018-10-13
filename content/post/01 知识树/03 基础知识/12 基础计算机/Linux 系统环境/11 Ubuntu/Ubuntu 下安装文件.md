---
title: Ubuntu 下安装文件
toc: true
date: 2018-10-04
---

# 需要补充的

- 要按照书来，系统的进行掌握，这样是不行的。
- 而且，之前遇到过没有这些文件的，要怎么安装。

# Ubuntu 下安装文件

一般情况下，多看看目录下的 readme 和 INSTALL 文件，里面会告诉你怎么安装软件。

这里我目前知道可能有两种情况：

1、目录下没有 `configure`，但有 `configure.am` 或 `configure.in` 时，需要用 `autoconf` 命令来生成 `configure`。代码如下：

```
$cd (软件名)-(版本号)
$autoconf
```

2、此软件或库安装方式不是按以下套路来安装,

```
$cd (软件名)-(版本号)
$./configure
$make
$sudo make install
```

就需要认真阅读文件夹下的相关文件 readme 等等，按里面写的方式来安装！




# 相关资料

- [如何在Ubuntu下安装”.deb“、”.bin“、”.tar.gz“、”.tar.bz2“格式的软件包！](https://blog.csdn.net/zyz511919766/article/details/7574040)
- [./configure: No such file or directory](https://www.cnblogs.com/niocai/archive/2011/07/14/2106088.html)
