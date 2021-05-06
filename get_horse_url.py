# horseの全情報のURLを入手する
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

import os
from os import path
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
HORSE_URL_DIR = "horse_url"

import logging
logger = logging.getLogger('get_horse_url') #ファイルの名前を渡す

from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
URL = "https://db.netkeiba.com/?pid=horse_search_detail"
WAIT_SECOND = 5


def get_horse_url():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path = 'C:\\Users\\vmlab\\chromedriver_win32\\chromedriver.exe') # mac はbrewでインストールしたのでpathはok
    driver.implicitly_wait(10)
    
    #all horse data
    horse_url_file = HORSE_URL_DIR + "/" + "horse" + ".txt" #保存先ファイル
    
    #url 取得の関数へ渡す
    try:
        get_horse_url_all(driver)
    except ConnectionError:
        pass


    driver.close()
    driver.quit()

def get_horse_url_all(driver):
    horse_url_file = HORSE_URL_DIR + "/" + "horse" + ".txt" #保存先ファイル

    # URLにアクセス
    wait = WebDriverWait(driver,10)
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)
    

    num = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    # 馬区分をチェック
    for i in num:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        terms = driver.find_element_by_id("check_umamark_"+ str(i))
        terms.click()
    
    #条件
    for i in reversed(range(2,5)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        terms = driver.find_element_by_id("check_"+ str(i))
        terms.click()
        
    #その他条件
    for i in range(3,5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        terms = driver.find_element_by_id("check_other_"+ str(i).zfill(2))
        terms.click()
        
    #表示順
    list_element = driver.find_element_by_name('sort')
    list_select = Select(list_element)
    list_select.select_by_value("birthyear")


    # 表示件数を選択(20,50,100の中から最大の100へ)
    list_element = driver.find_element_by_name('list')
    list_select = Select(list_element)
    list_select.select_by_value("100")

    # フォームを送信
    frm = driver.find_element_by_css_selector("#db_search_detail_form > form")
    frm.submit()
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)

    total_num_and_now_num = driver.find_element_by_xpath("//*[@id='contents_liquid']/div[1]/div[1]/div[2]").text
    total_num = re.sub("r\D", "", re.search(r'(.*)件中', total_num_and_now_num).group().strip("件中"))
    print(total_num)

    pre_url_num = 0
    if os.path.isfile(horse_url_file):
        with open(horse_url_file, mode='r') as f:
            pre_url_num = len(f.readlines())

    if total_num!=pre_url_num:
        with open(horse_url_file, mode='w') as f:
            #tableからraceのURLを取得(ループしてページ送り)
            total = 0
            while True:
                time.sleep(1)
                wait.until(EC.presence_of_all_elements_located)

                all_rows = driver.find_element_by_class_name('race_table_01').find_elements_by_tag_name("tr")
                total += len(all_rows)-1
                for row in range(1, len(all_rows)):
                    race_href = all_rows[row].find_elements_by_tag_name("td")[1].find_element_by_tag_name("a").get_attribute("href")
                    f.write(race_href+"\n")
                try:
                    target = driver.find_elements_by_link_text("次")[0]
                    driver.execute_script("arguments[0].click();", target) #javascriptでクリック処理
                except IndexError:
                    break
        logging.info("got "+ str(total) +" urls of " + str(total_num) +" ("+ "horse" + ")")
    else:
        logging.info("already have " + str(pre_url_num) +" urls ("+ "horse" + ")")


if __name__ == '__main__':
    formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
    logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

    logger.info("start get horse url!")
    get_horse_url()
