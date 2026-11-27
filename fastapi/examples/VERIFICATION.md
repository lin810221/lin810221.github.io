# 驗證範圍

查核日2026-11-27。主機Windows CPU、Python3.15.2；31個鎖版套件。52項unittest包含32個實驗入口：真實Pydantic、FastAPI、Starlette、SQLAlchemy、SQLite、Alembic、HTTPX、SSE、JSONL、JWT與WebSocket ASGI測試。TestClient採最新HTTPX2，HTTPX0.29.0另用於明確客戶端與MockTransport。

## 真正執行

輸入與輸出契約、認證與撤銷、角色和租戶、標題PATCH／ETag／邏輯DELETE、multipart和實際分段body限制、短交易、migration一致性、並行冪等、工作claim與fencing、取消、有限attempt、模擬當機恢復、引用與拒答、原生SSE續讀及JSONL、依賴scope與max_concurrency、deadline取消與有限GET重試。socket_smoke啟動真實Uvicorn回環TCP，以獨立Python程序執行worker，驗證上傳、工作、SSE與相同鍵找回。

## 測試替身

OpenAI Responses透過MockTransport核對固定endpoint、輸出schema、完成／拒答／截斷與引用錯誤、回應bytes上限。沒有付費模型呼叫。瀏覽器總覽12個互動實驗使用純本機固定資料與代數模型，與真正後端分開。

## 交付驗收

原稿、公式主題、KaTeX預排、中文SVG、全站連結、閱讀器互動與資料隔離、下載包來源一致性及乾淨解壓後重跑測試，均有對應建置與回歸程序。實際執行結果以本次交付紀錄與GitHub Actions為準。

## 尚未執行

付費模型品質、Docker／Compose、外部OIDC與JWKS輪替、反向代理TLS、正式負載、GPU推論、跨機器排程與時鐘、真正桌面／手機瀏覽器版面。本機TCP與DOM模擬不替代這些環境證據。SQLite lease不是跨供應商exactly-once保證；多次計算或計費仍可能發生。
