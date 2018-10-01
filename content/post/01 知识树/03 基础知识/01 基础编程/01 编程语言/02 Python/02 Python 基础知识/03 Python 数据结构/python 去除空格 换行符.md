# 需要补充的

- 这个后续合并到 string 的各种用法中去。

# python 去除空格 换行符




```python
s = "as, asdas \r\nasda"  
print s.split();  
#   result: ['as,', 'asdas', 'asda']  

print "".join(s.split());  
#    result: as,asdasasda  

l = "".join(s.split()).split(',');  
print l;  
#   result: ['as', 'asdasasda']  
```



join:在序列中添加元素
split: 将字符串分解成序列
两者为互逆方法




# 相关资料

- [python 去除空格/换行符](https://blog.csdn.net/Tcorpion/article/details/75452443)
