---
title: 01 Python 简介
toc: true
date: 2018-08-29
---
#### 第5章Python基础

Life is short, you need Python 人生苦短，你需要用Python

-Bruce Eckel

5.1 Python 简介

本节将介绍Python的最基本语法，以及一些和深度学习还有计算机视觉最相关的基本 使用。

5.1.1 Python 简史

Python是一门解释型的高级编程语言，特点是简单明确。Python作者是荷兰人Guido van Rossum, 1982年他获得数学和计算机硕士学位后，在荷兰数学与计算科学研究所 (Centrum Wiskunde & Informatica, CWI)谋了份差事。在 CWI 期间，Guido 参与到了一 门叫做ABC的语言开发工作中。ABC是一门教学语言，所以有简单、可读性好、语法更 接近自然语言等特点。在那个C语言一统天下的年代，ABC就是一股简单的清流。不过毕 竟是门教学语言，最后没有流行起来，但这段经历影响了 Guidoo 1989年的圣诞假期，Guido

决定设计一门简单易用的新语言，要介于C和Shell之间，同时吸取ABC语法中的优点， 并用自己喜欢的一部喜剧电视剧来命名这门语言《Monty Python’s Flying Circus》。

1991年，第一版基于C实现的Python编译器诞生，因为简单、拓展性好，Python很 快就在Guido的同事中大受欢迎，不久Python的核心开发人员就从Guido 一人变成了一个 小团队。后来随着互联网时代的到来，开源及社区合作的方式蓬勃发展，Python也借此上 了发展的快车道。因为Python非常容易拓展，在不同领域的开发者贡献下，许多受欢迎的 功能和特征被开发出来，渐渐形成了各种各样的库，其中一部分被加入到Python的标准库 中，这让本来就不需要过多思考底层细节的Python变得更加强大好用。在不过多考虑执行 效率的前提下，使用Python进行开发的周期相比传统的C/C++甚至Java等语言都大大缩 短，代码量也大幅降低，所以出bug的可能性也小了很多。因此有了语言专家Bruce Eckel 的那句名言：Life is short, you need Python。后来这句话的中文版“人生苦短，我用Python” 被Guido印在了 T恤上。发展至今，Python渐渐成了最流行的语言之一，在编程语言排行 榜TOBIE中常年占据前5的位置。另外随着Python的用户群越来越壮大，慢慢在本身特 点上发展出了自己的哲学，叫做Python的禅(The Zen of Python)。遵循Python哲学的做 法叫做很 Python (Pythonic)，具体参见 [https://www.python.org/dev/peps/pep-0020/](https://www.python.org/dev/peps/pep-0020/%e3%80%82)[。](https://www.python.org/dev/peps/pep-0020/%e3%80%82)

第5章Python基础

或者在Python中执行：

\>> import this

Python拥有很好的扩充性，可以非常轻松地用其他语言编写模块供调用，用Python 编写的模块也可以通过各种方式轻松被其他语言调用。所以一种常见的Python使用方式 是,底层复杂且对效率要求高的模块用C/C++等语言实现，顶层调用的API用Python封装， 这样可以通过简单的语法实现顶层逻辑，故而Python又被称为“胶水语言”。这种特性的 好处是无须花费很多时间在编程实现上，更多的时间可以专注于思考问题的逻辑。尤其是 对做算法和深度学习的从业人员，这种方式是非常理想的，所以现今的深度学习框架中， 除了 MATLAB或是Deepleaming4j这种给Java用的框架，其他框架基本上要么官方接口 就是Python,要么支持Python接口。

5.1.2安装和使用Python

Python有两大版本，考虑到用户群数量和库的各种框架的兼容性，本书以Python 2(2.7) 为准，语法尽量考虑和Python 3的兼容。

UNIX/Linux下的Python基本都是系统自带的，一般默认为Python 2，使用时在终端 直接输入python就能进入Python解释器界面：    <

dXcv^arreat-top:*$ python

Python 2.7.12 (default, Nov 19 2016, 06:48:10)

[GCC 5.4.0 20160609] on linux2

Type "help**, "copyright**, '.credits*' or "license'" for more information.

»>

在解释器下就已经可以进行最基本的编程了，例如：

dlcv^arreat    python

Python 2.7.12 (default, Nov 19 2016, 06:48:10)

[GCC 5.4.0 20160609] on linux2

Type ”help", "copyright”，"credits" or .’license” for more information,

\>» print ("hello world!") hello world•

»>

如写程序的话还是需要保存为文件再执行，比如写下面语句并且保存为helloworld.py： print(nHello world!")

然后在终端里执行：

dicv arreal    python helloworld.py

Hello world!

dlcv arreat-top

安装更多的python库一般有两种方法，第一是用系统的软件包管理，以Ubuntu 16.04 LTS为例，比如想要安装NumPy库(后面会介绍这个库)，软件包的名字就是python-numpy， 所以在终端中输入：

» sudo apt install python-numpy

第2篇实例精讲

Python自己也带了包管理器叫做pip：使用如下：

» pip install numpy

安装和深度学习相关的框架时，一般来说推荐使用系统自带的包管理，出现版本错误 的可能性低一些。另外也可以使用一些提前配置好很多第三方库的Python包，这些包通常 已经包含了深度学习框架中绝大多数的依赖库，比如最常用的是Anaconda,地址为 <https://www.continuum.io/downloadso>

Windows下的Python安装简单一些，从官方网站下载相应的安装程序就可以了，当然 也有更方便的已经包含了很全的第三方库的选择WinPython ,地址为 [http://winpython.github.io/,](http://winpython.github.io/,%e5%b9%b6%e4%b8%94%e6%98%af%e7%bb%bf%e8%89%b2%e7%9a%84%ef%bc%8c%e7%9b%b4%e6%8e%a5%e6%89%a7%e8%a1%8c%e5%8d%b3%e5%8f%af%e3%80%82)[并且是绿色的，直接执行即可。](http://winpython.github.io/,%e5%b9%b6%e4%b8%94%e6%98%af%e7%bb%bf%e8%89%b2%e7%9a%84%ef%bc%8c%e7%9b%b4%e6%8e%a5%e6%89%a7%e8%a1%8c%e5%8d%b3%e5%8f%af%e3%80%82)

5.2 Python基本语法

There should be one— and preferably only one —obvious way to do it.

对于一个特定的问题，应该只用最好的一种方法来解决。

-Tim Peters

5.2.1基本数据类型和运算

1.基本数据类型

Python中最基本的数据类型包括整型、浮点数、布尔值和字符串。类型是不需要声明

| 的，比如： |         |      |          |
| ---------- | ------- | ---- | -------- |
| a =        | 1       | #    | 整数     |
| b =        | 1.2     | #    | 浮点数   |
| c =        | True    | #    | 布尔类型 |
| d =        | HFalse" | #    | 字符串   |
| e =        | None    | #    | NoneType |

其中#是行内注释的意思。最后一个None是NoneType，注意不是0。在Python中利 用type()函数可以查看一个变量的类型：

| type(a) | #    | <type | 1int'>      |
| ------- | ---- | ----- | ----------- |
| type(b) | #    | <type | •float)     |
| type(c) | #    | <type | ^001*>      |
| type(d) | #    | <type | * str ’〉   |
| type(e) | #    | <type | 1NoneType'> |

注释中是执行type()函数后的输出结果，可以看到None是单独的一种类型NoneTypeo 在很多API中，如果执行失败就会返回None。

2.变量和引用

Python中基本变量的赋值一般建立的是个引用，比如下面的语句：

a =    1

b = a c =    1

a赋值为1后，b=a执行时并不会将a的值复制一遍，然后赋给b,而是简单地为a所

指的值，也就是1建立了一个引用，相当于a和b都是指向包含1这个值的内存的指针。

所以c=l执行的也是个引用建立，这3个变量其实是3个引用，指向同一个值。这个逻辑

虽然简单但也常易混淆，这没关系，Python内置了 id()函数，可以返回一个对象的地址，

用id()函数可以让我们知道每个变量指向的是不是同一个值：

id(a)    #    35556792L

id(b)    #    35556792L

id(c)    #    35556792L

注释中表示的仍是执行后的结果。如果这时候接下面两个语句：

b = 2    #    b的引用到新的一个变量上

id(b)    #    35556768L

可以看到b引用到了另一个变量上。

3.运算符

Python中数值的基本运算和C差不多，字符串的运算更方便，下面是常见的例子。

| a =      | 2    |                                                              |      |                                                          |
| -------- | ---- | ------------------------------------------------------------ | ---- | -------------------------------------------------------- |
| b        | =    | 2.3                                                          |      |                                                          |
| c        | =    | 3                                                            |      |                                                          |
| a        | +    | b                                                            | #    | 2    +    2.3    =    4.3    ,                           |
| c        | -    | a                                                            |      | 3-2    =    1    -                                       |
| a        | /    | b    #整数除以浮点数，运算以浮点数为准，2    /    2.3    =    0.8695652173913044 |      |                                                          |
| a        | /    | C                                                            | #    | Python 2中，整数除法，向下取整2/3    =    0              |
| a        | ★ ★  | C                                                            | #    | a的c次方，结果为8                                        |
| a        | +=   | 1                                                            | #    | Python中没有的用法，自增用+=                             |
| c        | -=   | 3                                                            | #    | c变成0 了                                                |
| d        | =    | 'Hello*                                                      |      |                                                          |
| d        | +    | 'world!*                                                     | #    | 相当于字符串拼接，结果为，Hello world!'                  |
| d        | +=   | * "world"!                                                   |      | 相当于把字符串接在当前字符串尾，d变为：Hello "world" ! 1 |
| e        | =    | r'\n\t\\»                                                    |      |                                                          |
| print(e) | #    | •WnWtWW*                                                     |      |                                                          |

需要注意的几点是：第一点，字符串用双引号和单引号都可以，区别主要是单引号字 符串中如果出现单引号字符则需要用转义符，双引号也是一样，所以在单引号字符串中使 用双引号，或者双引号字符串中使用单引号就会比较方便。另外3个双引号或者3个单引 号围起来的也是字符串，因为换行方便，更多用于文档。

第二点，Python 2中两个数值相除会根据数值类型判断是否整数除法，Python 3中则 都按照浮点数。想要在Python 2中也执行Python 3中的除法，只要执行下面语句：

from _future_ import division    # 使用 Python 3 中的除法

1    /    -    #    0.5

第三点，字符串前加r表示字符串内容严格按照输入的样子，好处是不用转义符了， 非常方便。

Python中的布尔值和逻辑的运算非常直接，例如：

| a     | =True  |
| ----- | ------ |
| b     | =False |
| a     | and b  |
| a     | or b   |
| not a |        |

\#    False

\#    True

\#    False

Python中也有位操作:

\4. ==， Mtlis

按位翻转，1000 右移3位，1000 左移3位，0001 按位与，101    &

按位或，101    |

按位异或，100

--> -(1000+1) —> 0001 —> 1000 010    =    000

010    =    111

001 = 101

Python中判断是否相等或者不等的语法和C语言一样，另外在Python中也常常见到 is操作符，两者的区别在于=和!=比较引用指向的内存中的内容，而is判断两个变量是否 指向一个地址，看下面的代码例子：

a    ==    b    #    True,值相等

a    is    b    #    False,指向的不是一个对象，这个语句等效于id(a) == id(b)

a    is    c    #    True，指向的都是整型值1

所以一定要分清要比较的对象应该用哪种方式，对于一些特殊的情况，比如None,本 着 Pythonic 的原则，最好用 is None / is not None。

5.注意关键字

Python中，万物皆对象。不过这并不是本节要探讨的话题，这里想说的是一定要注意 关键字，因为所有东西都是对象，所以一个简简单单的赋值操作就可以把系统内置的函数 给变成一个普通变量，下面来看例子：

id(type)

type =    1

id(type)

id = 2

from _future_ import

print =    3

\#    506070640L

\#    type成了指向1的变量

\#    35556792L

\#    id成了指向2的变量 print_function

\#    print成了指向3的变量

注意，print是个很特殊的存在，在Python 3中是按照函数用法用，而在Python 2中却 是命令式的语句，最早prim的用法其实是这样的：

print "Hello world!"

这样用主要是受到ABC语法的影响，但这个用法并不Pythonic,后来加入了 print函 数，为了兼容允许两种用法并存。所以单纯给print赋值是不灵的，在Python 2中使用Python 3中的一些特性都是用from _future_ import来实现。

6.模块导入

因为提到了对象名覆盖和import,所以这里简单讲一下。import是利用Python中各种

强大库的基础，比如要计算COS(7I)的值，可以有下面4种方式：

\#直接导入Python的内置基础数学库 import math

print(math.cos(math.pi))

\#从math中导入cos函数和pi变量 from math import cos, pi print(cos(pi))

\#如果是模块，在导入的时候可以起个别名，避免名字冲突或是方便使用 import math as m print(m.cos(m.pi))

\#从math中导入所有东西 from math import * print(cos(pi))

一般来说最后一种方式不是很推荐，因为不知道import导入的名字里是否和现有对象 名有冲突，很可能会不知不觉覆盖了现有的对象。

5.2.2容器

1.列表

Python中的容器是异常好用且异常有用的结构。本节主要介绍列表(list)，元组(tuple), 字典(diet)和集合(set)。这些结构和其他语言中的类似构并无本质不同，下面来通过 例子了解用法。

| a =  | [1,  | 2,    3,    4]    |
| ---- | ---- | ----------------- |
| b =  | [1]  |                   |
| c =  | [1]  |                   |
| d =  | b    |                   |
| e =  | [1,  | "Hello world!", c |

False]

\#    (194100040L,    194100552L)

\#    (194100040L,    194100040L)

\#    True

\#利用list函数从任何可遍历结构初始化

\#    fa' ,    *b',    :c',    ]

\#    [0, 0, 0, 1, 1, 1, 1, 2, 2]

print(id(b) , id(c))

print(id(b) , id(d))

print (b == c)

f = list("abed")

print(f)

g =    [0]*3    +    [1]*4    +    [2]*2

因为变量其实是对象的引用，对列表而言也没什么不同，所以列表对元素的类型没什 么限制。也正因为如此，和变量不同的是，即使用相同的语句赋值，列表的地址也是不同 的，在这个例子中体现在id(b)和id(c)不相等而内容相等。列表也可以用list()初始化，输入 参数需要是一个可以遍历的结构，其中每一个元素会作为列表的一项。操作符对于列 表而言是复制，最后一个语句用这种办法生成了分段的列表。

列表的基本操作有访问、增加、删除、拼接、子序列和倒序等：

a =    [1,    2,    3,    4]

a .pop ()    #把最后一个值4从列表中移除并作为pop的返回值

4 in a    # 判断4是否在a中，False

| a.append (5)             | #    | 末尾插入值，[1,    2,    3,    5]                            |
| ------------------------ | ---- | ------------------------------------------------------------ |
| a.index (2)              | #    | 找到第一个2所在的位置，也就是1                               |
| a[2]                     | #    | 取下标，即位置在2的值，也就是第3个值3                        |
| a +=    [4Z    3，    2] | #    | 拼接，[1,    2,    3,    5,    4,    3,    2]                |
| a.insert(1,    0)        | #    | 在下标为1处插入元素0，[1,    0,    2,    3,    5,    4,    3,    2] |
| a.remove(2)              | #    | 移除第一个 2，[1,    0,    3,    5,    4,    3,    2]        |
| a.reverse ()             | #    | 倒序，返回值为0，a变为[2,    3,    4,    5,    3,    0,    1] |
| a[3]    =    9           | #    | 指定下标处赋值，[2,    3,    4,    9,    3,    0,    1]      |
| b = a [2 : 5]            | #    | 取下标2开始到5之前的子序列，[4,    9,    3],此类方法叫做     |

slicing

| C    | =a[2:-2] |
| ---- | -------- |
| d    | =a[2:]   |
| e    | =a[:5]   |
| f    | =a [:]   |
| a[   | 2：-2]=[ |
| g    | =a[::-1] |

a.sort () print(a)

| #    | 下标也可以很方便地倒着数，-1对应最后一个元素，［4,          | 9,   | 3]    |
| ---- | ----------------------------------------------------------- | ---- | ----- |
| #    | 取下标2开始到结尾的子序列，［4,    9,    3,    0,    1］    |      |       |
| #    | 取开始到下标5之前的子序列，［2,    3,    4,    9,    3］    |      |       |
| #    | 取从开头到最后的整个子序列，相当于值拷贝，［2, 3, 4, 9,     | 3,   | 0, 1] |
| 2,   | 3］    #赋值也可以按照片段来，［2,    3,    1,    2,    3,  | 0,   | 1]    |
| #    | 也是倒序，通过slicing实现并赋值，效率略低于reverse          | 0    |       |
| #    | 列表内排序，返回值为None, a变为［0,    1,    1,    2,    2, | 3,   | ,3]   |

因为列表是有顺序的，所以和顺序相关的操作是列表中最常见的，首先来打乱一个列 表的顺序，然后再对这个列表排序。

import random

生成一个列表，从0开始+1递增到9

［0,    1,    2,    3,    4,    5,    6,    7,    8,    9］

shuffle函数可以对可遍历且可变结构打乱顺序

| [4,    3, | 8Z   |      | 0,   | 6,   | 2,   | 7,   | 5,   | 1]   |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| [0, 1,    | 2,   | 3,   | 4,   | 5,   | 6,   |      |      | 9]   |
| [9,    8, | 7,   | 6,   | 5,   | 4,   | 3,   | 2,   | lz   | 0]   |

其中range函数是一个可以生成等差数列的函数，比如代码中生成了 0〜9的10个元 素的列表。

2.元组

元组和列表有很多相似的地方，最大的区别在于不可变，此外，如果初始化只包含一 个元素的tuple,和初始化只包含一个元素的列表语法不一样，因为语法必须明确，所以必 须在元素后加上逗号。另外，直接用逗号分隔多个元素赋值默认是tuple,这在函数有多个 返回值的时候很好角。

\#也可以从列表初始化

print(e)

3.集合

集合是一种很有用的数学操作，比如列表去重，或是理清两组数据之间的关系，集合 的操作符和位操作符有交集，注意不要混淆。

| A =  | set  | ([1, | 2,   | 3,   |
| ---- | ---- | ---- | ---- | ---- |
| B =  | {3,  | 4,   | 5,   | 6}   |
| C =  | set  | ([1, | 1,   | 2,   |

print(C) print (A | B) print(A & B) print (A - B) print (B - A) print (A B)

4])

第5章Python基础

4.字典

字典是一种非常常见的“键-值” (key-value)映射结构，键无重复，一个键不能对应 多个值，不过多个键可以指向一个值。下面还是通过例子来了解，构建一个名字■-年龄的 字典，并执行一些常见操作。

a =    {* Tom':    8,    1 Jerry1:    7}

print(a[* Tom1])    #    8

b = dict(Tom=8, Jerry=7)    #

print(b[1 Tom* ])    #

一种字符串作为键更方便的初始化方式

8

if 'Jerry' in a:

print(a[* Jerry'])

\#判断1 Jerry *是否在keys里 #    7

print(a.values())

\# None,通过get获得值，即使键不存在也不会报异常

Mammy Two Shoes * :    42})

\# dict_values ( [8,    2,    3,    7,    10,    42])

print (a. pop (' Mammy Two Shoes’)) # 移除,Mammy Two Shoes* 的键值对，并返回 42 print(a.keys ()) # dict_keys([* Tom *,    *Tuffy',    * Tyke', ’Jerry', ’Spike*])

读者可能注意到初始化字典和集合很像，的确如此，集合就像是没有值只有键的字典。 既然有了人名到年龄的映射，是否可以给字典排序？在Python 3.6之前，这个问题是错误 的，字典是一种映射关系，没有顺序。当然，如果要把(键，值)的^对进行排序，是 没有问题的，前提是先把字典转化成可排序的结构，items()或者iteritemsO函数可以做到这 件事，接上段代码继续：

b = a.items()

print(b)    # [(，Tuffy', 2),    (1 Spike',    10),    ('Tom'r 8),    ('Tyke',

3), ('Jerry', 7)]

from operator import itemgetter c = sorted (a. items () , key=itemgetter ⑴)

print (c)    #    [ ('Tuffy' ,    2), ('Tyke，， 3),    ('Jerry' ,    7),    (,Tom,,    8),

(’Spike、 10)]

d = sorted(a.iteritems (), key=itemgetter (1))

print (d)    #    [ (^Tuffy* z 2),    ('Tyke* ,    3), (’Jerry，， 7), (，Tom\ 8),

('Spike，， 10)] e = sorted(a)

print (e)    # 只对键排序，['Jerry', 'Spike' z 'Tom',丨 Tuffy1, 'Tyke1 ]

items函数可以把字典中的键值对转化成一个列表，其中每个元素是一个tuple, tuple

的第一个元素是键，第二个元素是值。变量c是按照值排序，所以需要一个操作符itemgetter

取位置为1的元素作为排序参考，如果直接对字典排序，则其实相当于只是对键排序。字

典被当作一个普通的可遍历结构使用时，都相当于遍历字典的键。如果觉得字典没有顺序

不方便，可以考虑使用OrderedDict，使用方式如下：

from collections import OrderedDict a =    {1:    2,    3:    4,    5:    6,    7:    8,    9:    10}

b = OrderedDict ({1:    2,    3:    4,    5:    6,    7:    8,    9:    10})

print (a)    # {1: 2, 3: 4, 9: 10, 5: 6, 7: 8}

print (b)    # OrderedDict ([ (1，2) , (3, 4) , (9, 10) , (5, 6) , (7, 8)])

这样初始化时的顺序就保留了，除了有序的特性以外，用法上和字典没有区别。2016 年9月，Guido宣布在Python 3.6中字典将默认有序，这样就不用纠结了。另外需要注意 的一点是字典是通过哈希表实现的，所以键必须是可哈希的，list不能被哈希，所以也不能

第2篇实例精讲

作为字典的键，而tuple就可以。

因为上段代码中用到了 iteritems函数，所以这里顺带提一下迭代器(iterator)。迭代 器相当于一个函数，每次调用都返回下一个元素，从遍历的角度看和列表没有区别。 iteritemsO函数就是一个迭代器，所以效果一样，区别是迭代器占用更少内存，因为不需要 一上来就生成整个列表。一般来说，如果只需要遍历一次，用迭代器是更好的选择，若是 要多次频繁从一个可遍历结构中取值且内存够，则直接生成整个列表会更好。当然，用迭 代器生成一个完整列表并不麻烦，所以有个趋势是把迭代器作为默认的可遍历方式，比如 前面使用过用来生成等差数列列表的range()函数，在Python 2中对应的迭代器形式是 xrange()函数。在Python 3中，range()函数就不再产生一个列表了，而是作为迭代器，xrange() 函数直接消失了。

5.2.3分支和循环

从本节开始，代码就未必适合在Python终端中输入了，读者可选个熟悉的编辑器或者 IDE。笔者推荐可用PyCharm ,其虽然慢但好用，社区版免费下载地址为 [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/%e3%80%82)[。](https://www.jetbrains.com/pycharm/%e3%80%82)

\1. for循环

前面提到的4种容器类型都是可遍历的，所以该讲讲用来遍历的for循环了。for循环 的语法也是简单的英语：

| a    | =「This、      | ’ is ’， | fa'z   | 'list、 1 !']           |
| ---- | -------------- | -------- | ------ | ----------------------- |
| b    | =['This，，    | * is * r | 'a\    | :tuple,, :!,]           |
| c    | ={* ThisJ:     | ’ is 1,  | 'an':  | * unordered1,    * diet |
| #    | 依次输出：^Thi | s’，'    | 'is *, | 'list1,    1 ! 1        |

for x in a:

| print(x)           |        |                  |
| ------------------ | ------ | ---------------- |
| #依次输出：•This、 | ’ is', | 1 a * z 'tuple ’ |

for x in b:

print(x)

\#键的遍历。不依次输出：•This1, ：dict\ 'an' for key in c:

print(key)

\#依次输出0到9

for i in range(10):

print(i)

注意，每个for循环中，print都有缩进，这是Python中一个让人爱恨交织的特点：强 行缩进来表明成块的代码。这样做的好处是代码十分清晰工整，有助于防止写出过长的函 数或者过深的嵌套，坏处是有时不知为什么Tab缩进和空格就一起出现了，或是多重if-else 不知什么原因对不齐，有些麻烦。

回到for循环上，这种把每个元素拿出来的遍历方式叫for each风格，熟悉Java的人 就不会陌生，C++11中也开始支持这种for循环方式。但如果还是需要下标呢？比如遍历 一个list的时候，希望对应下标也打印出来，这时可以用enumerate。

names =    ["Rick，'， "Daryl", "Glenn"]

\#依次输出下标和名字

for i, name in enumerate (names): print(i, name)

需要注意的是，通过取下标遍历当然是可行的，比如用len()函数获得列表长度，然后

用range()/xrange()函数获得下标，但是并不推荐这样做。

words = ["This", "is", "not", "recommended"]

\# not pythonic :(

for i in xrange(len(words)):

print(words[i])

在使用for循环时，有时会遇到这样一种场景：需要对遍历的每个元素进行某种判断， 如果符合这种判断的情况没有发生，则执行一个操作。举个例子，某神秘部门要审核一个

字符串列表，如果没有发现不和谐的字眼，则将内容放心通过，一种解决办法是下面这样: wusuowei =["工"，"don * t", "give", "a", "shit"] # 无所谓 hexie = True    #默认和谐社会

for x in wusuowei:

if x ==    :

print("What the f**k!") hexie = False

break

if hexie:

print("Harmonious society!")

\#发现了不该出现的东西，WTF! #不和谐了

\#赶紧停下！不能再唱了 #未发现不和谐元素！

\#和谐社会！

这样需要设置一个标记是否发现不和谐因素的状态变量hexie,循环结束后再根据这个

变量判断内容是否可以放心通过。一种更简洁不过有些小众的做法是直＜捧和else—起，如

果for循环中的if块内的语句没有被触发，则通过else执行指定操作：＜

wusuowei =["工”，"don't", "give", "a", "shit"] for x in wusuowei:

if x ==

print("What the f**k!")

hexie = False

break

else:    # for循环中if内语句未被触发

print ("Harmonious society!’’) # 和谐社会！

\2. if和分支结构

上一个例子中已经出现if语句了，所以这部分先讲讲if。Python的条件控制主要是3

个关键字：if-elif-else,其中elif就是else

if的意思。下面还是看例子:

pets =    [* dog *,    * cat',    * droid*,

for pet in pets:

| if pet ==   | * dog *:=    * steak |          |
| ----------- | -------------------- | -------- |
|             | food                 |          |
| elif        | pet ==               | * cat *: |
|             | food                 | ='milk'  |
| elif        | pet ==               | 'droid'  |
|             | food                 | =* oil * |
| elif        | pet ==               | 'fly':   |
|             | food                 | =:sh*t.  |
| else:       | pass                 |          |
| print(food) |                      |          |

'fly1]

\#

\#

\#

\#

\#

\#

人

粮排粮奶器油姆 狗牛猫牛机机苍

需要提一下的是pass,这就是个空语句，什么也不做，占位用。Python并没有switch-case 的语法，等效的用法要么是像上面一样用if-elif-else组合，要么可以考虑字典：

pets =    [1 dog',    1 cat *,    'droid *,    1 fly *]

food_for_pet =    {

'dog *:    * steak',

1 cat *: 'milk*,

'droid*:    'oil',

'fly，： ’sh*t，

}

for pet in pets:

food = food_for_pet [pet] if pet in food_for_pet else None print(food)

这里还用到了一个if-else常见的行内应用，就是代替三元操作符，如果键在字典中， 则food取字典的对应值，否则为None。

\3.    if表达式中的小技巧

通过链式比较让语句更简洁：

Python中的对象都会关联一个真值，所以在if表达式中判断是否为False或者是否为 空的时候，无须写出明确的表达式。

a = True

if a:    #判断是否为真，相较于a is True

print(1 a is True'〉

if * sky * :    #判断是否空字符串，相较于len(*sky*) > 0

prin^.( 'birds')

if    #判断是否空字符串，同上

print(* Nothing!')

if {}：    #判断是否空的容器(字典)，相较于len({})    〉0

print(’Nothing!’)

隐式表达式为False的有如下状况：

□    None;

□    False;

□数值0;

□空的容器或序列(字符串也是一种序列)；

□用户自定义类中，如果定义了_len_0或者_nOnzerO_0,并且被调用后返回0 或者False。

\4.    while循环

While循环就是循环和if的综合体，是一种单纯的基于条件的循环，本身没有遍历的 意思，这是和for-each的本质差别，这种区别比起C/C++中要明确得多，用法如下：

i = 0

while i <    100:    # 笑 100 遍

print("ha")

while True:    # 一直笑

print("han)

5.2.4函数、生成器和类

1.函数

首先还是从几个例子看起:

def say_hello ():

print(* Hello!*)

| def                    | greetings        | (x= * Good   | morning!'):   |               |                      |
| ---------------------- | ---------------- | ------------ | ------------- | ------------- | -------------------- |
|                        | print (x         | )            |               |               |                      |
| say                    | hello()          |              |               | #             | Hello!               |
| greetings()            |                  |              | #             | Good morning! |                      |
| greetings("What’s up!’ |                  | #            | What * s up!  |               |                      |
| a =                    | greetings()      |              | #             | 返回值是None  |                      |
| def                    | create a         | list(x,      | y=2,    z=3): | #             | 默认参数项必须放后面 |
|                        | return           | [x, y,       | z]            |               |                      |
| b =                    | create a         | _list (1)    |               | #             | [1,    2,    3]      |
| c =                    | create a         | list(3,      | 3)            | #             | [3,    3,    3]      |
| d =                    | create a         | :list(6,     | 7,    8)      | #             | [6,    7,    8]      |
| def                    | traverse         | args(*args): |               |               |                      |
|                        | for arg in args: |              |               |               |                      |

print(arg) traverse_args(1,    2,    3)

\#依次打印il, 2, 3 #依次打印A, B, C, D

traverse_args(*A*,    'B' z *C1,    *D')

def traverse_kargs(**kwargs):

for k, v in kwargs.items () print(k, v)

traverse_kargs (x=3,    y=4,    z=5) # 依次打印('x*,    3),    (’y’，4),    (' z' z

5)

traverse_kargs(fighter1='Fedor', fighter2=•Randleman ’) def foo(x, y, *args, **kwargs):

print(x, y) print(args) print(kwargs)

\#第1个pring输出(1,    2)

\#    第 2 个 print 输出(3,    4,    5)

\#    第 3 个 print 输出{ 1 a’ ：    3,    'b1 : 'bar1 }

foo (1,    2,    3,    4,    5,    a=6, b=’bar’)

Python和很多语言一样，括号里面定义参数，参数可以有默认值，且默认值不能在无 默认值参数之前。Python中的返回值用return定义，如果没有定义返回值，默认返回值是 Noneo参数的定义可以非常灵活，可以有定义好的固定参数，也可以有可变长的参数(args: arguments)和关键字参数(kargs: keyword arguments)。如果要把这些参数都混用，则固 定参数在最前，关键字参数在最后。

Python中万物皆对象，所以有些情况下函数也可以当成一个变量使用。比如前面提到 的用字典代替switch-case的用法，有时要执行的不是通过条件判断得到对应的变量，而是

执行某个动作，比如有个小机器人在坐标(0,0)处，我们用不同的动作控制小机器人移动:

moves =    [1 up1z * left *,

coord =    [0,    0]

for move in moves:

if move == 'up':

coord[1]    +=    1

elif move ==    1 down1 :

\* right']

\#向上，纵坐标+1

\#向下，纵坐标-1

coord[1]    -=    1

| elif         | move ==  | 'left*:   | #                | 向左，横坐标-1 |
| ------------ | -------- | --------- | ---------------- | -------------- |
|              | coord[0] | -=1       |                  |                |
| elif         | move ==  | 'right *: | #                | 向右，横坐标+1 |
|              | coord[0] | += 1      |                  |                |
| else:        | pass     |           |                  |                |
| print(coord) |          | #         | 打印当前位置坐标 |                |

不同条件下对应的是对坐标这个列表中的值的操作，单纯的从字典取值就办不到了， 所以就把函数作为字典的值，然后用这个得到的值执行相应动作。

| moves =    [ * up * z ' left *, | * down *, | 'right1]        |
| ------------------------------- | --------- | --------------- |
| def move up (x):                |           | #定义向上的操作 |
| x[T] +=    1                    |           |                 |
| def move down (x):              |           | #定义向下的操作 |
| x[l] ―    1                     |           |                 |
| def move left (x):              |           | #定义向左的操作 |
| x[0]    -=    1                 |           |                 |
| def move right (x):             |           | #定义向右的操作 |

x[0]    +=    1

\#动作和执行的函数关联起来，函数作为键对应的值

actions =    {

\*    up * : move_up,

'down *: move_down,

'left *: move_left,

\*    right *: move_right

}

coord =    [0,    0]

for move in moves:

actions[move](coord) print(coord)

把函数作为值到后，直接加个括号就可以使用了，这样做在循环部分看上去很简洁。

有些类似C语言中的函数指针但更简单。其实这种用法在之前讲排序的时候已经见过了，

就是 operator 中的 itemgetter。itemgetter(l)得到的是一个可调用对象(callable object)，和

返回下标为1的元素的函数用法是一样的。

def get_val_at_pos_l(x): return x[l]

]

sorted_pairsO = sorted(heros, key=get_val_at_pos_l) sorted_pairsl = sorted(heros, key=lambda x: x [1]) print(sorted_pairsO)

print(sorted_pairsl)

在这个例子中用到了一种特殊的函数：lambda表达式。lambda表达式在Python中是

一种匿名函数，lambda关键字后面跟输入参数，然后冒号后面是返回值(的表达式)，比

如前面例子中就是一个取下标1元素的函数。当然还是那句话，万物皆对象，给lambda

表达式取名字也是一点问题没有的。

some_ops = lambda x, y: x + y + x*y + x**y some_ops (2f 3)    # 2 + 3 + 2*3 + 2A3 = 19

2.生成器(Generator)

生成器是迭代器的一种，形式上看和函数很像，只是把return换成了 yield,在每次调

用的时候都会执行到yield并返回值，同时将当前状态保存，等待下次执行到yield再继续。

\#从10倒数到0 def countdown(x):

while x >=    0:

yield x x -=    1

for i in countdown(10): print(i)

\#打印小于100的斐波那契数 def fibonacci(n):

a =    0

b =    1

while b < n:

yield b

a, b = b, a + b for x in fibonacci(100):

print(x)

生成器和所有可迭代结构一样，可以通过next()函数返回下一个值，如果迭代结束了

则抛出Stoplteration异常：

1

1

2

抛出 Stoplteration 异常

Python 3.3以上可以允许yield和return同时使用，return的是异常的说明信息:

\# Python 3.3以上可以return返回异常的说明

def another fibonacci(n): a =    0

b =    1

while b < n:

yield b

| a,                       | b    | =b, a + b                              |
| ------------------------ | ---- | -------------------------------------- |
| return "                 | 'No  | more . . . n                           |
| a = another fibonacci(3) |      |                                        |
| print(next(a))           | #    | 1                                      |
| print(next(a))           | #    | 1                                      |
| print(next(a))           | #    | 2                                      |
| print(next(a))           | #    | 抛出Stoplteration异常并打印No more消息 |

3•类(Class)

Python中的类的概念和其他语言类似，比较特殊的是protected和private在Python中 是没有明确限制的，通常的惯例是用单下画线开头的表示protected,用双下画线开头的表 示 private。

class A:

’""•Class a'""' def _init_(self, x, self.x = x self.y = y self._name =

y, name):

name

| def introduce(self): |                                           |
| -------------------- | ----------------------------------------- |
|                      | print(self. name)                         |
| def                  | greeting(self):print("What * s up!")      |
| def                  | _12norm(self):return self.x**2    + self. |
| def                  | cal 12norm(self):return self._12norm()    |
| A(ll,                | 11,    'Leonardo1)                        |

print (A._doc_)

a.introduce() a.greeting() print(a.—name > print(a.cal_12norm()) print(a,_A_12norm()) print(a._12norm())

\#    "Class A"

\#    "Leonardo"

\#    "What * s up!"

\#可以正常访问

\# 输出 11*11 + 11*11=242 #仍然可以访问，只是名字不一样

\# 报错：'A' object has no

attribute

12norm*

类的初始化使用的是_init_(self,)，所有成员变量都是self的，所以以self.开头。可 以看到，单下画线开头的变量是可以直接访问的，而双下画线开头的变量则触发了 Python 中一种叫做name mangling的机制，其实只是名字变了，仍然可以通过前面加上“_类名” 的方式访问。也就是说Python中变量的访问权限都是靠自觉的。类定义中紧跟着类名字下 一行的字符串叫做docstring,可以写一些用于描述类的介绍，如果有定义则通过“类 名._doC_”访问。这种前后都加双下画线访问的是特殊的变量/方法，除了_加(:_和 _init_还有很多，这里就不展开讲了。

Python中的继承也非常简单，最基本的继承方式就是定义类的时候把父类放入括号里 即可。

class B(A):

"""CJ_ass B inheritenced from A" def ^greeting (self):

print("How * s going!")

b =    B(12,    12f 'Flaubert1)

\#    Flaubert

\#    How * s going!

\#    Flaubert

\#    ''私有〃方法，必须通过A 12norm访问

b.introduce() b.greeting() print(b._name()) print(b,_A_12norm())

• 162 •

5.2.5 map、reduce 和 filter

map可以用于对可遍历结构的每个元素执行同样的操作，批量操作：

map (lambda x:    x**2,    [1,    2,    3,    4])    #    [1,    4,    9,    16]

map (lambda x,    y: x    + y, [1,    2,    3],    [5,    6,    7] )    #    [6,    8,    10]

reduce则是对可遍历结构的元素按顺序进行两个输入参数的操作，并且每次的结果保 存作为下次操作的第一个输入参数，还没有遍历的元素作为第二个输入参数。这样的结果 就是把一串可遍历的值，减少(reduce)成一个对象：

reduce (lambda    x,    y:    x + y,    [1,    2,    3,    4])    #    ( (1+2) +3) +4=10

filter顾名思义，根据条件对可遍历结构进行筛选：

filter (lambda    x:    x    % 2f [1,    2,    3,    4,    5])    # 筛选奇数，[1,    3,    5]

需要注意的是，对于filter和map，在Python 2中返回结果是列表，而在Python 3中

是生成器。

5.2.6 列表生成(list comprehension)

列表生成是Python 2.0中加入的一种语法，可以非常方便地用来生成列表和迭代器， 比如5.2.5节中map的两个例子和filter的一个例子可以用列表生成重写为：

5.X

7

2

6

%

\# # #



3

6

1

nu TJ

9 15

zip()函数可以把多个列表关联起来，在这个例子中，通过zip()函数可以按顺序同时输 出两个列表对应位置的元素对。有一点需要注意的是，zip()函数不会自动帮助判断两个列 表是否长度一样，所以最终的结果会以短的列表为准，想要以长的列表为准，可以考虑 itertools模块中的izip_longest()函数。如果要生成迭代器，只需要把方括号换成小括号，生 成字典也非常容易。

至于列表生成和map/filter应该优先用哪种，这个问题很难回答，尔过Python创始人 Guido似乎不喜欢map/filter/reduce,他曾表示过一些从函数式编程里拿来的特性是个错误。

5.2.7字符串

| Python中字符串相关的处理都非常方便，下面来看例子。 |                  |                                                 |
| -------------------------------------------------- | ---------------- | ----------------------------------------------- |
| a =    1 Life is short,                            | you need Python' |                                                 |
| a.lower()                                          | #                | 'life is short, you need Python *               |
| a.upper()                                          | #                | 'LIFE IS SHORT, YOU NEED PYTHON1                |
| a.count(* i 1)                                     | #                | 2                                               |
| a.find(’ e.)                                       | #                | 从左向右查找*e：，3                             |
| a.rfind('need *)                                   | #                | 从右向左查找'neecT, 19                          |
| a.replace(1 you',    ' I *)                        | #                | * Life is short, I need Python1                 |
| tokens = a.split()#                                | [fLife'          | ','is *, ’short,1, ’you’，'need*,    1 Python1] |
| b =    *    1.join(tokens)                         | #                | 用指定分隔符按顺序把字符串列表组合成新字符串    |
| c = a +    1 \n *                                  | #                | 加了换行符，注意+用法是字符串作为序列的用法     |
| c.rstrip ()                                        | #                | 右侧去除换行符                                  |
| [x for x in a]                                     | #                | 遍历每个字符并生成由所有字符按顺序构成的列表    |
| 1 Python * in a                                    | #                | True                                            |

Python 2.6中引入了 format进行字符串格式化，相比在字符串中用％的类似C语言的 方式，更加强大方便。

a = 'I'm like a {} chasing { } . *

\#    按顺序格式化字符串，*I'm like a dog chasing cars. *

a.    format(* dog*, ’cars')

\#在大括号中指定参数所在位置

b = 'I prefer {1}    {0} to {2}    {0}'

b.    format(1 food1, 'Chinese’， ’American’)

\#    >代表右对齐，>前是要填充的字符，依次输出：

\#    000001

\#    000019

\#    000256

for i in [1,    19,    256]:

print('The index is {:0>6d}*.format(i))

\#    <代表左对齐，依次输出：

\#    *---------

for x in    ，****•,    «******* •]:

progress_bar =    *{:-<10}'.format(x)

print(progress_bar)

for x in [0.0001, lei z,    3e-18]:

\#按照小数点后6位的浮点数格式 #按照小数点后1位的科学记数法格式 #系统自动选择最合适的格式 :s old.'

print(1{:.6f}*.format(x)) print(’{:.le}’.format(x)) print (1{:g}'•format(x))

template = ’{name} is {age} yec

c = template. format (name=1 Tom*, age=8) ) # Tom is 8 years old. d = template.format(age=7, name=1 Jerry *) # Jerry is 7 years old.

format在生成字符串和文档的时候非常有用，更多更详细的用法可以参考Python官网 [https://docs.python.Org/2/library/string.html#format-specification-mini-languageo](https://docs.python.org/2/library/string.html%23format-specification-mini-languageo)

5.2.8文件操作和pickle

在Python中，推荐用上下文管理器(with-as)来打开文件，IO资源的管理更加安全， 而且不用老惦记着给文件执行closeG函数。下面还是举例子来说明，例如有个文件 name_age.txt，里面存储着名字和年龄的关系，格式如下：

Tom, 8

Jerry,7 y

Tyke,3

读取文件内容并全部显示：

with open (' name_age. txt * ,    * r') as f:    # 打开文件，读取模式

lines = f. readlines ()    # 一次读取所有行

for line in lines:    #按行格式化并显示信息

name, age = line.rstrip().split(1,’)

print(1{} is { } years old.*.format(name, age))

openO函数的第一个参数是文件名，第二个参数是模式。文件的模式一般有4种，即 读取⑺、写入(w)、追加(a)和读写(r+)。如果希望按照二进制数据读取，则将文件模式和b 一起使用(wb，r+b…)。

再考虑一个场景，要读取文件内容，并把年龄和名字的顺序交换存成新文件

age_name.txt，这时可以同时打开两个文件：

with open(* name_age.txt',    * r *) as fread, open(* age_name.txt',    'w')

as fwrite:

line = fread.readline() while line:

name, age = line.rstrip().split(’，’) fwrite.write(1{},{}\n•.format(age, name)) line = fread.readline()

有的时候进行文件操作时希望把对象进行序列化，那么可以考虑用pickle模块。

import pickle lines 二 [

"I'm like a dog chasing cars.",

"I wouldn * t know what to do if I caught one...",

"I'd just do things."

]

with open (* lines .pkl *,    * wb *)    as    f:    #    序列化并保存成文件

pickle.dump(lines, f)

with open (* lines . pkl * ,    ' rb')    as    f:    #    从文件读取并反序列化

lines_back = pickle.load(f)

print(lines_back)    # 和 lines _■样

注意，序列化的时候就要使用b模式了。Python 2中有个效率更高的pickle叫cPickle, 用法和pickle 一样，在Python 3中就只有一个pickle。

5.2.9异常

相比起其他一些语言，在Python中可以更大胆地使用异常，因为异常在Python中是 常见的存在，比如下面这种简单的遍历。

a =    [* Why *,    1 so *,    * serious ',    *?’]

for x in a:

print(x)

当用for进行遍历时，会对要遍历的对象调用iter()函数。这需要¥对象创建一个迭代 器用来依次返回对象中的内容。为了能成功调用iter()函数，该对象要么需支持迭代协议(定 义_iter_()),要么需支持序列协议(定义_getitem_())。当遍历结束时，_iter_()或者 _getitem_()都需要抛出一个异常。_iter_()会抛出 Stoplteration，而_getitem_()会抛出 IndexError,于是遍历就会停止。

在深度学习中，尤其是数据准备阶段，常常遇到IO操作。这时候遇到异常的可能性 很高，采用异常处理可以保证数据处理的过程不被中断，并对有异常的情况进行记录或其 他动作。

for filepath in filelist:    # filelist 中是文件路径的列表

try:

with open (filepath, * r') as f:

\#执行数据处理的相关工作

print (*{} is processed!*.format(filepath)) except IOError:

print('{} with 工OError!*.format(filepath))

\#异常的相应处理

5.2.10 多进程(multiprocessing)

深度学习中对数据高效处理常常会需要并行，这时多进程就派上了用场。考虑这样一 个场景，在数据准备阶段，有很多文件需要运行一定的预处理，正好有台多核服务器，我 们希望把这些文件分成32份，并行处理：

from multiprocessing import Process#, freeze_support def process_data(filelist):

for filepath in filelist:

print('Processing { }    ...丨.format(filepath))

\#处理数据

if _name_ ==    *_main_’ ：

\#如果是在Windows下，还需要加上f reeze_support ()函数 #freeze_support()

\# full_list包含了要处理的全部文件列表

n_total = len (full_list)    # 一个远大于 32 的数

n_processes =    32

每段子列表的平均长度

length = float(n_total) / float(n_processes)

\#计算下标，尽可能均匀地划分输入文件列表

indices = [int(round(i*length)) for i in range(n_processes+l)]

\#生成每个进程要处理的子文件列表

sublists = [full一list [indices [i]: indices [i+1] ] for i in range (n_jprocesses)]

\#生成进程

processes = [Process(target=process_dataz args=(x,)) for x in sublists]

\#并行处理

for p in processes: p.start()

for p in processes: p. join ()

其中if _name_ = *_main_’用来标明在import时不包含，但是作为文件执行 时运行的语句块/为什么不用多线程呢？简单说就是Python中线程的并发无法有效利用多 核，如果有兴趣的读者可以从下面这个链接看起https://wiki.python.org/moin/ GloballnterpreterLock。

5.2.11 os 模块

深度学习中的数据多是文件，所以数据处理阶段和文件相关的操作非常重要。除了文 件IO, Python中一些操作系统的相关功能也能够非常方便地帮助数据处理。例如有一个文 件夹data，下面有3个子文件夹cat、dog和bat,里面分别是猫、狗和蝙蝠的照片。为了 训练一个三分类模型，先要生成一个文件，里面每一行是文件的路径和对应的标签。定义 cat是0，dog是1，bat是2，则可以通过如下脚本：

import os

\#定义文件夹名称和标签的对应关系

}

with open (1 data. txt *,    * w *) as f:

\#遍历所有文件，root为当前文件夹，dirs是所有子文件夹名，files是所有文件名 for root, dirs, files in os.walk(* data *):

for filename in files:

f ilepath = os . sep. join ( [root, filename]) # 获得文件 完整路径

dir name = root. split (os . sep) [-1] # 获取当前文件夹名称 label = label_map [dirname]    # 得至lj标签

line =    1{},{}\n1.format(filepath, label)

f.write(line)

其中，os.sep是当前操作系统的路径分隔符，在UNIX/Linux中是7, Windows中是’\\'。 有的时候我们已经有了所有的文件，在一个文件夹data下，希望获取所有文件的名称，则 可以用os.listdir()函数。

filenames = os.listdir(* data *)

os也提供了如复制、移动和修改文件名等操作。同时因为大部分深度学习框架最常见 的都是在UNIX/Linux下使用，并且UNIX/Linux的shell已经非常强大(比Windows好用)， 所以只需要用字符串格式化等方式生成shell命令的字符串，然后通过os.systemO函数就能 方便实现很多功能，有时比os以及Python中另一个操作系统相关模块shutil还要方便。

import os, shutil

filepathO =    ' data/bat/IMG_000001. jpg *

filepathl =    * data/bat/IMG一000000 . jpg’

\#修改文件名

os.system('mv {}    {} ' . format(filepathO, filepathl))

\#os.rename(filepathO, filepathl)

\#创建文件夹

dirname =    * data_samples *

os.system(*mkdir -p {}*.format(dirname))

\#if not os.path.exists(dirname):

\#    os.mkdir(dirname)

\#拷贝文件

os.system(* cp {}    {}'.format(filepathl, dirname))

\#shutil.copy(filepathl, dirname)

5.3 Python的科学计算包-NumPy

NumPy (Numerical Python extensions)是一个第三方的Python包，用于科学计算。这 个库的前身是1995年开始开发的一个用于数组运算的库，经过了长时间的发展之后，基 本上成为大部分Python科学计算的基础包，当然也包括所有提供Python接□的深度学习 框架。

NumPy在Linux下的安装已经在5.1.2节中作为例子讲过，Windows下也可以通过pip， 或者 <http://www.scipy.org/scipylib/download.html> 网址下载。

5.3.1 基本类型(array)

array,也就是数组，是NumPy中最基础的数据结构，最关键的属性是维度和元素类 型，在NumPy中，可以非常方便地创建各种不同类型的多维数组，并且执行一些基本操 作。下面来看例子：

b = np.array(a) type(b) b.shape b.argmax() b.max() b.mean()

c =    [[1,    2],    [3,    4]]

d = np.array(c) d.shape

d.size

d.max(axis=0) d.max(axis=l) d.mean(axis=0) d.flatten() np.ravel(c)

h = g. as type (np. float) # 用另一种类型表示

1    = np. arange (10) # 类似 range，array ([0,    1,    2,    3,    4,    5,    6,    7,    8,    9])

| m = np.linspace(0z    6,    5) #p = np.array([[1,    2,    3,    4],[5,    6,    7,    8]] | 等差数列，0到6之间5个取值，array([    0.,    1.5,3.,    4.5,    6.]) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |

)    y

np. save ('p.npy *, p)    # 保存到文件

q = np. load ('p.npy •)    # 从文件读取

注意，在导入NumPy的时候，将叩作为NumPy的别名。这是一种习惯性的用法， 后面的章节中也默认这么使用。作为一种多维数组结构，array的数组相关操作是非常丰 富的：

import numpy as np



10, 11]], ,15], b 19],

\    23]]])

vstack是指沿着纵轴拼接两个array，vertical

hstack是指沿着横轴拼接两个array, horizontal

更广义的拼接用concatenate实现，horizontal后的两句依次等效于vstack和hstack stack不是拼接而是在输入array的基础上增加一个新的维度

| 按指定轴进行转置 |       |        |
| ---------------- | ----- | ------ |
| array([[[    0,[ | 3],6Z | 9]]r   |
| [[               | If    | 4],    |
| [                | 7,    | 10]],  |
| [[               | 2,    | 5],    |
| [                | 8,    | 11]]]) |

[2, 6, 10],

[3,    7, 11]])

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-224.jpg)

a[0].transpose()

或者u=a [ 0 ] . T也是获得转置

逆时针旋转90°，第二个参数是旋转次数 array([ [    3,    2,    1,    0],

[7,    6,    5,    4],

| [11,I V 1             | 10,  | 9Z    |
| --------------------- | ---- | ----- |
| v = np.rot90(u,V V f  | 3)   |       |
| 沿纵轴左右翻转        |      |       |
| array([[    8,    4,  | 0],  |       |
| [                     |      | 1],   |
| [10,                  | 6,   | 2],   |
| [11,曹I 1             | 7,   | 3]])  |
| w = np.fliplr(u)1 1 ! |      |       |
| 沿水平轴上下翻转      |      |       |
| array([[    3,    7,  | 11], |       |
| [2,                   | 6,   | 10],  |
| [1,                   | 5,   | 9],   |
| [o,1 » 1              | 4,   | 8]]： |
| x = np.flipud(u)V V 1 |      |       |
| 按照一维顺序滚动位移  |      |       |
| array([[11,    0,     | 4],  |       |
| [8,                   | 1,   | 5],   |
| [9,                   | 2,   | 6],   |
| [10,                  | 3,   | 7]])  |

[10, 2, 6],



z = np.roll(uz 1, axis=l)

对于一维的array所有Python列表支持的下标相关的方法array也都支持，所以在此没 有特别列出。

既然叫numerical python,基础数学运算也是强大的：

import numpy as np

\#    绝对值，1

a = np.abs(-1)

\#    sin 函数，1.0

b = np.sin(np.pi/2)

\#    tanh 逆函数，0.50000107157840523 c = np.arctanh(0.462118)

\#    e 为g的指数函数，20.085536923187668 d = np. exp (3)

\#    2的3次方，8

\# 标准差，0.96824583655185426

P = np.std([l, 2r 3r 2r 1,    3,    2,    0])

对于array,默认执行对位运算。涉及多个array的对位运算时需要array的维度一致， 如果一个array的维度和另一个array的子维度一致，则在没有对齐的维度上分别执行对位 运算，这种机制叫做广播(broadcasting)，还是看例子理解。

| import numpy as |                                           |
| --------------- | ----------------------------------------- |
| a =])           | np.array([[1,    2,    3],[4,    5,    6] |
| b =             | np.array([[lz 2,    3],[1,    2,    3]    |

])

V V

维度一样的array,对位计算 array([[2, 4,    6],

[5,    7,    9]])

a + b

• I I

array([[0,

],3, O

,3, O [

3]

a - b

V V V

array([[ 1, 4f 9],

[4,    10,    18]])

a * b

曹V V

array([[1,

2

]2 T

Z 4 1 [

V V V

a / b

array([[    1,    4,    9],

| 1 1 V    | [16,    25,         | 36]])     |             |
| -------- | ------------------- | --------- | ----------- |
| aV 1 '   | * ★ 2               |           |             |
| array([[ | lz    4Z            | 27],      |             |
| i i      | i                   | [    4Z   | 25,    216] |
| a        | ** b                |           |             |
| c        | =np.array([         |           |             |
|          | [1,                 | 2,    3], |             |
|          | [4,                 | 5,    6], |             |
|          | [7,                 | 8,    9], |             |
|          | [10,                | 11, 12]   |             |
| ])       |                     |           |             |
| d        | =np.array([2,    2, | 2])       |             |



c * d.

V V t

1和c的每个元素分别进行运算

| array([[    0, | 1,   | 2],  |       |
| -------------- | ---- | ---- | ----- |
| [              | 3,   | 4,   | 5],   |
| [              | 6,   | 7Z   | 8],   |
| [              |      | 10,  | 11]]) |

c -    1

5.3.2线性代数模块(linalg)

在深度学习相关的数据处理和运算中，线性代数模块(linalg)是其中最常用的。结合 NumPy提供的基本函数，可以对向量、矩阵或是多维张量进行一些基本的运算。

\#矩阵和向量之间的乘法

np.dot(b, c)

\#    array([ 4, 10, 16])

\#    array([ 4, 10, 16])

\#求矩阵的迹，15

\#求矩阵的行列式值，0

\#求矩阵的秩，2,不满秩，因为行与行之间等差

np.dot(c, b.T)

np.trace(b)

np.linalg.det(b)

np.linalg.matrix_rank(b)

d = np.array([

[2,    I],

[1, 2]

])

» V I

对正定矩阵求本征值和本征向量

本征值为 u，array ( [    3 .,    1.])

本征向量构成的二维array为V，

array([[    0.70710678,    -0.70710678],

[0.70710678,    0.70710678]])

是沿着45°方向

eig()是一般情况的本征值分解，对于更常见的对称实数矩阵， eigh ()更快且更稳定，不过输出的值的顺序和eig ()是相反的

u, v = np.linalg.eig(d)

\# Cholesky分解并重建 1    = np.linalg.cholesky(d)

array([[    2.,    1.],

[1., 2.]])

np.dot(1, l.T)

e = np.array([

[1, 2],

[3,    4]

])

\#对不镇定矩阵，进行SVD分解并重建 U, s, V = np.linalg.svd(e)

S = np.array([

I V V

np.dot(U, np.dot(S, V))

5.3.3 随机模块(random)

随机模块包含了随机数产生和统计分布相关的基本函数，Python本身也有随机模块

random,不过功能更丰富，下面还是来看例子。    (

import numpy as np

import numpy.random as random

\#设置随机数种子

random.seed(42)

\#产生一个1x3, [0,1)之间的浮点型随机数

\# array([ [    0.37454012,    0.95071431,    0.73199394]])

\#后面的例子就不在注释中给出具体结果了

\#从a中无回放的随机采样7个

random.choice(a,    7, replace=False)

\#对a进行乱序并返回一个新的array b = random.permutation(a)

\#对a进行in-place乱序

random.shuffle(a)

\#生成一个长度为9的随机bytes序列并作为str返回

\#    *\x96\x9d\xdl?\xe6\xl8\xbb\x9a\xec' random.bytes(9)

随机模块可以很方便地做一些快速模拟，以验证一些结论。比如一个非常违反直觉的 概率题例子：一个选手去参加一个TV秀，有三扇门，其中一扇门后有奖品，这扇门只有 主持人知道。选手先随机选一扇门但并不打开，主持人看到后，会打开其余两扇门中没有 奖品的一扇门。然后主持人问选手，是否要改变开始的选择？

这个问题的答案是应该改变一开始的选择。在第一次选择的时候，选错的概率是2/3, 选对的概率是1/3。第一次选择之后，主持人相当于帮忙剔除了一个错误答案，所以如果 选手开始选的是错的，这时候换掉就选对了；而如果开始就选对了，则这时候换掉就错了。 根据以上分析，一开始选错的概率就是换掉之后选对的概率，2/3>1/3,所以应该换。虽然 道理上是这样，但还是有些绕，但用随机模拟就可以轻松得到答案。

import numpy.random as random random.seed(42)

\#做10000次实验 n_tests =    10000

生成g次实验的奖品所g的门的编号

\#    0表示第一扇门，1表示第二扇门，2表示第三扇门

winning—doors = random. randint (0,    3, n__tests)

\#记录如果换门的中奖次数

\#其他门的编号

remaining_choices = [i for i in range (3) if i != first_try]

\#没有奖品的门的编号，这个信息只有主持人知道

wrong—choices = [i for i in range (3) if i != winning_door]

\# 一并始选择的门，主持人没法打开，所以从主持人可以打开的门中剔除 if first_try in wrong—choices:

wrong_choices.remove(first_try)

\#这时wrong_choices变量就是主持人可以打开的门的编号 #注意此时如桌一开始选择正确，则可以打开的门是两扇，主持人随便开一扇门 #如果一开始选到了空门，则主持人只能打开剩下一扇空门

screened_out = random.choice(wrong—choices) remaining_choices.remove(screened_out)

\#所以虽然代码写了好些行，如果策略固定的话 #改变主意的获胜概率就是一开始选错的概率，是2/3 #而坚持选择的获胜概率就是一开始就选对的概率，是1/3

\#现在除了一开始选择的编号，以及主持人帮助剔除的错误编号，只剩下一扇门 #如果要改变主意则这扇门就是最终的选择 changed_mind_try = remaining_choices[0]

\#结果<晓，录下来

change_mind_wins += 1 if changed_mind_try == winning_door else 0 insist_wins +=    1 if first_try == winning_door else 0

\#输出10000 if测试的最终结果，与推导的i果类似

\#    You win 6616 out of 10000 tests if you changed your mind

\#    You win 3384 out of 10000 tests if you insist on the initial choice print(

\* You win {1} out of {0} tests if you changed your mind\n *

1 You win {2} out of {0} tests if you insist on the

initial choice'.format(

n_tests, change一mind_wins, insist_wins )_

)

本例代码以及本章后面的其他例子代码，可以到本书的github仓直接下载，地址为 <https://github.com/frombeijingwithlove/dlcv_for_beginnerso>

5.4 Python 的可视化包-matplotlib

matplotlib是Python中最常用的可视化工具之一，可以非常方便地创建海量类型的2D 图表和一些基本的3D图表。matplotlib最早是为了可视化癫痫病人的脑皮层电图相关的信 号而研发，因为在函数的设计上参考了 MATLAB，所以叫做matplotlib。matplotlib首次发 表于2007年，在开源和社区的推动下，现在在基于Python的各个科杀计算领域都得到了 广泛应用。matplotlib的原作者John D. Hunter博士是一名神经生物学家，2012年不幸因癌 症去世，感谢他创建了这样一个伟大的库。

安装matplotlib的方式和NumPy很像，可以直接通过UNIX/Linux的软件管理工具， 如 Ubuntu 16.04 LTS 下载，输入：

» sudo apt install python-matplotlib

或者通过pip安装：

» pip install matplotlib

Windows下也可以通过pip或是到官网下载http://matplotlib.org/。

matplotlib非常强大，不过在深度学习中常用的其实只有很基础的一些功能，本节主要

介绍2D图表、3D图表和图像显示。

5.4.1 2D 图表

matplotlib中最基础的模块是pyplot。先从最简单的点图和线图开始，比如有一组数据， 以及一个拟合模型，通过下面的代码图来可视化。

import numpy as np import matplotlib as mpl import matplotlib.pyplot as pit #通过rcParams设置全局横纵轴字体大小 mpl.rcParams[* xtick.labelsize']    =    24

mpl.rcParams[* ytick.labelsize *]    =    24

np.random.seed(42)

\# x轴的采样点

x = np.linspace(0,    5,    100)

\#通过下面曲线加上噪声生成数据，所以拟合模型就用y了

y = 2*np.sin(x)    +    0.3*x**2

y_data = y + np.random.normal(scale=O.3,    size=100)

\#    figure函数指定图表名称

pit.figure('data')

\#    •. •标明画散点图，每个散点的形状是个圆

pit.plot (x, y_data, *.')

\#画模型的图，plot函数默认画连线图

pit.figure(1model1)

pit.plot(x, y)

\#两个图画一起

pit.figure('data & model'〉

\#通过"V指定线的颜色，lw指定线的宽度

\#第三个参数除了颜色也可以指定线形，比如4--•表示红色虚线

\#    更多属性可以参考官网 <http://matplotlib.org/api/pyplot_api.html>

pit .plot (x, y, ’V,    lw=3)

\#    scatter可以更容易地生成散点图

pit.scatter (x, y_data)

\#将当前figure的图保存到文件result .png

pit.savefig('result.png1)

\#    一定要加上下面这句才能让画好的图显示在屏幕上

pit.show()

matplotlib和pyplot的惯用别名分别是mpl和pit,上面代码生成的图像如图5-1所示。

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-226.jpg)

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-227.jpg)

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-228.jpg)

图表例子

基本的画图方法就是这么简单，读者如果想了解更多pyplot的属性和方法来画出风格 多样的图像，可以参考官网 <http://matplotlib.org/api/pyplot_api.html> 或 <http://matplotlib.org/> users/customizing.html。

点和线图表只是最基本的用法，有的时候获取了分组数据要进行对比，则柱状或饼状

类型的图更合适。

import numpy as np

import matplotlib as mpl

import matplotlib.pyplot as pit

"'dog':    (48,    '#7199cf')z

'cat*:    (45,    ,#4fc4aa,),

\* cheetah *:    (120,    '#ela7a2 *)

}

\#整体图的标题

fig = pit.figure('Bar chart & Pie chart1)

\#在整张图上加入一个子图，121的意思是在一个1行2列的子图中的第一张 ax = fig.add_subplot(121)

ax.set_title('Running speed - bar chart *)

\#生成_x轴每个元素的位置 xticks = np.arange(3)

\#定义柱状图每个柱的宽度

bar_width =    0.5    /

\#动物名称

| animals = | speed— | —map.keys ()                  |
| --------- | ------ | ----------------------------- |
| #奔跑速度 |        |                               |
| speeds =  | [x[0]  | for x in speed_map.values()]  |
| #对应颜色 |        |                               |
| colors =  | [x[l]  | for x in speed一map.values()] |

\#画柱状图，横轴是动物标签的位置，纵轴是速度，定义柱的宽度，同时设置柱的边缘为透明 bars = ax.bar(xticks, speeds, width=bar_width, edgecolor= * none')

\#设置y轴的标题

ax.set_ylabel(* Speed(km/h) *)

\# x轴莓个标签的具体位置，设置为每个柱的中央

ax.set_xticks(xticks+bar_width/2)

\#设置每个标签的名字

ax.set_xticklabels(animals)

\#设置孓轴的范围

ax.set_xlim([bar_width/2-0.5, 3-bar_width/2])

\#设置；轴的范围

ax.set_ylim([0,    125])

\#给每+ bar分配指定的颜色

for bar, color in zip(bars, colors): bar.set_color(color)

\#在122位置加又新的图

ax = fig.add_subplot(122)

ax.set_title('Running speed - pie chart'〉

\#生成]1时包含名称和速度的标签

labels =    [1 {}\n{} km/h，•format(a, s) for a, s in zip(animals,

speeds)]

\#画饼状图，并指定标签和对应颜色

ax.pie(speeds, labels=labels, colors=colors)

\#设置横纵轴比例固定

pit.axis(* equal1)

pit. show ()

在这段代码中又出现了一个用ax命名的对象。在matplotlib中，画图时有两个常用概 念，一个是平时画图弹出的一个窗口，叫Figure。Figure相当于一个大的画布，在每个Figure 中，又可以存在多个子图，这种子图叫axes。顾名思义，有了横纵轴就是一幅简单的图表。 在上面代码中，先把Figure定义成了一个一行两列的大画布，然后通过fig.add_subplot函 数加入两个新的子图。subplot的定义格式很有趣，数字的前两位分别定义行数和列数，最 后一位定义新加入子图的所处顺序，当然想写明确些也没问题，用逗号分开即可。上面代 码生成的图像如图5-2所示。

《M/E>op<u(uds

Running speed - bar chart

806040



Running speed - pie chart cheetah



图5-2 2D柱状图和饼状图例子

5.4.2 3D 图表

matplotlib中也能支持一些基础的3D图表，比如曲面图、散点图和柱状图。这些3D 图表需要使用mpl_t00lkits模块，先来看一个简单的曲面图的例子。

import matplotlib.pyplot as pit import numpy as np # 3D图标必需的模块，projects 3d•的定义 from mpl_toolkits.mplot3d import Axes3D

np.random.seed(42) n_grids = 51 c = n_grids /    2

\# x-y平面的格点数 #中心位置 #低频成分的个数

nf =    2

\#生成格点

x = np.linspace (0, 1, n_grids)

y = np.linspace(0, 1, n_grids)

\#    x和y是长度为n_grids的array

\#    meshgrid会把x和y组合成n_grids*n_grids的array, X和Y对应位置就是所有格点的 坐标

X, Y = np.meshgrid(x, y) #生成一个0值的傅里叶谱

spectrum = np.zeros((n_grids, n_grids), dtype=np.complex)

\#生成一段噪音，长度是(2*nf+l) **2/2

noise = [np. complex (x,    y) for x, y in np. random.uniform (-1 z 1,

((2*nf+l)**2/2,    2))]

\#傅里叶频谱的每一项和其共轭关于中心对称

noisy block = np.concatenate((noise, [0j], np.conjugate(noise[::-!])))

\#将生成的频谱作为低频成分

spectrum[c-nf:c+nf+l, c-nf:c+nf+l] = noisy_block.reshape((2*nf+l,    2*nf+l))

\#进行反傅里叶变换

Z = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum)))

\#创建图表

fig = pit.figure(1 3D surface & wire *)

\#第一个子图，surface图

ax = fig.add_subplot(1,    2,    1, proj ection= * 3d')

\#    alpha 定义透明度，cmap 是 color map

\#    rstride和cstride是两个方向上的采样，越小越精细，lw是线宽

ax.plot_surface(X, Y, Z, alpha=0.7, cmap= * j et *, rstride=l, cstride=l, lw=0)

\#第二个子图，网线图

ax = fig.add_subplot(1,    2,    2, projection= * 3d')

ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3, lw=0.5) pit.show()

这个例子中先生成一个所有值均为0的复数array作为初始频谱，然后把频谱中央部 分用随机生成，但同时共轭关于中心对称的子矩阵进行填充。这相当于只有低频成分的一 个随机频谱。最后进行反傅里叶变换就得到一个随机波动的曲面，如图5-3所示。



0.004

0.002

jo.ooo

-0.002

■0.004

0.8

1.0 0 0



0.004

0.002

0.000

-0.002

•0.004

1.0 0 0

图5-3表面图和网线图例子

3D的散点图也是常常用来查看空间样本分布的一种手段，并且画起来比表面图和网线

图更加简单，来看例子：

import matplotlib.pyplot as pit import numpy as np

from mpl_toolkits.mplot3d import Axes3D np.random.seed(42)

\#采样个数500 n_samples =    500

dim =    3

\#先生成一组三维正态分布数据，数据方向完全随机

samples = np.random.multivariate_normal(

np.zeros(dim), np.eye(dim), n_samples

)

\#通过把每个样本到原点距离和均匀分布吻合得到球体内均匀分布的样本

for i in range(samples.shape[0]):

r = np.power(np.random.random(),    1.0/3.0)

samples[i]    *= r / np.linalg.norm(samples[i])

upper_samples.append((xz y, z))

else:

lower_samples.append((x, y, z)) fig = pit.figure(1 3D scatter plot *) ax = fig.add_subplot(111, projection= * 3d *) uppers = np.array(upper_samples) lowers = np.array(lower_samples)

\#用不同颜色不同形状的图标表呆平面上下的样本 #判别平面上半部分为红色圆点，下半部分为绿色三角

marker=1o') marker=1A *)

ax.scatter(uppers[:, 0], uppers[:, 1], uppers[:, 2], c=’r', ax.scatter(lowers[:, 0], lowers[:, 1], lowers[:, 2], c=1g* z pit.show()

例子中为了方便直接先采样了- •堆三维的正态分布样本，保证方向上的均匀性。然后 归一化，让每个样本到原点的距离为1，相当于得到了一个均匀分布在球面上的样本。再 接着把每个样本都乘上一个均匀分布随机数的开3次方，这样就得到了在球体内均匀分 布的样本，最后根据判别平面3x+2j^-l=0对平面两侧样本用不同的形状和颜色画出，如 图5-4所示。

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-233.jpg)

图5-4 3D散点图例子

5.4.3图像显示

matplotlib也支持图像的存取和显示，并且和OpenCV—类的接口比起来，对于一般的 二维矩阵的可视化要方便很多，下面来看例子。

import matplotlib.pyplot as pit

\#读取一张小白狗的照片并显示

pit.figure(*A Little White Dog *)

little_dog_img = pit.imread('little_white_dog.jpg1) pit.imshow(1i 111e_dog_img)

\#    Z是前面生成的随机_图案厂imgO就是Z, imgl是Z做了个简单的变换 imgO = Z

imgl =    3*Z    +    4

\#    cmap指定为*gray1用来显示灰度图

fig = pit.figure('Auto Normalized Visualization*)

axO = fig.add_subplot(121)

axO.imshow(imgO, cmap= * gray1)

axl = fig.add_subplot(122)

axl.imshow(imgl, cmap='gray *)

pit.show()

代码中第一个例子是读取一个本地图片并显示，第二个例子中直接把前面反傅里叶变 换生成的矩阵作为图像拿过来，原图和经过乘以3再加4变换的图直接绘制了两个形状一 样但是值的范围不一样的图案。显示的时候imshow会自动进行归一化，把最亮的值显示 为纯白，最暗的值显示为纯黑。这是一种非常方便的设定，尤其是查看深度学习中某个卷 积层的响应图时。得到图像如图5-5所示。

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-234.jpg)



0    10    20    30    40    50



0    10    20    30    40    50

图5-5图像和二维array的可视化

本节只讲到了最基本和常用的图表及最简单的例子，更多有趣精美的例子可以在

 matplotlib 的官网找到，地址为 [http://matplotlib.org/gallery.html](http://matplotlib.org/gallery.html%e3%80%82)[。](http://matplotlib.org/gallery.html%e3%80%82)
