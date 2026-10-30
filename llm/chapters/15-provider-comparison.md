## 同一個產品需求，三種協定

比較時先固定任務、資料、輸出要求、模型能力及評估方法。單看一次回答或聊天網站的表現，無法判斷 API 對你的實際工作是否更合適。

下表以本課採用的介面為基準，不代表各供應商所有產品的完整能力，也不表示每個模型支援全部欄位。

## 主要功能參數對照

| 目的 | OpenAI Responses | Gemini Interactions | Claude Messages |
| --- | --- | --- | --- |
| 高層設定 | instructions | system_instruction | system |
| 輸入 | input | input | messages |
| 最大輸出 | max_output_tokens | generation_config.max_output_tokens | max_tokens |
| 推理引導 | reasoning.effort | generation_config.thinking_level | thinking、output_config.effort |
| JSON Schema | text.format | response_format | output_config.format |
| 函式參數 schema | parameters | parameters | input_schema |
| 工具請求 | function_call | function_call step | tool_use block |
| 工具結果 | function_call_output | function_result | user 內的 tool_result |
| 配對識別 | call_id | id → call_id | id → tool_use_id |
| 可見文字的原生位置 | output → message → content | steps → model_output → content | content → text block |
| SDK 文字 helper | output_text | output_text | 遍歷 text blocks 或 SDK helper |
| 服務端歷史 | response / conversation 相關機制 | previous_interaction_id | 基本 Messages 由應用提供歷史 |
| 資源保存控制 | store 等介面設定 | store 等介面設定 | 按服務與資料政策查核 |

## 經典採樣與新模型

temperature、top_p、top_k 不能列成「三家都有所以通用」。它們曾出現在特定模型與舊介面，但新模型可能拒絕、忽略或不再暴露。採樣與 reasoning 也可能有組合限制。

最小 profile 應只包含已確認的功能。需要加參數時，記錄供應商、模型 ID、API / SDK 版本、設定值和驗證日期，再用測試確認它確實影響行為。

## 服務能力怎麼比較？

| 需求 | 比較問題 |
| --- | --- |
| 工具 Agent | 工具協定、平行請求、推理延續與工具成功率 |
| 文件問答 | PDF / 圖片能力、來源定位、檢索與引用 |
| 即時語音 | 支援的即時介面、音訊格式、延遲和中斷能力 |
| 大量抽取 | schema 支援、拒答處理、batch、費用 |
| 企業整合 | 資料政策、區域、權限、稽核與部署平台 |
| 長工作 | 背景執行、狀態保存、取消與恢復 |

圖片理解、圖片生成、音訊理解與音訊生成是不同能力；要對照具體模型和工具，不能只寫「支援多模態」就完成選型。

## 選型要用自己的資料

準備一組有答案、無答案、工具錯誤與邊界情況的測試，量測正確率、拒答、schema、工具選擇、時間與成本。較大的模型不一定在每一題都有足夠收益；較便宜也不代表整體成本低，錯誤重試會增加費用。

若要多供應商 fallback，先處理不同訊息和工具協定。遇到故障時任意把原生歷史送去另一家，可能丟失簽章或權限邊界。

**練習：**替「每天抽取 5000 份文件中的固定欄位」定義五個比較指標。先寫驗收門檻，再挑候選模型，不要先決定品牌再找理由。

官方來源：[OpenAI API](https://developers.openai.com/api/reference/responses/overview)、[Gemini API reference](https://ai.google.dev/api/interactions-api)、[Claude API reference](https://platform.claude.com/docs/en/api/messages/create)。
