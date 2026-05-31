# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "truststore",
# ]
# ///
"""資料中心領先指標掃描 — 循環階段儀表。

產業鏈時序：設備訂單 → 記憶體資本支出 → HBM 報價。
用「設備股 vs 記憶體股」的相對動能判斷循環位置：
  - 設備動能 ≥ 記憶體、皆正 → 循環早中期（capex 加速，順勢）
  - 設備動能轉弱、記憶體仍強 → 末期警訊（上游訂單見頂領先記憶體 1–2 季）

資料：Yahoo Finance Chart API + truststore（繞過 TLS 攔截代理）。
用法：uv run --native-tls 06_領先指標掃描_scan.py
"""
from __future__ import annotations
import sys

import truststore
truststore.inject_into_ssl()
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"}

# 三個產業鏈環節
GROUPS = {
    "設備(領先)": [("AMAT", "應用材料"), ("LRCX", "科林研發"),
                    ("KLAC", "科磊"), ("ASML", "艾司摩爾")],
    "記憶體(本體)": [("MU", "美光"), ("000660.KS", "SK Hynix·KRW")],
    "封裝/晶圓": [("TSM", "台積電")],
}


def pct(a, b):
    return (a / b - 1.0) * 100.0 if b else None


def fetch(tk):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?range=1y&interval=1d"
    try:
        r = requests.get(url, headers=UA, timeout=20)
        r.raise_for_status()
        q = r.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    except Exception as e:  # noqa: BLE001
        print(f"  ! {tk} 抓取失敗：{type(e).__name__}", file=sys.stderr)
        return None
    c = [x for x in q if x is not None]
    if len(c) < 70:
        return None
    last = c[-1]
    return {
        "price": last,
        "m1": pct(last, c[-21]),
        "m3": pct(last, c[-63]),
        "m6": pct(last, c[-126]) if len(c) > 126 else None,
    }


def main():
    print("\n=== 資料中心領先指標掃描（設備 → 記憶體 → 封裝）===\n")
    group_m3 = {}
    for gname, members in GROUPS.items():
        print(f"【{gname}】")
        vals = []
        for tk, desc in members:
            d = fetch(tk)
            if not d:
                print(f"  {tk:<11} 無資料")
                continue
            price = f"{d['price']:,.0f}" if d["price"] >= 1000 else f"{d['price']:.2f}"
            m6 = f"{d['m6']:+.1f}%" if d["m6"] is not None else "  n/a"
            print(f"  {tk:<11}{price:>11}  1M {d['m1']:+6.1f}%  3M {d['m3']:+6.1f}%  6M {m6:>8}  {desc}")
            if d["m3"] is not None:
                vals.append(d["m3"])
        group_m3[gname] = sum(vals) / len(vals) if vals else None
        print()

    eq = group_m3.get("設備(領先)")
    mem = group_m3.get("記憶體(本體)")
    print("=" * 56)
    if eq is None or mem is None:
        print("資料不足，無法判斷循環階段。")
        return
    print(f"設備平均 3M 動能：{eq:+.1f}%   記憶體平均 3M 動能：{mem:+.1f}%")
    if eq >= mem and mem > 0:
        verdict = "循環早中期 → capex 仍加速，順勢做多上游。"
    elif eq > 0 and mem > 0 and eq < mem:
        verdict = "循環中後期 → 設備動能落後記憶體，留意上游訂單見頂。"
    elif eq <= 0 < mem:
        verdict = "⚠ 末期警訊 → 設備轉弱、記憶體仍強，訂單可能領先見頂 1–2 季。"
    elif eq < 0 and mem < 0:
        verdict = "⚠ 循環下行 → 設備與記憶體同步走弱，動能已轉空。"
    else:
        verdict = "訊號混合，續觀察。"
    print(f"判讀：{verdict}")
    print("\n※ 退場雷達：另盯 HBM 合約價轉負 / CoWoS 交期縮短 / hyperscaler capex 指引下修。")


if __name__ == "__main__":
    main()
