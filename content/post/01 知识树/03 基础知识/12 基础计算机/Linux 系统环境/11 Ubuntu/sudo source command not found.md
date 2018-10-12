---
title: sudo source command not found
toc: true
date: 2018-10-07
---
# sudo source :command not found


之前想用 sudo source ~/.bashrc 来刷新环境变量的时候，提示说：`sudo source: command not found`


The problem is that `source` is a bash build-in command (not a program - like `ls` or `grep`). I think one approach is to login as root and then execute the source command.

```bsh
sudo -s
source /etc/bash.bashrc
```


# 相关资料

- [sudo: source: command not found](https://askubuntu.com/questions/20953/sudo-source-command-not-found)
