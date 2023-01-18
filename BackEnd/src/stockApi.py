import requests 
import pandas as pd
START_DATE = "2022-04-15"
END_DATE = "2023-01-01"

from yahoo_fin.stock_info import get_data as get_stock_data
def collect_api(url, is_stock = False):
  # Make a get request.
  response = requests.get(url)
  response_d = response.content.decode("utf-8")
  if (is_stock):
    #The json comes as dictionary from marketshare api, pandas doesn't need read_json in such a case :O
    df = pd.DataFrame(response.json()["data"])
  
  else:
    df = pd.read_json(response_d)
  return df

#Gets stock dataframe in date timeline, uses either yahoo-fi api or my very own crawler
def get_stock(symbol, start_date = START_DATE, end_date = END_DATE,
              date_format = '%Y-%m-%d', is_api = False):
    #Returns df with close prices from the first day of covid data to Jan 27th 2022
  if is_api:
    df = get_stock_data(symbol, start_date, end_date).filter(["adjclose", "ticker"])
  else:
      df = collect_crawling(symbol, start_date, end_date, date_format).filter(["adjclose", "ticker"])
  
  return df

import sys
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import bs4
import time
from bs4 import BeautifulSoup 
from selenium import webdriver
from datetime import datetime
from io import StringIO
def collect_crawling(stock_name, str_start_date, str_end_date, date_format):
  start_date = datetime.strptime(str_start_date, date_format)
  end_date = datetime.strptime(str_end_date, date_format)
  s = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
  url = "https://finance.yahoo.com/quote/"+ stock_name + "/history?period1=" + str(int(start_date.timestamp())) + "&period2=" + str(int(end_date.timestamp())) + "&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
  s.get(url)

  #Scroll down enough times that the whole table will be shown
  SCROLL_PAUSE_TIME = 0.01
  # Get scroll height
  last_height = s.execute_script("return document.documentElement.scrollHeight")
  while True:
      # Scroll down to bottom
      s.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
      # Wait to load page
      time.sleep(SCROLL_PAUSE_TIME)
      # Calculate new scroll height and compare with last scroll height
      new_height = s.execute_script("return document.documentElement.scrollHeight")
      if new_height == last_height:
          break
      last_height = new_height

  bsPage = BeautifulSoup(s.page_source, 'lxml')
  c_Table = bsPage.find('table', class_='W(100%) M(0)')
  try:
    c_Table_Rows = c_Table.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')
  except:
    #Not found
    return pd.DataFrame()
  c_data = []
  for row in c_Table_Rows:
    rowAsDict = {}
    Values = row.find_all('td')
  
  # Values (Open, High, Close etc.) are extracted and stored in dictionary
    if len(Values) == 7:
      rowAsDict["Date"] = Values[0].find('span').text.replace(',', '')
      try:
        rowAsDict["Open"] = Values[1].find('span').text.replace(',', '')
      except: 
        rowAsDict["Open"] = ""
      try:
        rowAsDict["High"] = Values[2].find('span').text.replace(',', '')
      except:
        rowAsDict["High"] = ""
      try:
        rowAsDict["Low"] = Values[3].find('span').text.replace(',', '')
      except:
        rowAsDict["Low"] = ""
      try:
        rowAsDict["Close"] = Values[4].find('span').text.replace(',', '')
      except:
        rowAsDict["Close"] = ""
      try:
        rowAsDict["Adj Close"] = Values[5].find('span').text.replace(',', '')
      except:
        rowAsDict["Adj Close"] = ""
      try:
        rowAsDict["Volume"] = Values[6].find('span').text.replace(',', '') 
      except:
         rowAsDict["Volume"] = ""
      # Dictionary is appended in list
      c_data.append(rowAsDict)
  df = pd.DataFrame(c_data)
  df = df.set_index("Date")
  df = df.rename(index = lambda s: datetime.strptime(s, "%b %d %Y"))
  df = df.rename(columns={"Adj Close": "adjclose"})
  df["ticker"] = stock_name
  return(df)
