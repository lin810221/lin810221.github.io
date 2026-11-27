# 啟動第一個完整網站

從資料表、帳號與種子資料走到可以操作的頁面。

## 使用完整下載包

在 `examples` 目錄啟動隔離環境後執行：

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo --username 你剛建立的帳號
python manage.py runserver 127.0.0.1:8000
```

開啟終端印出的本地網址，使用剛建立的帳號登入。密碼由你在終端設定，教材沒有通用預設帳號。也可以從網站註冊一般帳號，再建立自己的任務。

## 確認資料與程序的範圍

本地SQLite資料存於 `db.sqlite3`，停止伺服器不會自動刪除；獨立算例則每個程序建立記憶體資料庫。`seed_demo` 只替既有帳號加入合成任務，重跑不重複建立固定範例，也不重設密碼。

`runserver` 是開發工具，會提供除錯與自動重新載入。它不是正式部署方案；請先在自己的電腦練習，不因網頁能開就宣稱已經完成HTTPS、備份與正式權限設計。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大啟動第一個完整網站圖解"><img src="assets/figures/02.svg" alt="啟動第一個完整網站：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「啟動第一個完整網站」讀圖：區分project、app與設定，沿管理命令走到第一個頁面。再回答：重開01獨立算例後資料不見，但runserver資料還在，為什麼？</p></div>

## 自我檢查與解析

**題目：**重開01獨立算例後資料不見，但runserver資料還在，為什麼？

<details><summary>展開解析</summary><p>獨立算例使用程序內記憶體SQLite；完整網站預設使用檔案SQLite。資料保存位置與程序生命週期不同。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/install/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
