#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import psycopg2
from psycopg2 import sql


# Get the current date
current_date = datetime.now()

# Subtract one day from the current date
previous_date = current_date - timedelta(days=12)

# Extract year, month, and day from the previous date
year = previous_date.year
month = previous_date.month
day = previous_date.day
def find_endpoints(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a')
        endpoints = [urljoin(url, link.get('href')) for link in all_links if link.get('href') and '/boxes' in link.get('href') and link.get('href').endswith('.shtml')]
        return endpoints
    else:
        print("Failed to retrieve data")
        return None
# URL of the page containing the box scores
url = f"https://www.baseball-reference.com/boxes/?year={year}&month={month}&day={day}"
# Find endpoints
endpoints = find_endpoints(url)
if endpoints:
    print("List of endpoints:")
    for endpoint in endpoints:
        print(endpoint)
else:
    print("No endpoints found.")

print('done')


###Need to edit this function
def get_stat_data(link_list, type):
    soup_list = []
    for i in link_list:
        chrome_options = Options()
	chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        driver.get(i)
        time.sleep(5)

        if type == 'batting':
            stat_elements = ["/html[1]/body[1]/div[2]/div[4]/div[5]/div[1]/div[1]/ul[1]/li[1]",
                             "/html[1]/body[1]/div[2]/div[4]/div[6]/div[1]/div[1]/ul[1]/li[1]"]
        else:
            stat_elements = ["/html[1]/body[1]/div[2]/div[4]/div[8]/div[3]/div[1]/div[1]/div[1]/ul[1]/li[1]",
                             "/html[1]/body[1]/div[2]/div[4]/div[8]/div[3]/div[2]/div[1]/div[1]/ul[1]/li[1]"]
        i = 0
        for element in stat_elements:
            button = driver.find_element(By.XPATH, element)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", button)
            time.sleep(2)
            button.click()
            element = element + "/div/ul/li[3]/button"
            time.sleep(1)
            driver.find_element(By.XPATH, element).click()
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if type == 'batting':
                elements = soup.find_all(
                    lambda tag: tag.has_attr('id') and tag['id'].startswith('csv') and tag['id'].endswith('batting'))
            else:
                elements = soup.find_all(
                    lambda tag: tag.has_attr('id') and tag['id'].startswith('csv') and tag['id'].endswith('pitching'))
            csv = elements[i].text.split("\n")
            i = i + 1
            soup_list.append(csv)
        print('done')
    return soup_list
raw_batting_data = get_stat_data(endpoints, 'batting')
raw_pitching_data = get_stat_data(endpoints, 'pitching')
print('done')


def clean_csv(csv, type):
    no_blank = []
    for i in csv:
        for j in i:
            if j != '':
                no_blank.append(j)
        new_data_split = []
    for i in no_blank:
        new_line = pd.DataFrame(i.split(','))
        new_data_split.append(new_line)
    season_data = pd.concat(new_data_split, ignore_index = True, axis = 1).T
    header = season_data.iloc[2]
    season_data = season_data[3:]
    season_data.columns = header
    if type == 'batting':
        season_data = season_data[
            (season_data['AB'].notnull()) & (season_data['Batting'] != 'Team Totals') & (season_data['AB'] != '')
            & (season_data['Batting'] != 'Batting') & (season_data['R'].notnull())]
    else:
        season_data = season_data[
            (season_data['IP'].notnull()) & (season_data['Pitching'] != 'Team Totals') & (season_data['IP'] != '')
            & (season_data['Pitching'] != 'Pitching') & (season_data['H'].notnull())]
    season_data.replace('', pd.NA, inplace=True)
    season_data['cWPA'] = season_data['cWPA'].str.replace('%', '')
    return season_data

pitching_data_csv = clean_csv(raw_pitching_data, 'pitching')
pitching_data_csv['upload_dttm'] = previous_date
batting_data_csv = clean_csv(raw_batting_data, 'batting')
batting_data_csv['upload_dttm'] = previous_date
pitching_data_csv.rename(columns={col: col.lower() for col in pitching_data_csv.columns}, inplace=True)
batting_data_csv.rename(columns={col: col.lower() for col in  batting_data_csv.columns}, inplace=True)
batting_data_csv.rename(columns={'wpa+': 'wpaplus', 'wpa-': 'wpaminus'}, inplace=True)


##insert data
conn_params = {
    'dbname': 'db_init',
    'user': 'csca5028',
    'password': 'csca5028',
    'host': 'csca5028-db-instance.c1a04q2cyd4h.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# Insert for Pitching Data
table_name = 'pitching_data'
columns = pitching_data_csv.columns.tolist()
insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
    sql.Identifier(table_name),
    sql.SQL(', ').join(map(sql.Identifier, columns)),
    sql.SQL(', ').join(sql.Placeholder() * len(columns))
)
pitching_data_csv = pitching_data_csv.where(pd.notnull(pitching_data_csv), None)
data = [tuple(x) for x in pitching_data_csv.to_numpy()]
cur.executemany(insert_statement, data)
conn.commit()

# Insert for Batting Data
table_name = 'batting_data'
columns = batting_data_csv.columns.tolist()
insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
    sql.Identifier(table_name),
    sql.SQL(', ').join(map(sql.Identifier, columns)),
    sql.SQL(', ').join(sql.Placeholder() * len(columns))
)
batting_data_csv = batting_data_csv.where(pd.notnull(batting_data_csv), None)
data = [tuple(x) for x in batting_data_csv.to_numpy()]
cur.executemany(insert_statement, data)
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
print('done')
