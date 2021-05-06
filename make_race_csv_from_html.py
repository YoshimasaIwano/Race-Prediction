"""
race_htmlに含まれるhtmlを利用して、データを生成する
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import copy

import time
import re
import os
from os import path
OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
RACR_URL_DIR = "race_url"
RACR_HTML_DIR = "race_html"
CSV_DIR = "csv"

import logging
logger = logging.getLogger('make_race_csv_from_html') #ファイルの名前を渡す

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
    'pop',
    'horse_weight',
    ]

"""horse_data_columns=[
    'race_id',
    'rank',
    'frame_number',
    'horse_number',
    'horse_id',
    'sex_and_age',
    'burden_weight',
    'rider_id',
    'goal_time',
    'goal_time_dif',
    'time_value',
    'half_way_rank',
    'last_time',
    'odds',
    'popular',
    'horse_weight',
    'tame_time',
    'tamer_id',
    'owner_id'
]
"""

def make_race_csv_from_html():
    save_dir = CSV_DIR+"/race_data" 
    my_makedirs(save_dir)
    for year in range(2011, now_datetime.year+1):
        make_csv_from_html_year(year)

def make_csv_from_html_year(year):
    save_race_csv = CSV_DIR+"/race_data"+"/race-"+str(year)+".csv"
    #horse_race_csv = CSV_DIR+"/horse-"+str(year)+".csv"
    #my_makedirs(save_race_csv)
    #my_makedirs(horse_race_csv)
    if not ((os.path.isfile(save_race_csv)) ): # まだcsvがなければ生成
        race_df = pd.DataFrame(columns=race_data_columns )
        logger.info("saving csv (" + str(year) +")")
        total = 0;
        for month in range(1, 13):
            # race_html/year/month というディレクトリが存在すればappend, なければ何もしない
            html_dir = RACR_HTML_DIR+"/"+str(year)+"/"+str(month)
            if os.path.isdir(html_dir):
                file_list = os.listdir(html_dir) # get all file names
                total += len(file_list)
                logger.info(" appending " + str(len(file_list)) + " datas to csv (" + str(year)  +" "+ str(month)+ ")")
                for file_name in file_list:
                    with open(html_dir+"/"+file_name, "r") as f:
                        html = f.read()
                        list = file_name.split(".")
                        race_id = list[-2]                  #get race id
                        race_list = get_race_data_from_html(race_id, html)     #one race_list  with all horse data
                       
                        for race in race_list:     #split per horse   [race, horse1] [race, horse2],,,
                            #print(race)
                            horse_se = pd.Series(race, index=race_df.columns)             
                            race_df = race_df.append(horse_se, ignore_index=True) #complete one month data   [race, horse1]with columns ,,,
                        
                        

        
        race_df.to_csv(save_race_csv, header=True, index=False)     #all data in year to csv
       
        logger.info(' (rows, columns) of race_df:\t'+ str(race_df.shape))
        
        logger.info("saved " + str(total) + " htmls to csv (" + str(year) +")")
    else:
        logger.info("already have csv (" + str(year) +")")

def get_race_data_from_html(race_id, html):
    race_list = [race_id]
    
    soup = BeautifulSoup(html, 'html.parser')

    # race基本情報
    data_intro = soup.find("div", class_="data_intro")
    race_list.append(data_intro.find("dt").get_text().strip("\n")) # race_round
    race_list.append(data_intro.find("h1").get_text().strip("\n")) # race_title
    race_details1 = data_intro.find("p").get_text().strip("\n").split("\xa0/\xa0")
    race_list.append(race_details1[0]) # race_distance
    race_list.append(race_details1[1]) # weather
    race_list.append(race_details1[2]) # ground_condition
    race_list.append(race_details1[3]) # time
    race_details2 = data_intro.find("p", class_="smalltxt").get_text().strip("\n").split(" ")
    race_list.append(race_details2[0]) # date
    race_list.append(race_details2[1]) # place


    result_rows = soup.find("table", class_="race_table_01 nk_tb_common").findAll('tr') # レース結果
   #情報
    race_list.append(len(result_rows)-1) # total_horse_number  
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
    for order in range(1, len(result_rows)):
        horse_list = []                     #temporary list
        result_row = result_rows[order].findAll("td")
        # order
        horse_list.append(result_row[0].get_text())
        # frame_number
        horse_list.append(result_row[1].get_text())
        # horse_number
        horse_list.append(result_row[2].get_text())
        # horse_id
        horse_list.append(result_row[3].find('a').get('href').split("/")[-2])
        # sex_and_age
        horse_list.append(result_row[4].get_text())
        # burden_weight
        horse_list.append(result_row[5].get_text())
        # jockey_id
        horse_list.append(result_row[6].find('a').get('href').split("/")[-2])
        # goal_time
        horse_list.append(result_row[7].get_text())
        # goal_time_dif
        #horse_list.append(result_row[8].get_text())
        # time_value(premium)
        #horse_list.append(result_row[9].get_text())
        # half_order
        horse_list.append(result_row[10].get_text())
        # last_time(上り)
        horse_list.append(result_row[11].get_text())
        # odds
        horse_list.append(result_row[12].get_text())
        # popular
        horse_list.append(result_row[13].get_text())
        # horse_weight
        horse_list.append(result_row[14].get_text())
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
