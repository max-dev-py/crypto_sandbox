import pandas as pd
import requests

URL = "https://api.binance.com/api/v3/klines"


def get_df(symbol="BTCUSDT", interval="1d", limit=1000):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


import ccxt

def get_ccxt_df(symbol="BTC/USDT", timeframe='1d', limit=1000):
    # Instantiate the exchange
    exchange = ccxt.bybit({
        "timeout": 30000,
        "rateLimit": 2000,
    })

    # Fetch OHLCV data
    data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume"
    ])

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

