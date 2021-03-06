---
title: 03 Reshaping and Pivoting 整形和旋转
toc: true
date: 2018-07-08 13:32:45
---

# 8.3 Reshaping and Pivoting（整形和旋转）

> 8.1中的操作名
- join：连接
- combine：合并
- reshape：整形

> 8.2中的操作名
> - merge：归并
- concatenate：串联

> 8.3中的操作名
- pivot：旋转
- stack：堆叠

> 我在整个第八章对这些翻译做了更新，其他章节可能没有统一，如果有发现到不统一的翻译，可以在issue里提出，也可以直接pull request


有很多用于整理表格型数据的基本操作，指的就是reshape和pivot。

# 1 Reshaping with Hierarchical Indexing（对多层级索引进行整形）

多层级索引提供一套统一的方法来整理DataFrame中数据。主要有两个操作：

stack
- 这个操作会把列旋转为行

unstack
- 这个会把行变为列

下面我们会给出一些例子。这里有一个DataFrame，我们用字符串数组来作为行和列的索引：


```python
import numpy as np
import pandas as pd
```


```python
data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                    index=pd.Index(['Ohio', 'Colorado'], name='state'), 
                    columns=pd.Index(['one', 'two', 'three'], 
                    name='number'))
data
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>number</th>
      <th>one</th>
      <th>two</th>
      <th>three</th>
    </tr>
    <tr>
      <th>state</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Ohio</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Colorado</th>
      <td>3</td>
      <td>4</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



使用stack方法会把列数据变为行数据，产生一个Series：


```python
result = data.stack()
result
```




    state     number
    Ohio      one       0
              two       1
              three     2
    Colorado  one       3
              two       4
              three     5
    dtype: int64



对于一个有多层级索引的Series，可以用unstack把它变回DataFrame：


```python
result.unstack()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>number</th>
      <th>one</th>
      <th>two</th>
      <th>three</th>
    </tr>
    <tr>
      <th>state</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Ohio</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Colorado</th>
      <td>3</td>
      <td>4</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



默认会把最内层的层级unstack（取消堆叠），stack默认也是这样。我们可以传入一个表示层级的数字或名字，来指定取消堆叠某个层级：


```python
result.unstack(0)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>state</th>
      <th>Ohio</th>
      <th>Colorado</th>
    </tr>
    <tr>
      <th>number</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>one</th>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>two</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>three</th>
      <td>2</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>




```python
result.unstack('state')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>state</th>
      <th>Ohio</th>
      <th>Colorado</th>
    </tr>
    <tr>
      <th>number</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>one</th>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>two</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>three</th>
      <td>2</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



如果某个层级里的值不能在subgroup(子组)里找到的话，unstack可能会引入缺失值：


```python
s1 = pd.Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])

s2 = pd.Series([4, 5, 6], index=['c', 'd', 'e'])

data2 = pd.concat([s1, s2], keys=['one', 'two'])
```


```python
data2
```




    one  a    0
         b    1
         c    2
         d    3
    two  c    4
         d    5
         e    6
    dtype: int64




```python
data2.unstack()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
      <th>d</th>
      <th>e</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>one</th>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>two</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>6.0</td>
    </tr>
  </tbody>
</table>
</div>



stack默认会把缺失值过滤掉，所以这两种操作是可逆的：


```python
data2.unstack()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
      <th>d</th>
      <th>e</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>one</th>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>two</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>5.0</td>
      <td>6.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
data2.unstack().stack()
```




    one  a    0.0
         b    1.0
         c    2.0
         d    3.0
    two  c    4.0
         d    5.0
         e    6.0
    dtype: float64




```python
data2.unstack().stack(dropna=False)
```




    one  a    0.0
         b    1.0
         c    2.0
         d    3.0
         e    NaN
    two  a    NaN
         b    NaN
         c    4.0
         d    5.0
         e    6.0
    dtype: float64



如果对一个DataFrame使用unstack，被取消堆叠（unstack）的层级会变为结果中最低的层级：


```python
df = pd.DataFrame({'left': result, 'right': result + 5}, 
                  columns=pd.Index(['left', 'right'], name='side'))
