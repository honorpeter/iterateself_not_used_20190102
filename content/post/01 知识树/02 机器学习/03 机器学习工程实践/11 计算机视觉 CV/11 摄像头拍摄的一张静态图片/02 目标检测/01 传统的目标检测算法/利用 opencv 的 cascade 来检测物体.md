---
title: 利用 opencv 的 cascade 来检测物体
toc: true
date: 2018-10-31
---
# 需要补充的

- 这种方法现在真的还在使用吗？效果真的可以吗？不过还是可以借鉴下的。




# opencv 实时识别指定物体



opencv 实时识别指定物体


opencv人脸识别大家应该都听说过，本篇目的是利用 opencv 从视频帧中识别指定的物体，并框出来

- 包括训练自己的分类器，
- 使用训练好的分类器进行识别。


这里以识别舌头为例。



## 三. 训练自己的分类器

1. 注意点：训练集分为正样本，负样本，样本全部为灰度图片，正样本图片尺寸需要固定，一般40*40左右即可，大了电脑跑不动，负样本尺寸不固定，负样本数量要比正样本多才行，少了有问题。





2. 正样本制作，使用美图秀秀将舌头的图片全部裁剪出来（尺寸一致为：40*40的），保存到一个文件夹pos中，当然可以先用大尺寸正方形框进行裁剪，然后再用图片缩小工具进行制定尺寸缩小。最后再用美图秀秀批量灰度化。


处理后得到如下所示图片：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/a321Ikc9eh.png?imageslim)

3. 负样本制作：如上操作类似，不过这里不要求尺寸一样，但是负样本图片中一定不要包含待识别的区域（如这里的：舌头）
  如下所示：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/J7I65kBbaa.png?imageslim)



4. 生成样本资源记录文件：

a. 正样本资源记录文件

新建 pos 文件夹，将正样本的灰度图拷贝进去

生成后删除最后一行的带有(pos.txt)的内容，让正样本资源记录文件内容如下类似所示：

(1 0 0 40 40)分别指代： 数量  左上方的坐标位置(x,y)  右下方的坐标位置(x,y)
处理好后，将pos.txt 移动到上一级文件夹


b. 负样本资源记录文件

新建neg文件夹，将负样本的灰度图拷贝进去

生成后删除最后一行的带有(neg.txt)的内容，让负样本资源记录文件内容如下类似所示：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/5he2hmE6eK.png?imageslim)

处理好后，将negtxt 移动到上一级文件夹

得到如图所示文件夹结构：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/d8acJJ7df8.png?imageslim)

5. 使用opencv提供的opencv_createsamples.exe程序生成样本vec文件，新建批处理文件：createsamples.bat
  内容如下：

```
opencv_createsamples.exe -vec pos.vec -info pos.txt -num 25 -w 40 -h 40
pause
```

说明：25是正样本图片的数量   40 40 是正样本图片的宽高

这些参数的详细解释：http://www.opencv.org.cn/opencvdoc/2.3.2/html/doc/user_guide/ug_traincascade.html

运行后会生成 pos.vec文件


6. 使用opencv提供的opencv_traincascade.exe程序训练分类器，新建xml文件夹，再新建批处理文件：LBP_train.bat
  内容如下：

```
opencv_traincascade.exe -data xml -vec pos.vec -bg neg.txt -numPos 25 -numNeg 666 -numStages 10 -w 40 -h 40 -minHitRate 0.999 -maxFalseAlarmRate 0.2 -weightTrimRate 0.95 -featureType LBP
pause
```


说明： 25是正样本图片的数量   666是负样本图片的数量   numNeg是层级数  40 40是训练样本的宽高 .....
具体参数解释请查看文档：http://www.opencv.org.cn/opencvdoc/2.3.2/html/doc/user_guide/ug_traincascade.html

运行后会在xml文件夹生成如下文件：

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/KI3k903J8h.png?imageslim)

其中cascade.xml是我们需要使用的分类器


四 . 测试训练好的分类器

```python
import cv2

# 加载opencv自带的人脸分类器
# faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
# faceCascade.load('E:/python/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_alt2.xml')

faceCascade = cv2.CascadeClassifier("cascade.xml")
faceCascade.load('E:/tools/python/eclipse/work/pythonTest/demo/0202/img/train/tongue/xml/cascade.xml')

cap = cv2.VideoCapture(0)
flag = 0
timeF = 10
while True:
​    flag+=1
​    ret, frame = cap.read()
​    img = frame.copy()
​    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
​    rect = faceCascade.detectMultiScale(
​        gray,
​        scaleFactor=1.15,
​        minNeighbors=3,
​        minSize=(3,3),
​        flags = cv2.IMREAD_GRAYSCALE
​    )
​    for (x, y, w, h) in rect:
​        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
​        #识别到物体后进行裁剪保存
​        #jiequ = img[x:(x+w), y:(y+h)]
​        #cv2.imwrite('E://tools//python//eclipse//work//pythonTest//demo//0202//img//save//'+str(flag) + '.jpg',jiequ) #save as jpg

    #读取到保存图片
#     if(flag%timeF==0):
#         cv2.imwrite('E://tools//python//eclipse//work//pythonTest//demo//0202//img//save//'+str(flag) + '.jpg',frame) #save as jpg


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```

效果图如下所示：


![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/FH4A14clij.png?imageslim)


所有需要用到的文件下载地址：  http://download.csdn.net/download/qq_27063119/10238488  
（需要5积分，没有的至我邮箱 nuohy@qq.com）




# 相关资料

- [opencv实时识别指定物体](https://blog.csdn.net/qq_27063119/article/details/79247266?utm_source=blogxgwz4)
