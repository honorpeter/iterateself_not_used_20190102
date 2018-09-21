---
title: 08 CRAFT
toc: true
date: 2018-09-22
---
# R-CNN

R-CNN 系列算法的第一阶段是生成目标 proposals，第二阶段是对目标 proposals 进行分类，2016年中科院自动化所提出的 CRAFT 算法分别对 Faster R-CNN 中的这两个阶段进行了一定的改进。对于生成目标 proposals 阶段，在 RPN 的后面加了一个二值的 Fast R-CNN 分类器来对 RPN 生成的 proposals 进行进一步的筛选，留下一些高质量的 proposals；对于第二阶段的目标 proposals 分类，在原来的分类器后又级联了N个类别（不包含背景类）的二值分类器以进行更精细的目标检测。
