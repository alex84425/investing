---
name: daily-check
description: "Daily portfolio check routine. Use when: 每日檢查, daily check, 今天有什麼事, 早安, morning check, 持倉新聞, 財報提醒, earnings reminder, 每日流程, daily routine."
argument-hint: "no arguments needed"
---

# Daily Check Skill

每日持倉檢查流程，依序執行以下三個步驟。

腳本位置：`.github/skills/daily-check/script/`

---

## Step 1：抓取最新新聞，比對持倉

1. 讀取 `tw_stock.md` 取得台股持倉清單
2. 讀取 `personal_position.md` 取得美股持倉清單
3. 用 `fetch_webpage` 抓取 https://www.newsdigest.ai/ 的內容（已驗證可存取）
4. 比對新聞與持倉，**如果有任何新聞與持倉標的相關，用 ⚠️ 醒目標示提醒**

輸出格式：

```
## 📰 持倉相關新聞

⚠️ **CRDO** — 標題：xxx（摘要一句話）
⚠️ **台積電** — 標題：xxx（摘要一句話）
✅ 其餘持倉今日無重大新聞
```

若 newsdigest.ai 無法存取，改用 Google Finance 或 Yahoo Finance 查詢各持倉標的近期新聞。

---

## Step 2：台股法說會提醒

執行腳本：`uv run python .github/skills/daily-check/script/check_tw_conferences.py`

腳本會：

1. 讀取 `tw_stock.md` 取得持倉名單
2. 產生 Goodinfo 與 Google 搜尋連結
3. 用 `fetch_webpage` 查詢各連結，判斷近一週是否有法說會
4. 若一週內有法說會，用 🔴 標示

輸出格式：

```
## 🇹🇼 台股法說會提醒（未來 7 天）

🔴 **台積電** — 2026-05-10 法說會
✅ 群聯 — 近一週無法說
✅ 臺慶科 — 近一週無法說
```

---

## Step 3：美股財報日提醒

執行腳本：`uv run python .github/skills/daily-check/script/check_earnings.py`

腳本會：

1. 用 yfinance 即時查詢所有美股持倉的財報日期
2. 找出距今 **7 天內** 要公布財報的標的
3. 輸出人類可讀格式 + JSON

同時讀取 `personal_position.md` 中的持倉佔比與備註，合併顯示。

輸出格式：

```
## 🇺🇸 美股財報提醒（未來 7 天）

🔴 **PGY** — 2026-05-07（佔比 2.5%）⚠️ 虧損 -62%，需決定去留
🔴 **WLDN** — 2026-05-08（佔比 2.1%）
✅ 其餘持倉財報日皆超過一週
```

---

## 最終輸出

將三個步驟合併成一份簡潔報告：

```
# 📋 Daily Check — {今天日期}

## 📰 持倉相關新聞
（Step 1 結果）

## 🇹🇼 台股法說會（7 天內）
（Step 2 結果）

## 🇺🇸 美股財報（7 天內）
（Step 3 結果）

## 🎯 今日行動建議
- （根據以上資訊，列出 1-3 條具體建議）
```
