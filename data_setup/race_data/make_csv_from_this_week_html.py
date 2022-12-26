"""
create a csv using html in race_html
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

from bs4 import BeautifulSoup
import pandas as pd

import os
from os import path
RACR_URL_DIR = "../data/race_url"
RACR_HTML_DIR = "../data/race_html"
CSV_DIR = "../data/csv"

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



def make_csv_from_this_week_html():
    save_race_csv = CSV_DIR+"/2022"+"/Dec_4/12_25"+".csv"
    
    if not ((os.path.isfile(save_race_csv)) ): # if csv in not created yet
        race_df = pd.DataFrame(columns=race_data_columns )
        total = 0
        html_dir = RACR_HTML_DIR+"/2022"+"/"+"12_25"
        if os.path.isdir(html_dir):
            file_list = os.listdir(html_dir) # get all file names
            total += len(file_list)
            for file_name in file_list:
                with open(html_dir+"/"+file_name, "r") as f:
                    html = f.read()
                    list = file_name.split(".")
                    race_id = list[-2]                  #get race id
                    race_list = get_race_data_from_html(race_id, html)     #one race_list  with all horse data
                    for race in race_list:     #split per horse   [race, horse1] [race, horse2],,,
                        horse_se = pd.Series(race, index=race_df.columns)             
                        race_df = race_df.append(horse_se, ignore_index=True) #complete one month data   [race, horse1]with columns ,,,
        
        race_df.to_csv(save_race_csv, header=True, index=False)     #all data in year to csv

def get_race_data_from_html(race_id, html):
    race_list = [race_id]
    
    soup = BeautifulSoup(html, 'html.parser')

    # race information
    data_intro_1 = soup.find("div", class_="RaceList_Item01")
    race_list.append(data_intro_1.find("span", class_="RaceNum").get_text()) # race_round
    data_intro_2 = soup.find("div", class_="RaceList_Item02")
    race_list.append(data_intro_2.find("div", class_="RaceName").get_text().strip("\n")) 
    race_details1 = data_intro_2.find("div", class_="RaceData01").get_text().strip("\n").split("/")
    race_list.append(race_details1[1]) # race_distance
    race_list.append('晴') # weather 
    race_list.append('良') # ground_condition  
    race_list.append(race_details1[0]) # time
    race_details2 = data_intro_2.find("div", class_="RaceData02").get_text().split("\n")
    race_list.append("2022-12-25") # date
    race_list.append(race_details2[2]) # place

    result_rows = soup.find("div", {"class":"RaceTableArea"}).findAll('tr') 
    race_list.append(len(result_rows)-2) # total_horse_number  

    race_refined_list = [] 
   
    # horse data
    for order in range(2, len(result_rows)):
        horse_list = []                     #temporary list
        result_row = result_rows[order].findAll("td")
        # order
        horse_list.append("?")
        # frame_number
        horse_list.append(result_row[0].get_text())
        # horse_number
        horse_list.append(result_row[1].get_text())
        # horse_id
        horse_list.append(result_row[3].find('a').get('href').split("/")[-1])
        # sex_and_age
        horse_list.append(result_row[4].get_text())
        # burden_weight
        horse_list.append(result_row[5].get_text())
        # jockey_id
        horse_list.append(result_row[6].find('a').get('href').split("/")[-2])
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
        horse_list.append(result_row[9].find('span').get_text())
        # popular
        #horse_list.append(result_row[13].get_text())
        # horse_weight
        horse_list.append("?")
        # tame_time(premium)
        #horse_list.append(result_row[15].get_text())
        # 16: comments 17:additional information
        # tamer_id
        #horse_list.append(result_row[18].find('a').get('href').split("/")[-2])
        # owner_id
        #horse_list.append(result_row[19].find('a').get('href').split("/")[-2])
        

        race_refined_list.append(race_list + horse_list) #race_data + horse_data 

    
    return race_refined_list # one race data with horse   [[race, horse1], [race, horse2] ,,,]
