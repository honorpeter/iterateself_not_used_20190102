##### 第10章迁移学习和模型微调

第10章首先实现了一个图片爬虫用于搜集图片数据，并以美食图片分类为例子一步步讲解如何基于Caffe实现迁移学习。然后在此基础上进一步讲解了如何对数据进行预处理, 如何使用混淆矩阵、P-R和ROC曲线，最后介绍了如何实现可视化卷积神经网络对输入图 片的响应。


通过前面3章我们已经了解了回归和分类任务的基本流程。本章将再进一步讲讲图片 分类任务，从数据的采集开始，到预处理，再到迁移学习的简要概念和常用的模型微调法， 最后是评估模型的可视化和分析。

10.1吃货必备-通过Python采集美食圖片

本章不打算利用网上常用的CIFAR、Caltech-101甚至ImageNet等数据集，而是用自 行采集的美食图片，并训练一个专门的分类模型。数据的采集通过搜索引擎返回的图片 URL,通过讲解一个下载图片的Python脚本，说明如何通过关键词和图片搜索引擎来采集 数据。

10.1.1通过关键词和图片搜索引擎下载图片

本节讲解的是g集图片数据方法中最简单的一种:通过静态网页中图片链接下载图片。 思路是通过在搜索弓'I擎中搜索给定关键词，然后对返回结果的静态网页版本的源代码进行 匹配找到所有图片URL,下载即可。具体实现思路是先在一个文本文件中以UTF-8格式保 存要下载食品的关键词列表，然后编写脚本自动为每个关键词分配多进程，并行进行网页 源码获取和图片下载。一般来说是先在搜索引擎中输入关键词，然后返回结果后观察浏览 器地址栏是否有规律，比如关键词是哪个字段，翻页后变化的是哪个字段等。然后通过这 种规律就可以改变关键词和翻页数字，获取包含图片URL的页面源代码了。特别提一句的 是，本书提供的是最简单的基于静态网页源代码的版本，如果是动态网页结果，可以查看 页面上是否有“传统翻页版本”类的按钮，然后单击该类按钮就可以跳转到静态网页。如 果没有该类按钮，则需要动态网页扒取手段，具体方法，本书不展开讨论。

讲完思路，下面开始实战。首先是定义要下载图片的关键词，每行一个关键词：

串肉

鸭肉煮汤小条子 烤羊水鸡麻面包

这里一共定义了 7种食品，四菜一汤加两种主食。上面列表用UTF-8编码保存为 keywords.txtc然后就是要获取搜索引擎返回结果的列表了，下面以某主流图片搜索引擎返

回的结果为例，Python代码如下：

import os import re import urllib

from multiprocessing import Process #支持JPG和PNG格式

