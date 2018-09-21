---
title: bbox_labeling
toc: true
date: 2018-09-02
---
# 需要补充的

- 要把 《深度学习与计算机视觉》第六章中的内容总结到这里，这里只是先占在这里，因为目标检测算法 的 MXNet 的实现的例子里讲到了要制作自己的标注数据。



这个是把通过小工具标注的信息转化为 PASCAL VOC 格式的信息：

detection_anno_bbox2voc.py：

```python
import os
import sys
import xml.etree.ElementTree as ET
#import xml.dom.minidom as minidom
import cv2
from bbox_labeling import SimpleBBoxLabeling

input_dir = sys.argv[1].rstrip(os.sep)

# 获取所有 bbox 标注文件列表
bbox_filenames = [x for x in os.listdir(input_dir) if x.endswith('.bbox')]

for bbox_filename in bbox_filenames:
    bbox_filepath = os.sep.join([input_dir, bbox_filename])
    jpg_filepath = bbox_filepath[:-5]
    if not os.path.exists(jpg_filepath):
        print('Something is wrong with {}!'.format(bbox_filepath))
        break

    # 生成根节点 annotation
    root = ET.Element('annotation')

    # 文件名节点
    filename = ET.SubElement(root, 'filename')
    jpg_filename = jpg_filepath.split(os.sep)[-1]
    filename.text = jpg_filename

    # 读取基本图像信息
    img = cv2.imread(jpg_filepath)
    h, w, c = img.shape
    # 将图像信息写入节点
    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(w)
    height = ET.SubElement(size, 'height')
    height.text = str(h)
    depth = ET.SubElement(size, 'depth')
    depth.text = str(c)

    # 读取标注信息，需要调用第 6 章的小工具中的函数
    bboxes = SimpleBBoxLabeling.load_bbox(bbox_filepath)
    for obj_name, coord in bboxes:
        # 遍历每个标注框，并写入信息到 XML
        obj = ET.SubElement(root, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = obj_name
        bndbox = ET.SubElement(obj, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmax = ET.SubElement(bndbox, 'xmax')
        ymin = ET.SubElement(bndbox, 'ymin')
        ymax = ET.SubElement(bndbox, 'ymax')
        (left, top), (right, bottom) = coord
        xmin.text = str(left)
        xmax.text = str(right)
        ymin.text = str(top)
        ymax.text = str(bottom)

    # 生成 XML 标注文件
    xml_filepath = jpg_filepath[:jpg_filepath.rfind('.')] + '.xml'
    with open(xml_filepath, 'w') as f:
        anno_xmlstr = ET.tostring(root)
        # Python 自带的 ElementTree 输出的 xml 是一坨屎
        # 如果需要格式化好的输出，讲下面注释和 import 中的注释一起取消
        #anno_xml = minidom.parseString(anno_xmlstr)
        #anno_xmlstr = anno_xml.toprettyxml()
        f.write(anno_xmlstr)
```



用 Python 执行时第一个参数是包含图片和标注信息的文件夹，就可以根据第 6 章定义的后缀为 bbox 的标注信息，生成相应的 XML 标注信息并保存在同一文件夹下。





## 相关资料

- 《深度学习与计算机视觉》
