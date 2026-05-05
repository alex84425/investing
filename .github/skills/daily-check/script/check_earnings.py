"""
查詢美股持倉未來 7 天內的財報日期。
用法：uv run python .github/skills/daily-check/script/check_earnings.py
"""

import json
import os
import sys
from datetime import datetime, timedelta

# Windows terminal UTF-8 support
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import yfinance as yf


def check_earnings(tickers: list[str], days: int = 7) -> list[dict]:
    today = datetime.now()
    cutoff = today + timedelta(days=days)
    results = []

    for t in tickers:
        try:
            stock = yf.Ticker(t)
            cal = stock.calendar
            ed = None
            if cal is not None:
                # yfinance calendar 格式可能是 dict 或 DataFrame
                if isinstance(cal, dict):
                    raw = cal.get("Earnings Date")
                else:
                    raw = cal.get("Earnings Date", [None])
                if isinstance(raw, list) and len(raw) > 0:
                    ed = raw[0]
                elif hasattr(raw, "date"):
                    ed = raw

            if ed is not None and hasattr(ed, "date"):
                ed_date = ed if isinstance(ed, datetime) else datetime.combine(ed.date(), datetime.min.time())
                within = today.date() <= ed_date.date() <= cutoff.date()
                results.append(
                    {
                        "ticker": t,
                        "earnings_date": ed_date.strftime("%Y-%m-%d"),
                        "within_window": within,
                    }
                )
            else:
                results.append(
                    {
                        "ticker": t,
                        "earnings_date": None,
                        "within_window": False,
                    }
                )
        except Exception as e:
            results.append(
                {
                    "ticker": t,
                    "earnings_date": None,
                    "within_window": False,
                    "error": str(e),
                }
            )

    return results


# 預設美股持倉清單（同 personal_position.md）
DEFAULT_TICKERS = [
    "CRDO",
    "MU",
    "TSM",
    "NBIS",
    "AMZN",
    "PGY",
    "LEU",
    "LITE",
    "OPFI",
    "WLDN",
    "VFF",
]

if __name__ == "__main__":
    tickers = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_TICKERS
    results = check_earnings(tickers)

    upcoming = [r for r in results if r["within_window"]]
    later = [r for r in results if not r["within_window"]]

    print(f"=== 美股財報檢查 ({datetime.now().strftime('%Y-%m-%d')}) ===\n")

    if upcoming:
        print("🔴 未來 7 天內有財報：")
        for r in upcoming:
            print(f"   {r['ticker']:<6} — {r['earnings_date']}")
    else:
        print("✅ 未來 7 天內無持倉財報")

    print()
    if later:
        print("其他持倉財報日：")
        for r in later:
            ed = r["earnings_date"] or "N/A"
            print(f"   {r['ticker']:<6} — {ed}")

    # 同時輸出 JSON 方便程式讀取
    print("\n--- JSON ---")
    print(json.dumps(results, ensure_ascii=False, indent=2))
