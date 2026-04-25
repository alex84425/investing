import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

def fetch_yahoo_data(ticker):
    """
    Fetch 5 years of daily data from Yahoo Finance API using requests.
    """
    print(f"Fetching data for {ticker}...")
    # Yahoo Finance Chart API
    # range=5y, interval=1d
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5y&interval=1d"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]
        adj_close = result['indicators']['adjclose'][0]['adjclose']
        
        df = pd.DataFrame({
            'Date': pd.to_datetime(timestamps, unit='s'),
            'Adj Close': adj_close
        })
        
        df.set_index('Date', inplace=True)
        # Remove timezone info to make it tz-naive for alignment
        df.index = df.index.tz_localize(None)
        
        return df['Adj Close']
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def analyze_nanya_micron():
    tickers = {'2408.TW': 'Nanya Tech', 'MU': 'Micron'}
    
    # Fetch data
    series_list = []
    for ticker in tickers:
        s = fetch_yahoo_data(ticker)
        if s is not None:
            s.name = ticker
            series_list.append(s)
        else:
            print(f"Failed to fetch data for {ticker}. Aborting.")
            return

    # Combine into DataFrame
    data = pd.concat(series_list, axis=1)
    data.columns = tickers.keys()
    
    # Drop NaN values (alignment)
    data = data.dropna()
    
    if data.empty:
        print("No overlapping data found.")
        return

    print(f"\nData range: {data.index.min().date()} to {data.index.max().date()}")
    print(f"Number of overlapping trading days: {len(data)}")

    # Normalize data to start at 100
    normalized_data = (data / data.iloc[0]) * 100
    
    # Calculate Daily Returns
    returns = data.pct_change().dropna()
    
    # Calculate Correlation
    correlation = returns.corr().iloc[0, 1]
    print(f"\nCorrelation between Nanya Tech (2408.TW) and Micron (MU): {correlation:.4f}")
    
    # Lead-Lag Analysis
    lags = range(-10, 11)
    corrs = []
    
    # returns['2408.TW'] vs returns['MU'].shift(lag)
    # lag > 0: MU(t-lag) vs 2408(t). If high, MU leads.
    
    for lag in lags:
        if lag == 0:
            c = returns['2408.TW'].corr(returns['MU'])
        else:
            c = returns['2408.TW'].corr(returns['MU'].shift(lag))
        corrs.append((lag, c))
        
    print("\nLead-Lag Cross-Correlation (Daily Returns):")
    print("Lag > 0 means MU leads (MU's past predicts Nanya's current)")
    print("Lag < 0 means Nanya leads (Nanya's past predicts MU's current)")
    print("-" * 40)
    print(f"{'Lag (Days)':<10} | {'Correlation':<15}")
    print("-" * 40)
    
    best_lag = 0
    best_corr = 0
    
    for lag, c in corrs:
        print(f"{lag:<10} | {c:.4f}")
        if abs(c) > abs(best_corr):
            best_corr = c
            best_lag = lag
            
    print("-" * 40)
    print(f"Highest correlation {best_corr:.4f} occurs at lag {best_lag}")
    
    if best_lag > 0:
        print(f"Interpretation: Micron (MU) leads Nanya Tech (2408.TW) by {best_lag} day(s).")
    elif best_lag < 0:
        print(f"Interpretation: Nanya Tech (2408.TW) leads Micron (MU) by {abs(best_lag)} day(s).")
    else:
        print("Interpretation: They move simultaneously (no significant daily lead/lag observed).")

    # Plotting
    try:
        plt.figure(figsize=(14, 7))
        plt.plot(normalized_data.index, normalized_data['2408.TW'], label='Nanya Tech (2408.TW)')
        plt.plot(normalized_data.index, normalized_data['MU'], label='Micron (MU)')
        
        plt.title('Nanya Tech vs Micron - 5 Year Price Comparison (Normalized)')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price (Start = 100)')
        plt.legend()
        plt.grid(True)
        
        output_file = 'nanya_micron_comparison.png'
        plt.savefig(output_file)
        print(f"\nChart saved to {output_file}")
    except Exception as e:
        print(f"Error plotting: {e}")

if __name__ == "__main__":
    analyze_nanya_micron()
