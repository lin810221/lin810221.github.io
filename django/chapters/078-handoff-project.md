# 交接專題：乾淨環境重新啟動

成品能被另一個人重建，才算完成工程主線。

## 交付內容

提供README、鎖版、Model與migration、模板與資產、測試、合成資料命令及部署設定說明。不要把自己的真實帳號資料、密鑰、私人附件與本機資料庫一起當示範發佈。

在乾淨環境安裝、migrate、自行建立帳號、執行seed並啟動網站，再跑全部測試。若只能在原作者電腦運作，先找未記錄依賴、手動schema或路徑假設。

## 說明已驗證與尚未驗證

下載包的CPU與SQLite主線實際執行，外部PostgreSQL、寄信、快取與Task backend需各自環境。本課不替你建立付費帳戶或發布私人動態服務；靜態教材仍由現有網站流程管理。

最後寫出回復資料、更新套件與排錯步驟，讓維護者能理解成品。不只留下一條啟動命令，也留下發生錯誤時該檢查的版本、設定與證據。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大交接專題：乾淨環境重新啟動圖解"><img src="assets/figures/26.svg" alt="交接專題：乾淨環境重新啟動：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「交接專題：乾淨環境重新啟動」讀圖：依端到端操作找出帳號、CRUD、附件與API共用的權限邊界。再回答：交接時最不應放進公開程式包的是什麼？</p></div>

## 自我檢查與解析

**題目：**交接時最不應放進公開程式包的是什麼？

<details><summary>展開解析</summary><p>真實密鑰、cookie、私人附件與實際帳號資料庫；應提供安全的取得或建立流程。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/deployment/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
