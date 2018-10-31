---
title: OpenCV在图像中寻找轮廓和计算图像中物体的凸包
toc: true
date: 2018-10-31
---
# 需要补充的

- 这个效果有这么好吗？嗯，背景非常混乱的时候不是很容易找出来吧？要自己试下。


# OpenCV在图像中寻找轮廓和计算图像中物体的凸包



一、轮廓的寻找


用于寻找的函数：

```
void findContours( InputOutputArray image, OutputArrayOfArrays contours,
​                              OutputArray hierarchy, int mode,
​                              int method, Point offset = Point());
```

第一个参数为输入图像，要求为8位1通道。
第二个为用于输出的点的集合，应该为Point的向量。
第三个参数为可选输出向量，包含了图像的拓扑信息。

然后是用于绘图的函数：

```
void drawContours( InputOutputArray image, InputArrayOfArrays contours,
​                              int contourIdx, const Scalar& color,
​                              int thickness = 1, int lineType = LINE_8,
​                              InputArray hierarchy = noArray(),
​                              int maxLevel = INT_MAX, Point offset = Point() );
```

具体用法和findContours对照即可，其中contourIdx参数为contours的索引，所以在循环中使用比较好。

具体代码：

```
int main()
{
​    RNG rng(12345);
​    Mat a = imread("1RT05508-0.jpg");
​    imshow("原图", a);
​    cvtColor(a, a, CV_RGB2GRAY);

    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    Canny(a, a, 100, 300);
    findContours(a, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);
    Mat drawing = Mat::zeros(a.size(), CV_8UC3);
    Mat b = Mat::zeros(a.size(), CV_8UC3);
    for (int i = 0; i< contours.size(); i++)
    {
        Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
        drawContours(b, contours, i, color, 2, 8, hierarchy, 0);
    }
    imshow("效果图", b);
    cvWaitKey(10000);
}
```


二、凸包的计算
所使用的函数：


```
void convexHull( InputArray points, OutputArray hull,
​                              bool clockwise = false, bool returnPoints = true );
```



参数就是之前计算出的轮廓和用于输出的集合
具体代码：



```
int main()
{
​    RNG rng(12345);
​    Mat a = imread("9660416_102608612175_2.jpg");
​    imshow("原图", a);
​    cvtColor(a, a, CV_RGB2GRAY);

    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;

    Canny(a, a, 100, 300);
    findContours(a, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);

    vector<vector<Point> >hull(contours.size());
    for (int i = 0; i < contours.size(); i++)     //计算凸包
    {
        convexHull(Mat(contours[i]), hull[i]);
    }


    Mat b = Mat::zeros(a.size(), CV_8UC3);
    for (int i = 0; i< contours.size(); i++)
    {
        Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
        drawContours(b, contours, i, color, 2, 8, hierarchy, 0);
        drawContours(b, hull, i, color, 1, 8, vector<Vec4i>(), 0);    //绘制凸包
    }
    imshow("效果图", b);
    cvWaitKey(10000);
}
```


![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/hi6bGJIfJe.png?imageslim)





# 需要补充的

- [OpenCV在图像中寻找轮廓和计算图像中物体的凸包](https://blog.csdn.net/qq_22033759/article/details/48290213?utm_source=blogkpcl13)
