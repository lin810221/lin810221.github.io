# 外鍵、多對多與刪除行為

資料關係決定查詢、權限與刪除的後果。

## 用實際資料畫關係

一個User有多個Task，一個Task屬於一個owner；Task與Tag則是多對多，由中介表保存連結。Attachment指向Task，CompletionEvent保存一次命令的識別與版本。不要把多個tag名稱串成同一字串，再期待資料庫能可靠查詢。

ForeignKey的 `on_delete` 決定被參照物件刪除時的行為，例如CASCADE連帶刪除。它不是一般的使用者授權：能否發起刪除，仍要由應用層先判斷。

## 關係也有擁有者規則

資料庫知道某個tag存在，卻不會自動知道它是否屬於同一個使用者。表單與API要限制可選tag範圍，避免Alice把Bob的私人標籤接到自己的任務。Model、資料庫與請求驗證各負責不同條件。

用合成資料新增關聯、反向查詢與移除連結，再觀察刪除Task後哪些資料跟著消失。檔案儲存不是資料庫列本身，清理時還要處理提交後的檔案生命週期。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大外鍵、多對多與刪除行為圖解"><img src="assets/figures/07.svg" alt="外鍵、多對多與刪除行為：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「外鍵、多對多與刪除行為」讀圖：數清楚一對多與多對多的方向，指出外鍵與中介表的角色。再回答：外鍵能找到tag，是否代表目前使用者可以使用它？</p></div>

## 自我檢查與解析

**題目：**外鍵能找到tag，是否代表目前使用者可以使用它？

<details><summary>展開解析</summary><p>不代表。存在性與授權不同；需限制tag的owner範圍並驗證跨帳號輸入。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 05_relations.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:05_relations.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/models/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
