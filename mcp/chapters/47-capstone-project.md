# 完整專題：可審核的工單知識助理

把搜尋、租戶隔離、預覽、核准、冪等提交與稽核串成可執行專案。

## 專題交付目標

助理可以搜尋自己的知識、讀取工單、提出結案預覽，並在可信審核後提交。模型無法選 tenant、無法自填 approved，也找不到 approve 工具。工單狀態、預覽和收據保存在 SQLite，讓你能直接檢查執行事實。

這個專題刻意使用虛構資料與明確 fixture 身分。預設程序內／stdio 路線不提供正式多人登入；`protected_server.py` 展示另一條 HTTP 資源端驗證路徑，仍使用公開測試簽章金鑰，不能直接部署給真實使用者。

## 專案分層

| 檔案 | 責任 |
| --- | --- |
| integration_core.py | Principal、ACL、預覽與 SQLite 交易 |
| capstone_server.py | 將領域規則包成四個 MCP 工具與資源 |
| auth_verifier.py | 離線 Token 驗證測試 |
| protected_server.py | 將已驗證 HTTP 身分注入 Server |
| 29_capstone.py | 端到端流程與可信審核測試替身 |
| test_examples.py | 契約、拒絕、交易、stdio 與 HTTP 驗收 |

這些層分開，讓你可以更換資料庫或模型，而不需要把所有規則埋進同一個工具函式。也能分別確認問題出在協定包裝、身分處理或領域交易。

## 跑完一條完整流程

執行範例後，先產生 T1 預覽，再嘗試未核准提交，應被拒絕且工單保持 open。可信 operator 測試替身核准後，再用固定冪等鍵提交。第二次同鍵呼叫只讀取收據，工單版本與 committed audit 不再增加。

這裡的 reviewer 由測試程式直接呼叫內部方法，不是模型工具，也不是真實登入 UI。正式部署需要獨立的操作員介面、身分驗證、角色政策與稽核，不應把同一 fixture reviewer 當成所有人的核准來源。

## 擴展專題時保留不變量

若加入寄信、附件或外部工單 API，先確認哪些效果能在同一交易中完成，哪些需要 outbox 或上游冪等。不要在既有 commit 裡順手呼叫不可重送的外部動作，卻仍宣稱所有效果原子且只發生一次。

如果改成模型自動規劃，仍保留 Host allowlist 與 Server ACL；模型只改變提案來源，不應改變交易與審核不變量。

## 練習與解答

讓 beta 使用者嘗試 alpha 的 preview_id，應拒絕；讓 alpha 在核准後撤銷 tickets:write，也應拒絕。這兩種測試證明核准不會覆蓋當前授權。最後檢查工具 output schema，四個工具都應有可供程式使用的穩定結構。

## 可執行範例

在 `examples` 目錄執行 `python 29_capstone.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:29_capstone.py -->

## 官方閱讀

- [SDK Testing](https://py.sdk.modelcontextprotocol.io/get-started/testing/)
- [MCP tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [TokenVerifier](https://py.sdk.modelcontextprotocol.io/run/authorization/)
