# LLM 研究 Wiki

一個以大型語言模型（LLM）研究為主題的個人知識庫。專案把原始論文保存為唯讀來源，再由 AI 整理成互相連結、可追溯依據的繁體中文 Wiki，讓新增文獻、研究問題與分析成果能逐步累積，而非每次都從原始檔重新整理。

## 專案目的

本 Wiki 目前從 LLM Agent 與股票分析研究出發，整理系統架構、新聞情緒分析、技術指標、評估方法與研究限制。資料庫已收錄五篇相關論文，並建立來源頁、概念頁、主題頁與跨來源比較。

此專案用於研究整理與知識管理，不提供個人化投資建議；論文中的模型結果也不等於已證明可穩定獲利。

## 瀏覽網站

- 本機或 GitHub Pages 網站入口：[index.html](./index.html)
- Wiki Markdown 索引：[index.md](./index.md)
- AI 維護規則：[AGENTS.md](./AGENTS.md)

網站提供主題、概念、來源及綜述頁面，支援站內搜尋、頁面互連與原始 PDF 連結。網站使用純 HTML、CSS 和瀏覽器端 JavaScript，不需外部服務或套件。

## AI 如何依規則延續維護

`AGENTS.md` 是本專案的維護規格，告訴 AI：

1. 原始文獻放在 `raw/`，保存原檔且不覆寫；Wiki 知識放在 `wiki/`。
2. 新增來源時建立來源頁，整理研究問題、方法、結果、限制與引用，並更新相關概念、主題、綜述、索引與日誌。
3. 區分來源直接報告、作者解釋、跨來源推論與尚待驗證事項；結果不可超出原文證據。
4. 回答研究問題時先查 Wiki 並附可追溯的來源；若整理出可重用的研究分析，再歸檔到適當頁面。
5. Notes、逐頁簡報與 HTML 簡報各有獨立規則，避免把尚未納入 Wiki 的外部資料混成已確認知識。
6. Wiki 內容更新後，以建置工具重生網站呈現層，避免網站與 Markdown 知識脫節。

這些規則使 AI 能接續既有頁面和命名方式，知道哪些檔案可編輯、哪些原始檔必須保留，以及如何維持引用與索引，而不必每次重新猜測專案做法。

## 專案結構

```text
.
├── AGENTS.md             # AI 維護規格與工作流程
├── index.md              # Wiki 知識索引
├── index.html            # 可瀏覽網站首頁
├── raw/                  # 原始論文與來源檔案（唯讀）
├── wiki/
│   ├── sources/           # 單篇文獻整理
│   ├── concepts/          # 概念與方法
│   ├── topics/            # 研究主題
│   ├── syntheses/         # 跨來源綜述與比較
│   ├── entities/          # 研究者、機構、系統等
│   └── questions/         # 待研究問題
├── wiki-pages/            # 由 Markdown 產生的網站內容頁
├── wiki-assets/           # 由建置工具產生的網站樣式
├── tools/
│   └── build_wiki_site.py # 以標準 Python 套件重建網站
├── notes/                 # 研究問題的 Wiki 證據型筆記
├── slides/                # 簡報逐頁稿
├── html/                  # 可離線瀏覽的 HTML 簡報與素材
└── log.md                 # 來源匯入與維護紀錄
```

## 更新網站

新增或修改 `wiki/` 頁面或 `index.md` 後，於專案根目錄執行：

```powershell
python tools/build_wiki_site.py
```

之後開啟根目錄的 `index.html` 即可瀏覽。網站建置不需安裝額外 Python 套件；發布至 GitHub Pages 時，使用儲存庫根目錄的 `index.html` 作為網站入口。

## 目前研究頁面

- [LLM 金融技術分析主題](./wiki/topics/LLM金融技術分析.md)
- [四篇來源比較](./wiki/syntheses/LLM新聞技術指標股價預測-四篇來源比較.md)
- [全部 Wiki 頁面索引](./index.md)

## GitHub 與網站部署

GitHub 儲存庫：[ambertan0207/llm-research-wiki](https://github.com/ambertan0207/llm-research-wiki)；公開網站：[LLM 研究 Wiki](https://ambertan0207.github.io/llm-research-wiki/)。

## 教學 HTML 簡報作業

- [作業提交說明](./作業提交說明.md)
- [教學簡報：股票研究裡的 LLM Agent](./html/20261115-llm-agent-stock-market-tutorial/index.html)
- [執行與反思紀錄](./notes/20261115-llm-agent-stock-market-tutorial/execution-reflection.md)
