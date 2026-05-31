# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "truststore",
# ]
# ///
"""AI PC 動能掃描 — 抓上游受惠標的的即時價量動能，輸出排序表（主控台版）。

對應「更好的做法」：不賭單一機種，盯共同上游(鏟子的鏟子) HBM/晶圓。
動能 = 1M/3M/6M 報酬 + 是否站上 50/200 日均線 + 距 52 週高點。

資料來源：Yahoo Finance Chart API + truststore（繞過 TLS 攔截代理）。
用法:  uv run --native-tls 03_動能掃描_momentum_scan.py
"""
from __future__ import annotations
import sys

import truststore  # 使用 Windows 憑證庫，信任公司代理根憑證
truststore.inject_into_ssl()
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"}

# 上游公約數 + 陣營代表（與 04 監控頁一致）
TICKERS = [
    ("MU",        "美光 (HBM4 直接受惠) USD"),
    ("000660.KS", "SK Hynix (HBM 龍頭) KRW"),
    ("NVDA",      "NVIDIA (Rubin 引擎) USD"),
    ("TSM",       "台積電 (晶圓/封裝) USD"),
    ("AMD",       "AMD (Strix Halo 陣營) USD"),
]


def pct(a: float, b: float) -> float:
    return (a / b - 1.0) * 100.0 if b else float("nan")


def fetch(tk: str) -> dict | None:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?range=1y&interval=1d"
    try:
        r = requests.get(url, headers=UA, timeout=20)
        r.raise_for_status()
        q = r.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    except Exception as e:  # noqa: BLE001 — 單一標的失敗不中斷整批
        print(f"  ! {tk} 抓取失敗，略過：{type(e).__name__}", file=sys.stderr)
        return None
    c = [x for x in q if x is not None]
    if len(c) < 30:
        print(f"  ! {tk} 資料不足，略過", file=sys.stderr)
        return None
    last = c[-1]
    ago = lambda n: c[-n] if len(c) > n else None  # noqa: E731
    avg = lambda n: sum(c[-n:]) / min(n, len(c))    # noqa: E731
    return {
        "price": last,
        "m1": pct(last, ago(21)) if ago(21) else None,
        "m3": pct(last, ago(63)) if ago(63) else None,
        "m6": pct(last, ago(126)) if ago(126) else None,
        "ma50": last > avg(50),
        "ma200": last > avg(200),
        "hi": pct(last, max(c)),
    }


def fmt(v, suffix="%"):
    return "  n/a " if v is None else f"{v:+6.1f}{suffix}"


def main() -> None:
    print("\n=== AI PC 動能掃描（依 3 個月報酬排序）===\n")
    rows = []
    for tk, desc in TICKERS:
        d = fetch(tk)
        if d:
            rows.append((tk, desc, d))
    if not rows:
        print("無資料（檢查網路/憑證；記得 uv run --native-tls）")
        return
    rows.sort(key=lambda x: (x[2]["m3"] is not None, x[2]["m3"] or -9e9), reverse=True)

    hdr = f"{'代號':<11}{'價格':>12}{'1M':>9}{'3M':>9}{'6M':>9}{'50MA':>6}{'200MA':>7}{'距52高':>9}  說明"
    print(hdr)
    print("-" * len(hdr))
    for tk, desc, d in rows:
        price = f"{d['price']:,.0f}" if d["price"] >= 1000 else f"{d['price']:.2f}"
        print(f"{tk:<11}{price:>12}{fmt(d['m1'])}{fmt(d['m3'])}{fmt(d['m6'])}"
              f"{'✅' if d['ma50'] else '❌':>6}{'✅' if d['ma200'] else '❌':>7}"
              f"{d['hi']:>8.1f}%  {desc}")
    print("\n動能訊號：3M/6M 為正 + 站上 50/200MA + 接近 52 週高 → 動能確認。")


if __name__ == "__main__":
    main()
