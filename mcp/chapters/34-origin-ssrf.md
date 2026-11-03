# Origin、SSRF 與重新導向

保護本機服務與遠端連線，避免工具整合變成任意網路存取通道。

## 兩個方向的風險

Server 接收瀏覽器來源請求時，要考慮 Origin 與 DNS rebinding；Host 或 Server 主動連外時，要考慮 SSRF。前者避免不可信網站借用本機權限，後者避免攻擊者讓你的程式碰到內網、metadata endpoint 或其他敏感位置。

只驗證 URL 格式不足以解決這兩種問題。`https://` 不保證服務可信，合法網域也可能解析到私有位址；另一方面，本機 HTTP endpoint 即使不公開到網際網路，也可能被瀏覽器引導請求。

## Server 的 Origin 與 Host 檢查

現代 HTTP binding 要求檢查出現的 Origin，對不允許來源拒絕。開發服務預設綁定 loopback，正式代理則需明確定義允許的 Host 與 Origin。不要為了讓某個測試通過，就全域關閉 DNS rebinding 防護。

Origin 與 CORS 不完全相同：CORS 影響瀏覽器是否允許讀取回應，服務仍需自行阻止不合規請求。Token 驗證則處理「誰可以用」，不能用其中一種代替另外兩種。

## 主動連線的允許策略

對固定上游，採精確 host、scheme、port 允許清單，比接受任意 URL 容易審查。拒絕 URL 中的使用者密碼、非必要 fragment 與特殊 port；解析所有 DNS 回答，不能只檢查第一個。私有、loopback、link-local 與混合地址結果都要按政策處理。

本課 `endpoint_policy` 只檢查傳入的解析快照，不進行網路請求。正式系統必須把已驗證解析綁定到實際 connect，並處理 DNS rebinding；若只驗證一次、連線時再重新解析，就仍有時間差風險。

## 重新導向也會跨越邊界

允許的 URL 可以導向不允許的 origin。最保守做法是關閉自動重新導向，或對每一跳重新驗證目的地，而且不能把 Authorization 標頭帶往不同 origin。OAuth metadata 與登入導向也需要驗證，不是只有普通工具 API 才有 SSRF。

## 練習與解答

依序測試 loopback、雲端 metadata 位址、混合 IPv4／IPv6 回答，皆應拒絕。再問「已在允許清單的 host」是否足以通過？不夠，本課仍檢查實際解析位址。這個函式是防線示例，不應宣稱單靠它就完成所有 DNS 與代理的網路防護。

## 可執行範例

在 `examples` 目錄執行 `python 20_endpoint_policy.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:20_endpoint_policy.py -->

## 官方閱讀

- [安全最佳實務：SSRF](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- [HTTP Origin 要求](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
