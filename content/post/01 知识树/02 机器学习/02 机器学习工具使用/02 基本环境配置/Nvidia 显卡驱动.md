---
title: Nvidia 显卡驱动
toc: true
date: 2018-10-01
---
# 关于驱动与编译器版本的查询命令


1 首先验证你是否有nvidia的显卡（http://developer.nvidia.com/cuda-gpus 这个网站查看你是否有支持gpu的显卡）：

```
$ lspci | grep -i nvidia 
```

2,查看你的linux发行版本（主要是看是64位还是32位的）：

```
$ uname -m && cat /etc/*release
```

3,看一下gcc的版本：

```
$ gcc –version
```

4，查看NVIDIA显卡的驱动版本

```
$cat /proc/driver/nvidia/version
```

5，查看nvcc编译器的版本

```
nvcc -V i
```

6,/dev/nvidia*这里的文件代表了本机的NVIDIA显卡，如：

```
foo@bar-serv2:/dev$ ls -l nvidia*
crw-rw-rw- 1 root root 195, 0 Oct 24 18:51 nvidia0
crw-rw-rw- 1 root root 195, 1 Oct 24 18:51 nvidia1
crw-rw-rw- 1 root root 195, 255 Oct 24 18:50 nvidiactl
```

表示本机有两块NVIDIA显卡


7，查看显卡名称以及驱动版本


```
nvidia-smi
nvidia-smi -a
```




# 相关资料

- [关于驱动与编译器版本的查询命令](http://www.linuxdiyf.com/linux/16687.html)
- [深度学习（TensorFlow）环境搭建：（二）Ubuntu16.04+1080Ti显卡驱动](http://www.cnblogs.com/xuliangxing/p/7569946.html)
