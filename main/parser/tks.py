import json

import requests, os
from .models import Share
from datetime import timedelta
from tinkoff.invest import Client, CandleInterval
from tinkoff.invest.utils import now


TOKEN = os.environ["INVEST_TOKEN"]


def get_5minutes_candles(request, ticker_figi):
    candle_data = []
    with Client(TOKEN) as client:
        for candle in client.get_all_candles(
            figi=ticker_figi,
            from_=now() - timedelta(days=2),
            interval=CandleInterval.CANDLE_INTERVAL_5_MIN,
        ):
            candle_data.append(
                {
                    'open': {'units': candle.open.units, 'nano': candle.open.nano},
                    'high': {'units': candle.high.units, 'nano': candle.high.nano},
                    'low': {'units': candle.low.units, 'nano': candle.low.nano},
                    'close': {'units': candle.close.units, 'nano': candle.close.nano},
                    'time': candle.time,
                    'volume': candle.volume,
                    'is_complete': candle.is_complete
                }
            )
    print(candle_data)
    return candle_data

