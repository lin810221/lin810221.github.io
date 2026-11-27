# 安裝Django 6.1.3與隔離環境

以2026-11-26最新穩定版實測，不拿舊環境充當版本基準。

## 版本與前置條件

官方下載頁及PyPI確認Django 6.1.3，搭配Python 3.15.2；官方相容表已加入Python 3.15支援。REST API章使用DRF 3.18.3，完整相依保存在下載包。第一次安裝需要網路，核心操作不需外部API或資料庫服務。

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
python -m django --version
python 01_environment.py
```

## 確認你執行哪個Python

以上指令在解壓後的 `examples` 目錄執行。若PowerShell限制啟動腳本，可直接使用 `.venv\Scripts\python.exe` 執行，不必為了課程放寬整台電腦政策。Linux與macOS使用 `python3 -m venv .venv`，再啟動 `.venv/bin/activate`。

本課的獨立算例使用記憶體SQLite；完整網站使用本地資料檔，兩者不要混淆。更新套件時先查正式發布與相容性，再跑測試與重建鎖版；不要在其他課程的環境原地升級。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大安裝Django 6.1.3與隔離環境圖解"><img src="assets/figures/01.svg" alt="安裝Django 6.1.3與隔離環境：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「安裝Django 6.1.3與隔離環境」讀圖：追蹤瀏覽器與伺服器的請求及回應，指出靜態教材與Django程式各在哪裡執行。再回答：終端顯示已安裝Django，程式卻說找不到模組，先查什麼？</p></div>

## 自我檢查與解析

**題目：**終端顯示已安裝Django，程式卻說找不到模組，先查什麼？

<details><summary>展開解析</summary><p>檢查執行的Python與pip是否來自同一個虛擬環境，用python呼叫pip可減少環境混淆。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 01_environment.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:01_environment.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/install/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
