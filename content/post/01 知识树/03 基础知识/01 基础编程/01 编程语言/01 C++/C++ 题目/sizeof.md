---
title: sizeof
toc: true
date: 2018-08-28
---





#### [Q 11](http://blog.csdn.net/candyliuxj/article/details/6307814) :

题目：
某32位系统下, C++程序，请计算sizeof 的值：
```
char str[] = "http://www.xxxxx.com";
char *p = str;
int n = 10;
sizeof(str) = (1);
sizeof(p) = (2;
sizeof(n) = (3);
void Foo(char str[100]){
    sizeof(str) = (4);
}
void *p = malloc(100);
sizeof(p) = (5);
```

答案:
21
4
4
4
4

解答:
考察sizeof返回值。
1. 具体类型，返回该类型所占的空间大小。
2. 对象，返回对象的实际占用空间大小。
3. 数组，返回编译时分配的数组空间大小（数组名 ≠ 指针）。作为参数时数组退化为指针。<span style="color:red;">嗯，由于字符串有 /0 ，因此是 21 个。</span>
4. 指针，返回存储该指针所用的空间大小。
5. 函数，返回函数的返回类型所占的空间大小。函数的返回类型不能是void。<span style="color:red;">第5个返回的是什么？为什么是4？</span>
6. 上题中(2)(4)(5)均为指针。
