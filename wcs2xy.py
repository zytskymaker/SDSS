# -*- coding: utf-8 -*-
"""
@Time ： 2022/8/11 22:31
@Auth ： zyt_sky
@File ：wcs2xy.py
@IDE ：PyCharm
@Email: a2534487689@qq.com
@Motto：大威天龙 大罗法咒
"""
import glob

from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import pandas as pd


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


def zerosra(ra):
    if ra > 180:
        return ra - 360
    return ra


def get_fits_name(qso_inf):
    all_fits = []
    for i in range(len(qso_inf)):
        fits_info = qso_inf[i][0]
        run = str(fits_info[0]).zfill(6)
        camcol = str(fits_info[1])
        field = str(fits_info[2]).zfill(4)
        fits_name = r'E:\qso_corr\frame-r-' + run + '-' + camcol + '-' + field + '.fits'
        all_fits.append(fits_name)
    return all_fits


# qso_csv = r'E:\pycharmworkspace\workhard\sdss_download\MyResult_202281.csv'
# qso_infp = get_qso_info(qso_csv)
# fits_list = get_fits_name(qso_infp)
# for i in range(len(fits_list)):
#     hdu = fits.open(fits_list[i])
#     hdr = hdu[0].header
#     data = hdu[0].data
#     wcs = WCS(hdr)
#     hdu.close()
#     m_run = fits_list[i].split('-')[2].lstrip('0')
#     m_camCol = fits_list[i].split('-')[3]
#     m_field = fits_list[i].split('-')[4].strip('0').strip('.fits')
#
#     df = pd.read_csv(qso_csv)
#     qso_match = df.loc[(df['run'] == int(m_run)) & (df['camCol'] == int(m_camCol)) & (df['field'] == int(m_field))]
#     ra = qso_match['ra'].values[0]
#     dec = qso_match['dec'].values[0]
#     tmp = np.array(wcs.sub(2).all_world2pix(ra, dec, 0)).T
#     print(tmp[0])
#     with open(fits_list[i].replace('.fits', '.list'), 'a+') as f:
#         f.writelines('200 ' + str(tmp[0]) + ' ' + str(tmp[1]) + '\n')


fits_file_list = glob.glob(r'E:\qso_corr\*.fits')
for ff in fits_file_list:
    df = pd.read_csv(ff.replace('.fits', '.csv'))
    RAS = df["field_ra"]
    DECS = df["field_dec"]
    hdu = fits.open(ff)
    hdr = hdu[0].header
    data = hdu[0].data
    wcs = WCS(hdr)
    hdu.close()
    tmp = np.array(wcs.sub(2).all_world2pix(RAS, DECS, 0)).T
    with open(ff.replace('.fits', '.list'), 'a+') as f:
        for j in range(len(tmp)):
            f.writelines('100 ' + str(tmp[j][0]) + ' ' + str(tmp[j][1]) + '\n')