df # 行的话，有state和number两个层级，number是内层级。而列的话有side这一个层级
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>side</th>
      <th>left</th>
      <th>right</th>
    </tr>
    <tr>
      <th>state</th>
      <th>number</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">Ohio</th>
      <th>one</th>
      <td>0</td>
      <td>5</td>
    </tr>
    <tr>
      <th>two</th>
      <td>1</td>
      <td>6</td>
    </tr>
    <tr>
      <th>three</th>
      <td>2</td>
      <td>7</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">Colorado</th>
      <th>one</th>
      <td>3</td>
      <td>8</td>
    </tr>
    <tr>
      <th>two</th>
      <td>4</td>
      <td>9</td>
    </tr>
    <tr>
      <th>three</th>
      <td>5</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.unstack('state')  # state被unstack后，变为比side更低的层级
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>side</th>
      <th colspan="2" halign="left">left</th>
      <th colspan="2" halign="left">right</th>
    </tr>
    <tr>
      <th>state</th>
      <th>Ohio</th>
      <th>Colorado</th>
      <th>Ohio</th>
      <th>Colorado</th>
    </tr>
    <tr>
      <th>number</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>one</th>
      <td>0</td>
      <td>3</td>
      <td>5</td>
      <td>8</td>
    </tr>
    <tr>
      <th>two</th>
      <td>1</td>
      <td>4</td>
      <td>6</td>
      <td>9</td>
    </tr>
    <tr>
      <th>three</th>
      <td>2</td>
      <td>5</td>
      <td>7</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>



调用stack的时候，可以指明想要stack（堆叠）哪一个轴：


```python
df.unstack('state').stack('side')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>state</th>
      <th>Ohio</th>
      <th>Colorado</th>
    </tr>
    <tr>
      <th>number</th>
      <th>side</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">one</th>
      <th>left</th>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>right</th>
      <td>5</td>
      <td>8</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">two</th>
      <th>left</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>right</th>
      <td>6</td>
      <td>9</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">three</th>
      <th>left</th>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>right</th>
      <td>7</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>



# 2 Pivoting “Long” to “Wide” Format（把“长”格式旋转为“宽”格式）

一种用来把多重时间序列数据存储在数据库和CSV中的格式叫long or stacked format（长格式或堆叠格式）。下面我们加载一些数据，处理一下时间序列文件并做一些数据清理工作：


```python
data = pd.read_csv('../examples/macrodata.csv')
data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>quarter</th>
      <th>realgdp</th>
      <th>realcons</th>
      <th>realinv</th>
      <th>realgovt</th>
      <th>realdpi</th>
      <th>cpi</th>
      <th>m1</th>
      <th>tbilrate</th>
      <th>unemp</th>
      <th>pop</th>
      <th>infl</th>
      <th>realint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1959.0</td>
      <td>1.0</td>
      <td>2710.349</td>
      <td>1707.4</td>
      <td>286.898</td>
      <td>470.045</td>
      <td>1886.9</td>
      <td>28.98</td>
      <td>139.7</td>
      <td>2.82</td>
      <td>5.8</td>
      <td>177.146</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1959.0</td>
      <td>2.0</td>
      <td>2778.801</td>
      <td>1733.7</td>
      <td>310.859</td>
      <td>481.301</td>
      <td>1919.7</td>
      <td>29.15</td>
      <td>141.7</td>
      <td>3.08</td>
      <td>5.1</td>
      <td>177.830</td>
      <td>2.34</td>
      <td>0.74</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1959.0</td>
      <td>3.0</td>
      <td>2775.488</td>
      <td>1751.8</td>
      <td>289.226</td>
      <td>491.260</td>
      <td>1916.4</td>
      <td>29.35</td>
      <td>140.5</td>
      <td>3.82</td>
      <td>5.3</td>
      <td>178.657</td>
      <td>2.74</td>
      <td>1.09</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1959.0</td>
      <td>4.0</td>
      <td>2785.204</td>
      <td>1753.7</td>
      <td>299.356</td>
      <td>484.052</td>
      <td>1931.3</td>
      <td>29.37</td>
      <td>140.0</td>
      <td>4.33</td>
      <td>5.6</td>
      <td>179.386</td>
      <td>0.27</td>
      <td>4.06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1960.0</td>
      <td>1.0</td>
      <td>2847.699</td>
      <td>1770.5</td>
      <td>331.722</td>
      <td>462.199</td>
      <td>1955.5</td>
      <td>29.54</td>
      <td>139.6</td>
      <td>3.50</td>
      <td>5.2</td>
      <td>180.007</td>
      <td>2.31</td>
      <td>1.19</td>
    </tr>
  </tbody>
