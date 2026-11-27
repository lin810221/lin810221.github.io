# 遞迴CTE、階層與循環

遞迴需要明確的起點、擴展規則和終止條件。

## 從根節點往下走

遞迴CTE先以anchor查詢找起點，再把已找到的列交給遞迴部分繼續擴展。本例從沒有上層的lead開始，再按parent_id找子節點，產生depth。最後依深度與鍵排序，得到穩定的顯示結果。

## UNION ALL與終止

UNION ALL保留所有產生的路徑，若資料存在循環，就可能不斷產生新列。UNION去重也不一定能解決：當每次還加入不同depth或path，整列內容並不相同。因此真正的圖走訪需要決定如何追蹤已走過的節點或路徑，並按引擎能力使用合適語法。

範例設了明確深度上限，用來限制合成階層的展開；它不是通用的循環偵測。若某個合法組織真的比上限深，查詢可能截斷結果，必須回報限制而非宣稱已完整走訪。

## 階層樹與一般圖不同

樹的每個子節點通常只有一個父節點，一般有向圖可能有多條路徑走到同一節點。要列出所有路徑，還是只要可達節點，是不同問題。先定義粒度，才能決定何時去重。

執行實驗後，先畫出五個staff節點與父子邊，再核對輸出的深度。若出現未連到任何根的節點，還要檢查孤立節點、缺少父節點或循環，不能只看回傳列都是合法值。

## 可執行查詢

以下是下載包 `queries/09.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH RECURSIVE tree(id,parent_id,name,depth) AS (
  SELECT id,parent_id,name,0 FROM staff WHERE parent_id IS NULL
  UNION ALL
  SELECT s.id,s.parent_id,s.name,t.depth+1
  FROM staff s JOIN tree t ON s.parent_id=t.id WHERE t.depth<10
)
SELECT id,name,depth FROM tree ORDER BY depth,id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大遞迴CTE、階層與循環圖解"><img src="assets/figures/10.svg" alt="遞迴CTE、階層與循環：從根1沿父子邊讀出2與5，再到3與4；辨認深度上限只限制展開，不等於完整循環偵測。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「遞迴CTE、階層與循環」讀圖：從根1沿父子邊讀出2與5，再到3與4；辨認深度上限只限制展開，不等於完整循環偵測。請用圖回答：查詢加了深度上限10，能否宣稱已自動辨識所有循環？</p></div>

## 自我檢查與解析

**題目：**查詢加了深度上限10，能否宣稱已自動辨識所有循環？

<details><summary>展開解析</summary><p>不能。深度上限只限制展開成本，可能截斷合法深層資料；循環偵測需要另外的路徑或已訪問節點邏輯。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab09.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab09.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/query_syntax/with)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
