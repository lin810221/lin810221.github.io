# Learning Notes · 學習空間

每個領域一個資料夾，使用深色網頁整理從觀念到實作的完整教材。

網站已在 <https://lin810221.github.io/> 上線。長期維護採用 **修改原稿 → Commit → Push → GitHub Actions 編譯、檢查與發布**，設定和 SourceTree 操作見 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)。自動化設定已加入本機，需推送並將 Pages 的發布來源改成 GitHub Actions 才會啟用。

## 開始閱讀

直接雙擊根目錄的 `index.html`，或執行 `開始學習.cmd`。不需要 Node.js、Python、API Key 或本機伺服器。保留整個資料夾，讓 CSS、章節資料及字型可正確載入。

目前有兩個領域：**LangGraph 完整教學**（28 章）與 **LLM 服務與 AI Agents**（38 章）。各有 12 份 Python 入口及行為測試；LLM 範例預設離線，只有明確加上 `--live` 才呼叫供應商。

提供全文搜尋（Ctrl+K）、程式碼複製、章節目錄、閱讀進度、每章筆記、列印與互動流程示範。進度與筆記儲存在目前瀏覽器 localStorage，無跨裝置同步；重要內容請自行備份。檔案模式的儲存行為依瀏覽器而異，移動資料夾後可能需要重新記錄。

## 資料夾約定

```text
LearningNote/
├── index.html                 學習首頁
├── assets/                    共用閱讀器、深色樣式、程式碼色彩與本機 KaTeX
├── langgraph/
│   ├── index.html             領域閱讀器
│   ├── course.json            章節順序、摘要與分組
│   ├── chapters/*.md          可編輯教材原稿
│   ├── assets/course-data.js  產生好的離線教材
│   └── examples/              Python 範例與測試
├── llm/                       LLM 服務與 AI Agents
│   ├── course.json            38 章的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     三家 API 與採樣實驗室
│   ├── examples/              範例、共用模組與離線測試
│   └── examples.zip           完整範例壓縮包
└── tools/                     教材編譯與驗證工具
```

未來新增領域時，建立獨立資料夾（例如 `linear-algebra/`），再於首頁加入連結。共用閱讀器、樣式和公式引擎可繼續使用；編譯工具會自動發現第一層各資料夾中的 `course.json`。

## 修改教材

修改 `langgraph/chapters/*.md` 與 `course.json` 後，從根目錄執行：

```powershell
python -m pip install -r tools/requirements.txt
python tools/build.py
python tools/validate.py
```

上述指令會編譯並檢查全部領域；若只修改 LLM，可執行 `python tools/build.py llm`。閱讀器在 `assets/reader.js`，每個領域透過自己的課程資料與選用的 overview 模組定義內容。各課程的進度與筆記分別保存。

每章可用 `<!-- example:01_hello.py -->` 引入對應範例的完整程式碼，避免頁面和實際檔案內容不一致。`course-data.js` 需在修改後重新產生；它直接以 script 載入，因此雙擊 HTML 也能閱讀，不受 fetch 的 file:// 限制。

公式：行內用 `$S_t$`；區塊以獨立行的 `$$` 包住。程式碼區塊中的公式不會渲染。本機 KaTeX 0.16.22 及 WOFF2 字型已附帶，授權位於 `assets/vendor/katex/LICENSE.txt`。

## 執行 Python 範例

請參閱 `langgraph/examples/README.md`。實測基準是 Python 3.11、LangGraph 1.1.9 與 langchain-core 1.3.0；官方 1.2+ 的新功能另有說明。執行模型整合片段需要自行安裝供應商套件及設定憑證。

網站與 Python 範例是兩個獨立部分：閱讀網站不用安裝 LangGraph；網站也不會執行 Python 或呼叫模型。

LLM 的執行方式另外參閱 `llm/examples/README.md`。其核心入口與測試只需要 Python 3.11 標準函式庫；真正模型能力與帳號權限需另行驗證。
