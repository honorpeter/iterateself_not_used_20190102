# 需要补充的

- 感觉这个讲的不是很细致，而且缺乏一些应用场景的例子的讲解，还是要多补充一下的。

# dict

Python内置了字典：dict的支持，dict 全称 dictionary，在其他语言中也称为 map，使用键-值（key-value）存储，具有极快的查找速度。

举个例子，假设要根据同学的名字查找对应的成绩，如果用list实现，需要两个list：

```py
names = ['Michael', 'Bob', 'Tracy']
scores = [95, 75, 85]
```

给定一个名字，要查找对应的成绩，就先要在names中找到对应的位置，再从scores取出对应的成绩，list越长，耗时越长。

如果用dict实现，只需要一个“名字”-“成绩”的对照表，直接根据名字查找成绩，无论这个表有多大，查找速度都不会变慢。用 Python 写一个 dict 如下：<span style="color:red;">这个无论这个表有多大，查找速度都不会变慢，还是要理解下的，这个特性可以用在什么地方呢？而且，这个背后是怎么实现的？</span>

```py
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
```

为什么dict查找速度这么快？因为dict的实现原理和查字典是一样的。假设字典包含了1万个汉字，我们要查某一个字，一个办法是把字典从第一页往后翻，直到找到我们想要的字为止，这种方法就是在list中查找元素的方法，list越大，查找越慢。

第二种方法是先在字典的索引表里（比如部首表）查这个字对应的页码，然后直接翻到该页，找到这个字。无论找哪个字，这种查找速度都非常快，不会随着字典大小的增加而变慢。

dict 就是第二种实现方式，给定一个名字，比如 `'Michael'`，dict在内部就可以直接计算出`Michael`对应的存放成绩的“页码”，也就是`95`这个数字存放的内存地址，直接取出来，所以速度非常快。

你可以猜到，这种 key-value 存储方式，在放进去的时候，必须根据key算出value的存放位置，这样，取的时候才能根据key直接拿到value。

把数据放入dict的方法，除了初始化时指定外，还可以通过key放入：

```py
>>> d['Adam'] = 67
>>> d['Adam']
67
```

由于一个key只能对应一个value，所以，多次对一个key放入value，后面的值会把前面的值冲掉：

```py
>>> d['Jack'] = 90
>>> d['Jack']
90
>>> d['Jack'] = 88
>>> d['Jack']
88
```

如果key不存在，dict就会报错：

```
>>> d['Thomas']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Thomas'
```

要避免key不存在的错误，有两种办法，一是通过`in`判断key是否存在：<span style="color:red;">这个还是要注意使用的，如果不使用，还是不够严密的。</span>

```py
>>> 'Thomas' in d
False
```

二是通过dict提供的`get()`方法，如果key不存在，可以返回`None`，或者自己指定的value：<span style="color:red;">嗯，这个更好，但是之前在 C++ 的时候已经习惯使用 `d["Tomas"]` 这样的方式了。。嗯，还是要用 get 的方式，这样更加稳妥点，同时也能从字面上知道出现问题的时候返回的是什么。</span>

```py
>>> d.get('Thomas')
>>> d.get('Thomas', -1)
-1
```

注意：返回`None`的时候Python的交互环境不显示结果。<span style="color:red;">一直想知道，对于这种 None 的结果要怎么进行处理？python 好像特别喜欢返回 None 的结果。</span>

要删除一个key，用 `pop(key)` 方法，对应的 value 也会从 dict 中删除：<span style="color:red;">哇塞，之前好像没有见到过这种，嗯，这种一般的应用的地方是什么？嗯，下次还是要想一下这个使用的时候是啥样的。</span>

```py
>>> d.pop('Bob')
75
>>> d
{'Michael': 95, 'Tracy': 85}
```

请务必注意，dict内部存放的顺序和key放入的顺序是没有关系的。<span style="color:red;">嗯，这个之前在别的地方看到过，嗯，这里又强调了下。</span>

