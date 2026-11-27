# 去重、來源版本與衝突拒絕

去重不是刪除長得一樣的列，而是依契約選擇一份事實。

## 先區分事件鍵與業務鍵

同一個order_id可以有多個合法更新事件，但同一event_id在本課代表同一份事件。重送同事件可以去掉重複，最新訂單狀態則要按來源序列選勝出版本。把兩種鍵混用，會把更新歷史當成重複垃圾刪掉。

## 勝出必須形成完整順序

使用ROW_NUMBER按來源版本倒序選第一筆時，如果相同版本還有不同payload，必須決定拒絕還是有更高階的權威欄位。任意加一個檔案行號作同值處理，只會讓結果穩定但不一定正確。

本課contracts.deduplicate對相同鍵、相同seq但內容不同的列直接失敗。它是教學用的明確政策，不是宣稱所有來源都能用同一個seq欄位；真實來源可能需要分區位置、更新版本或其他比較方法。

## 驗證冪等

相同輸入重跑後，輸出集合與總額應保持不變。再加入較舊版本、較新版本和衝突版本，分別驗證忽略、更新與拒絕。這些反例能證明程式沒有只依輸入排列碰巧得到正確結果。

最後保存被淘汰版本或至少可追溯的來源證據。若只有最終結果而沒有理由，日後很難解釋某一筆資料為何不在報表裡。

## 可執行查詢

以下是下載包 `queries/22.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH source(id,seq,value) AS (VALUES (1,10,'old'),(1,11,'new'),(2,9,'other')),
ranked AS (SELECT *,ROW_NUMBER() OVER (PARTITION BY id ORDER BY seq DESC) AS winner FROM source)
SELECT id,seq,value FROM ranked WHERE winner=1 ORDER BY id;
```

## 專案中的實作

節錄 `examples/contracts.py` 的 `deduplicate`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def deduplicate(rows):
    """Greatest source sequence wins; conflicting equal-sequence payloads fail."""
    winners={}
    for row in rows:
        key=row['id'];old=winners.get(key)
        if old and row['seq']==old['seq'] and row!=old:raise ValueError('Ambiguous winner')
        if old is None or row['seq']>old['seq']:winners[key]=dict(row)
    return [winners[k] for k in sorted(winners)]
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大去重、來源版本與衝突拒絕圖解"><img src="assets/figures/22.svg" alt="去重、來源版本與衝突拒絕：對每個業務鍵依來源序列選最新版本，另辨認相同版本不同內容的情況，不能用讀取順序冒充權威。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「去重、來源版本與衝突拒絕」讀圖：對每個業務鍵依來源序列選最新版本，另辨認相同版本不同內容的情況，不能用讀取順序冒充權威。請用圖回答：同一訂單、同一來源版本卻有兩份不同金額時，直接取最後讀到的那筆有何問題？</p></div>

## 自我檢查與解析

**題目：**同一訂單、同一來源版本卻有兩份不同金額時，直接取最後讀到的那筆有何問題？

<details><summary>展開解析</summary><p>讀取排列不一定代表權威版本。除非契約明定更高階規則，應拒絕衝突並追查來源，不能以穩定排序冒充正確決策。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab22.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab22.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/functions/window_functions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
