---
title: char
toc: true
date: 2018-08-28
---



#### Q 22 :

题目：

```
char fun(char x, char y){
    if(x)
        return(y);
}
int main(){
    int a = '0', b = '1', c = '2';
    printf("%c\n", fun(fun(a, b), fun(b, c)));
}
```

答案:
2

解答:
1. 均为字符，非布尔值的0，所以每次返回后者。<span style="color:red;">'0' 也是不等于布尔值的 0 的吗？</span>


#### Q 17 :

题目：

若有以下定义和语句：

```
char s1[] = "12345", *s2 = "1234";
printf("%d\n", strlen(strcpy(s1, s2)));
```

则输出结果是：

答案:
4

解答:
考察strcpy和strlen。
1. 首先strlen得到的是'\0'之前的字符长度。<span style="color:red;">这个不知道</span>
2. strcpy将s2指向的字符串'1234\0'全部拷贝到s1指向位置并覆盖其'12345'部分。<span style="color:red;">s1 里面本身有 \0 吗？strlen 对一个字符数组进行操作的时候，也是只计算 \0 前面的字符长度吗？</span>
��度吗？</span>
