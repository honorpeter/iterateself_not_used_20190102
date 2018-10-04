---
title: Error sudo unable to resolve host xxx
toc: true
date: 2018-10-04
---
# 需要补充的

- 对于 sudo 还是有点不是很清楚。


# Error message 'sudo: unable to resolve host <USER>'

这个问题在使用 sudo 的时候出现的，应该是我之前在设置里面把 机器的名字改了，但是 hosts 里面还没有反应过来，所以 sudo 没有找。


## 解决办法

Two things to check (assuming your machine is called `my-machine`, you can change this as appropriate):

1. That the `/etc/hostname` file contains just the name of the machine.

2. That `/etc/hosts` has an entry for `localhost`. It should have something like:

   ```
    127.0.0.1    localhost.localdomain localhost
    127.0.1.1    my-machine
   ```

If either of these files aren't correct (since you can't sudo), you may have to reboot the machine into recovery mode and make the modifications, then reboot to your usual environment.



# 相关资料


- [Error message 'sudo: unable to resolve host <USER>'](https://askubuntu.com/questions/59458/error-message-sudo-unable-to-resolve-host-user)
