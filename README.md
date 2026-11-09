# Learning Notes · 學習空間

每個領域一個資料夾，使用深色網頁整理從觀念到實作的完整教材。

網站已在 <https://lin810221.github.io/> 上線。長期維護採用 **修改原稿 → Commit → Push → GitHub Actions 編譯、檢查與發布**，設定和 SourceTree 操作見 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)。GitHub Actions 自動發布已啟用，推送到 `main` 後會自動執行。

## 開始閱讀

直接雙擊根目錄的 `index.html`，或執行 `開始學習.cmd`。不需要 Node.js、Python、API Key 或本機伺服器。保留整個資料夾，讓 CSS、章節資料及字型可正確載入。

目前有十三個領域：**LangGraph 完整教學**（6 章、28 個單元、12 份 Python 範例）、**LLM 服務與 AI Agents**（8 章、38 個單元、12 份範例）、**RAG 檢索增強生成**（8 章、42 個單元、16 份範例、3 個互動實驗室）、**Embedding 與表示學習**（8 章、48 個單元、20 份範例、4 個互動實驗室）、**PyTorch 實作工程**（8 章、48 個單元、24 份範例、4 個互動實驗室）、**機器學習**（10 章、60 個單元、30 份範例、5 個互動實驗室）、**深度學習**（12 章、72 個單元、42 份範例、6 個互動實驗室）、**應用統計**（10 章主線、70 個單元、40 份範例、8 個互動實驗室），以及 **MCP 與工具整合**（9 章、54 個單元、30 份範例、6 個互動實驗；MCP 2026-07-28／Python SDK 2.3.0）。新增 **搜尋引擎與向量資料庫**（10 章、60 個單元、32 份範例、7 個互動實驗；SQLite 3.54.1、Elasticsearch 9.5.6、Qdrant 1.20.0、Faiss 1.15.1、PostgreSQL 18.6／pgvector 0.8.7）。另新增 **經濟學**（14章、84個單元、42份標準函式庫範例、10個互動實驗；Python 3.15.2）。另新增 **營養學與飲食科學**（16章、96個單元、48份標準函式庫範例、12個互動實驗；2026-11-09查核台灣DRIs第八版、現行標示與WHO指南）。另新增 **運動科學與訓練原理**（16章、96單元、48份標準函式庫範例、12個互動實驗；2026-11-09查核ACSM2026、WHO2020與Python3.15.2）。LLM、RAG 與 Embedding 範例預設離線，API 呼叫須明確加上 `--live`；Embedding 的模型下載另外明確指定。

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
│   ├── course.json            8 章、38 個單元的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     三家 API 與採樣實驗室
│   ├── examples/              範例、共用模組與離線測試
│   └── examples.zip           完整範例壓縮包
├── rag/                       RAG 檢索增強生成
│   ├── course.json            8 章、42 個單元的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     檢索、切塊與指標實驗室
│   ├── examples/              16 個入口、共用模組與虛構資料
│   └── examples.zip           含資料與測試的完整範例包
├── embedding/                 Embedding 與表示學習
│   ├── course.json            8 章、48 個單元的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     幾何、對比學習、門檻、投影實驗室
│   ├── examples/              20 個入口、共用數學與模型 adapter
│   └── examples.zip           含資料與測試的完整範例包
├── pytorch/                   PyTorch 實作工程（2.15.0）
│   ├── course.json            8 章、48 個單元的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     shape、梯度、更新與尾批實驗室
│   ├── examples/              24 個入口、共用實作、合成資料與測試
│   └── examples.zip           含需求檔與測試的完整範例包
├── machine-learning/          機器學習（scikit-learn 1.9.1）
│   ├── course.json            10 章、60 個單元的分組與摘要
│   ├── chapters/              Markdown 教材
│   ├── assets/overview.js     回歸、成本、CV、樹與 KMeans 實驗室
│   ├── examples/              30 個離線入口、完整管線與數值測試
│   └── examples.zip           含合成資料與鎖版需求的完整範例包
├── deep-learning/             深度學習（PyTorch 2.15.0）
│   ├── course.json            12 章、72 個單元的分組與摘要
│   ├── chapters/              Markdown 教材、公式、練習與解答
│   ├── assets/overview.js     梯度、XOR、卷積、正規化、Attention 與加噪
│   ├── examples/              42 個入口、獨立核心、合成資料與測試
│   └── examples.zip           完整可執行下載包
├── applied-statistics/        應用統計（SciPy 1.18.1 / statsmodels 0.15.0）
│   ├── course.json            原十章與附錄，共70個閱讀單元
│   ├── chapters/              單元教材、公式、手算與完整習題解答
│   ├── assets/overview.js     八個互動統計數值實驗
│   ├── examples/              40個入口、獨立核心、合成問卷CSV與測試
│   └── examples.zip           完整資料、程式及鎖版需求
├── mcp/                       MCP 與工具整合：54 個單元、30 份範例
├── search/                    搜尋引擎與向量資料庫
│   ├── course.json            10 章、60 個閱讀單元
│   ├── chapters/              索引、查詢、資料生命週期與維運教材
│   ├── assets/overview.js     7 個確定性互動實驗
│   ├── examples/              32 個入口、實際引擎、虛構資料與驗收
│   └── examples.zip           含依賴鎖版與資料的完整下載包
├── exercise-science/          運動科學與訓練原理：動作、適應、安排與觀察
│   ├── index.html
│   ├── course.json
│   ├── chapters/              96份可編輯課文
│   ├── assets/                課程資料與12個互動實驗
│   └── examples/              48份離線Python範例、虛構資料與測試
├── nutrition/                 營養學與飲食科學：原理、生活、證據與食安
│   ├── index.html
│   ├── course.json
│   ├── chapters/              96份可編輯課文
│   ├── assets/                離線課程資料與12個互動實驗
│   └── examples/              48份Python範例、虛構資料、模型與測試
├── economics/                 經濟學：個體、總體、國際與證據
│   ├── course.json            14章、84個單元
│   ├── chapters/              原創教材、公式、練習與解答
│   ├── assets/overview.js     10個互動數值／圖形實驗
│   ├── examples/              42個入口、模型、虛構CSV與驗收
│   └── examples.zip           可獨立執行的完整下載包
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

