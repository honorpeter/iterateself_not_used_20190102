---
title: data aug
toc: true
date: 2018-09-01
---


# 需要补充的

- 这个是《深度学习与计算机视觉》中的某一章的内容，那一章还没有进行总结，因此先把部分程序放在这，后面对那一章进行总结后合并进来。
- 之所以在这里占个位置，因为 CV 的关于手写数字识别的例子中涉及到了数据增强。
- 后续把对应的章节总结合并到这里。


# 数据增强




```python
import numpy as np
import cv2

crop_image = lambda img, x0, y0, w, h: img[y0:y0+h, x0:x0+w]

def random_crop(img, area_ratio, hw_vari):
    h, w = img.shape[:2]
    hw_delta = np.random.uniform(-hw_vari, hw_vari)
    hw_mult = 1 + hw_delta
    w_crop = int(round(w*np.sqrt(area_ratio*hw_mult)))
    if w_crop > w - 2:
        w_crop = w - 2
    h_crop = int(round(h*np.sqrt(area_ratio/hw_mult)))
    if h_crop > h - 2:
        h_crop = h - 2
    x0 = np.random.randint(0, w-w_crop-1)
    y0 = np.random.randint(0, h-h_crop-1)
    return crop_image(img, x0, y0, w_crop, h_crop)

def rotate_image(img, angle, crop):
    h, w = img.shape[:2]
    angle %= 360
    M_rotate = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    img_rotated = cv2.warpAffine(img, M_rotate, (w, h))

    if crop:
        angle_crop = angle % 180
        if angle_crop > 90:
            angle_crop = 180 - angle_crop
        theta = angle_crop * np.pi / 180.0
        hw_ratio = float(h) / float(w)
        tan_theta = np.tan(theta)
        numerator = np.cos(theta) + np.sin(theta) * tan_theta
        r = hw_ratio if h > w else 1 / hw_ratio
        denominator = r * tan_theta + 1
        crop_mult = numerator / denominator
        w_crop = int(round(crop_mult*w))
        h_crop = int(round(crop_mult*h))
        x0 = int((w-w_crop)/2)
        y0 = int((h-h_crop)/2)

        img_rotated = crop_image(img_rotated, x0, y0, w_crop, h_crop)

    return img_rotated

def random_rotate(img, angle_vari, p_crop):
    angle = np.random.uniform(-angle_vari, angle_vari)
    crop = False if np.random.random() > p_crop else True
    return rotate_image(img, angle, crop)

def hsv_transform(img, hue_delta, sat_mult, val_mult):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float)
    img_hsv[:, :, 0] = (img_hsv[:, :, 0] + hue_delta) % 180
    img_hsv[:, :, 1] *= sat_mult
    img_hsv[:, :, 2] *= val_mult
    img_hsv[img_hsv > 255] = 255
    return cv2.cvtColor(np.round(img_hsv).astype(np.uint8), cv2.COLOR_HSV2BGR)

def random_hsv_transform(img, hue_vari, sat_vari, val_vari):
    hue_delta = np.random.randint(-hue_vari, hue_vari)
    sat_mult = 1 + np.random.uniform(-sat_vari, sat_vari)
    val_mult = 1 + np.random.uniform(-val_vari, val_vari)
    return hsv_transform(img, hue_delta, sat_mult, val_mult)

def gamma_transform(img, gamma):
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)

def random_gamma_transform(img, gamma_vari):
    log_gamma_vari = np.log(gamma_vari)
    alpha = np.random.uniform(-log_gamma_vari, log_gamma_vari)
    gamma = np.exp(alpha)
    return gamma_transform(img, gamma)


```




