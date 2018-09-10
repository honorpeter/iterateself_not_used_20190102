---
title: Python Tornado
toc: true
date: 2018-06-14 12:15:15
---


# Tornado

**Tornado全称叫Tornado Web Server**,

目前是Facebook开源的一个版本,它和其他主流的框架有一个非常明显的区别：

Tornado 是非阻塞式服务器，速度非常快。特别对于长轮询，WebSocket 等实时要求高的 web 服务来说是一个福音，基本可以和 Node.js 一决高下。

<span style="color:red;">这么厉害吗？长连接大部分用的是这个吗？好像很少看到使用的，也许一般的项目都不是长轮询的。还是要深入了解下的，毕竟计算机视觉中的图像传输和数据流等 还是需要很快的速度的。</span>

<span style="color:red;">另外，Node.js 真的这么厉害吗？</span>
