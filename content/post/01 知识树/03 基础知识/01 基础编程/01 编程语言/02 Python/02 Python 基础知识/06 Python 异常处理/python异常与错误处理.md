---
title: python异常与错误处理
toc: true
date: 2018-06-11 08:14:29
---
# python异常与错误处理

python里面异常到底怎么处理好？最好能整理出系统的，完善的方法


## 要点：




### 1.关于except的使用


代码如下：


    import traceback

    try:
        r = 10 / 0
    except ZeroDivisionError as e:
        print(e)
        r = 1
    else:
        print('没有异常')
    finally:
        print('不管有没有异常都执行')
    print(r)


输出：


    division by zero
    不管有没有异常都执行
    1




### 2.traceback的使用


**需要补充**


### 3.logging的使用与配置


**需要补充**


## COMMENT：
