---
title: 02 Docker 安装
toc: true
date: 2018-08-01 18:37:12
---



## 相关资料

1. [Docker简单使用指南](https://www.w3cschool.cn/use_docker/)




## 需要补充的






  * aaa




# MOTIVE






  * aaa





* * *



照着官方文档 [http://docs.docker.com/installation/ubuntulinux/](http://docs.docker.com/installation/ubuntulinux/) 做吧.

一般就是:




  * 更新工具:




    $ sudo apt-get update
    $ sudo apt-get install apt-transport-https ca-certificates







  * 添加软件源的 KEY:




    $ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 \
                       --recv-keys 58118E89F3A912897C070ADBF76221572C52609D







  * 添加软件源:


<table >
<tbody >
<tr >
Ubuntu version
Repository
</tr>
<tr >

<td >Precise 12.04 (LTS)
</td>

<td >`deb https://apt.dockerproject.org/repo ubuntu-precise main`
</td>
</tr>
<tr >

<td >Trusty 14.04 (LTS)
</td>

<td >`deb https://apt.dockerproject.org/repo ubuntu-trusty main`
</td>
</tr>
<tr >

<td >Xenial 16.04 (LTS)
</td>

<td >`deb https://apt.dockerproject.org/repo ubuntu-xenial main`
</td>
</tr>
</tbody>
</table>




  * 更新源列表并安装:




    $ sudo apt-get update
    $ sudo apt-get install docker-engine



安装完成之后, 有一个 `docker` 命令可供使用. 同时, `docker` 的服务默认监听在一个 **sock** 文件上(这样除了命令行工具, 各语言的 API 都很容易实现了).

权限方面, `docker` 的功能限制于 root 用户, docker 用户组. 所以, 你要么带着 `sudo` 用, 要么把当前用户加入到 docker 组:


    $ sudo groupadd docker
    $ sudo gpasswd -a zys docker



重启一下系统吧.

最后, 先安装一个可用的"镜像":


    docker pull ubuntu:14.04



这可能需要一点时间, 也可能因为 GFW 的影响而不容易安装成功.

然后作一个 `Hello World` :


    docker run ubuntu:14.04 echo "Hello World"



安装成功.























* * *





# COMMENT
