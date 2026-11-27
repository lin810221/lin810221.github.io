# 參數化INSERT、UPDATE與DELETE

值使用參數，結構使用白名單；先讓寫入邊界可以被驗證。

## 值與SQL結構不同

DuckDB的Python值參數使用問號，Psycopg使用 `%s`。把使用者輸入直接用字串拼進SQL，可能讓資料被解讀成指令。參數應作為獨立引數傳入，不在外面再加SQL引號。

```python
connection.execute('UPDATE orders SET amount_cents=? WHERE order_id=?', [4500,102])
```

識別字、排序方向與整段WHERE結構不是一般值參數能替代的東西。需要動態欄位時，使用固定白名單，PostgreSQL的識別字則可用Psycopg提供的組合工具；不要將「有參數」誤認成整段SQL都安全。

## 寫入前後都要驗證

明列INSERT欄位，避免schema新增欄位後位置式寫入失效。UPDATE與DELETE先確認條件會選中哪些鍵，再在交易中執行並驗證影響結果。為了「先看看」而在正式資料上直接刪除再想辦法補回，並不是可靠的驗證方式。

## 本課的注入反例

將看似SQL片段的字串當作姓名查詢，正確的參數化結果應是找不到該姓名，而不是回傳所有客戶。測試還要確認客戶表仍完整。這個反例證明的是值綁定語意，不代表任何來自使用者的自由SQL都可以安全執行。

本課實驗使用獨立fixture或私人測試schema；不要將教學寫入指令直接指向公司的既有資料庫。

## 可執行查詢

以下是下載包 `queries/31.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT customer_id,name FROM customers WHERE name=? ORDER BY customer_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大參數化INSERT、UPDATE與DELETE圖解"><img src="assets/figures/13.svg" alt="參數化INSERT、UPDATE與DELETE：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「參數化INSERT、UPDATE與DELETE」讀圖：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。請用圖回答：使用參數後，能否把使用者輸入的排序欄位直接當作值參數？</p></div>

## 自我檢查與解析

**題目：**使用參數後，能否把使用者輸入的排序欄位直接當作值參數？

<details><summary>展開解析</summary><p>不能。值參數處理資料值，欄位與排序方向屬SQL結構，應使用白名單與適當識別字工具。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab31.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab31.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/sql-insert.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
