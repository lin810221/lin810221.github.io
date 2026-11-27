# PostgreSQL 19的私人伺服器實驗

把伺服器能力放到真實資料庫驗證，不以本機動畫代替。

## 環境與執行方式

2026-11-27查核最新穩定版PostgreSQL 19.0，Python驅動使用Psycopg 3.3.9。本課實測以私人、僅綁localhost的臨時叢集進行，結束後停止；不安裝系統服務、不操作既有公司資料表。下載包不包含大型伺服器binary，請依官方方式準備自己的私人環境。

```powershell
python -m pip install -r requirements-postgres.txt
$env:SQL_COURSE_PG_DSN='host=127.0.0.1 port=5432 dbname=course_lab user=course_admin connect_timeout=5'
python postgres_lab.py
```

上面連線字串是私人環境的範例，沒有附密碼；請依自己的認證與權限設定。實驗帳號需要建立私人schema與角色的權限，不是一般報表使用者帳號。

## 這次真正驗證的能力

Read Committed與Repeatable Read的雙連線結果不同；SKIP LOCKED略過鎖定列；Serializable寫偏差案例有一個40001；受限角色只看到RLS允許的租戶。19版的ON CONFLICT DO SELECT和IGNORE NULLS也在伺服器上執行。

## 新功能不等於應該立即使用

19版新增REPACK及其他管理能力，但本課不在既有資料庫執行維護重寫。升版或採用新功能時，先讀正式文件、測試與回復。也要確認舊環境是否支援，不能將19版語法貼到18版後把錯誤歸因於SQL概念。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/35.svg" target="_blank" rel="noopener" aria-label="放大PostgreSQL 19的私人伺服器實驗圖解"><img src="assets/figures/35.svg" alt="PostgreSQL 19的私人伺服器實驗：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「PostgreSQL 19的私人伺服器實驗」讀圖：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。請用圖回答：PostgreSQL 19專用語法在18版報錯，為何不能因此判定本課所有SQL概念都錯誤？</p></div>

## 自我檢查與解析

**題目：**PostgreSQL 19專用語法在18版報錯，為何不能因此判定本課所有SQL概念都錯誤？

<details><summary>展開解析</summary><p>語言概念與產品版本支援是不同層次。應先核對伺服器及驅動版本，再按對應文件驗證該語法是否可用。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab35.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab35.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/release-19.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
