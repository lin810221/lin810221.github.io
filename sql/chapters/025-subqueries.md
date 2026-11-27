# 純量、表格與相關子查詢

先確認子查詢回傳的形狀，再看它和外層資料的關係。

## 子查詢可以扮演不同角色

純量子查詢應回傳一個值；表格子查詢提供一組列與欄位；相關子查詢則引用外層的值。SQL成功解析，不代表每份資料都會符合這些形狀。例如純量位置回傳多列，通常會報錯，不能隨便加LIMIT隱藏不唯一的設計。

```sql
SELECT order_id,amount_cents
FROM orders
WHERE amount_cents > (SELECT AVG(amount_cents) FROM orders WHERE status='paid')
  AND status='paid'
ORDER BY order_id;
```

本例先定義付款平均3250美分，再找高於平均的付款訂單。外層與子查詢的付款條件都必須符合問題，否則可能用不同集合的平均去篩選資料。

## 相關條件的閱讀方法

把外層一列代入子查詢，理解它會找什麼，再思考所有外層列的結果。這是語意上的心智模型；最佳化器可能將它改寫成JOIN或其他運算，不保證實際逐列執行。效能判斷仍應查看執行計畫。

## 清楚優先於一行寫完

層數太深時，先抽成命名CTE或View，讓資料集合、聚合分母和過濾條件可單獨驗證。不要因為查詢短就認為比較快，也不要把所有子查詢都一律改成JOIN；改寫後必須重新確認空值、重複與粒度語意。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大純量、表格與相關子查詢圖解"><img src="assets/figures/09.svg" alt="純量、表格與相關子查詢：沿商品與退款兩條分支觀察粒度先縮成每訂單一列，再連到訂單主表，逐層核對唯一性。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「純量、表格與相關子查詢」讀圖：沿商品與退款兩條分支觀察粒度先縮成每訂單一列，再連到訂單主表，逐層核對唯一性。請用圖回答：純量子查詢回傳多筆客戶時，直接加LIMIT 1是否是可靠修正？</p></div>

## 自我檢查與解析

**題目：**純量子查詢回傳多筆客戶時，直接加LIMIT 1是否是可靠修正？

<details><summary>展開解析</summary><p>不可靠。應先找出為何無法唯一決定值；任意挑一列會把資料契約問題藏起來，只有業務明定挑選規則時才可排序後取一列。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab09.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab09.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
