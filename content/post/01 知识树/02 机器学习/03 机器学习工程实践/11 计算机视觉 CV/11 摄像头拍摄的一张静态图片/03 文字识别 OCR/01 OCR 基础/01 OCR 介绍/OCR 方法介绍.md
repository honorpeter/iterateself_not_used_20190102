---
title: OCR 方法介绍
toc: true
date: 2018-09-02
---
# 需要补充的

一般 OCR 步骤是这样的

## 单行的文本分割：

1. 先检测和提取 Text region.
2. 接着利用 radon hough 变换 等方法进行文本校正。
3. 通过投影直方图分割出单行的文本的图片。

## 对单行的 OCR

对单行的 OCR 主要由两种思想

- 需要分割字符(segmentation based method)的
- 无需分割字符(segmentation free method)的

### 第一种是需要分割字符(segmentation based method)的。

分割字符的方法也比较多，用的最多的是基于投影直方图极值点作为候选分割点并使用 分类器+beam search 搜索最佳分割点。具体可以参考 tesseract 的 presentation。

搜索到分割点之后对于单个字符，传统的就是 特征工程+分类器。
一般流程是 灰度 -> 二值化 -> 矫正图像 -> 提取特征(方法多种多样例如 pca lbp 等等) ->分类器(分类器大致有SVM ANN KNN等等 )。

现在的 CNN（卷积神经网络）可以很大程度上免去特征工程。

### 第二种是无需分割字符(segmentation free method)的