</table>
</div>




```python
periods = pd.PeriodIndex(year=data.year, quarter=data.quarter,
                         name='date')
```


```python
columns = pd.Index(['realgdp', 'infl', 'unemp'], name='item')
```


```python
data = data.reindex(columns=columns)
```


```python
data.index = periods.to_timestamp('D', 'end')
```


```python
ldata = data.stack().reset_index().rename(columns={0: 'value'})
```

对于PeriodIndex，我们会在第十一章讲得更详细些。在这里，这个函数把year和quarter这两列整合起来作为一种时间间隔类型。

ldata看起来是这样的：


```python
ldata[:10]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>item</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1959-03-31</td>
      <td>realgdp</td>
      <td>2710.349</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1959-03-31</td>
      <td>infl</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1959-03-31</td>
      <td>unemp</td>
      <td>5.800</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1959-06-30</td>
      <td>realgdp</td>
      <td>2778.801</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1959-06-30</td>
      <td>infl</td>
      <td>2.340</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1959-06-30</td>
      <td>unemp</td>
      <td>5.100</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1959-09-30</td>
      <td>realgdp</td>
      <td>2775.488</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1959-09-30</td>
      <td>infl</td>
      <td>2.740</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1959-09-30</td>
      <td>unemp</td>
      <td>5.300</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1959-12-31</td>
      <td>realgdp</td>
      <td>2785.204</td>
    </tr>
  </tbody>
</table>
</div>



这种格式叫做long format for multiple time series（用于多重时间序列的长格式），或者有两个以上键（keys）的观测数据（在这个例子里，keys指的是date和item）。表格中的每一行表示一个观测数据。

这种数据经常被存储于关系型数据库中，比如MySQL，这种固定的模式（列名和数据类型）能让作为item列中不同的数据，添加到表格中。在前一个例子里，date和item通常被用来当做primary keys（主键，这是关系型数据库里的术语），能实现relational integrity（关系完整性）和更方便的join（联结）。但是在一些例子里，这种格式的数据并不好处理；我们可能更喜欢有一个DataFrame，其中一列能有不同的item值，并用date列作为索引。DataFrame中的pivot方法，就能做到这种转换：


```python
pivoted = ldata.pivot('date', 'item', 'value')
pivoted
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>item</th>
      <th>infl</th>
      <th>realgdp</th>
      <th>unemp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1959-03-31</th>
      <td>0.00</td>
      <td>2710.349</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>1959-06-30</th>
      <td>2.34</td>
      <td>2778.801</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>1959-09-30</th>
      <td>2.74</td>
      <td>2775.488</td>
      <td>5.3</td>
    </tr>
    <tr>
      <th>1959-12-31</th>
      <td>0.27</td>
      <td>2785.204</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>1960-03-31</th>
      <td>2.31</td>
      <td>2847.699</td>
      <td>5.2</td>
    </tr>
    <tr>
      <th>1960-06-30</th>
      <td>0.14</td>
      <td>2834.390</td>
      <td>5.2</td>
    </tr>
    <tr>
      <th>1960-09-30</th>
      <td>2.70</td>
      <td>2839.022</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>1960-12-31</th>
      <td>1.21</td>
      <td>2802.616</td>
      <td>6.3</td>
    </tr>
    <tr>
      <th>1961-03-31</th>
      <td>-0.40</td>
      <td>2819.264</td>
      <td>6.8</td>
    </tr>
    <tr>
      <th>1961-06-30</th>
      <td>1.47</td>
      <td>2872.005</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>1961-09-30</th>
      <td>0.80</td>
      <td>2918.419</td>
      <td>6.8</td>
    </tr>
    <tr>
      <th>1961-12-31</th>
      <td>0.80</td>
      <td>2977.830</td>
      <td>6.2</td>
    </tr>
    <tr>
      <th>1962-03-31</th>
      <td>2.26</td>
      <td>3031.241</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>1962-06-30</th>
      <td>0.13</td>
      <td>3064.709</td>
      <td>5.5</td>
    </tr>
    <tr>
      <th>1962-09-30</th>
      <td>2.11</td>
      <td>3093.047</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>1962-12-31</th>
      <td>0.79</td>
      <td>3100.563</td>
      <td>5.5</td>
    </tr>
    <tr>
      <th>1963-03-31</th>
      <td>0.53</td>
      <td>3141.087</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>1963-06-30</th>
      <td>2.75</td>
      <td>3180.447</td>
      <td>5.7</td>
    </tr>
    <tr>
      <th>1963-09-30</th>
      <td>0.78</td>
      <td>3240.332</td>
      <td>5.5</td>
    </tr>
    <tr>
      <th>1963-12-31</th>
      <td>2.46</td>
      <td>3264.967</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>1964-03-31</th>
      <td>0.13</td>
      <td>3338.246</td>
      <td>5.5</td>
    </tr>
    <tr>
      <th>1964-06-30</th>
      <td>0.90</td>
      <td>3376.587</td>
      <td>5.2</td>
    </tr>
    <tr>
      <th>1964-09-30</th>
      <td>1.29</td>
      <td>3422.469</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>1964-12-31</th>
      <td>2.05</td>
      <td>3431.957</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>1965-03-31</th>
      <td>1.28</td>
      <td>3516.251</td>
      <td>4.9</td>
    </tr>
    <tr>
      <th>1965-06-30</th>
      <td>2.54</td>
      <td>3563.960</td>
      <td>4.7</td>
    </tr>
    <tr>
      <th>1965-09-30</th>
      <td>0.89</td>
      <td>3636.285</td>
      <td>4.4</td>
    </tr>
    <tr>
      <th>1965-12-31</th>
      <td>2.90</td>
      <td>3724.014</td>
      <td>4.1</td>
    </tr>
    <tr>
      <th>1966-03-31</th>
      <td>4.99</td>
      <td>3815.423</td>
      <td>3.9</td>
    </tr>
    <tr>
      <th>1966-06-30</th>
      <td>2.10</td>
      <td>3828.124</td>
      <td>3.8</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2002-06-30</th>
      <td>1.56</td>
      <td>11538.770</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>2002-09-30</th>
      <td>2.66</td>
      <td>11596.430</td>
      <td>5.7</td>
    </tr>
    <tr>
      <th>2002-12-31</th>
      <td>3.08</td>
      <td>11598.824</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>2003-03-31</th>
      <td>1.31</td>
      <td>11645.819</td>
      <td>5.9</td>
    </tr>
    <tr>
      <th>2003-06-30</th>
      <td>1.09</td>
      <td>11738.706</td>
      <td>6.2</td>
    </tr>
    <tr>
      <th>2003-09-30</th>
      <td>2.60</td>
      <td>11935.461</td>
      <td>6.1</td>
    </tr>
    <tr>
      <th>2003-12-31</th>
      <td>3.02</td>
      <td>12042.817</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>2004-03-31</th>
      <td>2.35</td>
      <td>12127.623</td>
      <td>5.7</td>
    </tr>
    <tr>
      <th>2004-06-30</th>
      <td>3.61</td>
      <td>12213.818</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>2004-09-30</th>
      <td>3.58</td>
      <td>12303.533</td>
      <td>5.4</td>
    </tr>
    <tr>
      <th>2004-12-31</th>
      <td>2.09</td>
      <td>12410.282</td>
      <td>5.4</td>
    </tr>
    <tr>
      <th>2005-03-31</th>
      <td>4.15</td>
      <td>12534.113</td>
      <td>5.3</td>
    </tr>
    <tr>
      <th>2005-06-30</th>
      <td>1.85</td>
      <td>12587.535</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>2005-09-30</th>
      <td>9.14</td>
      <td>12683.153</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>2005-12-31</th>
      <td>0.40</td>
      <td>12748.699</td>
      <td>4.9</td>
    </tr>
    <tr>
      <th>2006-03-31</th>
      <td>2.60</td>
      <td>12915.938</td>
      <td>4.7</td>
    </tr>
    <tr>
      <th>2006-06-30</th>
      <td>3.97</td>
      <td>12962.462</td>
      <td>4.7</td>
    </tr>
    <tr>
      <th>2006-09-30</th>
      <td>-1.58</td>
      <td>12965.916</td>
      <td>4.7</td>
    </tr>
    <tr>
      <th>2006-12-31</th>
      <td>3.30</td>
      <td>13060.679</td>
      <td>4.4</td>
    </tr>
    <tr>
      <th>2007-03-31</th>
      <td>4.58</td>
      <td>13099.901</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>2007-06-30</th>
      <td>2.75</td>
      <td>13203.977</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>2007-09-30</th>
      <td>3.45</td>
      <td>13321.109</td>
      <td>4.7</td>
    </tr>
    <tr>
      <th>2007-12-31</th>
      <td>6.38</td>
      <td>13391.249</td>
      <td>4.8</td>
    </tr>
    <tr>
      <th>2008-03-31</th>
      <td>2.82</td>
      <td>13366.865</td>
      <td>4.9</td>
    </tr>
    <tr>
      <th>2008-06-30</th>
      <td>8.53</td>
      <td>13415.266</td>
      <td>5.4</td>
    </tr>
    <tr>
      <th>2008-09-30</th>
      <td>-3.16</td>
      <td>13324.600</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>2008-12-31</th>
      <td>-8.79</td>
      <td>13141.920</td>
      <td>6.9</td>
    </tr>
    <tr>
      <th>2009-03-31</th>
      <td>0.94</td>
      <td>12925.410</td>
      <td>8.1</td>
    </tr>
    <tr>
      <th>2009-06-30</th>
      <td>3.37</td>
      <td>12901.504</td>
      <td>9.2</td>
    </tr>
    <tr>
      <th>2009-09-30</th>
      <td>3.56</td>
      <td>12990.341</td>
      <td>9.6</td>
    </tr>
  </tbody>
