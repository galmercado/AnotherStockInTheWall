import json
from fastapi import FastAPI
from pydantic import BaseModel
from stockApi import *
class Payload(BaseModel):
    data: str = ""

app = FastAPI()

@app.get("/")
def welcome():
    return "Welcome <3"

@app.get("/getStocks/{lstStocks}")
def getStocks(lstStocks):
    print("HHEHEHHEHEHEHE" + lstStocks)
    return get_stock(symbol = lstStocks, is_api = True)
