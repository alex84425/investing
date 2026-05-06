"""
查詢台股持倉近期法說會日期。
用法：uv run python .github/skills/daily-check/script/check_tw_conferences.py
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Windows terminal UTF-8 support
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 台股名稱 → 代號對照（可自行擴充）
TW_STOCK_MAP = {
    "台積電": "2330",
    "群聯": "8299",
    "臺慶科": "3609",
    "華城": "1519",
    "南亞科": "2408",
}


def read_tw_positions(filepath: str = "tw_stock.md") -> list[str]:
    """從tw_stock.md 讀取持倉名單"""
    p = Path(filepath)
    if not p.exists():
        # 嘗試從 workspace root 找
        workspace = Path(__file__).resolve().parents[3]
        p = workspace / filepath
    if not p.exists():
        print(f"⚠️ 找不到 {filepath}")
        return []
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def search_conference_url(stock_name: str, stock_code: str) -> str:
    """產生搜尋法說會的 URL"""
    now = datetime.now()
    query = f"{stock_name} {stock_code} 法說會 {now.year}年{now.month}月"
    return f"https://www.google.com/search?q={query}"


def build_goodinfo_url(stock_code: str) -> str:
    """Goodinfo 法說會/股東會頁面"""
    return f"https://goodinfo.tw/tw/StockInvestorConferenceList.asp?STOCK_ID={stock_code}"


def main():
    positions = sys.argv[1:] if len(sys.argv) > 1 else read_tw_positions()
    today = datetime.now()

    print(f"=== 台股法說會檢查 ({today.strftime('%Y-%m-%d')}) ===\n")
    print("持倉清單：", ", ".join(positions))
    print()

    # 輸出可供 agent 使用的查詢 URL
    results = []
    for name in positions:
        code = TW_STOCK_MAP.get(name, "")
        search_url = search_conference_url(name, code)
        goodinfo_url = build_goodinfo_url(code) if code else None
        results.append(
            {
                "name": name,
                "code": code,
                "search_url": search_url,
                "goodinfo_url": goodinfo_url,
            }
        )
        print(f"📋 {name}（{code or '未知代號'}）")
        if goodinfo_url:
            print(f"   Goodinfo: {goodinfo_url}")
        print(f"   Google:   {search_url}")
        print()

    print("--- JSON ---")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
