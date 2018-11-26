---
title: 合并一张 alpha 图像到另一张图像中
toc: true
date: 2018-11-26
---
# How to merge a transparent png image with another image using PIL


```py
import Image

background = Image.open("test1.png")
foreground = Image.open("test2.png")

background.paste(foreground, (0, 0), foreground)
background.show()
```

First parameter to `.paste()` is the image to paste. Second are coordinates, and the secret sauce is the third parameter. It indicates a **mask** that will be used to paste the image. If you pass a image with transparency, then the alpha channel is used as mask.


# 相关资料

- [How to merge a transparent png image with another image using PIL](https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil)
