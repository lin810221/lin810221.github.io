## 三層正確性

**語法正確**代表 JSON 能解析；**schema 正確**代表欄位與型別符合契約；**語意正確**代表內容真的符合來源與業務規則。這三層不能互相取代。

例如 `{"amount": -100}` 可能是合法 JSON，也符合 number schema，但對某個只接受正額的操作仍不合法。來源 ID 存在，也不代表它支持答案每一句話。

## JSON Mode 和 JSON Schema

JSON mode 通常聚焦產出 JSON 語法；結構化輸出可進一步約束欄位、型別與有限選項。各家支援的是 JSON Schema 的特定子集，不能假設任何複雜約束都可在服務端強制。

OpenAI Responses 使用 text.format；Gemini Interactions 使用 response_format；Claude Messages 使用 output_config.format。格式的形狀也不同，請使用第 4 章 with_schema 的對應。

## 完整的應用驗證程式

以下 contracts.py 是本課共用契約。它除了形狀檢查，也限制來源只能來自本輪檢索。

<!-- example:contracts.py -->

執行入口：

<!-- example:05_structured.py -->

## 為什麼還要在應用驗證？

服務可能因拒絕、截斷或不支援模式而沒有正常產生資料；應用也有 schema 之外的規則，例如來源權限、ID 是否存在或訂單狀態是否可修改。

如果供應商回傳的是 incomplete，先處理生成狀態，不要直接以 json.loads 的錯誤當成唯一線索。若用了官方 SDK parse helper，也要處理沒有 parsed result 的情況。

## 拒絕、空資料與錯誤要分開

無資料可以用明確狀態回覆，而不是偽造空白答案；供應商拒絕也不應被當成 schema 解析成功。對沒有依據的問題，本課完整專案在呼叫模型前就走拒答路徑。

解析錯誤需要重試時，限制次數並保存原始狀態與原因。不要無限要求「請修好 JSON」，也不要把缺失的 approved 自動補成 true。

## 如何測試？

測試有效 JSON、缺欄位、多欄位、錯型別、未知來源、重複來源和截斷輸出。再針對答案內容做獨立評估，確認它不是格式正確卻答非所問。

**練習：**在 sources 放入 D99，或在答案引用 D99 但 sources 只有 D1，驗證都會失敗。這只能驗證引用契約，仍不能證明語意支持。

官方來源：[OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)、[Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)、[Claude structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。
