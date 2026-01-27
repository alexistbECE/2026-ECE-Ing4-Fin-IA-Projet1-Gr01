import os
import pandas as pd
import requests
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv('.env.local')

API_KEY = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')
BASE_URL = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
DATA_DIR = Path('data')

def fetch_data(table_name, params=None, cache_file=None, force_reload=False):
    """
    Generic fetcher for Supabase tables.
    """
    if cache_file:
        cache_path = DATA_DIR / cache_file
        if cache_path.exists() and not force_reload:
            print(f"Loading {cache_file} from cache...")
            if cache_file.endswith('.parquet'):
                return pd.read_parquet(cache_path)
            return pd.read_csv(cache_path)

    if not API_KEY or not BASE_URL:
        print("Missing Credentials")
        return None

    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}"
    }
    # Supabase REST: URL/rest/v1/tablename?params
    url = f"{BASE_URL}/rest/v1/{table_name}"
    
    # Supabase uses query params for filtering e.g. ?select=*
    # We default to select=* if not provided
    if params is None:
        params = {"select": "*"}
    elif "select" not in params:
        params["select"] = "*"
    
    print(f"Fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data)
        
        if cache_file:
            print(f"Saving to {cache_file}...")
            if cache_file.endswith('.parquet'):
                df.to_parquet(DATA_DIR / cache_file)
            else:
                df.to_csv(DATA_DIR / cache_file, index=False)
        
        return df
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return None


# Validated Table Names
TABLE_PRICES = "prices_daily"
TABLE_MACRO = "macro_indicators"
TABLE_TECH = "technical_indicators"

def load_prices(tickers=None, start_date=None):
    """
    Fetch OHLCV data from 'prices_daily'.
    """
    params = {"select": "symbol,trade_date,open_price,high_price,low_price,close_price,adj_close,volume"}
    
    if tickers:
        # Supabase syntax for IN: symbol=in.(AAPL,GOOG)
        if isinstance(tickers, list):
            filter_val = f"({','.join(tickers)})"
            params["symbol"] = f"in.{filter_val}"
        else:
             params["symbol"] = f"eq.{tickers}"
             
    if start_date:
        params["trade_date"] = f"gte.{start_date}"

    # Default order
    params["order"] = "trade_date.asc"
    
    df = fetch_data(TABLE_PRICES, params=params, cache_file="prices.parquet")
    
    if df is not None and not df.empty:
        # Standardize columns
        df = df.rename(columns={
            "trade_date": "date",
            "symbol": "ticker",
            "open_price": "open",
            "high_price": "high",
            "low_price": "low",
            "close_price": "close"
        })
        df["date"] = pd.to_datetime(df["date"])
    return df

def load_macro():
    """
    Fetch Macroeconomic data from 'macro_indicators'.
    """
    # Load all macro data (usually smaller than prices)
    df = fetch_data(TABLE_MACRO, cache_file="macro.parquet")
    if df is not None and not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df

def load_technicals(tickers=None):
    """
    Fetch Technical Indicators from 'technical_indicators'.
    """
    params = {"select": "*"}
    if tickers:
        if isinstance(tickers, list):
             params["symbol"] = f"in.({','.join(tickers)})"
        else:
             params["symbol"] = f"eq.{tickers}"
             
    df = fetch_data(TABLE_TECH, params=params, cache_file="technicals.parquet")
    if df is not None and not df.empty:
        df = df.rename(columns={"symbol": "ticker"})
        df["date"] = pd.to_datetime(df["date"])
    return df

