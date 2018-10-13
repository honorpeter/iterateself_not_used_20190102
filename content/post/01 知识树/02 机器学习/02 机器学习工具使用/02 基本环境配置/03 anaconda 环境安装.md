---
title: 03 Anaconda 环境安装
toc: true
date: 2018-10-13
---
# 需要补充的

- 把需要用到的东西都总结到这里


# Anaconda 环境安装



## Anaconda 换源

这个还是必须要知道的。因为使用默认的国外的源速度有的时候非常的慢，因此还是会经常要配置国内的源的：

不错的源有两个：中科大的和清华的：

添加中科大的源：

```
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

添加清华的源：（清华的源有的时候不是很稳定，有的快，有的慢）

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

当用户第一次运行 `conda config` 命令时，将会在用户的家目录创建一个 `.condarc` 配置文件，一般会在 windows：`C:\users\username\`，linux：`/home/username/` 下生成。

在这个配置文件中可以修改删除或者添加想要的源：

比如我现在的 `.condarc` 文件内容是这样的：

```
channels:
  - https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
show_channel_urls: true
```

defaults 是官方默认的源，当 conda 在寻找安装包的时候，应该是从上到下查找源的。<span style="color:red;">这个不确定</span>




# 相关资料

- [anaconda镜像不要再用清华的了！](https://blog.csdn.net/qq_35608277/article/details/78714401?utm_source=copy)
- [中科大 Anaconda 源使用帮助](https://mirrors.ustc.edu.cn/help/anaconda.html)
- [清华 Anaconda 镜像使用帮助](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)
