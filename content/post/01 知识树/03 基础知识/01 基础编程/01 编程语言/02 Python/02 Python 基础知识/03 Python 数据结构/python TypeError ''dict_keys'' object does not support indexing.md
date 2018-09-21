---
title: python TypeError ''dict_keys'' object does not support indexing
toc: true
date: 2018-06-11 08:14:48
---

## 相关资料


- [TypeError: 'dict_keys' object does not support indexing](https://blog.csdn.net/qq_18433441/article/details/54782459)




## 需要补充的






  * aaa




# MOTIVE





* * *





# 问题出现情景


在学习决策树的时候，有这么一句：first_str = tree.keys()[0] ，报错了：TypeError: 'dict_keys' object does not support indexing


# 问题原因和解决


这是由于 python3 改变了 dict.keys ，返回的是 dict_keys 对象，支持 iterable 但不支持 indexable，我们可以将其明确的转化成 list：


    a = {0:'左左',1:'右右'}
    k = list(a.keys())
    print(k[0])#输出0






















* * *





# COMMENT