和list比较，dict有以下几个特点：

1. 查找和插入的速度极快，不会随着key的增加而变慢；
2. 需要占用大量的内存，内存浪费多。 <span style="color:red;">嗯，这个倒是哦</span>

而list相反：

1. 查找和插入的时间随着元素的增加而增加；
2. 占用空间小，浪费内存很少。

所以，dict 是用空间来换取时间的一种方法。

dict 可以用在需要高速查找的很多地方，在 Python 代码中几乎无处不在，正确使用dict非常重要，需要牢记的第一条就是dict的key必须是**不可变对象**。<span style="color:red;">非常想知道高速查找的那些场景中使用了 dict ，到底是怎么使用的？还是要看下这方面的例子，对于 dict 还是要有更深的额理解。tuple 可以作为 key 吗？不知道有没有 tuple 作为 key 的例子。</span>

这是因为 dict 根据 key 来计算value的存储位置，如果每次计算相同的 key 得出的结果不同，那 dict 内部就完全混乱了。这个通过 key 计算位置的算法称为哈希算法（Hash）。<span style="color:red;">嗯，对于 hash 还是要在理解下的，之前有些理解，但是还是想更深刻理解下的。以及现在的 hash 算法有没有什么发展，应用场景有没有什么新的场景。</span>

要保证hash的正确性，作为key的对象就不能变。在Python中，字符串、整数等都是不可变的，因此，可以放心地作为key。而list是可变的，就不能作为key：<span style="color:red;">tuple 可以作为 key 吗？</span>

```py
>>> key = [1, 2, 3]
>>> d[key] = 'a list'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

下面看下这个例子：

```py
b={1:'a',2:'dd'}
print(type(b))
print(b)
b={(1,2,3):'a',2:'bb'}
print(b)
b={(1,[1,2],3):'a',2:'bb'}
print(b)
```

输出：

```
<class 'dict'>
{1: 'a', 2: 'dd'}
{(1, 2, 3): 'a', 2: 'bb'}
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "D:\11.program_files\PyCharm 2018.3.1\helpers\pydev\_pydev_bundle\pydev_umd.py", line 198, in runfile
    pydev_imports.execfile(filename, global_vars, local_vars)  # execute the script
  File "D:\11.program_files\PyCharm 2018.3.1\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "D:/03.software/learn_opencv/l.py", line 7, in <module>
    b={(1,[1,2],3):'a',2:'bb'}
TypeError: unhashable type: 'list'
```

<span style="color:red;">嗯，可见，纯粹的 tuple 是可以作为 dict 的 key 的，但是含有 list 的 tuple 是不能作为 key 的。</span>

### set

set 和 dict 类似，也是一组 key 的集合，但不存储value。由于 key 不能重复，所以，在set中，没有重复的 key。

要创建一个 set，需要提供一个 list 作为输入集合：

```py
>>> s = set([1, 2, 3])
>>> s
{1, 2, 3}
```

注意，传入的参数`[1, 2, 3]`是一个list，而显示的`{1, 2, 3}`只是告诉你这个set内部有1，2，3这3个元素，显示的顺序也不表示set是有序的。。<span style="color:red;">嗯。</span>

看下下面这个例子：

```py
a = set([(1, 2, 3), (1, 2, 3), 3])
print(a)
a = set([(1, [1,2], 3), (1, 2, 3), 3])
print(a)
```

输出：

```
{3, (1, 2, 3)}
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "D:\11.program_files\PyCharm 2018.3.1\helpers\pydev\_pydev_bundle\pydev_umd.py", line 198, in runfile
    pydev_imports.execfile(filename, global_vars, local_vars)  # execute the script
  File "D:\11.program_files\PyCharm 2018.3.1\helpers\pydev\_pydev_imps\_pydev_execfile.py", line 18, in execfile
    exec(compile(contents+"\n", file, 'exec'), glob, loc)
  File "D:/03.software/learn_opencv/l.py", line 3, in <module>
    a = set([(1, [1,2], 3), (1, 2, 3), 3])
