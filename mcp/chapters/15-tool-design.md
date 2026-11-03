# 工具命名、描述與 annotations

讓工具容易被正確選用，同時維持可審查的業務邊界。

## 名稱要能穩定路由

工具名稱是 API 識別碼，title 是 UI 標籤，description 是用途說明。不要用一段中文標題直接當跨供應商路由鍵，也不要在模型回傳的名稱前後任意補字再猜原始工具。本課使用簡單的 snake_case 名稱，Host 另外保存伺服器與原始名稱的映射。

名稱要反映操作，例如 `search_notes`、`get_ticket`、`preview_close_ticket`、`close_ticket`。若工具叫 `manage` 且有任意 action 和 payload，模型較難選擇，權限也不容易拆分。具體工具通常比無邊界萬用工具更容易測試與審核。

## 描述要交代用途與條件

好的描述包含它解決什麼問題、必要識別資訊、回傳什麼，以及重要限制。像「讀取指定工單的狀態；僅限呼叫者租戶；未知工單回傳失敗」，比「最強工單管理工具」有用。描述中的祕密、內部路徑和不必要資料會被帶進模型上下文，不應隨意加入。

```text
不清楚：Do anything with tickets.
較清楚：Read a ticket by its stable identifier. Returns status and version.
有條件：Close an approved, unexpired preview using an idempotency key.
```

描述也不能要求模型忽略使用者或上層指令；來自第三方 Server 的工具描述屬於外部資料，需要 Host 的信任與變更管理。

## annotations 是提示，不是防線

`readOnlyHint` 提示是否唯讀，`destructiveHint` 提示破壞性，`idempotentHint` 提示重複呼叫的效果，`openWorldHint` 提示是否與開放外部世界互動。Python 欄位採 snake_case，線上名稱則依規範序列化。

這些都是 Server 提供的資訊，不能取代實際授權、審核或交易設計。將一個會寫入資料的函式標成 read-only 不會讓它變成唯讀；將沒有冪等保證的付款標成 idempotent，也不會阻止重複扣款。Host 應根據經審查的政策決定執行權限。

## 工具粒度以可驗證交易為基準

過大工具難以限制副作用，過小工具則可能讓模型一次任務要做很多不可靠步驟。適合的邊界是「一個可說明、可授權、可驗證的業務動作」。例如結案一次應在 Server 交易中處理狀態、版本、收據與稽核，不應拆成四個由模型自行排列的寫入工具。

## 練習與解答

為 preview 與 commit 各寫一段描述。preview 可能會保存待審核紀錄，因此不應一律標成唯讀；commit 可以具有冪等行為，但仍屬有副作用操作。解答要同時檢查實作與 annotations，避免只根據人類名稱做分類。

## 官方閱讀

- [Tool annotations](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [SDK 工具定義](https://py.sdk.modelcontextprotocol.io/servers/tools/)
