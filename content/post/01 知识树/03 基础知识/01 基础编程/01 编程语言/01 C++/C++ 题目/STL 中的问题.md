---
title: STL 中的问题
toc: true
date: 2018-08-28
---




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
