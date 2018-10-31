---
title: OpenCV_contri 找出任意物体可能在的位置 Selective search 物体检测
toc: true
date: 2018-10-31
---
# 需要补充的

-



# OpenCV_contri 找出任意物体可能在的位置 Selective search 物体检测

惯例先放效果（搜索图片里所有物体可能在的位置，之后对每个 bouding box 内的图像进行相似度匹配即可

//这个比金字塔采样+滑窗高明的地方在于可以少匹配很多次……

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/Gh2g7IB9jF.png?imageslim)

首先，Selective Search的原理可参考博客：  [地址](http://blog.csdn.net/mao_kun/article/details/50576003)



当然需要先配置下 opencv_contribute 的环境，然后就是简单粗暴的代码了…


```
#include "opencv2/ximgproc/segmentation.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include <iostream>
#include <ctime>

using namespace cv;
using namespace cv::ximgproc::segmentation;

int main() {
​
	// 多线程加速
	setUseOptimized(true);
	setNumThreads(4);

	// 读入图片
	Mat image = imread("dc.jpg");

	// 缩放到200  （图片太大很慢的……）
	int newHeight =200;
	int newWidth = 1.0*image.cols*newHeight / image.rows;
	Mat im;
	double 倍数 = 1.0* image.rows/ newHeight ;
	resize(image, im, Size(newWidth, newHeight));

	//用默认参数初始化selective search分割物体检测

	Ptr<SelectiveSearchSegmentation> ss = createSelectiveSearchSegmentation();
	//输入需要检测的图片
	ss->setBaseImage(im);

	// Switch to fast but low recall Selective Search method
	//切换到高速模式
		ss->switchToSelectiveSearchFast();
	//高recall模式，慢一点
	//	ss->switchToSelectiveSearchQuality();
	// 执行
	std::vector<Rect> rects;
	ss->process(rects);
	std::cout << "Total Number of Region Proposals: " << rects.size() << std::endl;

	// 显示的数目
	int numShowRects = 10;
	//每次按键增减的数量
	int increment = 5;

	while (true) {
		Mat imOut = image.clone();

		// 遍历得出的矩形框…
		for (int i = 0; i < rects.size(); i++) {

			if (i < numShowRects) {
				Rect temp(rects[i].x*倍数, rects[i].y*倍数, rects[i].width*倍数, rects[i].height*倍数);
				rectangle(imOut, temp, Scalar(0, 0, 255));
			}
			else {
				break;
			}
		}
		imshow("i键增加d键减少", imOut);

		int k = waitKey();

		// 按下i键增加显示的框的数量
		if (k == 'i') {
			numShowRects += increment;
		}
		// 按下d键减少
		else if (k == 'd' && numShowRects > increment) {
			numShowRects -= increment;
		}
		else if (k == 'q') {
			break;
		}
	}
	return 0;
}
```

大佬的博客中提到，物体不太多的时候一般 1000-1200 的数量就足够表征物体啦~



附上原图方便大家自己验证~

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/181031/8mD8af625d.png?imageslim)


# 相关资料

- [【OpenCV_contri】找出任意物体可能在的位置（Selective search，物体检测）](https://blog.csdn.net/zmdsjtu/article/details/78242521?utm_source=blogxgwz7)
