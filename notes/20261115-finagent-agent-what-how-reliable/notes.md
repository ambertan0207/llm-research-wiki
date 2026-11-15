---
title: "以 LLM Agent 為核心之股票技術面分析輔助系統是什麼？如何運作？可靠度有多高？"
created: 2026-11-15
updated: 2026-11-15
status: complete
wiki_pages:
  - "LLM金融技術分析"
  - "大型語言模型代理人"
  - "ReAct推理與行動"
  - "PAL程式輔助與外部執行"
  - "Agent反思與檢索式記憶"
  - "自適應提示詞與PromptEvolver"
  - "LLM-as-a-Judge評估"
  - "李旻珊2026-LLM-Agent股票技術分析"
---

# 研究問題

**以 LLM Agent 為核心之股票技術面分析輔助系統是什麼？如何運作？可靠度有多高？**

範圍依目前 Wiki 中的 FinAgent 論文為主：說明此類 Agent 的系統分工、資料與計算流程，以及該研究的小型概念驗證能支持到什麼程度。本文不把「指標計算答對」等同於「投資建議正確」或「交易獲利」。

## 簡答

FinAgent 是一個以 GPT-4o 為推理核心的金融技術分析輔助原型。它讓模型理解自然語言問題、決定需要哪些外部工具、整理計算結果並生成說明；行情資料和技術指標由工具取得或計算，具體數值再交由程式實際執行。論文在特定、很小的概念驗證中顯示：工具增強和實際執行對即時資料問答及數值正確性有明顯幫助。但目前證據不足以說它在真實市場中能持續提供正確判斷，更沒有證明可改善投資報酬。

## 這種系統是什麼

大型語言模型代理人（LLM Agent）是把 LLM 放進一個能按任務規劃步驟、呼叫工具、讀取結果並繼續處理的工作流程。它不只生成文字；資料工具、程式執行環境、記憶及結果檢查也共同構成系統能力。FinAgent 將 Agent 用在台股技術面分析問答，定位是協助使用者查詢與解讀資料，不是自動交易者，也不是投資決策的替代者。參見 [大型語言模型代理人](../../wiki/concepts/大型語言模型代理人.md) 與 [LLM 金融技術分析](../../wiki/topics/LLM金融技術分析.md)。

## 如何運作

1. **理解問題與規劃**：使用者提出股價、RSI、MACD、多指標交叉訊號或 K 線型態問題。GPT-4o 判斷回答需要哪些資訊。
2. **取得外部資料**：ReAct 迴圈使 Agent 按問題需要呼叫行情與指標工具；資料來源與工具順序可依任務不同而改變。此步補足模型內部知識無法提供即時行情的缺口。參見 [ReAct：推理與行動迴圈](../../wiki/concepts/ReAct推理與行動.md)。
3. **執行數值計算**：當問題需要指標或時序條件計算時，模型將問題轉成程式步驟，由 Node.js 後端實際執行，再把結果交回模型解讀。這是 PAL 式分工：LLM 負責語意理解／分解，執行環境負責確定性運算。參見 [PAL：程式輔助與外部執行](../../wiki/concepts/PAL程式輔助與外部執行.md)。
4. **修復與保存經驗**：Reflexion 可利用執行錯誤進行任務內診斷與重試；RAG 將修復經驗保存並在相似任務中檢索。PromptEvolver 則從回答評估中整理提示詞改進規則。這些是不同的記憶／改善用途，不能因系統包含它們就假設準確率已提升。參見 [Agent 反思與檢索式記憶](../../wiki/concepts/Agent反思與檢索式記憶.md) 與 [自適應提示詞與 PromptEvolver](../../wiki/concepts/自適應提示詞與PromptEvolver.md)。
5. **形成分析回答**：模型結合實際工具輸出，整理指標數值、訊號解釋與限制，回覆使用者。系統的文字解讀品質與計算正確性是兩個不同評估面向。

## 可靠度：目前測到了什麼

論文以 GPT-4o、Temperature 0 做四項概念驗證；結果應讀作「這幾組受控題目中的表現」，不應當作系統在所有情境的可靠度百分比。

| 測試 | 設定與樣本 | 論文報告 | 可支持的解讀 |
|---|---|---|---|
| 工具增強 | 原生 LLM 對上 Tool-Augmented Agent；各 6 題 | 原生模型 0/6 得分；工具組 6/6 滿分 | 在這些即時資料／技術指標題中，外部工具讓系統能完成原生模型無法完成的查詢。 |
| 程式碼提示策略 | Few-Shot AAB、BBA、CoT；各 10 次 MACD 程式碼生成 | 三組風格一致率與程式可執行率均 100% | 輸出形式可穩定，但一致／可執行不等於所有計算已在更廣泛任務中正確。 |
| Reflexion 與 RAG | 三個對照組；各 6 筆歷史多指標任務 | 三組 Pass@1 都是 6/6，沒有修復或失敗案例 | 因基線已全數通過，此設計無法測出 Reflexion 或 RAG 的額外效益；不是它們已被證明有效或無效。 |
| PAL 實際執行 | Native LLM、PAL No-Execution、PAL Full；各 6 題 | No-Execution 平均 0.17/3，5/6 失敗（其中 4 題方向錯誤）；PAL Full 6/6 滿分 | 這組結果支持：在所測問題中，讓程式真的執行比讓模型自行估算數字可靠。 |

