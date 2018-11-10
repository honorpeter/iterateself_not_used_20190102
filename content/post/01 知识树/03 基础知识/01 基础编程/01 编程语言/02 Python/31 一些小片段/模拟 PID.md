---
title: 模拟 PID
toc: true
date: 2018-11-10
---
# Python 模拟 PID

之前，想模拟一个东西的运动到的位置，但是后来发现我相差了，实际上，这个与PID 没啥关系，而是单纯的回归的方式进行拟合。

对于这个 PID，以前学习过，但是基本都忘记了，现在还是把这个代码记一下：

pid.py 如下：

```py
# PID控制一阶惯性系统测试程序




# 增量式PID系统
class IncrementalPID:
    def __init__(self, p, i, d):
        self.kp = p
        self.ki = i
        self.kd = d

        self.pid_output = 0.0  # PID控制器输出
        self.system_output = 0.0  # 系统输出值
        self.last_system_output = 0.0  # 上次系统输出值

        self.error = 0.0  # 输出值与输入值的偏差
        self.last_error = 0.0
        self.last_last_error = 0.0

    # 设置一阶惯性环节系统  其中InertiaTime为惯性时间常数
    def set_inertia_time(self, inertia_time, sample_time):
        self.system_output = (inertia_time * self.last_system_output + sample_time * self.pid_output) / (
            sample_time + inertia_time)
        self.last_system_output = self.system_output

    # 设置PID控制器参数
    def set_step_signal(self, step_signal):
        self.error = step_signal - self.system_output
        increment_value = self.kp * (self.error - self.last_error) + self.ki * self.error + self.kd * (
            self.error - 2 * self.last_error + self.last_last_error)
        self.pid_output += increment_value
        self.last_last_error = self.last_error
        self.last_error = self.error


# 位置式PID系统
class PositionalPID:
    def __init__(self, p, i, d):
        self.kp = p
        self.ki = i
        self.kd = d

        self.system_output = 0.0
        self.result_value_back = 0.0
        self.pid_output = 0.0
        self.pid_error_add = 0.0
        self.err_back = 0.0

    def set_inertia_time(self, inertia_time, sample_time):
        self.system_output = (inertia_time * self.result_value_back + sample_time * self.pid_output) / (
            sample_time + inertia_time)
        self.result_value_back = self.system_output

    def set_step_signal(self, step_signal):
        err = step_signal - self.system_output
        kp_work = self.kp * err
        ki_work = self.ki * self.pid_error_add
        kd_work = self.kd * (err - self.err_back)
        self.pid_output = kp_work + ki_work + kd_work
        self.pid_error_add += err
        self.err_back = err

```



调用：

pid_simu.py 如下：

```py
from pid import IncrementalPID,PositionalPID
import matplotlib.pyplot as plt

plt.figure(1)  # 创建图表1
plt.figure(2)  # 创建图表2


# 测试PID程序
def try_pid(p, i, d):
    incremental_pid = IncrementalPID(p, i, d)
    positional_pid = PositionalPID(p, i, d)
    incremental_xaxis = [0]
    incremental_yaxis = [0]
    positional_xaxis = [0]
    positional_yaxis = [0]

    for i in range(1, 500):
        # 增量式
        incremental_pid.set_step_signal(100.2)
        incremental_pid.set_inertia_time(3, 0.1)
        incremental_yaxis.append(incremental_pid.system_output)
        incremental_xaxis.append(i)

        # 位置式
        positional_pid.set_step_signal(100.2)
        positional_pid.set_inertia_time(3, 0.1)
        positional_yaxis.append(positional_pid.system_output)
        positional_xaxis.append(i)

    plt.figure(1)  # 选择图表1
    plt.plot(incremental_xaxis, incremental_yaxis, 'r')
    plt.xlim(0, 120)
    plt.ylim(0, 140)
    plt.title("IncrementalPID")

    plt.figure(2)  # 选择图表2
    plt.plot(positional_xaxis, positional_yaxis, 'b')
    plt.xlim(0, 120)
    plt.ylim(0, 140)
    plt.title("PositionalPID")

    plt.show()


if __name__ == "__main__":
    try_pid(4.5, 0.5, 0.1)

```
