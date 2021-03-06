---
title: DL 激活函数
toc: true
date: 2018-06-26 19:34:32
---
## 相关资料
1. 《解析卷积神经网络》魏秀参




## 需要补充的






  * aaa



* * *




# INTRODUCTION






  * aaa
















激活函数





“激活函数”,又称“非线性映射函数”,是深度卷积神经网络中不可或缺的 关键模块。可以说,深度网络模型其强大的表示能力大部分便是由激活函数的 非线性带来的。在上一篇第2.5节中，我们曾简单介绍了 Sigmoid型函数和修 正线性单元（ReLU型函数）这两种著名的激活函数。本节将系统介绍、对比 七种当下深度卷积神经网络中常用的激活函数：Sigmoid型函数、tanh（x）型函 数、修正线性单元（ReLU）、Leaky ReLU、参数化ReLU、随机化ReLU和指 数化线性单元（ELU）。

直观上,激活函数模拟了生物神经元特性,接受一组输人信号并产生输出,

并通过一个阈值模拟神经元的激活和兴奋状态，如图8.1所示，可明显发现二者 在抽象层面极其相似。下面，我们从在人工神经网络发展过程中首个被广泛接 受的激活函数 Sigmoid型函数 说起。

8.1 Sigmoid 型函数
Sigmoid型函数也称Logistic函数:

(8+1)

其函数形状如图8.2a所示。很明显可以看出，经过Sigmoid型函数作用后，输 出响应的值域被压缩到［0,1］之间，而0对应了生物神经元的“抑制状态”，1 则恰好对应了 “兴奋状态”。但对于Sigmoid函数两端大于5 （或小于-5）的 区域，这部分输出会被压缩到1 （或0）。这样的处理会带来梯度的“饱和效 应” （saturation effect）。不妨对照Sigmoid型函数的梯度图（图8.2b）,大于5 （或小于-5）部分的梯度接近0,这会导致在误差反向传播过程中导数处于该 区域的误差很难甚至无法传递至前层，进而导致整个网络无法正常训练。




（b） Sigmoid型函数梯度


图8.2: Sigmoid型函数及其函数梯度。

另外，从图8.2a中可观察到Sigmoid型激活函数值域的均值并非为0而是 全为正，这样的结果实际上并不符合我们对神经网络内数值的期望（均值）应 为0的设想。

3.2. TANH(X)型函数

8.2    tanh(x)型函数
tanh(x)型函数是在Sigmoid型函数基础上为解决均值问题提出的激活函数：

tanh(x) = 2a(2x) — 1.    (8.2)

tanh(x)型函数又称作双曲正切函数(hyperbolic tangent function),其函数范 围是(-1, +1),输出响应的均值为0。但由于tanh(x)型函数仍基于Sigmoid 型函数，使用tanh(x)型函数依然会发生“梯度饱和”现象。

8.3修正线性单元(ReLU)
为了避免梯度饱和现象的发生，Nair和Hinton在2010年将修正线性单元 (Rectified Linear Unit,简称ReLU)引人神经网络［69］。ReLU函数是目前深 度卷积神经网络中最为常用的激活函数之一。

ReLU函数实际上是一个分段函数，其定义为：



(8+3)

(8+4)

与前两个激活函数相比：ReLU函数的梯度在x》0时为1,反之为0 (如图 8.3所示)；对x >0部分完全消除了 Sigmoid型函数的梯度饱和效应。计算复 杂度上，ReLU函数也相对前两者的指数函数计算更为简单。同时，实验中还发 现ReLU函数有助于随机梯度下降方法收敛，收敛速度约快6倍左右［52］。不 过，ReLU函数也有自身缺陷，即在x<0时，梯度便为0。换句话说，对于小 于0的这部分卷积结果响应，它们一旦变为负值将再无法影响网络训练——这



（a） ReLU 函数    （b） ReLU

图8+3: ReLU函数及其函数梯度

8.4 Leaky ReLU
为了缓解“死区”现象，研究者将ReLU函数中x < 0的部分调整为f （x） = a + x, 其中a为0.01或0.001数量级的较小正数。这种新型的激活函数被称作“Leaky ReLU” ［641：

ax


if x > 0

if x < 0


(8+5)


可以发现，原始ReLU函数实际上是Leaky ReLU函数的一个特例，即a = 0 （见图8.4a和图8.4b）。不过由于Leaky ReLU中a为超参数，合适的值较难设 定且较为敏感，因此Leaky ReLU函数在实际使用中的性能并不十分稳定。

参数化ReLU ［34］的提出很好的解决了 Leaky ReLU中超参数a不易设定的问 题：参数化ReLU直接将a也作为一个网络中可学习的变量融人模型的整体训 练过程。在求解参数化ReLU时，文献［34］中仍使用传统的误差反向传播和随 机梯度下降，对于参数 a 的更新遵循链式法则，具体推导细节在此不过多赘述， 感兴趣的读者可参考文献［34］。

