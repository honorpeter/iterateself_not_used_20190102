# 需要补充的

- 资料还没总结进来。


今天看到一个，从文本中读入一行到 line 里面，line 内容是一个字符串，`'Horse', (255, 255, 0)`，然后他写了：

```
label, color = eval(line)
```

我在 console 试了下：

```python
line="'Horse', (255, 255, 0)"
label,color=eval(line)
print(label,color)
```

输出：

```
Horse (255, 255, 0)
```

说实话，以前没想到还可以这么做，相当于不用解析了，但是感觉这样eval 有风险，需要确认下。





# 相关资料

- [详解python eval函数的妙用](https://www.jb51.net/article/128410.htm) 要总结进来
