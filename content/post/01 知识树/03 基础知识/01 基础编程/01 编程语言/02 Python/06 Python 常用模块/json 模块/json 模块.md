---
title: json 模块
toc: true
date: 2018-10-31
---

# 读取和写入 json 文件

```python
import json

def generate_json():

    json_info = json.dumps({
        'img_folder': "./img_origin",
        'x_precise': 0.5,
        'y1_precise': 0.5,
        'y2_precise': 0.5,

        'x_inertia': 2,
        'y1_inertia': 2,
        'y2_inertia': 2,
    }, sort_keys=False, indent=4, separators=(',', ': '))

    with open('config.json', 'w') as f:
        f.write(json_info)


def read_json_config():
    with open('config.json', 'r') as f:
        content = f.read()
    info = json.loads(content)
    print(type(info))
    print(info)
    img_folder = info["img_folder"]
    x_precise = float(info["x_precise"])
    y1_precise = float(info['y1_precise'])
    y2_precise = float(info['y2_precise'])
    x_inertia = float(info['x_inertia'])
    y1_inertia = float(info['y1_inertia'])
    y2_inertia = float(info['y2_inertia'])


if __name__ == "__main__":
    generate_json()
    read_json_config()
```



输出的 json 文件是：

```json
{
    "img_folder": "./img_origin",
    "x_precise": 0.5,
    "y1_precise": 0.5,
    "y2_precise": 0.5,
    "x_inertia": 2,
    "y1_inertia": 2,
    "y2_inertia": 2
}
```
