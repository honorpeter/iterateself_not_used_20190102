# 需要补充的

- 还是要自己运行下的

## 1.利用pandas进行数据分析+matplot进行可视化

```py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = np.random.rand(10,4)
df = pd.DataFrame(data,columns = list("ABCD"),index=np.arange(0,100,10))
df.plot()
plt.show()
```

上面一段代码的运行结果如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/bdeq69kxnz.png?imageView2/2/w/1620)



## 2.

```py
fig, axes = plt.subplots(2,1)
data = pd.Series(np.random.randn(16),index=list("abcdefghijklmnop"))
data.plot(kind='bar', ax=axes[0], color='k',alpha=0.7)
data.plot(kind='barh', ax=axes[1], color='r', alpha=0.7)
plt.show()
```

上面一段代码的运行结果如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/0qii9u08d2.png?imageView2/2/w/1620)

image.png

## 3.折线图

```py
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("pandas-matplotlib.xlsx")
var = df.groupby('BMI').Sales.sum()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('BMI')
ax.set_ylabel('Sum of Sales')
ax.set_title('BMI while Sum of Sales')
var.plot(kind='line')
plt.show()
```

上面一段代码的运行结果如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/bwbgl425jd.png?imageView2/2/w/1620)

image.png

## 4.条形图

```py
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("pandas-matplotlib.xlsx")
```

上面一段代码的运行结果如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/sx4rbojwct.png?imageView2/2/w/1620)

image.png

## 5.柱状堆积图

```py
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("pandas-matplotlib.xlsx")
var = df.groupby(["BMI","Gender"]).Sales.sum()
var.unstack().plot(kind='bar',stacked=True,color=['red','blue'])
plt.show()
```

上面一段代码的运行结果如下：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/qmedv4rd61.png?imageView2/2/w/1620)

image.png

## 6.绘制散点图

```py
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("pandas-matplotlib.xlsx")
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(df['Age'],df['Sales'])
plt.show()
```

上面一段代码的运行结果如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/5yu40csesq.png?imageView2/2/w/1620)

image.png

## 7.绘制气泡图

```py
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("pandas-matplotlib.xlsx")
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(df['Age'],df['Sales'],s=df['Income'])
plt.show()
```

上面一段代码的运行结果如下图所示：

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/l9f7syj4yp.png?imageView2/2/w/1620)

image.png

## 8.

```py
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("pandas-matplotlib.xlsx")
var = df.groupby(['Gender']).sum().stack()
temp =var.unstack()
x_list = temp['Sales']
label_list = temp.index
plt.axis('equal')
plt.pie(x_list,labels=label_list,autopct='%1.1f%%')
plt.title('experience')
plt.show()
```

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/904buibry8.png?imageView2/2/w/1620)

image.png

# 2.PyEcharts画图

```py
pip install pyecharts -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

## 2,1

```py
import pyecharts as pye
bar = pye.Bar("我的第一个图表","这里是副标题")
x = ["衬衫", "羊毛衫", "雪纺衫","裤子", "高跟鞋", "袜子"]
y = [5, 20, 36, 10, 75, 90]
label = '服装'
bar.add(label,x,y)
bar.render('bar01.html')
```

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/q2gmeeywij.png?imageView2/2/w/1620)

image.png

![img](https://ask.qcloudimg.com/http-save/yehe-2318291/rmsil93o6p.png?imageView2/2/w/1620)



# 相关资料

- [Matplotlib进阶](https://cloud.tencent.com/developer/article/1331932)
