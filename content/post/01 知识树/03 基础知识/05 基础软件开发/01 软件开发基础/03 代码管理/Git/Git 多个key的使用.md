---
title: Git 多个key的使用
toc: true
date: 2018-08-26 15:40:00
---
# Git 多个 key 的使用

当需要连接 github 的多个 repo 的时候，肯定要对应每个 repo 有不同的key，那么就需要每次在某个 repo 里提交的时候，要先把 key 加进去：

```
ssh-agent bash
ssh-add /c/Users/evo/.ssh/id_rsa_hugo
```

每次重启电脑之后，就需要重新更新一下，那么有什么好的办法呢？


按照第一个 文章配置了下，暂时还不知道有没有其效果。



## 相关资料


- [git-ssh-auth-win-setup.md](https://gist.github.com/bsara/5c4d90db3016814a3d2fe38d314f9c23)
- [Running SSH Agent when starting Git Bash on Windows](https://stackoverflow.com/questions/18404272/running-ssh-agent-when-starting-git-bash-on-windows)
- [Getting ssh-agent to work with git run from windows command shell](https://stackoverflow.com/questions/3669001/getting-ssh-agent-to-work-with-git-run-from-windows-command-shell/15870387#15870387)
- [Working with SSH key passphrases](https://help.github.com/articles/working-with-ssh-key-passphrases/#auto-launching-ssh-agent-on-git-for-windows)

