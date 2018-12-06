---
title: Ubuntu 更换源
toc: true
date: 2018-10-04
---
# 需要补充的

- 后续看看还有什么不错的源需要补充进来的。

# Ubuntu 更换源

这个源的确是要更换的，不然，如果没有翻墙，很多时候源的资源是拉不下来的。而且，换源之后，更新的速度也更快。

ubuntu，我们在使用apt新装软件的时候，会使用官方的网站去下载软件，但是会因为国内的转接点太多，而导致下载的速度非常慢 ，我们可以通过换成一些中间的节点来进行下载，比如阿里源，中科大源，清华源等等，这样的网站，他们会定时和官方的源进行同步和更新，而我们直接同步他们，速度就会比直接同步官方的源快很多，这样能够大大增加我们的下载软件的速度。


## 一些可供选择的源

### ubuntu16.04 LTS

#### 阿里源：

```
deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse
```

#### 东北大学：

```
deb-src http://mirror.neu.edu.cn/ubuntu/ xenial main restricted #Added by software-properties
deb http://mirror.neu.edu.cn/ubuntu/ xenial main restricted
deb-src http://mirror.neu.edu.cn/ubuntu/ xenial restricted multiverse universe #Added by software-properties
deb http://mirror.neu.edu.cn/ubuntu/ xenial-updates main restricted
deb-src http://mirror.neu.edu.cn/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirror.neu.edu.cn/ubuntu/ xenial universe
deb http://mirror.neu.edu.cn/ubuntu/ xenial-updates universe
deb http://mirror.neu.edu.cn/ubuntu/ xenial multiverse
deb http://mirror.neu.edu.cn/ubuntu/ xenial-updates multiverse
deb http://mirror.neu.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirror.neu.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirror.neu.edu.cn/ubuntu/ xenial-security main restricted
deb-src http://mirror.neu.edu.cn/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirror.neu.edu.cn/ubuntu/ xenial-security universe
deb http://mirror.neu.edu.cn/ubuntu/ xenial-security multiverse
```

#### 清华大学：


```
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security multiverse
```

### ubuntu 14.04 LTS

#### Ubuntu 官方更新服务器（欧洲，此为官方源，国内较慢，但无同步延迟问题，电信、移动/铁通、联通等公网用户可以使用)：

```
deb http://archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse
```

Ubuntu官方提供的其他软件（第三方闭源软件等）：

```
deb http://archive.canonical.com/ubuntu/ trusty partner
deb http://extras.ubuntu.com/ubuntu/ trusty main
```

#### 阿里云：

```
deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
```



## 更换源的方法

### 修改 `/etc/apt/sources.list` 文件

```
cd /etc/apt
sudo cp sources.list sources.list.bak
sudo vi sources.list (要有管理员权限)
```

### 删除掉sources.list的其他内容，任意选择一种源的内容复制粘贴进去，保存，例如，选择阿里源

![mark](http://images.iterate.site/blog/image/181004/ABlG9C6Ela.png?imageslim)

### 更新 apt

```
sudo apt-get update
```

## 要注意的问题

源更换了之后，一般是没有什么问题的，但是，有的时候，比如我之前想安装 teamviewer 的时候，提示说一些依赖找不到。到网上查了下，说可以使用：

```
sudo apt-get install -f
```

来在安装失败的时候自动安装上缺失的一些依赖。

但是，我试了下，却直接提示说会卸载 teamviewer。

后来才发现，如果你不是使用的原来官方的源，而是自己修改了源，那么可能找不到依赖，没法 fix，因此这个时候，还是要使用原来的源。

使用了原来的源之后，运行上面的 `sudo apt-get install -f` ，就会提示安装一些依赖。这样才完成的 teamviewer 的安装。







# 相关资料

- [ubuntu16.04 14.04更换源](https://www.cnblogs.com/dtiove/p/5917263.html)
