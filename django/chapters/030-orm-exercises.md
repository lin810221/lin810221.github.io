# ORM練習：先手算，再看SQL

用小資料驗證結果，用較多資料觀察成本。

## 建立能算清楚的資料

準備兩個使用者、不同狀態任務及共享名稱但不同owner的tag。手算各人的任務數、完成數與查詢結果，再對照ORM。讓錯誤的跨帳號篩選會被清楚看見，而不是剛好測試資料都屬於同一人。

逐步增加列表筆數，比較未預載、select_related與prefetch的查詢。對新fetch mode另做延後欄位存取測試，確認被阻擋的是額外取值，而不是原本已載入的資料。

## 留下可追查的證據

報告包含資料集、SQL結構、查詢次數、結果分母與資料庫版本。以交易回滾和違反約束的反例驗證一致性，將SQLite已測與PostgreSQL待驗證的部分分開。

本章不是鼓勵手寫所有SQL，而是讓ORM不再成為黑箱。當結果不對或網站變慢，你能定位是查詢條件、關聯展開、資料量還是交易邊界，而不是先加更多快取。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大ORM練習：先手算，再看SQL圖解"><img src="assets/figures/10.svg" alt="ORM練習：先手算，再看SQL：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「ORM練習：先手算，再看SQL」讀圖：沿交易邊界讀提交與回滾，指出跨資料庫不能直接推論的部分。再回答：所有查詢結果正確，就代表效能也合格嗎？</p></div>

## 自我檢查與解析

**題目：**所有查詢結果正確，就代表效能也合格嗎？

<details><summary>展開解析</summary><p>不代表。還需檢查查詢數、資料量、索引與目標負載；正確性與效能各自驗證。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 24_fetch_mode.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:24_fetch_mode.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/optimization/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
