# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import json
import pandas as pd
import numpy as np
import os
import httpx
import json
from dotenv import load_dotenv
import jwt

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
load_dotenv()
st.session_state.username = ''
st.session_state.token = ''
def user_update(token):
    try:
        st.session_state.token = jwt.decode(token, "f3ad56778d7ca1e1fc7ff8532e89c88de32501ea9e56a5902aeef6ad65e1415c", algorithms = "HS256")
        st.session_state.username = st.session_state.token["sub"]
    except Exception as e:
        st.write(e)
    
def authenticate_user(username, password):
    resJSON = httpx.post("http://172.17.0.1:8000/token", data = {'grant_type': '', 'username' : username, 'password' : password, 'scope' : '' , 'client_id' : '', 'client_secret': ''}, headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}).json()
    try:
        user_update(resJSON["access_token"])
    except:
        return
login_form = st.sidebar.form(key='signin_form', clear_on_submit=True)
username = login_form.text_input('Enter Username', placeholder = "user", key = "a")
password = login_form.text_input('Enter Password', placeholder = "pass", key = "b", type='password')
login = login_form.form_submit_button(label='Sign In')
if (login):
    authenticate_user(username, password)
    st.sidebar.success("Hi " + st.session_state.username)
    st.title("Welcome to our site")
    st.write("Logged in succesfuly")
