---
title: Python 工具 pip
toc: true
date: 2018-06-11 08:14:44
---

# 需要补充的

- **还需要再补充下。**
- **pip管理与conda管理有什么区别？conda可以代替pip吗？**
- **pip的管理与linux自己的安装指令优先用那个？**
- **pip 安装的环境到底是在哪里？要不要给一个项目单独创造一个pip的环境，这样大家用的时候可以通用？还是说电脑上只有一个pip的环境，每个人的pip环境都要自己配置？**
- **requirements.txt 一般什么时候用到？这个txt文档一般放在项目的那个地方，那个文件夹里面？在什么文档中要提到这个txt？README.md里面吗？**



# pip 介绍





# pip 简单使用




## 使用 pip 来管理 python 的包




    # 安装，可指定版本号
    (sudo) pip install Django==1.6.8
    # 升级
    (sudo) pip install bpython --upgrade
    # 一次安装多个
    (sudo) pip install BeautifulSoup4 fabric virtualenv
    # 删除
    (sudo) pip uninstall xlrd




## requirements.txt 文件的使用


可以导出当前已经安装包到 requirements.txt 文本中，这样别人如果使用你的程序，安装环境的时候子需要把requirements.txt 安装进来即可，他会自动安装里面的内容。


    # 导出当前已经安装包到 requirements.txt 文本中
    pip freeze > requirements.txt
    # 从文本中安装，文本中为包名，一行一个，可以指定版本号
    (sudo) pip install –r requirements.txt





# 相关资料

- [python基础教程 w3cschool](https://www.w3cschool.cn/python/)
- [Python 3 教程 菜鸟教程](http://www.runoob.com/python3/python3-tutorial.html)
- [Installation](https://pip.pypa.io/en/latest/installing.html)
