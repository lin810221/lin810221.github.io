# 術語與三條學習路線

依起點安排閱讀，仍保留完整網站主線。

## 第一次學後端

從HTTP、Python環境與project開始，依序學路由、模板、Model、表單與登入。先親手完成一筆資料的建立與讀取，再追查每個檔案負責什麼；不要一開始就同時選所有外部服務。

## 已懂Python，要做網站

可先跑StudyHub與測試，再回讀ORM、權限、附件與API，逐步替換成自己的需求。框架熟悉度不代表可以跳過跨帳號與CSRF驗證，這些是資料網站的核心契約。

## 已有Django經驗

深入6.1 fetch modes、內建Tasks、CSP、查詢測試、交易與部署界線。升級前查基準與實際API，保留舊功能測試。下載學習包附術語定義與原創圖解，可離線複習。

跨課閱讀：[應用統計](../applied-statistics/index.html)補報表判讀，[LLM服務與AI Agents](../llm/index.html)可作日後AI功能整合，[MCP](../mcp/index.html)補工具協定。[SQL與資料工程](../sql/index.html)深入查詢、交易與資料交付；FastAPI維持獨立課程規劃。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大術語與三條學習路線圖解"><img src="assets/figures/28.svg" alt="術語與三條學習路線：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「術語與三條學習路線」讀圖：沿版本、測試與回復流程，指出交接前最後需要確認的內容。再回答：已有API經驗，哪部分仍值得優先補？</p></div>

## 自我檢查與解析

**題目：**已有API經驗，哪部分仍值得優先補？

<details><summary>展開解析</summary><p>Model與migration、表單及模板、Session、物件授權、Admin與私人檔案，這些是完整網站的重要主線。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
