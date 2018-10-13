---
title: GPU 到底比 CPU 快多少
toc: true
date: 2018-10-13
---

# GPU 到底能比 CPU 快多少


对于 3.50GHz 的 CPU 和 8G 的 GPU，两者的速度差大约在 32-37 倍;

性价比上，同样的钱买 GPU 和买 CPU，在做神经网络的时候，速度上大约有 14.5~16.8 倍的差距。

在我的感觉，确实是这样，而且很好验证，在一台装了 GPU 的电脑上，先用它的 CPU 跑一个模型，看 100 个 batch 的时间，再用 GPU 跑以下。基本上是 3.5G*12 的 CPU 用 20s 跑完的，1080Ti 的 GPU 用 0.5 s 可以跑完。<span style="color:red;">这个 CPU 到底是不是用满了 12 核好像忘记了，好像在 top 里看到的是 1100% ，但是也不是很确定。</span>


# 相关资料

- [Pytorch用GPU到底能比CPU快多少？](https://zhuanlan.zhihu.com/p/35434175)
