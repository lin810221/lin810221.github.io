# API客戶端與共用業務流程

用同一契約檢查網站與程式客戶端。

## 建立另一種使用方式

先讀取API列表，再建立、修改與完成自己的任務。客戶端處理狀態、JSON欄位與分頁連結，不假設所有回應都有相同本文。若使用Session，需要取得並帶入合法cookie及CSRF資訊。

本課獨立算例以真實Django Client操作API，方便離線驗證；它不等於已建立瀏覽器跨來源整合。將來接前端框架或行動客戶端時，依實際認證方案另外設計。

## 共用服務的驗收

HTML與API的complete都進同一服務，應有一致的owner、交易與命令識別。用相同key重送，確認事件與revision不重複；不同用戶仍不能操作同一私人Task。

若API新增功能而HTML沒有，不代表需要複製整套Model邏輯。先定義服務行為，再分別處理輸入與回應；這讓日後增加背景工作或其他入口時仍有可追查的契約。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大API客戶端與共用業務流程圖解"><img src="assets/figures/26.svg" alt="API客戶端與共用業務流程：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「API客戶端與共用業務流程」讀圖：依端到端操作找出帳號、CRUD、附件與API共用的權限邊界。再回答：Django Client API測試成功，能否證明另一個網域的前端已完成CORS及Cookie整合？</p></div>

## 自我檢查與解析

**題目：**Django Client API測試成功，能否證明另一個網域的前端已完成CORS及Cookie整合？

<details><summary>展開解析</summary><p>不能。Client不等於真實跨來源瀏覽器，需在實際網域、HTTPS及認證條件下測試。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 18_rest_create.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:18_rest_create.py -->

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/api-guide/testing/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
