---
name: yt-summary
description: "Summarize a YouTube video from its URL. Use when: yt summary, youtube summary, YT 摘要, 幫我總結這支影片, summarize youtube, 看這個影片, youtube url, youtu.be, watch?v="
argument-hint: "<youtube_url>"
---

# YouTube Summary Skill

將任意 YouTube 影片網址轉成結構化摘要。

腳本位置：`.github/skills/yt-summary/script/get_transcript.py`

---

## 流程

### Step 1：安裝依賴（首次使用）

```
uv sync
```

### Step 2：抓取逐字稿

```
uv run python .github/skills/yt-summary/script/get_transcript.py <youtube_url>
```

腳本輸出格式：

```
VIDEO_ID: <id>
URL: <url>
LANGUAGE: <zh/en/...>
ENTRY_COUNT: <n>
---TRANSCRIPT---
[00:00] 文字內容
[00:05] 文字內容
...
```

- 語言優先順序：`zh-TW` → `zh-Hant` → `zh` → `en` → 其他可用語言
- 若逐字稿被停用或不存在，腳本自動 fallback 至 **yt-dlp + Whisper** 本地轉錄
- Whisper fallback 需要：`yt-dlp`（`uv tool install yt-dlp`）和 `openai-whisper`（已在 pyproject.toml）
- Whisper 使用 `base` 模型 + `language="zh"`，首次執行會下載模型（~139MB）
- LANGUAGE 欄位顯示 `zh (whisper)` 表示使用了 Whisper fallback

### Step 3：產生摘要

拿到逐字稿後，按以下格式輸出摘要：

```
# 📺 YouTube 摘要

**標題**（從逐字稿推斷）
**連結**：<url>
**語言**：<language>

## 🗂️ 重點摘要

（3–5 條核心重點，每條一句話）

## 📋 章節概述

（依時間戳分段，每段 2–3 句說明內容）

## 💡 關鍵結論

（1–2 句整體結論或行動建議）
```

### 錯誤處理

| 錯誤訊息                   | 原因                    | 解法                          |
| -------------------------- | ----------------------- | ----------------------------- |
| `Transcripts are disabled` | 影片作者關閉字幕        | 自動 fallback 至 Whisper      |
| `No transcript found`      | 無任何語言的字幕        | 自動 fallback 至 Whisper      |
| `yt-dlp failed`            | yt-dlp 未安裝或下載失敗 | 執行 `uv tool install yt-dlp` |
| `Whisper fallback failed`  | Whisper 未安裝          | 執行 `uv add openai-whisper`  |
| `Cannot extract video ID`  | URL 格式不對            | 請使用者確認網址              |
| `ImportError`              | 套件未安裝              | 執行 `uv sync`                |
