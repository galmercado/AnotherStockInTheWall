import streamlit as st
import httpx
import json


if(st.session_state.username):
    lst500 = httpx.get("http://172.17.0.1:8000/getlstsp500/").json()
    stocks = st.multiselect(label = "choose stocks", options = lst500)
    btn = st.button(label = "select")
    if (btn):
        addToDB = httpx.post("http://172.17.0.1:8000/addStocksToFavourite/", data = json.dumps({'lstStock': stocks, 'username': st.session_state.username}), 
                            headers = {'Content-Type': 'application/json', 'accept': 'application/json'})
        st.write(Success)
