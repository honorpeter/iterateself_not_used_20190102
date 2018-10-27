---
title: Python 对于 None 还是有点不清楚
toc: true
date: 2018-10-27
---

今天遇到一个问题：

a=cv2.imread(img_path)

如果文件是坏的，那么 type(a) 是 NoneType

但是如果文件是好的，那么 type(a) 就是 np.array
因此 使用 a==None 来判断是否正确加载是不行的，他会提示说 用 .all() 或者 .any()
但是，使用  (a==None).all() 这个好像也是不行的 <span style="color:red;">这个不是很确定要怎么写</span>
后来，使用了 type(a)==type(None) 这个好像暂时是可以的，不确定。<span style="color:red;">后续要进行确认下。</span>
