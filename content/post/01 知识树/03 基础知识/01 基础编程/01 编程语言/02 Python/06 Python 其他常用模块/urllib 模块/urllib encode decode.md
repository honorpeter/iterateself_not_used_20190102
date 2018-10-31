# 需要补充的

- 其实非常想知道，json 打包后，是不是就可以直接放在 url 中传递了？还需要 urlencode 来打包吗？
- 而且，为什么，我之前在网上用的一个在线的 urlencode 试了下，它的结果是：`aa="%7b%22img_name%22%3a+%22%5cu4e2d%5cu6587.jpg%22%2c%22is_check_black%22%3a+false%2c%22current_align_step%22%3a+0%7d"` 跟我的结果不一样。是为什么？
`

# 把 dict 打包成 json 然后 用 urlencode 加密



```python
from urllib import request
from urllib import parse
from urllib.request import urlopen
import urllib
import json

# 原始的数据
values = {'img_name': '中文.jpg',
          'is_check_black': False,
          'current_align_step': 0
          }

# 进行 json 化：
values_json_info = json.dumps(values,
                       sort_keys=False,
                       indent=4,
                       separators=(',', ': '))
print(values_json_info)

# 进行 urllib 加密：
encode_values_json_info = urllib.parse.quote(values_json_info)
print(encode_values_json_info)


decode_values_json_info=urllib.parse.unquote(encode_values_json_info)
print(decode_values_json_info)

info = json.loads(decode_values_json_info)
print(type(info))
print(info)
```


输出：

```
{
    "img_name": "\u4e2d\u6587.jpg",
    "is_check_black": false,
    "current_align_step": 0
}
%7B%0A%20%20%20%20%22img_name%22%3A%20%22%5Cu4e2d%5Cu6587.jpg%22%2C%0A%20%20%20%20%22is_check_black%22%3A%20false%2C%0A%20%20%20%20%22current_align_step%22%3A%200%0A%7D
{
    "img_name": "\u4e2d\u6587.jpg",
    "is_check_black": false,
    "current_align_step": 0
}
<class 'dict'>
{'img_name': '中文.jpg', 'is_check_black': False, 'current_align_step': 0}
```




# 相关资料

- [Python3中的urlencode和urldecode](https://blog.csdn.net/qq_39377696/article/details/80454950)
