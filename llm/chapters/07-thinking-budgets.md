## 推理預算不等於答案字數

推理模型可能先使用內部工作，再輸出可見答案。最大輸出額度可能同時涵蓋 thinking 與可見文字；若設得太小，模型可能花完預算卻只留下極短或空白輸出。

提高推理深度通常會影響延遲與用量，但不保證每個任務都更好。簡單分類、固定格式抽取或已有明確程式解法的工作，不一定需要高推理設定。

## 三家介面的對照

| 介面 | 常用控制位置 | 不能直接假設的事 |
| --- | --- | --- |
| OpenAI Responses | `reasoning.effort`、`max_output_tokens` | 每個模型都接受相同 effort 值 |
| Gemini Interactions | `generation_config.thinking_level`、`max_output_tokens` | 降輸出上限會自動降低思考深度 |
| Claude Messages | `thinking`、`output_config.effort`、`max_tokens` | 舊 budget_tokens 對所有新模型有效 |

effort 或 level 的 low、medium、high 是供應商與模型各自定義的控制值，不是跨三家可直接比較的固定 token 數。

## 最小的設定示意

```python
# 片段：接在各家支援的請求 body 上，先確認模型能力。
openai_options = {"reasoning": {"effort": "low"}}
gemini_options = {"generation_config": {"thinking_level": "low"}}
claude_options = {"thinking": {"type": "adaptive"}, "output_config": {"effort": "low"}}
```

這三段並不是通用的標準介面。合併 Gemini generation_config 時要保留原來的 max_output_tokens；合併 Claude output_config 時也要保留需要的格式設定。

## Claude 舊手動預算與新模式

舊的 extended thinking 範例可能使用 `thinking={"type":"enabled","budget_tokens":...}`。這是特定舊模型的手動預算方式，文件包含最小與輸出預算關係；新模型可能只接受 adaptive，甚至有不同的預設或不能關閉規則。

因此不要把「至少 1024」當成所有 Claude thinking 的通用起點。先查模型支援的模式，再選 output_config.effort 與 max_tokens。

## 推理內容和可驗證解說

服務可能提供摘要、簽章或不可見的推理用量，不一定提供完整內部過程。需要產品解釋時，要求可檢查的解法、引用或計算步驟即可，不必依賴取得內部 chain of thought。

工具與多輪對話需要的思考簽章應按協定原樣保留，不能任意改寫或只存可見摘要。它們也不能跨供應商直接搬移。

## 遇到截斷怎麼做？

檢查 status、stop_reason、incomplete details 與 usage。視任務提高適當上限、降低支援的推理深度、縮短問題，或分成多個可驗證步驟。不要對一半的 JSON 自行補括號後就視為可信結果。

**練習：**說明為什麼「輸出最多 100 tokens」可能無法得到 100 tokens 的完整解說。再列出你會記錄的三個診斷欄位。

官方來源：[OpenAI reasoning](https://developers.openai.com/api/docs/guides/reasoning)、[Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)、[Claude steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)。
