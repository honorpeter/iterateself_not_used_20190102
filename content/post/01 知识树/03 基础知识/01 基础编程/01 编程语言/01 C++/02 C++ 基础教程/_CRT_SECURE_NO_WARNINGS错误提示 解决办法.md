# `_CRT_SECURE_NO_WARNINGS` 错误提示，解决办法




```
#include <stdio.h>

int main(void)
{
​	char str[256] = {0};
​	scanf("%255s",str);
​	printf("Hello World!\n");
​	printf("%s\n",str);
​	return 0;
}
```



一个简单的 C 的 Hello World，如果用高版本的 VS 来编译，会提示

```
'scanf': This function or variable may be unsafe. Consider using scanf_s instead. To disable deprecation, use _CRT_SECURE_NO_WARNINGS. See online help for details.
```


这个是高版的VS默认不让使用 scanf，fopen 等函数，说是 scanf，fopen 等函数不安全，而代替其函数的是scanf_s，fopen_s等函数，后边有个 `_s` 的形式


想要使用，可以在源文件开头加个:

```
#define _CRT_SECURE_NO_WARNINGS
```

或

右击工程 - 属性 - 配置属性 - C/C++  - 命令行
命令行增加:`_CRT_SECURE_NO_WARNINGS`


效果都一样，就是预编时处理一下，加个宏而已，让其忽略安全检测


```
#define _CRT_SECURE_NO_WARNINGS
//添加到头行，添加到stdio.h等头文件后还是会出警告的
#include <stdio.h>

int main(void)
{
​	char str[256] = {0};
​	scanf("%255s",str);
​	printf("Hello World!\n");
​	printf("%s\n",str);
​	return 0;
}
```



# 相关资料

- [_CRT_SECURE_NO_WARNINGS错误提示，解决办法](https://blog.csdn.net/duke56/article/details/52403458)
