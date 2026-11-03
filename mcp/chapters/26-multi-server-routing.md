# 多伺服器整合與工具命名空間

處理同名工具、連線清理、權限差異與動態工具清單。

## 同名工具非常常見

兩個 Server 都可能提供 search、get 或 list。若只把全部工具放進同一字典，後加入的工具可能覆蓋前一個。模型呼叫 search 時，你也無法確定原本指哪個資料來源。Host 必須建立命名空間與可逆路由映射。

本課使用 `notes__search_notes` 這類 Host 內名稱，映射到特定 Client 與 Server 原始工具名。這只是本課策略，不是 MCP 規範要求所有 Host 都使用相同字串格式。不同模型 API 對名稱長度與字元的限制也可能不同。

## 不要從字串猜路由

若原始工具名本來就含有分隔符號，直接 split 可能出錯。更可靠的方式是保存明確的 `exposed_name → client, original_name, schema_revision` 映射，並在送給模型前驗證 exposed name 唯一。這個映射屬於 Host 的可信控制資料。

工具清單重新載入時，應建立新修訂；已在進行中的呼叫繼續綁定原本版本，或依政策拒絕再探索。不要在模型產生呼叫後，把相同名稱悄悄改指到另一個 Server。

## 每個連線有自己的責任

使用 `AsyncExitStack` 可以集中管理多個 Client，確保離開時全部關閉。正式 Host 也要考慮部分 Server 失敗的情況：必要工具無法連線時阻止相關任務，選用工具失敗則可以保留其他能力，同時明確揭露缺少的資料來源。

連線的 Token、tenant、允許工具與結果預算應各自保存。不能因為兩個 Server 的名稱相似，就把 A 的權限或快取套用到 B。使用同一 OAuth subject，也不代表對不同資源有相同 scope。

## 工具很多時先做選擇

把數千個工具描述全部送給模型，會增加 token 成本與選錯機率。可先按使用者授權、任務領域與能力縮小候選，再讓模型看到必要的工具集合。工具搜尋本身也應有可追蹤的來源與權限邊界，不應成為發現未授權能力的側門。

## 練習與解答

執行範例，兩個 Server 的 search_notes 應同時存在於 routes 中，並能明確呼叫 notes 那一個。再把其中一個名稱改成與既有名稱衝突，合理策略是拒絕配置或使用無碰撞名稱，而不是悄悄採最後註冊者。

## 可執行範例

在 `examples` 目錄執行 `python 16_multi_server.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:16_multi_server.py -->

## 官方閱讀

- [SDK 多伺服器](https://py.sdk.modelcontextprotocol.io/client/session-groups/)
- [Client best practices](https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices)
