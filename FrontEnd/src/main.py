# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import json
import pandas as pd
import numpy as np
import os
import httpx




# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
st.session_state.username = ''
def user_update(name):
    st.session_state.username = name

login_form = st.sidebar.form(key='signin_form', clear_on_submit=True)
username = login_form.text_input(label='Enter Username')
user_pas = login_form.text_input(label='Enter Password', type='password')
if(httpx.post("http://172.17.0.1:8000/token", data = {'grant_type': '', 'username' : username, 'password' : user_pas, 'scope' : '' , 'client_id' : '', 'client_secret': ''}, headers = {'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'})):
    login = login_form.form_submit_button(label='Sign In', on_click = user_update(username))
mainTitle=st.title ("""hello""" + st.session_state.username)
st.sidebar.success("Select a demo above.")

