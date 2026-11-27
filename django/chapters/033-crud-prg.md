# CRUD與POST Redirect GET

把修改成功與重新整理的行為設計清楚。

## 四種資料操作

建立、讀取、更新與刪除共用資料模型，但請求、驗證與回應不同。GET顯示表單，POST驗證並儲存，成功後redirect到GET頁；無效POST則回原表單含錯誤。不能為了跳轉而丟掉錯誤資訊。

PRG讓成功後的重新整理重讀頁面，而不是直接重送原POST。它能改善一般瀏覽器流程，卻不是所有重複請求的去重機制；網路重試或連點仍可能發生，重要命令另需冪等設計。

## 標籤管理也是CRUD

導覽列的「管理標籤」可新增、改名與刪除自己的標籤，再回任務表單選取。TagForm限制owner範圍與同名檢查，資料庫唯一條件處理競爭；刪除tag只移除連結，不刪任務。以第二個帳號測修改與刪除，避免標籤管理變成另一條越權入口。

## 刪除要有明確動作

刪除確認頁的GET只顯示後果，POST才刪除。先以owner範圍取得物件，再接受確認。即使按鈕在畫面上隱藏，也不能省掉伺服器授權與CSRF檢查。

用本課建立入口觀察302及Location，再跟到詳情頁。回傳訊息只說明這次操作結果，不應把全部內部例外直接顯示給使用者。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大CRUD與POST Redirect GET圖解"><img src="assets/figures/11.svg" alt="CRUD與POST Redirect GET：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CRUD與POST Redirect GET」讀圖：追蹤輸入到cleaned_data，指出資料擁有權與欄位白名單在哪裡確認。再回答：使用PRG後，是否就不用處理重複付款或重複命令？</p></div>

## 自我檢查與解析

**題目：**使用PRG後，是否就不用處理重複付款或重複命令？

<details><summary>展開解析</summary><p>仍需要。PRG改善重新整理流程，不保證網路層或使用者重送時只執行一次。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 12_create_prg.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:12_create_prg.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/forms/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
