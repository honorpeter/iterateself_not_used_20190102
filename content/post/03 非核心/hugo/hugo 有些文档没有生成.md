---
title: hugo 有些文档没有生成
toc: true
date: 2018-08-26
---

# hugo 有些文档没有生成

我发现，有些文档没有生成，而且，并不是由于 url 错误我没有找到，而是的确没有生成。

我看了下 gihub 的 gh-pages ，也的确没有找到应该生成的 index.html 。

而，我的 md 文件的确上传到 github了，说明travis 在 hugo 的时候，这个文件是存在的。

但是不知道为什么，没有build。

我在本地试了下，也的确是没有生成。

在网上查了下，找到了：

问题的原因是：hugo 根据 date 认为这个文件是未来的，这个时间还没到。

可以用：`hugo -F` 来把date为未来的文件也build 出来。

但是，我的date 写的是今天已经过了的时间呀？为什么还出现了这个情况？

猜测应该是这个时间对于美国来说是还没有到的时间。<span style="color:red;">不清楚是不是这个原因。以及不知道是不是可以通过修改 config.toml 里面的 defaultContentLanguage 为 zh-cn 来修正这个问题。暂时我是通过 `hugo -F` 来对应的。</span>



## 相关资料

- [Issue with generating site - missing posts](https://discourse.gohugo.io/t/issue-with-generating-site-missing-posts/12149)
