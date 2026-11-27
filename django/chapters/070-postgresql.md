# 從SQLite到PostgreSQL

連線字串改了，資料與交易語意仍需驗證。

## 為什麼需要另一條支線

SQLite適合本機起步與部分應用，但寫入競爭、鎖定、部署保存與資料庫能力應按需求評估。PostgreSQL支線使用選定驅動與正式設定，需另外提供資料庫服務、帳密、網路與備份。

```powershell
python -m pip install -r requirements-postgres.txt
python manage.py migrate --settings=studyhub.production
```

先確認設定指向預期資料庫。上面的migrate建立schema，不會自動把SQLite既有資料搬過去；資料匯出、轉換、匯入與校驗是另一份工作。

## 重新驗證資料庫行為

測約束、查詢、大小寫、排序、交易隔離、select_for_update與併發重試。使用EXPLAIN研究查詢計畫，記錄代表性資料與統計；不要只沿用SQLite的一次快速結果。

本課提供驅動版本與設定模板，未啟動真實PostgreSQL服務，不能宣稱其並行與備份還原已實測。正式使用時先在隔離資料庫完成遷移及回復演練。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大從SQLite到PostgreSQL圖解"><img src="assets/figures/24.svg" alt="從SQLite到PostgreSQL：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「從SQLite到PostgreSQL」讀圖：區分程式、資料、靜態檔與備份，確認更新與回復的順序。再回答：切到PostgreSQL後執行migrate，原SQLite資料會自動出現嗎？</p></div>

## 自我檢查與解析

**題目：**切到PostgreSQL後執行migrate，原SQLite資料會自動出現嗎？

<details><summary>展開解析</summary><p>不會。migration處理schema演進，跨資料庫資料搬移需另行規劃並校驗。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/ref/databases/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
