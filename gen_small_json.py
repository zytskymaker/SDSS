# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/18 14:44
@Auth ： zyt_sky
@File ：gen_small_json.py
@IDE ：PyCharm
@Email: a2534487689@qq.com
@Motto：大威天龙 大罗法咒
"""
from astropy.io import fits
import pandas as pd
import glob
import json
import csv


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

        del text[0:5]
        with open(cat.replace('.cat', '.txt'), 'a+') as f:
            pa_str = 'X_IMAGE  Y_IMAGE  A_IMAGE  B_IMAGE CLASS_STAR\n'
            f.write(pa_str)
            f.writelines(text)
        txt2csv(cat.replace('.cat', '.txt'), cat.replace('.cat', '.csv'))


def generate_json(csv_file):
    for csv in csv_file:
        data = fits.getdata(csv.replace('.csv', '.fits'))
        h, w = data.shape[0], data.shape[1]
        df = pd.read_csv(csv)

        galaxy = df.loc[(df['CLASS_STAR'] < 0.005)].reset_index()
        cx, cy = galaxy['X_IMAGE'], galaxy['Y_IMAGE']
        bd = galaxy['B_IMAGE']

        shapes = []
        for i in range(len(cx)):
            points = [[cx[i], cy[i]], [cx[i], cy[i] + bd[i]]]
            info = {
                "label": "galaxy",
                "points": points,
                "group_id": None,
                "shape_type": "circle",
                "flags": {}
            }
            shapes.append(info)

        all_info = {
            "version": "4.5.13",
            "flags": {},
            "shapes": shapes,
            "imagePath": csv.replace('.csv', '.fits').split('\\')[-1],
            "imageData": "wo fang ni zai zhe li yi si yi si ",
            "imageHeight": h,
            "imageWidth": w,

        }
        with open(csv.replace('.csv', '.json'), 'w', encoding='utf-8') as fw:
            json.dump(all_info, fw, indent=4, ensure_ascii=False)


def gen_label():
    all_cat_list = glob.glob(r"C:\Users\Admin\Desktop\small\*.cat")
    generate_csv(all_cat_list)
    all_csv_list = glob.glob(r"C:\Users\Admin\Desktop\small\*.csv")
    generate_json(all_csv_list)


if __name__ == '__main__':
    gen_label()
