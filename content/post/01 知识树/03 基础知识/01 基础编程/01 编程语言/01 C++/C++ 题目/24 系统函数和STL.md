---
title: 24 系统函数和STL
toc: true
date: 2018-08-28
---


#### Q 78 :

题目：
STL中的一级容器有：

答案：
vector, deque, list

解答：
考察STL容器概念。
1. STL中一级容器是容器元素本身是基本类型，非组合类型。



## 迭代器



#### [Q 4](http://blog.csdn.net/dgyanyong/article/details/21268469) :

题目：
下列代码的输出为：
```
#include "iostream"
#include "vector"
using namespace std;
int main(void)
{
    vector<int>array;
    array.push_back(100);
    array.push_back(300);
    array.push_back(300);
    array.push_back(500);
    vector<int>::iterator itor;
    for(itor = array.begin(); itor != array.end(); itor++){
        if(*itor == 300){
            itor = array.erase(itor);
        }
    }
    for(itor = array.begin(); itor != array.end(); itor++){
        cout << *itor << " ";
    }
    return 0;
}
```

答案:
100
300
500

解答:
考察STL中erase和迭代器问题。
1. erase返回值是一个迭代器，指向删除元素下一个元素。
2. 删除第一个300时返回指向下一个300的迭代器，在循环体又被再加了一次，跳过了第二个300。



#### Q 59 :

题目：
std::vector::iterator重载了下面哪些运算符：

答案：
++
==
*

解答：
考察迭代器基本概念。
1. ++和--用于迭代器以后移动。
2. ==用于判断迭代器是否相等。
3. *用于对迭代器指向的变量的引用。



#### Q 58 :

题目：
以下函数中，和其他函数不属于一类的是：

答案：
pwrite

解答：
考察系统调用和库函数。
1. 常见文件系统的系统函数：
    fcntl 文件控制
    open 打开文件
    creat 创建新文件
    close 关闭文件描述字
    read 读文件
    write 写文件
    read 从文件读入数据到缓冲数组中
    write 将缓冲数组里的数据写入文件
    pread 对文件随机读
    pwrite 对文件随机写
