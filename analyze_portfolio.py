import re

def parse_position_file(filepath):
    positions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Symbol Quantity Price Change Change% MarketValue CostBasis TotalCost GainLoss GainLoss% actions
    # Note: Quantity, MarketValue, TotalCost, GainLoss can have commas.
    # Regex might be safer or just splitting by whitespace if the columns are consistent.
    # Looking at the file, it seems tab or space separated.
    # Let's try splitting by whitespace.
    
    for line in lines:
        line = line.strip()
        if not line: continue
        parts = line.split()
        # Expected at least 10 parts + 'actions' = 11 parts.
        # Some symbols might be complex? No, they look standard.
        # Let's assume the last part is 'actions' and work backwards?
        # Or just standard split.
        
        if len(parts) < 11:
            continue
            
        # Mapping based on observation:
        # 0: Symbol
        # 1: Quantity (remove commas)
        # 2: Price
        # 3: Change
        # 4: Change%
        # 5: Market Value (remove commas)
        # 6: Cost Basis
        # 7: Total Cost (remove commas)
        # 8: Gain/Loss (remove commas)
        # 9: Gain/Loss % (remove commas, %)
        # 10: actions
        
        try:
            symbol = parts[0]
            qty = float(parts[1].replace(',', ''))
            price = float(parts[2].replace(',', ''))
            market_value = float(parts[5].replace(',', ''))
            total_cost = float(parts[7].replace(',', ''))
            gain_loss = float(parts[8].replace(',', ''))
            gain_loss_pct = float(parts[9].replace(',', '').replace('%', ''))
            
            positions.append({
                'symbol': symbol,
                'qty': qty,
                'price': price,
                'market_value': market_value,
                'total_cost': total_cost,
                'gain_loss': gain_loss,
                'gain_loss_pct': gain_loss_pct
            })
        except Exception as e:
            print(f"Error parsing line: {line}\nError: {e}")
            continue
            
    return positions

def generate_summary(positions):
    total_market_value = sum(p['market_value'] for p in positions)
    total_cost = sum(p['total_cost'] for p in positions)
    total_gain_loss = total_market_value - total_cost
    total_gain_loss_pct = (total_gain_loss / total_cost * 100) if total_cost != 0 else 0
    
    # Sort by Market Value
    sorted_by_value = sorted(positions, key=lambda x: x['market_value'], reverse=True)
    top_5_holdings = sorted_by_value[:5]
    
    # Sort by Gain $
    sorted_by_gain = sorted(positions, key=lambda x: x['gain_loss'], reverse=True)
    top_5_winners = sorted_by_gain[:5]
    top_5_losers = sorted_by_gain[-5:]
    
    summary = []
    summary.append("# 投資組合摘要")
    summary.append(f"**總市值**: ${total_market_value:,.2f}")
    summary.append(f"**總成本**: ${total_cost:,.2f}")
    summary.append(f"**未實現損益**: ${total_gain_loss:,.2f} ({total_gain_loss_pct:+.2f}%)")
    
    summary.append("\n## 前五大持倉 (按市值)")
    summary.append("| 代號 | 數量 | 價格 | 市值 | 佔比 |")
    summary.append("|---|---|---|---|---|")
    for p in top_5_holdings:
        pct = (p['market_value'] / total_market_value * 100) if total_market_value else 0
        summary.append(f"| {p['symbol']} | {p['qty']:,.4f} | ${p['price']:,.2f} | ${p['market_value']:,.2f} | {pct:.2f}% |")
        
    summary.append("\n## 前五大獲利 ($)")
    summary.append("| 代號 | 獲利 ($) | 獲利 (%) |")
    summary.append("|---|---|---|")
    for p in top_5_winners:
        summary.append(f"| {p['symbol']} | ${p['gain_loss']:+,.2f} | {p['gain_loss_pct']:+.2f}% |")

    summary.append("\n## 前五大虧損 ($)")
    summary.append("| 代號 | 虧損 ($) | 虧損 (%) |")
    summary.append("|---|---|---|")
    # Losers should be displayed from worst to least worst, so reverse the last 5
    for p in sorted(top_5_losers, key=lambda x: x['gain_loss']):
        summary.append(f"| {p['symbol']} | ${p['gain_loss']:+,.2f} | {p['gain_loss_pct']:+.2f}% |")
        
    return "\n".join(summary)

if __name__ == "__main__":
    filepath = r"g:\AI\anti-gravity\investing\position.txt"
    positions = parse_position_file(filepath)
    report = generate_summary(positions)
    print(report)
    
    # Save to file for the user
    with open(r"g:\AI\anti-gravity\investing\portfolio_summary.md", "w", encoding="utf-8") as f:
        f.write(report)
