---
title: K-means 计算 anchor
toc: true
date: 2018-11-10
---
# YOLOv3使用笔记——Kmeans聚类计算anchor boxes


anchor boxes用来预测bounding box，faster rcnn中用128*128,256*256,512*512,分三个尺度变换1：1,1：2,2：1,共计9个anchor来预测框，每个anchor预测2000个框左右，使得检出率提高很多。YOLOv2开始增加了anchor机制，在v3中增加到9个anchor。例如yolov3-voc.cfg中这组anchor，anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326，由作者通过聚类VOC数据集得到的，20类目标中大到bicycle、bus，小到bird、cat，目标大小差距很大，如果用自己的数据集训练检测目标，其中部分anchor并不合理，本文记录下在自己的数据集上聚类计算anchor，提高bounding box的检出率。



原工程：https://github.com/lars76/kmeans-anchor-boxes

Joseph Redmon论文数据avg iou在67.2，该作者验证在k=9时，多次迭代在VOC 2007数据集上得到avg iou在67.13，相差无几。



修改的example.py



```
import glob
import xml.etree.ElementTree as ET

import numpy as np

from kmeans import kmeans, avg_iou

ANNOTATIONS_PATH = "Annotations"
CLUSTERS = 9


def load_dataset(path):
dataset = []
for xml_file in glob.glob("{}/*xml".format(path)):
​    tree = ET.parse(xml_file)

 height = int(tree.findtext("./size/height"))
 width = int(tree.findtext("./size/width"))

 for obj in tree.iter("object"):
   xmin = int(obj.findtext("bndbox/xmin")) / width
   ymin = int(obj.findtext("bndbox/ymin")) / height
   xmax = int(obj.findtext("bndbox/xmax")) / width
   ymax = int(obj.findtext("bndbox/ymax")) / height

   xmin = np.float64(xmin)
   ymin = np.float64(ymin)
   xmax = np.float64(xmax)
   ymax = np.float64(ymax)
   if xmax == xmin or ymax == ymin:
      print(xml_file)
   dataset.append([xmax - xmin, ymax - ymin])
return np.array(dataset)

if __name__ == '__main__':
#print(__file__)
data = load_dataset(ANNOTATIONS_PATH)
out = kmeans(data, k=CLUSTERS)
#clusters = [[10,13],[16,30],[33,23],[30,61],[62,45],[59,119],[116,90],[156,198],[373,326]]
#out= np.array(clusters)/416.0
print(out)
print("Accuracy: {:.2f}%".format(avg_iou(data, out) * 100))
print("Boxes:\n {}-{}".format(out[:, 0]*416, out[:, 1]*416))

ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
print("Ratios:\n {}".format(sorted(ratios)))
```

Kmeans因为初始点敏感，所以每次运行得到的anchor值不一样，但是对应的avg iou稳定。用于训练的话就需要统计多组anchor，针对固定的测试集比较了。

可以计算下VOC的这组anchor在自己数据集上的avg iou，对比直接在数据集上聚类得到的anchor以及avg iou。





参考：

https://blog.csdn.net/hrsstudy/article/details/71173305?utm_source=itdadao&utm_medium=referral

https://blog.csdn.net/sinat_24143931/article/details/78773936


# 相关资料


- [YOLOv3使用笔记——Kmeans聚类计算anchor boxes](https://blog.csdn.net/cgt19910923/article/details/82154401)
