# 帳號與授權驗收矩陣

用第二個帳號主動找出漏掉的入口。

## 建立跨帳號測試

列出任務列表、詳情、編輯、刪除、標記完成、附件、匯出與API。以匿名、Alice、Bob及具有不同管理權限者操作，記錄每項預期狀態與資料庫變化。不能只證明按鈕沒有顯示。

對每個會寫入的入口，另外測錯誤方法、缺CSRF、非法關聯ID與偽造owner。測試拒絕後確認資料沒有變；只檢查回應狀態，有時會漏掉已經發生的副作用。

## 確認框架能力的邊界

內建登入提供身分，但不理解你的資料擁有權。CSP限制資源來源，但不保證內容可信。Admin方便管理，但仍須按職責配置模型權限與資料範圍。請為每項防護寫一句它能處理與不能代替的責任。

本章完成後，應能將「已登入所以可看」改寫成具體的授權條件與測試。後續檔案與REST API沿用同樣原則，而不是新增入口後重新打開安全缺口。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大帳號與授權驗收矩陣圖解"><img src="assets/figures/14.svg" alt="帳號與授權驗收矩陣：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「帳號與授權驗收矩陣」讀圖：追蹤cookie、CSRF token及來源，說明哪些防護不能互相取代。再回答：越權測試回404，但資料真的被更新了，算通過嗎？</p></div>

## 自我檢查與解析

**題目：**越權測試回404，但資料真的被更新了，算通過嗎？

<details><summary>展開解析</summary><p>不通過。拒絕回應與沒有未授權副作用都要驗證，必要時檢查交易與例外處理順序。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 16_csrf_valid.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:16_csrf_valid.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/security/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
