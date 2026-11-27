# 專題報告：查詢、快取與限制

只報你量測過的條件，不把算例當成負載結果。

## 建立可比較的實驗

固定資料、使用者、URL與設定，量測QuerySet評估及HTTP流程的查詢數。比較逐列owner、select_related與prefetch，說明關聯型別與載入內容。若測延遲，記錄暖機、樣本數及包含哪些階段。

快取實驗需同時核對命中、失效與跨帳號隔離。若數字快但資料過期或洩漏，不能視為優化成功。LocMem測試也不代表多worker共享快取。

## 結論附條件

例如可寫「在本課固定合成資料下，預載owner將這段查詢由逐列存取改為單次join」，而非「Django永遠快二十倍」。查詢數不是完整耗時，資料庫、網路與資料量都會改變結果。

將SQLite、真實HTTP、本機服務與待測PostgreSQL支線分開記錄。保存失敗與限制，未來才知道需要重測哪部分，而不是只留下最漂亮的數字。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大專題報告：查詢、快取與限制圖解"><img src="assets/figures/26.svg" alt="專題報告：查詢、快取與限制：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「專題報告：查詢、快取與限制」讀圖：依端到端操作找出帳號、CRUD、附件與API共用的權限邊界。再回答：查詢從二十一次變一次，就能宣稱網站快二十一倍嗎？</p></div>

## 自我檢查與解析

**題目：**查詢從二十一次變一次，就能宣稱網站快二十一倍嗎？

<details><summary>展開解析</summary><p>不能。單次查詢成本、資料量、網路、呈現與其他工作仍不同，需實際量測延遲或吞吐。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 08_n_plus_one.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:08_n_plus_one.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/optimization/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