TypeError: unhashable type: 'list'
```

<span style="color:red;">嗯，可见，纯粹的 tuple 是可以作为 set 的 key 的，但是里面含有 list 的 tuple 是无法作为 key 被 hash 的。</span>

重复元素在set中自动被过滤：

```
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}
```

通过`add(key)`方法可以添加元素到set中，可以重复添加，但不会有效果：

```
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}
```

通过`remove(key)`方法可以删除元素：

```
>>> s.remove(4)
>>> s
{1, 2, 3}
```

set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：

```py
>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}
```

<span style="color:red;">对于集合，之前只是在文字识别的时候，想在识别错误的时候尽可能匹配到对应的字符串的时候用到过，感觉平时的时候很少会使用到这个。嗯，用来去重好像也不错。</span>

set和dict的唯一区别仅在于没有存储对应的value，但是，set的原理和dict一样，所以，同样不可以放入可变对象，因为无法判断两个可变对象是否相等，也就无法保证 set 内部“不会有重复元素”。试试把list放入set，看看是否会报错。<span style="color:red;">嗯，也不能放可变对象。</span>

### 再议不可变对象

上面我们讲了，str是不变对象，而list是可变对象。<span style="color:red;">嗯，关于这一点再强调下，str 是不可变的对象，平时我们用的时候，感觉它好像也是可以修改的，但是实际上是用了一个新的 str 代替了旧的 str </span>

对于可变对象，比如 list，对 list 进行操作，list 内部的内容是会变化的，比如：

```py
>>> a = ['c', 'b', 'a']
>>> a.sort()
>>> a
['a', 'b', 'c']
```

<span style="color:red;">好像很少用到 a.sort() 来对列表进行排序。</span>

而对于不可变对象，比如str，对str进行操作呢：

```py
>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'
```

虽然字符串有个`replace()`方法，也确实变出了`'Abc'`，但变量`a`最后仍是`'abc'`，应该怎么理解呢？<span style="color:red;">嗯，这个地方要注意的。</span>

我们先把代码改成下面这样：

```py
a = 'abc'
b = a.replace('a', 'A')
print(b)
print(a)
```

输出：

```
Abc
abc
```

要始终牢记的是，`a`是变量，而`'abc'`才是字符串对象！有些时候，我们经常说，对象`a`的内容是`'abc'`，但其实是指，`a`本身是一个变量，它指向的对象的内容才是`'abc'`：<span style="color:red;">是的，这一点</span>

```ascii
┌───┐                  ┌───────┐
│ a │─────────────────>│ 'abc' │
└───┘                  └───────┘
```

当我们调用`a.replace('a', 'A')`时，实际上调用方法`replace`是作用在字符串对象`'abc'`上的，而这个方法虽然名字叫`replace`，但却没有改变字符串`'abc'`的内容。相反，`replace`方法创建了一个新字符串`'Abc'`并返回，如果我们用变量`b`指向该新字符串，就容易理解了，变量`a`仍指向原有的字符串`'abc'`，但变量`b`却指向新字符串`'Abc'`了：<span style="color:red;">`replace`方法创建了一个新字符串`'Abc'`并返回，嗯。</span>

```ascii
┌───┐                  ┌───────┐
│ a │─────────────────>│ 'abc' │
└───┘                  └───────┘
┌───┐                  ┌───────┐
│ b │─────────────────>│ 'Abc' │
└───┘                  └───────┘
```

所以，对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。<span style="color:red;">是的，这种机制保证了不变对象本身永远是不变的。关于这一点的理解可以在有些时候明白一些困惑。</span>

### 小结

使用 key-value 存储结构的 dict 在 Python 中非常有用，选择不可变对象作为key很重要，最常用的key是字符串。




# 相关资料

- [使用dict和set](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143167793538255adf33371774853a0ef943280573f4d000)
