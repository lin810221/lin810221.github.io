## 你需要什麼

網頁閱讀不需要 Python、API Key 或開啟伺服器。若要執行程式，準備 Python 3.11 以上與一個終端機即可。這個課程的離線範例使用標準函式庫；`sqlite3` 是 Python 內建模組，適合本機教學。[Python sqlite3 文件](https://docs.python.org/3/library/sqlite3.html)

下載本章下方的完整範例包，解壓後保留整個 `examples` 目錄。編號程式會匯入 `rag_core.py`，也會讀取 `data/documents.json`，所以只下載單一 `.py` 檔不足以執行。Windows 可在該資料夾以檔案總管開啟終端機。

## 第一次執行

```powershell
python --version
python 01_first_rag.py
python 16_capstone.py "國內出差住宿費上限"
```

若電腦以 `py` 作為 Python 啟動器，可以把命令開頭換成 `py -3`。若你在整個網站原始碼根目錄，則使用 `python rag/examples/01_first_rag.py`。範例依自身位置尋找資料，不依賴終端機工作目錄。

<!-- example:01_first_rag.py -->

## 讀懂輸出，而非只看程式沒有報錯

`mode=offline_bm25_extractive` 表示 BM25 找片段、程式擷取原句。`answer` 應包含「提前三個工作日」，`citations` 應帶有文件 ID、版本、頁碼、原句，`context` 是實際使用的證據。這些欄位讓你能檢查答案從哪裡來。

如果使用「火星基地氧氣費率」作為問題，教材沒有相關資料，應得到 `insufficient_evidence`。這裡的拒答只是詞元覆蓋啟發式；真正語意不足仍要用測試集與生成評估確認，不能把這個閾值當作普遍保證。

## 先改一個變數觀察

打開 `data/documents.json`，找到 `leave` 文件，把特休規則改成另一個明確值，再執行一次。答案應跟著文件改變，而不需要改動回答程式中的固定答案。接著改回原值，以維持後續測試的基準。

教材有已失效的舊差旅規範、人資專用薪資資料與另一租戶資料。一般讀者查詢時，這些內容應在進入證據前被排除。資料不是越多越好，可見且適用才是使用條件。

## 執行檢查

```powershell
python -m unittest discover -s . -p test_examples.py -v
```

測試包含切塊邊界、租戶與角色、引用映射、指標算式、更新與刪除。測試預設離線，API 回應使用 fixture；它能確認程式行為，不能證明真實模型的回答品質。第 13、14 份程式只有加上 `--live` 才會呼叫外部服務。

## 常見問題與練習

`ModuleNotFoundError: rag_core` 通常表示少了解壓檔或搬移了單一程式；找不到 `documents.json` 則檢查 `data/` 是否完整。終端機中文字亂碼可設定 `$env:PYTHONUTF8="1"` 後重新執行。

**練習：**用「VPN-403」提問，確認答案引用 `it` 文件，再用不存在的錯誤碼比較。不要只確認終端機有印出任何字串；驗收還要確認片段、來源和結果狀態。
