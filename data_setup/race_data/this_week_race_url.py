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
# from requests_html import HTMLSession

import os
from os import path
# OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "../data/race_url"

# import logging
# logger = logging.getLogger('this_week_race_url') #ファイルの名前を渡す

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# import chromedriver_binary
from bs4 import BeautifulSoup
URL = "https://race.netkeiba.com/top/race_list.html"
WAIT_SECOND = 5

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def this_week_race_url(date):
    options = Options()
    options.add_argument('--headless')
#     driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=options, executable_path = '/usr/bin/chromedriver') # mac はbrewでインストールしたのでpathはok
    driver.implicitly_wait(5)
    # データ
    race_url_file = RACR_URL_DIR + "/2022" + "/" + date + ".txt" #保存先ファイル
    my_makedirs( RACR_URL_DIR + "/2022")
    try:
        get_race_url_weekend(driver, date)
    except ConnectionError:
        pass
   

    driver.close()
    driver.quit()

def get_race_url_weekend(driver, date):
    race_url_file = RACR_URL_DIR + "/2022" + "/" + date + ".txt" #保存先ファイル

    # URLにアクセス
    wait = WebDriverWait(driver,2)
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)
    
    
    #日つけ選択
#     terms = driver.find_element_by_xpath("//*[@date='20221225']")
#     terms.click()
#     wait.until(EC.presence_of_all_elements_located)
#     time.sleep(2)
    
    race_columns = driver.find_elements_by_xpath("//*[@id='RaceTopRace']/div/dl")
    
    with open(race_url_file, mode='w') as f:
        #tableからraceのURLを取得(ループしてページ送り)
        time.sleep(1)
        wait.until(EC.presence_of_all_elements_located)
            
        places = []
        for column in range(len(race_columns)):
            place = race_columns[column].find_element_by_class_name("RaceList_Data").find_elements_by_tag_name("li")
            places.append(place)
       
        for place in places:
            for i in range(7,len(place)-1):
                race_href = place[i].find_element_by_tag_name("a").get_attribute("href")
                f.write(race_href + "\n")
           
            




# if __name__ == '__main__':
#     formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
#     logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

#     logger.info("start get race url!")
#     get_race_url()
