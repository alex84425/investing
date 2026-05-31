# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "truststore",
# ]
# ///
"""每日監控頁產生器 — 抓即時價量動能 → 產出自包含 HTML。

主軸：Rubin 放量 → HBM4 → 記憶體上游 (MU / SK Hynix)。
DGX Spark / AI PC 僅當情緒領先指標，不是部位主軸。

資料來源：直接打 Yahoo Finance Chart API（避開 yfinance 的 curl/crumb 問題）。
truststore：改用 Windows 憑證庫，繞過 TLS 攔截代理的憑證鏈問題。

用法:  uv run 04_監控頁_generate.py
       跑完開啟同資料夾的 04_監控頁.html（資料動態、每跑一次更新一次）。
"""
from __future__ import annotations
import datetime as dt
import html
import json
import sys
from pathlib import Path

import truststore  # 使用 Windows 系統憑證庫（信任公司代理根憑證）
truststore.inject_into_ssl()
import requests

# Windows 主控台預設 cp950，輸出中文/emoji 會亂碼或報錯 → 強制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"}

OUT = Path(__file__).with_name("04_監控頁.html")

# 監控清單：角色 → (ticker, 說明)
WATCH = [
    ("HBM 純度最高", "MU", "美光 — Rubin HBM4 最直接受惠 (USD)"),
    ("HBM 純度最高", "000660.KS", "SK Hynix — HBM 龍頭 (KRW)"),
    ("引擎本體", "NVDA", "NVIDIA — Rubin 放量 Q3→Q4 2026"),
    ("全員上游", "TSM", "台積 — 封裝+晶圓必經之路"),
    ("AI PC 黑馬", "AMD", "Strix Halo — 情緒/x86 陣營"),
]


def pct(a: float, b: float) -> float:
    return (a / b - 1.0) * 100.0 if b else float("nan")


def fetch(tk: str) -> dict | None:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?range=1y&interval=1d"
    try:
        r = requests.get(url, headers=UA, timeout=20)
        r.raise_for_status()
        q = r.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    except Exception as e:  # noqa: BLE001
        print(f"  ! {tk} 抓取失敗：{type(e).__name__}: {str(e)[:60]}")
        return None
    c = [x for x in q if x is not None]  # 去掉 null 收盤
    if len(c) < 30:
        print(f"  ! {tk} 資料不足（{len(c)} 筆）")
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
        "from_hi": pct(last, max(c)),
    }


def cell(v: float | None) -> str:
    if v is None:
        return '<td class="muted">—</td>'
    cls = "pos" if v >= 0 else "neg"
    return f'<td class="{cls}">{v:+.1f}%</td>'


def flag(b: bool) -> str:
    return '<span class="ok">✅</span>' if b else '<span class="no">❌</span>'


def fmt_price(p: float) -> str:
    return f"{p:,.0f}" if p >= 1000 else f"{p:.2f}"


def build_rows() -> str:
    out = []
    for role, tk, desc in WATCH:
        d = fetch(tk)
        if d is None:
            out.append(
                f'<tr><td>{html.escape(role)}</td><td class="tk">{tk}</td>'
                f'<td>{html.escape(desc)}</td>'
                f'<td colspan="6" class="muted">資料抓取失敗（檢查網路/憑證）</td></tr>'
            )
            continue
        out.append(
            f'<tr><td>{html.escape(role)}</td><td class="tk">{tk}</td>'
            f'<td>{html.escape(desc)}</td>'
            f'<td>{fmt_price(d["price"])}</td>'
            f'{cell(d["m1"])}{cell(d["m3"])}{cell(d["m6"])}'
            f'<td>{flag(d["ma50"])}</td><td>{flag(d["ma200"])}</td>'
            f'<td class="muted">{d["from_hi"]:.1f}%</td></tr>'
        )
    return "\n".join(out)


def build_trends_section() -> str:
    """讀 05 產生的 trends_data.json，渲染真實搜尋動能；無檔則提示先跑 05。"""
    jf = Path(__file__).with_name("trends_data.json")
    if not jf.exists():
        return ('<div class="section"><h2><span class="dot" style="background:#ffb454"></span>'
                'AI PC 搜尋動能（Google Trends）</h2>'
                '<p class="muted">尚無資料。先跑 <code>uv run --native-tls 05_搜尋趨勢_trends.py</code> '
                '產生 trends_data.json 後重生本頁。</p></div>')
    data = json.loads(jf.read_text(encoding="utf-8"))
    kws = data["keywords"]
    maxv = max((k["recent_avg"] for k in kws), default=1) or 1
    rows = []
    for k in kws:
        w = k["recent_avg"] / maxv * 100
        m = k["momentum_pct"]
        arrow = "▲" if m > 3 else ("▼" if m < -3 else "→")
        cls = "pos" if m > 3 else ("neg" if m < -3 else "muted")
        rows.append(
            f'<div class="trow"><span class="tkw">{html.escape(k["keyword"])}</span>'
            f'<div class="ttrack"><div class="tfill" style="width:{w:.0f}%"></div></div>'
            f'<span class="muted" style="text-align:right">{k["recent_avg"]:.0f}</span>'
            f'<span class="{cls}" style="text-align:right">{m:+.1f}% {arrow}</span></div>'
        )
    body = "\n".join(rows)
    return (f'<div class="section"><h2><span class="dot" style="background:#ffb454"></span>'
            f'AI PC 搜尋動能（Google Trends · {html.escape(data["timeframe"])} · 更新 {html.escape(data["updated"])}）</h2>'
            f'{body}'
            f'<p class="muted" style="margin-top:12px;font-size:12px">真實搜尋熱度（相對 0–100，近14日均）；右為動能(近14日 vs 前14日)。'
            f'「Mac Studio」屬通用詞、會壓低利基詞，僅供相對參考。'
            f'<b style="color:var(--accent)"> 解讀：消費端 AI PC 搜尋普遍降溫，但記憶體仍在漲價 → 拉動 HBM 的是資料中心/Rubin，不是 AI PC。</b></p></div>')


