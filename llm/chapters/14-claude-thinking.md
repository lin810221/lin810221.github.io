## Thinking 的模式與版本

目前 Claude 的 thinking 行為依模型而異。Adaptive 讓模型決定何時及多少推理，應用可用 output_config.effort 引導；舊的手動 enabled / budget_tokens 只適用支援它的模型。

有些新模型預設啟用思考、可能不接受直接關閉，或有其他模式。請查特定模型的能力表，不要把「thinking 是 true / false」當成通用抽象。

## Effort 不在 thinking 裡

```python
# 支援 adaptive 的模型才可使用；這是 body 片段。
options = {
    "thinking": {"type": "adaptive"},
    "output_config": {"effort": "medium"},
}
```

effort 是控制訊號，不是保證使用固定 token 數。Max_tokens 太低仍可能截斷答案；回應 thinking 摘要的長度也不能直接代表完整推理成本。

## Claude 的工具宣告與結果

```python
tool = {
    "name": "lookup_document",
    "description": "查詢已授權文件。",
    "input_schema": {
        "type": "object", "properties": {"document_id": {"type": "string"}},
        "required": ["document_id"], "additionalProperties": False,
    },
}
```

模型 content 中的 tool_use 有 id、name 和 input。執行後，把 tool_result 放進新的 user content，並使用對應 tool_use_id：

```python
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": [{
    "type": "tool_result", "tool_use_id": tool_use.id,
    "content": "文件摘要",
}]})
```

這是接在已取得工具請求的原生對話上的片段。多個工具時，每份結果都要正確配對。不要刪掉同一份 assistant content 中需要保留的 thinking 簽章。

## 結構化輸出

目前 Messages 的原生 JSON schema 格式在 output_config.format：

```python
output_config = {
    "format": {"type": "json_schema", "schema": answer_schema},
}
```

answer_schema 需要另外定義，且所選模型必須支援。若同時設定 effort，把兩項合併到同一個 output_config，不要後面的設定把前面覆蓋掉。

官方 SDK 也有解析 helper 與 schema 轉換能力；支援的 JSON Schema 子集仍有界線。應用解析後，仍要驗證來源 ID、實際權限與業務條件。

## Cache、工具與思考的互動

Prompt caching 可以減少重複處理穩定前綴，並不是把完整答案固定保存。工具定義、system 和內容順序都可能影響命中；thinking 模式變更也可能影響相容性。

對代管 web search、code execution 等工具，使用官方工具型別與支援模型；不要把自己定義的同名函式誤認為供應商已代為執行。

**練習：**把 output_config 先設定 effort，再加入 format，確認兩者都存在。接著模擬 tool_use 回應，檢查你的工具結果使用的是 tool_use_id 而不是名稱。

官方來源：[Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)、[Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)、[Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。
