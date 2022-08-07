# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/9 16:02
@Auth ： zyt_sky
@File ：gen_qso_list.py
@IDE ：PyCharm
@Motto：大威天龙 大罗法咒

"""
# 把大图割一下 然后将有类星体的部分搞出来
from astropy.io import fits
import pandas as pd
import csv
import glob


def get_data_from_corr(corr_file):
    data = fits.open(corr_file)
    return data[1].data


def generate_csv(corr_data, txt_file):
    with open(txt_file, 'a+') as f:
        f.writelines('field_x   field_y   field_ra   field_dec   index_x   index_y   index_ra   index_dec   index_id   '
                     'field_id   match_weight   mag_auto \n')
        f.writelines(
            str(corr_data).replace(',', ' ').replace('[', ' ').replace(']', ' ').replace('(', ' ').replace(')', ' '))
        f.close()
    csv_file = txt_file.replace('txt', 'csv')
    txt2csv(csv_file, txt_file)


def txt2csv(csv_file, txt_file):
    csvFile = open(csv_file, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    csvRow = []

    f = open(txt_file, 'r', encoding='GB2312')
    for line in f:
        csvRow = line.split()
        writer.writerow(csvRow)

    f.close()
    csvFile.close()


def get_qso_info(qso_csv):
    df = pd.read_csv(qso_csv)

    run = df['run']
    camCol = df['camCol']
    field = df['field']

    ra = df['ra']
    dec = df['dec']

    qso_info_list = []
    for i in range(len(run)):
        qso_info = [[run[i], camCol[i], field[i]], [ra[i], dec[i]]]
        qso_info_list.append(qso_info)
    return qso_info_list


def get_match_info(match_csv_name, qso_info):
    m_run = match_csv_name.split('-')[2].strip('0')
    m_camCol = match_csv_name.split('-')[3]
    m_field = match_csv_name.split('-')[4].strip('0').strip('.csv')

    m_run = int(m_run)
    m_camCol = int(m_camCol)
    m_field = int(m_field)

    match_qso = []
    for i in range(len(qso_info)):
        if [m_run, m_camCol, m_field] == qso_info[i][0]:
            match_qso.append(qso_info[i][1])

    return match_qso


def get_all_star(match_csv):
    match_result = pd.read_csv(match_csv)
    all_star = []

    star_x = match_result['field_x']
    star_y = match_result['field_y']

    for i in range(len(star_x)):
        all_star.append([star_x[i], star_y[i]])
    return all_star


def qso_match(match_csv, qso_list):
    match_result = pd.read_csv(match_csv)
    field_ra = match_result['field_ra']
    qso_xy = []
    for f_ra in field_ra:
        flag = False
        if not flag:
            for num, location in enumerate(qso_list):
                ra = location[0]
                print(ra)
                if abs(f_ra - ra) < 0.0001:
                    print('match')
                    qso_x = match_result.loc[field_ra == f_ra]['field_x'].values
                    qso_x = str(qso_x).strip('[').strip(']')
                    qso_x = float(qso_x)
                    # print(qso_x)
                    qso_y = match_result.loc[field_ra == f_ra]['field_y'].values
                    qso_y = str(qso_y).strip('[').strip(']')
                    qso_y = float(qso_y)
                    # print(qso_y)
                    qso_xy.append([qso_x, qso_y])

    return qso_xy


def write2list(list_name, qso_loc, all_star_loc):
    with open(list_name, 'a+') as f:
        for i in range(len(qso_loc)):
            f.writelines(str(200) + ' ' + str(qso_loc[i][0]) + ' ' + str(qso_loc[i][1]) + '\n')
        for i in range(len(all_star_loc)):
            f.writelines(str(100) + ' ' + str(all_star_loc[i][0]) + ' ' + str(all_star_loc[i][1]) + '\n')
        f.close()


def generate_label():
    corr_file_list = glob.glob(r'E:\qso_corr\*.corr')
    for corr_file in corr_file_list:
        # 1.从corr获取数据
        corr_data = get_data_from_corr(corr_file)
        # 2.corr转成csv
        generate_csv(corr_data, corr_file.replace('.corr', '.txt'))
        corr_csv = corr_file.replace('.corr', '.csv')
        # 3.获取一张fits里所有的qso
        qso_info_list = get_qso_info(r'E:\pycharmworkspace\workhard\sdss_download\MyResult_202281.csv')
        # 4.从casJob查询的csv和qso_info_list进行匹配
        match_qso = get_match_info(corr_csv, qso_info_list)
        # 5.获取csv里所有的恒星
        all_star = get_all_star(corr_csv)
        # 6.获取匹配成功的qso的x,y
        qso_location = qso_match(corr_csv, match_qso)
        # 7.写入list文件
        write2list(corr_file.replace('.corr', '.list'), qso_location, all_star)


if __name__ == '__main__':
    generate_label()
