# GLW 康寧 Glass Bridge — 技術、利空名單與估值

資料更新：2026-06-30
相關筆記：[光通信產業鏈.md](光通信產業鏈.md)、[coupe.md](coupe.md)、[crdo_or_lite.md](crdo_or_lite.md)

---

## 1. Glass Bridge 是什麼

- 發表日：2026-06-24
- 一個用**半導體級離子交換波導 (ion-exchange waveguide)** 製程做的玻璃光學連接器
- 作用：**把光纖的光直接導進光子晶片 (PIC),省去傳統 FAU(光纖陣列單元)或可插拔收發器**
- 解決 CPO 最頭痛的「**尺寸落差 (dimensional gap)**」— 光纖與 PIC 差好幾個數量級
- 合作:GlobalFoundries(玻璃核心封裝);長約客戶 Nvidia / Meta / Amazon

### 首版規格
| 項目 | 規格 | 評語 |
| ---- | ---- | ---- |
| PIC core pitch | **≥ 30µm** | 夠用但非領先,高密度 CPO 還要更細 |
| 耦合損耗 | 目標 **< 2 dB** | 對準用 passive alignment,簡化組裝 |
| 量產狀態 | qualification / 可靠度 / 良率 ramp **都未完成** | 真實不確定性 |

---

## 2. 利空哪些技術 (誰被取代)

| 被衝擊的技術 | 為什麼利空 | 衝擊時程 |
| ------------ | ---------- | -------- |
| **FAU(光纖陣列單元)** | Glass Bridge 賣點就是「**消除對 FAU 的需求**」— 最直接受害 | 長線 (CPO/NPO 商用 2028–2030) |
| **光纖耦合 / 精密對準接合** | 玻璃內波導取代外掛光纖陣列的對準工序 | 長線 |
| **可插拔光收發器 (pluggable transceiver)** | CPO 路線本來就在蠶食 pluggable,Glass Bridge 再加一刀 | 中長線 |
| **稜鏡準直鏡頭 (prism collimator) 方案** | 部分切入 FAU 的鏡頭廠用此卡位,被替代風險 | 長線 |

> ⚠️ 但短期保護傘:導入 Glass Bridge 需 PIC 設計商**重做光介面佈局、重設 spot-size converter、改 bump 結構** → 巨大切換成本形成「**技術慣性 (inertia)**」,反而短期保護現有 FAU 玩家。

---

## 3. 利空哪些公司

### 美股
| Ticker | 公司 | 受影響點 |
| ------ | ---- | -------- |
| LITE | Lumentum | 收發器核心光源 / pluggable 暴露,CPO 路線承壓 |
| (FAU / 收發模組鏈普遍) | — | CPO 賣壓波及整條光模組 |

### 台股(盤面賣壓重心 — FAU / 光纖耦合 / 矽光子題材)
| 個股 | 角色 | 當日反應 |
| ---- | ---- | -------- |
| **上詮** | 光纖陣列 (FAU) 與矽光子晶片精密對準接合 — **最核心受害** | 走弱 |
| **大立光** | 切入矽光子 FAU + 稜鏡準直鏡頭(仍送樣未量產) | 下跌 |
| **環宇-KY、光聖、聯鈞、光環、聯光通、全新、穩懋、康聯訊** | FAU / 光耦合 / 磊晶相關 | 跌 2%~5% |
| **智邦、統新、前鼎、台聯電、華星光、IET-KY、波若威** | 光收發模組 / 光學元件 | 走弱 |

> 註:波若威是 Nvidia Spectrum-X 矽光子生態系官方夥伴 — 生態地位仍在,但情緒面被掃到。

---

## 4. 受惠方(對照組,非利空)

| 對象 | 為何受惠 |
| ---- | -------- |
| **GLW 康寧自己** | 噴出創新高,+10~15%,加 Nvidia 注資 + Amazon 訂單 |
| **玻璃基板 / 玻璃核心 (glass substrate / glass-core)** | TGV、玻璃載板題材同步走強 |
| **GFS GlobalFoundries** | Glass Bridge 封裝合作方 |

---

## 5. 是否誇大 — 故事真,時間軸被壓縮

- 技術本身不是吹的(離子交換波導、<2dB、解決 dimensional gap 是真問題)
- **誇大在「多快兌現」**:
  - 大摩 (Morgan Stanley)、花旗 (Citi):**未來 1–2 年對現有供應鏈實質影響「極有限」**
  - 真正破壞要等 **CPO/NPO 商用化 2028–2030**
  - 長約是 framework / 預付款,不等於明天放量出貨
- → 單日大漲反映的是**3–5 年後的選擇權,卻用今天估值付了全額**

---

## 6. 便宜嗎 / 風險回報比 — 不便宜,R/R 對追高者不利

| 指標 | 數值 | 對照 |
| ---- | ---- | ---- |
| 現價 | ~$248–255 | 6/25 創歷史新高 |
| Trailing P/E | **~90–105x** | 自己 5 年中位數 ~45x → 貴一倍以上 |
| Forward P/E | **~70–78x** | 硬體業中位數 ~24x → 高 3 倍 |
| 分析師共識目標價 | **$182–188** | 比現價低 25~35% |
| GuruFocus GF Value | $60(估) / fair value ~$149 | 模型派:嚴重高估 |

### 下檔風險清單
- 太陽能晶圓廠瓶頸 → Q2 多 $3,000 萬費用
- 內部人(CEO Weeks 等)6 月賣超 16 萬股、~$3,000 萬,**零買進**
- 被重分類進 Russell Growth 指數 → 部分漲幅是**被動資金機械式買進**,退潮也快

---

## 7. 結論

> 技術是真利多,但 $248、70–105x P/E 已把 2030 年劇本提前付清。**便宜談不上,R/R 目前對追高者不利。**
> Glass Bridge 不是騙局,但「短期會顛覆」被市場誇大 — 良率未過、客戶切換成本、30µm 早期規格,決定它是 **2028+ 的故事,不是 2026**。
>
> 想參與:不追高,等指數被動買盤 + 財報情緒退潮後的回檔,或靠近分析師共識 $180 分批。

---

## 來源
- [康寧 Glass Bridge 衝擊 FAU? — CMoney](https://www.cmoney.tw/forum/article/180191689)
- [康寧發布 Glass Bridge 恐衝擊 FAU — 經濟日報](https://money.udn.com/money/story/5599/9588628)
- [康寧 Glass Bridge 引爆 CPO 賣壓 — 鉅亨網](https://news.cnyes.com/news/id/6515191)
- [康寧新組件掀革命 光通訊族群承壓 — 工商時報](https://www.ctee.com.tw/news/20260630700232-439901)
- [Wall Street: FAU 廠承壓、光模組短期相對安全 — AllWeatherFinance](https://allweatherfinance.com/how-significant-is-the-impact-of-the-glass-bridge-wall-street-fau-manufacturers-face-disruptive-pressure-while-ai-optical-module-companies-are-relatively-safe-for-now/)
- [大摩/花旗:2 年內不太可能顛覆 — BigGo](https://finance.biggo.com/news/3a55b7c6-504f-4fd7-84d5-db01180f454d)
- [GLW Forward PE — GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/GLW)
- [GLW 目標價 — MarketBeat](https://www.marketbeat.com/stocks/NYSE/GLW/forecast/)
