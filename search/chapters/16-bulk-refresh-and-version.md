# Bulk、Refresh 與版本：寫入成功多久能搜尋

分開理解批次請求、單筆錯誤、可搜尋性與併發覆寫。

## Bulk 不是全有全無交易

Bulk 以 NDJSON 傳送多個 action。整個 HTTP 請求成功，裡面仍可能有 mapping conflict、版本衝突或資源不足。應檢查 errors 與每個 item，記錄業務 ID、錯誤類別與可重試性。只重送可重試的失敗項目，避免把已成功文件無條件重做。

## Refresh 與持久性不同

搜尋依讀取可見的 segment；寫入成功未必立即可被一般 search 找到。refresh 讓新變更可搜尋，並不等同 flush、備份或跨節點一致。`refresh=wait_for` 可等待正常 refresh，適合少量需要後續立即搜尋的操作；對每個小寫入強制 refresh 可能產生很多小 segment，增加成本。

## 併發寫入有兩種版本概念

業務 revision 應由來源管理。Elasticsearch 的 seq_no 與 primary_term 可作樂觀併發控制，避免用舊讀取結果覆蓋別人剛寫入的版本；它們不是跨引擎業務時間線。外部版本模式有其比較規則，採用前必須定義重送、相等版本與刪除事件的行為。

## 範例邊界

入口展示真正 SDK 產生的 action/body、Content-Type 與 refresh 參數。記錄節點是模擬回應，沒有逐筆引擎結果，不能作為 Bulk 全部成功的證據。正式匯入器需要受控服務驗證 item failures、退避、死信與最終來源對帳，並以文件數與抽樣內容確認。

## 可執行範例

先依 [範例說明](examples/README.md) 建立隔離環境，再於 `examples` 目錄執行 `python 08_bulk_refresh.py`。未加 `--live` 的入口都不連線遠端服務，也不下載模型。先讀輸出中的 mode 與限制，再解釋分數。

<!-- example:08_bulk_refresh.py -->

## 練習與解答

**請先嘗試：** Bulk 有 1000 筆，其中 3 筆 mapping error，是否直接全部重試直到成功？

<details><summary>展開解答與判斷依據</summary>

先解析每筆結果。mapping error 通常需修正資料或 schema，不會因重試自動好；暫時資源錯誤可依冪等與重試預算處理。輸出成功、失敗與待處理計數，保留失敗 ID，避免無限重試掩蓋缺資料。

</details>

## 官方文件與延伸閱讀

- [Elasticsearch 官方參考](https://www.elastic.co/docs/reference/elasticsearch)

[回到課程總覽](#overview) · [下載完整實作](examples.zip)
