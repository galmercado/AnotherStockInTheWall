import json
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def welcome():
    return "Welcome <3"
