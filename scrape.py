import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date, timedelta
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# GOAL 1: OPEN WEBSITE AND GET THE HTML FOR THE SCHEDULE

# Use requests and webdriver to get the MLS site
# Creating new driver for Firefox
driver = webdriver.Firefox()
fireFoxOptions= Options()
fireFoxOptions.add_argument("--headless")

today = date.today()
next_week = today + timedelta(days=7)

# Launch website--la galaxy site didn't work but mls does?
link = "https://www.mlssoccer.com/schedule/#competition=all&club=MLS-CLU-00000G&date=" + str(today)
driver.get(link)
time.sleep(15)
div_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "mls-c-schedule__matches"))
)

# Get the HTML content directly from Selenium element
inner_html = div_element.get_attribute('innerHTML')


# Parse with BeautifulSoup
soup = BeautifulSoup(inner_html, "html.parser")

# get the game info for this week !!!
date_div = soup.findAll('div', class_='sc-iJnaPW gtujJv mls-c-status-stamp__status -pre')

cup_div = soup.findAll('div', class_='sc-eDvSVe jOWTAi mls-c-explainer-bar')

team_span = soup.findAll('span', class_='mls-c-club__shortname')

time_div = soup.findAll('div', class_ = 'sc-jSUZER dhPUPP mls-c-scorebug mls-c-scorebug--horizontal')

location_div = soup.findAll('p', class_ = 'sc-iveFHk fMBbsK')

print("done collecting data")

print("there are ", len(date_div), " game(s) this week")   
print()
index_of_cup = 0
index_of_team = 0
flag = False 
for i in range(0, len(date_div)):
    print("game #", i+1, " details:")
    print("date: ", date_div[i].text)
    print("time: ", time_div[i].text)
    if cup_div[index_of_cup].text == "MLS Regular Season":
        print("cup: ", cup_div[index_of_cup].text)
        index_of_cup = index_of_cup + 1
    else:
        print("cup: ", cup_div[index_of_cup].text, cup_div[index_of_cup + 1].text)
        index_of_cup = index_of_cup + 2
    print("team 1: ", team_span[index_of_team].text, " team 2: ", team_span[index_of_team + 1].text)
    index_of_team += 2
    print("location: ", location_div[i].text)
    i = i + 1
    print()


