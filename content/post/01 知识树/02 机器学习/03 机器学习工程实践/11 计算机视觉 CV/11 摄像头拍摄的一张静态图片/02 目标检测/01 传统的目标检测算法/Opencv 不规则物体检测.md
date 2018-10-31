---
title: Opencv 不规则物体检测
toc: true
date: 2018-10-31
---

# 需要补充的

- 对于这种不规则物体的检测也是要知道的，这个没准就用上了。

# Opencv--不规则物体检测


如图所示，一副不规则物体离散分布的灰度图，要想检测并标记。需要以下步骤：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/HFG5BD7GC6.png?imageslim)


1、 二值化，这个过程很简单

```
def thresh_img(img):
​    if img.ndim==3:
​        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
​    img=cv2.medianBlur(img,3)
​    _,thresh=cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
​    return thresh
```


2、 利用opencv 中connectedComponents这个函数返回两个值，一个是标记总个数，从0开始，一个是标记的举证。其中，物体的个数==max(标记矩阵最大值)

```
def label_image(thresh):
​    h,w=thresh.shape[:2]
​    _,markers=cv2.connectedComponents(thresh)#返回两个值，一个是label总个数，一个是label后的矩阵吧
​    objects_total_number=np.max(markers)
​    print("总共有%g物体"%objects_total_number)
​    center_pts=[]# 存储每个label的坐标的重心作为对象重心
​    for i in range(1,objects_total_number):
​        temp=[[j,i] for i,j in zip(*np.where(markers==i))]
​        mean_pts=np.mean(temp,0)
​        center_pts.append([np.float32(mean_pts[0]),np.float32(mean_pts[1])])
​    return markers,center_pts
```


3、 将灰度图转为色彩图，首先将标记矩阵值扩展到0-179之间作为HIS中H，S,I 分别等于与其同样大小的白色矩阵。再将HIS图像转为BGR即可

```
def gray_to_bgr_image(markers,center_pts):
​    h,w=markers.shape[:2]
​    hue_markers = np.uint8(179*np.float32(markers)/np.max(markers))
​    blank_channel = 255*np.ones((h, w), dtype=np.uint8)
​    marker_img = cv2.merge([hue_markers, blank_channel-50, blank_channel])
​    marker_img = cv2.cvtColor(marker_img, cv2.COLOR_HSV2BGR)
​    i=1
​    for pt in center_pts:
​        cv2.putText(marker_img,"%s"%str(i),(pt[0],pt[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,[0,0,0],2)
​        i+=1
​    cv2.putText(marker_img,"objects number is:%g"%i,(20,10),cv2.FONT_HERSHEY_SIMPLEX,0.5,[0,0,0],2)
​    cv2.imshow('Colored markers', marker_img)
​    cv2.waitKey(0)
```

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/igbiK0LcEH.png?imageslim)


完整代码如下：

```python
# -*- coding: utf-8 -*-
#discrete irregular objects detect and asssign color
import cv2
import numpy as np
from numba import autojit
@autojit
def thresh_img(img):
​    if img.ndim==3:
​        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
​    img=cv2.medianBlur(img,3)
​    _,thresh=cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
​    return thresh
def label_image(thresh):
​    h,w=thresh.shape[:2]
​    _,markers=cv2.connectedComponents(thresh)#返回两个值，一个是label总个数，一个是label后的矩阵吧
​    objects_total_number=np.max(markers)
​    print("总共有%g物体"%objects_total_number)
​    center_pts=[]
​    for i in range(1,objects_total_number):
​        temp=[[j,i] for i,j in zip(*np.where(markers==i))]
​        mean_pts=np.mean(temp,0)
​        center_pts.append([np.float32(mean_pts[0]),np.float32(mean_pts[1])])
​    return markers,center_pts
def gray_to_bgr_image(markers,center_pts):
​    h,w=markers.shape[:2]
​    hue_markers = np.uint8(179*np.float32(markers)/np.max(markers))
​    blank_channel = 255*np.ones((h, w), dtype=np.uint8)
​    marker_img = cv2.merge([hue_markers, blank_channel-50, blank_channel])
​    marker_img = cv2.cvtColor(marker_img, cv2.COLOR_HSV2BGR)
​    i=1
​    for pt in center_pts:
​        cv2.putText(marker_img,"%s"%str(i),(pt[0],pt[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,[0,0,0],2)
​        i+=1
​    cv2.putText(marker_img,"objects number is:%g"%i,(20,10),cv2.FONT_HERSHEY_SIMPLEX,0.5,[0,0,0],2)
​    cv2.imshow('Colored markers', marker_img)
​    cv2.waitKey(0)
if __name__=="__main__":
​    im=cv2.imread(r'C:\Users\Y\Desktop\w.png')
​    thresh=thresh_img(im)
​    markers,center_pts=label_image(thresh)
    gray_to_bgr_image(markers,center_pts)


```







# 相关资料

- [Opencv 不规则物体检测](https://blog.csdn.net/qq_15642411/article/details/80462581?utm_source=blogkpcl1)
