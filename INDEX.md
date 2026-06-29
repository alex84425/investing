# 研究筆記索引 INDEX

> 全庫 22 篇筆記的目錄。更新：2026-06-29
> 用法：找主題 → 點檔名。問「誰卡關」直接看下方〈供應鏈瓶頸速查〉。

---

## 📊 持倉與操作

| 檔案 | 一句話 |
|---|---|
| [portfolio_summary.md](portfolio_summary.md) | 美股組合摘要：總市值 $19.3 萬、未實現 -16%；前五大持倉 NBIS / CRDO / SSRM / PGY / WLDN |
| [personal_position.md](personal_position.md) | 持股財報日曆 + 重要程度標記；CRDO+MU+TSM 合計佔 72%，6–7 月是決定性時刻 |
| [台股倉位.md](台股倉位.md) | 台股觀察清單：台積電、群聯、臺慶科、華城 |
| [daily_check.md](daily_check.md) | 每日流程 SOP：查 newsdigest、法說/財報提醒、貪婪/VIX/put-call、OpenAI×馬斯克官司 |
| [options_strategy_explained.md](options_strategy_explained.md) | 選擇權槓桿教學：為何選 Deep ITM（Strike 175）做 2 倍槓桿 |

## 🔌 AI 基礎設施 — 光通信 / 互連

| 檔案 | 一句話 |
|---|---|
| [光通信產業鏈.md](光通信產業鏈.md) | 光通信上中下游分類（GLW/LITE→CRDO/MRVL/AVGO/TTMI→AMD）+ 毛利/PE/財報日 |
| [crdo_or_lite.md](crdo_or_lite.md) | LITE（光/訓練骨幹）vs CRDO（銅/推論機櫃內）戰略；啞鈴式配置 CRDO 40%/LITE 30% |

## 🧠 AI 算力 — GPU / 記憶體 / 封裝

| 檔案 | 一句話 |
|---|---|
| [NVIDIA-Q1-FY2027/nvidia_q1_fy2027_analysis.md](NVIDIA-Q1-FY2027/nvidia_q1_fy2027_analysis.md) | NVDA Q1 FY27 財報解析：營收 $81.6B（+85%），Blackwell/Rubin 動能 |
| [20260101_discuss.md](20260101_discuss.md) | 美光 MU（HBM 低估追趕者）+ 台積電 TSM（CoWoS 壟斷者）雙引擎；2027 供給海嘯日曆 |
| [cbrs.md](cbrs.md) | Cerebras（CBRS）IPO 深度分析：推論市場定位、晶圓級晶片，仍虧損、財務危機 |

## 🖥️ AI-PC 社交工程（趨勢觀察專案）

| 檔案 | 一句話 |
|---|---|
| [AI-PC-社交工程/00_任務_task.md](AI-PC-社交工程/00_任務_task.md) | 專案任務定義：用 Google 搜尋趨勢看大家跑 agent 買哪種 PC |
| [AI-PC-社交工程/01_報告_report.md](AI-PC-社交工程/01_報告_report.md) | 四種主流配置比較；結論：拉動 HBM 的是資料中心/Rubin 不是消費端 AI PC |
| [AI-PC-社交工程/06_資料中心領先指標_report.md](AI-PC-社交工程/06_資料中心領先指標_report.md) | 四大領先指標：HBM 供需、Hyperscaler capex、CoWoS、循環階段儀表 |

## ⚠️ 風險 / 其他主題

| 檔案 | 一句話 |
|---|---|
| [黑天鵝.md](黑天鵝.md) | 黑天鵝清單：OpenAI IPO 失敗、海力士上市致美光暴跌 |
| [potential.md](potential.md) | Seeking Alpha 高 Quant Rating 清單（多檔 6 月漲 100–1000%，追高風險） |
| [腸道微生物抗癌研究.md](腸道微生物抗癌研究.md) | 生技主題：腸道微生物群決定免疫療法成效（腎癌/肺癌/黑色素瘤三研究） |

---

## 🔧 供應鏈瓶頸速查（誰卡關）

> 從上述筆記抽取的關鍵卡點，AI 算力鏈由下而上：

| 環節 | 卡關點 / 瓶頸 | 受惠標的 | 來源筆記 |
|---|---|---|---|
| **先進封裝** | CoWoS 是 Rubin 真瓶頸；TSM 2026 把月產能拉 ~4 倍至 13–15 萬片，嘉義 AP7 為全球最大 | **TSM**（壟斷） | 06_資料中心領先指標、20260101 |
| **HBM 記憶體** | 2026 三家（SK海力士/美光/三星）產能**全售罄**、HBM3E 漲價 ~20%；3:1 排擠效應推升 DDR5 | **MU**、SK海力士、三星 | 06_資料中心領先指標、20260101 |
| **機櫃內互連（銅）** | <3m 銅線是王道（NVL72/Groq 依賴）；銅價暴漲壓 Credo 毛利但證明不可替代 | **CRDO**、ALAB、MRVL | crdo_or_lite |
| **長距光互連** | >3m 必須用光；Google TPU 的 OCS 架構鎖死高階雷射需求 | **LITE**、GLW | crdo_or_lite、光通信產業鏈 |
| **訊號處理** | 800G+ 光模組的 PAM4 DSP / SerDes IP | MRVL、AVGO、CRDO | 光通信產業鏈 |
| **算力源頭** | GPU 需求拉動全鏈；Blackwell→Rubin 迭代 | **NVDA**、AMD | nvidia_q1_fy2027 |

**轉折風險時間軸**：2026 全年偏安全 → 2027/2 SK海力士 M15X 放量 → **2027/5 龍仁廠完工＝產能海嘯（紅色警戒）**。
