# Wiki 維護日誌

此檔案為追加式時間紀錄。每筆以 `## [YYYY-MM-DD] 類型 | 標題` 開始。類型使用 `ingest`、`query`、`lint`、`setup` 或 `output`。

## [2026-11-15] setup | 建立 LLM 研究 Wiki

- 建立繁體中文維護規範、原始來源區、Wiki 分類、索引與日誌。
- 尚無研究來源；索引中的待建立標記會在首次 ingest 時更新。

## [2026-11-15] ingest | 以 LLM Agent 為核心之股票技術面分析輔助系統

- 將原始 74 頁 PDF 保存至 `raw/以LLM-Agent為核心之股票技術面分析輔助系統.pdf`。
- 建立來源頁：`wiki/sources/李旻珊2026-LLM-Agent股票技術分析.md`。
- 建立／更新相關概念與主題頁：大型語言模型代理人、ReAct、PAL 與外部執行、Agent 反思與檢索式記憶、CoT/Few-Shot、LLM-as-a-Judge、LLM 金融技術分析。
- 更新 `index.md`。主要證據：工具組與 PAL Full 各 6/6 滿分；PAL No-Execution 5/6 失敗；Reflexion/RAG 三組均 6/6 首輪通過，因此未測出增量效果。已在來源頁標註小樣本、同模型評審與未測交易績效等限制。
- 補建自適應提示詞與 PromptEvolver 概念頁，並補入索引和來源頁連結。
- 將使用者偏好寫入 `AGENTS.md`：之後提供並要求整理的原始文章先保存到 `raw/`，再進行整理；同名來源不得逕自覆蓋。


## [2026-11-15] setup | 建立研究產出流程

- 在 `AGENTS.md` 加入以 Wiki 為唯一證據來源的 notes 流程、網路搜尋候選文獻隔離規則、逐頁稿與 HTML 同步規範及版本狀態要求。
- 建立 `notes/`、`slides/`、`html/` 產出資料夾、說明與空白模板。HTML 簡報的視覺風格與互動細節待和使用者討論後採用。

## [2026-11-15] setup | 約定 HTML 簡報視覺方向

- 設定預設風格為「奶油手帳＋薰衣草剪貼簿」，並記錄低飽和配色與裝飾原則於 `AGENTS.md`、`html/README.md`。
- 頁面版型、導覽、鍵盤操作與列印／匯出細節仍待首次製作前討論。

## [2026-11-15] setup | 建立簡報風格試樣

- 建立 `html/style-preview/index.html`，以封面、系統概念與研究結果三頁展示候選風格；內容依 Wiki 的 FinAgent 來源頁整理。
- 另存靜態總覽 `html/style-preview/preview.png` 及向量原稿 `preview.svg`，方便快速預覽。
- 修正前一筆風格紀錄：奶油手帳＋薰衣草剪貼簿目前僅為候選方向；使用者看過試樣並明確確認前，不視為最終風格。

## [2026-11-15] output | FinAgent 是什麼、如何運作、可靠度有多高

- Notes：`notes/20261115-finagent-agent-what-how-reliable/notes.md`；正文只用 Wiki 證據，末尾另列網路搜尋的候選文獻及查詢紀錄。
- 逐頁簡報：`slides/20261115-finagent-agent-what-how-reliable/slides.md`；依上述 Notes 編排 9 頁。
- HTML 簡報：`html/20261115-finagent-agent-what-how-reliable/index.html`；依逐頁稿製作，採已確認風格，離線可用，含方向鍵／按鈕導覽與列印樣式。
- 主要依據：FinAgent 來源頁及 LLM Agent、ReAct、PAL、反思／記憶、LLM-as-a-Judge 概念頁；三份產物同步完成。外部候選文獻尚未納入 Wiki。

## [2026-11-15] ingest | 新增三篇 LLM 新聞與台股預測論文

- 將三份使用者提供的 PDF 原樣保存至 `raw/`，未修改原始檔。
- 新增來源頁：張耿瑜（2025）、吳奉恩（2026）、孫佳鴻（2026），整理研究問題、方法、結果及限制。
- 更新 `wiki/topics/LLM金融技術分析.md`，納入四篇來源脈絡；新增 `wiki/syntheses/LLM新聞技術指標股價預測-四篇來源比較.md`，對照 Agent 工具協調、新聞情緒、特徵融合及評估限制。
- 更新 `index.md`。比較時保留不可直接比較的邊界；標記張耿瑜論文題名與迴歸目標不一致、吳奉恩論文摘要與方法章股票數不一致，以及孫佳鴻研究所承接之何銘哲（2025）論文尚未納入 Wiki。
- 吳奉恩來源頁及跨來源比較標記 `needs-review`，待查股票數差異與兩篇 MTI-LLM 研究的版本／承接關係；未將個別論文的主張寫成領域共識。

## [2026-11-15] update | FinAgent 簡報加入小人物貼圖

- 生成一張 3×2 透明 PNG 小人物貼圖組，保存在 `html/20261115-finagent-agent-what-how-reliable/assets/characters.png`。
- 更新同專案 `index.html`，以 CSS 精靈圖方式在封面、系統流程、ReAct、記憶、可靠度及後續閱讀頁放入六個裝飾貼圖；簡報文字與逐頁稿未改。
- 靜態檢查確認 9 頁、6 個貼圖引用與素材檔案存在。內建瀏覽器的本機檔案 URL 政策阻止重新預覽，未能完成畫面目視檢查。

## [2026-11-15] setup | 建立可瀏覽的 Wiki 網站

- 新增 `tools/build_wiki_site.py`，使用 Python 標準函式庫將 `wiki/` Markdown 生成為根目錄 `index.html` 與 13 個 `wiki-pages/` 頁面，另產生 `wiki-assets/site.css`。
- 網站首頁含專案介紹、知識分類、搜尋框與頁數統計；各知識頁保留 Markdown 格式轉譯、Obsidian 連結、來源 PDF 連結與返回導覽。搜尋在瀏覽器端執行，不依賴外部服務。
- 更新 `AGENTS.md`，記錄網站生成層的維護方式與 `python tools/build_wiki_site.py` 建置流程；Wiki Markdown 與 `index.md` 仍為唯一內容來源。
- 靜態檢查 14 個 HTML 頁面及所有本機連結路徑均存在。內建瀏覽器無法連接本機預覽伺服器，故未完成畫面目視檢查；網站留待下一步本機瀏覽確認後再上傳 GitHub Pages。

## [2026-11-15] setup | 整理 GitHub 專案說明

- 新增 `README.md`，說明 Wiki 的目的、資料架構、AI 如何依 `AGENTS.md` 延續維護，以及網站重建方式。
- README 連結本機網站、Wiki 索引、維護規則及跨來源比較，並標記 GitHub／Pages 連結待部署後補上。
