# 多檔schema演進與版本manifest

把可相容的變動和危險的自動合併分開。

## 名稱對齊不會修正語意

多個檔案的欄位順序可能不同，依名稱讀取有助避免位置錯配；但同名欄位若換了單位或精度，名稱對齊仍會產生錯誤。缺欄位補空值也需要下游明確接受，不能當成無條件相容。

## 保存一份發布清單

manifest記錄檔案、schema或模型版本、來源範圍、筆數、必要總額與雜湊。讀取者依這份清單取得一致版本，而不是每次猜某個目錄下哪幾個檔案才屬於同一批。

DataHarbor的manifest保存目前版本、最後處理序列、訂單筆數、付款美分總額與Parquet的SHA-256。回讀會再次驗證檔案雜湊與簡單對帳；這能發現損壞，不是驗證未受信任發布者身分的數位簽章。

## 演進的驗收

新增欄位可先讓舊讀取者忽略，再升級模型；改型別或單位則可能需要新版本產物與回補。無論哪一種，都先用舊資料與新資料混合測試，確認不會在某個分割才觸發錯誤。

本課的已發布版本不原地改寫。若模型定義改變，建立新的版本或重建工作區，再以驗證過的指標切換，保留回復到上一個有效結果的方法。

## 專案中的實作

節錄 `examples/pipeline.py` 的 `validate_snapshot`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def validate_snapshot(workspace,manifest):
    if set(manifest)!={'model_version','version_id','through_seq','rows','paid_cents','sha256','file'} or manifest['model_version']!=MODEL_VERSION:raise ValueError('Invalid publication manifest')
    path=(Path(workspace)/manifest['file']).resolve();versions=(Path(workspace)/'versions').resolve()
    if not path.is_relative_to(versions) or path.name!='orders.parquet' or not path.is_file():raise ValueError('Invalid artifact path')
    if file_digest(path)!=manifest['sha256']:raise ValueError('Artifact checksum mismatch')
    with connect() as connection:
        count,total=connection.execute("SELECT COUNT(*),COALESCE(SUM(amount_cents) FILTER (WHERE status='paid'),0) FROM read_parquet(?)",[str(path)]).fetchone()
    if count!=manifest['rows'] or total!=manifest['paid_cents']:raise ValueError('Artifact reconciliation failed')
    return manifest
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/36.svg" target="_blank" rel="noopener" aria-label="放大多檔schema演進與版本manifest圖解"><img src="assets/figures/36.svg" alt="多檔schema演進與版本manifest：沿四種不同版本追蹤變動，再說明哪一組反例與恢復測試能證明語意在升級後仍成立。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「多檔schema演進與版本manifest」讀圖：沿四種不同版本追蹤變動，再說明哪一組反例與恢復測試能證明語意在升級後仍成立。請用圖回答：讓讀取器按欄位名稱合併檔案，是否能解決同名欄位由美元改成美分？</p></div>

## 自我檢查與解析

**題目：**讓讀取器按欄位名稱合併檔案，是否能解決同名欄位由美元改成美分？

<details><summary>展開解析</summary><p>不能。名稱對齊處理結構對應，無法推斷單位變更；需要模型版本、明確轉換與對帳。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab20.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab20.py -->

## 官方來源

[本單元對應文件](https://parquet.apache.org/docs/file-format/)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
