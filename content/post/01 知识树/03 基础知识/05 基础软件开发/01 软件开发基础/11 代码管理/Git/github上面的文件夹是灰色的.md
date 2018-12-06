---
title: github上面的文件夹是灰色的
toc: true
date: 2018-08-25 22:27:00
---

# 在自己的 repo 里 clone 了别的repo ，然后 push 的时候有问题

之前，我在使用 hugo 的时候，clone 了一个 theme 到 themes 文件夹，但是，我把整个repo push 到github 的时候，发现，好像并没有真的把 这个 even 的theme push 上去，而且，在 github 上看的话，这个文件夹是这样的：

![mark](http://images.iterate.site/blog/image/180825/fcF8J3JJlC.png?imageslim)

而普通的文件夹是这样的：

![mark](http://images.iterate.site/blog/image/180825/98kDhfAIlB.png?imageslim)

因此查了下：

这是因为子文件夹下还有 git 仓库。

做法是：

先把 even 剪切到另一个地方，然后 git add . git commit -m 'commit' git push 然后，把 even 里面的.git 文件夹删掉，再把 even 剪切到原来的地方，然后在提交，就行了。


## 相关资料

- [有时候发现git push后在github上文件夹是灰色的](https://blog.csdn.net/github_37360787/article/details/54619552)
