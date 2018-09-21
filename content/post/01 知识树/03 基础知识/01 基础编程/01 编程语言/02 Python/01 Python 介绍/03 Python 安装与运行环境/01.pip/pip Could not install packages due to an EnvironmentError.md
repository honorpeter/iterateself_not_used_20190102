
在 Pycharm 的 console 里面进行更新的收遇到了一个问题:

```
(venv) E:\02.try\092001>pip install pytesseract
Collecting pytesseract
Collecting Pillow (from pytesseract)
  Downloading https://files.pythonhosted.org/packages/2e/5f/2829276d720513a434f5bcbf61316d98369a5707f6128b34c03f2213feb1/Pillow-5.2.0-cp35-cp35m-win_amd64.whl (1.6MB)
Could not install packages due to an EnvironmentError: raw write() returned invalid length 2 (should have been between 0 and 1)
```


这个好像是 windows 的问题：

[Python throws IOError in some scripts in Windows Integrated Terminal](https://github.com/Microsoft/vscode/issues/36630)

windows 升级到 1803 应该是可以的。
