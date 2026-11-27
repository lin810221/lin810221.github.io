# WHERE、範圍與字串條件

讓條件寫出真正的業務集合，再檢查空值與邊界。

## 先處理運算優先序

`AND`與 `OR`混用時，以括號表達業務意圖。例如「已付款，而且地區屬北部或南部」需要先把兩個地區條件組合；否則可能把某個地區的取消訂單一起納入。不要讓讀者靠記憶猜運算優先序。

`BETWEEN`一般包含兩端。時間區間則常採包含起點、不包含終點，避免相鄰批次在午夜重複計入。每次列出邊界值，包含剛好在起點、終點與空值的資料，會比只拿中間值測試更有效。

## IN、LIKE與轉型

`IN`表達列舉集合，`LIKE`使用萬用字元；字元大小寫、定序和Unicode行為可能因產品與設定不同。若把索引欄位包進函數再比較，也可能改變可用的存取路徑，因此正確語意與效能應一起量測。

不要用字串拼接組成來自使用者的值條件。參數綁定會在寫入與安全章完整實作；欄位名稱和排序方向則需白名單，因為值參數不能任意替代SQL結構。

## 本課的付款篩選

查詢先保留已付款訂單，再按金額分成large或small。判定門檻使用美分，不是美元；4000代表40美元。將來源單位放回條件後，才知道查詢究竟選中了哪個集合。

## 可執行查詢

以下是下載包 `queries/05.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
SELECT order_id, CASE WHEN amount_cents >= 4000 THEN 'large' ELSE 'small' END AS band
FROM orders
WHERE status = 'paid' AND amount_cents BETWEEN 1000 AND 5000
ORDER BY order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大WHERE、範圍與字串條件圖解"><img src="assets/figures/05.svg" alt="WHERE、範圍與字串條件：先找哪些訂單通過付款條件，再用4000美分門檻分類，別把篩選與輸出標籤混為一件事。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「WHERE、範圍與字串條件」讀圖：先找哪些訂單通過付款條件，再用4000美分門檻分類，別把篩選與輸出標籤混為一件事。請用圖回答：時間批次的終點若也使用包含條件，相鄰批次會有什麼風險？</p></div>

## 自我檢查與解析

**題目：**時間批次的終點若也使用包含條件，相鄰批次會有什麼風險？

<details><summary>展開解析</summary><p>剛好落在共同邊界的資料可能被重複讀取。常用半開區間並搭配明確的游標及去重策略，而非只依目測結果。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab05.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab05.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/queries.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
