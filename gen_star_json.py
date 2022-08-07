# -*- coding: utf-8 -*-
"""
@Time ： 2022/7/18 17:00
@Auth ： zyt_sky
@File ：gen_star_json.py
@IDE ：PyCharm
@Email: a2534487689@qq.com
@Motto：大威天龙 大罗法咒
"""

'''
思路：
目前我们有星系的json，直接拿过来将里边的东西替换掉就可以

恒星的坐标的话 有之前的csv结果作为保证
class_star>0.005作为筛选条件搞出来 基本问题不大 明日跑
左上 右下
'''
import pandas as pd
import glob
import json

train_json_list = glob.glob(
    r'E:\Galaxy_detection\Swin-Transformer-Object-Detection-master\data\coco\train2017_two_galaxy'
    r'\*.json')
val_json_list = glob.glob(
    r'E:\Galaxy_detection\Swin-Transformer-Object-Detection-master\data\coco\val2017_two_galaxy'
    r'\*.json')

train_csv_list = glob.glob(r'E:\new_dsss\sdss_train\*.csv')
val_csv_list = glob.glob(r'E:\new_dsss\sdss_val\*.csv')

for i in range(len(val_csv_list)):
    df = pd.read_csv(val_csv_list[i])
    star = df.loc[(df['CLASS_STAR'] > 0.005)].reset_index()
    cx = star['X_IMAGE']
    cy = star['Y_IMAGE']
    bc = star['A_IMAGE']
    bd = star['B_IMAGE']
    new_shapes = []
    for j in range(len(cx)):
        points = [[cx[j] - (bc[j] / 2), cy[j] - (bd[j] / 2)], [cx[j] + (bc[j] / 2), cy[j] + (bd[j] / 2)]]
        info = {
            "label": "star",
            "points": points,
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {}
        }
        new_shapes.append(info)
    with open(val_json_list[i], 'r', encoding='utf-8') as fw:
        train_info = json.load(fw)
        train_info['shapes'] = new_shapes
    with open(val_json_list[i].replace('.json', '_cs.json'), 'a+', encoding='utf-8') as ff:
        json.dump(train_info, ff, indent=4, ensure_ascii=False)
