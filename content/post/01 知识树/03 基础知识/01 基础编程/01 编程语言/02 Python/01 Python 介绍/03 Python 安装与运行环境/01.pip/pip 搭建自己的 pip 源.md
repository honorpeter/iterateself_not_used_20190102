---
title: pip 搭建自己的 pip 源
toc: true
date: 2018-09-21
---



为什么会需要安装自己的 pip 源呢？

我是由于在离线的环境下想要安装 python 的环境，然后这个环境要用到 pip2pi ，又找了下找到这个的。

这个人说：当我们一个团队开发一个项目的时候，需要的 Python 第三方包基本是固定的，每次搭建新环境的时候总是因为各种内外网，https 问题花费大量的时间来安装运行环境。 所以搭建一个本地的，小巧的，只包含需要的 package 的源，或者 cache 都行，对于搭建环境可以节省很多时间。这个的确是一个使用的场景。而且是一个现实的问题。


- [Python环境下使用pip2pi搭建属于自己的pip源](https://blog.csdn.net/wenwenxiong/article/details/52474741)
- [Pipy 利用pip2pi搭建本地pypi源](https://blog.csdn.net/orangleliu/article/details/37969115)
