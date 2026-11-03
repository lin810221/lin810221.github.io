# 可觀測性與稽核：從對話追到執行事實

串起模型提案、工具呼叫、上游請求與交易收據，同時控制敏感資訊。

## Trace、Log、Metric 與 Audit 不同

Trace 描述跨服務因果與時間，Log 記錄離散事件，Metric 聚合延遲與錯誤，Audit 則保存誰在什麼條件下做了哪個重要操作。它們可以共用關聯 ID，但保存期限、權限與不可變要求可能不同。

例如一個工具有三次上游重試，Trace 可以呈現耗時；Metric 計算 transient error 比率；Audit 則只在交易確實完成時記錄結案事實。不能把「開始嘗試」日誌當成已完成的稽核紀錄。

## 定義可跨層關聯的識別

Host 的任務 ID、模型 call_id、MCP request ID、預覽 ID 與冪等鍵摘要用途不同。你可以記錄它們的映射，但不要強行用同一個字串代替全部。特別是冪等鍵必須在重送時保持穩定，請求關聯 ID 則可以每次不同。

原始 Token、完整工具參數與文件內容通常不應進入一般日誌。使用必要識別、受控錯誤代碼與資料量，讓維運能定位問題而不需要取得完整私人對話。

## 應量測的基本指標

| 指標 | 能協助回答的問題 |
| --- | --- |
| discovery／call 延遲 | 慢在探索還是執行 |
| 工具錯誤與協定錯誤比率 | 業務拒絕還是連線故障 |
| 取消與 deadline 耗盡 | 任務是否超出合理時間 |
| 結果大小與工具數 | 上下文是否被過量資料塞滿 |
| 交易與重送收據數 | 重試是否重複產生效果 |

平均值會掩蓋長尾，可觀察 p50、p95 與 p99，並按工具和租戶等合適維度分類。Metric labels 不應包含無限變化的 query、Token 或整段工具參數，否則會造成高基數與資料外洩。

## SDK tracing 與自有業務 span

Python SDK 提供 OpenTelemetry 整合能力，但你仍需配置 exporter、採樣、服務識別與資料政策。協定 span 可以看請求，領域 span 則說明資料庫或上游操作。教材示範不啟用遠端 telemetry exporter，不會把你的學習內容傳出。

## 練習與解答

為一次「預覽、核准、提交、重送」畫出事件。預期只有一次 committed audit，但可以有兩次提交請求與一次 receipt replay。若監控只計算 HTTP 200 次數，就無法區分這些情況，也可能把 is_error 結果當成成功業務。

## 官方閱讀

- [SDK OpenTelemetry](https://py.sdk.modelcontextprotocol.io/run/opentelemetry/)
- [Context 與進度](https://py.sdk.modelcontextprotocol.io/handlers/progress/)
- [OpenTelemetry 概念](https://opentelemetry.io/docs/concepts/)
