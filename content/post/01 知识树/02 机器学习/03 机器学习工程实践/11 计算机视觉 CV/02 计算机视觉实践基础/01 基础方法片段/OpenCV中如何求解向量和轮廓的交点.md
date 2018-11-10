---
title: OpenCV中如何求解向量和轮廓的交点
toc: true
date: 2018-11-10
---
# 需要补充的

- 还没有仔细理解


# OpenCV中如何求解向量和轮廓的交点


在“学习OpenCV3"的QQ群众，网友且行且珍惜针对前期博客（[https://www.cnblogs.com/jsxyhelu/p/9345590.html](http://link.zhihu.com/?target=https%3A//www.cnblogs.com/jsxyhelu/p/9345590.html)）中的内容提出了以下问题：



![img](https://pic3.zhimg.com/80/v2-a3c10c144918baec42528f031eb91ac6_hd.jpg)



*比如这张图，利用 PCA 求出了特征向量之后，我想要求解与轮廓的交点，不知道有没有简单的方法@禾老师*



非常好的问题！在寻找到轮廓的”主方向“后，往往下一个动作就是寻找向量和轮廓的交点，因为往往这才是我们更关心的地方。为了解决这个问题，我认为的思路应该是这样的：

1、首先要界定范围。对于交点来说，肯定是在这个轮廓的“最小外接矩形”中的，所以先求出外接矩形作为限定；

2、向量只是一个方向，要将其变成一条直线（如果在“最小外接矩形”中就是线段），推荐使用LineIterator来表示直线；

3、最后，判断这条线段上的点是否在轮廓上，可以使用pointpolytest函数。



结合代码具体讲解。为了凸显本文知识重点，本文采用以下一幅图像来说明算法



![img](https://pic3.zhimg.com/80/v2-2ae212875edb7e39a90f9775dff7b3a2_hd.jpg)



最后得到的结果是这样的，其中黄点为主方向向量和外界矩形交点，红点为和轮廓交点。



![img](https://pic4.zhimg.com/80/v2-943846728c0883b0c6ac6c10fab36aeb_hd.jpg)





全部代码为：

```text
/************************************************************************/
// 求解向量和轮廓的交点
// by jsxyhelu(jsxyhelu.cnblogs.com)
// 2018/10/05
/************************************************************************/
#include "stdafx.h"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/photo.hpp"
using namespace std;
using namespace cv;
//寻找最大外接轮廓
vector<Point> FindBigestContour(Mat src){
 int max_area_contour_idx = 0;
 double max_area = -1;
    vector<vector<Point> >contours;
    findContours(src,contours,RETR_LIST,CHAIN_APPROX_SIMPLE);
    //handle case if no contours are detected
    CV_Assert(0 != contours.size());
 for (uint i=0;i<contours.size();i++){
 double temp_area = contourArea(contours[i]);
 if (max_area < temp_area ){
            max_area_contour_idx = i;
            max_area = temp_area;
        }
    }
 return contours[max_area_contour_idx];
}
//程序主要部分
int main( int argc, char** argv )
{
    //读入图像，转换为灰度
    Mat src = imread("E:/sandbox/cloud.png");
    Mat src_gray;
    cvtColor(src, src_gray, COLOR_BGR2GRAY);
    //阈值处理
    Mat threshold_output;
    cv::threshold(src_gray,threshold_output,150,255,THRESH_OTSU|THRESH_BINARY_INV);
    //轮廓分析
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    vector<Point> biggestContour =  FindBigestContour(threshold_output);//寻找最大轮廓
    Rect boundRect    = boundingRect( Mat(biggestContour) ); //获得轮廓最小外接矩形
    cv::rectangle(src,boundRect,Scalar(0,0,255));
    //pca分析,求出斜率和经过的一点
    Mat data_pts = Mat(biggestContour.size(), 2, CV_64FC1);//Construct a buffer used by the pca analysis
 for (int i = 0; i < data_pts.rows; ++i)
    {
        data_pts.at<double>(i, 0) = biggestContour[i].x;
        data_pts.at<double>(i, 1) = biggestContour[i].y;
    }
    PCA pca_analysis(data_pts, Mat(), CV_PCA_DATA_AS_ROW);//执行PCA运算
    Point pos = Point2f(pca_analysis.mean.at<double>(0, 0),
        pca_analysis.mean.at<double>(0, 1));    //主方向直线经过的一点
    vector<Point2d> eigen_vecs(2);    //保存PCA分析结果，其中0组为主方向，1组为垂直方向
    vector<double> eigen_val(2);
 for (int i = 0; i < 2; ++i)
    {
        eigen_vecs[i] = Point2d(pca_analysis.eigenvectors.at<double>(i, 0),
            pca_analysis.eigenvectors.at<double>(i, 1));
        eigen_val[i] = pca_analysis.eigenvalues.at<double>(i,0);
    }
    line(src, pos - 0.02 * Point(eigen_vecs[0].x * eigen_val[0],eigen_vecs[0].y * eigen_val[0]),
        pos+0.02 * Point(eigen_vecs[0].x * eigen_val[0],eigen_vecs[0].y * eigen_val[0]) , Scalar(255, 255, 0));//绘制概略主方向
    //求出主方向直线和外接矩形的交点，
 float k = eigen_vecs[0].y/eigen_vecs[0].x; //斜率
    Point2f pt1 = Point2f(boundRect.x,k*(boundRect.x - pos.x)+pos.y);
    Point2f pt2 = Point2f((boundRect.x+boundRect.width),k*((boundRect.x+boundRect.width)-pos.x)+pos.y);
    circle(src,pt1,5,Scalar(0,255,255),-1);
    circle(src,pt2,5,Scalar(0,255,255),-1);
    //遍历两个交点之间的线段，得出和轮廓的交点
    LineIterator it(src, pt1, pt2, 8);
 for(int i = 0; i < it.count; i++, ++it)
    {
         Point pt(it.pos());//获得线段上的点
 if (abs(pointPolygonTest(biggestContour,pt,true)) < 1)
                circle(src,pt,5,Scalar(0,0,255),-1);
    }
    waitKey();
 return 0;
}
```

知识重点：



1、FindBigestContour为寻找轮廓中最大轮廓的函数，目前这个函数还没有merge到OpenCV中，下一步有这个计划，注意这个函数的命名规则是按照OpenCV的方法定

义的；



2、我们采用Rect boundRect = boundingRect( Mat(biggestContour) );

来获得轮廓的最小外接矩形。为什么要首先获得这个外接矩形了，因为我们这里来所有要求的点肯定都在这个矩形中，我们做这一步就能够降低算法的计算复杂程度；



3、PCA分析的具体原来和细节，请查看

《如何获得物体的主要方向？》

[https://www.cnblogs.com/jsxyhelu/p/7690699.html](http://link.zhihu.com/?target=https%3A//www.cnblogs.com/jsxyhelu/p/7690699.html)



我们这里使用，主要是获得两个数据，一个是该轮廓的重心，这个点是我们最后要求的那条直线肯定经过的；二个是求出直线的斜率。那么对于一条直线，已经知道斜率和

经过的一点，就已经能够被定义出来；



4、最后在求该直线和轮廓的交点的时候，采用了LineIterator 和pointPolygonTest，前者是OpenCV中专门用来遍历直线的；后者是专门用来计算点和轮廓的关系的，应该说这里的应用还是非常高效的。






# 相关资料

- [OpenCV中如何求解向量和轮廓的交点](https://zhuanlan.zhihu.com/p/46055147)
