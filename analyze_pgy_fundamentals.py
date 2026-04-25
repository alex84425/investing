import yfinance as yf
import pandas as pd

def analyze_pgy_fundamentals():
    ticker_symbol = "PGY"
    print(f"Fetching fundamentals for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    
    # 1. Key Statistics
    info = ticker.info
    print("\n--- Key Statistics ---")
    print(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
    print(f"Trailing PE: {info.get('trailingPE', 'N/A')}")
    print(f"Forward PE: {info.get('forwardPE', 'N/A')}")
    print(f"Price/Sales: {info.get('priceToSalesTrailing12Months', 'N/A')}")
    print(f"Beta: {info.get('beta', 'N/A')}")
    print(f"52 Week Range: {info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}")
    
    # 2. Recent Earnings (Quarterly)
    print("\n--- Recent Quarterly Financials (Income Statement) ---")
    q_financials = ticker.quarterly_financials
    if not q_financials.empty:
        # Show last 4 quarters of Revenue and Net Income
        try:
            rev = q_financials.loc['Total Revenue']
            net_income = q_financials.loc['Net Income']
            
            df_fin = pd.DataFrame({'Revenue': rev, 'Net Income': net_income})
            # Sort by date ascending
            df_fin = df_fin.sort_index(ascending=True)
            print(df_fin)
            
            # Calculate growth
            last_q_rev = df_fin['Revenue'].iloc[-1]
            prev_q_rev = df_fin['Revenue'].iloc[-2]
            qoq_growth = (last_q_rev - prev_q_rev) / prev_q_rev
            print(f"\nQoQ Revenue Growth: {qoq_growth:.2%}")
            
        except KeyError as e:
            print(f"Could not extract specific fields: {e}")
            print(q_financials.head())
    else:
        print("No quarterly financials available.")

    # 3. Recent News
    print("\n--- Recent News ---")
    news = ticker.news
    if news:
        for item in news[:5]: # Show top 5
            print(f"- [{item.get('providerPublishTime', 'N/A')}] {item.get('title', 'N/A')}")
            # print(f"  Link: {item.get('link', 'N/A')}")
    else:
        print("No recent news found via API.")

if __name__ == "__main__":
    analyze_pgy_fundamentals()
