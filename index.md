# LLM 研究 Wiki 索引

> 研究範圍：大型語言模型及其相關方法、評估、資料與應用。所有研究主張應追溯至來源頁；單篇證據不視為領域共識。

## 研究主題

- [LLM 金融技術分析](wiki/topics/LLM金融技術分析.md) — Agent 技術分析、新聞情緒與多特徵股價預測的研究脈絡。

## 概念

- [大型語言模型代理人](wiki/concepts/大型語言模型代理人.md) — 工具、規劃、執行與記憶如何組成 Agent。
- [ReAct：推理與行動迴圈](wiki/concepts/ReAct推理與行動.md) — 依觀察結果動態選用外部工具。
- [PAL：程式輔助語言模型與外部執行](wiki/concepts/PAL程式輔助與外部執行.md) — 將語意推理與確定性計算分工。
- [Agent 反思與檢索式記憶](wiki/concepts/Agent反思與檢索式記憶.md) — 任務內修復與跨任務記憶的分工及證據限制。
- [CoT 與 Few-Shot 提示策略](wiki/concepts/CoT與FewShot提示策略.md) — 提示策略與示範配置的關係。
- [LLM-as-a-Judge 評估](wiki/concepts/LLM-as-a-Judge評估.md) — LLM 評審的設計、偏誤與交叉驗證。
- [自適應提示詞與 PromptEvolver](wiki/concepts/自適應提示詞與PromptEvolver.md) — 依回答品質回饋保存並檢索提示改進規則。

## 綜述與比較

- [LLM 新聞與技術指標股價預測：四篇來源比較](wiki/syntheses/LLM新聞技術指標股價預測-四篇來源比較.md) — 比較 Agent、LLM 新聞情緒與多特徵融合設計，整理研究限制及待查差異。

## 來源

- [李旻珊（2026），以 LLM Agent 為核心之股票技術面分析輔助系統](wiki/sources/李旻珊2026-LLM-Agent股票技術分析.md) — 國立中興大學碩士論文；介紹 FinAgent 及四項概念驗證。
- [張耿瑜（2025），結合 LLM 新聞標題情緒分析與股價方向預測之研究](wiki/sources/張耿瑜2025-LLM新聞情緒與台積電預測.md) — 本地 Gemma／DeepSeek 新聞情緒與台積電隔日收盤價迴歸；題名與實際目標需區分。
- [吳奉恩（2026），結合 LLM 驅動之新聞處理與多元技術指標於股票趨勢預測](wiki/sources/吳奉恩2026-MTI-LLM多技術指標與新聞處理.md) — Qwen 新聞處理、技術特徵與 XGBoost／TFT；標的數量待核。
- [孫佳鴻（2026），融合大語言模型新聞篩選、財經情感分析與技術指標之台灣股價預測研究](wiki/sources/孫佳鴻2026-LLM新聞篩選與台股預測.md) — 五檔台股、16 種特徵組合及五種子比較；承認前視偏誤風險。

## 待研究問題

- [LLM 金融技術分析](wiki/topics/LLM金融技術分析.md#待追問題) — 資料新鮮度、跨模型評估、使用者信任及回測偏誤。


