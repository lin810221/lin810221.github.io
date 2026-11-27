# 網站、後端與Django的角色

先知道瀏覽器在哪裡、Python在哪裡，才不會把部署方式混在一起。

## 一次網頁存取發生什麼事

瀏覽器把網址、方法、標頭與可能的表單資料送給伺服器。伺服器決定誰可以看什麼、讀寫資料，再回傳HTML、JSON或檔案。HTML不是Python程式；使用者也不應直接取得資料庫連線與伺服器密鑰。

Django提供路由、資料模型、模板、表單、登入、管理後台及測試工具，適合有帳號與資料管理的網站。本課以StudyHub學習任務網站串起這些功能，讓每個新概念都能接回同一個專案。

## 課程網站與實作網站不同

目前閱讀的教材是靜態HTML與JavaScript，可以離線開啟，也能放在GitHub Pages。下載包中的Django專案則需要Python程序與資料庫；GitHub Pages不能執行Django後端。把 `manage.py` 上傳到repo，不會自動得到可登入的伺服器。

先完成本機網站，再學正式WSGI服務、HTTPS與資料保存。前端框架、雲端服務或容器都是可選組件，初學不必先同時安裝；核心主線只需Python、相依套件與內建SQLite。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大網站、後端與Django的角色圖解"><img src="assets/figures/01.svg" alt="網站、後端與Django的角色：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「網站、後端與Django的角色」讀圖：追蹤瀏覽器與伺服器的請求及回應，指出靜態教材與Django程式各在哪裡執行。再回答：為什麼教材能放GitHub Pages，但StudyHub登入與儲存不能直接靠它執行？</p></div>

## 自我檢查與解析

**題目：**為什麼教材能放GitHub Pages，但StudyHub登入與儲存不能直接靠它執行？

<details><summary>展開解析</summary><p>教材只需傳送靜態檔；Django登入與資料寫入需要持續運行的Python後端及資料庫，屬於不同部署能力。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