```python
import os
import argparse
import random
import math
from multiprocessing import Process, cpu_count

import cv2

import image_augmentation as ia

def parse_args():
    parser = argparse.ArgumentParser(
        description='A Simple Image Data Augmentation Tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('input_dir',
                        help='Directory containing images')
    parser.add_argument('output_dir',
                        help='Directory for augmented images')
    parser.add_argument('num',
                        help='Number of images to be augmented',
                        type=int)

    parser.add_argument('--num_procs',
                        help='Number of processes for paralleled augmentation',
                        type=int, default=cpu_count())

    parser.add_argument('--p_mirror',
                        help='Ratio to mirror an image',
                        type=float, default=0.5)

    parser.add_argument('--p_crop',
                        help='Ratio to randomly crop an image',
                        type=float, default=1.0)
    parser.add_argument('--crop_size',
                        help='The ratio of cropped image size to original image size, in area',
                        type=float, default=0.8)
    parser.add_argument('--crop_hw_vari',
                        help='Variation of h/w ratio',
                        type=float, default=0.1)

    parser.add_argument('--p_rotate',
                        help='Ratio to randomly rotate an image',
                        type=float, default=1.0)
    parser.add_argument('--p_rotate_crop',
                        help='Ratio to crop out the empty part in a rotated image',
                        type=float, default=1.0)
    parser.add_argument('--rotate_angle_vari',
                        help='Variation range of rotate angle',
                        type=float, default=10.0)

    parser.add_argument('--p_hsv',
                        help='Ratio to randomly change gamma of an image',
                        type=float, default=1.0)
    parser.add_argument('--hue_vari',
                        help='Variation of hue',
                        type=int, default=10)
    parser.add_argument('--sat_vari',
                        help='Variation of saturation',
                        type=float, default=0.1)
    parser.add_argument('--val_vari',
                        help='Variation of value',
                        type=float, default=0.1)

    parser.add_argument('--p_gamma',
                        help='Ratio to randomly change gamma of an image',
                        type=float, default=1.0)
    parser.add_argument('--gamma_vari',
                        help='Variation of gamma',
                        type=float, default=2.0)

    args = parser.parse_args()
    args.input_dir = args.input_dir.rstrip('/')
    args.output_dir = args.output_dir.rstrip('/')

    return args

def generate_image_list(args):
    filenames = os.listdir(args.input_dir)
    num_imgs = len(filenames)

    num_ave_aug = int(math.floor(args.num/num_imgs))
    rem = args.num - num_ave_aug*num_imgs
    lucky_seq = [True]*rem + [False]*(num_imgs-rem)
    random.shuffle(lucky_seq)

    img_list = [
        (os.sep.join([args.input_dir, filename]), num_ave_aug+1 if lucky else num_ave_aug)
        for filename, lucky in zip(filenames, lucky_seq)
    ]

    random.shuffle(img_list)  # in case the file size are not uniformly distributed

    length = float(num_imgs) / float(args.num_procs)
    indices = [int(round(i * length)) for i in range(args.num_procs + 1)]
    return [img_list[indices[i]:indices[i + 1]] for i in range(args.num_procs)]

def augment_images(filelist, args):
    for filepath, n in filelist:
        img = cv2.imread(filepath)
        filename = filepath.split(os.sep)[-1]
        dot_pos = filename.rfind('.')
        imgname = filename[:dot_pos]
        ext = filename[dot_pos:]

        print('Augmenting {} ...'.format(filename))
        for i in range(n):
            img_varied = img.copy()
            varied_imgname = '{}_{:0>3d}_'.format(imgname, i)
            if random.random() < args.p_mirror:
                img_varied = cv2.flip(img_varied, 1)
                varied_imgname += 'm'
            if random.random() < args.p_crop:
                img_varied = ia.random_crop(
                    img_varied,
                    args.crop_size,
                    args.crop_hw_vari)
                varied_imgname += 'c'
            if random.random() < args.p_rotate:
                img_varied = ia.random_rotate(
                    img_varied,
                    args.rotate_angle_vari,
                    args.p_rotate_crop)
                varied_imgname += 'r'
            if random.random() < args.p_hsv:
                img_varied = ia.random_hsv_transform(
                    img_varied,
                    args.hue_vari,
                    args.sat_vari,
                    args.val_vari)
                varied_imgname += 'h'
            if random.random() < args.p_gamma:
                img_varied = ia.random_gamma_transform(
                    img_varied,
                    args.gamma_vari)
                varied_imgname += 'g'
            output_filepath = os.sep.join([
                args.output_dir,
                '{}{}'.format(varied_imgname, ext)])
            cv2.imwrite(output_filepath, img_varied)

def main():
    args = parse_args()
    params_str = str(args)[10:-1]

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    print('Starting image data augmentation for {}\n'
          'with\n{}\n'.format(args.input_dir, params_str))

    sublists = generate_image_list(args)
    processes = [Process(target=augment_images, args=(x, args, )) for x in sublists]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print('\nDone!')

if __name__ == '__main__':
    main()
```



## 相关资料

- 《深度学习与计算机视觉》
