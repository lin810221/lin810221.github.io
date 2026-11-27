# 資料模型練習：變更之前先問資料

用關係、約束與migration一起描述需求。

## 增加一個功能

假設任務需要「預計完成日期」與「標籤」。先定義未填的意義、日期是否可為過去、標籤是否跨帳號共用，以及刪除任務時附件怎麼處理。這些問題決定欄位、關聯與驗證，不應等畫面完成後才補猜測。

畫出資料關係，再產生migration並閱讀SQL。用空資料庫重建一次，確認所有必要表與約束都在版本紀錄中，而不是依賴開發者曾手動改過資料庫。

## 在舊資料上思考變更

為有一千筆既有任務的情境設計新增必填欄位流程，說明先填值、預設、資料搬移與驗收。這是一個設計練習，不宣稱已在真實大表測量鎖定或部署時間。

交付物包含Model、關係圖、約束、migration與資料變更說明。後續ORM與API才能建立在可重現的資料契約上，而不是只有一份看起來完整的models.py。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大資料模型練習：變更之前先問資料圖解"><img src="assets/figures/08.svg" alt="資料模型練習：變更之前先問資料：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「資料模型練習：變更之前先問資料」讀圖：沿schema變更與資料搬移的順序，說明哪些舊資料必須先處理。再回答：本機資料庫有欄位，migration卻沒有，能直接交付嗎？</p></div>

## 自我檢查與解析

**題目：**本機資料庫有欄位，migration卻沒有，能直接交付嗎？

<details><summary>展開解析</summary><p>不能。乾淨環境無法重建相同schema；需找出手動變更並補成可審查、可重現的migration。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/migrations/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
