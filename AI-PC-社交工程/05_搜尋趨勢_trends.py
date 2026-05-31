# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pytrends",
#     "truststore",
#     "pandas",
# ]
# ///
"""真 · 社交工程引擎 — 抓 Google Trends 真實搜尋熱度與動能。

回答原始任務：「透過 google search 觀察關鍵字變化」。
不是讀評測文章，而是看群眾真實搜尋行為的時間序列。

輸出：
  - 主控台動能排序表
  - trends_data.json   （給 04 監控頁讀取）
  - 05_搜尋趨勢.html    （獨立視覺頁）

用法：uv run --native-tls 05_搜尋趨勢_trends.py
注意：Google Trends 為「相對熱度 0–100」非絕對搜尋量；偶爾 429 限流，稍後重跑即可。
"""
from __future__ import annotations
import datetime as dt
import json
import sys
from pathlib import Path

import truststore  # Windows 憑證庫，繞過 TLS 攔截代理
truststore.inject_into_ssl()
from pytrends.request import TrendReq

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
JSON_OUT = HERE / "trends_data.json"
HTML_OUT = HERE / "05_搜尋趨勢.html"

# Google Trends 一次最多 5 個關鍵字（同一批才可比較相對熱度）
KEYWORDS = ["RTX 5090", "DGX Spark", "Mac Studio", "AMD Strix Halo", "local LLM"]
TIMEFRAME = "today 3-m"   # 近 3 個月日資料


def fetch_trends() -> dict:
    py = TrendReq(hl="en-US", tz=480)
    py.build_payload(KEYWORDS, timeframe=TIMEFRAME)
    df = py.interest_over_time()
    if df.empty:
        raise RuntimeError("Trends 回傳空資料（可能被 429 限流，稍後重跑）")
    # 去掉最後一天的 isPartial（未完整）
    if "isPartial" in df.columns:
        df = df[~df["isPartial"]].drop(columns=["isPartial"])

    rows = []
    for kw in KEYWORDS:
        s = df[kw].astype(float)
        level = float(s.iloc[-1])              # 最新熱度
        recent = float(s.tail(14).mean())      # 近 14 天均
        prior = float(s.iloc[-28:-14].mean())  # 前 14 天均
        momentum = (recent / prior - 1.0) * 100.0 if prior else 0.0
        peak = float(s.max())
        rows.append({
            "keyword": kw,
            "level": round(level, 1),
            "recent_avg": round(recent, 1),
            "momentum_pct": round(momentum, 1),
            "from_peak_pct": round((level / peak - 1.0) * 100.0, 1) if peak else 0.0,
        })
    rows.sort(key=lambda r: r["recent_avg"], reverse=True)
    return {
        "updated": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "timeframe": TIMEFRAME,
        "keywords": rows,
    }


def print_table(data: dict) -> None:
    print(f"\n=== Google Trends 搜尋動能（{data['timeframe']}，更新 {data['updated']}）===\n")
    print(f"{'關鍵字':<18}{'熱度':>6}{'近14日均':>10}{'動能Δ':>9}{'距峰值':>9}")
    print("-" * 54)
    for r in data["keywords"]:
        arrow = "▲" if r["momentum_pct"] > 3 else ("▼" if r["momentum_pct"] < -3 else "→")
        print(f"{r['keyword']:<18}{r['level']:>6.0f}{r['recent_avg']:>10.1f}"
              f"{r['momentum_pct']:>+8.1f}% {arrow}{r['from_peak_pct']:>8.1f}%")
    top = data["keywords"][0]
    hot = max(data["keywords"], key=lambda r: r["momentum_pct"])
    print(f"\n聲量最高：{top['keyword']}（{top['recent_avg']}）　"
          f"動能最強：{hot['keyword']}（{hot['momentum_pct']:+.1f}%）")


def bar(width_pct: float, color: str) -> str:
    return (f'<div class="track"><div class="fill" '
            f'style="width:{width_pct:.0f}%;background:{color}"></div></div>')


def render_html(data: dict) -> str:
    maxv = max((r["recent_avg"] for r in data["keywords"]), default=1) or 1
    palette = ["#76b900", "#5b8cff", "#a8b3c4", "#ff5d6c", "#3fd68c"]
    bars = []
    for i, r in enumerate(data["keywords"]):
        w = r["recent_avg"] / maxv * 100
        arrow = "▲" if r["momentum_pct"] > 3 else ("▼" if r["momentum_pct"] < -3 else "→")
        acls = "pos" if r["momentum_pct"] > 3 else ("neg" if r["momentum_pct"] < -3 else "flat")
        bars.append(
            f'<div class="row"><span class="kw">{r["keyword"]}</span>'
            f'{bar(w, palette[i % len(palette)])}'
            f'<span class="val">{r["recent_avg"]:.0f}</span>'
            f'<span class="mom {acls}">{r["momentum_pct"]:+.1f}% {arrow}</span></div>'
        )
    bars_html = "\n".join(bars)
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI PC 搜尋趨勢 · {data['updated']}</title><style>
:root{{--bg:#0b0e14;--panel:#141925;--panel2:#1c2333;--line:#2a3450;--txt:#e6ecff;
--muted:#8a96b3;--accent:#5b8cff;--green:#3fd68c;--red:#ff5d6c}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Segoe UI","Microsoft JhengHei",sans-serif;background:
radial-gradient(1200px 600px at 70% -10%,#16203a 0,var(--bg) 60%);color:var(--txt);
padding:32px 18px;min-height:100vh}}
.wrap{{max-width:880px;margin:0 auto}}
.kicker{{color:var(--accent);font-weight:700;letter-spacing:3px;font-size:12px;text-transform:uppercase}}
h1{{font-size:26px;margin:6px 0}}
.ts{{color:var(--muted);font-size:13px;margin-bottom:22px}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px}}
.row{{display:grid;grid-template-columns:130px 1fr 42px 92px;align-items:center;gap:12px;margin:12px 0}}
.kw{{font-size:14px}}
.track{{background:var(--panel2);border-radius:8px;height:16px;overflow:hidden}}
.fill{{height:100%;border-radius:8px}}
.val{{font-size:13px;color:var(--muted);text-align:right}}
.mom{{font-size:13px;font-weight:700;text-align:right}}
.pos{{color:var(--green)}} .neg{{color:var(--red)}} .flat{{color:var(--muted)}}
.note{{color:var(--muted);font-size:12px;margin-top:16px;line-height:1.6}}
code{{background:var(--panel2);padding:2px 6px;border-radius:5px}}
</style></head><body><div class="wrap">
<div class="kicker">真 · 社交工程 · Google Trends</div>
<h1>大家在搜尋哪種 AI PC？</h1>
<div class="ts">真實搜尋熱度（相對 0–100）· {data['timeframe']} · 更新 {data['updated']}</div>
<div class="panel">
{bars_html}
<div class="note">數值＝近 14 日平均搜尋熱度（同一批 5 詞相對比較）；右側為動能（近14日均 vs 前14日均）。
▲ 加速、▼ 退燒、→ 持平。資料來自 Google Trends，重跑 <code>uv run --native-tls 05_搜尋趨勢_trends.py</code> 更新。</div>
</div></div></body></html>"""


def main() -> None:
    print("抓取 Google Trends 中…（約 5–15 秒）")
    data = fetch_trends()
    print_table(data)
    JSON_OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    HTML_OUT.write_text(render_html(data), encoding="utf-8")
    print(f"\n[OK] 已寫出 {JSON_OUT.name} 與 {HTML_OUT.name}")


if __name__ == "__main__":
    main()
