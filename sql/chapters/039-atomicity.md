# BEGIN、COMMIT、ROLLBACK與原子性

相關資料變更一起成立，但外部副作用仍有自己的失敗邊界。

## 交易要包住一個完整決策

BEGIN開始交易，COMMIT提交，ROLLBACK撤銷未提交變更。本課把更新資料、前進checkpoint與建立發布outbox放在同一個資料庫交易中，避免出現資料尚未處理但游標已前進的狀態。

```python
connection.execute('BEGIN TRANSACTION')
try:
    connection.execute('UPDATE orders SET amount_cents=? WHERE order_id=?',[1,101])
    raise RuntimeError('test failure')
except Exception:
    connection.execute('ROLLBACK')
```

上例回滾後，訂單101仍應為3000美分。測試讀回實際值，而不只檢查有沒有呼叫ROLLBACK。正式程式也應確保連線在例外後進入可理解狀態，再決定重試或關閉。

## 原子性不會跨越所有系統

資料庫提交不會同時原子地寄信、更新外部API或替換檔案指標。若先提交資料再寫Parquet，程序可能在中間失敗；若反過來先公開檔案，使用者又可能讀到尚未提交的資料。

因此專題使用資料庫outbox記錄待發布工作，再以可重試的發布步驟完成檔案。這是明確處理兩個邊界，不宣稱得到通用跨系統交易。SAVEPOINT等細節亦需按產品支援確認，不把PostgreSQL能力直接套到DuckDB。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大BEGIN、COMMIT、ROLLBACK與原子性圖解"><img src="assets/figures/13.svg" alt="BEGIN、COMMIT、ROLLBACK與原子性：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「BEGIN、COMMIT、ROLLBACK與原子性」讀圖：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。請用圖回答：資料庫COMMIT成功，能否證明外部Parquet指標也已更新？</p></div>

## 自我檢查與解析

**題目：**資料庫COMMIT成功，能否證明外部Parquet指標也已更新？

<details><summary>展開解析</summary><p>不能。檔案系統是另一個提交邊界；需要outbox、不可變產物與可恢復的發布流程，不能把資料庫原子性擴大成跨系統保證。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab13.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab13.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/statements/transactions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
