---
title: Python list 删除元素
toc: true
date: 2018-10-17
---

# Python list 删除元素


### 1. 使用del删除指定元素

```
li = [1, 2, 3, 4]
del li[3]
print(li)
# Output [1, 2, 3]
```

### 2. 使用list方法pop删除元素

```
li = [1, 2, 3, 4]
li.pop(2)
print(li)
# Output [1, 2, 4]
```

注：指定pop参数，将会删除该位置的元素；无参数时默认删除最后一个元素

### 3. 使用切片删除元素

```
li = [1, 2, 3, 4]
li = li[:2] + li[3:]
print(li)
# Output [1, 2, 4]
```

### 4. 使用list方法remove删除指定值的元素

```
li = [1, 2, 3, 4]
li.remove(3)
print(li)
# Output [1, 2, 4]
```

注：remove方法删除指定值的元素，与其他方法不同。


# 相关资料

- [Python List 删除元素](https://blog.csdn.net/u012956540/article/details/50816334)
- [python 3.x中列表中元素删除del、remove、pop的用法及区别](https://blog.csdn.net/deqiangxiaozi/article/details/75808863)
