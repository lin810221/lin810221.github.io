# 批次寫入、COPY與staging

先把大量輸入放到可驗證的中間層，再決定正式合併。

## 不必逐列建立網路往返

大量資料若每列各開交易與連線，常有額外成本。Python的批次介面、資料庫COPY或直接讀檔都有不同適用情境。它們可以改善輸入成本，卻不會替你決定去重、空值與業務規則。

在DuckDB本機主線，可明確指定CSV欄位型別後讀入staging；PostgreSQL則區分伺服器端COPY與psql的客戶端 `\copy`。檔案在哪台機器、由誰讀取、需要哪些權限，都不能混為一談。

## 原始值與轉型值分開

先保留來源編號與原始金額，再建立解析後欄位、有效性與失敗原因。若直接將所有輸入CAST進正式表，一個錯誤可能讓整批失敗，也可能依設定被忽略；兩種行為都需要明確契約與筆數對帳。

## 批次邊界與交易

一次輸入多大，要考慮記憶體、鎖定、失敗重試與來源可重讀能力。不要只用小fixture的毫秒數決定正式批量。每批需有穩定識別、來源範圍和驗收結果，才知道重跑是不是同一批。

本課CSV實驗保留前導零與包含逗號的文字，確認讀檔不是用簡單字串分割冒充CSV解析。後面DataHarbor則使用固定事件外框與閉合序列範圍，讓整批是否完整可以被測試。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大批次寫入、COPY與staging圖解"><img src="assets/figures/13.svg" alt="批次寫入、COPY與staging：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「批次寫入、COPY與staging」讀圖：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。請用圖回答：COPY成功是否就表示來源所有列都符合報表契約？</p></div>

## 自我檢查與解析

**題目：**COPY成功是否就表示來源所有列都符合報表契約？

<details><summary>展開解析</summary><p>不一定。成功只表示該次讀取與寫入被接受，仍需核對schema、解析狀態、筆數、鍵與金額；若設定忽略錯誤，尤其要對帳被略過的資料。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab13.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab13.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/data/csv/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