def render(rows: str, trends: str) -> str:
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 記憶體動能監控 · {ts}</title>
<style>
:root{{--bg:#0b0e14;--panel:#141925;--panel2:#1c2333;--line:#2a3450;--txt:#e6ecff;
--muted:#8a96b3;--accent:#5b8cff;--green:#3fd68c;--red:#ff5d6c;--amber:#ffb454}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Segoe UI","Microsoft JhengHei",system-ui,sans-serif;background:
radial-gradient(1200px 600px at 70% -10%,#16203a 0,var(--bg) 60%);color:var(--txt);
padding:30px 18px;line-height:1.6;min-height:100vh}}
.wrap{{max-width:1000px;margin:0 auto}}
.kicker{{color:var(--accent);font-weight:700;letter-spacing:3px;font-size:12px;text-transform:uppercase}}
h1{{font-size:26px;margin:6px 0}}
.ts{{color:var(--muted);font-size:13px}}
.thesis{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);
border-radius:12px;padding:16px 18px;margin:20px 0;font-size:14px}}
.thesis b{{color:var(--accent)}}
.section{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;margin:16px 0}}
h2{{font-size:16px;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
h2 .dot{{width:8px;height:8px;border-radius:50%;background:var(--accent)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{padding:9px 10px;border-bottom:1px solid var(--line);text-align:right}}
th:nth-child(-n+3),td:nth-child(-n+3){{text-align:left}}
th{{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.5px}}
.tk{{font-weight:700;color:var(--accent)}}
.pos{{color:var(--green);font-weight:600}} .neg{{color:var(--red);font-weight:600}}
.muted{{color:var(--muted)}} .ok{{color:var(--green)}} .no{{color:var(--red)}}
ol{{padding-left:20px}} ol li{{margin:8px 0;font-size:14px}}
code{{background:var(--panel2);padding:2px 6px;border-radius:5px;font-size:12px}}
.trow{{display:grid;grid-template-columns:140px 1fr 44px 92px;align-items:center;gap:12px;margin:10px 0}}
.tkw{{font-size:13px}}
.ttrack{{background:var(--panel2);border-radius:8px;height:14px;overflow:hidden}}
.tfill{{height:100%;border-radius:8px;background:linear-gradient(90deg,var(--accent),#8db4ff)}}
footer{{color:var(--muted);font-size:12px;margin-top:20px;border-top:1px solid var(--line);padding-top:12px}}
</style></head><body><div class="wrap">
<div class="kicker">AI 記憶體動能監控</div>
<h1>看 Rubin / HBM，不看 DGX Spark</h1>
<div class="ts">資料更新：{ts}　·　重跑 <code>uv run 04_監控頁_generate.py</code> 後重新整理本頁</div>

<div class="thesis">
真正撐起記憶體需求的是 <b>Rubin 放量 → HBM4</b>（單顆 288GB、機櫃記憶體成本佔比 ~25%、漲價 435%）。
DGX Spark/AI PC 用的是 LPDDR5x、<b>不吃 HBM</b>，只當情緒領先指標。
<br>口訣：<b>DGX Spark = 看人心；Rubin/HBM = 看金流。</b>
</div>

<div class="section">
<h2><span class="dot"></span>部位主軸 · 即時動能</h2>
<table>
<thead><tr><th>角色</th><th>代號</th><th>說明</th><th>價格</th><th>1M</th><th>3M</th><th>6M</th><th>&gt;50MA</th><th>&gt;200MA</th><th>距52高</th></tr></thead>
<tbody>
{rows}
</tbody></table>
<p class="muted" style="margin-top:10px;font-size:12px">綠=正動能。理想進場：3M/6M 轉正 + 站上 50/200MA + 貼近 52 週高。</p>
</div>

{trends}

<div class="section">
<h2><span class="dot" style="background:var(--amber)"></span>每日只追 3 個訊號</h2>
<ol>
<li><b>Rubin 放量節奏</b> — Q3 2026 量產、Q4 放量。出貨/排單新聞轉強 = 主升段確認。</li>
<li><b>HBM4 供給/良率</b> — 缺貨、漲價、良率不足 = MU/SK Hynix 動能加速器（現正發生）。</li>
<li><b>價量驗證</b> — 上表 MU/NVDA/TSM 轉正且貼前高 = 進場窗口。</li>
</ol>
</div>

<footer>價量來自 Yahoo Finance Chart API、搜尋動能來自 Google Trends（由 05 產生）。投資決策請結合自身風險。</footer>
</div></body></html>"""


def main() -> None:
    print("抓取即時動能中…")
    rows = build_rows()
    trends = build_trends_section()
    OUT.write_text(render(rows, trends), encoding="utf-8")
    print(f"\n[OK] 已產生：{OUT}")
    print("   直接用瀏覽器打開即可；要更新就重跑本腳本後重新整理。")


if __name__ == "__main__":
    main()
