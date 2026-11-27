# 列鎖、死結與整個交易重試

把可重試衝突和永久輸入錯誤分開處理。

## 列鎖和工作領取

PostgreSQL的FOR UPDATE可鎖住選定資料列；SKIP LOCKED則略過已被其他交易鎖住的列，適合部分工作佇列領取情境。它不是一般報表的完整一致讀法，因為你刻意容許略過資料。

本課雙連線實驗先鎖住第一列，再讓第二個連線使用SKIP LOCKED，只取得第二列。測試結束會回滾並清理私人schema，不碰既有應用程式資料。

## 以固定順序降低死結

若兩個交易以相反順序取得相同資源，可能形成死結。盡量縮短交易、使用一致鎖定順序並設定合理等待限制。發生衝突時，先辨認錯誤類型；缺欄位或資料違反契約不應當作暫時問題無限重試。

## Serializable可能主動中止

本課讓兩個交易都讀到兩筆有效資料，再分別更新不同列，重現跨列決策衝突。19版實驗應有一個提交、一個回報SQLSTATE 40001。正確重試範圍是整個交易，包括先前讀取與決策，不是只重送最後一條UPDATE。

外部副作用則需要命令識別或outbox等機制。即使資料庫交易重試安全，也不代表外部寄信或扣款重送可以沒有自己的重複處理契約。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大列鎖、死結與整個交易重試圖解"><img src="assets/figures/14.svg" alt="列鎖、死結與整個交易重試：沿讀取、另一連線提交與再次讀取三個時點，分辨Read Committed和Repeatable Read的可見值。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「列鎖、死結與整個交易重試」讀圖：沿讀取、另一連線提交與再次讀取三個時點，分辨Read Committed和Repeatable Read的可見值。請用圖回答：收到40001後，只重送最後一條UPDATE為什麼不夠？</p></div>

## 自我檢查與解析

**題目：**收到40001後，只重送最後一條UPDATE為什麼不夠？

<details><summary>展開解析</summary><p>因為先前的讀取與判斷可能已不再成立。序列化失敗應在新的交易中重新執行整個決策，並確保外部副作用另有去重或outbox設計。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab14.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab14.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/explicit-locking.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
