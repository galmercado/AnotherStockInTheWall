import streamlit as st
import httpx
import json
from io import StringIO


@st.cache(hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True)
def getLst500():
    return httpx.get("http://172.17.0.1:8000/getlstsp500/", timeout = 10.0).json()
    
@st.experimental_memo
def getCurrLstStock():
    return httpx.get("http://172.17.0.1:8000/getStocksByUser?username=" + st.session_state.username, timeout = 15.0).json()
    

if(st.session_state.username):
    curr_lst_stock = getCurrLstStock()
    lst500 = getLst500()
    stocks = st.multiselect(label = "choose stocks", options = lst500, default = curr_lst_stock)
    btn = st.button(label = "select")
    if (btn):
        addToDB = httpx.post("http://172.17.0.1:8000/addStocksToFavourite/", data = json.dumps({'lstStock': stocks, 'username': st.session_state.username}), 
                            headers = {'Content-Type': 'application/json', 'accept': 'application/json'})
        st.write("Success")
        st.experimental_memo.clear()
