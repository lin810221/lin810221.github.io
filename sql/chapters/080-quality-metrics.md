# 完整率、唯一率與空分母

品質指標必須明定樣本集合，不能把空資料誤判成百分之百正常。

## 完整率的正式定義

本課以「每列所有必要欄位皆非空」判定該列完整。令 $N$ 為列數，$N_{valid}$ 為完整列數，當 $N>0$：

$$C=\frac{N_{valid}}{N}.$$

例如三列中兩列金額已知，對應完整率為三分之二。若不同欄位要各自計算，應另外定義欄位完整率，不把兩種分母混用。空表時本課回傳未定義值，並另顯示列數為零。

## 唯一率的正式定義

令 $K$ 為鍵非空的列數，$D$ 為其中不重複鍵數，當 $K>0$：

$$U=\frac{D}{K}.$$

已知鍵為1、1、2時，唯一率是三分之二。空鍵不會因被排除在這個分母之外就變成合法；它由完整性規則另行攔截。若全部鍵都缺少，唯一率亦不應回傳百分之百。

## 指標不是單一通行證

高比例可能仍掩蓋關鍵訂單錯誤，小樣本也可能完全沒有代表性。請同時顯示分子、分母、範圍與嚴重度。唯一性和完整性也不能證明金額與日期的業務意義正確，仍需對帳與來源契約。

## 可執行查詢

以下是下載包 `queries/27.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
WITH raw(id,amount) AS (VALUES (1,10),(1,10),(2,NULL)),
counts AS (SELECT COUNT(*) AS total,COUNT(amount) AS present,COUNT(DISTINCT id) AS unique_keys FROM raw)
SELECT total,present,unique_keys,present*1.0/NULLIF(total,0) AS completeness FROM counts;
```

## 專案中的實作

節錄 `examples/contracts.py` 的 `quality`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def quality(rows,required=('id','amount_cents')):
    total=len(rows);missing=sum(any(r.get(k) is None for k in required) for r in rows)
    ids=[r.get('id') for r in rows if r.get('id') is not None]
    duplicates=sum(n-1 for n in Counter(ids).values())
    return {'rows':total,'missing_rows':missing,'known_keys':len(ids),'distinct_keys':len(set(ids)),'duplicate_excess':duplicates,
            'completeness':None if not total else (total-missing)/total,
            'uniqueness':None if not ids else len(set(ids))/len(ids)}
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大完整率、唯一率與空分母圖解"><img src="assets/figures/27.svg" alt="完整率、唯一率與空分母：逐列數完整欄位，再對已知鍵算不同鍵數；看見缺值與重複是不同責任，空分母需另行回報。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「完整率、唯一率與空分母」讀圖：逐列數完整欄位，再對已知鍵算不同鍵數；看見缺值與重複是不同責任，空分母需另行回報。請用圖回答：空資料表沒有發現缺值，為何本課不直接回報完整率100%？</p></div>

## 自我檢查與解析

**題目：**空資料表沒有發現缺值，為何本課不直接回報完整率100%？

<details><summary>展開解析</summary><p>因為比例沒有可用分母，且可能代表來源完全沒到。應回報列數為零與比例未定義，再按來源完成契約判斷是否正常。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab27.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab27.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
