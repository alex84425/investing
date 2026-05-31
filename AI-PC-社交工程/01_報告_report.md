# AI PC 社交工程 — 投資觀察報告

> 任務：透過搜尋關鍵字趨勢，觀察「跑 AI agent 大家都買哪種 PC/硬體」→ 找出三種主流配置 → 做成 table → 提出更好的做法
> 日期：2026-05-31

---

## 第 1 步：關鍵字趨勢觀察

**真實 Google Trends 數據**（`05_搜尋趨勢_trends.py` 抓取，today 3-m，2026-05-31）：

| 關鍵字 | 近14日均熱度 | 動能(近14日 vs 前14日) |
|---|---|---|
| Mac Studio | 38 | **-53%** ▼ |
| RTX 5090 | 35 | **-41%** ▼ |
| local LLM | 16 | **-66%** ▼ |
| DGX Spark | 8 | **-49%** ▼ |
| AMD Strix Halo | 0 | **-80%** ▼ |

**關鍵解讀**：消費端 AI PC 的搜尋熱度**全面降溫**（五個關鍵字動能全為負）。但同期記憶體仍在漲價（RTX 5090 / DGX Spark 因記憶體短缺漲）。**搜尋降溫 + 記憶體漲價 = 拉動 HBM 的不是消費端 AI PC，而是資料中心/Rubin。** 這個社交工程訊號**獨立驗證**了下方「看 Rubin / HBM、不看 AI PC」的結論。

> 補充（質化）：社群討論仍圍繞 **VRAM≥24GB**（跑 agent 多吃顯存）、**128GB 統一記憶體**（能否跑 70B）。但搜尋量級上「Mac Studio」這類通用詞會壓低利基詞，僅供相對參考。

---

## 第 2 步：四種主流配置（含售價比較）

| 類型 | 代表機種 | 記憶體/VRAM | 售價 (USD, 2026/5) | 強項 | 弱項 | 受惠標的(momentum) |
|---|---|---|---|---|---|---|
| **① 單卡暴力型 (CUDA 王道)** | RTX 5090 自組 PC | 32GB GDDR7 | 顯卡 $2,900–3,500，整機 ~$4,000+（街價，MSRP 原 $1,999，記憶體短缺漲價） | 最快吞吐 (~186 tok/s @8B)、生態最成熟 | 725W 耗電、要當系統管理員、VRAM 卡 70B | **NVDA**、記憶體 **MU** |
| **② 統一記憶體型 (省心王)** | Mac Studio M4 Max 128GB | 128GB 統一記憶體 | ~$3,500–4,000（128GB 配置） | 跑 70B 不量化、省電、開箱即用「最會被真正用起來」 | 帶寬(~400GB/s)輸 5090、非 CUDA | **AAPL**、台積 **TSM** |
| **③ CUDA + 大記憶體型 (專業/離線)** | NVIDIA DGX Spark 128GB | 128GB 統一記憶體 + CUDA | **$4,699**（2/27 由 $3,999 漲價，記憶體短缺） | 大模型 + CUDA、適合 air-gapped/合規/離線迭代 | 利基、性價比爭議、出貨小眾 | **NVDA**（生態綁定） |
| **④ 性價比黑馬 (x86 統一記憶體)** | AMD Strix Halo / Ryzen AI Max+ 395 128GB | 128GB 統一記憶體 @256GB/s | **~$2,000**（Framework Desktop $1,999、GMKtec ~$1,499、AMD 官方 Halo 開發機 $3,999） | 最便宜、x86 相容、Linux 生態、70B 吞吐略勝 Mac | 軟體生態落後 CUDA、NPU 工具鏈不成熟 | **AMD**、台積 **TSM**、記憶體 **MU** |

> ⚠️ **動能訊號**：RTX 5090 與 DGX Spark 在 2026 上半年皆因「記憶體短缺」漲價（DGX Spark +18%）。硬體漲價≠終端需求降溫，而是**上游記憶體吃緊**——這直接驗證下方第 3 步「盯記憶體上游」的論點。

---

## 第 3 步：更好的做法（升級版觀察框架）

純看搜尋熱度的盲點——**熱搜的是「型號名」，但賺錢的是「賣鏟子的上游」**。建議把觀察框架從「大家買哪台」升級成「不管買哪台，錢最後流去哪」：

1. **抓「結構性公約數」而非熱門機種**：三種配置全都吃 **HBM/高速記憶體 + 先進封裝 + 晶圓代工**。與其賭 NVDA vs AAPL 誰贏，不如盯共同上游：**TSM、MU、SK Hynix**——「鏟子的鏟子」，動能不易被單一機種輪動打斷。
2. **用 Google Trends 當領先指標**：固定追蹤 `RTX 5090`、`DGX Spark`、`Mac Studio AI`、`local LLM`、`VRAM` 的 **週/月斜率**，斜率轉正 + 突破前高時，對應標的進場時機通常領先財報 1–2 季。
3. **加一層「賣方訊號」交叉驗證**：搜尋趨勢疊上各家**出貨/缺貨/交期**新聞（5090 缺貨、DGX Spark 排隊），缺貨 = 需求 > 供給 = 動能確認。

---

## 資料來源 Sources

- [Best Hardware for Running Local AI Models (2026)](https://www.modemguides.com/blogs/ai-infrastructure/best-hardware-running-local-ai-models-2026)
- [Best Hardware for Local AI Agents 2026 — Compute Market](https://www.compute-market.com/blog/best-hardware-ai-agents-local-2026)
- [Mac Mini M4 Pro vs RTX 5090 vs DGX Spark — MindStudio](https://www.mindstudio.ai/blog/mac-mini-m4-pro-vs-rtx-5090-vs-dgx-spark-local-ai-hardware-2026)
- [RTX 5090 vs DGX Spark vs AMD Benchmark — InsiderLLM](https://insiderllm.com/guides/rtx-5090-local-ai-benchmarks/)
- [What to Buy for Local LLMs (April 2026) — Julien Simon](https://julsimon.medium.com/what-to-buy-for-local-llms-april-2026-a4946a381a6a)
- [AMD Ryzen AI Max+ 395 (Strix Halo) for Local AI — Local AI Master](https://localaimaster.com/blog/strix-halo-ai-max-395-guide)
- [Nvidia DGX Spark $700 price hike (memory shortage) — Tom's Hardware](https://www.tomshardware.com/desktops/mini-pcs/nvidia-dgx-spark-gets-18-percent-price-increase-as-memory-shortages-bite-founders-edition-now-usd4-699-up-from-usd3-999)
- [RTX 5090 Price Tracker (May 2026) — BestValueGPU](https://bestvaluegpu.com/history/new-and-used-rtx-5090-price-history-and-specs/)
