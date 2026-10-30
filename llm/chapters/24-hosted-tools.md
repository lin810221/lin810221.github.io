## 工具可能由不同地方執行

| 類別 | 誰執行 | 應用要做什麼 |
| --- | --- | --- |
| 自訂 function | 自己的服務 | 驗證、授權、呼叫與結果回傳 |
| 供應商代管搜尋 | 供應商工具服務 | 設定工具、處理引用、監控用量 |
| 程式執行環境 | 指定的沙盒或代管環境 | 管理檔案、限制和輸出生命週期 |
| 電腦 / 瀏覽器操作 | 受控環境或執行代理 | 畫面觀察、動作限制、必要審核 |

同樣放在 tools，並不代表執行協定或責任相同。模型能要求某動作，和服務已提供可執行環境是不同事情。

## Web Search 和 Grounding

OpenAI Responses 可使用支援的 web_search；Gemini Interactions 有 google_search 等工具；Claude 的搜尋工具也有自己的型別、版本與模型條件。

搜尋可以補上即時資料，但搜尋結果可能過時、互相衝突或沒有直接支持答案。保存來源與日期，依產品要求顯示引用；不要只留下模型改寫的結論。

```python
# 片段：各自加入對應的 API 請求，不是通用工具陣列。
openai_tools = [{"type": "web_search"}]
gemini_tools = [{"type": "google_search"}]
```

是否支援與可用設定仍按模型及帳號查核。本課不會真的啟動搜尋工具或消耗其費用。

## File Search 與直接文件輸入

直接把 PDF 交給模型適合一次處理特定材料；file search 通常需要先準備可查詢的資料資源，再由工具檢索。兩者的更新、引用、保存與費用不同。

上傳成功不表示資料會永久存在，也不表示索引已立即就緒。確認處理狀態、權限、保留期限與刪除流程；來源更新後也要更新相關索引。

## 程式執行

代管 code execution 可以協助計算與資料分析，但要知道支援語言、可讀檔案、網路能力、資源上限和產物取得方式。模型說「已畫出圖」時，應檢查實際檔案產物。

對確定的商業計算，仍可由你自己的受測函式完成，不必每次讓模型生成任意程式。可重複的計算應有固定資料與測試。

## Computer Use 和其他工具的選擇

若有穩定 API，通常先用 API；需要視覺介面才考慮電腦操作。畫面座標和頁面狀態容易變動，權限和副作用也要清楚控制。

將「讀取頁面」與「按下送出」分開設計。涉及發信、付款或刪除的步驟，應綁定具體內容審核，不能只依模型自行判斷授權。

## 工具結果如何進入產品？

分別保留原始來源、工具執行狀態、衍生摘要和最終答案。不要把內部工具 log 全部直接送給前端，也不要為了簡化畫面而丟掉可追溯資訊。

**練習：**比較「直接讀一份 PDF」和「對 1 萬份文件做 file search」，列出準備資料、更新、引用和費用上的差別。

官方來源：[OpenAI using tools](https://developers.openai.com/api/docs/guides/tools)、[Gemini Google Search](https://ai.google.dev/gemini-api/docs/google-search)、[Claude tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)。
