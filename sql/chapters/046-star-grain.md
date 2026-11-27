# 星型模型與事實表粒度

先宣告事實的一列，再選擇維度和可相加的量。

## 事實與維度

事實表保存度量與連接到維度的鍵，維度提供描述性的分析角度。訂單層事實可保存每訂單付款金額，明細層事實則保存商品與數量；兩者不能在沒有處理粒度差異時直接混合加總。

## 量的可加性

金額在相同幣別與口徑下通常可按訂單相加，平均值與比率則需要回到分子、分母。餘額等快照量可能可以跨客戶加總，卻不能跨時間直接加總。可加性是一份模型說明，不是資料型別自動提供的能力。

## 日期與狀態的選擇

訂單日期、付款日期與退款日期回答不同問題；即使都用同一張日期維度，也需以不同角色表達。狀態變動又可能改寫目前事實，或形成獨立的狀態事件歷史。先決定要回答當下狀態還是歷史流程，再選適合的粒度。

## 本課的最小倉儲

先使用目前訂單狀態與客戶地區生成地區付款mart，再加入歷史地區示範。DataHarbor則發布仍存活訂單的快照與每天付款彙總，不聲稱已完成完整會計或多幣別倉儲。

檢查每個事實鍵是否唯一、每個維度鍵是否找到對象，並將未知維度與延遲抵達的維度當作明確情境。不要因為分析表比較寬，就省略資料契約與對帳。

## 可執行查詢

以下是下載包 `queries/29.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT c.region,COUNT(*) AS paid_orders,SUM(o.amount_cents) AS paid_cents
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
WHERE o.status='paid' GROUP BY c.region ORDER BY c.region;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大星型模型與事實表粒度圖解"><img src="assets/figures/29.svg" alt="星型模型與事實表粒度：找到事實主鍵和歷史維度代理鍵，解釋多個客戶版本不應讓同一筆訂單多配對。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「星型模型與事實表粒度」讀圖：找到事實主鍵和歷史維度代理鍵，解釋多個客戶版本不應讓同一筆訂單多配對。請用圖回答：平均訂單金額能否像付款總額一樣直接跨地區相加？</p></div>

## 自我檢查與解析

**題目：**平均訂單金額能否像付款總額一樣直接跨地區相加？

<details><summary>展開解析</summary><p>不能。平均值不是可直接相加的量，整體平均需由各組總和及筆數重建，並保持相同時間與幣別口徑。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab29.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab29.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries-table-expressions.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
