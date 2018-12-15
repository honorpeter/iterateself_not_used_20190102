# 需要补充的

- 这个例子是在灰度图上的，彩色的要改一下
- 关于 shape 的用法还是要在 python 里详细总结
- 关于这些噪音背后的原理要总结下
- 为什么感觉高斯噪音的图片这么的奇怪？为什么有值得地方感觉没有很多的变化？还是说实际上是有变化的，但是变化不明显？<span style="color:red;">哇塞，当我把高斯噪音的图片放大后与 gray 图片详细对比了下，才知道，这个高斯噪音就是我之前做的项目的时候分频器处理过的视频画面的噪声！！简直了，我之前还以为这个是一种变异的 0~250 的椒盐噪音，所以撒了很多变种的椒盐噪音在画面上然后生成数据。。好吧，原来是高斯噪音！！厉害了。</span>

# 高斯噪声和椒盐噪声的python程序实现

首首先我们先来看下python中shape()函数的用法


```py
import numpy as np

a = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])
print(a.shape[0])
print(a.shape[1])
```

输出：

```
4
3
```

可以看到 `shape[0]` 表示的为行数，`shape[1]` 表示的为列数


进入正题：

我们先定义高斯噪声函数：`gaussian_noise(img,means,sigma)`

通过使用函数 `random.gauss(means,sigma)` 生成均值为`means`，标准差为 `sigma` 的高斯白噪声。<span style="color:red;">这个random.gauss 之前没有使用过，也不知道 random 里面还可以这样生成，嗯，对于 random 还是要了解更多。</span>

高斯噪声的代码如下：

```py
import numpy as np
import random


def gaussian_noise(img, means, sigma):
    img_noise = img
    h = img_noise.shape[0]
    w = img_noise.shape[1]
    for i in range(h):
        for j in range(w):
            img_noise[i, j] = img_noise[i, j] + random.gauss(means, sigma)
            if img_noise[i, j] < 0:
                img_noise[i, j] = 0
            elif img_noise[i, j] > 255:
                img_noise[i, j] = 255
    return img_noise

```


椒盐噪声的函数定义如下：<span style="color:red;">一直想知道什么样的噪声叫椒盐噪声？为什么会有椒盐噪声？什么是有效的去处椒盐噪声的方法？而且，在视频传输的过程中海油什么别的噪声吗？分别要怎么处理？分别要怎么模拟生成？嗯，这些其实都是可能会用到的。</span>


```py
import numpy as np
import random


def pepper_and_salt(img, percetage):
    img_noise = img.copy()
    noise_num = int(percetage * img.shape[0] * img.shape[1])
    for i in range(noise_num):
        r = random.randint(0, img.shape[0] - 1)
        c = random.randint(0, img.shape[1] - 1)
        if random.random() <= 0.5:
            img_noise[r, c] = 0
        else:
            img_noise[r, c] = 255
    return img_noise
```



例子如下：

```py
import numpy as np
import random
import cv2


def gaussian_noise(img, means, sigma):
    img_noise = img.copy()
    h = img_noise.shape[0]
    w = img_noise.shape[1]
    for i in range(h):
        for j in range(w):
            img_noise[i, j] = img_noise[i, j] + random.gauss(means, sigma)
            if img_noise[i, j] < 0:
                img_noise[i, j] = 0
            elif img_noise[i, j] > 255:
                img_noise[i, j] = 255
    return img_noise

def pepper_and_salt(img, percetage):
    img_noise = img.copy()
    noise_num = int(percetage * img.shape[0] * img.shape[1])
    for i in range(noise_num):
        r = random.randint(0, img.shape[0] - 1)
        c = random.randint(0, img.shape[1] - 1)
        if random.random() <= 0.5:
            img_noise[r, c] = 0
        else:
            img_noise[r, c] = 255
    return img_noise



if __name__=="__main__":
    img_gray=cv2.imread("1.jpg", 0)
    img_gaussian=gaussian_noise(img_gray, 2, 4)
    img_pepper_and_salt=pepper_and_salt(img_gray, 0.2)
    cv2.imwrite('1_gray.jpg',img_gray)
    cv2.imwrite('1_gaussian.jpg',img_gaussian)
    cv2.imwrite('1_pepper_and_salt.jpg',img_pepper_and_salt)
```


结果如下：

1.jpg：

![mark](http://images.iterate.site/blog/image/20181215/w6nxktnasA4u.jpg?imageslim)

1_gray.jpg：

![mark](http://images.iterate.site/blog/image/20181215/rrpcbooPehRr.jpg?imageslim)

1_gaussian.jpg：

![mark](http://images.iterate.site/blog/image/20181215/ieaRThsJqKNX.jpg?imageslim)

1_pepper_and_salt.jpg：

![mark](http://images.iterate.site/blog/image/20181215/mnKBDrD3EWIA.jpg?imageslim)



# 相关资料

- [高斯噪声和椒盐噪声的python程序实现](https://blog.csdn.net/kaikai______/article/details/53535909)
