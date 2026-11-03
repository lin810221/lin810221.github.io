# 部署 ASGI：反向代理、認證與服務生命週期

從本機測試走向服務部署，明確處理路由、資源、HTTPS 與身分注入。

## Server 與 ASGI 應用

`streamable_http_app()` 產生 ASGI app，可以交給 Uvicorn 或掛在既有服務。路徑要和 Client 配置一致，尤其掛載到另一個前綴時，避免變成 /mcp/mcp。ASGI lifespan 必須正確進入，才能管理 SDK 與你的資料庫／HTTP pool。

初期可先讓 MCP 獨立服務，確認認證、路徑與流量，再決定是否合併到既有 FastAPI。不要只把路由 mount 進去卻忘了 lifespan，或把既有應用的 middleware 順序改到認證上下文無法到達 handler。

## 正式身分不能沿用 fixture

capstone 預設以 ALICE 作本機測試身份，這只適合教材。正式 HTTP 必須將 Token 驗證後的 Principal 注入，並替換公開 HS256 測試金鑰與 .invalid issuer。下載包的 protected_server 展示此注入接點，不提供正式登入服務或生產祕密。

MCP 資源端設定 issuer URL、resource URL、required scopes 與 resource validation。外部 URL 應和 Client 真正連線的資源識別一致，不能讓容器內 localhost URL 與對外 audience 在未說明下混用。

## 反向代理與串流

代理需正確轉送 Authorization、MCP 版本及能力相關標頭，並對 Host／Origin 採明確政策。串流路線要檢查 buffering、idle timeout、請求大小和使用者中斷；JSON 回應正常不代表 SSE 或訂閱一定正常。

TLS 終結、forwarded headers 與可信 proxy 設定也需一致。不要相信任意用戶傳來的 X-Forwarded-User；若身分由代理提供，必須確保外部請求無法直接偽造或繞過代理。

## 容器與健康檢查

容器內監聽所有介面時，主機發布埠仍可限制在 loopback；正式公開服務則應走授權入口。映像採固定相依、非 root 使用者與最小讀寫掛載，祕密在執行時注入。部署命令與容器本身需另外驗證，本課不宣稱已替你部署到雲端。

readiness 應檢查服務是否可接受流量，liveness 則避免把短暫上游故障直接變成重啟風暴。不要用會修改資料或昂貴生成的工具當每秒健康檢查。

## 受保護服務接點

下列模組會在測試中建立受保護的 ASGI app，驗證沒有 Token 被拒絕，以及有效但缺少 scope 的請求仍不能讀工單。

<!-- example:protected_server.py -->

## 練習與解答

列出公開前必須替換的項目：fixture 金鑰、issuer／resource、身分供應商、審核者介面、持久資料庫與對外 TLS。只把 host 改成 0.0.0.0 不會完成這些工作；那只是改變了哪些網路介面可以接收連線。

## 官方閱讀

- [SDK ASGI](https://py.sdk.modelcontextprotocol.io/run/asgi/)
- [Deploy & scale](https://py.sdk.modelcontextprotocol.io/run/deploy/)
- [Authorization](https://py.sdk.modelcontextprotocol.io/run/authorization/)
