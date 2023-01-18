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
DATA_URL = 'test'
#columns=["name", "email"]


data = pd.read_json(httpx.get('http://172.17.0.1:8000/getStocks/AAPL'))
data1=pd.DataFrame(data)

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
mainTitle=st.title ("""hello Gal""")
table=st.table(data1)
but=st.button("Good Morning gal")
title: str=st.text_input("testing text","Enter your text here")

if (but):
	title = ("what we want to do with it ?")
	st.write(title)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