</table>
<p>203 rows × 3 columns</p>
</div>



前两个传入的值是列，分别被用于作为行索引和列索引（date是行索引，item是列索引），最后是一个是可选的value column（值列），用于填充DataFrame。假设我们有两列值，我们想要同时整形：


```python
ldata['value2'] = np.random.randn(len(ldata))
ldata[:10]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>item</th>
      <th>value</th>
      <th>value2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1959-03-31</td>
      <td>realgdp</td>
      <td>2710.349</td>
      <td>0.284176</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1959-03-31</td>
      <td>infl</td>
      <td>0.000</td>
      <td>-1.428019</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1959-03-31</td>
      <td>unemp</td>
      <td>5.800</td>
      <td>-1.238330</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1959-06-30</td>
      <td>realgdp</td>
      <td>2778.801</td>
      <td>0.144937</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1959-06-30</td>
      <td>infl</td>
      <td>2.340</td>
      <td>-0.553085</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1959-06-30</td>
      <td>unemp</td>
      <td>5.100</td>
      <td>-0.833374</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1959-09-30</td>
      <td>realgdp</td>
      <td>2775.488</td>
      <td>0.147826</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1959-09-30</td>
      <td>infl</td>
      <td>2.740</td>
      <td>-0.059040</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1959-09-30</td>
      <td>unemp</td>
      <td>5.300</td>
      <td>0.531887</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1959-12-31</td>
      <td>realgdp</td>
      <td>2785.204</td>
      <td>-0.169839</td>
    </tr>
  </tbody>
</table>
</div>



舍弃最后一个参数，我们能得到一个有多层级列的DataFrame：


```python
pivoted = ldata.pivot('date', 'item')
pivoted[:5]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">value</th>
      <th colspan="3" halign="left">value2</th>
    </tr>
    <tr>
      <th>item</th>
      <th>infl</th>
      <th>realgdp</th>
      <th>unemp</th>
      <th>infl</th>
      <th>realgdp</th>
      <th>unemp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1959-03-31</th>
      <td>0.00</td>
      <td>2710.349</td>
      <td>5.8</td>
      <td>-1.428019</td>
      <td>0.284176</td>
      <td>-1.238330</td>
    </tr>
    <tr>
      <th>1959-06-30</th>
      <td>2.34</td>
      <td>2778.801</td>
      <td>5.1</td>
      <td>-0.553085</td>
      <td>0.144937</td>
      <td>-0.833374</td>
    </tr>
    <tr>
      <th>1959-09-30</th>
      <td>2.74</td>
      <td>2775.488</td>
      <td>5.3</td>
      <td>-0.059040</td>
      <td>0.147826</td>
      <td>0.531887</td>
    </tr>
    <tr>
      <th>1959-12-31</th>
      <td>0.27</td>
      <td>2785.204</td>
      <td>5.6</td>
      <td>-0.436330</td>
      <td>-0.169839</td>
      <td>-0.203380</td>
    </tr>
    <tr>
      <th>1960-03-31</th>
      <td>2.31</td>
      <td>2847.699</td>
      <td>5.2</td>
      <td>1.038559</td>
      <td>0.644242</td>
      <td>-1.872500</td>
    </tr>
  </tbody>
