# 部署提案與驗收清單

把本地已驗證與目標環境待驗證寫清楚。

## 畫出你的部署

標示網域、TLS、反向代理、WSGI或ASGI服務、資料庫、快取、工作系統及儲存。沒有使用的元件可省略，不為了看起來完整就加入不必要的服務。每個元件寫出誰設定、資料存哪裡與如何觀測。

列出環境值、啟動命令、migration、collectstatic、健康檢查、權限回歸與備份還原步驟。執行check --deploy後保留警告與處理理由，不以隱藏警告充當驗收。

## 發布前的確認

用非管理者帳號完成主要操作，再測跨帳號拒絕與私人下載。確認DEBUG未開、靜態檔可載入、HTTPS與cookie符合實際代理環境，並有可用回復路徑。

本課的靜態教學站和Django動態專案分開交付。前者已依本repo流程建置，後者先提供可重現本機版本；真實雲端服務與PostgreSQL保留額外條件，不冒稱已替你發布。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大部署提案與驗收清單圖解"><img src="assets/figures/24.svg" alt="部署提案與驗收清單：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「部署提案與驗收清單」讀圖：區分程式、資料、靜態檔與備份，確認更新與回復的順序。再回答：正式方案尚未決定網域，應直接開啟所有HSTS子網域選項嗎？</p></div>

## 自我檢查與解析

**題目：**正式方案尚未決定網域，應直接開啟所有HSTS子網域選項嗎？

<details><summary>展開解析</summary><p>不應。需先確認所有相關子網域與HTTPS條件，再按實際部署決策。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
