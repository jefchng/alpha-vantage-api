import datetime as dt

from fastapi import FastAPI

from app import service
from app.service import LookupResponse, MaxPriceResponse, MinPriceResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lookup/{symbol}/{date}")
async def lookup(
    symbol: str,
    date: dt.date,
) -> LookupResponse:
    return service.lookup(symbol, date)


@app.get("/min/{symbol}")
async def min(
    symbol: str,
    n: int,
) -> MinPriceResponse:
    return service.min_price(symbol, n)


@app.get("/max/{symbol}")
async def max(
    symbol: str,
    n: int,
) -> MaxPriceResponse:
    return service.max_price(symbol, n)
