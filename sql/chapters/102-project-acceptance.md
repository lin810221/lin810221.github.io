# DataHarbor：完整交付與乾淨環境驗收

將可以執行的程式、資料、說明與測試一起交給下一位使用者。

## 從零重建

把完整程式包解壓到新目錄，以requirements建立隔離環境，先列出36個實驗，再執行測試和workflow。不要只在作者目錄執行成功；漏掉queries或data目錄，通常會在乾淨環境立刻暴露。

```powershell
python -m pip install -r requirements.txt
python -m unittest test_examples -v
python workflow.py --workspace .runtime/acceptance
python workflow.py --workspace .runtime/acceptance
```

兩次workflow完成後，應維持位置8、存活4筆與付款11500，且最後公開manifest一致。程式、SQL與資料都在包內，不依賴外部API、模型下載或公司資料庫。

## 交付資料

保存資料字典、版本、執行方式、預期結果、故障恢復與已知限制。DuckDB原生資料檔、Parquet與manifest分別有自己的格式及模型版本，升級時按這些邊界驗證。

## 明確的範圍

本課完成本機單寫入工作區、合成來源契約和可恢復發布。外部來源CDC、物件儲存、服務身分、分散式協調及正式負載不是這個小程式已自動完成的能力；後續整合時需按相同責任逐項驗收。

先能完整交接這一條流程，再擴展工具，會比只留下幾張成功截圖更容易長期維護。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/34.svg" target="_blank" rel="noopener" aria-label="放大DataHarbor：完整交付與乾淨環境驗收圖解"><img src="assets/figures/34.svg" alt="DataHarbor：完整交付與乾淨環境驗收：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DataHarbor：完整交付與乾淨環境驗收」讀圖：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。請用圖回答：完整交付為什麼要在解壓後的新目錄重跑？</p></div>

## 自我檢查與解析

**題目：**完整交付為什麼要在解壓後的新目錄重跑？

<details><summary>展開解析</summary><p>可以發現漏包的SQL、fixture、依賴與隱藏的工作目錄依賴，證明成果不是只在作者機器的既有狀態下可用。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab34.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab34.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/clients/python/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