对于短长度的可以使用 mutli-label classification 。比如像车牌，验证码,不过提前需要预测长度。
[车牌识别中的不分割字符的端到端(End-to-End)识别](https://link.zhihu.com/?target=http%3A//blog.csdn.net/relocy/article/details/52174198)

google 做街景门牌号识别就是用的这种方法。

要是长度很长的话呢，就得用 CTC 模型了。  ctc loss 能自动对其标签而不需要标注信息。

另外主要注意的一点是 CTC 不一定要配合 RNN 才能 work。纯 CNN 也能做时序任务，只是时序依赖没有 RNN 强而已。







首先OCR是模式识别的一个领域，所以整体过程也就是模式识别的过程。其过程整体来说可以分为以下几个步骤：

1. 预处理：对包含文字的图像进行处理以便后续进行特征提取、学习。这个过程的主要目的是减少图像中的无用信息，以便方便后面的处理。在这个步骤通常有：灰度化（如果是彩色图像）、降噪、二值化、字符切分以及归一化这些子步骤。经过二值化后，图像只剩下两种颜色，即黑和白，其中一个是图像背景，另一个颜色就是要识别的文字了。降噪在这个阶段非常重要，降噪算法的好坏对特征提取的影响很大。字符切分则是将图像中的文字分割成单个文字——识别的时候是一个字一个字识别的。如果文字行有倾斜的话往往还要进行倾斜校正。归一化则是将单个的文字图像规整到同样的尺寸，在同一个规格下，才能应用统一的算法。
2. 特征提取和降维：特征是用来识别文字的关键信息，每个不同的文字都能通过特征来和其他文字进行区分。对于数字和英文字母来说，这个特征提取是比较容易的，因为数字只有10个，英文字母只有52个，都是小字符集。对于汉字来说，特征提取比较困难，因为首先汉字是大字符集，国标中光是最常用的第一级汉字就有3755个；第二个汉字结构复杂，形近字多。在确定了使用何种特征后，视情况而定，还有可能要进行特征降维，这种情况就是如果特征的维数太高（特征一般用一个向量表示，维数即该向量的分量数），分类器的效率会受到很大的影响，为了提高识别速率，往往就要进行降维，这个过程也很重要，既要降低维数吧，又得使得减少维数后的特征向量还保留了足够的信息量（以区分不同的文字）。
3. 分类器设计、训练和实际识别：分类器是用来进行识别的，就是对于第二步，你对一个文字图像，提取出特征给，丢给分类器，分类器就对其进行分类，告诉你这个特征该识别成哪个文字。在进行实际识别前，往往还要对分类器进行训练，这是一个监督学习的案例。成熟的分类器也很多，什么svm，kn，神经网络etc。我当时不知天高地厚用经典bp神经网络去学习，结果……呵呵……
4. 后处理：后处理是用来对分类结果进行优化的，第一个，分类器的分类有时候不一定是完全正确的（实际上也做不到完全正确），比如对汉字的识别，由于汉字中形近字的存在，很容易将一个字识别成其形近字。后处理中可以去解决这个问题，比如通过语言模型来进行校正——如果分类器将“在哪里”识别成“存哪里”，通过语言模型会发现“存哪里”是错误的，然后进行校正。第二个，OCR的识别图像往往是有大量文字的，而且这些文字存在排版、字体大小等复杂情况，后处理中可以尝试去对识别结果进行格式化，比如按照图像中的排版排列什么的，举个栗子，一张图像，其左半部分的文字和右半部分的文字毫无关系，而在字符切分过程中，往往是按行切分的，那么识别结果中左半部分的第一行后面会跟着右半部分的第一行诸如此类。




现在 的 ORC 技术还需要对图像先进行处理吗？

主要是图像的处理，包括灰度处理、二值化、去噪、旋转、水平切割、垂直切割








在深度学习方法出现之前，基于传统的手工设计特征（Handcraft Features），包括基于连通区域，以及基于HOG的检测框描述的方法是比较主流的；如通过最大稳定极值区域（MSER-Maximally Stable Extremal Regions）得到字符的候选，并将这些字符候选看作连通图(graph)的顶点，此时就可以将文本行的寻找过程视为聚类（clustering）的过程，因为来自相同文本行的文本通常具有相同的方向、颜色、字体以及形状。OPENCV3.3中实现了MSER的场景文字检测和识别的算法。

在基于深度学习的办法中，目前看到的大多数解决办法还是Detection和Recognition分开来研究，并没有真正的看Detection+Recognition的端到端完成识别的成果。

Detection部分大多数也是基于proposal的，一般先借助Faster R-CNN或者SSD得到许多个proposal，然后训练分类器对proposal进行分类，最后再做细致处理得到精细的文本区域；这个过程中学者们也解决了文字的方向，大小等的问题。同时，也有基于图像分割来做的，但是看到的不是很多，具体可见参考文献。

如果已经检测到了稳定的文本区域，Recognition部分可以采用比较通用的做法；可以对字符进行分割后单独识别，也可以进行序列识别，容易想见的是，序列识别才是真正有意义的。如前面的答主所说CNN+RNN+CTC的办法是论文中常看到的；这个办法也常用在验证码的自动识别上面。

在Detection方面，乔宇老师团队的：Detecting Text in Natural Image with Connectionist Text Proposal Network, ECCV, 2016. 这篇文章在github上有多个实现(CPTN)；在Recognition方面白翔老师的CRNN也有不错的表现。有人在github上将CPTN和CRNN结合了起来，前者采用Caffe实现，后者采用PyTorch实现，但是这并不是真正意义上的端到端。

如何实现自然场景图片到正确有意义的文本输出是还需一些努力的。

参考文献和链接：

(1) [文字的检测与识别资源 - dllTimes - CSDN博客](https://link.zhihu.com/?target=http%3A//blog.csdn.net/u010183397/article/details/56497303)

(2)[白翔：趣谈“捕文捉字”-- 场景文字检测 | VALSE2017之十](https://zhuanlan.zhihu.com/p/29549641)

(3) [bgshih/crnn](https://link.zhihu.com/?target=https%3A//github.com/bgshih/crnn)

(4) [tianzhi0549/CTPN](https://link.zhihu.com/?target=https%3A//github.com/tianzhi0549/CTPN)

(5) [Scene Text Detection](https://link.zhihu.com/?target=https%3A//docs.opencv.org/3.0-beta/modules/text/doc/erfilter.html)






















作者：大熊

链接：https://www.zhihu.com/question/20191727/answer/184135484

来源：知乎

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

传统的ocr都是二值化，字符分割识别吧。速度比较快，但是只能适应简单背景。

深度学习检测，end-to-end识别适应性好，但是cpu速度不行，手机端更别说了。

百度，阿里的demo都不错，应该也是深度学习检测，序列识别的。

电脑GPU还行的话，可以自己去训练一个

[https://github.com/bear63/sceneReco](https://link.zhihu.com/?target=https%3A//github.com/bear63/sceneReco)

http://blog.csdn.net/u013293750/article/details/73188934

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/E525AB0kJ0.png?imageslim)

![mark](http://pacdb2bfr.bkt.clouddn.com/blog/image/180902/5J9bH63deE.png?imageslim)


训练的模型样本只有100多玩，模型还不稳定，标点符号错得比较多，因为没有专门对标点符号进行训练，都识别成中文了。有硬件支持的话样本增加到几千万，上亿，应该会有更好的结果.

里面的CTPN项目只提供了deploy.prototxt文件，不知道您是否复现了train.proto文件？
