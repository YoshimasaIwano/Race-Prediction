"""
race_htmlに含まれるhtmlを利用して、データを生成する
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
import asyncio
if asyncio.get_event_loop().is_running(): # Only patch if needed (i.e. running in Notebook, Spyder, etc)
    import nest_asyncio
    nest_asyncio.apply()
import numpy as np
import pandas as pd
import copy
#from requests_html import HTMLSession

import time
import re
import os
from os import path
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "race_url"
RACR_HTML_DIR = "race_html"
CSV_DIR = "csv"

import logging
logger = logging.getLogger('make_csv_from_this_week_html') #ファイルの名前を渡す

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

race_data_columns=[
    'race_id',
    'race_round',
    'race_title',
    'race_distance',
    'weather',
    'ground_condition',
    'time',
    'date',
    'place',
    'total_horse_number',
    'order',
    'frame_number',
    'horse_number',
    'horse_id',
    'sex_and_age',
    'burden_weight',
    'jockey_id',
    'goal_time',
    'half_order',
    'last_time',
    'odds',
    'horse_weight',
    ]



def make_csv_this_week_with_odds():
    save_race_csv = CSV_DIR+"/data"+"/sep_3/9_20"+".csv"
    
    if not ((os.path.isfile(save_race_csv)) ): # まだcsvがなければ生成
        race_df = pd.DataFrame(columns=race_data_columns )
        total = 0;
        # race_html/year/month というディレクトリが存在すればappend, なければ何もしない
        with open(RACR_URL_DIR+"/"+ "9_20-win5" + ".txt", "r") as f:
#             save_dir = RACR_HTML_DIR+"/9_20" 
#             my_makedirs(save_dir)
            urls = f.read().splitlines()

#             file_list = os.listdir(save_dir) # get all file names
#             if len(urls) != len(file_list):
#                 logger.info("getting htmls ("+"this week" + ")")
            for url in urls:
                list = url.split("=")
                race_id = list[-2]
                time.sleep(1)
                race_list = get_race_data_from_html(race_id, url)     #one race_list  with all horse data
                for race in race_list:     #split per horse   [race, horse1] [race, horse2],,,
                    horse_se = pd.Series(race, index=race_df.columns)             
                    race_df = race_df.append(horse_se, ignore_index=True) #complete one month data   [race, horse1]with columns ,,,
                        
                        

        
        race_df.to_csv(save_race_csv, header=True, index=False)     #all data in year to csv
       
        logger.info(' (rows, columns) of race_df:\t'+ str(race_df.shape))
        
        logger.info("saved " + str(total) + " htmls to csv (" + "this week" +")")
    else:
        logger.info("already have csv (" + "this week" +")")

def get_race_data_from_html(race_id, url):
    race_list = [race_id]
    
#     soup = BeautifulSoup(html, 'html.parser')

#     session = HTMLSession()
#     r = session.get(url)
#     r.html.render()
    
    session = AsyncHTMLSession()
    async def process():
        r = await session.get(url)
        #await r.html.arender(wait=5, sleep=5)
        return r
    r = session.run(process)[0]

    # race基本情報
    data_intro_1 = r.html.find(".RaceNum")[0]
    race_list.append(data_intro_1.text) # race_round
#     print(r.html.find(".RaceName")[0].text.strip("\n"))
    race_list.append(r.html.find(".RaceName")[0].text.strip("\n"))  # race_name
#     print(r.html.find(".RaceData01")[0].text.strip("\n").split("/"))
    race_details1 = r.html.find(".RaceData01")[0].text.strip("\n").split("/")
    race_list.append(race_details1[1]) # race_distance
    race_list.append(race_details1[2]) # weather
    race_list.append(race_details1[3]) # ground_condition
    race_list.append(race_details1[0]) # time
#     print(r.html.find(".RaceData02")[0].text.split(" "))
    race_details2 = r.html.find(".RaceData02")[0].text.split(" ")
    race_list.append("2020-9-20") # date
#     print(race_details2[1])
    race_list.append(race_details2[1]) # place

    print(r.html.find(".HorseList"))
    result_rows = r.html.find(".HorseList") # レース結果
    #情報
    print(len(result_rows))
    race_list.append(len(result_rows)) # total_horse_number  
    """
    for i in range(1,4):
        row = result_rows[i].findAll('td')
        race_list.append(row[1].get_text()) # frame_number_first or second or third
        race_list.append(row[2].get_text()) # horse_number_first or second or third
    """

    """# 払い戻し(単勝・複勝・三連複・3連単)
    pay_back_tables = soup.findAll("table", class_="pay_table_01")

    pay_back1 = pay_back_tables[0].findAll('tr') # 払い戻し1(単勝・複勝)
    race_list.append(pay_back1[0].find("td", class_="txt_r").get_text()) #tansyo
    hukuren = pay_back1[1].find("td", class_="txt_r")
    tmp = []
    for string in hukuren.strings:
        tmp.append(string)
    for i in range(3):
        try:
            race_list.append(tmp[i]) # hukuren_first or second or third
        except IndexError:
            race_list.append("0")

    # 枠連
    try:
        race_list.append(pay_back1[2].find("td", class_="txt_r").get_text())
    except IndexError:
        race_list.append("0")

    # 馬連
    try:
        race_list.append(pay_back1[3].find("td", class_="txt_r").get_text())
    except IndexError:
        race_list.append("0")



    pay_back2 = pay_back_tables[1].findAll('tr') # 払い戻し2(三連複・3連単)

    # wide 1&2
    wide = pay_back2[0].find("td", class_="txt_r")
    tmp = []
    for string in wide.strings:
        tmp.append(string)
    for i in range(3):
        try:
            race_list.append(tmp[i]) # hukuren_first or second or third
        except IndexError:
            race_list.append("0")

    # umatan
    race_list.append(pay_back2[1].find("td", class_="txt_r").get_text()) #umatan

    race_list.append(pay_back2[2].find("td", class_="txt_r").get_text()) #renhuku3
    try:
        race_list.append(pay_back2[3].find("td", class_="txt_r").get_text()) #rentan3
    except IndexError:
        race_list.append("0")
    """

    race_refined_list = [] #最終的にまとめるデータボックス
   
    # horse data
    for order in range(len(result_rows)):
        horse_list = []                     #temporary list
        result_row = result_rows[order]
        # order
        horse_list.append("?")
        # frame_number
        print(result_row)
        horse_list.append(result_row[0].text)
        # horse_number
        horse_list.append(result_row[1].text)
        # horse_id
        horse_list.append(result_row[3].find('a[href^="https"]').split("/")[-1])
        # sex_and_age
        horse_list.append(result_row[4].text)
        # burden_weight
        horse_list.append(result_row[5].text)
        # jockey_id
        horse_list.append(result_row[6].find('a[href^="https"]').split("/")[-2])
        # goal_time
        horse_list.append("?")
        # goal_time_dif
        #horse_list.append(result_row[8].get_text())
        # time_value(premium)
        #horse_list.append(result_row[9].get_text())
        # half_order
        horse_list.append("?")
        # last_time(上り)
        horse_list.append("?")
        # odds
        horse_list.append(result_row[9].text)
        # popular
        #horse_list.append(result_row[13].get_text())
        # horse_weight
        horse_list.append("?")
        # tame_time(premium)
        #horse_list.append(result_row[15].get_text())
        # 16:コメント、17:備考
        # tamer_id
        #horse_list.append(result_row[18].find('a').get('href').split("/")[-2])
        # owner_id
        #horse_list.append(result_row[19].find('a').get('href').split("/")[-2])
        

        race_refined_list.append(race_list + horse_list) #race_data + horse_data 

    
    return race_refined_list #one race data with horse   [[race, horse1], [race, horse2] ,,,]



#def update_csv():


if __name__ == '__main__':
    formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
    #formatter_func = "%(asctime)s\t[%(levelname)8s]\t%(message)s from %(func)" # フォーマットを定義
    logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

    logger.info("start making csv!")
    make_race_csv_from_html()

    # テスト
    #make_csv_from_html_by_year(2011)
    """
    with open("race_html/2008/1/200810010312.html", "r") as f:
        html = f.read()
        get_rade_and_horse_data_by_html(200810010312,html)
"""
