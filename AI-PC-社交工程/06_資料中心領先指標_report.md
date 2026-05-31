# 資料中心領先指標追蹤（A）

> 修正前面工具的盲點：Google Trends 量的是**消費端搜尋**，但賺錢的是**資料中心**。
> 本報告改盯「真正領先資料中心/HBM 週期」的四個指標 + 一個可即時量化的循環階段儀表。
> 研究日期：2026-05-31

---

## 四大領先指標（即時讀數）

### ① HBM 供需與報價 —— 最直接的領先指標
- **2026 全數完售**：SK Hynix、Micron、Samsung 三家 HBM 產能 2026 年**全部售罄**。
- **漲價**：Samsung / SK Hynix 對 2026 訂單 **HBM3E 漲價約 20%**；Micron 2026 HBM（含 HBM4）價量全鎖定。
- **HBM4 放量 2Q26**：2026 年營收結構約 **55% HBM4 / 45% HBM3E**，HBM4 從第三季起量。
- ⚠️ **唯一的警鈴**：部分分析師預期 **2026 之後** HBM 價格可能進入修正（產能擴出、競爭加劇）。
- **解讀**：現在仍是「完售 + 漲價」= 多頭續命；**轉折點在 2027，不在 2026**。

### ② Hyperscaler 資本支出 —— 訂單的源頭
- **2026**：四大（GOOGL/AMZN/MSFT/META）合計 **$725B（年增 77%）**，其中約 **75%（$450B）投 AI 基礎建設**。
  - 個別：Amazon ~$200B、MSFT ~$190B、Alphabet ~$185B、Meta ~$135B。
- **2027**：多家投行（Evercore、BofA）估**突破 $1 兆**；Goldman 估 2025–27 三年 $1.15 兆（是 2022–24 的兩倍多）；Alphabet 2027 上看 $250B。
- **解讀**：花錢的源頭還在**加速**，且能見度延伸到 2027 → 對記憶體/封裝是結構性拉力。

### ③ CoWoS 先進封裝 —— Rubin 的真瓶頸
- **TSM 2026 capex $52–56B**，把 CoWoS 月產能拉到 **13–15 萬片（約翻 4 倍）**、嘉義 AP7 成全球最大封裝廠。
- **NVIDIA 已鎖定 TSM 2026 封裝產能的 60%+**，Rubin R100 2026 年底全產。
- **瓶頸**：微影/鍵合設備交期；若 Phase 1/2 提前上線，**AI 晶片荒可能 2027 年初緩解**。
- **解讀**：封裝是卡點，倍增=供給在追上來。「2027 初緩解」與 ① 的「2026 後修正」**指向同一個時間窗**。

### ④ 循環階段儀表（可即時量化）—— 見 `06_領先指標掃描_scan.py`
- 產業鏈時序：**設備訂單 → 記憶體資本支出 → HBM 報價**。
- 用**設備股 vs 記憶體股的相對動能**判斷循環位置：
  - 設備動能 ≥ 記憶體動能、皆為正 → **循環早中期（capex 仍加速，順勢做多）**
  - 設備動能轉弱、記憶體仍強 → **循環末期警訊（上游訂單見頂領先記憶體）**

---

## 綜合結論（給動能投資者）

**三條質化指標(HBM、capex、CoWoS)2026 全部朝上、吃緊**，沒有一條現在轉空 → **2026 全年仍是順勢做多記憶體/上游的環境**。

但**三條獨立指標都指向「2027 年初」是第一個轉折窗**：
- HBM 報價「2026 後」可能修正
- CoWoS 產能倍增、晶片荒「2027 初」緩解
- capex 雖續創高，但 2027 是「兆元級基期」，年增率必然放緩

**操作含義**：
1. **現在**：繼續順勢，記憶體雙雄(MU/SK Hynix)動能未破不需動作（價量已在 52 週高）。
2. **退場雷達(2026Q4–2027Q1 啟動)**：盯 **HBM 合約價環比轉負**、**CoWoS 交期縮短/產能過剩新聞**、**hyperscaler capex 指引下修**——三者任一出現即「循環見頂」的第一槍。
3. **量化哨兵**：每日跑 `06_領先指標掃描_scan.py`，當**設備動能掉到記憶體之下**時，就是產業鏈訂單見頂的領先訊號，比財報早 1–2 季。

> 一句話：**2026 抱緊，2027 初開始看後照鏡。** 這次社交工程方法論的真正升級——把儀表從「消費搜尋」換成「資料中心領先指標」。

---

## 資料來源
- [SK hynix 2026 Outlook / HBM4 — TrendForce](https://www.trendforce.com/news/2026/01/05/news-sk-hynix-2026-outlook-hbm3e-remains-mainstream-hbm4-dual-strategy-amid-triple-market-headwinds/)
- [Micron 2026 HBM fully booked, CapEx $20B — TrendForce](https://www.trendforce.com/news/2025/12/18/news-micron-hikes-capex-to-20b-with-2026-hbm-supply-fully-booked-hbm4-ramps-2q26/)
- [Samsung/SK Hynix ~20% HBM3E price hike 2026 — TrendForce](https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/)
- [Big Tech capex $725B in 2026 (+77%) — Tom's Hardware](https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion)
- [AI capex topping $1 trillion in 2027 — CNBC](https://www.cnbc.com/2026/04/30/ai-boom-big-tech-capital-expenditures-now-seen-topping-1-trillion-in-2027-.html)
- [TSMC $56B capex to double CoWoS for Rubin — FinancialContent](https://www.financialcontent.com/article/tokenring-2026-1-26-the-great-unclogging-tsmc-commits-56-billion-capex-to-double-cowos-capacity-for-nvidias-rubin-era)
