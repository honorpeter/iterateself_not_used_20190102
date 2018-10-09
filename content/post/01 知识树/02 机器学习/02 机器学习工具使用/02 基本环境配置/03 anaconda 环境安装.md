anaconda 换源

这个还是必须要知道的

清华的源有的包速度非常慢，但是有的包速度非常快，现在暂时使用中科大的包.


清华的anaconda镜像挂了，用中科大的镜像吧
conda config –add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config –set show_channel_urls yes  

加个小tip:要删除 .condarc文件 。
.condarc以点开头，一般表示 conda 应用程序的配置文件，在用户的根目录
（windows：C:\users\username\，linux：/home/username/）。但对于.condarc配置文件，是一种可选的（optional）运行期配置文件，其默认情况下是不存在的。
当用户第一次运行 conda config命令时，将会在用户的家目录创建该文件。

---------------------

本文来自 rrr2 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/qq_35608277/article/details/78714401?utm_source=copy
