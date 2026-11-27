# Hash Join、排序、記憶體與spill

演算法名稱需要搭配資料量與資源限制一起解讀。

## 相同SQL可以有不同物理策略

Hash Join通常為一側建立雜湊結構再配對另一側；Nested Loop逐一嘗試配對，若一側很小或可用索引也可能合適；Merge類策略則利用已排序資料。沒有一個名稱在所有資料量與分布下都必然最好。

## 輸入規模與偏斜

某個鍵有大量重複，可能造成遠多於預期的配對列與記憶體使用。這既是語意上的fanout，也可能是效能瓶頸。先檢查鍵頻率與目標粒度，再決定是否能先聚合、縮小欄位或改變處理方式。

## 記憶體與磁碟

超出記憶體時，某些運算可spill到暫存磁碟，但支援範圍與限制依引擎而異。暫存空間不足也會失敗，不能把「能使用磁碟」當作無限容量。適當限制執行緒、記憶體與暫存位置，並在受控環境下觀察。

## 先保持結果不變

移動篩選或先做聚合可能改善成本，也可能改變外連接與空值語意。每次改寫先跑小資料的正確性測試，再看大型資料的計畫。若只比較時間，錯誤地少算資料也可能看起來很快。

課程的五筆資料不提供正式規模壓測結論；它提供的是可以手算的語意基線，讓你之後量測效能時知道自己有沒有改變問題。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大Hash Join、排序、記憶體與spill圖解"><img src="assets/figures/17.svg" alt="Hash Join、排序、記憶體與spill：沿五列來源、四列付款與三組客戶追蹤列數，區分實際計畫證據與只憑函數名稱的推測。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Hash Join、排序、記憶體與spill」讀圖：沿五列來源、四列付款與三組客戶追蹤列數，區分實際計畫證據與只憑函數名稱的推測。請用圖回答：Hash Join看起來耗用很多記憶體，是否應直接把所有JOIN改成Nested Loop？</p></div>

## 自我檢查與解析

**題目：**Hash Join看起來耗用很多記憶體，是否應直接把所有JOIN改成Nested Loop？

<details><summary>展開解析</summary><p>不應。應先檢查資料規模、偏斜、估計與實際計畫，再選擇可保持語意的改善；單憑演算法名稱無法判定最佳方案。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab18.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab18.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/guides/performance/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
