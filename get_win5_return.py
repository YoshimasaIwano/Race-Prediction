# win5 raceの全情報のURLを入手する
"""
https://db.netkeiba.com/?pid=race_search_detail
検索窓から全レースを一覧表示
→レースへのリンクを取得
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

import re
import time
from selenium.common.exceptions import StaleElementReferenceException

import os
from os import path
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "race_url"

import logging
logger = logging.getLogger('get_win5_return') #ファイルの名前を渡す

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
URL = "https://race.netkeiba.com/top/win5_results.html"
WAIT_SECOND = 5


def get_win5_return():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path = 'C:\\Users\\vmlab\\chromedriver_win32\\chromedriver.exe') # mac はbrewでインストールしたのでpathはok
    driver.implicitly_wait(5)
    # データ
    for year in range(2011, now_datetime.year + 1):
        #year = str(year) + "年"
        race_url_file = RACR_URL_DIR + "/" + str(year) + "-win5-return" + ".txt" #保存先ファイル
        if not os.path.isfile(race_url_file): # まだ取得していなければ取得
            logger.info("getting urls ("+str(year) +" " + ")")
            try:
                get_win5_race_url_year(driver,year)
            except ConnectionError:
                pass
   

    driver.close()
    driver.quit()

def get_win5_race_url_year(driver, year):
    race_url_file = RACR_URL_DIR + "/" + str(year) + "-win5-return" + ".txt" #保存先ファイル

    # URLにアクセス
    wait = WebDriverWait(driver,2)
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)

    # 期間を選択
    year_element = driver.find_element_by_name('year')
    year_select = Select(year_element)
    year_select.select_by_value(str(year))


    all_rows = driver.find_elements_by_xpath("//*[@class='Win5_PaybackBox']/ul/li")#一年間に行われたwin5の回数
    
    with open(race_url_file, mode='w', encoding = 'utf-8') as f:
        #tableからraceのURLを取得(ループしてページ送り)
        time.sleep(1)
        wait.until(EC.presence_of_all_elements_located)
            #print(all_rows)
            #total += len(all_rows)-1
        targets = []
        for row in range(1, len(all_rows)):
            target = all_rows[row].find_element_by_class_name("Win5_PaybackWrap").text
            #print(target)
            f.write(target+"\n")
            
            
            




if __name__ == '__main__':
    formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
    logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

    logger.info("start get race url!")
    get_race_url()
