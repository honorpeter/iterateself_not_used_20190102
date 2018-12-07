---
title: 21 使用list和tuple
toc: true
date: 2018-12-07
---

# 使用 list 和 tuple

### list

Python内置的一种数据类型是列表：list。list是一种有序的集合，可以随时添加和删除其中的元素。

比如，列出班里所有同学的名字，就可以用一个list表示：

```py
>>> classmates = ['Michael', 'Bob', 'Tracy']
>>> classmates
['Michael', 'Bob', 'Tracy']
```

变量`classmates`就是一个list。用`len()`函数可以获得list元素的个数：

```py
>>> len(classmates)
3
```

用索引来访问list中每一个位置的元素，记得索引是从`0`开始的：

```py
>>> classmates[0]
'Michael'
>>> classmates[1]
'Bob'
>>> classmates[2]
'Tracy'
>>> classmates[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```

当索引超出了范围时，Python会报一个`IndexError`错误，所以，要确保索引不要越界，记得最后一个元素的索引是`len(classmates) - 1`。

如果要取最后一个元素，除了计算索引位置外，还可以用`-1`做索引，直接获取最后一个元素：<span style="color:red;">嗯，是的，这个比较常用。</span>

```py
>>> classmates[-1]
'Tracy'
```

以此类推，可以获取倒数第2个、倒数第3个：

```py
>>> classmates[-2]
'Bob'
>>> classmates[-3]
'Michael'
>>> classmates[-4]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```

当然，倒数第4个就越界了。

list是一个可变的有序表，所以，可以往list中追加元素到末尾：

```py
>>> classmates.append('Adam')
>>> classmates
['Michael', 'Bob', 'Tracy', 'Adam']
```

也可以把元素插入到指定的位置，比如索引号为`1`的位置：<span style="color:red;">这个好像不是这么常用，这样 insert 是会移动后面的所有的数吗？会不会很慢？还是说这个 list 实际上是以链表的形式保存的？直接插入就行的？想知道效率怎么样。</span>

<span style="color:red;">而且，这个 1 是当前这个元素插入后的 index。</span>

```py
>>> classmates.insert(1, 'Jack')
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']
```

要删除 list 末尾的元素，用 `pop()` 方法： <span style="color:red;">嗯，这个是删除最后一个元素吗？嗯，如果是这样的话，感觉list 是不是就可以代替 stack 了？</span>

```py
>>> classmates.pop()
'Adam'
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy']
```

要删除指定位置的元素，用 `pop(i)` 方法，其中 `i` 是索引位置：<span style="color:red;">嗯，这样还是真的很好用的。</span>

```py
>>> classmates.pop(1)
'Jack'
>>> classmates
['Michael', 'Bob', 'Tracy']
```

要把某个元素替换成别的元素，可以直接赋值给对应的索引位置：

```py
>>> classmates[1] = 'Sarah'
>>> classmates
['Michael', 'Sarah', 'Tracy']
```

list 里面的元素的数据类型也可以不同，比如：<span style="color:red;">说实话，这个list 里面元素的数据类型不同的感觉用起来很变扭。。而且，这个也没有办法批量处理，感觉还不如用 类来写比较清晰。。不知道为什么会有这样的机制，一般在什么场景下使用呢？</span>

```py
>>> L = ['Apple', 123, True]
```

list元素也可以是另一个list，比如：

```py
>>> s = ['python', 'java', ['asp', 'php'], 'scheme']
>>> len(s)
4
```

要注意`s`只有4个元素，其中`s[2]`又是一个list，如果拆开写就更容易理解了：

```py
>>> p = ['asp', 'php']
>>> s = ['python', 'java', p, 'scheme']
```

要拿到`'php'`可以写`p[1]`或者`s[2][1]`，因此`s`可以看成是一个二维数组，类似的还有三维、四维……数组，不过很少用到。

