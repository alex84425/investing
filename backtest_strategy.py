import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_backtest(ticker="GOOG", start_date="2020-01-01", initial_capital=100000):
    print(f"Downloading data for {ticker} from {start_date}...")
    df = yf.download(ticker, start=start_date, progress=False)
    
    if df.empty:
        print("No data found.")
        return

    # Debug: Print columns
    print(f"Columns: {df.columns}")
    
    # Use 'Close' if 'Adj Close' is missing (yfinance new version behavior)
    price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
    # Handle MultiIndex columns if present (e.g. ('Close', 'GOOG'))
    if isinstance(df.columns, pd.MultiIndex):
        # Flatten or access correctly. For single ticker, it might be ('Close', 'GOOG')
        # Let's try to access 'Close' directly or check level 0
        try:
            df = df.xs(ticker, axis=1, level=1)
            price_col = 'Close'
        except:
            pass

    if price_col not in df.columns:
        # Fallback for simple single-level
        price_col = 'Close'

    df['Return'] = df[price_col].pct_change()
    
    # Simulate 3x Leverage Daily Return
    # Note: 3x ETFs have expense ratios and borrowing costs. 
    # We'll approximate by subtracting a small daily cost (e.g., 5% annual / 252)
    # And volatility decay is inherent in the daily compounding.
    borrow_cost_annual = 0.05
    daily_cost = borrow_cost_annual / 252
    df['Return_3x'] = (df['Return'] * 3) - daily_cost
    
    # Strategy: 1/3 in 3x, 2/3 in Cash
    # "Buy the Dip" Logic: 
    # Let's define a simple rule: If GOOG drops > 20% from All-Time High, deploy 50% of remaining cash.
    # If drops > 40%, deploy remaining.
    
    cash = initial_capital * (2/3)
    position_3x_val = initial_capital * (1/3)
    
    # Benchmark: 100% in GOOG
    benchmark_val = initial_capital
    
    strategy_equity = []
    benchmark_equity = []
    
    ath = 0
    cash_deployed_levels = set() # Track if we deployed at 20%, 40%
    
    # Risk Free Rate for Cash (approx 2% avg over period? or 4% now? let's use 0 for conservative or 3%)
    rf_daily = 0.03 / 252
    
    print("Running simulation...")
    
    for i in range(len(df)):
        if i == 0:
            strategy_equity.append(initial_capital)
            benchmark_equity.append(initial_capital)
            ath = df[price_col].iloc[i]
            continue
            
        # Update Benchmark
        r = df['Return'].iloc[i]
        benchmark_val = benchmark_val * (1 + r)
        
        # Update Strategy
        r_3x = df['Return_3x'].iloc[i]
        position_3x_val = position_3x_val * (1 + r_3x)
        cash = cash * (1 + rf_daily)
        
        # Check for Buy the Dip
        current_price = df[price_col].iloc[i]
        if current_price > ath:
            ath = current_price
            cash_deployed_levels.clear() # Reset if new ATH? Or keep deployed? 
            # Usually you don't sell the dip-buy immediately. Let's assume we hold.
            # But we reset the "levels" so we can buy again if it drops again from new ATH.
        
        drawdown = (ath - current_price) / ath
        
        # Dip Buying Logic
        if drawdown > 0.30 and 0.30 not in cash_deployed_levels and cash > 0:
            # Deploy 50% of available cash
            amount_to_invest = cash * 0.5
            cash -= amount_to_invest
            position_3x_val += amount_to_invest
            cash_deployed_levels.add(0.30)
            print(f"[{df.index[i].date()}] Dip > 30% (DD: {drawdown:.2%}). Deployed ${amount_to_invest:,.0f} into 3x.")
            
        if drawdown > 0.40 and 0.40 not in cash_deployed_levels and cash > 0:
            # Deploy remaining cash
            amount_to_invest = cash
            cash -= amount_to_invest
            position_3x_val += amount_to_invest
            cash_deployed_levels.add(0.40)
            print(f"[{df.index[i].date()}] Dip > 40% (DD: {drawdown:.2%}). Deployed remaining ${amount_to_invest:,.0f}.")
            
        total_val = position_3x_val + cash
        strategy_equity.append(total_val)
        benchmark_equity.append(benchmark_val)

    # Results
    df['Strategy'] = strategy_equity
    df['Benchmark'] = benchmark_equity
    
    final_strat = strategy_equity[-1]
    final_bench = benchmark_equity[-1]
    
    strat_ret = (final_strat - initial_capital) / initial_capital
    bench_ret = (final_bench - initial_capital) / initial_capital
    
    print("-" * 50)
    print(f"Final Results ({start_date} to {df.index[-1].date()})")
    print(f"Strategy Final: ${final_strat:,.2f} ({strat_ret:+.2%})")
    print(f"Benchmark Final: ${final_bench:,.2f} ({bench_ret:+.2%})")
    print("-" * 50)
    
    # Correlation / Beta
    # Calculate daily returns of strategy equity
    strat_daily_ret = pd.Series(strategy_equity).pct_change().dropna()
    bench_daily_ret = pd.Series(benchmark_equity).pct_change().dropna()
    
    correlation = strat_daily_ret.corr(bench_daily_ret)
    beta = strat_daily_ret.cov(bench_daily_ret) / bench_daily_ret.var()
    
    print(f"Correlation to GOOG: {correlation:.4f}")
    print(f"Beta to GOOG: {beta:.4f}")
    print("-" * 50)
    print("Analysis:")
    if beta < 1:
        print("The strategy is LESS volatile than holding GOOG directly (Beta < 1).")
        print("This is because 2/3 cash dampens the volatility, even with 3x leverage on the 1/3.")
    else:
        print("The strategy is MORE volatile than GOOG.")
        
    if strat_ret > bench_ret:
        print("The strategy OUTPERFORMED GOOG.")
    else:
        print("The strategy UNDERPERFORMED GOOG.")
        print("Reasons could be: Volatility decay of 3x, or cash drag during bull markets.")

if __name__ == "__main__":
    try:
        run_backtest()
    except Exception as e:
        print(f"An error occurred: {e}")
