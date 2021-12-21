"""
horse_htmlに含まれるhtmlを利用して、データを生成する
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import copy
import codecs

import time
import re
import os
from os import path
# OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
HORSE_URL_DIR = "horse_url"
HORSE_HTML_DIR = "horse_html"
CSV_DIR = "csv"

# import logging
# logger = logging.getLogger('make_horse_csv_from_html') #ファイルの名前を渡す

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

"""race_data_columns=[
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
"""
horse_data_columns=[
    'horse_id',
    'father_id',
    'grandfather_id',
    'mother_id',
    'total_race_number',
    'date',
    'place',
    'weather',
    'race_name',
    'whole_horse_number',
    'odds',
    'order',
    'jockey_id',
    'burden_weight',
    'race_distance',
    'ground_condition',
    'goal_time',
    'half_order',
    'last_time',
    'horse_weight',
]


def make_horse_csv_from_html():
    save_dir = "../data/" + CSV_DIR + "/horse_data" 
    my_makedirs(save_dir)
    for i in range(62):
        make_horse_csv_split(i)

def make_horse_csv_split(i):
    save_horse_csv_dir = "../data/" + CSV_DIR + "/horse_data" + "/horse_" + str(i)
    my_makedirs(save_horse_csv_dir)
    
    
    # logger.info("saving csv (" + "horse_" + str(i) +")")
    total = 0
    # indicate horse_html/horse_(i) dirs
    html_dir = HORSE_HTML_DIR+ "/" + "horse_" + str(i) 
    if os.path.isdir(html_dir):                #confirm existance of html dir
        file_list = os.listdir(html_dir) # get all html file names in horse(i) dir
        total += len(file_list)
        # logger.info(" appending " + str(len(file_list)) + " datas to csv (" + "horse_"+ str(i)+ ")")
        for file_name in file_list:      #list all html file in horse(i) dir
            list = file_name.split(".")
            horse_id = list[-2]
            save_file_csv = save_horse_csv_dir + "/" + horse_id + ".csv"
            if not  os.path.isfile(save_file_csv):
                with codecs.open(html_dir+"/"+file_name, "r", "utf-8") as f:  #open one horse html
                    horse_df = pd.DataFrame(columns = horse_data_columns )
                    try:
                        html = f.read()
                    except UnicodeError:
                        continue
                    list = file_name.split(".")
                    horse_id = list[-2]
                    horse_race_list = get_horse_data_from_html(horse_id, html) #one horse data with all race
                    if horse_race_list:
                        for horse_race in horse_race_list:                      #split each race
                            race_se = pd.Series(horse_race, index = horse_df.columns) 
                            horse_df = horse_df.append(race_se, ignore_index=True)  #complete one horse data [pedigree, race1],,,with columnns
                        
                    if not horse_df.empty:
                        horse_df.to_csv(save_file_csv, header=True, index=False) #horse data to csv 
             
            

            
            
#         logger.info(' (rows, columns) of race_df:\t'+ str(horse_df.shape))
        
#         logger.info("saved " + str(total) + " htmls to csv (" + str(i) +")")
        

def get_horse_data_from_html(horse_id, html):
    horse_list = [horse_id]
    
    soup = BeautifulSoup(html, 'html.parser')

    # horse基本情報
    try:
        pedigree_table = soup.find("table", class_="blood_table").findAll('tr') #get blood_table
        father_row = pedigree_table[0].findAll("td")        #table[0]=father,grnfather table[1]=father's mother table table[2]=mother, mother'sfather table[3] = granmother
        horse_list.append(father_row[0].find('a').get('href').split("/")[-2]) #father_id  
        horse_list.append(father_row[1].find('a').get('href').split("/")[-2]) #grandfather_id
        mother_row =pedigree_table[2].findAll("td") 
        horse_list.append(mother_row[0].find('a').get('href').split("/")[-2]) #mother_id  mother_row[1] = mother's father
    except AttributeError:
        print(horse_id)
        horse_list.append('')
        horse_list.append('')
        horse_list.append('')
    
    
    #horse_race_data
    try:
        result_rows = soup.find("table", class_ = "db_h_race_results nk_tb_common").findAll('tr') #all race result row
        horse_list.append(len(result_rows)-1)     #total race number
    except AttributeError:
        print(horse_id)

    horse_refined_list = [] #最終的にまとめるデータボックス
   
    # race data
    for race in range(1, len(result_rows)):
        race_list = []                     #temporary list
        result_row = result_rows[race].findAll("td")
        if not len(result_row) == 28:
            break
        #date
        race_list.append(result_row[0].find('a').get('href').split("/")[-2])
        #place
        race_list.append(result_row[1].get_text())
        #weather
        race_list.append(result_row[2].get_text())
        #result_row[3] = R
        #race_name
        race_list.append(result_row[4].get_text())
        #result_row[5] = movie
        #whole_horse_number
        race_list.append(result_row[6].get_text())
        #result_row[7] = frame_number
        #result_row[8] = horse_number
        #odds
        race_list.append(result_row[9].get_text())
        #result_row[10] = attractiveness
        #order
        race_list.append(result_row[11].get_text())
        #jockey_id
        try:
            race_list.append(result_row[12].find('a').get('href').split("/")[-2])
        except AttributeError:
            race_list.append('')
        #burden_weight
        race_list.append(result_row[13].get_text())
        #race_distance
        race_list.append(result_row[14].get_text())
        #ground_condition
        race_list.append(result_row[15].get_text())
        #result_row[16] = babasisuu?
        #goal_time
        race_list.append(result_row[17].get_text())
        #result_row[18] = difference
        #result_row[19] = time_reputation
        #half_order
        race_list.append(result_row[20].get_text())
        #result_row[21] = pace
        #last_time
        race_list.append(result_row[22].get_text())
        #horse_weight
        race_list.append(result_row[23].get_text())
        

        horse_refined_list.append(horse_list + race_list)

    
    return horse_refined_list



#def update_csv():


# if __name__ == '__main__':
#     formatter = "%(asctime)s [%(levelname)s]\t%(message)s" # フォーマットを定義
#     #formatter_func = "%(asctime)s\t[%(levelname)8s]\t%(message)s from %(func)" # フォーマットを定義
#     logging.basicConfig(filename='logfile/'+OWN_FILE_NAME+'.logger.log', level=logging.INFO, format=formatter)

#     logger.info("start making csv!")
#     #make_horse_csv_from_html()

#     # テスト
#     make_horse_csv_split(4)
#     """
#     with open("race_html/2008/1/200810010312.html", "r") as f:
#         html = f.read()
#         get_rade_and_horse_data_by_html(200810010312,html)
# """