SUPPORTED_FORMATS =    [ 1 jpg', 'png',    * jpeg*]

\#搜索引擎 1取关键词和指定样本的模板

\#    {keyword}是关键词字段

\#    {index}是图片的开始下标字段

URL_TEMPLATE = r'http://image.b***u•com/search/flip?tn=b***uimage&ie=Litf— 8 &word={keyword}&pn={index}'

\#定义每个进程内下载的函数，参数分别是

\#    dir_name :文件要保存的位置

\#    keyword: 关键词

\#    start_index:要下载文件的开始编号

\#    end_index:要下载文件的结束编号

def download_images_f rom_b***u (dir_name, keyword, start—index, end_index): index = start_index

\#结束下载的判断

while index < end_index:

\#通过输入关键词和当前下标生成获取返回结果的URL，

url = URL_TEMPLATE. format (keyword=keyword"z index=index)

try:

\#打开URL获取HTML源代码

html_text = urllib.urlopen(url).read().decode(* utf-8',

\#    ignore *)

\#正则匹配获取所有URL的

image_urls = re.findall (r' nobjURLn:n (.*?)'*', html_text)

\#很苛能是没有更多的返回结果了，结束当前函数

if not image_urls:

print(1 Cannot retrieve anymore image urls \nStopping ...*.format(url))

break

\#如果发生I/O错误也可能是没有返回结果，或者超时严重，结束当前函数 except IOError as e:

print(e)

print(* Cannot open {} . \nStopping ...'.format(url)) break

\#记录已经下载的URL downloaded_urls =    []

\#依次下载URL对应的图片 for url in image_urls:

filename = url.split (*/*) [-1 ]

ext = filename[filename.rfind(*.*)+1：]

\# URL命名五花八门，只下载支持的文件后缀 if ext.lower () not in SUPPORTED_FORMATS:

index +=    1

continue

\#为了方便后期处理，直接在下载阶段就指定好要保存的文件名为数字

的规则形式

filename = *{}/{：0>6d}.{}'.format(dir_name, index, ext) cmd =    * wget "{}" -t 3 -T 5    -0    {} 1 . format (url,

filename)

os.system(cmd)

如果下载成功，并且文件大于1KB,说明是个有效的图片文件，1KB

\#

是笔者随手定的

if    os.path.exists(filename)    and    os.path.getsize

(filename) >    1024:

index_url =    ’{:0〉6d},{}*•format(index, url)

downloaded_urls.append(index_url)

\#否则很可能是无效f件，删除 else :

os.system(* rm {}'.format(filename))

\#判断是否已经下载完当前进程的任务

index +=    1

if index >= end_index: break

\#保存已经下载的图片并和文件名建立对应关系

with open (' {}_urls . txt * . format (dir_name) ,    * a *) as furls:

urls_text =    *{}\n1.format(1\n1.j oin(downloaded_urls))

if len (urls_text) >    11:

furls.write(urls_text)

\#启动下载任务的函数

def download_images(keywords, num_per_kw, procs_per_kw): args_list =    []

\#生&每个进程子任务的输入参数列表

for class_id, keyword in enumerate(keywords):

\#另每个类别建立保存图片的文件夹

dir_name =    1 { : 0>3d} *.format(class_id)

os.system('mkdir -p {}1.format(dir_name))

num_per_proc = int(round(float(num_per_kw/procs_per_kw)))

for i in range(procs_per_kw):

start_index = i * num_per_proc

end_index = start_index + num_per_proc -    1

args_list.append((dir_name, keyword, start_index,

end_index))

\#生成进程列表

processes = [Process(target=download_images_from_b***u, args=x) for x in args_list]

\#开始并吞下载

print (1 Starting to download images with {} processes ...1. format(len(processes)))

for p in processes: p.start ()

for p in processes: p. join ()

print(1 Done!1)

if _name_ ==    "_main_":

'# ilx关键词

with open('keywords•txt’，    'rb *) as f:

foods = f.read().split()

\#设置每个类别下载目标2000张，每类别用3个进程下载 download_images(foods, 2000,    3)

代码中，按照keywords.txt文件中关键词的排列顺序为每个类别的图片建立一个数字 序号的文件夹，然后每个类别分3个进程下载2000张图片，并且每类图片都以数字命名， 数字就代表着返回结果的排序。把代码保存为COlleCt_data.Py，并执行下载，结束后得到 7个文件夹的图片样本和对应的URL列表。笔者自己每类得到了从1100〜1700不等的样

本数。

这段代码和笔者实验时得到的URL列表都已经同步到本书的github代码仓库中。需 要声明的是，这段脚本仅作为示例，其中涉及的搜索引擎名字已经用“*”隐去，如果读 者需要，请按照思路自行在指定的搜索引擎上编写脚本进行图片URL抓取。请勿用于不 良目的。

10.1.2数据预处理——去除无效和不相关图片

虽然指定下载每类2000张图片，但是最后能下载到的可能远少于这个数字。原因主要 有两个：第一，搜索引擎返回的URL未必都是有效结果，所以下载过程中很可能会得到一 些无效的文件；第二，搜索引擎返回结果的相关性随着排序的靠后越来越低，所以会出现 很多不相关的图片，这也是为什么要给图片按照排序结果的先后命名。那么为什么不把下 载目标数设置高一些，这样返回有效结果可能也多一些？这是因为百度图片搜索中，我们 要下载的关键词并非热门词汇，能返回的结果不会超过2000个。如果读者想进行其他热门 关键词图片分类，可以设置更多的下载目标数。

回到正题，第一步先通过Python程序移除无效文件，思路是用OpenCV尝试打开，只 要打开不成功就删除文件，代码如下：

import os import sys import cv2

from collect_data import SUPPORTED_FORMATS    *

input_path = sys.argv[1]

for root, dirs, files in os.walk(input_path): for filename in files:

ext = filename[filename.rfind(*.*)+1:].lower() if ext not in SUPPORTED_FORMATS:

continue

filepath = os.sep.join([root, filename]) if cv2 . imread (f ilepath) is None:

os.system('rm { }'.format(filepath))

print (* { } is not a valid image file.

Deleted!*.format(filepath))

在和collect data.py相同的文件夹中，把上面代码保存为remove invalid images.py, 然后执行：

» python remove_invalid_images.py . /

这样就可以删除所有OpenCV无法读取的无效文件。接下来就是删除无关的图片，用 缩略图模式打开图片所在文件夹，默认按照文件名排列就会发现，越是靠前的图片，就是 搜索的关键词图片，越是靠后的图片就越不相关。就笔者使用的百度图片搜索而言，应该 前半部分返回结果是通过图像特征，后半部分是关键词关联。所以可以通过肉眼观察大概 截止到哪个位置，然后删除之后所有的图片就粗略删除了大部分不相关的图片。剩下的图 片中一般还是会有一些不相关的图片，我们可以视作为数据中的噪音，噪音的大小取决于 使用图像搜索引擎的结果质量，这种噪音当然是删除了好。经过删除无效图片和去除不相 关图片后，剩余图片中每类从800〜1500不等。

10.1.3数据预处理——去除重复图片

前面步骤完成的是去除无效图片和噪声，接下来还有一个很重要的步骤是去重复。因

为训练的时候要抽出一部分作为验证集，如果同一张图片同时出现在了训练和验证集里， 结果就不可靠了。去重复对于大规模数据集是个需要计算资源的工作，不过对于本章中的 例子就简单多了，本节介绍两种去重的办法：fdupes和findimagedupeso

fdupes是通过MD5来查找并删除重复文件的工具，比较策略是先找到大小相同的文 件，然后在结果里找到MD5相同的文件，然后逐byte比较。使用apt install就可以安装 fdupes o

\>> sudo apt install fdupes

然后在数据所在文件夹下执行：

» fdupes -rdN . /

r代表递归查找，d代表删除重复图片并保留一张，N代表不确认直接删除。这样就删 除了完全一样的文件，在笔者搜集的数据里一共删除了8对，说明返回结果的重复率还是 很低。使用fdupes策略并不能删除视觉上一样，或是非常相似的图片。这个时候可以考虑 linux 下的另一个工具 findimagedupes：

\>> sudo apt install findimagedupes

该工具基于的是 perceptual hash 算法 [http://www.phash.org/](http://www.phash.org/%e3%80%82)[。](http://www.phash.org/%e3%80%82)

为了方便，到这一步先建立一个train文件夹，然后把所有包含图片样本的文件夹移入

train文件夹下：

» mkdir train >> mv 00? train

接下来还不能直接执行findimagedupes,因为这种工具的执行效率和图片的分辨率大 小直接相关。而当前大多数流行的分类模型的输入分辨率并不高，所以在去重复前先增加 一个预处理步骤：即降低样本分辨率。批量降低图片分辨率的代码如下：

import os

import cv2

import sys

\#第一个参数，包含样本的文件夹

input_path = sys.argv[l].rstrip(os.sep)

\#第£个参数，目标图片的短边最大分辨率

target_short_edge = int(sys.argv[2])

\#递归S找遍运所有图片文件

for root, dirs, files in os.walk(input_path): print('scanning { }    ...'.format(root))

for filename in files:

filepath = os.sep.join([root, filename])

img = cv2.imread(filepath)

h, w = img.shape[:2]

short_edge = min(w, h)

\#如i图片的短边大于设定的短边大小，则进行缩小

if short_edge > target_short_edge:

scale = float(target_short_edge) / float(short_edge) new_w = int(round(w*scale))

new_h = int(round(h*scale))

print ('Down sanpling {} from {}x{} to {}x{} ___*. format (

f ilepath, w, h, new_w, new_h

img = cv2.resize(img, (new_w, new_h)) cv2.imwrite(filepath, img)

print(* Done!')

将代码文件保存为downscale.py文件。因为我们将要采用的分类模型的输入为 224x224,考虑到数据增加有旋转操作，所以留一部分余量，统一缩放到短边不超过256

像素。

» python downscale.py train 256

###### 接下来可以进行图片去重了：

» findimagedupes -R train > dup_list

这样所有的重复文件的路径就保存到了 dupjist文件里，格式是每行的路径就是相同

的文件。以笔者下载的图片为例，一共找出了 188组重复图像。接下来再编写一个小脚本

读取这个列表，保留每行的第一个文件，删除其余的文件。

import os import sys

dup_list = sys.argv[1]

with open (dup_list, * r *) as f:

lines = f.readlines() for line in lines:

\#列出所有重复的图像文件

dups = line.split()

print('Removing duplicates of {}*.format(dups[0]))

\#保留第一张，其余删除

for dup in dups [1:]:

cmd =    * rm {}*.format(dup)    /

os.system(cmd)

将代码保存为remove dups from list.py并执行：

» python remove_dups_from_list.py dup_list

这样就可以删除重复的图片了。这两个小工具是用来处理小规模数据的，如想效果更 好的去重复则需要更好的手段。而且对于图像去重复/相似这件事来说，本身就是个一直在 研究的课题，很多基于深度学习的方法也在被不断提出。本书提到的这两种小工具只是很 粗略的去重复，仅供参考。

10.1.4生成训练数据

生成训练数据的步骤其实前面讲过，不过考虑到这是本书目前为止第一次处理彩色图 片，所以再一步步写一下。第一步是从每类中采样一部分作为验证集，因为每类数量有限， 这里就不单独做个测试集了，验证测试合二为一，代码如下：

import os

import random

\#每类采样300张

N =    300

\#建立val文件夹

os.system(* mkdir -p val’)

\#列出所有的类别文件夹

class_dirs = os.listdir(* train *)

for class_dir in class_dirs:

\# 4 val文件夹下建:£对应的类别文件夹

os.system('mkdir - p val/{}*.format(class_dir))

root =    * train/{}*.format(class_dir)

print(1 Sampling validation set with { } images from

{}    . . . *.format(N, root))

filenames = os.listdir(root)

\#对文件名进行乱序实现随机采样

random.shuffle(filenames)

\#取前300张

val_filenames = filenames[:N]

\#呆样并移动文件到val文件夹下 for filename in val_filenames:

src_filepath = os.sep.join([root, filename])

dst_filepath    =    os.sep.join([1val1,    class_dir,

filename])

cmd = *mv {}    {}'•format(src_filepath, dst_filepath)

os.system(cmd)

执行代码就得到验证集，剩下的图片就是训练集。接下来第二步是给训练集做数据增

加操作，需要利用第6章实现的数据增加小工具：

» In -s /path/to/run_augmentation.py run_augmentation.py » In -s /path/to/image_augmentation.py image_augmentation.py

如果是用本书的github代码，直接执行link data augmentaion.sho这样就建立了使用 run augmentation.py的链接，然后执行如下代码：

import os

\#每类增加到3000张

n_total =    3000

\#从train文件夹获取子文件夹

class一dirs = os.listdir('train *)

\#遍房每个子文件夹

for class_dir in class_dirs:

src_path =    * train/{}*.format(class_dir)

\#获％类别下已有样本的数量

n_samples = len(os.listdir(src_path))

计算需要增加的样本数量

n_aug = n_total - n_samples

\#执行数据增加，并在temp文件夹下生成增加的数据

cmd =    * python run_augmentation.py {} temp {}'.format

(src一path, n_aug)

os.system(cmd)

\#把增加的数据添加到原文件夹下

cmd = *mv temp/* {}'.format(src_path)

os.system(cmd)

\#删除临时文件夹

os.system(1rm -r temp')

运行结束后就完成了数据的增加和均衡操作，每类有了 3000张作为训练数据。接下来

需要生成lmdb,首先产生文件和对应标签的列表，代码如下：

import os import sys

\#获取输入文件的名称作为数据集名字 dataset = sys.argv[l].rstrip(os.sep) class_dirs = os.listdir(dataset)

\#遍房每个类别并将生成的列表写入文件

with open('{}.txt'.format(dataset),    ' w1) as f:

for class_dir in class_dirs:

class_path = os . sep. join ( [dataset, class_d.ir]) label = int (class_dir)

lines =    ['{}/{}    {}*.format(class_path, x, label) for

x in os.listdir(class_path)]

f.write(*\n'.join(lines) +    *\n *)

将代码保存为gen label list.py,然后执行：

» python gen_label_list.py train » python gen_label_list.py val

最后一步生成lmdb,和之前不同的是生成彩色图片不需要-gray参数了。

» /path/to/caffe/build/tools/convert_imageset ./ train.txt train_lmdb -resize_width 224 -resize_height 224 --shuffle

\>>    /path/to/caffe/build/tools/convert_imageset    . / val.txt val_lmdb

-resize_width 224 -resize_height 224 --shuffle

10.2美食分类模型

本节通过训练美食分类模型，来讲解在实践中应用非常广泛的模型微调方法。最后再 结合得到的结果讲解混淆矩阵和ROC这两种常用的分析模型的手段。

10.2.1迁移学习

前面章节中提到，机器学习可以看作是从一个分布中的采样进行学习，然后泛化到对 这个分布中的数据进行预测。那么如果数据不是同一分布来的呢？是否就需要从头再来 呢？实际的应用场景中并不是这样。很多时候数据虽然不一样，但可能是相关的。比如我 们训练了一个模型区分猫狗和花草，这个模型很可能已经学到了眼睛、耳朵、腿等动物的 特征以及叶子、花瓣等植物的特征。那么当这个模型遇见一张绵羊的照片时，在特征空间 里，这张照片所在和猫狗的距离就会比花草近很多。这是因为数据之间有一部分共性。如 果原来的数据中除了猫狗还有其他的动物，那么很可能模型也学到了角和毛发形状等特征。 这时很可能只需要一张或者几张绵羊的样本就能够训练模型识别绵羊，这个叫做One-Shot 学习。甚至我们不给任何绵羊的样本，只是通过某种方法让模型知道如果遇到卷毛弯角的 动物就是绵羊，那么模型也能正确识别出绵羊，这叫做Zem-Shot学习。总之，讲到这里 主要要表达的是，即使是不同的数据，也常常有一部分共性。如果把学习过程粗略分成两 个部分，第一部分只关注模型学习各种分布之间的共性，第二部分才是具体任务，也就是 具体要区分的更细化的数据分布。从这个角度，其实很多任务都是相关的。只要能先学习 到这些任务或是数据之间的共性，然后再泛化到每一个具体任务就不是难事了。所以很多 时候迁移学习也常和多任务学习一起提到。

在深度学习中，迁移学习能力的很大一部分来源于第4章讲到过的分布式表征。因为 特征是一层层组合起来的，所以越是底层的特征就越基本，共性也越大。比如第4章提到 过，底层的卷积核学到的是边缘、块等特征，这种特征通常被称为纹理特征。再高层学到 的形状就会更加复杂，到了顶层附近学习到的特征已经可以大概描述一个物体了，这时候 的特征常被称为语义特征。

图片分类任务中，一个很常见的场景是实际中并没有大量的数据（数据永远是最昂贵 的部分），如果从头训练一个模型，泛化能力很不好。这种情况下，迁移学习就成了一个 理想的选项，可以利用别人已经训练好的模型，然后只尝试改变这个模型的语义层面的参 数，这样就能得到很好的效果，甚至很多情况下比重新训练的效果还要好。这种方法就是 接下来要讲的模型微调法。

10.2.2模型微调法(nnetune)

笔者手上只有少量数据正好是美食分类的场景，所以本节利用模型微调法来训练美食 分类模型。具体到Caffe中，模型微调的做法就是：首先，训练开始时用一个别人已经在 大量数据集上训练好的模型和参数作为起始点；其次，固定前面层的参数不动，只让后面 一层或几层的参数在少量数据上进行学习。

所以第一步就是要找别人已经在大量数据集上训练好的模型,Caffe在这方面是所有框 架中做的最好的，在不同代表性数据集上，多种已经训练好的模型可以在 <https://github.com/BVLC/caffe/wiki/Model-Zoo> 网址中找到。

直译过来叫模型动物园。我们采用的网络结构和预训练好的模型来自于德国耶拿大学 (Friedrich Schiller Universitat Jena)的计算机视觉组 CVGJ (Computer Vision Group Jena) 在ImageNet数据集上训练好的ResNet-10模型。这个模型的好处是简单、效果好(略高于 Alexnet),同时比较方便的一点的是数据一上来就做了 Batch Normalization,减不减均值

都很方便。

Caffe进行finetune的机制非常简单，只要网络定义中出现的层的名字在caffemodel文

件中能够找到就可以读取，否则就按一般情况初始化。所以基于CVGJ的模型，主要的改

动有数据层和最后全连接层：

name: "Food-fesNet-10-CVGJ" layer {

name: "data" type: ’’Data” top: "data" top: "label" include {

phase: TRAIN

}

| transform param          | {    |
| ------------------------ | ---- |
| #mean value:             | 104  |
| #mean value:             | 117  |
| #mean value:             | 123  |
| mirror: false            |      |
| Idata param {            |      |
| source: "data/train lmdb |      |
| batch size:              | 14   |

backend: LMDB

}

}

layer {

name: "data" type: '’Data" top: "data" top: "label" include {

phase: TEST

}

| transform | param   | {    |
| --------- | ------- | ---- |
| #mean_    | value:  | 104  |
| #mean     | value:  | 117  |
| #mean_    | value:  | 123  |
| mirror    | : false |      |

}

data_param {

source: "data/val_lmdb" batch_size:    7

backend: LMDB

}

}

...中间部分省略...

layer {

name: "global_pool" type: ’’Pooling" bottom:    "1aye r_512_l_sum"

top: "global_pool" pooling_param {

pool: AVE

global_pooling: true

}

}

layer {

name: "global_pool_drop" type :    "Dropout"

bottom: ',global_pooln top: "global_pool" dropout一param {

dropout_ratio:    0.382

}

}

layer {

name: "fc_food" type: "InnerProduct" bottom: "global_pool" top: "fc_food" param {

}

}

layer {

name: ’’loss"

type:    "SoftmaxWithLoss"

bottom: "fc_food"

bottom: "label"

top: "loss"

}

layer {

name: ''accuracy*' type: "Accuracy" bottom: "fc_food"

bottom: "label" top: "accuracy’' include {

phase: TEST

}

}

数据层换成了我们自己的lmdb数据，最后的全连接输出改为7输出的fc_food，并对 计算精度和loss的层做相应的改动。另外还在输入前加入了 Dropout层，主要是因为数据 量不多，为了防止过拟合。参数上，ResNet-10 —共4个残差模块，这里只对最后一个模 块中的卷积层：layer_512_l_convl、layer_512_l_conv2 和 layer_512_l_conv_expand,以及 所有的Scale层进行梯度下降。

说到这里需要单独谈一下Caffe中的BatchNorm层。之所以对Scale层进行梯度下降 是因为在Caffe中BatchNorm层其实只实现了归一化的步骤，最后缩放方差和偏置的步骤 是通过再接了一层Scale层完成的。对于BatchNorm层，使用的时候需要把所有的lr_mult 置0。BatchNorm中有个参数use global stats,这个参数的意思是是否使用全局的归一化 参数。根据BatchNorm的原理，在训练阶段应该使用每个batch的方差和均值，而预测阶 段则需要用全局的。通常这个参数不需要设置，因为默认在TEST时是真，TRAIN时是假。

把上面提到的卷积层、Scale层和fc_food层以外所有其他层的学习率参数lr_mult设置

为0就可以了，如果不想手动改动这些地方，本书的github代码仓也提供了完整的训练文

件 food_resnet_10_cvgj_finetune_val.prototxt。设置好训练的网络结构，然后根据 Caffe Model

Zoo 提供的链接 <https://github.com/cvjena/cnn-models/tree/master/ResNet_preact/ResNetlO_>

cvgj,在里面的 model_download_link.txt 中找到下载地址，并下载 ResNet-10 在 ImageNet

上训练出的参数resnetl0_cvgj_iter_320000.caffemodel。本书的github代码中也提供了

download_resnetl02.cvgj_weights.sh,直接执行就可以下载。这个例子中我们来尝试一次自

适应梯度下降法，用AdaDelta,相应的Solver描述如下：

net:    "food_resnet_10_cvgj_finetune_val.prototxt"

snapshot_prefix: "food_resnet-10" test_initialization: false solver_mode: GPU type: "AdaDelta11

和之前的solver文件比起来，主要的区别是type变成了 AdaDelta,同时需要指定delta 参数。将代码保存为soker.prototxt，然后执行下面命令就可以用Caffe进行模型微调了。

»    /path/to/caffe/buiId/tools/caffe    train -solver solver.prototxt

-weights resnetl0_cvgj_iter_320000.caffemodel -log_dir . /

其中-weights就是用来指定resnetl0_cvgj」ter_320000.caffemodel的参数作为微调的初 始化参数。按照本书中的配置，训练过程中的显存占用不到1.5GB，如果是更老的显卡，

可以考虑进一步减小batch size或者只训练最后的卷积层和全连接层。训练的loss和准确 率的曲线如图10-1所示。

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-276.jpg)

0.0

5

ssol



—Train Loss --Test Loss -• • Test Accuracy

s/匕 Au£nyv

90的888786858483

5000

10000

Iterations

15000

20000

图10-1 loss和准确率随迭代次数变化的曲线

可以看到，准确率能达到90%, loss在1万次左右最小，我们就取1、万次为最终模型。 用于部署的food_resnet_10_cvgj_deploy.prototxt的写法已经讲过，这里就不赞述了，读者 也可以参考本书githiib代码库中的完整文件。因为这次用了彩色图片，所以用Python调用 模型的脚本比起第9章中又有些许不同，代码如下：

import sys

import numpy as np

sys.path.append(*/path/to/caffe/python*)

import caffe

WEIGHTS—FILE =    * food_resnet-10_iter_10000.caffemodel*

DEPLOY_FILE =    'food_resnet_10_cvgj_deploy.prototxt1

\#caffe.set_mode_cpu()

net = caffe.Net(DEPLOY_FILE, WEIGHTS_FILE, caffe.TEST)

\#不需要用set_mean() 了，垣是需要设置通道顺奔和OpenCV—致(BGR)

transformer = caffe.io.Transformer({* data *:    net.blobs[* data *] .data.

shape})

\#获取图片列表文#的路径，#生成保存结果

image_list = sys.argv[1]

result_list =    *{}_results.txt'.format(image_list[:image_list.rfind(*.*)])

\#获取键词

foods = open(*/path/to/keywords.txt',    * rb').read() .split()

with open (image_list, 1 r *) as f, open (result_list,    * w*) as

f_ret:

image)

for line in f. readlines ():

filepath, label = line.split() label = int(label)

image = caffe.io.load_image(filepath)

transformed_image = transformer.preprocess('data', net.blobs['data *].data[...]    = trans formed_image

\#各类对应的概率就在output中第一个元素中

output = net.forward() probs = output['prob'] [0 ]

pred = np.argmax(probs)

print(*{}, predicted:    {}, true:    {}'.format(filepath,

foods[pred], foods[label]))

\#把结果保存到文件

result_line =    ’{}    {}    {}    {}\n1.format(filepath, label,

pred, '    * . join ( [str (x) for x in probs]))

f_ret.write(result_line)

二者主要的不同是需要用set_channel_Swap()变换通道顺序，另外这份代码接受的输入 是文件路径和对应标签的列表，在执行的时候还保存一份预测结果和各类对应概率的列表， 后面内容中会有用。如果要单纯预测图片，只需要把代码中和标签相关的部分抹去即可。 将代码保存为recognize_food.py,然后对验证/测试集的文件和标签列表执行如下命令，就 能够输出预测的结果，并把结果保存一份在val_results.txt中。

» python recognize_food.py val.txt

10.2.3 混淆矩阵(Confusion Matrix)

截止目前我们评估一个模型的时候都是用准确率。准确率一般是用来评估模型的全局 准确程度的，并且只是一个数字，并不能包含太多细节信息。如果希望更全面地了解评估 模型，混淆矩阵是个常用的手段。

混淆矩阵又称错误矩阵，一句话来说就是把每个类别下，模型预测错误的结果数量， 以及错误预测的类别和正确预测的数量都在一个矩阵中显示出来，方便直观地评估模型分 类的结果。在Python中计算混淆矩阵非常简单，利用第三方库skleam的metrics模块就可 以方便地进行混淆矩阵计算和可视化。skleam是scikit的一部分，是专门用于机器学习的

模块，在Ubuntu 16.04 LTS下，安装方式下面两种都可以：

(

» sudo apt install python-sklearn

» sudo pip install sklearn

安装好后，利用以下代码就可以计算本例中的四菜一汤两主食分类模型，在2100张测

试集上得到的混淆矩阵和准确率：

import itertools

import numpy as np

import matplotlib.pyplot as pit

from sklearn.metrics import confusion_matrix

\# plot_confusion_matrix ()函数就是 sklearn 官网关于 confusion matrix 的不例

\#主要i用是计算出'i淆矩阵之后进行可视化 def plot_confusion_matrix(cm, classes,

normalize=False,

title=1 Confusion matrix *,

cmap=plt.cm.Blues):

pit.imshow(cm, interpolation:1 nearest *, cmap=cmap) pit.title(title) pit.colorbar()

tick_marks = np.arange(len(classes)) plt.xticks(tick_marks, classes, rotation=45) pit.yticks(tick_marks, classes)

if normalize:

cm = cm.astype(* float')    / cm.sum(axis=l) [:, np.newaxis]

print("Normalized confusion matrix")

else:

print('Confusion matrix, without normalization')

print(cm)

thresh = cm. max ()    /    2.

for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])): pit.text(j, i, cm[i, j],

horizontalalignment=ncenter,', color="whiten if cm[i, j ]    > thresh else

"black")

pit.tight_layout()

pit.ylabel('True label *)

pit.xlabel(1 Predicted label *)

result_filepath =    'val_results.txt *

with open (result_filepath, * r *) as f: lines = f.readlines() for line in lines:

tokens = line.split() true_label = int (tokens[1]) pred_label = int(tokens[2]) true_labels.append(true_label) pred一labels.append(pred_label)

n_correct +=    1 if true_label == pred_label else 0

\#计算准确率并打

print('Accuracy =    {:.2f}% *.format(float(n_correct)/float(len(true_labels))*

100)) ~ (

\#通过sklearn的confusion_matrix ()计算混淆矩阵

cnf_mat = confusion_matrix(true_labels, pred一labels)

\#苛视化的每类名字，因方matplotlib砑中文支持不好，<拼音代替

foods =    [*kaoya’， 'yangrouchuan *,    * shuizhurou *, 'jitang’， 'maxiao *,

\* miantiao *, 'baozi']

plot_confusion_matrix(cnf_mat, classes=foods) pit.show()

保存为make_confusion_matrix.py,直接执行即可以对10.2.2节中生成的val_results.txt (在本书github代码仓中可以下载)进行准确率(90.14%)的计算，并得到图10-2所示的

混淆矩阵信息和可视化。

l<uqel<p21

Confusion matrix

yangrouchuan

shuizhurou

jitang

maxiao

miantiao

kaoya

7'

o

ba

|      |      |      |       |      |      |      |
| ---- | ---- | ---- | ----- | ---- | ---- | ---- |
|      | 284  |      |       |      |      |      |
|      |      | 239  |       |      |      |      |
|      |      |      | 276 ; |      |      |      |
|      |      |      |       | 264  |      |      |
|      |      |      |       |      | 273  |      |
|      |      |      |       |      |      |      |

270

240

210

180

150

120

90

60

30

0



Predicted label

图10-2四菜一汤两主食模型在测试集上的混淆矩阵

混淆矩阵中横轴是模型预测的类别数量统计，纵轴是数据真实标签的数量统计，所以 每行数字的和都是300。首先来看对角线，表示的是模型预测和数据标签一致的数目，所 以对角线之和除以测试集总数就是准确率。对角线上数字越大越好，在可视化结果中颜色 就越深，说明模型在该类别的预测准确率越髙。比如我们看到包子的预测值和真实值一致 的有296个，说明该类别模型结果的可靠性最高。然后来按行查看，每行不在对角线位置 上的就是错误预测的类别，比如非对角线上的最大值20对应的是水煮肉，但是被模型预测 成了麻辣小龙虾。一般来说如果一个值很高，则沿对角线对称的位置上的值通常也很高， 比如麻辣小龙虾中被预测成水煮肉的也有12个，是麻辣小龙虾这一行中被误判类别中最高 的。说明这两类属于较难区分的，也就是容易混淆，混淆矩阵很直观地帮助我们分析出了 这一结论。从视觉上来说这也合理，麻辣小龙虾和水煮肉看起来都是红汤加堆辣椒，视 觉相似度较高，而包子和其他所有类别的视觉相似程度都较低。总体而言，我们希望一个 模型的混淆矩阵对角线越高越好，非对角线部分越低越好。另外注意可视化混淆矩阵的时 候有个normalize的选项，其是每类别数量归一化的选项，如果每个类别数量不一样则用这 个选项会更加直观。

10.2.4 P-R曲线和ROC曲线

1.二分类混淆矩阵

虽然例子中的四菜一汤两主食模型处理是个多标签分类问题，在很多场景更关注的可 能是某一个类别对错与否的指标，相当于一个二分类。比如我们接了烤鸭店的委托，要做 人工智能找烤鸭照片的任务。这个时候，精度-召回曲线(Precision-Recall, PR)和受试者 工作特征曲线(Receiver Operating Characteristic curve，ROC)是更为常见的评估方式。

理解什么是P7?和还要先从混淆矩阵说起，如例子中把是否为烤鸭的混淆矩阵 的值表示在表10-1所示的表格中。

表10-1评估模型预测是否为烤鸭的混淆矩阵

| Positive：是烤鸭 Negative：不是烤鸭 | 模型预测       |                |                             |
| ----------------------------------- | -------------- | -------------- | --------------------------- |
| 正：Positive                        | 负：Negative   |                |                             |
|                                     | True Positive  | False Negative | Sensitivity/Recall/TPR      |
| jtr    丄L. . 1 V31I.1 V V          | 261            | 39             | 261/(261+39)=0.870          |
| 标签    负.Negative                 | False Positive | True Negative  | Specificity/TNR             |
|                                     | 28             | 1772           | 1772/(28+1772)=0.984        |
|                                     | Precision/PPV  | NPV            | Accuracy                    |
|                                     | 261/(261+28)   | 1772/(39+1772) | (261+1772)/(261+1772+39+28) |
|                                     | =0.903         | =0.978         | =96.81%                     |

表10-1是衡量二分类模型的一个常用表格。首先来看类别的定义，通常会定义一个正 (Positive)类别和一个负(Negative)类别，真实的类别用True来表示。比如定义是烤鸭 为正，则模型预测对的“是烤鸭”的个数就是True Positive (TP)；模型预测是烤鸭，然 而实际却不是烤鸭的，是False Positive (FP)。相应地，模型预测正确的“非烤鸭”为True

Negative (TN),模型预测为非烤鸭，然而确实是烤鸭的为False Negative (FN)。

有了这4个基本的数字，就吋以计算指标了，首先是最常见的准确率(Accuracy), 在10.2.3节也提到了，对角线之和除以所有样本和。不过这并不能详细了解两个类别分别 的准确率，尤其是当两个类别样本数量不等的时候，很难反映出模型的分类能力。在烤鸭 的例子中已经能看出一些，虽然准确率96.81%,但是预测为烤鸭的精度并不高。接下来再 来考虑更极端的情况，比如10个正样本和990个负样本，哪怕模型把1000个样本全都预 测为负样本，正确率也有99%。可这显然是有问题的，所以我们来考虑一些其他的指标。

首先是敏感度(Sensitivity),又称为召回(Recall)或者 TPR (True Positive Rate)是 预测为Positive的样本中正确的数量除以真正的Positive的数量。

TPR =——一    (公式 10-1)

TP + FN

把分子换一换就是FNR和TPR互补：

FNR = ―—— = \-TPR    (公式 10-2)

TP + FN

相应地预测为Negative中正确的数量除以真正的Negative的总数得到特指度 (Specificity),又称为 TNR (True Negative Rate),与之互补的是 FPR (False Positive Rate)

TNR=———    (公式 10-3)

FP + TN

FPR = 一—一 = 1 - TNR    (公式 10-4)

FP + TN    <

前面这4个指标中分母项都是真实类别的数量，以模型预测的数量为分母也有两个常 见指标，第一个是衡量 Positive 预测精度(Precision)的 PPV (Positive Predictive Value)， 其实就是看看模型预测为Positive的里面有多少是准的；相应的指标是NPV (Negative Predictive Value),其实也是一种精度，预测为Negative的精度.

PPV = TP    (公式 10-5)

TP + FP

NPV =———    (公式 10-6)

TN + FN

这么一个小小的二维矩阵就有这么多指标，但其实常用的就两对，分别是Precision和 Recall； FP尺和層。这两对指标的形象理解在wikipedia上有个非常好的图示，如图10-3 所示。

图10-3中的实心圆点是正样本，分布在方框的左侧；空心小圆圈是负样本，全都分布 在方框右侧。大圆圈是模型预测为正样本的，可以看到左半部分是模型预测正确的部分， 也就是True Positive，右半部份是模型预测错误的部分，即False Positive。所以当提到 FP、7W和这4个指标时，里面的Positive和Negative说的是模型预测的结果。整个大 圆内的结果就是TP+FP，所以精度就是TP!(TP七FP)，意义是预测为正的样本中真正正样 本的占比，图示对应图10-3左下角的小图。如果想知道真正的正样本中有多少被模型正确 预测出来了，那就是用大圆左半边的部分除以方框左半边的部分，这就是召回和7P/?。定 性理解这个指标对应的是模型的预测能覆盖多少正样本，所以这个指标还有个名字叫做敏 感度，也就是对真正的正样本是否足够敏感。和7P7?相对的就是FP7? 了，代表着错误预 测为正样本数量在真实负样本中的“覆盖”占比。所以一个越好的分类器，7P7?就越高， 同时FP7?越低。



2.精度-召回曲线(Precision-Recall curve)和F分数(F-Measure)

在上面的结果分析中，一直隐含了一个假设，就是类别的判断是根据每个类别的概率 最大值确定的。比如是否是烤鸭，是看Softmax层后，模型对烤鸭预测的概率值是不是最 大值。这在多分类的时候是个很自然的想法，然而具体到二分类问题却未必是最合适的。 比如把模型预测为烤鸭的概率从高到低排个序，并和真实的标签对应，会得到如下输出：

1    0.999988

1    0.999971

1    0.999962

1    0.999956

1    0.999952

1    0.999936

1    0.413589

1    0.412204

0    0.412093

1    0.411163

1    0.399088

0    0.395039

0    0.391183

0 0.000000

0 0.000000

0 0.000000

0 0.000000

概率值高的部分几乎都是1 (是烤鸭)，低的部分则几乎都是0(不是烤鸭)。如果是 理想的分类器，所有的1都会排在前面，0排在后面，当然这一般不太可能，所以中间会 有一定区域0和1混合出现。如果选定一个阈值，比如对上面这个例子，用0.413作为分 类阈值，大于等于阈值是模型预测的正样本，小于阈值则是模型预测的负样本。那么所有 大于等于0.413的样本中1的数量就是7P,除以大于0.413的样本总数（7P+FP）就是精 度，而召回则是7P除以所有真正的正样本数量。也就是说，随着选取阈值的不同，混淆 矩阵中的4个值和基于这4个值衍生出来的指标，包括精度和召回是不一样的。把选取不 同阈值时对应的精度和召回画出来，就得到了 P-7?曲线，通过例子的排列样本分数画P-7? 曲线的代码如下：

from operator import itemgetter

import numpy as np

import matplotlib.pyplot as pit

from sklearn.metrics import precision_recall_curve, average_precision_score result_filepath =    * val_results.txt *

\#    ky_probs存储一个tuple, tuple中是烤鸭标签和模型预测概率的对

ky一probs =    []

with open (result_filepath, * r * ) as f: lines = f.readlines() for line in lines:

tokens = line.split()

true_label = int(tokens[1 ])

is_ky =    1 if true_label ==    0 else 0

ky_prob = float(tokens[3])

ky_probs.append([is_ky, ky_prob])    (

\#用模型预测的概f从高到低排列

ky_probs_sorted = np.array (sorted(ky_probs, key=itemgetter(1), reverse=True))

for is_ky, ky_prob in ky_probs_sorted:

print(*{:.Of}    { : .6f}*.format(is_ky, ky_prob))

labels = ky_probs_sorted[:,    0]

probs = ky_probs_sorted[:,    1]

\#得到precision和对应的recall

precision, recall, ths = precision_recall_curve(labels, probs)

\#    计算 average-precision

ap = average_precision_score(labels, probs)

\#可视化

pit.figure(* Kao Ya Precision-Recall Curve *)

pit.plot(recall, precision, * k *, lw=2, label= * Kao Ya *)

pit.xlabel('Recall * , fontsize=16)

pit.ylabel(* Precision', fontsize=16) pit.ylim([0.0,    1.05])

pit.xlim([0•0,    1.0])

pit.title (* Precision-Recall Curve: Average Precision={:.4f}*.format(ap)) pit.legend(loc="lower left") pit.show()

其中绘制P-穴曲线和计算平均精度用到了 sklearn.metrics中的precision_recall_curve() 和average_precision_score()函数。执行程序后，得到P-A曲线如图10-4所示。

从图10-4中可以看到，总体趋势精度越高召回越低，当召回达到1的时候，对应的是 概率分数最低的正样本，这个时候正样本数量除以所有大于等于该阈值的样本数量就是最 低的精度值。通过曲线衡量模型的一个指标是平均精度(Average-Precision，AP)， 也可以理解为P-7?曲线围起来的面积。通常来说一个越好的分类器，值越高。

Precision-Recall Curve: Average P「ecision=0.9476 i.o-u______ ___    __

6 4

o- n COISDQJJd

0.2

—Kao Ya |

0.0-----*—

0.8

1.0

0.0    0.2    0.4    0.6

Recall

图10-4精度-召回曲线

在实际用到分类任务的时候，需要综合考虑精度和召回，选取一个分类阈值。F-Measure 是选取这个阈值的常用手段，F-Measure的公式如下：

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-280.jpg)

(1 +，)

PR

/32P + R

（公式10-7）

其中是个关于召回的权重，大于1的时候说明更看重召回的影响，小于1则更看 重精度，等于r的时候相当于两个值的调和平均，这是一个更常用的指SG-Measure:

(公式 io-8)

P + R

当我们想用Fj-Measure的时候，只需选取Fi-Measure最大时对应的阈值就可以。

3.受试者工作特征曲线(Receiver Operating Characteristic curve)

通过选取不同阈值还可以得到另一种常见的曲线叫做受试者工作特征曲线，简称7?OC 曲线，方法和P-7?曲线很像，就是根据不同阈值，横轴为FPR，纵轴为7P7?的曲线。 skleam.metrics中同样提供了很方便的接口分别是roc_curve()和auc()函数，为了方便对比， 我们画出烤鸭和水煮肉分别作为正样本时的ROC曲线，代码如下：

import matplotlib.pyplot as pit

from sklearn.metrics import confusion_matrix, roc_curve, auc result_filepath =    * val_results.txt *

with open (result filepath, * r') as f:

lines = f.readlines() for line in lines:

tokens = line.split()

\#真实标签，预测标签和两类的概率位置分别是1,2,3, 5

true_label = int(tokens[1]) pred_label = int (tokens[2]) ky_prob = float(tokens[3]) szr_prob = float (tokens[5])

is_ky. append (1 if true_label ==    0 else 0)

pred_ky. append (1 if pred_label ==    0 else 0)

\#把率作为预测某一类别的分＜

ky一scores.append(ky_prob)

is_szr. append (1 if true_label ==    2 else 0)

szr_scores.append(szr_prob)

\#打印是否是烤鸭的i淆矩阵

ky_cnf_mat = confusion_matrix(is_ky, pred_ky, labels=[l, 0]) print(ky_cnf_mat)

\#计算烤極的t"^r, fpr在不同分数阈值下的值

ky_fpr, ky_tpr, ky_ths = roc_curve(is一ky, ky_scores)

\#根据tpr柘fpr计算瘅鸭的AUC ky_auc = auc(ky_fpr, ky_tpr)

\#计算水煮肉的tpr，fpr在不同分数阈值下的值

szr_fpr, szr_tpr, szr_ths = roc_curve(is_szr, szr_scores)

\#根据tpr和fpr计算水煮肉的AUC

szr_auc = auc(szr_fpr, szr_tpr)    ；

\#逯行可视化

pit.plot(ky_fpr, ky_tpr, 1k--*,    lw=2,

| label='Kao                                                   | Ya      | ROC    curve    (auc    = | {:.2f}) ’ |
| ------------------------------------------------------------ | ------- | ------------------------- | --------- |
| format(ky_auc))pit.plot(szr_fpr, szr_tpr,                    | 丨b-.'  | ,lw=2,                    |           |
| label= * Shui                                                | Zhu     | Rou ROC curve    (auc =   |           |
| format(szr auc))plt.plot([0, 1],    [0,    1],               |         | lw=l)                     |           |
| plt.plot([0, 0,    1],    [0,                                | 1, 1],  | ’k:.,    lw=2)            |           |
| plt.xlim([-0.02,    1.0])plt.ylim([0.0z    1.02])pit.xlabel('False Positive | Rate'   | r fontsize=16)            |           |
| pit.ylabel(* True Positive                                   | Rate *, | fontsize=16)              |           |

pit.title('Receiver operating characteristic example *) pit.legend(loc="lower right") pit.show()

代码中还包含了产生表10-1中4个值的代码，执行代码可以得到烤鸭混淆矩阵的4个

值和烤鸭+水煮肉的曲线如图10-5所示。

在AOC曲线中，左下到右上的对角线代表•个完全没有效果的分类器，如果曲线在对

角线左上，说明分类器有效果，在对角线右下说明是负效果。曲线越“靠近”左上角说明 分类器越好，理想的分类器对应的7?OC曲线是和(0,0)-(0,1)-(1,1)所在的折线重合。7?OC曲 线围住的面积被称为AUC (Area Under Curve),和曲线中的dP类似，是一个可以 直接拿来量化比较的简单指标，越大说明分类器效果越好。回想前面提到过的准确率的例 子，7?OC和df/C因为是基于FP7?和rp/?/因为这两个指标都是一种相对的比例，所以当 要检验的样本数量不相等时，结果比准确率可靠很多。

通过图10-5可以看到判断是否是烤鸭的ROC曲线，整体比判断是否是烤肉的7?OC曲 线更接近左上角，JC/C也更高，说明模型对于是否是烤鸭的判断整体优于对是否是水煮肉

的判断，这和10.2.3节中的结论是一致的。

_Receiver operating characteristic example

L0 p...............二二：---:------——

o.O.

34fT3a:(u>Q 一 soQ.(unJH



X - • Kao Ya ROC curve (auc = 0.99)

J    •■- Shui Zhu Rou ROC curve (auc = 0.98)

0 0 0.0    0.2    0.4    0.6    0.8    1.0

False Positive Rate

图10-5烤鸭和水煮肉分类的和dt/C

在P-R曲线中可以通过F-measure选定一个合适的分类阈值，在ROC曲线中也有类似 的方法叫做EER (Equal Error Rate),指的是的情况，因为FNR=l-TPR，所以 在7?OC中就是曲线和(0，1)-(1,0)对角线的交点。从漏检和误检的角度，可以把理解为 对正样本的漏检率，F7W?则是预测为正样本的误检率。芯幻?是均衡考虑漏检率和误检率时 的阈值选定标准。

10.2.5全局平均池化和激活响应图

第4章已经提到过全局平均池化，本节来讲讲如何利用这种池化后的全连接层得到一 个类别的激活响应图。首先再来回顾一下全局平均池化，如图10-6所示。

全局平均 值池化

全连接

F1



Fn

a)



图10-6全局平均池化和激活响应图示意

![img](file:///E:/00.Ebook/__Recent__html__/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)/00_深度学习与计算机视觉%20%20算法原理、框架应用与代码实现_14279998(1)_files/00_f1a666600ea1973ac6c9%20%2097d59f060146b694280ee3019eb0_14279998(1)-284.jpg)

图10-6a是全局平均池化示意图。在最后一层的响应图上，相比传统的直接上全连接， 先经过全局平均池化得到每个响应图的平均值，再接全连接，使得全连接的复杂性一下子 下降了，因为池化后每个通道只剩下一个值，所以对于某一个特定类别而言，全连接就 相当于简单的加权相加。这样做的好处是，在响应图和类别之间建立了一种对应。比如 图10-6a,只画出模型预测的类别对应的权重，这个时候把池化后每个通道的值看作是一 个函数的话，对特定类别全连接就相当于一个广义线性模型，泛化的性能也会比参数多很 多的直接全连接好很多。

全局平均池化的另一个好处是，因为响应图和类别之间建立了一种线性的对应，所以 如果不经过池化，而是如图10-6b所示，直接把这种权重和每个通道的响应图相乘再相加 的话，得到的就是该类别的激活响应图。因为不池化的响应图带有一定程度的位置信息， 所以加权相加之后得到的该类别的激活响应图应该也会带有非常直观的位置信息。下面通 过代码来对这种响应图进行可视化：

import sys

import numpy as np

import matplotlib.pyplot as pit

import cv2

sys.path.append(*/path/to/caffe/python*)

import caffe

WEIGHTS_FILE =    * food_resnet-10_iter_10000.caffemodel'

DEPLOY_FILE =    * food_resnet_l0_cvgj_deploy.prototxt *

\#指定＞后一层响应图的blob名称_

FEATURE_MAPS =    *layer_512_l_sum'

\#指定 ＜后一层全连接层的名＞

FC LAYER =    1fc food

\#caffe.set_mode_cpu()

net = caffe.Net(DEPLOY_FILEZ WEIGHTS_FILE, caffe.TEST)

transformer = caffe.io.Transformer({* data *:    net.blobs[* data'].data.

shape})

transformer.set_transpose(* data *, transformer.set_raw_scale('data 1, #预处理数据，从rgbSiIbgr

(2, 0, 255)

1))

transformer.set_channel_swap(* data *,    (2,    1,    0))

image_list = sys.argv[1]

\#采M jet作为响应图的热度图方案

cmap = pit.get_cmap(* j et *)

with open (image_list, ' r *) as f:

for line in f. readlines ():

filepath = line.split()[0]

image = caffe.io.load_image(filepath)

\#取消下面两行的注释，可&^原大小的图生成分辨率更高的响应图

^transformer.inputs['data']    =    (1,    3, image.shape[0],

image. shape[1])

\#net.blobs['data'] .reshape (1, 3,    image.shape[0],    image.

shape[1])

transformed_image = transformer.preprocess(* data *, image) net.blobs[* data *] .data[...]    = transformed_image

output = net.forward()

pred = np.argmax(output[*prob *] [0])

\#获取最后一层的7x7响应图，一共512通道

feature_maps = net.blobs[FEATURE—MAPS].data[0]

\#获取＜后一层全连接的参数值

fc_params = net.params[FC_LAYER]

\#    取预测类别对应的参数值

f c_w = fc_params[0].data[pred]

\# _计算该类另if对应的响应图

activation_map = np.zeros_like(feature一maps[0]) for feature_map, w in zip(feature_maps, fc_w):

activation_map += feature_map * w #可视化：左图为原窗，中间为响应图，右圍为热度图和原图的叠加 #原图重新表示为OpenCV可接受的格式

image = np.round(image*255).astype(np.uint8) h, w = image.shape[:2]

\#响应图放大到和原图一样大，为了可视化效果用CUBIC插值让变化平滑 activation_map = cv2.resize(activation_map, (w, h),

interpolation=cv2.工NTER—CUBIC)

\#归一化然后重新表示为OpenCV可接受的格式 activation_map -= activation_map.min() activation_map /= activation_map.max()

\#生成热度S

activation_color_map = np.round(cmap(activation_map)[:,

:,    :3]*255).astype(np.uint8)

\#生成三通道响应图方便拼接

activation一map = np.stack(np.round([activation_map*255]*3). astype(np.uint8))

activation_map = activation_map.transpose(1,    2,    0)

\#生成叠加氣度图

overlay_img = image/2    + activation_color_map/2

\#横向接

vis_img = np.hstack([image, activation_map, overlay_img])

\#运道交换：RGB-->BGR

vis_img = cv2.cvtColor(vis_imgf cv2.COLOR—RGB2BGR) cv2.imshow(1 Activation Map Visualization', vis_img) cv2.waitKey()

默认图像都是先缩放到224x224,最后得到的响应图大小是7x7,如果希望得到分辨 率更高的响应图，可U按照代碍中的指示把执行transformer.preprocess()函数之前的两行语 句注释掉，这样就可以按照原图大小读取图片并得到响应图。我们从烤鸭、羊肉串和面条 类中各找一张试一试，得到结果如图10-7所示。



图10-7烤鸭、羊肉串、面条样本和对应的响应图

可以看到，在食物自身特征最明显的区域都出现了高的响应。第4章讲到过卷积有 个性质叫做同变性，其实就是原图中物体移动到哪里，响应图中的响应也移动到哪里。 这种位置信息通过池化层后也能够得到一定程度的保留，所以能通过分类学习得到这样 的响应图。从弱监督学习的角度来理解，这是通过分类的弱监督数据，得到了更强的物 体位置的信息。有了位置信息，岂不是就可以进行目标检测了？这正是第11章要讲的 内容。
