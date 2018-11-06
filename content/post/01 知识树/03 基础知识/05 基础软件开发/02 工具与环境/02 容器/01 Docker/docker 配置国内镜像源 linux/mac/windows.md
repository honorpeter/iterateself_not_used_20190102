# 需要补充的

- 这个是不是所有的镜像都在上面？



# docker 配置国内镜像源 linux/mac/windows




> 部分内容来自：[http://guide.daocloud.io/dcs/daocloud-9153151.html](https://link.jianshu.com?t=http://guide.daocloud.io/dcs/daocloud-9153151.html)
> 加速器官方DaoCloud承诺：加速器服务永久免费且无流量限制
> **使用前提：**[注册DaoCloud账号](https://link.jianshu.com?t=https://account.daocloud.io/signin) 并 确保Docker 版本 > 1.8
> 命令`docker --version`

使用 Docker 需要经常从官方获取镜像，国内拉取镜像的过程非常耗时。

DaoCloud 推出[DaoCloud 加速器](https://link.jianshu.com?t=https://www.daocloud.io/mirror) ，通过智能路由和缓存机制，极大提升了国内网络访问 Docker Hub 的速度，并得到了 Docker 官方的大力推荐。

### linux

自动配置 Docker 加速器（推荐）
 *适用于 Ubuntu14.04、Debian、CentOS6 、CentOS7、Fedora、Arch Linux、openSUSE Leap 42.1*

[registry-mirror配置命令](https://link.jianshu.com?t=https://www.daocloud.io/mirror#accelerator-doc)  如下（注意修改为自己的地址）：

```
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://你的的地址.m.daocloud.io
```

**在配置完成后根据终端中的提示重启 docker使配置生效。**

手动配置 Docker 加速器
 Docker 版本在 1.8 - 1.11
 找到 Docker 配置文件，不同的 Linux 发行版的配置路径不同，具体路径请参考 [Docker官方文档](https://link.jianshu.com?t=https://docs.docker.com/engine/admin/)
 在配置文件中的 DOCKER_OPTS 加入

```
--registry-mirror=你的加速地址
```

重启Docker（不同的 Linux 发行版的重启命令不一定相同）
 `service docker restart`

### Docker for Mac

获取[加速地址](https://link.jianshu.com?t=https://www.daocloud.io/mirror#accelerator-doc)
 操作如图所示
 点击 Apply & Restart 按钮使设置生效




![img](https:////upload-images.jianshu.io/upload_images/2795885-4ffcb0c48c005ae2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/330/format/webp)





![img](https:////upload-images.jianshu.io/upload_images/2795885-18216c0a9772aa4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/378/format/webp)



建议加入其他国内镜像



```
https://docker.mirrors.ustc.edu.cn
https://hub-mirror.c.163.com
```

### Docker for Windows

在桌面右下角状态栏中右键 docker 图标，修改在 Docker Daemon 标签页中的 json ，把 加速地址(在[加速器](https://link.jianshu.com?t=https://www.daocloud.io/mirror#accelerator-doc)页面获取)加到"registry-mirrors"的数组里。点击 Apply 使设置生效。
 如图所示




![img](https:////upload-images.jianshu.io/upload_images/2795885-595dd1726679ad2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/519/format/webp)





注意!
 上方的文本为 json 语法，请确定您的修改符合语法规则，否则将无法配置成功。

### Docker Toolbox

（不推荐使用 docker toolbox，建议使用新的 docker for mac 及 docker for windows 以在这两种平台运行 docker ）
 请确认你的 Docker Toolbox 已经启动，并执行下列命令（请将 **加速地址** 替换为在[加速器](https://link.jianshu.com?t=https://www.daocloud.io/mirror#accelerator-doc)页面获取的专属地址）

```
docker-machine ssh defaultsudo sed -i "s|EXTRA_ARGS='|EXTRA_ARGS='--registry-mirror=加速地址 |g" /var/lib/boot2docker/profileexitdocker-machine restart default
```




# 相关资料

- [docker 配置国内镜像源 linux/mac/windows](https://www.jianshu.com/p/9fce6e583669)
- [Docker 加速器](https://www.daocloud.io/mirror#accelerator-doc)
