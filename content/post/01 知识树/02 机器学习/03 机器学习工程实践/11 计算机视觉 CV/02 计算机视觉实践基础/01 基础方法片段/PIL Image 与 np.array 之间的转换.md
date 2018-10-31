---
title: PIL Image 与 np.array 之间的转换
toc: true
date: 2018-10-31
---


# PIL Image 与 np.array 之间的转换

Open I as an array:

```
I = numpy.asarray(PIL.Image.open('test.jpg'))
```


Do some stuff to I, then, convert it back to an image:

```
im = PIL.Image.fromarray(numpy.uint8(I))
```



# 相关资料

- [How to convert a PIL Image into a numpy array?](https://stackoverflow.com/questions/384759/how-to-convert-a-pil-image-into-a-numpy-array)