</table>
</div>




```python
pivoted['value'][:5]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>item</th>
      <th>infl</th>
      <th>realgdp</th>
      <th>unemp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1959-03-31</th>
      <td>0.00</td>
      <td>2710.349</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>1959-06-30</th>
      <td>2.34</td>
      <td>2778.801</td>
      <td>5.1</td>
    </tr>
    <tr>
      <th>1959-09-30</th>
      <td>2.74</td>
      <td>2775.488</td>
      <td>5.3</td>
    </tr>
    <tr>
      <th>1959-12-31</th>
      <td>0.27</td>
      <td>2785.204</td>
      <td>5.6</td>
    </tr>
    <tr>
      <th>1960-03-31</th>
      <td>2.31</td>
      <td>2847.699</td>
      <td>5.2</td>
    </tr>
  </tbody>
</table>
</div>



这里pivot相当于用set_index创建了一个多层级用里，并调用了unstack：


```python
unstacked = ldata.set_index(['date', 'item']).unstack('item')
unstacked[:7]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">value</th>
      <th colspan="3" halign="left">value2</th>
    </tr>
    <tr>
      <th>item</th>
      <th>infl</th>
      <th>realgdp</th>
      <th>unemp</th>
      <th>infl</th>
      <th>realgdp</th>
      <th>unemp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1959-03-31</th>
      <td>0.00</td>
      <td>2710.349</td>
      <td>5.8</td>
      <td>-1.428019</td>
      <td>0.284176</td>
      <td>-1.238330</td>
    </tr>
    <tr>
      <th>1959-06-30</th>
      <td>2.34</td>
      <td>2778.801</td>
      <td>5.1</td>
      <td>-0.553085</td>
      <td>0.144937</td>
      <td>-0.833374</td>
    </tr>
    <tr>
      <th>1959-09-30</th>
      <td>2.74</td>
      <td>2775.488</td>
      <td>5.3</td>
      <td>-0.059040</td>
      <td>0.147826</td>
      <td>0.531887</td>
    </tr>
    <tr>
      <th>1959-12-31</th>
      <td>0.27</td>
      <td>2785.204</td>
      <td>5.6</td>
      <td>-0.436330</td>
      <td>-0.169839</td>
      <td>-0.203380</td>
    </tr>
    <tr>
      <th>1960-03-31</th>
      <td>2.31</td>
      <td>2847.699</td>
      <td>5.2</td>
      <td>1.038559</td>
      <td>0.644242</td>
      <td>-1.872500</td>
    </tr>
    <tr>
      <th>1960-06-30</th>
      <td>0.14</td>
      <td>2834.390</td>
      <td>5.2</td>
      <td>0.765028</td>
      <td>-0.835805</td>
      <td>2.014334</td>
    </tr>
    <tr>
      <th>1960-09-30</th>
      <td>2.70</td>
      <td>2839.022</td>
      <td>5.6</td>
      <td>0.168310</td>
      <td>0.362230</td>
      <td>1.603777</td>
    </tr>
  </tbody>
