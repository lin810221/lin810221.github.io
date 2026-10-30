## 三種容易混淆的快取

Prompt / context caching 重用穩定的輸入前綴或上下文處理；答案快取保存整份先前結果；應用記憶保存工作或使用者資料。它們的目標與失效條件不同。

命中 prompt cache 仍可能生成新答案；有快取也不代表模型學會資料。答案快取若保存錯誤判斷，反而會讓相同輸入一直得到相同錯誤。

## 三家的快取設計

OpenAI 提供符合條件的 prompt caching；Gemini 有 context caching 能力與對應介面；Claude 提供 prompt cache 控制與 usage 細項。最低長度、模型、TTL、讀寫與儲存費用要各自查核。

穩定的規則、工具 schema 與文件放在適合重用的位置；變動的使用者輸入放在後面。改變前綴、模型或工具可能影響命中，但實際規則不能只靠猜測。

## 何時值得使用？

粗略比較重複處理成本與快取的建立、讀取及儲存成本：

$$
C_{cache}=C_{write}+N\,C_{read}+C_{storage}
$$

這是教學成本模型，不是供應商價目公式。真實費用可能還有輸出、工具和其他項目；請用實際 usage 與方案計算。

快取 key 或資源範圍要包含會改變結果的資料版本與使用者權限。對不能跨使用者共用的內容，先確保隔離，再談命中率。

## Batch 適合什麼？

批次 API 適合不必立刻回應的大量獨立工作，例如資料集標註、文件分類與離線抽取。通常先提交工作與穩定 custom ID，再觀察狀態，最後取回結果與錯誤。

不能假設結果順序與輸入完全一致；以 ID 對應每筆。部分失敗時，只重送需要的項目，避免整批重複產生費用或副作用。

## Background、Queue 與 Webhook

背景生成或代管 Agent 讓長工作在同步請求結束後繼續。你的應用仍要保存工作 ID、狀態、取消與逾時政策，並處理重複通知。

Webhook 需要驗證來源、簽章或官方指定機制，且同一事件可能重送。先去重、記錄，再執行後續動作；不能把收到通知當成新的無限次發布授權。

## Fine-tuning 何時才需要？

若 prompt、資料品質與工具已經足夠，但特定行為或格式仍需要穩定改善，可評估支援模型的 fine-tuning。準備具有權限的高品質訓練資料、獨立驗證集和回歸測試，再比較收益與訓練 / 維運成本。

不要把經常變動的事實只塞進訓練集，期待它取代可更新的 RAG。也不要用評估集的答案訓練後，再把同一份評估成績當成泛化能力。

**練習：**替每天處理的 5000 份文件選擇同步、batch 或佇列；再指出哪些輸入可重用快取，哪些結果必須按資料版本失效。

官方來源：[OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)、[OpenAI batch](https://developers.openai.com/api/docs/guides/batch)、[Gemini caching](https://ai.google.dev/gemini-api/docs/caching)、[Claude prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)。
