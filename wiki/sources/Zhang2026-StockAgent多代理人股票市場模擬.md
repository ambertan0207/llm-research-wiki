---
title: "StockAgent：LLM 多代理人股票市場模擬"
type: source
created: 2026-11-15
updated: 2026-11-15
tags: [LLM-Agent, 金融, 多代理人, 市場模擬]
sources: []
status: needs-review
---

# When AI Meets Finance (StockAgent)

## 書目與版本

Chong Zhang et al. *When AI Meets Finance (StockAgent): Large Language Model-based Stock Trading in Simulated Real-world Environments*. arXiv:2407.18957v5（2026-06-23）。[arXiv 版本頁](https://arxiv.org/abs/2407.18957)，[DOI](https://doi.org/10.48550/arXiv.2407.18957)，[arXiv PDF](https://arxiv.org/pdf/2407.18957)，本機原件另存於 raw/When-AI-Meets-Finance-StockAgent.pdf，共 33 頁。

**版本待核：** arXiv 摘要頁記錄論文刊於 ACM TIST；下載的 v5 PDF 封面仍標「Preprint, under review」並有佔位 DOI。此頁以可追溯的 arXiv v5 為閱讀版本，不猜測正式書目。

## 研究問題與定位

StockAgent 是以 LLM 驅動的多代理人股票市場模擬框架，用來觀察不同模型與外部條件下的代理人交易行為。它研究模擬市場中的交易及群體行為，不等同於真實市場股價預測，也不是已驗證的投資獲利系統。

## 系統設計

論文包含三個主要模組（PDF 頁 5–8）：

1. **投資代理人**：設定保守、積極、平衡、成長導向等人格，決定借貸、買賣、持有、預測隔日行動並分享想法。
2. **交易撮合模組**：代理人提交買賣訂單，由 order book 撮合並更新成交和價格；格式檢查機制修正不合規輸出。
3. **BBS 討論模組**：代理人匿名分享交易提示，供其他代理人後續讀取。

模擬可設定財報、利率、貸款與外部事件。實驗使用 GPT-3.5-Turbo 與 Gemini-Pro、匿名股票 A/B 及事件驅動環境，屬該論文版本設定。

## 實驗與作者報告

- **模型差異（PDF 頁 14–16）**：在 10 個交易日設定中，成交量、交易頻率、價格路徑與群體行為不同；表 10–11 報告 GPT 組交易量較大、交易次數較少。這是特定模型與模擬條件下的觀察。
- **條件消融（PDF 頁 16–20）**：移除 BBS、利率、財報、貸款等條件會改變部分模擬情境的交易行為和盈虧分布，不能推論為真實市場的普遍因果效果。

## 限制與待核

- 模擬使用人工設定市場及匿名股票，不能直接當作真實市場報酬、風險或可投資性證據。
- 使用早期 GPT-3.5-Turbo、Gemini-Pro，不能外推至其他或目前模型版本。
- PDF 表 9 對 RQ3 標為 154 個交易日；第 16 頁則稱 Gemini-Pro 在不同條件下做 30 rounds over 10 days。期間描述不一致，需回查圖表／附錄或正式版本。
- arXiv 摘要頁稱已刊於 ACM TIST，PDF v5 仍標 under review 並有佔位出版資訊。正式書目及 DOI 待核。
- 作者指出股票推薦與交易策略可靠度仍需進一步研究（PDF 頁 20–21）。

## Wiki 關聯

[[大型語言模型代理人]] · [[LLM金融技術分析]] · [[LLM新聞技術指標股價預測-四篇來源比較]]。此研究補充 FinAgent 問答輔助以外的多代理人市場模擬；各自任務不同，不宜直接排名。

## 參考資料

Zhang, C. et al. (2024–2026). *When AI Meets Finance (StockAgent): Large Language Model-based Stock Trading in Simulated Real-world Environments*. arXiv:2407.18957v5. https://doi.org/10.48550/arXiv.2407.18957
