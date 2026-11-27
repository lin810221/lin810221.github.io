# 筆數、金額與鍵的來源對帳

多種互補檢查，才能避免錯誤互相抵消。

## 從一個可以手算的條件開始

每張訂單的明細數量乘單價後加總，應等於本課訂單表的金額。這份條件來自本課fixture契約；真實世界若有稅、運費、折扣與分攤，必須一起定義，不能直接套用相同公式。

## 訂單層對帳的定義

令 $q_{ij}$ 為訂單 $i$ 第 $j$ 項數量，$p_{ij}$ 為美分單價，$A_i$ 為訂單金額：

$$\Delta_i=A_i-\sum_j q_{ij}p_{ij}.$$

本課要求每張訂單的差異為零。實驗查詢只回傳不一致鍵，正常fixture因此是空結果；這和「查不到任何來源訂單」完全不同，還要另外驗證來源筆數。

## 全體總額仍不夠

一筆多算100、一筆少算100，總差異仍為零。所以先按主要鍵或分割找差異，再看全體總額。對退款、取消與日期歸屬亦分開核對，避免口徑混在一起。

## 驗收紀錄

記錄來源範圍、模型版本、比較欄位、容許差異和處理方式。若允許四捨五入誤差，也要說清楚最小單位與累積規則；不能看到差一點點就臨時增加容許值。

## 可執行查詢

以下是下載包 `queries/28.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH by_item AS (SELECT order_id,SUM(quantity*unit_cents) AS item_cents FROM items GROUP BY order_id)
SELECT o.order_id,o.amount_cents,i.item_cents,o.amount_cents-i.item_cents AS difference
FROM orders o JOIN by_item i ON o.order_id=i.order_id
WHERE o.amount_cents<>i.item_cents;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/28.svg" target="_blank" rel="noopener" aria-label="放大筆數、金額與鍵的來源對帳圖解"><img src="assets/figures/28.svg" alt="筆數、金額與鍵的來源對帳：在故意修改的反例中找出正負100的兩筆差異，說明只核對全體總額會漏掉個別錯誤。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「筆數、金額與鍵的來源對帳」讀圖：在故意修改的反例中找出正負100的兩筆差異，說明只核對全體總額會漏掉個別錯誤。請用圖回答：所有訂單差異加總為零，是否就代表每張訂單都正確？</p></div>

## 自我檢查與解析

**題目：**所有訂單差異加總為零，是否就代表每張訂單都正確？

<details><summary>展開解析</summary><p>不代表。正負差異可能互相抵消，應逐鍵檢查並另外核對來源完整性與指標口徑。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab28.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab28.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/datatype-numeric.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
