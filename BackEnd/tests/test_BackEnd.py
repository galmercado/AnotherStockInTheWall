from main import *
import requests
import json
import pandas as pd
from fastapi.testclient import TestClient


aapl_golden_json = {"adjclose":{"2022-12-12T00:00:00":144.49000549316406,"2022-12-13T00:00:00":145.47000122070312,"2022-12-14T00:00:00":143.2100067138672,"2022-12-15T00:00:00":136.5,"2022-12-16T00:00:00":134.50999450683594},
"ticker":{"2022-12-12T00:00:00":"AAPL","2022-12-13T00:00:00":"AAPL","2022-12-14T00:00:00":"AAPL","2022-12-15T00:00:00":"AAPL","2022-12-16T00:00:00":"AAPL"}}

client = TestClient(app)

def test_getStocks():
    response = client.get("getStockDate/?stock=AAPL&startDate=2022-12-12&endDate=2022-12-19")
    assert response.json() == aapl_golden_json



def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome <3"