</table>
</div>



# 3 Pivoting “Wide” to “Long” Format（把“宽”格式旋转为“长”格式）

用于DataFrame，与pivot相反的操作是pandas.melt。相对于把一列变为多列的pivot，melt会把多列变为一列，产生一个比输入的DataFrame还要长的结果。看一下例子：


```python
df = pd.DataFrame({'key': ['foo', 'bar', 'baz'], 
                   'A': [1, 2, 3], 
                   'B': [4, 5, 6], 
                   'C': [7, 8, 9]})
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>key</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4</td>
      <td>7</td>
      <td>foo</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>5</td>
      <td>8</td>
      <td>bar</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>6</td>
      <td>9</td>
      <td>baz</td>
    </tr>
  </tbody>
</table>
</div>



'key'列可以作为group indicator（群指示器），其他列可以作为数据值。当使用pandas.melt，我们必须指明哪些列是群指示器。这里我们令key作为群指示器：


```python
melted = pd.melt(df, ['key'])
melted
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>variable</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bar</td>
      <td>A</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>baz</td>
      <td>A</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>foo</td>
      <td>B</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>bar</td>
      <td>B</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>baz</td>
      <td>B</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>foo</td>
      <td>C</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>bar</td>
      <td>C</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>baz</td>
      <td>C</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>



