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

import numpy as np
import pandas as pd
import time
import os
from multiprocessing.dummy import Pool
from os import path
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "race_url"
CSV_DATA_DIR = "csv"


import logging
logger = logging.getLogger('get_win5_return_csv') #ファイルの名前を渡す

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

def get_win5_return_csv():
    # 去年までのデータ
    for year in range(2011, now_datetime.year + 1):
        get_win5_racce_id_year(year)
    
    

def get_win5_racce_id_year(year):
    save_win5_race_id_csv = CSV_DATA_DIR + "/data" + "/win5-return-" + str(year) + ".csv"
    with open(RACR_URL_DIR+"/"+str(year)+"-win5-return"+".txt", "r",encoding = 'utf-8') as f:
        win5_race_id = pd.DataFrame(columns = ["win5_return"])
        urls = f.read().splitlines()
        url_list = []

        for url in urls:
            race_id = url.split("=")[-1]
            url_list.append(race_id)
            
        win5_race_id = pd.DataFrame(url_list, columns = ["win5_return"])
        win5_race_id.to_csv(save_win5_race_id_csv, header = True, index = False)
        
        
        

    
if __name__ == '__main__':
    formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
    logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

    logger.info("start get race html!")
    get_win5_race_id()
