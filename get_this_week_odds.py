# win5 race 今週のURLを入手する
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
from requests_html import HTMLSession

import os
from os import path
import numpy as np
import pandas as pd
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "race_url"

import logging
logger = logging.getLogger('this_week_race_url') #ファイルの名前を渡す

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
URL = "https://www.jra.go.jp/JRADB/accessO.html"
WAIT_SECOND = 5
CSV_DIR = "csv"


def get_this_week_odds():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path = 'C:\\Users\\vmlab\\chromedriver_win32\\chromedriver.exe') # mac はbrewでインストールしたのでpathはok
    driver.implicitly_wait(5)
    # データ
    save_race_csv = CSV_DIR+"/data"+"/sep_4/9_26_odds"+".csv" #保存先ファイル
    try:
        get_race_url_weekend(driver)
    except ConnectionError:
        pass
   

    driver.close()
    driver.quit()

def get_race_url_weekend(driver):
    save_race_csv = CSV_DIR+"/data"+"/sep_4/9_26_odds"+".csv" #保存先ファイル

    # URLにアクセス
    wait = WebDriverWait(driver,2)
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)

    odds_df = pd.DataFrame(columns = ["odds"])
    
    
    race_columns = driver.find_elements_by_xpath("//*[@id='odds_list']/tbody/tr")
    
    #tableからraceのURLを取得(ループしてページ送り)
    for column in range(len(race_columns)):
        odds = race_columns[column].find_element_by_class_name("odds_tan").get_text()
        odds_df.append(odds)
       
        