使用pivot，我们可以得到原来的布局：


```python
reshaped = melted.pivot('key', 'variable', 'value')
reshaped
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>variable</th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
    <tr>
      <th>key</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>bar</th>
      <td>2</td>
      <td>5</td>
      <td>8</td>
    </tr>
    <tr>
      <th>baz</th>
      <td>3</td>
      <td>6</td>
      <td>9</td>
    </tr>
    <tr>
      <th>foo</th>
      <td>1</td>
      <td>4</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>



因为pivot会给行标签创建一个索引（key列），所以这里我们要用reset_index来让数据变回去：


```python
reshaped.reset_index()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>variable</th>
      <th>key</th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bar</td>
      <td>2</td>
      <td>5</td>
      <td>8</td>
    </tr>
    <tr>
      <th>1</th>
      <td>baz</td>
      <td>3</td>
      <td>6</td>
      <td>9</td>
    </tr>
    <tr>
      <th>2</th>
      <td>foo</td>
      <td>1</td>
      <td>4</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
</div>



当然，我们也可以在使用melt的时候指定哪些列用于值：


```python
pd.melt(df, id_vars=['key'], value_vars=['A', 'B'])
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>variable</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bar</td>
      <td>A</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>baz</td>
      <td>A</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>foo</td>
      <td>B</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>bar</td>
      <td>B</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>baz</td>
      <td>B</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



pandas.melt也能在没有群指示器的情况下使用：


```python
pd.melt(df, value_vars=['A', 'B', 'C'])
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>variable</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>C</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>C</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.melt(df, value_vars=['key','A', 'B'])
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>variable</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>key</td>
      <td>foo</td>
    </tr>
    <tr>
      <th>1</th>
      <td>key</td>
      <td>bar</td>
    </tr>
    <tr>
      <th>2</th>
      <td>key</td>
      <td>baz</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>A</td>
      <td>3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>B</td>
      <td>4</td>
    </tr>
    <tr>
      <th>7</th>
      <td>B</td>
      <td>5</td>
    </tr>
    <tr>
      <th>8</th>
      <td>B</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>





