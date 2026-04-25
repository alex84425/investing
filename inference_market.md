# AI 推論市場投資分析
> 更新日期：2026-04-18

---

## Q：Agent 場景推論 — 這些公司是 Chip 公司嗎？他們是算力 Infrastructure 嗎？

**是，但分層次。**

Agent 推論與傳統 LLM 推論的本質差異：
- Agent 會**反覆呼叫模型**（Observe → Reason → Act 循環）
- 每個任務可能觸發數十到數百次 inference pass
- 需要**低延遲 + 高吞吐量**同時兼顧

| 層次 | 代表公司 | 是 Chip 公司？ | 是算力 Infrastructure？ | 備注 |
|:---|:---|:---:|:---:|:---|
| GPU 霸主 | NVIDIA | ✅ | ✅ | 萬用型，市占 75-87% |
| 低延遲特化 | Groq | ✅ | ✅ | LPU 架構，SRAM-based，適合 agent 即時推論 |
| 超大 on-chip 記憶體 | Cerebras | ✅ | ✅ | Wafer-Scale Engine |
| 雲端自製晶片 | Google (TPU), AWS (Inferentia) | ✅ | ✅ | 非公開投資標的 |
| 邊緣 AI | Qualcomm | ✅ | ⚠️ | Edge 推論，非數據中心 infra |
| 新創競爭者 | Tenstorrent, SambaNova | ✅ | ⚠️ | 非上市，無法直接投資 |

**投資含義**：可投資的公開標的主要是 NVIDIA + AMD。Groq/Cerebras 仍是私有公司。

---

## Q：CPU GPU 推論比

GPU 在 transformer 模型推論上的效率通常比 CPU 快 **10x~100x**，取決於模型大小與批次大小。

| 場景 | 偏好硬體 | 原因 |
|:---|:---|:---|
| 大型語言模型（LLM）推論 | GPU / ASIC | 需要高記憶體頻寬 + 並行計算 |
| 小模型 / 邊緣推論 | CPU / NPU | 成本低，延遲可接受 |
| Agent 多 pass 推論 | GPU（低延遲型） | 需要高吞吐 + 快速 context 重建 |
| 批量推論（Batch） | GPU | 效率最高 |

---

## Q：GPU CPU 毛利率

| 公司 | 毛利率 | 核心產品 | 評注 |
|:---|:---|:---|:---|
| **NVIDIA** | **70% – 88%** | AI GPU (H100, B200) | 定價權極強，CUDA 護城河 |
| **AMD** | **45% – 50%** | CPU + GPU 混合 | 成長中，受競爭壓制 |
| **Intel** | **30% – 35%** | 傳統 CPU + 晶圓廠轉型 | 重資本轉型拖累毛利 |

NVIDIA 的高毛利率 = CUDA 軟體護城河讓切換成本極高，定價權無人能敵。

---

## Q：AMD 還算便宜嗎？

**當前估值（截至 2026-04-17）**

| 指標 | 數值 |
|:---|:---|
| TTM P/E（歷史本益比） | ~104x – 105x |
| **Forward P/E（預期本益比）** | **~28.6x** |
| 分析師平均目標價 | ~$291（現價 ~$278） |
| 分析師共識評級 | Moderate Buy |

**🐂 Bull Case（便宜論）：**
- Forward P/E ~28.6x 對高成長 AI 公司不貴
- DCF 模型顯示可能低估約 20%
- MI350/MI450 + Helios 平台搶食 NVIDIA 市場
- 數據中心 CPU 市占近 50%，作為 GPU 的導流基礎
- 收購 ZT Systems，打造端到端機架級解決方案

**🐻 Bear Case（不便宜論）：**
- TTM P/E 達 104x，任何不確定性都危險
- 市場已大幅 price in AI 增長預期
- CUDA 生態護城河難以突破，ROCm 仍在追趕

**結論**：AMD 不算「傳統便宜」，但在 AI 成長邏輯下有合理性。
適合作為 NVIDIA 的 Beta 替代，邏輯是「押注 AI infra 第二名追趕」，而非撿便宜。

---

## Q：GPU 在 Agent 體系

Agent 的「反覆推論循環」讓硬體面臨特殊需求：

| 需求 | 原因 |
|:---|:---|
| 超低延遲（< 100ms/token） | Agent 快速輪轉，否則任務積壓 |
| 高記憶體頻寬 | 每次呼叫需載入完整模型權重 |
| 高吞吐量 | 並行 subagent 同時運行 |
| 長 context 處理 | Agent 任務 context 可達百萬 token |

- **GPU 優勢**：HBM 讓權重存取快，支援大批量並行，CUDA 生態最成熟
- **GPU 劣勢**：單次低延遲場景不理想，Groq LPU（SRAM-based）比 GPU 快 10x+

**結論**：NVIDIA GPU 是 Agent 時代最大受益者（量增），但低延遲架構（Groq/Cerebras）技術適配更優。

---

## Q：Claude Code 底層邏輯 — 會並行執行嗎？會的話誰受益？

**會，有兩層並行：**

**層 1：單 Agent 內部**
- Read-only 工具（搜尋、讀檔） → **並行執行**
- 寫入 / 修改狀態工具 → **序列執行**（避免衝突）

**層 2：Orchestrator-Subagent 多 Agent**
- Orchestrator 將任務拆解，派出多個 Subagent 並行運作
- 每個 Subagent 有**獨立的 context window**
- 透過共享 task.md / TODO.md 協調狀態

**誰受益？**

| 受益者 | 受益邏輯 | 程度 |
|:---|:---|:---|
| **Anthropic** | 並行 subagent = N倍 token 消耗，直接拉動 API 收入 | ⭐⭐⭐⭐⭐ |
| **NVIDIA** | 並行推論需要更多 GPU 算力，推論集群持續擴容 | ⭐⭐⭐⭐ |
| **AWS/GCP/Azure** | Anthropic Claude 部署在這些雲上，算力需求 = 雲端收入 | ⭐⭐⭐⭐ |
| **SK Hynix / Micron** | 更多 GPU = 更多 HBM 需求 | ⭐⭐⭐ |
| **Broadcom / Arista** | Agent cluster 需要更高速的內部網路 | ⭐⭐⭐ |
| **Groq / Cerebras** | Agent 低延遲需求讓其架構更具吸引力（但私有） | ⭐⭐⭐ |

**核心洞察**：
> 一個 Coding Agent 用戶在後端可能觸發 **5–20 個並行 subagent**，每個都是完整的 LLM inference call。
> 算力消耗等於 **5–20 個普通 LLM 用戶**。
> 這是 AI 推論需求爆炸式增長的核心驅動力之一。

---

## 投資框架整合

```
Agent 時代算力需求爆炸
         │
         ▼
最直接受益：NVIDIA (GPU 霸主)           ← 確定性最高
第二受益：AMD (第二大 GPU 廠)           ← 成長邏輯 OK，估值需注意
結構受益：AWS/GCP/Azure (雲算力)        ← 穩定但成長率較低
配套受益：SK Hynix / Micron (HBM)      ← 間接但確定性高
網路受益：Broadcom / Arista            ← Agent cluster 網路升級
爆發潛力：Groq / Cerebras (低延遲 AI)  ← 私有，目前無法直接投資
```

> ⚠️ 本文為研究性分析，不構成投資建議。