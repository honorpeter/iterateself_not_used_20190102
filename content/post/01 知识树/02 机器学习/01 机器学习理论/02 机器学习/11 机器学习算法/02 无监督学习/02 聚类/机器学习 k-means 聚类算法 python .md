---
title: 机器学习 k-means 聚类算法 python 
toc: true
date: 2018-10-31
---

# 机器学习之k-means聚类算法(python实现)

次简单介绍了kNN算法，简单来说，通过计算目标值与样本数据的距离，选取k个最近的值，用出现概率大的分类值代表目标值的分类，算法实现比较简单，属于监督学习方法。 这篇文章打算简单介绍k-means聚类算法，与之前不同，是一种非监督的学习方法。 机器学习中两类大问题，分类和聚类。 分类是根据一些给定的已知类别标号的样本，训练某种学习机器，使它能够对未知类别的样本进行分类。这属于supervised learning（监督学习）。而聚类指事先并不知道任何样本的类别标号，希望通过某种算法来把一组未知类别的样本划分成若干类别，这在机器学习中被称作 unsupervised learning （无监督学习）。

### k-means 聚类算法

通常，根据样本间的某种距离或者相似性来将样本分为不同类别，成为聚类。 比如给定数据集，部分数据（二维， 共80个）如下：

```
1.658985    4.285136
-3.453687   3.424321
4.838138    -1.151539
-5.379713   -3.362104
0.972564    2.924086
复制代码
```

其可视化如下：

![image.png](https://user-gold-cdn.xitu.io/2018/3/1/161e0fac478c5871?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

 从分布状态，可以大概知道可以聚为4个cluster。最后目的是将4个不同的cluster标上不同的颜色。 利用k-means算法如下实现：



1. 随机选取k个点作为初始质心。
2. 对于样本中每一个点，分别求与k点的距离。距离最小者就属于该类。
3. 此时对得到的k各类，重新计算新的质心。
4. 当3步得到的质心与之前的质心误差很小时，分类结束。 其中用到的公式都特别简单，后面代码有详细叙述。

### python 代码实现

```
# 数据初始化
import numpy as np
import random
import re
import matplotlib.pyplot as plt

def loadDataSet():
    dataSet = np.loadtxt("dataSet.csv")
    return dataSet
复制代码
```

------

```
def initCentroids(dataSet, k):
    # 从数据集中随机选取k个数据返回
    dataSet = list(dataSet)
    return random.sample(dataSet, k)
复制代码
```

对应第2步，计算距离并分类，根据到不同质心的最短距离分类，用字典保存。

```
def minDistance(dataSet, centroidList):

    # 对每个属于dataSet的item， 计算item与centroidList中k个质心的距离，找出距离最小的，并将item加入相应的簇类中
    clusterDict = dict() #dict保存簇类结果
    k = len(centroidList)
    for item in dataSet:
        vec1 = item
        flag = -1
        minDis = float("inf") # 初始化为最大值
        for i in range(k):
            vec2 = centroidList[i]
            distance = calcuDistance(vec1, vec2)  # error
            if distance < minDis:
                minDis = distance
                flag = i  # 循环结束时， flag保存与当前item最近的蔟标记
        if flag not in clusterDict.keys():
            clusterDict.setdefault(flag, [])
        clusterDict[flag].append(item)  #加入相应的类别中
    return clusterDict  #不同的类别
复制代码
```

------

```
def getCentroids(clusterDict):
    #重新计算k个质心
    centroidList = []
    for key in clusterDict.keys():
        centroid = np.mean(clusterDict[key], axis=0)
        centroidList.append(centroid)
    return centroidList  #得到新的质心
复制代码
```

计算计算各蔟集合间的均方误差，来衡量聚类的效果

```
def getVar(centroidList, clusterDict):
    # 计算各蔟集合间的均方误差
    # 将蔟类中各个向量与质心的距离累加求和
    sum = 0.0
    for key in clusterDict.keys():
        vec1 = centroidList[key]
        distance = 0.0
        for item in clusterDict[key]:
            vec2 = item
            distance += calcuDistance(vec1, vec2)
        sum += distance
    return sum
复制代码
```

------

```
#测试聚类效果，并可视化
def test_k_means():
    dataSet = loadDataSet()
    centroidList = initCentroids(dataSet, 4)
    clusterDict = minDistance(dataSet, centroidList)
    # # getCentroids(clusterDict)
    # showCluster(centroidList, clusterDict)
    newVar = getVar(centroidList, clusterDict)
    oldVar = 1  # 当两次聚类的误差小于某个值是，说明质心基本确定。

    times = 2
    while abs(newVar - oldVar) >= 0.00001:
        centroidList = getCentroids(clusterDict)
        clusterDict = minDistance(dataSet, centroidList)
        oldVar = newVar
        newVar = getVar(centroidList, clusterDict)
        times += 1
        showCluster(centroidList, clusterDict)

if __name__ == '__main__':
    # show_fig()
    test_k_means()
复制代码
```

如上如，当两次计算质心之间的误差在0.00001之内时，可以认为聚类完成。 运行函数：

![image.png](https://user-gold-cdn.xitu.io/2018/3/1/161e0fac47550ee4?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

![image.png](https://user-gold-cdn.xitu.io/2018/3/1/161e0fac478d0be6?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

![image.png](https://user-gold-cdn.xitu.io/2018/3/1/161e0fac47790544?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

![image.png](https://user-gold-cdn.xitu.io/2018/3/1/161e0fac4768095d?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)



从结果可以看出，对着不断的迭代，聚类的效果越来越好，直至小于误差，完成聚类。

完成代码和数据请参考github：
 [github:k-means](https://link.juejin.im?target=https%3A%2F%2Fgithub.com%2Fyunshuipiao%2Fcheatsheets-ai-code%2Ftree%2Fmaster%2Fmachine_learning_algorithm%2Fk_means)





# 相关资料

- [机器学习之k-means聚类算法(python实现)](https://juejin.im/post/5a97d129f265da239235c2eb)
