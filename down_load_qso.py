import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

"""
大致编写完成
存在以下问题:
1.去重
2.多线程提速
"""


def get_data(csvfile):
    df = pd.read_csv(csvfile)
    # df.drop_duplicates()
    run = df['run']
    camCol = df['camCol']
    field = df['field']
    return run, camCol, field


def generate_url(run, camCol, field):
    urls = []
    for i in range(len(run)):
        base_url = f"https://dr12.sdss.org/fields/runCamcolField?run={run[i]}" + f"&camcol={camCol[i]}" + f"&field={field[i]}"
        print(base_url)
        urls.append(base_url)
    return urls


def set_proxy():
    proxies = {'http': 'http://127.0.0.1:7777', 'https': 'http://127.0.0.1:7777'}
    return proxies


def get_query(urls):
    proxies = set_proxy()
    download_fits_url = []
    download_jpg_url = []
    for url in urls:
        r = requests.get(url, proxies=proxies)
        print('Querying ', r.status_code == 200)

        soup = BeautifulSoup(r.text, features='html.parser')  # features值可为lxml
        hrefs = []

        for link in soup.findAll('a'):
            hrefs.append(link.get('href'))

        download_jpg_url.append(hrefs[-8])
        hrefs = hrefs[-7:-2]

        for href in hrefs:
            href = 'https://dr12.sdss.org' + href
            download_fits_url.append(href)

    return download_fits_url, download_jpg_url


def get_fits(download_fits_urls):
    proxies = set_proxy()
    for d in download_fits_urls:
        r = requests.get(d, proxies=proxies)  # 根据文件的大小，这一步为主要耗时步骤
        print('Downloading ', r.status_code == 200)
        file_name = d[-30:]
        file_name = os.path.join(r'E:\pycharmworkspace\workhard\filrs', file_name)
        print(file_name)
        with open(file_name, "wb") as code:
            code.write(r.content)
            print("fits download over")


def get_jpg(download_jpg_url):
    proxies = set_proxy()
    for j in download_jpg_url:
        print('https://dr12.sdss.org' + j)
        r = requests.get('https://dr12.sdss.org' +j, proxies=proxies)  # 根据文件的大小，这一步为主要耗时步骤
        print('Downloading ', r.status_code == 200)
        file_name = j[-27:]
        file_name = os.path.join(r'E:\pycharmworkspace\workhard\filrs', file_name)
        print(file_name)
        with open(file_name, "wb") as code:
            code.write(r.content)
            print("jpg download over")


if __name__ == '__main__':
    run, camcol, filed = get_data('MyResult_202253.csv')
    urls = generate_url(run, camcol, filed)
    fits_url, jpg_url = get_query(urls)
    get_fits(fits_url)
    get_jpg(jpg_url)
