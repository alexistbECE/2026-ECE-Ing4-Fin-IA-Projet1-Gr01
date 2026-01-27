import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicates and handle missing values.
    """
    if df is None or df.empty:
        return df
        
    df = df.drop_duplicates()
    # Sort by date just in case
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
    return df

def merge_data(prices, technicals, macro):
    """
    Merge Prices, Technicals (on ticker, date) and Macro (on date).
    """
    print("Merging data...")
    # Base is prices
    df = prices.copy()
    
    # Merge Technicals
    if technicals is not None and not technicals.empty:
        # Ensure dates are datetime
        technicals['date'] = pd.to_datetime(technicals['date'])
        # Drop duplicates in technicals just in case
        technicals = technicals.drop_duplicates(subset=['ticker', 'date'])
        df = pd.merge(df, technicals, on=['ticker', 'date'], how='left', suffixes=('', '_tech'))
    
    # Merge Macro
    # Macro data might be long format (series_id, date, value) -> Pivot to wide
    if macro is not None and not macro.empty:
        macro['date'] = pd.to_datetime(macro['date'])
        # Pivot macro: index=date, columns=name/series_id, values=value
        # We assume 'name' or 'series_id' identifies the feature
        # Let's use 'name' if available and unique per date, else 'series_id'
        pivot_col = 'name' if 'name' in macro.columns else 'series_id'
        
        # Remove duplicates
        macro = macro.drop_duplicates(subset=['date', pivot_col])
        
        macro_wide = macro.pivot(index='date', columns=pivot_col, values='value')
        macro_wide = macro_wide.sort_index().fillna(method='ffill') # Forward fill macro data
        
        # Reset index to make 'date' a column again for merge
        macro_wide = macro_wide.reset_index()
        
        # Merge on date
        df = pd.merge(df, macro_wide, on='date', how='left')
        
    return df

def create_target(df: pd.DataFrame, horizon: int = 20) -> pd.DataFrame:
    """
    Create binary target: 1 if Return(t+horizon) > 0, else 0.
    """
    if df.empty:
        return df
        
    # Ensure sorted
    df = df.sort_values(['ticker', 'date'])
    
    # Calculate forward return
    # shift(-horizon) gets the price at t+horizon
    df['close_future'] = df.groupby('ticker')['close'].shift(-horizon)
    
    df['fwd_return'] = (df['close_future'] / df['close']) - 1
    df['target'] = (df['fwd_return'] > 0).astype(int)
    
    # Drop rows where target cannot be calculated (unknown future)
    valid_df = df.dropna(subset=['close_future'])
    
    return valid_df

def temporal_split(df: pd.DataFrame, train_ratio: float = 0.7, val_ratio: float = 0.15):
    """
    Strict temporal split: Train < Val < Test
    """
    if df.empty:
        return df, df, df
        
    dates = df['date'].sort_values().unique()
    n = len(dates)
    
    train_end = dates[int(n * train_ratio)]
    val_end = dates[int(n * (train_ratio + val_ratio))]
    
    train = df[df['date'] <= train_end]
    val = df[(df['date'] > train_end) & (df['date'] <= val_end)]
    test = df[df['date'] > val_end]
    
    print(f"Split details:")
    print(f"Train: {train['date'].min()} -> {train['date'].max()} ({len(train)} rows)")
    print(f"Val:   {val['date'].min()}   -> {val['date'].max()}   ({len(val)} rows)")
    print(f"Test:  {test['date'].min()}  -> {test['date'].max()}  ({len(test)} rows)")
    
    return train, val, test
