---
title: ran out of gpu memory
toc: true
date: 2018-10-13
---
# ran out of gpu memory

在跑 CRNN 模型的时候，有这个提示，嗯，后来我看了下，因为要对每个 图片对应最长长度的图像进行补齐，因此，每个图像都会变得很大，在 BATCH_SIZE =128 的时候，就需要很多的内存，因此，我把它改成了 BATCH_SIZE=32 就可以了。




# 相关资料

- [How can I solve 'ran out of gpu memory' in TensorFlow](https://stackoverflow.com/questions/36927607/how-can-i-solve-ran-out-of-gpu-memory-in-tensorflow)
