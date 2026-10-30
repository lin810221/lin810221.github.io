# Learning Notes · 學習空間

每個領域一個資料夾，使用深色網頁整理從觀念到實作的完整教材。

網站已在 <https://lin810221.github.io/> 上線。長期維護採用 **修改原稿 → Commit → Push → GitHub Actions 編譯、檢查與發布**，設定和 SourceTree 操作見 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)。GitHub Actions 自動發布已啟用，推送到 `main` 後會自動執行。

## 開始閱讀

直接雙擊根目錄的 `index.html`，或執行 `開始學習.cmd`。不需要 Node.js、Python、API Key 或本機伺服器。保留整個資料夾，讓 CSS、章節資料及字型可正確載入。

目前有七個領域：**LangGraph 完整教學**（28 章、12 份 Python 範例）、**LLM 服務與 AI Agents**（38 章、12 份範例）、**RAG 檢索增強生成**（42 章、16 份範例、3 個互動實驗室）、**Embedding 與表示學習**（48 章、20 份範例、4 個互動實驗室）、**PyTorch 實作工程**（48 章、24 份範例、4 個互動實驗室）、**機器學習**（60 章、30 份範例、5 個互動實驗室）與 **深度學習**（72 章、42 份範例、6 個互動實驗室）。LLM、RAG 與 Embedding 範例預設離線，API 呼叫須明確加上 `--live`；Embedding 的模型下載另外明確指定。

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
├── rag/                       RAG 檢索增強生成
│   ├── course.json            42 章的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     檢索、切塊與指標實驗室
│   ├── examples/              16 個入口、共用模組與虛構資料
│   └── examples.zip           含資料與測試的完整範例包
├── embedding/                 Embedding 與表示學習
│   ├── course.json            48 章的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     幾何、對比學習、門檻、投影實驗室
│   ├── examples/              20 個入口、共用數學與模型 adapter
│   └── examples.zip           含資料與測試的完整範例包
├── pytorch/                   PyTorch 實作工程（2.15.0）
│   ├── course.json            48 章的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     shape、梯度、更新與尾批實驗室
│   ├── examples/              24 個入口、共用實作、合成資料與測試
│   └── examples.zip           含需求檔與測試的完整範例包
├── machine-learning/          機器學習（scikit-learn 1.9.1）
│   ├── course.json            60 章的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     回歸、成本、CV、樹與 KMeans 實驗室
│   ├── examples/              30 個離線入口、完整管線與數值測試
│   └── examples.zip           含合成資料與鎖版需求的完整範例包
├── deep-learning/             深度學習（PyTorch 2.15.0）
│   ├── course.json            72 章的分組與摘要
│   ├── chapters/              Markdown 教材、公式、練習與解答
│   ├── assets/overview.js     梯度、XOR、卷積、正規化、Attention 與加噪
│   ├── examples/              42 個入口、獨立核心、合成資料與測試
│   └── examples.zip           完整可執行下載包
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

上述指令會編譯並檢查全部領域；若只修改 RAG，可執行 `python tools/build.py rag`。閱讀器在 `assets/reader.js`，每個領域透過自己的課程資料與選用的 overview 模組定義內容。各課程的進度與筆記分別保存。

每章可用 `<!-- example:01_hello.py -->` 引入對應範例的完整程式碼，避免頁面和實際檔案內容不一致。`course-data.js` 需在修改後重新產生；它直接以 script 載入，因此雙擊 HTML 也能閱讀，不受 fetch 的 file:// 限制。

公式：行內用 `$S_t$`；區塊以獨立行的 `$$` 包住。程式碼區塊中的公式不會渲染。本機 KaTeX 0.16.22 及 WOFF2 字型已附帶，授權位於 `assets/vendor/katex/LICENSE.txt`。

## 執行 Python 範例

請參閱 `langgraph/examples/README.md`。實測基準是 Python 3.11、LangGraph 1.1.9 與 langchain-core 1.3.0；官方 1.2+ 的新功能另有說明。執行模型整合片段需要自行安裝供應商套件及設定憑證。

網站與 Python 範例是兩個獨立部分：閱讀網站不用安裝 LangGraph；網站也不會執行 Python 或呼叫模型。

LLM 的執行方式另外參閱 `llm/examples/README.md`。其核心入口與測試只需要 Python 3.11 標準函式庫；真正模型能力與帳號權限需另行驗證。

RAG 範例見 [rag/examples/README.md](rag/examples/README.md)。離線版使用真實 BM25 與原句擷取，向量幾何示範使用手工數字；真正 Embedding／生成請用選配 live 入口。預設不下載模型、不連線。所有規章均為虛構教材。從根目錄驗證：

```powershell
python -m unittest discover -s rag/examples -p test_examples.py -v
```

Embedding 範例見 [embedding/examples/README.md](embedding/examples/README.md)。包含手工幾何、TF–IDF、微型梯度訓練、Pooling、分類／聚類／推薦、PCA、量化與模型接點；表示來源皆有標記。從根目錄驗證：

```powershell
python -m unittest discover -s embedding/examples -p test_examples.py -v
```

PyTorch 範例見 [pytorch/examples/README.md](pytorch/examples/README.md)。課程依 2026-10-30 查核的最新穩定版 **2.15.0** 製作，已在 Python 3.11 / 2.15.0+cpu 執行 40 項測試。預設 CPU、合成資料、不下載模型；GPU 與多程序另列條件。閱讀網站仍不需要安裝 Python。

```powershell
python -m pip install -r pytorch/examples/requirements.txt --index-url https://download.pytorch.org/whl/cpu
python -m unittest discover -s pytorch/examples -p test_examples.py -v
```

新增或更新課程前，先確認官方最新穩定版，再固定版本驗證與記錄日期。完整規範見 [COURSE_AUTHORING.md](COURSE_AUTHORING.md)，開發清單見 [COURSE_CHECKLIST.md](COURSE_CHECKLIST.md)。

機器學習範例見 [machine-learning/examples/README.md](machine-learning/examples/README.md)。以 2026-10-30 查核的最新穩定版 **scikit-learn 1.9.1** 製作，Python 3.11 與相容依賴實測 45 項測試。涵蓋 train-only 前處理、主要模型、CV、校準、成本門檻、非監督與模型保存；預設 CPU、合成資料、完全離線。

```powershell
python -m pip install -r machine-learning/examples/requirements.txt
python -m unittest discover -s machine-learning/examples -p test_examples.py -v
```

深度學習範例見 [deep-learning/examples/README.md](deep-learning/examples/README.md)。依 2026-10-30 查核的最新穩定版 **PyTorch 2.15.0** 製作，Python 3.11 / CPU 實測 55 項測試與全部 42 入口。涵蓋梯度推導、架構、生成與完整專題；使用合成資料，安裝完成後離線執行。GPU 與真實資料效果未驗證。

```powershell
python -m pip install -r deep-learning/examples/requirements.txt --index-url https://download.pytorch.org/whl/cpu
python -m unittest discover -s deep-learning/examples -p test_examples.py -v
```