实验结果验证方面，文献［34］曾在一个14层卷积网络上对比了 ReLU和参 数化ReLU在ImageNet 2012数据集上的分类误差（top-1和top-5）。网络结

8.6.随机化RELU

构如表8.1,每层卷积操作后均有参数化ReLU操作。表中第二列和第三列数 值分别表示各层不同通道(channel)共享参数a和独享参数a15时网络自动学 习的a取值。实验结果如表8.2中所示。可以发现，在分类精度上，使用参数 化ReLU作为激活函数的网络要优于使用原始ReLU的网络，同时自由度较大 的各通道独享参数的参数化ReLU性能更优。另外，需指出表8.1中几个有趣 的观察：

1.    与第一层卷积层搭配的参数化ReLU的a取值(表8.1中第一行0.681和 0.596)远大于ReLU中的0。这表明网络较浅层所需非线性较弱。同时, 我们知道浅层网络特征一般多为表示“边缘”、 “纹理”等特性的泛化特 征。这一观察说明对于此类特征正负响应(activation)均很重要；这也解 释了固定a取值的ReLU (a = 0)和Leaky ReLU相比参数化ReLU性 能较差的原因。

2.    请注意独享参数设定下学到的a取值(表8.1中的最后一列)呈现由浅层 到深层依次递减的趋势，说明实际上网络所需的非线性能力随网络深度增 加而递增。

不过万事皆具两面性，参数化ReLU在带来更大自由度的同时，也增加了网络 模型过拟合的风险，在实际使用中需格外注意。

8.6随机化ReLU
另一种解决a超参设定的方式是将其随机化，这便是随机化ReLU。该方法首 次提出并实用于kaggle16上举办的2015年“国家数据科学大赛”(national data science bowl)——浮游动物的图像分类17。比赛中参赛者凭借随机化ReLU — 举夺冠。

表8+1:文献［34］实验中的14层网络，及不同设定下学到的参数化ReLU中超 参数a取值。

学到的a取值

网络结枸

共享参数a

独享参数a

convl

f = 7; s = 2; d =64

0.681

0.596

pooll

f = 3; s = 3

conv2i

f = 2; s = 1; d =128

0.103

0.321

conv22

f = 2; s = 1; d =128

0.099

0.204

conv23

f = 2; s = 1; d =128

0.228

0.294

conv24

f = 2; s = 1; d =128

0.561

0.464

pool2

f = 2； s = 2

conv3i

f = 2; s = 1; d =256

0.126

0.196

conv32

conv33

f = 2; s = 1; d =256

0.124

U.丄02

0.145

conv34

f = 2; s = 1; d =256

0.062

0.124

conv35

f = 2; s = 1; d =256

0.008

0.134

conv36

f = 2; s = 1; d =256

0.210

0.198

SPP [35]

{6, 3, 2,1}

fci

4096

0.063

0.074

fC2

fC3

4096

1000

0.031

0.075

对于随机化ReLU中a的设定，其取值在训练阶段服从均匀分布，在测试 •段则将其指定为该均匀分布对应的分布期望18:

(8+6)


8.7.指数化线性单元（ELU）

表8.2: ReLU与参数化ReLU在ImageNet 2012数据集上分类错误率对比

top-1

top-5

ReLU

33.82

13.34

参数化ReLU （共享参数a）

参数化ReLU （独享参数a）

32.71

32.64

12.87

12.75

其中，

a'    U(l, u), l < u,

最后，我们在图8.4中对比了 ReLU、Leaky ReLU、参数化ReLU和随机化 ReLU四种激活函数，读者可直观比较各自差异。

8.7指数化线，|
2016 年，Clevert 等人［8］提出了指数化线性单元(Exponential Linear Unit, ELU)：


x0

x<0


(8+8)


显然，ELU具备ReLU函数的优点，同时ELU也解决了 ReLU函数自身的 “死区”问题。不过，ELU函数中的指数操作稍稍增大了计算量。实际使用中， ELU中的超参数A —般设置为1。

8.8小结
§ 激活函数（非线性映射函数）对向深度网络模型引人非线性而产生强大表

示能力功不可没；

§ Sigmoid型函数是历史上最早的激活函数之一，但它与tanh（x）型函数一 样会产生梯度饱和效应，因此在实践中不建议使用；




为指定，而参数化ReLU中a则经



（c）随机化ReLU。


图8.4: ReLU函数及其函数梯度。

建议首先使用目前最常用的ReLU激活函数，但需注意模型参数初始化 （参见第7章内容）和学习率（参见第II.2.2节内容）的设置； 为了进一步提高模型精度，可尝试Leaky ReLU、参数化ReLU、随机化 ReLU和ELU。但四者之间实际性能优劣并无一致性结论，需具体问题具

8.8.小结





:b) ELU的导数。





















* * *




# COMMENT
