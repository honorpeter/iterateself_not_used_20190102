---
title: 对于完整页面的 OCR
toc: true
date: 2018-09-03
---



作者：匿名用户

链接：https://www.zhihu.com/question/20191727/answer/155920501

来源：知乎

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

利益相关，OCR类app开发者；目前识别印刷体中文已经稳定在95%以上。

OCR一般分为几个步骤：

1 版面分析 2 行拆分为字符  3 识别字符 4 识别后矫正

如果要进行商业应用，一般来讲使用C++和opencv的组合是最好的

如果仅仅学术研究，直接使用matlab即可；但是注意：matlab很多内置算法的效果不如opencv对应算法的效果

下面展开来讲——

1 版面分析

版面分析也就是把一整张图像拆分为行；便于后面一行一行地处理。

在图像没有明显倾斜扭曲时，可以先使用笔画等宽算法(swt算法)把非笔迹的像素过滤掉，再使用投影直方图进行分行；以下是一个分行样例。

<img src="https://pic2.zhimg.com/v2-c5bc27071b2f0fb4366e009e641420f9_b.png" data-rawwidth="1620" data-rawheight="784" class="origin_image zh-lightbox-thumb" width="1620" data-original="https://pic2.zhimg.com/v2-c5bc27071b2f0fb4366e009e641420f9_r.jpg">

2 行拆分为字符

拆分，就是把每一行拆分到独立的字；最简单的办法就是使用连通域分析或者直方图投影进行拆分

<img src="https://pic2.zhimg.com/v2-597ef67d63a0c1f8ce2842e792c45829_b.png" data-rawwidth="2194" data-rawheight="234" class="origin_image zh-lightbox-thumb" width="2194" data-original="https://pic2.zhimg.com/v2-597ef67d63a0c1f8ce2842e792c45829_r.jpg">

3  识别字符

识别字符就在于生成样本+选择识别算法

入门可以参考这篇文章[OpenCV 2.4+ C++ SVM文字识别](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/justany/archive/2012/11/27/2789767.html)

里面采用了最简单的办法进行建模(定位字符区域后缩放到8x8方块)，并且使用了一种很常见的方法(SVM)进行训练和识别。

实践中，要注意几点：

（1）大样本+简单识别方法优于小样本+复杂识别算法。所以不需要选择太复杂的建模和分类方法，尽量通过缩放平移等方法把原始样本展开即可。

（2）字体数量要跟建模方法适应。字体不能太少；否则样本不足；字体也不能太多，以免样本互相覆盖——多个相似的样本指向不同的标签。

  (3)要考虑单个字符被不当分割和不同字符粘连的情况。这个时候就需要识别算法能提供置信度的计算，并且尝试不同识别组合，找到总的置信度最高的一种情况。可以先进行过切分，再使用图相关算法找出最佳组合——找到最佳切分组合就相当于在图里找到一条最短路径（这里的“图”说的是算法导论中的图）。

<img src="https://pic1.zhimg.com/v2-8c0d8fa5206c5089317e07c1c681a580_b.png" data-rawwidth="540" data-rawheight="184" class="origin_image zh-lightbox-thumb" width="540" data-original="https://pic1.zhimg.com/v2-8c0d8fa5206c5089317e07c1c681a580_r.jpg">

<img src="https://pic4.zhimg.com/v2-f817e5944b83c6ba13403ec8604070a3_b.png" data-rawwidth="1934" data-rawheight="190" class="origin_image zh-lightbox-thumb" width="1934" data-original="https://pic4.zhimg.com/v2-f817e5944b83c6ba13403ec8604070a3_r.jpg">

4 识别后矫正

再好的算法，也难免会有识别错误的时候。比如“了”和“T”, “1”和“|”，等等。可以考虑使用马尔可夫模型或者其它类似算法进行识别结果矫正。






手写的别想啦，目前没人做的出商用的。印刷体的搞得好就很了不起了。在不规范输入的情况下，识别的快和准，支持多种字体；就够你折腾一壶的了。


艺术字字体再多也是有限的嘛。就算你1000种艺术字又如何。而手写字体风格是接近无限的，10万个人就10万种字体，根本没法训。

那字体数多了，如果都训练。就会有边界模糊（基于概率的一类机器学习算法），导致识别率下降。



请问在进行切割的时候字体有粘连，最好怎么处理呢。字切割还有些什么办法呢，目前在做文字识别的一个东西，但是切割的时候效果都不太好。

腐蚀 然后过切分 然后尝试所有切割组合







这个主要分为 text detection 和 recognition两个部分，text detection可以借鉴fast-Rcnn rpn等方法，这种bottom up的方法来处理图片文字会有很多问题，比如proposal太多，随着up过程会不断顺序累积，而且需要通过额外步骤对这些proposal进行过滤等。而ctpn方法通过固定宽度的锚定机制，在卷积特征上直接操作，提供了端到端处理的可能性,而且通过使用lstm层，进一步增加了识别的准确性。recognition部分的话，可以使用之前大神们说的 CNN + LSTM + CTC方法，crnn也是一个不错的选择，guthub上已经有了ctpn + crnn结合的caffe代码，可以作为参考，当然，我还是比较喜欢tensorflow来写^_^

作者：catherineaustin
链接：https://www.zhihu.com/question/20191727/answer/271079695
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

您不觉得text detection最大的问题在于样本不够么~毕竟需要人手工画框的~



预处理（倾斜校正 去噪等）版面分析 字符切分 特征提取（确定特征 降维等） 分类（比如最近邻 神经网络 svm等等） 后处理（自然语言理解范畴）





刚好现在在公司做OCR和STR, 现在主流的方法是CNN（基于featuremap的文字检测）+lstm（任意序列的文字行识别），ICDAR2015文字竞赛上top的成绩基本都是这种方法了，另外题主如果想实现end to end的训练和预测可以直接考虑简单暴力的fasterrcnn，出来的结果用cnn过滤下可以达到ICDAR几个challenge的top3.

作者：steve tim
链接：https://www.zhihu.com/question/20191727/answer/126167192
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
