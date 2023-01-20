import json
from fastapi import FastAPI
from pydantic import BaseModel
from stockApi import *
from pymongo import MongoClient
import pymongo
import pandas as pd
from config import settings

class Payload(BaseModel):
    data: str = ""

class stocksToUser(BaseModel):
    lstStock: list
    username: str

app = FastAPI()
app.mongoClient = MongoClient(settings.DATABASE_URL)
db = app.mongoClient[settings.MONGO_INITDB_DATABASE]
app.userDB = db["users"]
app.userDB.create_index([("username", pymongo.ASCENDING)], unique=True)
app.stocksDB = db["stocks"]
app.stocksDB.create_index([("username", pymongo.ASCENDING)],unique = True)
@app.get("/")
def welcome():
    return "Welcome <3"

@app.get("/getStock/")
def getStocks(stock):
    return get_stock(stock, is_api = True)

def getStocksFromList(lstStocks: list[str]):
    df = pd.DataFrame()
    for stock in lstStocks:
        df[stock] = get_stock(symbol = stock, is_api = True)["adjclose"]
    return df

@app.get("/getStockDate/")
def getStocksByDate(stock: str = "", startDate:str = "2022-12-12", endDate:str = "2022-12-19"):
    return get_stock(symbol = stock, start_date = startDate, end_date = endDate, is_api = True)

@app.get("/getStocksByUser")
def getStocksByUser(username: str):
    curr_lstStocks = app.stocksDB.find_one({'username': username})["lstStocks"]
    return getStocksFromList(curr_lstStocks)

@app.post("/addStocksToFavourite/")
def addStockToDB(stock: stocksToUser):
    curr_lstStocks = app.stocksDB.find_one({'username': stock.username})["lstStocks"]
    new_lstStocks = {"$set": {'lstStocks' : (curr_lstStocks + stock.lstStock)}}
    app.stocksDB.update_one(filter = {"username": stock.username}, update = new_lstStocks)

@app.get("/getlstsp500/")
def getlstsp500():
    print("****************************")
    return get_lstSP500()


from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    '''if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)'''
    u_dict = app.userDB.find_one({'username': username})
    return UserInDB(**u_dict)
        


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

