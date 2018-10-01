---
title: Git如何从远程拉取最新代码与本地代码合并
toc: true
date: 2018-09-10
---
# Git如何从远程拉取最新代码与本地代码合并


在团队开发中，git的使用已经很常见了，博主也是经常使用coding，github等代码托管平台。在多人协同开发中，我们经常会遇到这样的问题：A在本地开发完成后，将代码推送到远程，这时候B的本地代码的版本就低于远程代码的版本，这时候B该如何从远程拉取最新的代码，并与自己的本地代码合并呢？ 具体步骤如下：

1. 查看远程仓库:

```
git remote -v
```

1. 比如 在步骤一中，我们查看到远程有一个叫origin的仓库，我们可以使用如下命令从origin远程仓库获取最新版本的代码

```
git fetch origin master:temp
```

上面代码的意思是：从远程的origin仓库的master分支下载到本地master并新建一个temp分支

1. 查看temp分支与本地原有分支的不同

```
git diff temp
```

1. 将temp分支和本地的master分支合并

```
git merge temp
```

现在，B的本地代码已经和远程仓库处于同一个版本了，于是B可以开心coding了。

最后再提一下，上面的步骤中我们创建了temp分支，如果想要删除temp分支，也是可以的，命令如下：

```
git branch -d temp
```


## 相关资料

- [Git如何从远程拉取最新代码，并与本地代码合并](https://my.oschina.net/simonWang/blog/654998)
