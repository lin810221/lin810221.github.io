# Elicitation 與 MRTR：向使用者補齊輸入

在新版中以結果攜帶輸入需求，理解 Resolve、重送與不透明狀態。

## 什麼資料不該讓模型猜

語言偏好、某個選項或需要使用者提供的資訊，不能因為模型沒收到就自行編造。Server 可以要求 Client 協助取得補充輸入，再完成原本操作。這與模型自己多想一步不同，也與 OAuth 授權不是同一種流程。

舊版允許 Server 在處理工具時主動向 Client 發出請求；2026-07-28 改以 Multi Round-Trip Requests。Server 回傳輸入需求，Client 取得回應，再向同一操作送出下一輪。所有主要請求方向仍是 Client 到 Server。

## 一次多輪流程

```text
Client → tools/call
Server → InputRequiredResult（問題、requestState）
Host   → 使用者回答
Client → 同一操作＋inputResponses＋原樣回傳的 requestState
Server → 完成結果
```

request state 是不透明狀態，Client 不應自行修改。Server 需要保護它不被竄改、重播或帶到其他主體；如果多節點共用處理，也要考慮狀態保護金鑰與過期策略，不能只用一個可偽造的字串當成核准證明。

## 高階 SDK 的 Resolve

工具參數以 `Annotated[T, Resolve(fn)]` 宣告可注入依賴，resolver 可以回傳 `Elicit` 要求使用者回答。這個依賴不暴露成模型參數，因此模型不能自己填入一個看似已回答的物件，來繞過你的注入路徑。

本課要求顯示語言，Client callback 是明確的測試替身，回傳 zh-TW。它用來驗證協定多輪及資料注入，不代表完成真實人類審核。對寫入操作，仍需獨立保存審核者身分與具體變更。

## 接受、拒絕、取消

使用者接受表單但勾選 false，與拒絕回答或取消，是不同結果。Host UI 應能表達這些情況；Server 不能把所有「沒有 true」都當成網路錯誤並無限重問。對不能缺少的前提，拒絕就應停止執行。

## 練習與解答

確認範例的 input schema 沒有 preference，卻能在完成時讀到語言。再把 callback 改成 decline，工具不應憑空產生偏好。最後回答：這個 callback 能不能直接當付款核准？不能；付款需要綁定主體、金額、收款人、期限及可查驗的核准來源，單一語言表單沒有那些保證。

## 可執行範例

在 `examples` 目錄執行 `python 15_elicitation.py`。完整共用模組、資料與測試包含於 [範例下載包](examples.zip)，請先依 [安裝說明](examples/README.md) 建立隔離環境。

<!-- example:15_elicitation.py -->

## 官方閱讀

- [Resolve 與 Elicit](https://py.sdk.modelcontextprotocol.io/handlers/dependencies/)
- [MRTR](https://py.sdk.modelcontextprotocol.io/handlers/multi-round-trip/)
- [Client callbacks](https://py.sdk.modelcontextprotocol.io/client/callbacks/)
