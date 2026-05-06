"""
market_sentiment_chart.py
抓取近一個月的貪婪指數、VIX 指數、Call/Put Ratio 並畫成折線圖
"""

import datetime
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import requests
import yfinance as yf

CNN_API = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"
_CNN_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def _fetch_cnn_json() -> dict:
    resp = requests.get(CNN_API, timeout=15, headers=_CNN_HEADERS)
    resp.raise_for_status()
    return resp.json()


# ── 1. Fear & Greed Index (CNN) ──────────────────────────────────────────────
def fetch_fear_greed(cnn_data: dict) -> pd.DataFrame:
    records = cnn_data["fear_and_greed_historical"]["data"]
    # Each record: {'x': epoch_ms, 'y': value, 'rating': str}
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["x"], unit="ms").dt.normalize()
    df = df.set_index("date")[["y"]].rename(columns={"y": "fear_greed"})
    df["fear_greed"] = pd.to_numeric(df["fear_greed"], errors="coerce")
    return df


# ── 2. VIX ───────────────────────────────────────────────────────────────────
def fetch_vix(start: datetime.date, end: datetime.date) -> pd.DataFrame:
    raw = yf.download("^VIX", start=start, end=end, progress=False, auto_adjust=True)
    # yfinance may return MultiIndex columns — flatten to 1-D Series
    close = raw["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    df = close.to_frame(name="vix")
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df["vix"] = pd.to_numeric(df["vix"], errors="coerce")
    return df


# ── 3. Put/Call Ratio (CNN API — put_call_options field) ─────────────────────
def fetch_put_call(cnn_data: dict) -> pd.DataFrame:
    records = cnn_data["put_call_options"]["data"]
    # Each record: {'x': epoch_ms, 'y': value, ...}
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["x"], unit="ms").dt.normalize()
    df = df.set_index("date")[["y"]].rename(columns={"y": "put_call"})
    df["put_call"] = pd.to_numeric(df["put_call"], errors="coerce")
    return df


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=35)  # 取 35 天確保 30 個交易日

    print(f"Date range: {start} → {today}")

    print("Fetching CNN Fear & Greed data...")
    try:
        cnn_json = _fetch_cnn_json()
        print("  CNN API OK")
    except Exception as e:
        print(f"  ERROR fetching CNN API: {e}")
        cnn_json = None

    print("Parsing Fear & Greed Index...")
    try:
        fg = fetch_fear_greed(cnn_json)
        fg = fg[fg.index >= pd.Timestamp(start)].copy()
        print(f"  Got {len(fg)} data points")
    except Exception as e:
        print(f"  ERROR: {e}")
        fg = pd.DataFrame()

    print("Fetching VIX (yfinance)...")
    try:
        vix = fetch_vix(start, today)
        print(f"  Got {len(vix)} data points")
    except Exception as e:
        print(f"  ERROR: {e}")
        vix = pd.DataFrame()

    print("Parsing Put/Call Ratio (CNN API)...")
    try:
        pc = fetch_put_call(cnn_json)
        pc = pc[pc.index >= pd.Timestamp(start)].copy()
        print(f"  Got {len(pc)} data points")
    except Exception as e:
        print(f"  ERROR: {e}")
        pc = pd.DataFrame()

    # ── Plot ──────────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle(
        f"Market Sentiment — Last ~30 Days  (as of {today})",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    date_fmt = mdates.DateFormatter("%m/%d")

    # ── Fear & Greed ──
    ax1 = axes[0]
    if not fg.empty:
        ax1.plot(fg.index, fg["fear_greed"], color="darkorange", linewidth=2, marker="o", markersize=3)
        ax1.fill_between(fg.index, fg["fear_greed"], 50,
                         where=fg["fear_greed"] >= 50, alpha=0.2, color="green", label="Greed")
        ax1.fill_between(fg.index, fg["fear_greed"], 50,
                         where=fg["fear_greed"] < 50, alpha=0.2, color="red", label="Fear")
        # 最新值標注
        last_val = float(fg["fear_greed"].iloc[-1])
        last_date = fg.index[-1]
        ax1.annotate(f"{last_val:.0f}", xy=(last_date, last_val),
                     xytext=(5, 5), textcoords="offset points", fontsize=9, color="darkorange")
        ax1.legend(loc="upper left", fontsize=8)
    ax1.axhline(50, color="gray", linestyle="--", linewidth=0.8)
    ax1.set_ylabel("Fear & Greed (0–100)", fontsize=9)
    ax1.set_ylim(0, 100)
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.set_yticklabels(["0\nExtreme\nFear", "25", "50", "75", "100\nExtreme\nGreed"], fontsize=7)
    ax1.xaxis.set_major_formatter(date_fmt)
    ax1.grid(True, alpha=0.3)

    # ── VIX ──
    ax2 = axes[1]
    if not vix.empty:
        ax2.plot(vix.index, vix["vix"], color="firebrick", linewidth=2, marker="o", markersize=3)
        last_vix = float(vix["vix"].iloc[-1])
        last_date = vix.index[-1]
        ax2.annotate(f"{last_vix:.2f}", xy=(last_date, last_vix),
                     xytext=(5, 5), textcoords="offset points", fontsize=9, color="firebrick")
    ax2.axhline(20, color="gray", linestyle="--", linewidth=0.8, label="VIX=20 (elevated)")
    ax2.axhline(30, color="orange", linestyle="--", linewidth=0.8, label="VIX=30 (high fear)")
    ax2.set_ylabel("VIX", fontsize=9)
    ax2.xaxis.set_major_formatter(date_fmt)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left", fontsize=8)

    # ── Put/Call Ratio ──
    ax3 = axes[2]
    if not pc.empty:
        ax3.plot(pc.index, pc["put_call"], color="steelblue", linewidth=2, marker="o", markersize=3)
        last_pc = float(pc["put_call"].iloc[-1])
        last_date = pc.index[-1]
        ax3.annotate(f"{last_pc:.2f}", xy=(last_date, last_pc),
                     xytext=(5, 5), textcoords="offset points", fontsize=9, color="steelblue")
    ax3.axhline(1.0, color="orange", linestyle="--", linewidth=0.8, label="P/C=1.0 (bearish)")
    ax3.axhline(0.7, color="green", linestyle="--", linewidth=0.8, label="P/C=0.7 (neutral)")
    ax3.set_ylabel("Put/Call Ratio (CNN)", fontsize=9)
    ax3.xaxis.set_major_formatter(date_fmt)
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc="upper left", fontsize=8)

    plt.tight_layout()
    out_path = f".github/skills/daily-check/market_sentiment_{today}.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"\nChart saved → {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
