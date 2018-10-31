---
title: mv 是不是有文件数量限制
toc: true
date: 2018-10-31
---


mv 很多文件的时候，总是出现 argument list too long

还是要确认下的。

```
find folder2 -name '*.*' -exec mv {} folder \;
```



- [Moving large number of files](https://stackoverflow.com/questions/11942422/moving-large-number-of-files)
