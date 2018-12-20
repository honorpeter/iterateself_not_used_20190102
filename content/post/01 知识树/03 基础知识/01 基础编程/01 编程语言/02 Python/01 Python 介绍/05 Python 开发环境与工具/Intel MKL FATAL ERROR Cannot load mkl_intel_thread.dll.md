# 需要补充的


# Intel MKL FATAL ERROR: Cannot load mkl_intel_thread.dll.

这个问题，当我把 pycharm 升级到最新的时候，再安装 matplotlib 的时候总是遇到。

而且，是这样的，在 console 里执行这个的时候是没有问题的：

```py
from matplotlib import pyplot as plt
fig = plt.figure()
```

但是，在 pycharm 里用 py 脚本执行这个的时候就有问题：

```
Intel MKL FATAL ERROR: Cannot load mkl_intel_thread.dll.
```

之前查了下，以为是 numpy+mkl 的问题，因此，把 mkl 卸载了，然后重新用 pip 安装了 numpy，但是后面 用 conda 安装的时候又把 mkl 安装上了，所以这个问题还是没解决。

后来看了下：

- [Intel MKL FATAL ERROR: Cannot load mkl_intel_thread.dll. ](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360000365510-Intel-MKL-FATAL-ERROR-Cannot-load-mkl-intel-thread-dll-)
- [Anaconda Intel MKL FATAL ERROR when running scripts in 2017.3 and no py.test suites found in project](https://youtrack.jetbrains.com/issue/PY-27466)

这个问题之后，发现，好像新版本的 pycharm 就是有这个问题，应该是 pycharm 的 科学计算模式是要对接 matplotlib 来画图。

所以是有这个问题的。

换了低版本的 pycharm 应该是没有这个问题的。


# 相关资料

- [Intel MKL FATAL ERROR: Cannot load mkl_intel_thread.dll. ](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360000365510-Intel-MKL-FATAL-ERROR-Cannot-load-mkl-intel-thread-dll-)
- [Anaconda Intel MKL FATAL ERROR when running scripts in 2017.3 and no py.test suites found in project](https://youtrack.jetbrains.com/issue/PY-27466)
