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



# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
mainTitle=st.title ("""hello Gal""")
but=st.button("Submit")
title=st.text_input("testing text","Enter Stock name")

if (but):
	st.write(title)
	data = pd.read_json(httpx.get('http://172.17.0.1:8000/getStocks/' + title))
	data1=pd.DataFrame(data)
	table=st.table(data1)


