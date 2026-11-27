# 第一次查詢與結果驗證

用一個可以手算的結果，理解SQL查詢的基本形狀。

## 從SELECT讀到結果

`SELECT`列出要回傳的欄位，`FROM`指定資料來源，`WHERE`保留符合條件的列，`ORDER BY`規定顯示順序。這是描述你要的資料，執行器可以自行選擇實際的掃描與連接策略；畫面上文字的先後不等於底層機器逐步照抄執行。

範例中已付款的是101、102、104、105，金額分別為3000、5000、4000、1000，單位一律為USD cents。四筆加總為13000，也就是130美元。取消訂單103的2000不算入這個付款總額，但它仍是存在的訂單，不應從原始資料直接刪除。

## 欄位與資料型別

表的欄位有名字與型別。結果中的整數不是自動帶有貨幣語意；欄名 `amount_cents` 和來源契約共同說明單位。用 `DESCRIBE orders` 觀察schema，再查詢幾列，會比先對未知資料做總和更可靠。

## 穩定順序與實作邊界

排序使用建立時間，再使用訂單鍵作為同值處理。若只寫 `LIMIT`而未排序，重跑看見不同列不一定是資料遺失。程式入口先建立獨立記憶體資料庫並載入固定fixture；你看到的結果不會受到其他實驗先前修改資料的影響。真正保存資料的檔案模式會在專題再介紹。

## 可執行查詢

以下是下載包 `queries/01.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
-- Grain: one returned row per paid order, in a deterministic order.
SELECT order_id, customer_id, amount_cents
FROM orders
WHERE status = 'paid'
ORDER BY created_at, order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大第一次查詢與結果驗證圖解"><img src="assets/figures/02.svg" alt="第一次查詢與結果驗證：同一訂單102對應兩筆不同商品明細，指出重複訂單鍵為何不是應刪除的重複事實。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「第一次查詢與結果驗證」讀圖：同一訂單102對應兩筆不同商品明細，指出重複訂單鍵為何不是應刪除的重複事實。請用圖回答：為什麼付款總額13000不能直接顯示成13000美元？</p></div>

## 自我檢查與解析

**題目：**為什麼付款總額13000不能直接顯示成13000美元？

<details><summary>展開解析</summary><p>欄位使用USD cents，須依契約換算為美元；數字型別本身不會保存這個業務單位。先核對分母與單位，再格式化輸出。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab02.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab02.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
