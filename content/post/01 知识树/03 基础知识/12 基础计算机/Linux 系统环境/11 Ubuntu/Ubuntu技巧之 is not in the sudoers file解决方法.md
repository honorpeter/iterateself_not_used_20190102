---
title: Ubuntu技巧之 is not in the sudoers file解决方法
toc: true
date: 2018-11-25
---
# Ubuntu技巧之 is not in the sudoers file 解决方法

这个问题是在 git adduser git 然后使用 git 账户来创建 repo 的时候出现的，嗯，按照这个文章的确解决了这个问题。

本文介绍了在[Ubuntu](https://www.linuxidc.com/topicnews.aspx?tid=2)使用过程中遇到 is not in the sudoers file 时的解决办法。

用sudo时提示"xxx is not in the sudoers file. This incident will be reported.其中XXX是你的用户名，也就是你的用户名没有权限使用sudo,我们只要修改一下/etc/sudoers文件就行了。

例子：

www_linuxidc_com@linuxidc-Aspire-3680:~$ sudo add-apt-repository ppa:stk/dev
[sudo] password for www_linuxidc_com:
www_linuxidc_com is not in the sudoers file.  This incident will be reported.
www_linuxidc_com@linuxidc-Aspire-3680:~$

![Ubuntu技巧之 is not in the sudoers file解决方法](https://www.linuxidc.com/upload/2010_12/10120719174561.png)

下面是解决方法：

1）进入超级用户模式。也就是输入"su -",系统会让你输入超级用户密码，输入密码后就进入了超级用户模式。（当然，你也可以直接用root用）
(注意有- ，这和su是不同的，在用命令”su”的时候只是切换到root，但没有把root的环境变量传过去，还是当前用户的环境变量，用”su -”命令将环境变量也一起带过去，就象和root登录一样)

![Ubuntu技巧之 is not in the sudoers file解决方法](https://www.linuxidc.com/upload/2010_12/10120719187480.png)

2）添加文件的写权限。也就是输入命令"chmod u+w /etc/sudoers"。
3）编辑/etc/sudoers文件。也就是输入命令"gedit /etc/sudoers",进入编辑模式，找到这一 行："root ALL=(ALL) ALL"在起下面添加"www_linuxidc_com ALL=(ALL) ALL"(这里的xxx是你的用户名)，然后保存退出。

![Ubuntu技巧之 is not in the sudoers file解决方法](https://www.linuxidc.com/upload/2010_12/10120719186314.png)

4）撤销文件的写权限。也就是输入命令"chmod u-w /etc/sudoers"。





# 相关资料

- [Ubuntu技巧之 is not in the sudoers file 解决方法](https://www.linuxidc.com/Linux/2010-12/30386.htm)
