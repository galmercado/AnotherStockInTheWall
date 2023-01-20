# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import json
import pandas as pd
import numpy as np
import os
import httpx

#DATA_URL1 = "C:\Users\User\Desktop\BGU\gal\test"
#DATA_URL = 'test'
#columns=["name", "email"]



# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
if (st.session_state.username):
   mainTitle=st.title ("""hello """ + st.session_state.username)
   js = httpx.get('http://172.17.0.1:8000/getStocksByUser?username=' + st.session_state.username, timeout = 15.0).json()
   df = pd.DataFrame.from_dict(js)
   df.index = pd.to_datetime(df.index)
   st.line_chart(df)



