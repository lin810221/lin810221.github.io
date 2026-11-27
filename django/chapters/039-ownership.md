# 物件授權與資料擁有者

每個列表、詳情、修改、下載與API都要有範圍。

## 先限制查詢，再取得物件

StudyHub以 `Task.objects.for_user(request.user)` 作為一般使用者入口。詳情、更新與刪除的get_queryset沿用範圍；附件下載則透過task的owner限制。改URL中的pk不應取得其他人的內容。

列表也要限制範圍，不能只做detail的object permission。建立時owner由伺服器填入，tag選項也限制owner，避免輸入關聯ID造成另一種越權。

## 四種入口分別驗證

同一Task可以經由HTML、API、Admin與背景工作存取。這些入口各有自己的身分與授權條件，一個安全不代表其他都安全。後台superuser可跨帳號管理是明確設計，一般staff則仍需模型權限與資料範圍。

測試至少準備Alice與Bob，各有資料，互換ID嘗試讀取、更新、刪除與下載。只用一個帳號測happy path，不足以證明物件授權存在。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大物件授權與資料擁有者圖解"><img src="assets/figures/13.svg" alt="物件授權與資料擁有者：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「物件授權與資料擁有者」讀圖：區分身分驗證與物件授權，找出每次查詢的擁有者條件。再回答：detail有owner檢查，API列表是否就自然只顯示自己的任務？</p></div>

## 自我檢查與解析

**題目：**detail有owner檢查，API列表是否就自然只顯示自己的任務？

<details><summary>展開解析</summary><p>不會自然繼承。API列表需要限制get_queryset，建立及關聯欄位也要各自驗證。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 14_ownership.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:14_ownership.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/auth/default/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
