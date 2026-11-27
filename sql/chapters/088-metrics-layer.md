# Mart、指標定義與語意層

同一個名稱，必須對應同一份可重算的問題。

## 指標是一份完整定義

付款總額需要說明狀態、時間欄位、幣別、退款與取消政策；訂單數需要指定訂單粒度；平均則要列分子與分母。只把一段SUM取名revenue，不等於已建立團隊共同語意。

## Mart整理使用情境

地區mart將資料整理成每地區一列，日mart則是每天一列。維度、日期角色與過濾條件應固定並公開，避免不同報表各自重寫稍有差異的查詢。對可重用指標保存測試與來源連結。

## 半可加與不可加量

去重客戶數跨地區加總可能重複，平均需加權重建，比率需重新聚合分子分母。餘額快照跨時間直接相加也通常不符合問題。語意層工具不能替代對這些規則的理解。

## 版本與變更

指標定義改變時，評估歷史重算和下游影響，保存舊版本及對帳。用相同欄名覆寫新口徑，會讓使用者誤以為歷史可直接比較。若只是修正錯誤，也應留下原因與受影響範圍。

本課的region報表分別示範目前地區與歷史地區；公開版本由manifest連到模型與來源序列。這提供最小的可追溯主線，不假裝已實作完整的企業指標管理平台。

## 可執行查詢

以下是下載包 `queries/29.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT c.region,COUNT(*) AS paid_orders,SUM(o.amount_cents) AS paid_cents
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
WHERE o.status='paid' GROUP BY c.region ORDER BY c.region;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大Mart、指標定義與語意層圖解"><img src="assets/figures/29.svg" alt="Mart、指標定義與語意層：找到事實主鍵和歷史維度代理鍵，解釋多個客戶版本不應讓同一筆訂單多配對。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Mart、指標定義與語意層」讀圖：找到事實主鍵和歷史維度代理鍵，解釋多個客戶版本不應讓同一筆訂單多配對。請用圖回答：平均與去重客戶數為什麼不適合直接把各地區值相加？</p></div>

## 自我檢查與解析

**題目：**平均與去重客戶數為什麼不適合直接把各地區值相加？

<details><summary>展開解析</summary><p>平均需要分子分母，去重客戶可能跨地區重複；兩者都需按全體問題重新聚合，而非套用付款總額的可加性。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab29.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab29.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