以上數字與設計細節來自 [李旻珊的研究來源頁](../../wiki/sources/李旻珊2026-LLM-Agent股票技術分析.md)，原論文第三章印刷頁 22–40。評分基準部分由後端計算並與 TradingView 人工比對；評分者仍是 GPT-4o。另見 [LLM-as-a-Judge 評估](../../wiki/concepts/LLM-as-a-Judge評估.md)。

## 可靠度判斷與限制

### 較有支持的部分

在論文測試的題型與資料範圍內，外部工具能補足即時行情取得，實際執行能避免模型只靠內部估算數值。這些是針對特定系統配置與六題測試的概念驗證，不是普遍準確率保證。

### 仍未確立的部分

- **樣本有限**：幾項核心評估每組只有 6 或 10 次；目前無法穩健估計不同股票、日期、模型或罕見情況下的錯誤率。
- **評審獨立性不足**：GPT-4o 同時生成回答和擔任評審，可能出現共同模型偏誤；論文提出跨模型或金融專家評審作為後續方向。
- **記憶增益未被測出**：Reflexion/RAG 三組的首輪通過率都達 100%，天花板效應及任務覆蓋不足使本測試無法判斷增量效益。
- **投資績效未知**：研究未以回測或前瞻性市場資料驗證交易策略的報酬、風險或穩定性。
- **範圍狹窄**：原型主要處理技術面，未納入基本面、新聞情緒與總體經濟資訊；也沒有正式的使用者研究驗證有用性、易用性或信任校準。
- **計算正確不代表判斷正確**：正確行情與指標仍需配合資料品質、指標公式、情境理解和投資者自身風險判斷。本文提供的是輔助分析，不構成個人化買賣建議。

## 結論

**可靠度應拆成不同層次看。** 在這篇論文的小型受控測試中，工具呼叫和程式實際執行展現了明顯的技術價值；但 Agent 的分析解讀能否跨市場情境保持正確、長期記憶是否提升表現、系統是否帶來更好的交易結果，Wiki 目前沒有足夠證據回答。因此較準確的結論是：FinAgent 展示了可行的技術分析輔助架構及初步數值驗證，不等於已證明具有高投資可靠度。

## 建議後續閱讀（尚未納入 Wiki）

以下文獻是為補足 Agent 架構、工具執行與記憶機制的原始研究而搜尋的候選讀物。它們尚未納入本 Wiki，本文及簡報沒有使用其研究發現作為論據。

1. **Wang, L. et al. (2024). “A survey on large language model based autonomous agents.” *Frontiers of Computer Science*, 18, 186345.** [DOI: 10.1007/s11704-024-40231-1](https://doi.org/10.1007/s11704-024-40231-1). 建議理由：作為 Agent 元件與研究地圖的綜述型入門，幫助定位 FinAgent 的工具、規劃、記憶設計。
2. **Yao, S. et al. (2023). “ReAct: Synergizing Reasoning and Acting in Language Models.” ICLR 2023.** [OpenReview 論文頁](https://openreview.net/forum?id=WE_vluYUL-X). 建議理由：閱讀 ReAct 推理與行動交替機制的原始設計及其評估方式。
3. **Gao, L. et al. (2023). “PAL: Program-aided Language Models.” *Proceedings of the 40th International Conference on Machine Learning*, PMLR 202, 10764–10799.** [PMLR 論文頁](https://proceedings.mlr.press/v202/gao23f.html). 建議理由：追查語意分解與外部程式執行分工的原始方法。
4. **Shinn, N. et al. (2023). “Reflexion: Language Agents with Verbal Reinforcement Learning.” *Advances in Neural Information Processing Systems 36*.** [NeurIPS 論文頁](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html). 建議理由：了解文字反思與 episodic memory 的原始設計，以及論文所採用的任務評估。
5. **Lewis, P. et al. (2020). “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” *Advances in Neural Information Processing Systems 33*.** [NeurIPS 論文頁](https://proceedings.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). 建議理由：補讀檢索式外部記憶的基礎設計，對照 FinAgent 的長期記憶用法。

### 搜尋紀錄

- 搜尋日期：2026-11-15。
- 搜尋範圍：以 Wiki 來源頁引用的 Agent 綜述、ReAct、PAL、Reflexion、RAG 為線索；優先查會議論文集、期刊出版社與 OpenReview 等原始出版頁。
- 關鍵字：論文完整題名 + venue / publisher。
- 使用界線：搜尋所得資料只用於核對書目並列為閱讀候選；沒有把搜尋頁內容融入正文證據或簡報主張。
