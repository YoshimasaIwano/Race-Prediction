"""
race_urlディレクトリに含まれるURLを利用して、htmlを取得する
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests_html import AsyncHTMLSession
import asyncio
if asyncio.get_event_loop().is_running(): # Only patch if needed (i.e. running in Notebook, Spyder, etc)
    import nest_asyncio
    nest_asyncio.apply()
from bs4 import BeautifulSoup
import cchardet

import time
import os
from os import path
# OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "../data/race_url"
RACR_HTML_DIR = "../data/race_html"


# import logging
# logger = logging.getLogger('this_week_race_html') #ファイルの名前を渡す

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



def this_week_race_html():
    with open(RACR_URL_DIR + "/2022" + "/"+ "6_26" + ".txt", "r") as f:
        save_dir = RACR_HTML_DIR + "/2022" + "/6_26" 
        my_makedirs(save_dir)
        urls = f.read().splitlines()

        file_list = os.listdir(save_dir) # get all file names

        # 取得すべき数と既に保持している数が違う場合のみ行う
        if len(urls) != len(file_list):
            # logger.info("getting htmls ("+"this week" + ")")
            for url in urls:
                list = url.split("=")
                race_id = list[-2]
                save_file_path = save_dir+"/"+race_id+'.html'
                time.sleep(1)
                if not os.path.isfile(save_file_path): # まだ取得していなければ取得
                    try:
                        session = AsyncHTMLSession()
                        async def process():
                            r = await session.get(url)
                            #await r.html.arender(wait=5, sleep=5)
                            return r
                        #r.html.render()
                        
#                         session = requests.Session()
#                         retries = Retry(total = 5, backoff_factor = 1, status_forcelist = [500, 502, 503, 504])
#                         session.mount("https://", HTTPAdapter(max_retries = retries))
                        
#                         response = session.get(url, timeout = (5.0, 10.0)) #connection timeout 10s, read timeout 30s
                        
                        #response = get_retry(url, 5, [500, 502, 503, 504])
                    except requests.exceptions.ConnectionError:
                        response.status_code = "Connection refused"
#                     response.encoding = cchardet.detect(response.content)["encoding"]  # https://qiita.com/nittyan/items/d3f49a7699296a58605b
#                     html = response.text
                    results = session.run(process)[0]
                    results.encoding = cchardet.detect(results.content)["encoding"] 
                    html = results.text
                    time.sleep(1)
                    with open(save_file_path, 'w') as file:
                        file.write(html)
            # logging.info("saved " +" htmls ("+ "this week" + ")")
        # else:
            # logging.info("already have " + str(len(urls)) +" htmls ("+ "this week" + ")")


# if __name__ == '__main__':
#     formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
#     logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

#     logger.info("start get race html!")
#     get_race_html()
