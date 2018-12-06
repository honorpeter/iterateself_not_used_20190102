---
title: ll command not found 当ll 无法识别时解决办法
toc: true
date: 2018-10-22
---
# ll command not found

ll 并不是linux下一个基本的命令，它实际上是 ls -l 的一个别名。

Ubuntu 默认不支持命令 ll，必须用 ls -l，这样使用起来不是很方便。

如果要使用此命令，可以作如下修改：

打开 `~/.bashrc`

找到 `#alias ll='ls -l'`，去掉前面的#就可以了。（关闭原来的终端才能使命令生效）

这样个人用户可以使用ll命令，当切换成超级用户后，使用ll命令时提示找不到命令，那是因为你只是修改了个人用户的配置，所以，切换成root后做相同的操作即可解决问题。

启示：我们可以通过修改 `~/.bashrc` 添加任何其他的命令别名。



操作如下：

- `vim ~/.bashrc` 编辑文件   加入 `alias ll='ls -l'` 如图![mark](http://images.iterate.site/blog/image/181022/IJ8bkjhGC4.png?imageslim)

- 保存。 `source ~/.bashrc` 立即生效



# 相关资料

- [ll command not found 当ll 无法识别时解决办法](https://blog.csdn.net/qq_27292113/article/details/69942507)
