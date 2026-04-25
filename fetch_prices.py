import yfinance as yf
import pandas as pd
from datetime import datetime

def get_option_data(ticker_symbol, expiration_date):
    print(f"Fetching data for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    
    # Get stock price
    stock_price = ticker.history(period="1d")['Close'].iloc[-1]
    print(f"Current Stock Price: ${stock_price:.2f}")
    
    # Get option chain
    print(f"Fetching option chain for expiration: {expiration_date}")
    try:
        opts = ticker.option_chain(expiration_date)
        calls = opts.calls
    except Exception as e:
        print(f"Error fetching options: {e}")
        # List available expirations
        print("Available expirations:")
        print(ticker.options)
        return

    # Filter for strikes we care about - for PGY (price ~22), strikes will be much lower
    # We want deep ITM for 2x leverage. If price is 22, 2x leverage means option price ~11.
    # Strike + 11 = 22 => Strike ~11.
    # So let's look at strikes around 10-15.
    target_strikes = [5, 7.5, 10, 12.5, 15, 17.5, 20]
    
    print("-" * 80)
    print(f"{'Strike':<10} {'Bid':<10} {'Ask':<10} {'Last':<10} {'Vol':<10} {'Implied Vol':<15}")
    print("-" * 80)
    
    for index, row in calls.iterrows():
        if row['strike'] in target_strikes:
            print(f"{row['strike']:<10.2f} {row['bid']:<10.2f} {row['ask']:<10.2f} {row['lastPrice']:<10.2f} {row['volume']:<10.0f} {row['impliedVolatility']:<15.2%}")
            
    print("-" * 80)

if __name__ == "__main__":
    ticker_symbol = "PGY"
    ticker = yf.Ticker(ticker_symbol)
    
    print(f"Fetching expirations for {ticker_symbol}...")
    expirations = ticker.options
    print(f"Available expirations: {expirations}")
    
    # Find a 2028 expiration
    target_date = None
    for date in expirations:
        if "2028" in date:
            target_date = date
            break
    
    if not target_date:
        # Fallback to 2027
        for date in expirations:
            if "2027" in date:
                target_date = date
                break
                
    if target_date:
        print(f"\nSelected target expiration: {target_date}")
        get_option_data(ticker_symbol, target_date)
    else:
        print("\nNo 2027/2028 expiration found via API.")
