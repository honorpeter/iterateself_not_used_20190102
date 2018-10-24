---
title: conda 创建 删除 环境
toc: true
date: 2018-10-24
---
# Anaconda 虚拟环境

## 创建环境


```
# 下面是创建python=3.6版本的环境，取名叫py36
conda create -n py36 python=3.6 
```



## 删除环境（不要乱删）

```
conda remove -n py36 --all
```



## 激活环境


```
# 下面这个py36是个环境名
source activate py36
```



## 退出环境

```
source deactivate
```




# 相关资料


- [Anaconda创建环境、删除环境、激活环境、退出环境](https://blog.csdn.net/H_O_W_E/article/details/77370456)
