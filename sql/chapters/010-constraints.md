# 主鍵、外鍵與CHECK約束

用資料庫保護不可違反的條件，再把業務驗證放在正確邊界。

## 約束各自保護什麼

主鍵要求唯一且不為空；外鍵限制關聯值必須存在；`NOT NULL`限制缺值；`CHECK`限制資料列內可表達的條件。本課的訂單不能指向不存在的客戶，狀態只能是允許的集合，金額不能小於零。

約束不是前端驗證的替代，也不是只靠前端就可以省略。不同程式入口、批次工作和人工SQL都可能寫入資料；共用的不可違反規則應盡量落在資料庫，再在應用端提供比較好理解的錯誤訊息。

## 空值與CHECK的交互作用

`CHECK(amount_cents >= 0)`本身不等同於 `NOT NULL`。空值可能使比較結果為unknown，並未直接成為false。因此欄位若不得缺值，還要明確宣告 `NOT NULL`。唯一約束對空值的預設處理也有產品與選項差異，不可憑一個資料庫的行為推論全部。

## 在失敗後驗證資料

離線實驗分別嘗試重複訂單鍵、不存在的客戶與負金額，三者都應被拒絕，訂單仍是五筆。測試不能只看有沒有印出錯誤；還要確認資料沒有改變。跨列或跨表的複雜規則，例如退款總額是否超過付款，則需要另外的交易與對帳設計，不能假裝單列CHECK能完成所有責任。

## 專案中的實作

節錄 `examples/fixtures.py` 的 `seed`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def seed(connection):
    connection.execute(SCHEMA)
    connection.executemany('INSERT INTO customers VALUES (?,?,?,?)',[(1,'Ada','north','ada@example.test'),(2,'Bo','south',None),(3,'Cy','north','cy@example.test'),(4,'Dee','east',None)])
    connection.executemany('INSERT INTO orders VALUES (?,?,?,?,?)',[(101,1,'2026-11-01T09:00:00Z','paid',3000),(102,1,'2026-11-02T09:00:00Z','paid',5000),(103,2,'2026-11-02T09:00:00Z','cancelled',2000),(104,2,'2026-11-03T09:00:00Z','paid',4000),(105,3,'2026-11-03T09:00:00Z','paid',1000)])
    connection.executemany('INSERT INTO items VALUES (?,?,?,?,?)',[(1,101,'book',2,1500),(2,102,'pen',3,1000),(3,102,'notebook',1,2000),(4,103,'book',2,1000),(5,104,'mouse',2,2000),(6,105,'pen',1,1000)])
    connection.executemany('INSERT INTO refunds VALUES (?,?,?)',[(11,101,500),(12,102,1000),(13,102,500)])
    connection.executemany('INSERT INTO staff VALUES (?,?,?)',[(1,None,'lead'),(2,1,'engineering'),(3,2,'data'),(4,2,'web'),(5,1,'sales')])
    connection.executemany('INSERT INTO readings VALUES (?,?,?)',[(1,'2026-11-01',10),(2,'2026-11-02',None),(3,'2026-11-03',30),(4,'2026-11-04',40)])
    return connection
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大主鍵、外鍵與CHECK約束圖解"><img src="assets/figures/04.svg" alt="主鍵、外鍵與CHECK約束：從唯一客戶鍵走向訂單外鍵，再檢查重複鍵、不存在的關聯與非法欄位值會在哪裡被拒絕。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「主鍵、外鍵與CHECK約束」讀圖：從唯一客戶鍵走向訂單外鍵，再檢查重複鍵、不存在的關聯與非法欄位值會在哪裡被拒絕。請用圖回答：CHECK限制金額非負後，是否就不需要NOT NULL？</p></div>

## 自我檢查與解析

**題目：**CHECK限制金額非負後，是否就不需要NOT NULL？

<details><summary>展開解析</summary><p>仍可能需要。空值與三值邏輯使CHECK的unknown不等於false；若業務要求必填，應同時宣告NOT NULL。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab04.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab04.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
