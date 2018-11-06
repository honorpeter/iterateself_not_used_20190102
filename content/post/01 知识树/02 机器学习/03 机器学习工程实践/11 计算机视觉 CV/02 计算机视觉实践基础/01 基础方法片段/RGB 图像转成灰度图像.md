# 需要补充的

- 这个地方还是要再消化下的，之前是想找 PIL 的 RGB 转 gray 的，应该就是：`img = Image.open('image.png').convert('L')`，如果是 LA 就是有 alpha 通道的，即 RGBA 。



# RGB 图像转化成灰度图像

I'm trying to use `matplotlib` to read in an RGB image and convert it to grayscale.

In matlab I use this:

```py
img = rgb2gray(imread('image.png'));
```

In the [matplotlib tutorial](http://matplotlib.sourceforge.net/users/image_tutorial.html) they don't cover it. They just read in the image

```py
import matplotlib.image as mpimg
img = mpimg.imread('image.png')
```

and then they slice the array, but that's not the same thing as converting RGB to grayscale from what I understand.

```py
lum_img = img[:,:,0]
```

I find it hard to believe that numpy or matplotlib doesn't have a built-in function to convert from rgb to gray. Isn't this a common operation in image processing?

I wrote a very simple function that works with the image imported using `imread` in 5 minutes. It's horribly inefficient, but that's why I was hoping for a professional implementation built-in.

Sebastian has improved my function, but I'm still hoping to find the built-in one.

matlab's (NTSC/PAL) implementation:

```py
import numpy as np

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray
```




How about doing it with [Pillow](https://pillow.readthedocs.io/en/latest/):

```py
from PIL import Image
img = Image.open('image.png').convert('LA')
img.save('greyscale.png')
```

------

Using matplotlib and [the formula](http://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale)

```py
Y' = 0.299 R + 0.587 G + 0.114 B
```

you could do:

```py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

img = mpimg.imread('image.png')     
gray = rgb2gray(img)    
plt.imshow(gray, cmap = plt.get_cmap('gray'))
plt.show()
```




# 相关资料

- [How can I convert an RGB image into grayscale in Python?](https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python)
