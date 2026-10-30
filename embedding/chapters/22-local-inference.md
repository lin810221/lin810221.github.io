## 本機模型帶來什麼

本機推論可以自行管理權重、硬體與資料流，但仍有套件、授權、記憶體、冷啟動和維護成本。初次模型下載需要網路與磁碟；權重已完整下載後，才可在合適環境離線使用。

只寫「使用本機模型」不代表沒有資料或供應鏈責任。保存模型卡、revision 和實際 recipe，才能重建相同表示。[SentenceTransformer 類別](https://sbert.net/docs/package_reference/sentence_transformer/model.html)

## 範例的三種模式

預設只印準備方式，不匯入重型套件。`--model-path` 使用已存在模型資料夾並設定 `local_files_only=True`；`--download-model` 則需同時提供固定 revision，明確允許下載。

<!-- example:19_local_model.py -->

選配執行前，在自己的虛擬環境安裝相依套件。套件版本與模型 revision 一起記錄，因為 tokenizer 或推論實作變更也可能影響結果。

## Query 與文件輸入

程式分別呼叫 encode_query 和 encode_document，並提供 `--query-prefix`、`--document-prefix` 覆寫選項。若模型本身已設定正確 prompt，可沿用；若模型卡要求額外前綴，就明確傳入，避免漏加或重複。

```powershell
python 19_local_model.py --model-path "D:\Models\your-model"
# 若模型卡要求 query: 與 passage:，再依其規範加對應前綴
python 19_local_model.py --model-path "D:\Models\your-model" --query-prefix "query: " --document-prefix "passage: "
```

這些是操作模板，需自行準備真正模型。教材建置不會下載模型，也不會把沒有權重時的結果冒充成語意輸出。

## 硬體與批次

CPU、GPU、dtype 與 batch size 影響吞吐與記憶體。batch 加大不一定無限加速，長短輸入混合還可能被 padding 拖慢。測試真實長度分布、預熱前後與 p95，而非只測同長短句。

對大量文件保存索引；不要每次 query 都重新算所有文件。encoder 通常以推論模式執行，確認 dropout 關閉並採適當無梯度計算，避免非預期差異。

## 固定版本還要記錄哪些環境

保存 Python、框架、tokenizer、device、dtype、batch 與最大長度。不同硬體的浮點細微差異不一定是錯誤，但若排序邊界很接近，就可能影響 top-k。用容許誤差和任務指標驗收，不要求所有浮點位元完全相同。

模型檔案完整不代表配套 processor 正確。檢查 prompts、pooling 和 normalization 模組是否隨載入保留；使用裸 backbone 與完整 Sentence Transformer 時尤其需要對照。

## 練習與參考答案

**題目：**模型路徑存在，但本機缺 tokenizer 檔，程式應偷偷上網補嗎？

**參考答案：**若選擇離線模式就應明確失敗，提示模型資料不完整。使用者可在允許下載的環境補齊，再重新固定與驗證；不能讓「離線」選項悄悄失效。