如果一个list中一个元素也没有，就是一个空的list，它的长度为0：

```py
>>> L = []
>>> len(L)
0
```

### tuple

另一种有序列表叫元组：tuple。tuple和list非常类似，但是tuple一旦初始化就不能修改，比如同样是列出同学的名字：

```py
>>> classmates = ('Michael', 'Bob', 'Tracy')
```

现在，classmates这个tuple不能变了，它也没有append()，insert()这样的方法。其他获取元素的方法和list是一样的，你可以正常地使用`classmates[0]`，`classmates[-1]`，但不能赋值成另外的元素。

不可变的 tuple 有什么意义？因为 tuple 不可变，所以代码更安全。如果可能，能用 tuple 代替 list 就尽量用 tuple。<span style="color:red;">嗯，这个之前实际上没有特别注意过，不过的确，是要注意的，如果一组数据是固定不变的，还是最好创建为 tuple 。</span>

tuple 的陷阱：当你定义一个 tuple 时，在定义的时候，tuple 的元素就必须被确定下来，比如：

```py
>>> t = (1, 2)
>>> t
(1, 2)
```

如果要定义一个空的tuple，可以写成`()`：

```py
>>> t = ()
>>> t
()
```

但是，要定义一个只有1个元素的tuple，如果你这么定义：

```py
>>> t = (1)
>>> t
1
```

定义的不是tuple，是`1`这个数！这是因为括号 `()` 既可以表示tuple，又可以表示数学公式中的小括号，这就产生了歧义，因此，Python规定，这种情况下，按小括号进行计算，计算结果自然是 `1`。<span style="color:red;">嗯，说实话，之前没有明确这一点，也没有写过这样的，因为感觉上使用 tuple 的时候一般都是多个数据的时候。</span>

所以，只有1个元素的tuple定义时必须加一个逗号`,`，来消除歧义：<span style="color:red;">看到这个地方，我突然想到了，为什么之前有的函数传的参数是一个 tuple ，而且，这个tuple 还提别的在最后加了一个逗号，原来是这样，之前看的时候，感觉就是随手加了一个逗号，现在看，的确是有必要加的。</span>

```py
>>> t = (1,)
>>> t
(1,)
```

Python在显示只有 1 个元素的 tuple 时，也会加一个逗号`,`，以免你误解成数学计算意义上的括号。

最后来看一个 “可变的” tuple：

```
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])
```

这个tuple定义的时候有3个元素，分别是`'a'`，`'b'`和一个list。不是说 tuple 一旦定义后就不可变了吗？怎么后来又变了？

别急，我们先看看定义的时候 tuple 包含的3个元素：

![mark](http://images.iterate.site/blog/image/20181206/b7dKEBhP6AET.png?imageslim)

当我们把list的元素`'A'`和`'B'`修改为`'X'`和`'Y'`后，tuple变为：

![mark](http://images.iterate.site/blog/image/20181206/0g3Hjt7M7F2f.png?imageslim)

表面上看，tuple的元素确实变了，但其实变的不是tuple的元素，而是list的元素。tuple 一开始指向的 list 并没有改成别的 list，所以，tuple所谓的“不变”是说，tuple的每个元素，指向永远不变。即指向`'a'`，就不能改成指向`'b'`，指向一个list，就不能改成指向其他对象，但指向的这个list本身是可变的！<span style="color:red;">嗯，是要注意的，tuple 所谓的不变是指：tuple 的每个元素，指向永远不变。</span>

理解了“指向不变”后，要创建一个内容也不变的 tuple 怎么做？那就必须保证 tuple 的每一个元素本身也不能变。<span style="color:red;">是的，这种细节还是要明确的。</span>

### 小结

list 和 tuple 是 Python 内置的有序集合，一个可变，一个不可变。根据需要来选择使用它们。




# 相关资料

- [使用list和tuple](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014316724772904521142196b74a3f8abf93d8e97c6ee6000)
