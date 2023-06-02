import datetime as dt
from collections import OrderedDict
from typing import Optional

import requests
from cachetools import TTLCache, cached
from pydantic import BaseModel

from app.settings import get_settings

ALPHA_VANTAGE_QUERY_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_QUERY_FUNCTION = "TIME_SERIES_DAILY_ADJUSTED"
ALPHA_VANTAGE_COMPACT_OUTPUT_SIZE = "compact"
CACHE_SIZE = 100
CACHE_TTL = 60 * 60  # 1 hour

settings = get_settings()


class Data(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int

    @classmethod
    def from_av_response(cls, raw_response):
        return cls(
            **{
                "open": raw_response.get("1. open"),
                "high": raw_response.get("2. high"),
                "low": raw_response.get("3. low"),
                "close": raw_response.get("4. close"),
                "volume": raw_response.get("6. volume"),
            }
        )


class LookupResponse(Data):
    pass


class MinPriceResponse(BaseModel):
    min: float


class MaxPriceResponse(BaseModel):
    max: float


def lookup(symbol: str, date: dt.date) -> Optional[Data]:
    daily_time_series_data = get_daily_time_series(symbol)
    return daily_time_series_data.get(date)


def min_price(symbol: str, n: int):
    n = min(n, 100)
    return MinPriceResponse(
        min=min([data.low for data in list(get_daily_time_series(symbol).values())[:n]])
    )


def max_price(symbol: str, n: int):
    n = min(n, 100)
    return MaxPriceResponse(
        max=max(
            [data.high for data in list(get_daily_time_series(symbol).values())[:n]]
        )
    )


@cached(cache=TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL))
def get_daily_time_series(symbol: str) -> dict[dt.date, Data]:
    params = {
        "function": ALPHA_VANTAGE_QUERY_FUNCTION,
        "symbol": symbol,
        "outputsize": ALPHA_VANTAGE_COMPACT_OUTPUT_SIZE,
        "apikey": settings.alpha_vantage_api_key,
    }
    r = requests.get(ALPHA_VANTAGE_QUERY_URL, params)

    def sort_by_date(data: dict[dt.date, Data]):
        return OrderedDict(
            (date, data)
            for date, data in sorted(
                [(key, value) for key, value in data.items()],
                key=lambda x: x[0],
            )
        )

    if r.status_code == 200:
        return sort_by_date(
            {
                dt.date.fromisoformat(key): Data.from_av_response(value)
                for key, value in r.json().get("Time Series (Daily)").items()
            }
        )
    r.raise_for_status()
