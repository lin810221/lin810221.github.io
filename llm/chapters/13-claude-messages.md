## Messages 的基本契約

Claude Messages API 使用頂層 system、max_tokens 與 messages。messages 主要包含 user / assistant 回合；system 指令不是隨便新增一筆 role=system 就完成。

回應 content 是內容區塊列表，可以有文字、工具請求、thinking 或其他型別。不要假設第一塊永遠是文字。

## 可執行入口與版本

<!-- example:03_claude.py -->

共用 REST 模組使用官方目前範例的版本標頭 `anthropic-version: 2026-10-21`，也允許以 ANTHROPIC_VERSION 明確指定。日期代表 API 契約版本，不是模型名稱或模型知識日期。

認證方式請依使用的平台確認；本課 REST 採官方目前文件中的 Authorization Bearer。不同雲端代管平台可能使用自己的認證，不能只替換網址。

## 官方 SDK 寫法

```python
import os
import anthropic

client = anthropic.Anthropic(timeout=45.0, max_retries=0)
message = client.messages.create(
    model=os.environ["ANTHROPIC_MODEL"],
    max_tokens=2048,
    system="請以繁體中文回答。",
    messages=[{"role": "user", "content": "用一個例子解釋 Agent。"}],
)
print(message.stop_reason)
for block in message.content:
    if block.type == "text":
        print(block.text)
```

SDK 自行處理對應的 HTTP 細節；你仍要確認套件版本、API 版本及模型支援。這段為連線片段，教材未實際送出。

## 重要欄位

| 欄位 | 用途 | 注意 |
| --- | --- | --- |
| model | Claude 模型 ID | 模式支援與預設依模型 |
| max_tokens | 最大生成額度 | 可能包含 thinking；不是保證輸出長度 |
| system | 系統設定 | 與 messages 分開 |
| messages | 原生對話內容 | user / assistant 可有多種 content block |
| tools | 工具 schema | 工具參數使用 input_schema |
| tool_choice | 控制工具選擇 | 支援組合依思考模式與模型 |
| thinking | 思考模式 | 舊 enabled 與新 adaptive 要區分 |
| output_config | effort 與結構化格式 | 不是放到 thinking 物件裡 |

## 讀懂 stop_reason

end_turn 表示模型完成該輪；tool_use 表示要處理工具；max_tokens 表示碰到上限；stop_sequence 是遇到指定停止字串。還可能有需要繼續處理或拒絕的狀態與 details，不能只看文字是否存在。

串流的 message_stop 只是事件結束標記，真正結束原因可能在先前 message_delta。API 成功回應也不代表內容必然通過你的業務驗證。

## 續接對話

保留完整 assistant content，接著加入新的 user 訊息；若有工具，回傳對應 tool_result。長歷史仍需要你決定保留、摘要與召回方式，不會因為同一個 client 物件而自動形成跨請求記憶。

**練習：**讓 fixture 的第一個 block 是 thinking、第二個才是 text，確認畫面只顯示文字。再把 stop_reason 改為 max_tokens，應標記 incomplete。

官方來源：[Messages create](https://platform.claude.com/docs/en/api/messages/create)、[Working with Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)、[Client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)。
