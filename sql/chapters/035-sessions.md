# 移動視窗、缺日與sessionization

時間分析要分清楚最近幾列和最近幾天。

## 三列不一定是三天

`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`取最近最多三列。若某天沒有資料，三列可能跨越一週；如果一天有多列，三列又可能都在同一天。想分析固定天數，應先定義日期粒度與缺日補值政策，再選時間範圍。

用日期骨架補齊缺日後，零與缺值仍要分開。當天確定沒有訂單可補零，當天資料尚未抵達則應保留未知或未完成標記。若補錯，移動平均會看起來平穩卻失去真實意義。

## 以時間間隔形成session

先按使用者與完整事件順序排序，用LAG取上一個時間；若間隔超過規則門檻，就標記新session，接著對標記做累積和。門檻來自業務定義，不是SQL函數替你提供的自然常數。

遲到事件可能插進原本兩筆之間，改變session邊界。增量模型若只處理最新一列，可能無法修正先前的群組；需要重算足夠範圍或保存可修復的歷史，後面會在遲到資料章接續討論。

## 驗收方法

建立同時間、剛好等於門檻、超過門檻、缺日與遲到的反例，逐一手算分組。先驗證排序和邊界，再量測效能。只用規律連續資料測試，很容易讓「幾列」和「幾天」看起來像同一件事。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大移動視窗、缺日與sessionization圖解"><img src="assets/figures/12.svg" alt="移動視窗、缺日與sessionization：讀取三列測量值，對照第三列的前值，並辨認PostgreSQL 19與DuckDB空值選項的語法位置不同。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「移動視窗、缺日與sessionization」讀圖：讀取三列測量值，對照第三列的前值，並辨認PostgreSQL 19與DuckDB空值選項的語法位置不同。請用圖回答：最近三列的平均，是否就等於最近三天的平均？</p></div>

## 自我檢查與解析

**題目：**最近三列的平均，是否就等於最近三天的平均？

<details><summary>展開解析</summary><p>不一定。列的時間間隔可能不同，一天也可能多列；必須先定義日期粒度、缺日與資料完整性，再建立相應時間視窗。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab12.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab12.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/functions/window_functions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
