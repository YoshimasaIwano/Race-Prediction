"""
horse_urlディレクトリに含まれるURLを利用して、htmlを取得する
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import cchardet
import codecs

import time
import os
from os import path
# OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
HORSE_URL_DIR = "horse_url"
HORSE_HTML_DIR = "horse_html"

# import logging
# logger = logging.getLogger('get_horse_html') #ファイルの名前を渡す

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
        
def get_horse_html():
    for i in range(64):
        get_horse_html_split(i)

def get_horse_html_split(i):
    with open("../data/" + HORSE_URL_DIR+"/"+ "horse_" + str(i) +".txt", "r") as f:
        global save_dir
        save_dir = "../data/" + HORSE_HTML_DIR+"/"+ "horse_" + str(i)
        my_makedirs(save_dir)
        urls = f.read().splitlines()

        file_list = os.listdir(save_dir) # get all file names
        if len(urls) != len(file_list):
            x = list(map(write_html, urls))
"""
        # 取得すべき数と既に保持している数が違う場合のみ行う
        if len(urls) != len(file_list):
            logger.info("getting htmls ("+ "horse" + ")")
            for url in urls:
                list = url.split("/")
                horse_id = list[-2]
                save_file_path = save_dir+"/"+horse_id+'.html'
                if os.path.isfile(save_file_path):
                    continue
                time.sleep(0.3)
                if not os.path.isfile(save_file_path): # まだ取得していなければ取得
                    try:
                        session = requests.Session()
                        retries = Retry(total = 5, backoff_factor = 1, status_forcelist = [500, 502, 503, 504])
                        session.mount("https://", HTTPAdapter(max_retries = retries))
                        response = session.get(url, timeout = (5.0, 15.0)) #connection timeout 5s, read timeout 15s
                        #response = get_retry(url, 5, [500, 502, 503, 504])
                    except requests.exceptions.ConnectionError:
                        r.status_code = "Connection refused"
                    response.encoding = cchardet.detect(response.content)["encoding"] #https://qiita.com/nittyan/items/d3f49a7699296a58605b
                    html = response.text
                    time.sleep(0.3)
                    with codecs.open(save_file_path, 'w', 'utf-8') as file:
                        file.write(html)
            logging.info("saved " + str(len(urls)) +" htmls ("+ "horse" + ")")
        else:
            logging.info("already have " + str(len(urls)) +" htmls ("+ "horse" + ")")
"""

def write_html(url):
    global save_dir
    list = url.split("/")
    horse_id = list[-2]
    save_file_path = save_dir+"/"+horse_id+'.html'
    if os.path.isfile(save_file_path):
        return
    time.sleep(0.3)
    if not os.path.isfile(save_file_path): # まだ取得していなければ取得
        try:
            session = requests.Session()
            retries = Retry(total = 5, backoff_factor = 1, status_forcelist = [500, 502, 503, 504])
            session.mount("https://", HTTPAdapter(max_retries = retries))
            response = session.get(url, timeout = (5.0, 15.0)) #connection timeout 5s, read timeout 15s
        except requests.exceptions.ConnectionError:
            r.status_code = "Connection refused"
        response.encoding = cchardet.detect(response.content)["encoding"] #https://qiita.com/nittyan/items/d3f49a7699296a58605b
        html = response.text
        time.sleep(0.3)
        with codecs.open(save_file_path, 'w', 'utf-8') as file:
            file.write(html)

# if __name__ == '__main__':
#     formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
#     logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

#     logger.info("start get horse html!")
#     get_horse_html_split(4)
