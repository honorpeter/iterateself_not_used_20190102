---
title: Django makemigrations 时候报错：No changes detected
toc: true
date: 2018-06-11 08:15:04
---

## 相关资料

- [解决Django migrate No changes detected 不能创建表](https://blog.csdn.net/hanglinux/article/details/75645756)







## 需要补充的






  * aaa





* * *





# INTRODUCTION






  * aaa





##


我把django 博客放到服务器上运行之前，忘记 先把数据库生成了，结果说缺少一个表，我才想起来，于是运行：




  * python manage.py makemigrations


结果，却说：No changes detected

后来，查了下，知道了，原先生成的 __pycache__ 文件夹要删除掉。

因此我除掉每一个 app里面的 __pycache__ 文件夹。

然后重新生成：


  * python manage.py makemigrations


但是，还是报这个问题：No changes detected

我后面，只能每个 app 都 makemigrations：**为什么会有这个问题？**




  * python manage.py makemigrations blog


  * python manage.py makemigrations comment


然后：


  * python manage.py migrate


这样就可以了，数据库正确生成了。

























* * *





# COMMENT
