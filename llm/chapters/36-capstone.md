## 完整專案要驗證的行為

這是一個可切換模型供應商的知識助理：先從固定文件檢索，沒有依據就拒答；有依據才建立草稿；檢查引用後保存待審提案；用相同內容 digest 核准，才建立本機發布紀錄。

它使用固定 Workflow，沒有把所有決策交給模型。這正是實務上常見的組合：生成可用 LLM，資料權限、引用契約與核准仍由程式處理。

```text
問題 → 檢索 → 無依據：拒答
            └→ 有依據：離線模板 / 選定模型
                 → 驗證引用 → SQLite 待審提案
                 → 外部審核 → 核准發布 / 拒絕
```

## 完整入口程式

請保留整個 examples 資料夾，因為它使用前面各章的共用模組。

<!-- example:12_capstone.py -->

## 第一步：執行離線示範

```powershell
python examples/12_capstone.py
```

預設使用臨時 SQLite 和固定模擬核准，沒有模型費用，也沒有寄信或外部發布。它用來確認檢索、提案和本機交易路徑可以完成。

## 第二步：真正分成兩次審核操作

```powershell
python examples/12_capstone.py ask "AI Agent 如何使用工具？" --db assistant.sqlite
```

記下回傳的 id 和 digest，檢查 body.answer 與 sources，再自行決定：

```powershell
python examples/12_capstone.py review "上一步的id" --digest "上一步的digest" --approve --db assistant.sqlite
```

若不核准，把 --approve 換成 --reject。這次 ask 與 review 可以是不同 Python 程序，因為資料在同一個 SQLite 檔案。需使用相同可信 owner；CLI 預設 student 只適合本機示範。

## 第三步：預覽與接上模型

```powershell
python examples/12_capstone.py ask "Agent 如何使用工具？" --provider gemini --db assistant.sqlite
```

沒有 --live 仍只回傳 dry_run 和結構化請求，不建立待審草稿。先設定該供應商環境變數，選擇支援 JSON Schema 的模型，再自行加上 --live。

OpenAI、Gemini、Claude 都使用相同應用 Answer 契約，但 with_schema 轉成各自原生格式。若模型拒絕、截斷或回傳未知來源，會失敗而不發布。

## 逐一檢查重要邊界

retrieve 只是小型關鍵字基線，不能宣稱語意召回品質；真模型可能生成格式正確但語意不受支持的答案，仍需人工或評估；ApprovalStore 的 publications 只是本機紀錄，不會對外傳送。

如果要修改草稿，先驗證新內容，再建立新提案。不要直接修改已核准資料或拿舊 digest 核准不同版本。

## 如何走向正式系統？

先替換檢索器，保留來源契約；再用資料集比較模型；接著加入已認證的 API、適合的資料庫與真正的審核 UI。若要改成更自由的 Agent，可將查詢資料作為受限工具，但保留外層審核與停止政策。

完整範例可從 [Python 範例壓縮包](examples.zip) 取得。**完成標準：**你能證明無依據時拒答、未核准不發布、舊 digest 無效，以及重複核准只產生一筆本機紀錄。

官方來源：[OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)、[Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output)、[Claude structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)。