應用統計見 [applied-statistics/examples/README.md](applied-statistics/examples/README.md)。保留使用者十章目錄與內容，章內單元由閱讀器重新編號，問卷章改為 Python，不包含 SPSS 操作。2026-11-02 查核最新穩定版 **SciPy 1.18.1 / statsmodels 0.15.0**，Python 3.13 實測 60 項測試。合成問卷保留完整計分、缺失、信度、因素與比較流程；不宣稱代表真實母體或正式量表驗證。

此課使用獨立 Python >=3.12 環境（建議 3.13），不要在既有 Python 3.11 課程環境直接混裝。

```powershell
python -m pip install -r applied-statistics/examples/requirements.txt
python -m unittest discover -s applied-statistics/examples -p test_examples.py -v
```

## MCP 與工具整合

入口：[完整課程](mcp/index.html)。原稿、共用模組與 30 份範例位於 `mcp/`；安裝與實測範圍見 [範例說明](mcp/examples/README.md)。新增獨立 MCP CI job，避免與既有課程相依互相影響。

## 搜尋引擎與向量資料庫

課程入口：[search/index.html](search/index.html)。完整安裝與驗收見 [search/examples/README.md](search/examples/README.md)。從根目錄執行：

```powershell
py -3.11 -m venv .qa/search-latest
.qa/search-latest/Scripts/python.exe -m pip install -r search/examples/requirements.txt
.qa/search-latest/Scripts/python.exe -m unittest discover -s search/examples -p test_examples.py -v
python tools/build.py search
python tools/validate.py
```

實測路線為 APSW／SQLite FTS5、Faiss CPU 與 Qdrant Local；Elasticsearch 預設記錄真實 SDK 序列化，PostgreSQL 預設檢查參數化 SQL。遠端服務、RLS、容器、服務快照與叢集效能需另驗證。人工八維特徵不是語意模型；預設不連線、不下載模型。與 RAG／Embedding 的重疊以必要回顧和交叉閱讀處理，本課主線聚焦索引、儲存、更新與維運。

## 經濟學

入口：[economics/index.html](economics/index.html)。[執行與模型說明](economics/examples/README.md)。Python 3.15.2、僅標準函式庫，不需安裝第三方套件；閱讀網站不需Python。從根目錄執行：

```powershell
py -3.15 -m unittest discover -s economics/examples -p test_examples.py -v
py -3.15 economics/examples/42_policy_report.py --output my-economics-report
python tools/build.py economics
python tools/validate.py
```

涵蓋個體／總體、賽局、資訊、行為、貿易、貨幣金融及政策情境。全部CSV為虛構，預設不下載官方資料；模型算術不冒充真實預測或因果估計。2025 SNA／BPM7與各國資料採用過渡分開說明。「課內進階內容」屬同門課；其他獨立課程明確標示「跨課閱讀」。

## 營養學與飲食科學

入口：[nutrition/index.html](nutrition/index.html)。[執行、來源與資料限制](nutrition/examples/README.md)。Python 3.15.2、標準函式庫；網頁閱讀不需Python。台灣正式指南與美國換算分開標示，草案不取代現行規範。食物與部分日誌為明示虛構，計算不產生個人診斷、需要量或安全判決。

```powershell
py -3.15 -m unittest discover -s nutrition/examples -p test_examples.py -v
py -3.15 nutrition/examples/48_complete_report.py --output my-nutrition-report
python tools/build.py nutrition
```

## 運動科學與訓練原理

入口：[exercise-science/index.html](exercise-science/index.html)。[執行、模型與資料說明](exercise-science/examples/README.md)。2026-11-09查核ACSM2026阻力訓練立場、WHO2020正式指南與2026說明頁；發布年與查核日分開。Python3.15.2、標準函式庫，閱讀不需Python。範例明示虛構，不產生個人課表、醫療許可或ACWR傷害安全區。

```powershell
py -3.15 -m unittest discover -s exercise-science/examples -p test_examples.py -v
py -3.15 exercise-science/examples/48_complete_project.py --output my-exercise-report
python tools/build.py exercise-science
```
