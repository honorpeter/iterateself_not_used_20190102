---
title: Django DisallowedHost at  Invalid HTTP_HOST header
toc: true
date: 2018-06-11 08:15:04
---

## 相关资料

- [Django运行访问项目出现的问题:DisallowedHost at / Invalid HTTP_HOST header](https://blog.csdn.net/will5451/article/details/53861092)







## 需要补充的






  * aaa





* * *





# INTRODUCTION






  * aaa





# 缘由


在刚把django 博客放到服务器上运行的时候，它报错说：DisallowedHost at xx.xx.xx.xx Invalid HTTP_HOST header，查了下，解决了。


# 解决如下


修改一下 setting.py 文件中的 ALLOWED_HOSTS：

原来是：




  * ALLOWED_HOSTS = []


改为：


  * ALLOWED_HOSTS = ['*']  ＃在这里请求的host添加了＊


**具体原因没有追究**





















* * *





# COMMENT
