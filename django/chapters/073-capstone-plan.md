# StudyHub專題：先定義交付範圍

將所有章節組成一個可以交接的完整網站。

## 任務與資料契約

使用者能建立帳號、登入、管理自己的任務與標籤、保存私人文字附件，並透過API操作相同資料。staff依模型權限與owner管理，superuser保留明確的跨帳號管理能力。這些條件構成測試與交付標準。

核心資料包括User、Task、Tag、Attachment與CompletionEvent。先畫關係及授權範圍，再做頁面、表單與API；不從一個漂亮列表開始，最後才猜資料該如何保存。

## 分階段完成

先跑環境、migration與登入；接著完成CRUD、跨帳號拒絕與私人檔案；再加API、快取及命令去重。每階段保持測試可跑，避免一次把未驗證元件堆在一起。

完整下載包是可執行參考版本；學習時可從骨架逐步比對，不需一次記住全部檔案。每次修改都能說明更動的契約與對應測試，才是完成專題的目的。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大StudyHub專題：先定義交付範圍圖解"><img src="assets/figures/25.svg" alt="StudyHub專題：先定義交付範圍：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「StudyHub專題：先定義交付範圍」讀圖：沿專題的資料到評估路徑，列出每一階段應留下的成果。再回答：哪些功能最適合先做成可驗證基準？</p></div>

## 自我檢查與解析

**題目：**哪些功能最適合先做成可驗證基準？

<details><summary>展開解析</summary><p>環境、schema、登入與擁有者CRUD，先確保核心資料與權限，再擴充附件、API與進階工程。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
