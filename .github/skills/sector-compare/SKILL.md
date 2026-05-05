---
name: sector-compare
description: 'Compare stocks within the same sector or industry. Use when: comparing multiple tickers, sector comparison, industry peer analysis, which stock is cheaper, forward PE comparison, earnings date, gross margin, moat comparison, 比較同產業, 哪支比較便宜, 產業比較, 同類股比較.'
argument-hint: 'tickers to compare (e.g. AVGO MRVL CRDO) or sector name'
---

# Sector Comparison Skill

## When to Use

- 比較同產業多支股票
- 想知道哪支 Forward PE 最低（最便宜）
- 查詢各股財報日期
- 比較毛利率、護城河強度
- 決定相同產業中要買哪支

---

## Procedure

### Step 1：用 yfinance 抓取基本數據

```python
import yfinance as yf
from datetime import datetime

tickers = ["AVGO", "MRVL", "CRDO"]  # 替換成要比較的標的

results = []
for t in tickers:
    stock = yf.Ticker(t)
    info = stock.info
    results.append({
        "ticker": t,
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "forward_pe": info.get("forwardPE"),
        "trailing_pe": info.get("trailingPE"),
        "gross_margin": round(info.get("grossMargins", 0) * 100, 1),
        "market_cap_b": round(info.get("marketCap", 0) / 1e9, 1),
        "earnings_date": info.get("earningsDate") or info.get("earningsTimestamp"),
    })

# 排序：Forward PE 由低到高
results.sort(key=lambda x: (x["forward_pe"] or 9999))

print(f"{'Ticker':<8} {'Price':>8} {'Fwd PE':>8} {'Trl PE':>8} {'GrossM':>8} {'MktCap(B)':>10} {'EarningsDate'}")
print("-" * 75)
for r in results:
    ed = r["earnings_date"]
    if isinstance(ed, (int, float)):
        ed = datetime.fromtimestamp(ed).strftime("%Y-%m-%d")
    print(f"{r['ticker']:<8} {str(r['price'] or 'N/A'):>8} {str(r['forward_pe'] or 'N/A'):>8} {str(r['trailing_pe'] or 'N/A'):>8} {str(r['gross_margin']) + '%':>8} {str(r['market_cap_b']) + 'B':>10} {ed or 'N/A'}")
```

### Step 2：輸出比較表

格式如下：

| Ticker | 現價 | Forward PE | Trailing PE | 毛利率 | 市值 | 財報日 | 貴不貴 |
|--------|------|-----------|-------------|--------|------|--------|--------|
| AVGO   | ...  | 23.3x     | 82.6x       | 76.7%  | ...  | 2026-06-04 | ✅ 合理 |
| MRVL   | ...  | 30.3x     | 53.5x       | 51.0%  | ...  | 2026-05-29 | ✅ 合理 |
| CRDO   | ...  | 35.8x     | 107.8x      | 67.8%  | ...  | 2026-06-02 | 🟡 偏貴 |

### Step 3：評估「貴不貴」

用 Forward PE 判斷：

| Forward PE | 評估 |
|-----------|------|
| < 25x | ✅ 合理 |
| 25x ~ 40x | 🟡 偏貴但看成長性 |
| 40x ~ 60x | 🔴 貴，需高成長支撐 |
| > 60x | 🔴🔴 非常貴 |

同時考量：
- **毛利率 > 60%** = 高品質護城河
- **財報日** 即將到來 = 短期波動風險提高

### Step 4：給出結論

```
推薦順序：Forward PE 最低 + 毛利率最高 = 最甜蜜點
避開：毛利率低 + PE 貴 + 護城河弱
```

---

## 快速參考：常見護城河評分

| 護城河強度 | 特徵 |
|-----------|------|
| ★★★★★ | 壟斷性技術/平台，客戶鎖定期長 |
| ★★★★  | 雙頭壟斷，替換成本高 |
| ★★★   | 技術壁壘存在但有競爭者 |
| ★★    | 差異化不明顯，定價能力弱 |
| ★     | 純商品化，價格競爭 |
