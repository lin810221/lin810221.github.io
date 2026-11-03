# OAuth 授權流程：Client、資源伺服器與身分服務

理解登入、取得 Token、發現 metadata 與使用 scope 的責任分工。

## 三個角色不要混在一起

Client 代表應用要求存取；Authorization Server 負責登入、同意與簽發 Token；MCP Server 是 Resource Server，驗證每個請求是否可存取。MCP Server 可以與身分服務部署在相近位置，但兩種責任仍然不同。

協定的 HTTP 授權機制以 OAuth 2.1 相關要求為基礎。stdio 通常從受控環境取得必要憑證，並不要求照搬 HTTP 的整條登入流程。本課不自行編寫正式授權伺服器，而是示範資源端驗證與應用權限如何銜接。

## Client 如何找到身分服務

受保護資源 metadata 告訴 Client 應信任哪個 Authorization Server；身分服務 metadata 再提供授權及 Token 端點等資訊。Client 不應從任意工具結果抓一個「登入網址」就轉送祕密，發現流程本身也需要 issuer 與 URL 驗證。

目前規範包含 Client ID Metadata Documents 等註冊路線；Dynamic Client Registration 保留向後相容，但已列為棄用。正式整合應查看身分供應商與 Host 的支援，不能假設所有服務都使用同一種註冊機制。

## 一條典型互動路徑

```text
Client → MCP Server：受保護請求
Server → Client：401 與 metadata／scope 提示
Client → Authorization Server：登入與授權，使用 PKCE 等保護
Client ← Authorization Server：針對此資源的 Access Token
Client → MCP Server：Bearer Token
Server：驗證 Token、scope 與業務權限後才執行
```

resource 參數用來指定 Token 的目標資源，避免把原本給另一個 API 的 Token 拿到 MCP Server 使用。Token 有效與使用者對特定工單有權限，仍然是兩個檢查層次。

## Scope 與逐步要求權限

一開始只搜尋，就先要求必要的讀取 scope。當使用者需要寫入，再依正式流程取得相應權限，而不是一開始要求所有管理權限。401、403 與 insufficient_scope 的處理應符合協定和服務政策，不應把任何拒絕都變成重複登入。

重新登入也不一定能解決業務 ACL 拒絕。若使用者不屬於該租戶，Server 必須持續拒絕，不能因為模型多試幾次就接受另一個 tenant 參數。

## 練習與解答

把「登入頁、驗證 JWT、查工單租戶、刷新 Token」分配角色。參考答案：登入與簽發屬身分服務；JWT 與工單 ACL 屬資源 Server；刷新由 Client 配合身分服務處理。若你把所有流程都寫成工具參數 approved=true，就沒有真正建立 OAuth 授權。

## 官方閱讀

- [MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [Server authorization](https://py.sdk.modelcontextprotocol.io/run/authorization/)
- [Client OAuth](https://py.sdk.modelcontextprotocol.io/client/oauth/)
