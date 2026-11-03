# 多租戶與資料 ACL：每次呼叫都要隔離

把主體綁在伺服器端，讓列舉、搜尋、讀取、預覽與提交遵守同一條權限路徑。

## 工具可見與資料可見不同

兩個使用者都可能看得到 get_ticket 工具，但只能讀自己租戶的資料。Host 隱藏工具只能限制可用能力；資料隔離仍需在 Server 和資料層執行。若查詢只用 ticket_id 而沒有 tenant 條件，同名工單便可能跨租戶洩漏。

本課刻意讓 alpha 與 beta 都有 T1，確保測試能抓出這個問題。只使用全球唯一而且永遠不重複的測試 ID，容易掩蓋查詢漏掉租戶條件的錯誤。

## Principal 從可信環境取得

Server 的 Principal 包含 issuer、subject、tenant 與 scopes。正式 HTTP 環境由驗證 Token 產生；程序內測試則注入明確的 fixture。模型只提供 query 或 ticket_id，不能提供「我現在是 alpha 管理員」來改變身分。

如果產品允許使用者切換租戶，也要由受信任的 Host／授權流程確認其 membership，再產生本次有效主體。不能把 header 或模型欄位直接當成 membership 證據。

## 每個介面都要遵守同一邊界

搜尋前先套 tenant filter，資源讀取再驗證一次，預覽與提交也重新檢查權限。Prompt 補全、文件標題、工具列表與快取同樣可能洩漏資料。你不能只保護正文讀取，卻讓未授權使用者透過補全列出所有機密文件名。

| 路徑 | 必須保留的條件 |
| --- | --- |
| 搜尋 | 租戶、資料可見性、結果上限 |
| 讀取 | 穩定 ID、同一主體的 ACL |
| 快取 | 主體與權限修訂隔離 |
| 預覽 | 寫入資格與資源版本 |
| 提交 | 目前權限、預覽綁定與審核 |

## 錯誤也要隔離

對未授權資源，可以使用一致的不可用訊息，避免讓使用者從「不存在」與「無權限」差異判斷他人資料是否存在。內部稽核仍可記錄精確分類，但不需要將所有細節傳給模型。

## 練習與解答

讓 alpha 搜尋 beta 的機密文字，應得到空集合；beta 搜同一文字則可以命中。再把 scope 移除，應得到權限拒絕，而非成功空集合。這兩種結果語意不同：前者是已授權搜尋中的無命中，後者是根本不允許執行這項能力。

## 可執行範例

在 `examples` 目錄執行 `python 21_tenant_acl.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:21_tenant_acl.py -->

## 官方閱讀

- [Server authorization](https://py.sdk.modelcontextprotocol.io/run/authorization/)
- [MCP 安全邊界](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
