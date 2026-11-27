# EXPLAIN與實際執行計畫

把邏輯查詢和物理運算對照，再根據證據找瓶頸。

## 計畫在說什麼

掃描、篩選、JOIN、聚合、排序與視窗是常見運算節點。讀計畫時先追蹤資料從哪裡進入，再看每層列數如何變化。估計列數與實際列數不一致，可能讓最佳化器選到不適合的策略。

EXPLAIN說明計畫，EXPLAIN ANALYZE會實際執行工作再加入量測。若敘述會修改資料，不能因為前面加了ANALYZE就當成唯讀觀察；本課先用SELECT示範，其他操作需在明確測試交易與環境中驗證。

## 列數比單一耗時更有解釋力

看見某節點輸出倍增，可能指向JOIN粒度；掃描後只剩極少數列，可能值得評估存取路徑；排序或視窗占大量時間，則需檢查輸入規模與必要欄位。這些是診斷方向，不是只看一個節點名稱就能決定修法。

## 小資料的限制

五筆fixture只能驗證查詢能執行及計畫結構，不代表正式資料的最佳索引或耗時。本課測試只核對計畫包含合理運算，不把每次浮動的毫秒數寫死成正確答案。

效能報告應附引擎版本、資料量、查詢、設定、冷熱狀態與重複量測方式。先保存基線，再一次改一個假設，才能知道改善是否來自你以為的原因。

## 可執行查詢

以下是下載包 `queries/17.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
EXPLAIN ANALYZE SELECT customer_id,SUM(amount_cents)
FROM orders WHERE status='paid' GROUP BY customer_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大EXPLAIN與實際執行計畫圖解"><img src="assets/figures/17.svg" alt="EXPLAIN與實際執行計畫：沿五列來源、四列付款與三組客戶追蹤列數，區分實際計畫證據與只憑函數名稱的推測。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「EXPLAIN與實際執行計畫」讀圖：沿五列來源、四列付款與三組客戶追蹤列數，區分實際計畫證據與只憑函數名稱的推測。請用圖回答：對UPDATE使用EXPLAIN ANALYZE，是否就不會真的修改資料？</p></div>

## 自我檢查與解析

**題目：**對UPDATE使用EXPLAIN ANALYZE，是否就不會真的修改資料？

<details><summary>展開解析</summary><p>不是。ANALYZE會執行敘述，可能產生副作用；應在適當測試環境與交易中驗證，不能當成通用唯讀操作。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab17.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab17.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/guides/meta/explain_analyze)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
