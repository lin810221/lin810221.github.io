# 請求生命週期與MVT

沿著URL、View、Model與Template追蹤資料。

## 一條可以追蹤的路徑

請求先經過middleware，URL resolver依順序比對路由，選到View。View讀取已驗證的輸入與使用者身分，透過ORM查詢Model，將結果交給Template或回傳JSON。回應再經middleware送回瀏覽器。

MVT中的Model負責資料表示，Template負責呈現，View協調請求。這是責任分工，不是強迫所有商業邏輯塞進View。跨多個入口共用的操作，可抽到明確的服務函式。

## 用健康端點看最短路徑

下載包的 `/health/` 回傳簡單JSON，不查私人資料。它適合確認程序與路由能回應，但不能證明資料庫、登入與全部功能都正常。後續另用需要登入的任務列表測完整流程。

在測試中觀察狀態碼、內容型別與request ID，再逐步加入資料查詢。遇到404先確認路由與參數，遇到500查伺服器例外；不要在看不見錯誤來源時一口氣重寫所有層。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大請求生命週期與MVT圖解"><img src="assets/figures/02.svg" alt="請求生命週期與MVT：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「請求生命週期與MVT」讀圖：區分project、app與設定，沿管理命令走到第一個頁面。再回答：health回傳200，是否代表整個網站都可用？</p></div>

## 自我檢查與解析

**題目：**health回傳200，是否代表整個網站都可用？

<details><summary>展開解析</summary><p>只能證明該路徑當時能回應；資料庫、登入、權限及其他依賴要有各自的檢查。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 03_request_response.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:03_request_response.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/ref/request-response/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
