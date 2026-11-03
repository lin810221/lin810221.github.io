# Token 驗證：簽章、issuer、audience 與主體

驗證 Token 的目標與期限，將可信 claims 轉成 Server 內部 Principal。

## 能解碼不代表可信

JWT 的 payload 可以被讀出，但若未驗證簽章，任何人都可能偽造 subject 或 tenant。正式 verifier 應使用允許的演算法與受信任金鑰來源，驗證 issuer、audience、期限和必要 claims；不能根據 Token 自己寫的 alg 就無條件接受。

$$
allow=signature\land issuer\land audience\land time\land scope\land ACL
$$

這是授權檢查的邏輯示意。前幾項建立 Token 的有效性，scope 與 ACL 再約束實際操作；單一簽章成功不能取代後面的判斷。

## Audience 與 Resource

給工單網站的 Token，不一定能用在 MCP Server。Verifier 應明確驗證它是否為此資源簽發，再回傳 SDK `AccessToken`。當 resource URL 與 audience 契約一致時，可使用 `validate_token_resource=True`，防止接受其他資源的 Token。

有些身分服務採自訂 audience 識別，不能只拿 URL 字串硬比，應依已選供應商的契約檢查。無論採哪種方式，都要能說明 Token 為何屬於這個服務，而不是把 incoming Token 原樣傳給上游系統碰碰運氣。

## 呼叫應用與人類使用者不同

`client_id` 常代表 OAuth 應用，`subject` 才代表資源擁有者或所代表主體。Subject 也需要和 issuer 一起辨識，避免兩個 issuer 都有 alice 而被當成同一人。租戶應來自已驗證且符合業務映射的資料，而不是模型填入的欄位。

本課 `token_principal()` 保存 issuer、subject、tenant 與 scopes。capstone 的模型 Schema 不提供 tenant 或 approved 參數，因為這些資料不應由模型決定。

## 教學驗證器的範圍

下載包用公開的 HS256 fixture key 做離線簽章測試，測試錯誤 audience、過期、無簽章與錯誤 claims。這個 key 刻意公開，不能用於部署；它也不是 OAuth 登入服務。正式系統需使用實際身分供應商、JWKS 或 introspection、金鑰輪替與對應失敗策略。

## 練習與解答

一個簽章正確但 aud 指向其他 API 的 Token 應被拒絕；過期 Token 同樣被拒絕。若只檢查 scope 字串而不驗證簽章，攻擊者可以自行填入 tickets:write。執行範例時只能印驗證後的必要識別，不應把完整 Token 留在終端輸出或日誌。

## 可執行範例

在 `examples` 目錄執行 `python 19_jwt_verifier.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:19_jwt_verifier.py -->

## 官方閱讀

- [SDK TokenVerifier](https://py.sdk.modelcontextprotocol.io/run/authorization/)
- [MCP token requirements](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [PyJWT 驗證](https://pyjwt.readthedocs.io/en/stable/usage.html)
