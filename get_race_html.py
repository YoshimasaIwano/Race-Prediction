"""
race_urlディレクトリに含まれるURLを利用して、htmlを取得する
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import cchardet

import time
import os
from os import path
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "race_url"
RACR_HTML_DIR = "race_html"


import logging
logger = logging.getLogger('get_race_html') #ファイルの名前を渡す

proxies_dic = {
    "http": "http://proxy.example.co.jp:8080",
    "https": "https://proxy.example.co.jp:8080",
}

"""
def get_retry(url, retry_time, errs):
    for t in range(retry_time + 1):
        r = requests.get(url, proxies = proxies_dic)
        if t < retry_time:
            if r.status_code in errs:
                time.sleep(2)
                continue
        return r
"""
    

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def get_race_html():
    # 去年までのデータ
    for year in range(2011, now_datetime.year):
        for month in range(1, 13):
                get_race_html_by_year_and_mon(year,month)
    # 今年のデータ
    for year in range(now_datetime.year, now_datetime.year+1):
        for month in range(1, now_datetime.month+1):
                get_race_html_by_year_and_mon(year,month)
    

def get_race_html_by_year_and_mon(year,month):
    with open(RACR_URL_DIR+"/"+str(year)+"-"+str(month)+".txt", "r") as f:
        save_dir = RACR_HTML_DIR+"/"+str(year)+"/"+str(month)
        my_makedirs(save_dir)
        urls = f.read().splitlines()

        file_list = os.listdir(save_dir) # get all file names

        # 取得すべき数と既に保持している数が違う場合のみ行う
        if len(urls) != len(file_list):
            logger.info("getting htmls ("+str(year) +" "+ str(month) + ")")
            for url in urls:
                list = url.split("/")
                race_id = list[-2]
                save_file_path = save_dir+"/"+race_id+'.html'
                time.sleep(0.5)
                if not os.path.isfile(save_file_path): # まだ取得していなければ取得
                    try:
                        session = requests.Session()
                        retries = Retry(total = 5, backoff_factor = 1, status_forcelist = [500, 502, 503, 504])
                        session.mount("https://", HTTPAdapter(max_retries = retries))
                        response = session.get(url, timeout = (5.0, 15.0)) #connection timeout 10s, read timeout 30s
                        #response = get_retry(url, 5, [500, 502, 503, 504])
                    except requests.exceptions.ConnectionError:
                        r.status_code = "Connection refused"
                    response.encoding = cchardet.detect(response.content)["encoding"]  # https://qiita.com/nittyan/items/d3f49a7699296a58605b
                    html = response.text
                    time.sleep(0.5)
                    with open(save_file_path, 'w') as file:
                        file.write(html)
            logging.info("saved " + str(len(urls)) +" htmls ("+str(year) +" "+ str(month) + ")")
        else:
            logging.info("already have " + str(len(urls)) +" htmls ("+str(year) +" "+ str(month) + ")")


if __name__ == '__main__':
    formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
    logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

    logger.info("start get race html!")
    get_race_html()
