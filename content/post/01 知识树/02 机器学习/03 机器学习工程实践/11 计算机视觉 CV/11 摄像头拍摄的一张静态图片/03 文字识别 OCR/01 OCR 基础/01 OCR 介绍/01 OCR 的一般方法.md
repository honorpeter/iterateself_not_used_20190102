---
title: 01 OCR 的一般方法
toc: true
date: 2018-09-25
---
一般的 OCR 包含两步：

- detection -> 找到包含文字的区域(proposal)
- classification -> 识别区域中的文字

detection就是为了从给定的区域中找到存在文字的区域和不存在文字的区域（背景），faster-rcnn的分类是关于该区域是否是存在文字，并且将存在文字的这部分区域框起来给出坐标。为后续对框出来的区域进行文字的识别做准备
