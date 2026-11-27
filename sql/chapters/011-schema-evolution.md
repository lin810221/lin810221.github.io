# CREATE、ALTER與schema演進

把欄位變更當作資料契約遷移，而不是只修改一段DDL。

## 新表與既有資料有不同風險

`CREATE TABLE`定義新表，`ALTER TABLE`修改既有schema；但實際可用語法、是否重寫資料及鎖定成本要看引擎。不要把DuckDB上能執行的ALTER選項直接當成PostgreSQL部署方案，也不要反向推論。

新增非空欄位時，舊資料從哪裡取得合法值？縮窄型別時，既有值是否都可轉換？刪除欄位時，哪些下游模型與報表還在使用？這些問題應在變更之前回答。先備份不代表已經具備可恢復能力，還要演練回讀與驗證。

## 擴充、搬移、收斂

常見做法是先新增可相容欄位，再回補舊資料，讓新舊程式在過渡期都能運作，最後才移除舊欄位。這個順序需要配套的資料檢查與觀察期；若資料語意也改變，就不是重新命名欄位而已。

本課專題把模型版本寫進發布manifest。不同模型版本應有自己的產出與回復計畫，不能在同一份已發布Parquet中偷偷改變欄位意義。schema演進的測試應同時包含舊資料、新資料和下游讀取者，不只測最新的空資料庫。

## 最小交付紀錄

記錄變更前後schema、影響的資料集、回補查詢、驗收結果與回復方法。大型表的DDL成本要在相近資料量與引擎上觀察，這裡的五筆fixture只驗證語意，不宣稱能代表正式環境的耗時。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大CREATE、ALTER與schema演進圖解"><img src="assets/figures/04.svg" alt="CREATE、ALTER與schema演進：從唯一客戶鍵走向訂單外鍵，再檢查重複鍵、不存在的關聯與非法欄位值會在哪裡被拒絕。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CREATE、ALTER與schema演進」讀圖：從唯一客戶鍵走向訂單外鍵，再檢查重複鍵、不存在的關聯與非法欄位值會在哪裡被拒絕。請用圖回答：把欄位型別改成功，是否就代表下游報表一定相容？</p></div>

## 自我檢查與解析

**題目：**把欄位型別改成功，是否就代表下游報表一定相容？

<details><summary>展開解析</summary><p>不是。名稱、空值、單位、精度與業務意義都可能改變；需要下游讀取和指標對帳，DDL成功只代表某一層接受變更。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab04.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab04.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-alter.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
