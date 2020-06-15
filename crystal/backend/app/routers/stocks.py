from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import json

router = APIRouter()


@router.get("/")
def availableStocks():
    stocks = pd.read_csv('app/data/spxCodes.csv')
    stocksJSON = stocks.to_json(orient='records')
    return json.loads(stocksJSON)
