# 更新時間與主鍵的複合游標

在同時間多列的情況下，讓分頁有完整順序。

## 單一時間不足以定位一列

如果三筆更新都在同一個時間，第一頁只讀兩筆，下一頁只用時間嚴格大於就會漏掉第三筆。複合游標保存時間與穩定鍵，使用相同排序及比較，才能接續同時間尚未讀的列。

```sql
WHERE (updated_at,id) > (:last_time,:last_id)
ORDER BY updated_at,id
LIMIT :page_size
```

這是邏輯形狀，值參數實際寫法依驅動而定；本課Python資料演算法與DuckDB查詢各有可執行入口。

## 更新欄位仍可能移動

若讀取期間來源把排序鍵更新到游標之前，或使用不可靠的更新時間，複合游標仍可能遺漏。對同一個快照的穩定排序，與對持續變動資料庫的完整增量，是不同承諾。

## 雙重驗收

先測同時間、不同鍵的分頁是否正確；再測來源變動、固定上界與重讀。游標值也必須與目前查詢的條件及排序方向相容，不能把另一個篩選條件產生的token直接拿來續讀。

實驗資料按3、1、2輸入，但結果會按時間與鍵排序；游標在1之後應取得2、3。這說明排序規則，而不是宣稱輸入順序就是來源權威順序。

## 專案中的實作

節錄 `examples/contracts.py` 的 `cursor_page`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def cursor_page(rows,after=None,limit=2):
    if type(limit) is not int or limit<=0:raise ValueError('Positive page size required')
    ordered=sorted(rows,key=lambda r:(utc(r['updated_at']),r['id']))
    if after is not None:ordered=[r for r in ordered if (utc(r['updated_at']),r['id'])>(utc(after[0]),after[1])]
    return ordered[:limit]
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大更新時間與主鍵的複合游標圖解"><img src="assets/figures/23.svg" alt="更新時間與主鍵的複合游標：辨認本課序列範圍不包含after而包含through，再與日期半開區間對照，避免把兩個契約混成同一條件。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「更新時間與主鍵的複合游標」讀圖：辨認本課序列範圍不包含after而包含through，再與日期半開區間對照，避免把兩個契約混成同一條件。請用圖回答：同一時間三列分兩頁讀取時，時間與鍵的複合游標解決了哪個問題？</p></div>

## 自我檢查與解析

**題目：**同一時間三列分兩頁讀取時，時間與鍵的複合游標解決了哪個問題？

<details><summary>展開解析</summary><p>它建立同時間列的完整順序，避免只用時間嚴格大於而漏掉剩餘列；但仍需另外處理來源在擷取中的變動。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab23.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab23.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
