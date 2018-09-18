---
title: pyinstaller
toc: true
date: 2018-09-18
---



`pyinstaller -F -w -i 1003.ico cutimage.py`


这个是用 pyinstaller 来打包的

在 Anaconda 环境下使用这个来打包遇到很多问题。

最后，卡到了：`Exception: Cannot find PyQt5 plugin directories`，无论是怎么重装都不行。

看了下，好像只能使用原生的 Python3.5 来打包。

- [Exception: Cannot find PyQt5 plugin directories when using Pyinstaller despite PyQt5 not even being used](https://stackoverflow.com/questions/39736000/exception-cannot-find-pyqt5-plugin-directories-when-using-pyinstaller-despite-p?noredirect=1)

- [将自己的python程序打包成.exe/.app(秀同学一脸呐)](https://blog.csdn.net/MrLevo520/article/details/51840217)
- [Python 3.6打包成EXE可执行程序](https://blog.csdn.net/zt_xcyk/article/details/73786659)



在使用 pyinstaller cutimage.py 来打包我的 py 程序的时候，有下面的问题：
`No module named 'setuptools._vendor'`
查看了下面的文章，应该是 Setuptools 版本不够：
[Python 3: ImportError “No Module named Setuptools”](https://stackoverflow.com/questions/14426491/python-3-importerror-no-module-named-setuptools)
升级了版本之后可以了：
`python -m pip install -U pip setuptools`

然后遇到下面的问题：

`Cannot find existing PyQt5 plugin directories`

这个问题网上有很多，暂时没有跟进下去。

- [Pyinstaller cannot find PyQt5 plugin directories](https://github.com/pyinstaller/pyinstaller/issues/3636)

跟进了，但是还是不行，使用原生的 Python ，但是打包的时候好像使用的是这个原生的 Python，这个不确定，但是如果是这样的话是不行的。暂时没有找到好的方法。


- [python3.4写好的.py文件如何打包成exe?](https://www.zhihu.com/question/31784262)


- [pyinstaller](https://github.com/pyinstaller/pyinstaller)
