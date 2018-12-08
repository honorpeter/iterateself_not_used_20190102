---
title: char 与 string 的转换
toc: true
date: 2018-12-08
---



# c++ 中 char 与 string 之间的相互转换问题

这个还是要好好掌握下的，不能每次遇到都去查一下，这个经常用到。



```cpp
const char c = 'a';
//1.使用 string 的构造函数
string s(1,c);
//2.声明string 后将char push_back
string s1;
s1.push_back(c);
//3.使用stringstream
stringstream ss;
ss << c;
string str2 = ss.str();

//注意 使用to_string 方法会转化为char对应的ascii码
//原因是 to_string 没有接受char型参数的函数原型，有一个参数类型
//为int 的函数原型，所以传入char型字符 实际是先将char 转化
//为int 型的ascii 码，然后再转变为string
//以下输出结果为 97
cout << to_string(c) << endl;
```

# 相关资料

- [c++ 中 char 与 string 之间的相互转换问题](https://www.cnblogs.com/devilmaycry812839668/p/6353807.html)

- [c++ 将一个char 转化为string](https://blog.csdn.net/carbon06/article/details/79353821)
