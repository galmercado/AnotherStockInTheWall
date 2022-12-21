import json
from fastapi import FastAPI
from pydantic import BaseModel
from stockApi import *
from pymongo import MongoClient
class Payload(BaseModel):
    data: str = ""

class stocksToUser(BaseModel):
    lstStock: list
    userid: str

app = FastAPI()
app.mongoClient = MongoClient("database:27017")


@app.get("/")
def welcome():
    return "Welcome <3"

@app.get("/getStocks/{lstStocks}")
def getStocks(lstStocks):
    return get_stock(symbol = lstStocks, is_api = True)

@app.get("/getStockDate/")
def getStocksByDate(stock: str = "", startDate:str = "2022-12-12", endDate:str = "2022-12-19"):
    return get_stock(symbol = stock, start_date = startDate, end_date = endDate, is_api = True)

@app.post("/addStocksToFavourite/")
def addStockToDB(stock: stocksToUser):
    return stock #TODO: add to DB, in the meantime just returns the item
