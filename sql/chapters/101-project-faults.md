# DataHarbor：注入失敗與恢復演練

故意中斷，才知道哪一層真的可以恢復。

## 三個故障時點

before_commit在資料庫交易內失敗，資料、來源位置和outbox都回滾。after_commit在提交後、檔案公開前失敗，留下pending工作。after_pointer在指標替換後失敗，產物已可讀，但outbox尚待完成。

```powershell
# 使用新的測試工作區，故意得到非零結束狀態
python dataharbor.py --workspace .runtime/fault-demo --batch data/batch-001.json --fault after_commit
# 相同批次重跑，恢復後驗證公開結果
python dataharbor.py --workspace .runtime/fault-demo --batch data/batch-001.json --show
```

## 驗收不能只期待錯誤

在提交前失敗，確認資料與游標都沒有前進；提交後失敗，確認下次先恢復發布；指標後失敗，確認重跑不改寫成另一個版本。這些都由下載包測試讀回實際資料庫與檔案完成。

## 其他反例

再測範圍缺口、同識別衝突、負金額、無時區時間與損壞Parquet。輸入失敗和暫時執行失敗應走不同處理路徑，不把所有例外都改成「再試一次」。

最後確認鎖已釋放、工作區可以重新開啟、目前快照符合契約。正式恢復演練還需要更多部署與儲存條件，本課只對實際測試的本機邊界作結論。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/34.svg" target="_blank" rel="noopener" aria-label="放大DataHarbor：注入失敗與恢復演練圖解"><img src="assets/figures/34.svg" alt="DataHarbor：注入失敗與恢復演練：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DataHarbor：注入失敗與恢復演練」讀圖：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。請用圖回答：after_pointer故障後，重新執行為何不應再次增加付款金額？</p></div>

## 自我檢查與解析

**題目：**after_pointer故障後，重新執行為何不應再次增加付款金額？

<details><summary>展開解析</summary><p>訂單變更與來源位置早已提交；恢復只需驗證既有產物並完成發布標記，不能再次套用同一批業務副作用。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab34.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab34.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/statements/transactions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
