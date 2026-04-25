import yfinance as yf
import pandas as pd
import numpy as np

def analyze_pgy_history():
    ticker = "PGY"
    print(f"Downloading data for {ticker}...")
    # Download max history
    df = yf.download(ticker, period="max", progress=False)
    
    if df.empty:
        print("No data found.")
        return

    # Handle columns
    print(f"Columns: {df.columns}")
    price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
    
    # Handle MultiIndex if present
    if isinstance(df.columns, pd.MultiIndex):
        try:
            df = df.xs(ticker, axis=1, level=1)
            price_col = 'Close'
        except:
            pass
            
    if price_col not in df.columns:
        price_col = 'Close'

    # Calculate Drawdown from ATH
    df['ATH'] = df[price_col].cummax()
    df['Drawdown'] = (df[price_col] - df['ATH']) / df['ATH']
    
    current_price = df[price_col].iloc[-1]
    ath_price = df['ATH'].iloc[-1]
    current_drawdown = df['Drawdown'].iloc[-1]
    
    print("-" * 50)
    print(f"PGY Analysis ({df.index[0].date()} to {df.index[-1].date()})")
    print(f"Current Price: ${current_price:.2f}")
    print(f"All-Time High: ${ath_price:.2f}")
    print(f"Current Drawdown: {current_drawdown:.2%}")
    print("-" * 50)
    
    # Volatility (Annualized)
    daily_ret = df[price_col].pct_change()
    volatility = daily_ret.std() * np.sqrt(252)
    print(f"Annualized Volatility: {volatility:.2%}")
    
    # Recent Support/Resistance (Last 1 year)
    last_year = df.last('12M') # deprecated, use slice
    # Actually just slice last 252 days
    last_year = df.iloc[-252:] if len(df) > 252 else df
    
    year_high = last_year[price_col].max()
    year_low = last_year[price_col].min()
    
    print(f"52-Week High: ${year_high:.2f}")
    print(f"52-Week Low: ${year_low:.2f}")
    
    # Moving Averages
    ma_50 = df[price_col].rolling(window=50).mean().iloc[-1]
    ma_200 = df[price_col].rolling(window=200).mean().iloc[-1]
    
    print(f"50-Day MA: ${ma_50:.2f}")
    print(f"200-Day MA: ${ma_200:.2f}")
    
    print("-" * 50)
    print("Price Distribution (Volume Profile Proxy):")
    # Simple histogram of prices in the last year
    hist, bins = np.histogram(last_year[price_col], bins=10)
    for i in range(len(hist)):
        print(f"${bins[i]:.2f} - ${bins[i+1]:.2f}: {hist[i]} days")

if __name__ == "__main__":
    analyze_pgy_history()
