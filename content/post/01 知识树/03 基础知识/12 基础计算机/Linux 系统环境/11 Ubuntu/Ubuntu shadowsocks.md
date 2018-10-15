---
title: Ubuntu shadowsocks
toc: true
date: 2018-10-13
---

# Ubuntu shadowsocks

1.首先使用快捷键 ctrl+alt+t，打开我们的终端窗口
2.接着安装 shadowsocks-qt5

```
sudo add-apt-repository ppa:hzwhuang/ss-qt5
sudo apt-get update
sudo apt-get install shadowsocks-qt5
```

3.然后安装genpac

```
sudo apt-get install python-pip
sudo pip install genpac
```


4.接下来使用 genpac 生成 autoproxy.pac

```
cd /home/xxx
genpac -p "SOCKS5 127.0.0.1:1080" --output="autoproxy.pac"
```


该命令会在 /home/xxx/ 下生成 autoproxy.pac（其中xxx是用户名，比如我的是 /home/zp/）
5.运行shadowsocks-qt5（可通过搜索功能找到），填写server address,server port,password,Encryptioin Method等信息，其他的使用默认的就行了。
6.最后一步，打开 SystemSetting->Network->Network Proxy ，将 Method 改为 Automatic，Configuration Url 填 `file:///home/xxx/autoproxy.pac`，然后 Apply System Wide 即可
7.打开浏览器，现在可以开始科学上网了




这个应该是最方便的方法。



# 相关资料

- [Ubuntu16.04下配置shadowsocks（亲测可用）](https://blog.csdn.net/mynameis121/article/details/70191057)
