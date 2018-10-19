# 需要补充的

- 感觉还有很多需要补充的。

# os.path

python 中的 os.path 是比较常用的模块，把其中的几个函数介绍如下：

## dirname()   用于去掉文件名，返回目录所在的路径

如：

```python
import os
os.path.dirname('d:\\library\\book.txt')
```

```
'd:\\library'
```

## basename()   用于去掉目录的路径，只返回文件名

如：

```python
import os
os.path.basename('d:\\library\\book.txt')
```

```
'book.txt'
```

## join()   用于将分离的各部分组合成一个路径名

<span style="color:red;">一直对这个心里有些疑虑，到底中间的 `\` 是会自动去掉的吗？</span>

如：

```python
import os
os.path.join('d:\\library','book.txt')
```

```
'd:\\library\\book.txt'
```

## split()  用于返回目录路径和文件名的元组

如：

```python
import os
os.path.split('d:\\library\\book.txt')
```

```
('d:\\library', 'book.txt')
```

## splitdrive()    用于返回盘符和路径字符元组

```python
import os
os.path.splitdrive('d:\\library\\book.txt')
```

```
('d:', '\\library\\book.txt')
```

<span style="color:red;">嗯，不错，没想到还有这种方法。好像第一次看到</span>

## splitext()    用于返回文件名和扩展名元组

如：

```python
os.path.splitext('d:\\library\\book.txt')
os.path.splitext('book.txt')
```

```
('d:\\library\\book', '.txt')
('book', '.txt')
```

<span style="color:red;">哇塞，竟然有这种函数，之前我都是使用的 basename 或者 [:-4] 来截取文件名。</span>



# 相关资料

- [python中的os.path模块用法（一）](https://blog.csdn.net/ziyuzhao123/article/details/8811496)
