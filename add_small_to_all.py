# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/20 15:03
@Auth ： zyt_sky
@File ：add_small_to_all.py
@IDE ：PyCharm
@Email: a2534487689@qq.com
@Motto：大威天龙 大罗法咒
"""
import os

import pandas as pd
import glob
import json
import csv
import shutil


def txt2csv(txt_name, csv_name):
    csv_file = open(csv_name, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)
    csv_row = []

    f = open(txt_name, 'r', encoding='GB2312')
    for line in f:
        csv_row = line.split()
        writer.writerow(csv_row)

    f.close()
    csv_file.close()


def generate_csv(cat_list):
    for cat in cat_list:
        with open(cat, 'r') as f:
            text = f.readlines()

        del text[0:8]
        with open(cat.replace('.cat', '.txt'), 'a+') as f:
            pa_str = 'X_IMAGE  Y_IMAGE  A_IMAGE  B_IMAGE THETA_IMAGE CLASS_STAR MAG_AUTO MAG_BEST\n'
            f.write(pa_str)
            f.writelines(text)
        txt2csv(cat.replace('.cat', '.txt'), cat.replace('.cat', '.csv'))


def add_small(json_list, csv_list):
    for i in range(len(json_list)):
        print(csv_list[i])
        csv_info = pd.read_csv(csv_list[i])
        # csv_info = csv_info.loc[(csv_info['CLASS_STAR'] < 0.001) & (csv_info['B_IMAGE'] > 2) ].reset_index()
        csv_info = csv_info.loc[(csv_info['CLASS_STAR'] < 0.001) & (csv_info['MAG_AUTO'] < -5)].reset_index()
        x_image = csv_info['X_IMAGE']
        y_image = csv_info['Y_IMAGE']
        bd = csv_info['B_IMAGE']
        with open(json_list[i], 'r') as f:
            info = json.load(f)
            shapes = info['shapes']
            for j in range(len(x_image)):
                points = [[x_image[j], y_image[j] - bd[j]], [x_image[j], y_image[j] + bd[j]], [x_image[j] + bd[j], y_image[j]],
                          [x_image[j] - bd[j], y_image[j]]]
                # points = [[x_image[j], y_image[j]], [x_image[j], y_image[j] + bd[j]]]
                add_info = {
                    "label": "galaxy",
                    "points": points,
                    "group_id": None,
                    "shape_type": "polygon",
                    "flags": {}
                }
                shapes.append(add_info)

            all_info = {
                "version": info["version"],
                "flags": {},
                "shapes": shapes,
                "imagePath": info['imagePath'],
                "imageData": info['imageData'],
                "imageHeight": info['imageHeight'],
                "imageWidth": info['imageWidth'],

            }
            with open(csv_list[i].replace('.csv', '_all.json'), 'w', encoding='utf-8') as fw:
                json.dump(all_info, fw, indent=4, ensure_ascii=False)


def gen_train():
    all_cat_list = glob.glob(r"E:\new_dsss\sdss_train\*.cat")
    generate_csv(all_cat_list)
    json_list = glob.glob(
        r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\train2017_zscale_five\*.json')
    csv_list = glob.glob(r'E:\new_dsss\sdss_train\*.csv')
    add_small(json_list, csv_list)


def gen_val():
    all_cat_list = glob.glob(r"E:\new_dsss\sdss_val\*.cat")
    generate_csv(all_cat_list)
    json_list = glob.glob(
        r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\val2017_zscale_five\*.json')
    csv_list = glob.glob(r'E:\new_dsss\sdss_val\*.csv')
    add_small(json_list, csv_list)


def remove_txt(txt_lists):
    for txt in txt_lists:
        os.remove(txt)


def remove_csv(csv_lists):
    for csv in csv_lists:
        os.remove(csv)


def remove_json(json_lists):
    for json in json_lists:
        os.remove(json)


def remove_all():
    remove_txt(glob.glob(r'E:\new_dsss\sdss_train\*.txt'))
    remove_txt(glob.glob(r'E:\new_dsss\sdss_val\*.txt'))
    remove_csv(glob.glob(r'E:\new_dsss\sdss_train\*.csv'))
    remove_csv(glob.glob(r'E:\new_dsss\sdss_val\*.csv'))
    remove_json(glob.glob(r'E:\new_dsss\sdss_train\*.json'))
    remove_json(glob.glob(r'E:\new_dsss\sdss_val\*.json'))
    remove_json(glob.glob(r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\train2017_two_galaxy'
                          r'\*.json'))
    remove_json(
        glob.glob(r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\val2017_two_galaxy\*.json'))


def gen_all():
    gen_train()
    gen_val()


def move_all():
    all_train = glob.glob(r'E:\new_dsss\sdss_train\*.json')
    all_val = glob.glob(r'E:\new_dsss\sdss_val\*.json')
    train_dst = r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\train2017_two_galaxy'
    val_dst = r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\val2017_two_galaxy'
    for train in all_train:
        shutil.move(train, train_dst)
    for val in all_val:
        shutil.move(val, val_dst)


def rename_all():
    train_json_list = glob.glob(
        r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\train2017_two_galaxy\*.json')
    for jsons in train_json_list:
        os.rename(jsons, jsons.replace('_all.json', '.json'))
    val_json_list = glob.glob(
        r'E:\xjbx\Swin2\Swin-Transformer-Object-Detection-master\data\coco\val2017_two_galaxy\*.json')
    for jsons in val_json_list:
        os.rename(jsons, jsons.replace('_all.json', '.json'))


if __name__ == '__main__':
    remove_all()
    gen_all()
    move_all()
    rename_all()
