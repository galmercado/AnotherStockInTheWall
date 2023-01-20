# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import json
import pandas as pd
import numpy as np
import os
import httpx
from dateutil.relativedelta import *
import datetime
#DATA_URL1 = "C:\Users\User\Desktop\BGU\gal\test"
#DATA_URL = 'test'
#columns=["name", "email"]


def getSpecRange(username, startDate, endDate):
    return httpx.get('http://172.17.0.1:8000/getStocksByUser?username=' + st.session_state.username + "&startDate=" + startDate.strftime("%x") + "&endDate=" 
                    + endDate.strftime("%x"), timeout = 15.0).json()
# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
if (st.session_state.username):
   mainTitle=st.title ("""hello """ + st.session_state.username)
   username = st.session_state.username
   start_date = st.date_input(label = "Start Date", value = (datetime.date.today() - datetime.timedelta(days = 7)))
   end_date = st.date_input(label = "End Date", value = datetime.date.today())
   btn_cust_range = st.button(label = "show custom date range")
   btn_week_range = st.button(label = "show last week")
   btn_month_range = st.button(label = "show last month")
   btn_3month_range = st.button(label = "show 3 months")
   btn_year_range = st.button(label = "show last year")
   if (btn_cust_range or btn_week_range or btn_month_range or btn_3month_range or btn_year_range):
       if (btn_cust_range):
           js = getSpecRange(username, start_date, end_date)
       if(btn_week_range):
           js = getSpecRange(username, datetime.date.today() -  relativedelta(days = 7), datetime.date.today())
       if (btn_month_range):
           js = getSpecRange(username, datetime.date.today() - relativedelta(months = 1), datetime.date.today())
       if(btn_3month_range):
           js = getSpecRange(username, datetime.date.today() - relativedelta(months = 3), datetime.date.today())
       if(btn_year_range):
           js = getSpecRange(username, datetime.date.today() - relativedelta(years = 1), datetime.date.today())
       df = pd.DataFrame.from_dict(js)
       df.index = pd.to_datetime(df.index)
       st.line_chart(df)



