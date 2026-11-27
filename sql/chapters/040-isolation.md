# MVCC與隔離等級

快照、鎖與序列化各自回答不同併發問題。

## 同時執行的交易會看見什麼

MVCC讓不同交易讀到符合隔離規則的資料版本。它不是「沒有鎖」的同義詞，也不表示任何讀改寫流程都安全。先說明你要防止的是髒讀、同一交易內再次讀取不同值，還是跨多列條件的寫偏差。

PostgreSQL的Read Committed通常每個敘述取得新的快照；Repeatable Read在交易中維持一致快照，但仍可能有序列化異常；Serializable則要求可對應某個序列順序，必要時會中止交易，讓應用程式重新執行整個決策。

## 本課的真實雙連線實驗

第一個連線先讀100，第二個連線提交更新為200。Read Committed的第一個連線再次讀會看到200，Repeatable Read則維持100。這些結果來自PostgreSQL 19私人叢集，不用JavaScript動畫冒充資料庫快照。

## 條件寫入與重試

只讀出庫存再由程式減一，可能有lost update風險。可按問題使用帶條件的UPDATE與RETURNING、列鎖或Serializable交易，但每種方式都有等待、衝突與錯誤處理成本。不能只把隔離等級調高，就假設應用程式不再需要重試。

DuckDB嵌入式模式使用自身的併發與衝突規則，不提供與PostgreSQL完全相同的伺服器多連線操作方式。教材分別驗證，而不讓名稱相近的交易語法掩蓋部署差異。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大MVCC與隔離等級圖解"><img src="assets/figures/14.svg" alt="MVCC與隔離等級：沿讀取、另一連線提交與再次讀取三個時點，分辨Read Committed和Repeatable Read的可見值。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「MVCC與隔離等級」讀圖：沿讀取、另一連線提交與再次讀取三個時點，分辨Read Committed和Repeatable Read的可見值。請用圖回答：PostgreSQL的Repeatable Read能否自動保證所有跨列業務條件都等同序列執行？</p></div>

## 自我檢查與解析

**題目：**PostgreSQL的Repeatable Read能否自動保證所有跨列業務條件都等同序列執行？

<details><summary>展開解析</summary><p>不能。它維持快照並防止部分異常，但仍可能有寫偏差等序列化異常；必要時用Serializable並正確重試整個交易。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab14.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab14.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/transaction-iso.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
