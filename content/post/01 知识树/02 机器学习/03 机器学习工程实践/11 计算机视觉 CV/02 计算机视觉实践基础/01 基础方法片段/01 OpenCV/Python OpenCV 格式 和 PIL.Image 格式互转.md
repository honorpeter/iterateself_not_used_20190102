
# OpenCV 和 PIL.Image 互转

这个还是会经常遇到的，之前我用到这个是在图像数据增强的时候，要加噪声，有的是在 Image 格式上加噪声，有的是在 OpenCV 的 image 格式i上加噪声，因此还是要互相转化下的.

```
import cv2
from PIL import Image
import numpy

def convert_cv2_to_pil(cv2_img):
    img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    return img


def convert_pil_to_cv2(pil_img):
    img = cv2.cvtColor(numpy.asarray(pil_img), cv2.COLOR_RGB2BGR)
    return img
```


- [Python OpenCV格式和PIL.Image格式 互转](https://blog.csdn.net/qq_19707521/article/details/78367617)
