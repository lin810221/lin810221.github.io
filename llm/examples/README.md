# LLM 服務與 AI Agents 範例

12 個編號入口，使用 Python 3.11 標準函式庫，預設不需要 API Key、第三方套件或網路。請保留整個 examples 資料夾，入口共用其他 `.py` 模組。

從 `llm` 資料夾執行：

```powershell
python examples/01_openai.py
python examples/02_gemini.py
python examples/03_claude.py
python examples/06_agent.py
python examples/12_capstone.py
python -m unittest discover -s examples -p test_examples.py -v
```

| 入口 | 主題 |
| --- | --- |
| 01_openai.py | Responses REST；預設只顯示請求 |
| 02_gemini.py | Interactions REST；預設只顯示請求 |
| 03_claude.py | Messages REST；預設只顯示請求 |
| 04_sampling.py | 人造 logits 的 softmax / top-p |
| 05_structured.py | JSON 形狀與來源 ID 驗證 |
| 06_agent.py | 離線工具 Agent，或三家原生工具迴圈 |
| 07_events.py | 三家串流事件分流 fixtures |
| 08_rag.py | 關鍵字檢索與引用基線 |
| 09_cost.py | 假設價格的成本計算 |
| 10_memory.py | SQLite 記憶隔離與重新開啟 |
| 11_approval.py | 內容摘要核准與本機發布去重 |
| 12_capstone.py | 知識助理與跨程序審核 |

## 自行接上 API

設定對應 API Key 和模型 ID：OpenAI 使用 `OPENAI_API_KEY` / `OPENAI_MODEL`；Gemini 使用 `GEMINI_API_KEY` / `GEMINI_MODEL`；Claude 使用 `ANTHROPIC_API_KEY` / `ANTHROPIC_MODEL`。Claude REST 的 API 版本預設為 `2026-10-21`，可由 `ANTHROPIC_VERSION` 明確替換。

```powershell
python examples/01_openai.py --live
python examples/06_agent.py --provider openai
python examples/06_agent.py --provider openai --live
```

只有 --live 才送出真實請求，可能產生多次模型費用。Agent 範例只允許 multiply。請使用支援相應工具 / 結構化輸出的可用模型；本課不提供通用的參數相容性保證。

可持久審核：

```powershell
python examples/12_capstone.py ask "AI Agent 如何使用工具？" --db assistant.sqlite
python examples/12_capstone.py review "回傳的id" --digest "回傳的digest" --approve --db assistant.sqlite
```

使用 --reject 可拒絕。若草稿改變，需重新建立提案，不重用舊 digest。`--owner` 是本機示範值，公開服務應從已認證身分取得，不能讓使用者任意冒用。

## 驗證範圍

離線測試使用固定資料與 mocked API 回應，涵蓋請求、解析、工具迴圈、原生歷史保留、預算、資料隔離與審核交易。沒有真的呼叫付費模型，也沒有測試帳號權限、外部搜尋、即時語音或雲端部署。

RAG 基線使用關鍵字與固定模板，不是語意檢索。採樣分數與費用範例都是人造數據。本機 publications 是 SQLite 紀錄，沒有寄信、付款或外部發布；其交易保證不等於外部系統的 exactly-once。
