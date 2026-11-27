# DataHarbor：版本產物與可恢復發布

將資料庫提交和檔案公開分成兩個可檢查階段。

## 先有產物，再有公開指標

程式為待發布批次建立版本目錄，寫入Parquet，回讀筆數與付款總額，計算SHA-256，再產生manifest。驗證通過後，才替換current.json。讀取者因此依指標找到一份已完成的版本，不用掃描半成品目錄。

## 中間失敗怎麼恢復

若資料庫已提交但還沒發布，outbox仍是pending；下一次處理先完成它，再接新批次。若指標已替換但標記尚未更新，重新驗證既有版本後完成標記，不重新套用訂單變更。

## 不可變與驗證的限制

已完成版本不原地改寫。雜湊用來辨認檔案是否與manifest一致，不能代替可信發布者身分，也不能證明來源業務資料本來沒有錯。模型版本與品質檢查仍需要自己的責任。

## 儲存系統差異

本機原子rename只保護適用檔案系統中的指標替換。搬到S3等物件儲存，要按服務提供的條件寫入與版本機制重新設計，不能假設所有系統都有同樣rename語意。課程不呼叫外部物件儲存。

這裡驗收的是程序中斷恢復與完整讀回，不將結果擴大成已測過所有斷電、硬體損壞或分散式故障。

## 專案中的實作

節錄 `examples/pipeline.py` 的 `publish_pending`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def publish_pending(connection,workspace,fault=None):
    pending=connection.execute('SELECT batch_id,payload_hash,through_seq,version_id FROM publication_outbox WHERE NOT published ORDER BY through_seq,batch_id').fetchall()
    if len(pending)>1:raise RuntimeError('Recover pending publication before ingesting another batch')
    for batch_id,payload_hash,through_seq,version_id in pending:
        current=connection.execute('SELECT last_seq FROM cursor_state WHERE singleton=1').fetchone()[0]
        if through_seq!=current:raise RuntimeError('Publication checkpoint does not match current state')
        folder=workspace/'versions'/version_id;folder.mkdir(parents=True,exist_ok=True)
        manifest_path=folder/'manifest.json'
        if manifest_path.exists():
            manifest=json.loads(manifest_path.read_text(encoding='utf-8'));validate_snapshot(workspace,manifest)
            if manifest['version_id']!=version_id or manifest['through_seq']!=through_seq:raise ValueError('Manifest identity mismatch')
        else:
            parquet=folder/'orders.parquet';temporary=folder/(uuid.uuid4().hex+'.parquet.tmp')
            connection.execute("COPY (SELECT * FROM live_orders ORDER BY order_id) TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",[str(temporary)])
            os.replace(temporary,parquet)
            count,total=connection.execute("SELECT COUNT(*),COALESCE(SUM(amount_cents) FILTER (WHERE status='paid'),0) FROM live_orders").fetchone()
            manifest={'model_version':MODEL_VERSION,'version_id':version_id,'through_seq':through_seq,'rows':count,'paid_cents':int(total),'sha256':file_digest(parquet),'file':parquet.relative_to(workspace).as_posix()}
            validate_snapshot(workspace,manifest);atomic_json(manifest_path,manifest)
        atomic_json(workspace/'current.json',manifest)
        if fault=='after_pointer':raise RuntimeError('Injected crash after pointer publication')
        connection.execute('UPDATE publication_outbox SET published=TRUE WHERE batch_id=?',[batch_id])
    return len(pending)
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/34.svg" target="_blank" rel="noopener" aria-label="放大DataHarbor：版本產物與可恢復發布圖解"><img src="assets/figures/34.svg" alt="DataHarbor：版本產物與可恢復發布：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DataHarbor：版本產物與可恢復發布」讀圖：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。請用圖回答：為什麼先公開current.json再補寫Parquet會有問題？</p></div>

## 自我檢查與解析

**題目：**為什麼先公開current.json再補寫Parquet會有問題？

<details><summary>展開解析</summary><p>讀取者可能立刻依指標讀到不存在或未完成的產物。應先完成並驗證不可變產物，再公開指標，並保留發布恢復紀錄。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab34.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab34.py -->

## 官方來源

[本單元對應文件](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
