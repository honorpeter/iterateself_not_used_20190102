---
title: Python 2 与 3
toc: true
date: 2018-06-14 14:56:53
---
# 需要补充的

- 有些类库在 2 和 3 中已经变更了，也要总结下的，比如urllib requrest 什么的。

# python 2 与 python 3

## python 2 与 python 3 的区别


​
* `print`函数：3.x 必须加上`()`
* Unicode：3.x 默认使用unicode编码
* 除法运算：3.x 中整数相除也能得到浮点数的结果
* 异常：3.x 中只能抛出集成字`BaseException`的异常
* `xrange`：3.x 版本中取消了`xrange`，`range`与`xrange`一样位实现为惰性求值。因此`range`也变得很高效。 2.7 版本里面效率要求高的时候用`xrange`
* 二/八进制：<span style="color:red;">3.x版本必须强制写成0b1011和0o7236</span>
* 不等式：3.x 取消了`<>`  只有 `!=`
* ”“表达式：3.x 必须使用 repr 函数
* 多个模块改名：`Queue->queue`，`repr->reprlib`...
* 3.x 取消了`long`，统一为`int`
* 新增`bytes`类型，可与`string`相互转换  <span style="color:red;">bytes 类型？</span>
* `dict` 的 `keys`/`items`/`values` 方法返回迭代器，`iterkeys` 函数被废弃，`has_key` 被 `in` 取代。

## 对于中文的支持





## Python3 已经是大趋势了

本书使用的是 Python3，Python2 将会在 2020 年停止维护，所以整个社群转向 Python3 已经是大趋势了。

而且 Python3 不用担心编码问题，对于中文使用环境的我们来说，非常友好。



## 相关资料
