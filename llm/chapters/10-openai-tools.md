## Function Calling 的請求形狀

在 Responses API 中，函式工具以 type、name、description 和 parameters 定義。這段只是工具宣告，不會執行 Python：

```python
tools = [{
    "type": "function",
    "name": "lookup_document",
    "description": "取得允許查詢的文件摘要。",
    "parameters": {
        "type": "object",
        "properties": {"document_id": {"type": "string"}},
        "required": ["document_id"],
        "additionalProperties": False,
    },
    "strict": True,
}]
```

strict 模式有對 schema 子集與必要欄位的要求；可省略的業務值有時需以 nullable 欄位表達，而不是直接刪掉 required。請依目前文件核對支援約束。

## 請求、執行、回傳

模型輸出的 function_call 會有工具名稱、JSON 字串 arguments、項目 ID 與 call_id。回傳執行結果時，對應的是 **call_id**。

```python
import json

# response 是含有工具請求的 Responses 回應。
# history 是本輪使用的原生 input 歷史。
history.extend(response.output)
for item in response.output:
    if item.type != "function_call":
        continue
    arguments = json.loads(item.arguments)
    result = execute_allowed_tool(item.name, arguments)
    history.append({
        "type": "function_call_output",
        "call_id": item.call_id,
        "output": json.dumps(result, ensure_ascii=False),
    })
```

這是迴圈內的協定片段；execute_allowed_tool 必須由應用建立白名單與輸入驗證。不要用 eval、任意 import 或依模型文字執行 shell。

之後把更新過的 history 再送入模型，直到得到最後回答或到達上限。需要延續的 reasoning items 也應按官方要求保留，不能只取 message 文字。

## 結構化答案與工具參數不同

工具參數的 schema 是給應用執行工作；最終答案的 schema 是給產品或後續程式使用。兩者都可能是 JSON，但責任不同。

Responses 的最終格式在 `text.format`，例如 type=json_schema、name、schema、strict。官方 Python SDK 也有 `responses.parse(..., text_format=YourPydanticModel)` 的便利方式。

即使 schema 保證形狀，也必須處理拒絕與 incomplete，並驗證來源、權限與業務規則。正確的 JSON 仍可能包含錯誤的訂單號碼。

## 代管工具和本機工具

web_search、file_search 等服務端工具，執行位置與輸出事件和自己的 function 不同。不能看到 tools 陣列就認為每一項都需要本機執行。

代管搜尋仍需讀取引用與來源資訊；檔案搜尋需要準備資料資源；程式執行與電腦操作需要確認執行環境、可用資源及工具限制。功能不是只在 prompt 裡要求一次就會出現。

## 何時改用 Agent 層？

手動 Responses 迴圈適合學習協定及小型控制。OpenAI 的 Agents SDK 與相關 Agent 服務提供更高層的執行與管理能力。它們仍需要你設計工具、狀態與驗收條件，不會替應用決定所有權限。

**練習：**讓工具參數包含一個不在 schema 的欄位，確認應用拒絕它。再模擬兩個 function_call，要求每個結果使用各自的 call_id。

官方來源：[Function calling](https://developers.openai.com/api/docs/guides/function-calling)、[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)、[Using tools](https://developers.openai.com/api/docs/guides/tools)。
