"""
create a csv using html in race_html
"""
import datetime
import pytz
now_datetime = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

import os
import time
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



def make_csv_from_this_week_html_selenium(week, date, year_date):
    save_race_csv = CSV_DIR+"/2022"+"/" + week + "/" + date +".csv"
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path = '/usr/bin/chromedriver') 
    driver.implicitly_wait(5)
    
    if not ((os.path.isfile(save_race_csv)) ): # if csv in not created yet
        race_df = pd.DataFrame(columns=race_data_columns )
        url_dir = RACR_URL_DIR + "/2022/" + date + ".txt"
        with open(url_dir, "r") as f:
            urls = f.read().splitlines()
            for url in urls:
                url_arg = url.split("=")
                race_id = url_arg[-2]                  #get race id
                race_list = get_race_data_from_html_selenium(driver, race_id, url, year_date)     #one race_list  with all horse data
                for race in race_list:     #split per horse   [race, horse1] [race, horse2],,,
                    horse_se = pd.Series(race, index=race_df.columns)             
                    race_df = race_df.append(horse_se, ignore_index=True) #complete one month data   [race, horse1]with columns ,,,
            
            race_df.to_csv(save_race_csv, header=True, index=False)     #all data in year to csv
    driver.close()
    driver.quit()

def get_race_data_from_html_selenium(driver, race_id, url, year_date):
    race_list = [race_id]
    # URLにアクセス
    wait = WebDriverWait(driver,10)
    driver.get(url)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)

    # race information
    data_intro_1 = driver.find_element(By.CLASS_NAME, "RaceList_Item01")
    race_list.append(data_intro_1.find_element(By.CLASS_NAME,"RaceNum").text) # race_round
    data_intro_2 = driver.find_element(By.CLASS_NAME,"RaceList_Item02")
    race_list.append(data_intro_2.find_element(By.CLASS_NAME,"RaceName").text.strip("\n")) 
    race_details1 = data_intro_2.find_element(By.CLASS_NAME,"RaceData01").text.strip("\n").split("/")
    race_list.append(race_details1[1]) # race_distance
    race_list.append('晴') # weather 
    race_list.append('良') # ground_condition  
    race_list.append(race_details1[0]) # time
    race_details2 = data_intro_2.find_element(By.CLASS_NAME,"RaceData02").text.split(" ")
    race_list.append(year_date) # date
    race_list.append(race_details2[1]) # place

    result_rows = driver.find_element(By.CLASS_NAME,"RaceTableArea").find_elements_by_tag_name('tr') 
    race_list.append(len(result_rows)-2) # total_horse_number  

    race_refined_list = [] 
   
    # horse data
    for order in range(2, len(result_rows)):
        horse_list = []                     #temporary list
        result_row = result_rows[order].find_elements_by_tag_name("td")
        # order
        horse_list.append("?")
        # frame_number
        horse_list.append(result_row[0].text)
        # horse_number
        horse_list.append(result_row[1].text)
        # horse_id
        horse_list.append(result_row[3].find_element_by_tag_name("a").get_attribute("href").split("/")[-1])
        # sex_and_age
        horse_list.append(result_row[4].text)
        # burden_weight
        horse_list.append(result_row[5].text)
        # jockey_id
        horse_list.append(result_row[6].find_element_by_tag_name("a").get_attribute("href").split("/")[-2])
        # goal_time
        horse_list.append("?")
        # goal_time_dif
        #horse_list.append(result_row[8].text)
        # time_value(premium)
        #horse_list.append(result_row[9].text)
        # half_order
        horse_list.append("?")
        # last_time()
        horse_list.append("?")
        # odds
        horse_list.append(result_row[9].text)
        # popular
        #horse_list.append(result_row[13].text)
        # horse_weight
        horse_list.append("?")
        # tame_time(premium)
        #horse_list.append(result_row[15].text)
        # 16: comments 17:additional information
        # tamer_id
        #horse_list.append(result_row[18].find('a').get('href').split("/")[-2])
        # owner_id
        #horse_list.append(result_row[19].find('a').get('href').split("/")[-2])
        

        race_refined_list.append(race_list + horse_list) #race_data + horse_data 

    
    return race_refined_list # one race data with horse   [[race, horse1], [race, horse2] ,,,]
