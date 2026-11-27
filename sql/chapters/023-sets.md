# UNION、INTERSECT與EXCEPT

把集合與多重集合分清楚，別讓預設去重改變來源事實。

## 合併資料前先對齊schema

集合操作要求欄位數與型別可對應。它通常依位置對應欄位，不因欄名相同就自動重排。先明列欄位與單位，確認兩個來源都是同一粒度，再決定如何合併。

UNION預設去除重複結果列，UNION ALL保留所有來源列。若同一筆業務事件可以重送，單純UNION不會完成可靠去重：不同欄位的事件可能仍是同一實體，同值列也可能是不同合法事件。

## 交集與差集

INTERSECT找兩邊共同存在的結果列，EXCEPT找左邊有、右邊沒有的列。適用於對帳與資料差異檢查，但要先確定比較的欄位就是你要驗收的契約。若把不重要的產製時間也放進比較，每次重建可能都顯示全表不同。

```sql
SELECT order_id FROM orders
EXCEPT
SELECT DISTINCT order_id FROM items;
```

本例應為空結果，因為每個訂單都有明細。這只能驗證「至少有明細鍵」，不能證明明細總額正確；還需後面的金額對帳。

## 差異的解釋

零差異是否等於成功，取決於驗收欄位是否完整。列數相同但金額不同、總額相同但個別鍵不同，都需要另外的檢查。集合操作是很好的比較工具，但不是品質保證的替代名稱。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大UNION、INTERSECT與EXCEPT圖解"><img src="assets/figures/08.svg" alt="UNION、INTERSECT與EXCEPT：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「UNION、INTERSECT與EXCEPT」讀圖：數出兩筆明細與兩筆退款形成的四格配對，再說明直接SUM為何重複，及先各自聚合如何修正。請用圖回答：UNION ALL得到重複外觀的列，是否一定應改用UNION？</p></div>

## 自我檢查與解析

**題目：**UNION ALL得到重複外觀的列，是否一定應改用UNION？

<details><summary>展開解析</summary><p>不一定。同值列可能代表不同合法事件；是否去重應依業務識別與來源契約決定，不能只依外觀或避免多幾筆資料。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab08.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab08.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
