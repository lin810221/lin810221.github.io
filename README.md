# Learning Notes · 學習空間

每門課程一個獨立資料夾，使用深色網頁整理從觀念到實作的完整教材。首頁依五大知識領域分類。

網站已在 <https://lin810221.github.io/> 上線。長期維護採用 **修改原稿 → Commit → Push → GitHub Actions 編譯、檢查與發布**，設定和 SourceTree 操作見 [GIT_WORKFLOW.md](GIT_WORKFLOW.md)。GitHub Actions 自動發布已啟用，推送到 `main` 後會自動執行。

## 開始閱讀

直接雙擊根目錄的 `index.html`，或執行 `開始學習.cmd`。不需要 Node.js、Python、API Key 或本機伺服器。保留整個資料夾，讓 CSS、章節資料及字型可正確載入。

目前有二十八門課程，整理為五大領域：**LangGraph 完整教學**（6 章、28 個單元、12 份 Python 範例）、**LLM 服務與 AI Agents**（8 章、38 個單元、12 份範例）、**RAG 檢索增強生成**（8 章、42 個單元、16 份範例、3 個互動實驗室）、**Embedding 與表示學習**（8 章、48 個單元、20 份範例、4 個互動實驗室）、**PyTorch 實作工程**（8 章、48 個單元、24 份範例、4 個互動實驗室）、**機器學習**（10 章、60 個單元、30 份範例、5 個互動實驗室）、**深度學習**（12 章、72 個單元、42 份範例、6 個互動實驗室）、**應用統計**（10 章主線、70 個單元、40 份範例、8 個互動實驗室），以及 **MCP 與工具整合**（9 章、54 個單元、30 份範例、6 個互動實驗；MCP 2026-07-28／Python SDK 2.3.0）。新增 **搜尋引擎與向量資料庫**（10 章、60 個單元、32 份範例、7 個互動實驗；SQLite 3.54.1、Elasticsearch 9.5.6、Qdrant 1.20.0、Faiss 1.15.1、PostgreSQL 18.6／pgvector 0.8.7）。另新增 **經濟學**（14章、84個單元、42份標準函式庫範例、10個互動實驗；Python 3.15.2）。另新增 **營養學與飲食科學**（16章、96個單元、48份標準函式庫範例、12個互動實驗；2026-11-09查核台灣DRIs第八版、現行標示與WHO指南）。另新增 **運動科學與訓練原理**（16章、96單元、48份標準函式庫範例、12個互動實驗；2026-11-09查核ACSM2026、WHO2020與Python3.15.2）。LLM、RAG 與 Embedding 範例預設離線，API 呼叫須明確加上 `--live`；Embedding 的模型下載另外明確指定。

新增 **[代謝健康與慢性病預防](metabolic-health/index.html)**：16章、96單元、48份標準函式庫範例、12個互動實驗。2026-11-10查核ADA／CKM／血脂2026、AGA2026、KDIGO2024正式版、台灣高齡血壓及預防保健。

新增 **[心理健康與壓力科學](mental-health/index.html)**：16章、96單元、48份標準函式庫範例、12個互動實驗。2026-11-13查核WHO2026說明、現行NICE正式版與草案、HRV方法及台灣資源，核心與課內進階皆已納入。

新增 **[肌肉骨骼健康與人體工學](ergonomics/index.html)**：16章、96單元、48份標準函式庫範例、12個互動實驗。2026-11-13查核NIOSH RNLE2021修訂、HSE工具、台灣條文及2026正式臨床來源，含工作改善與證據專題。

新增 **[人體解剖與生理學](anatomy-physiology/index.html)**：20章、120單元、64張原創中文圖解、8個互動讀圖活動，附120題學習單、完整解答與100個中英名詞。以構造、機制、生活情境為主線，不設程式配額；2026-11-16核對官方基礎資料。

提供全文搜尋（Ctrl+K）、程式碼複製、章節目錄、閱讀進度、每章筆記、列印與互動流程示範。進度與筆記儲存在目前瀏覽器 localStorage，無跨裝置同步；重要內容請自行備份。檔案模式的儲存行為依瀏覽器而異，移動資料夾後可能需要重新記錄。

## 資料夾約定

右上角的「簡易版」還原原本的單欄橫式課程清單；「詳細版」提供新版分類、路線與直式牌卡。切回詳細版時會恢復搜尋與篩選條件，瀏覽器會記住顯示選擇。

詳細版可點選領域、學習起點與 tag 即時篩選，也能搜尋課名、主題和關鍵字。tag 每次選一個，可搭配其他條件；點選已選 tag 或條件旁的 × 即可取消。篩選網址可分享，重新整理及返回上一頁會恢復條件。課程卡上的 tag 也可以直接點選。

「接著學下去」讀取目前瀏覽器內既有的課程進度，連回上次閱讀或第一個未完成單元；沒有紀錄時不顯示。首頁原稿與新增課程的分類方式見 [課程製作規範](COURSE_AUTHORING.md#首頁分類與探索)。只調整首頁時，執行 `python tools/build_library.py`，再以 `python tools/build_library.py --check` 確認產出。

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
├── metabolic-health/          代謝健康與慢性病預防：量測、器官與整合預防
│   ├── index.html
│   ├── course.json
│   ├── chapters/              96份可編輯課文
│   ├── assets/                課程資料與12個互動實驗
│   └── examples/              48份離線Python範例、虛構資料與測試
├── mental-health/             心理健康與壓力科學：經驗、技能、環境與支持
│   ├── course.json            16章、96個閱讀單元
│   ├── chapters/              可編輯原創教材、案例、練習與解答
│   ├── assets/                離線資料與12個互動實驗
│   ├── examples/              48份Python入口、五份合成資料與測試
│   └── examples.zip           可獨立解壓執行的下載包
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
├── ergonomics/                肌肉骨骼健康與人體工學：身體、工作與環境改善
│   ├── course.json            16章、96個閱讀單元
│   ├── chapters/              可編輯原創教材、公式、案例與解答
│   ├── assets/                離線資料與12個互動實驗
│   ├── examples/              48份Python入口、五份合成資料與80項測試
│   └── examples.zip           可獨立解壓執行的下載包
├── anatomy-physiology/        人體解剖與生理學：圖解優先，不需程式
│   ├── course.json            20章、120單元與圖解索引
│   ├── chapters/              每單元均有圖解、情境、自測與理由
│   ├── assets/figures/        64張原創中文SVG，放大與離線閱讀
│   ├── assets/overview.js     8個互動讀圖、路徑與自測活動
│   ├── study/                學習單、答案、名詞與來源
│   └── study-pack.zip        圖解與紙筆練習下載包
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

## 代謝健康與慢性病預防

入口：[metabolic-health/index.html](metabolic-health/index.html)。[離線程式、資料與公式說明](metabolic-health/examples/README.md)。包含代謝調節、體位、血糖、第二型糖尿病預防、血壓血脂、心血管風險、MASLD、腎臟、生活與環境、台灣預防保健、證據與整合專題。核心與課內進階均已納入；回連營養、運動與統計既有課程。

截至2026-11-10查核正式指南與生效狀態，草案與2027未來規則另列；單位、分析物、量測程序、族群與用途一起說明。Python3.15.2、標準函式庫，虛構資料不作個人診斷、藥物或PREVENT預測。網頁閱讀與KaTeX均可離線。

```powershell
py -3.15 -m unittest discover -s metabolic-health/examples -p test_examples.py -v
py -3.15 metabolic-health/examples/48_complete_project.py --output my-metabolic-report
python tools/build.py metabolic-health
```

## 心理健康與壓力科學

入口：[mental-health/index.html](mental-health/index.html)。[離線程式、資料與方法說明](mental-health/examples/README.md)。從壓力、情緒、注意與習慣，到日常技能、睡眠活動、人際與職場，接到常見困擾、照護、台灣資源、支持他人和證據專題。一般教育、專業照護與課內模型的用途分清；可以全程使用虛構案例，不需寫私人日記。

截至2026-11-13查核，說明頁、正式指南、審查與草案分列；Python3.15.2只用標準函式庫。原創0–10觀察不是臨床量表，不提供診斷、危機預測或治療處方。閱讀、公式和預設實作完全離線。

```powershell
py -3.15 -m unittest discover -s mental-health/examples -p test_examples.py -v
py -3.15 mental-health/examples/48_complete_project.py --output my-mental-learning-report
python tools/build.py mental-health
```

## 肌肉骨骼健康與人體工學

入口：[ergonomics/index.html](ergonomics/index.html)。[離線程式、資料與方法說明](ergonomics/examples/README.md)。從結構、力學、疼痛與工作觀察，到電腦工作、搬抬、重複、振動、工作設計、台灣預防計畫、不同需求與證據判讀。互動算術不代替個人診療、正式現場評估或合規認證。

截至2026-11-13查核，RNLE標2021修訂與2026入口日期，台灣指引保留2014初版；現行條文、國外方法和臨床指南各標範圍。Python3.15.2只用標準函式庫，資料完全虛構；閱讀、公式與預設實作皆離線。

```powershell
py -3.15 -m unittest discover -s ergonomics/examples -p test_examples.py -v
py -3.15 ergonomics/examples/48_complete_project.py --output my-ergo-learning-report
python tools/build.py ergonomics
```

## 人體解剖與生理學：圖解學習

入口：[anatomy-physiology/index.html](anatomy-physiology/index.html)。從細胞、組織、位置與穩態到各器官系統，用可放大的中文圖、剖面、物質路徑、回饋及生活情境教學。核心與課內進階皆已納入，章內單元從01重新編號。

[圖解與練習包](anatomy-physiology/study-pack.zip)包含64張SVG、120題學習單及解答、100個中英名詞與來源。讀者不需Python或其他環境；少數簡式為選讀，沒有個人健康計算或診斷評分。圖解非比例，專業影像與個人照護另有方法。

健康系列的圖解優先原則見[課程製作規範](COURSE_AUTHORING.md)。人體解剖課採圖解主線，既有五門健康課也於2026-11-16補入逐單元示意圖與讀圖任務；原文、範例與進度識別碼保留。來源查核日為2026-11-16，不代表原頁全部當年出版。

```powershell
python tools/build.py anatomy-physiology
python -m unittest discover -s tools -p test_anatomy_materials.py -v
python tools/validate.py
```


## 健康系列圖解補強（2026-11-16）

營養學、運動科學、代謝健康、心理健康與人體工學，每門新增48張本機SVG及96個逐單元讀圖任務，共240張圖、480個任務。每章三張圖，同一圖在兩個單元有不同問題；原有課文、章節順序、筆記和進度識別碼保留。240張中234張為這次新繪、6張為本學習空間的原創解剖圖再用，各圖記錄來源。

圖解包含餐盤與消化吸收、肌肉收縮與供能、器官回饋與量測、壓力與情緒循環，以及工作站、搬抬和接觸受力。課程總覽可依章節篩圖，圖可另開放大；課文有中文圖說、替代文字和讀圖任務。圖稿與任務可離線使用，不需安裝Python；原範例與互動實驗保留為輔助。

| 課程 | 圖解學習包 | 讀圖任務 |
| --- | --- | --- |
| [營養學與飲食科學](nutrition/index.html#overview/health-visuals) | [下載](nutrition/study-pack.zip) | [任務](nutrition/study/read-tasks.md) |
| [運動科學與訓練原理](exercise-science/index.html#overview/health-visuals) | [下載](exercise-science/study-pack.zip) | [任務](exercise-science/study/read-tasks.md) |
| [代謝健康與慢性病預防](metabolic-health/index.html#overview/health-visuals) | [下載](metabolic-health/study-pack.zip) | [任務](metabolic-health/study/read-tasks.md) |
| [心理健康與壓力科學](mental-health/index.html#overview/health-visuals) | [下載](mental-health/study-pack.zip) | [任務](mental-health/study/read-tasks.md) |
| [肌肉骨骼健康與人體工學](ergonomics/index.html#overview/health-visuals) | [下載](ergonomics/study-pack.zip) | [任務](ergonomics/study/read-tasks.md) |

解壓後保留study-pack內的study和assets資料夾。學習包包含圖與任務，不包含完整網站或全部課文。每張圖的適用範圍、簡化與再用記錄見圖說和各課study/sources.md；圖解查核日不取代原課指南、套件與資料的基準日期。

補強驗證：`python -m unittest discover -s tools -p test_health_visuals.py -v`。閱讀器驗證同時覆蓋圖解篩選、逐單元映射、放大連結、重進總覽與筆記進度隔離。


## 實證健康與醫學研究判讀

新增[完整圖解課程](evidence-health/index.html)：18章、108單元、54張原創中文SVG、9個互動判讀活動、108題學習單與解析、120個中英名詞。從零補足必要統計與方法，不需要安裝Python或提供私人健康資料。

主線包含PICO與搜尋、研究設計、隨機試驗、觀察研究與因果、二元與連續結果、信賴區間與多重比較、診斷與篩檢、系統性回顧、森林圖與異質性、GRADE與指南、報告與研究誠信、共同決策，以及新聞、保健品、AI與真實世界資料。最後用原創試驗、觀察、診斷與回顧案例完成一頁證據摘要。

互動活動涵蓋問題拆解、相對與絕對風險、效果精確度、自然頻率、失訪極端情境、共同效果森林圖、DAG、確定性概念與自測。空白、零分母、無法估計、數值界限與假設分開處理，不產生自動GRADE評級或個人醫療建議。

查核2026-11-16：CONSORT／SPIRIT 2025、PRISMA 2020、RoB 2正式文件、IPDAS 5.0（2026）與官方方法資料。ROBINS-I V2 2025-11-20仍是草案；Cochrane6.5.1更新紀錄與入口6.5/2024的差異、GRADE Book漸進更新，以及來源存取限制均另記，不虛構統一年版。

原稿在evidence-health/chapters，圖稿在assets/figures，學習單、解析、名詞、來源及原創案例在study。[下載離線學習包](evidence-health/study-pack.zip)，解壓後保持study-pack內相對路徑。學習包不包含完整網站閱讀器，完整課程仍可由本機index.html離線開啟。

驗證：`python tools/build.py evidence-health`、`python tools/validate.py`、`python -m unittest discover -s tools -p test_evidence_materials.py -v`，以及tools/test-evidence-reader.mjs與全站閱讀器回歸。


## 睡眠科學與晝夜節律

新增[完整圖解課程](sleep-science/index.html)：18章、108單元、54張原創中文SVG、10個互動學習活動、108份含情境學習單與解析、120個中英名詞。延續暗色、離線、可放大圖解與LaTeX，核心學習不需寫程式或提供私人睡眠資料。

從睡眠階段、腦與身體、睡眠壓力、分子及晝夜時鐘，走到光照、生命階段、記憶情緒代謝、日誌與穿戴；再介紹失眠、呼吸及其他睡眠問題、節律障礙、輪班、時差與研究宣稱。必要條件在課內補足，與解剖、心理、代謝及實證健康課另作跨課閱讀。

互動包含虛構睡眠圖、S/C模型、生物相位、跨日與清醒段日誌、缺失與圓形時間、半衰期、AHI／REI分母、穿戴錯分表、固定UTC偏移換算與原創自測。數字、模型值及分數不轉成個人診斷、光照／睡眠限制處方或裝置設定。

2026-11-17查核：AASM2026輪班工作障礙與成人失眠合併治療正式指南、VA/DoD2025失眠／OSA、2025中樞型呼吸事件、2026穿戴科技立場，以及NIH基礎資料。成人2015、兒少2016與AAP2022等正式資料保留原年份；出版、草案、會議摘要、線上發表與存取限制分開記錄。

原稿在sleep-science/chapters，圖稿在assets/figures，練習、解析、名詞、來源與原創案例在study。[下載離線學習包](sleep-science/study-pack.zip)，保留study-pack內相對路徑。學習包是圖與練習，不包含完整網站閱讀器，也不會同步網頁筆記。

驗證：`python tools/build.py sleep-science`、`python tools/validate.py`、`python -m unittest discover -s tools -p test_sleep_materials.py -v`，以及tools/test-sleep-reader.mjs與全站閱讀器回歸。


## 公共衛生與流行病學

新增[完整圖解課程](public-health/index.html)：20章、120單元、60張原創中文SVG、12個互動學習活動、120份情境學習單與解析、140個中英名詞。深色、離線、可放大圖解、獨立筆記與進度及本機LaTeX；核心學習不需程式。

從人口健康、發生與盛行、人時、疾病負擔、描述與標準化，進到研究設計、關聯、偏差、DAG與因果；再連監測、傳播、群聚調查、疫苗與抗藥性、篩檢、慢性病、環境職業氣候、公平、健康體系、政策與資源配置，以及緊急應變、全球治理、倫理和溝通。必要方法在課內完整補足，其他健康、統計與經濟學另標跨課閱讀。

互動使用12組獨立原創案例資料，涵蓋頻率、人時、世代二乘二、標準化、Simpson悖論、通報與發病日期、SIR、疫苗效果、篩檢期望人數、公平尺度、成本效果、聚餐調查及自測；部分活動含多組案例。未知與零分母不硬填0，不將模型作真實疫情預報或自動政策決策。

查核2026-11-17：WHO現行公共衛生與體系資料、World Health Statistics2026與GHE2023方法、2026飲水與熱健康更新、CDC方法及臺灣CDC／衛福部／健保署資料。IHR2024修正與2026整合文本分開說明；大流行協定2025採納與截至2026-11-13仍在談判的PABS附件及生效程序分開。原正式年份、資料年、來源存取限制另見課程來源索引。

原稿：public-health/chapters；圖：public-health/assets/figures；練習、解析、名詞、來源及虛構案例：public-health/study。[離線學習包](public-health/study-pack.zip)含圖與練習，完整互動另在課程閱讀器使用。

驗證：`python tools/build.py public-health`、`python tools/validate.py`、`python -m unittest discover -s tools -p test_public_materials.py -v`及tools/test-public-reader.mjs與全站閱讀器回歸。


## 急救與緊急應變

新增[完整圖解課程](first-aid/index.html)：20章、120單元、60張原創中文SVG、12個固定情境學習活動、120份學習單與解析、125個中英名詞。延續深色、離線、可放大圖與獨立筆記進度；核心不需程式，也不為形式設定公式配額。

從安全、119、反應與正常呼吸，走到成人及兒童嬰兒CPR、AED、哽塞、溺水、出血創傷、熱與化學電傷、胸痛中風、抽搐血糖、嚴重過敏咬傷、環境中毒、不同生命階段、災害準備、合作交接與技能複訓。概念與動作理由在課內補足，實體技巧需合適模型、教具與回饋；網頁答題不作認證。

2026-11-18查核：主線採AHA2025BLS及相關2026更正，其他急救參考AHA／ARC2024、IFRC2025（2026官方發布）與臺灣消防、衛福及防災資料。不同分齡、民眾／受訓分支、藥物與器材條件分開；舊2021臺灣摘要不改稱2026新版，不把他國號碼混作臺灣119流程。

互動只使用固定原創教學案例，不輸入真實病人資料、產生即時分流或治療倒數。包含危害、119資訊、喘息、CPR比較、AED無需電擊、哽塞、出血、燒傷、中風時間、常見迷思、準備清單與自測。中風08:50紀錄明示為已發生延遲，08:40發現本應立即求援。

原稿在first-aid/chapters，圖在assets/figures，學習單、解析、名詞、來源與固定案例在study。[離線學習包](first-aid/study-pack.zip)含圖與練習，完整情境互動另在課程閱讀器使用。

驗證：`python tools/build.py first-aid`、`python tools/validate.py`、`python -m unittest discover -s tools -p test_first_aid_materials.py -v`，以及tools/test-first-aid-reader.mjs與全站閱讀器回歸。


## 影像辨識

新增[完整課程](image-recognition/index.html)：14章、84單元、28張原創中文SVG、24份離線Python範例與8個互動實驗。主線從像素、色彩、座標與資料工程，走到CNN／ViT、分類、物件偵測、分割、可靠性與ONNX部署；含四條專題及真實資料稽核。每章單元重編、搜尋、筆記、進度與離線LaTeX沿用共用閱讀器。

2026-11-23查核：PyTorch2.15.0、TorchVision0.29.2、OpenCV headless5.1.0.95、Pillow13.0.0、NumPy2.5.5；ONNX1.23.2／Script0.7.2／Runtime1.32.0。完整CPU相容環境使用Python3.13.13；這不是宣稱Python3.13是最新分支，ORT1.32目前沒有Windows cp315 wheel。新課的版本基準不自動更動其他課程。

`image-recognition/chapters`為教材，`assets/figures`為中文圖，`examples`含共用核心、24個入口、鎖版需求與測試；[完整程式包](image-recognition/examples.zip)與[圖解學習包](image-recognition/study-pack.zip)可下載。安裝完成後，預設範例用原創合成影像、不下載資料或權重；網站本身不需安裝。分類、單物件定位與分割的教學結果不當成自然影像效能；COCO mAP與玩具AP分開。

```powershell
python -X utf8 tools/build.py image-recognition
python -X utf8 tools/validate.py
.qa/vision-current/Scripts/python.exe -X utf8 -m unittest discover -s image-recognition/examples -p test_examples.py -v
python -X utf8 tools/prepare_pages.py --target pages
```

本機獨立環境建立與一般讀者命令見[範例README](image-recognition/examples/README.md)。閱讀器QA在`tools/test-vision-reader.mjs`，與其他課程一併由`tools/test-readers.mjs`執行。實測範圍見[驗證紀錄](image-recognition/examples/VERIFICATION.md)。


## Transformer與LLM原理

新增[完整課程](transformer/index.html)：16章、96單元、32張原創中文SVG、28份離線Python範例、10個互動實驗與110個術語。從條件機率、UTF8／BPE、Embedding、Q／K／V、位置與區塊，走到手寫GPT訓練、生成、KV Cache、GQA、推論效率、模型家族、後訓練、評估與可靠性。保留必要數學、手算、練習解析及完整專題；API操作連回LLM服務課，微調工程另見[LLM微調與模型適應](finetuning/index.html)。

2026-11-24查核與CPU實測基準：Python3.15.2、PyTorch2.15.0、Transformers5.24.0、Tokenizers0.23.3、Safetensors0.8.0、NumPy2.5.5。新API採cache=／output.cache及TokenizersBackend；不沿用已棄用的Llama快取名稱。其他課程維持各自更新時的版本基準。

原稿在transformer/chapters，圖在assets/figures，完整小模型與測試在examples；[程式下載包](transformer/examples.zip)含完整鎖版需求，[圖解學習包](transformer/study-pack.zip)含96份任務、解說與來源。安裝後預設不下載權重／語料、不呼叫API；原創短文法的生成與PPL只驗證教學機制，不作自然語言能力benchmark。

```powershell
python -X utf8 tools/build.py transformer
python -X utf8 tools/validate.py
.qa/transformer-latest/Scripts/python.exe -X utf8 -m unittest discover -s transformer/examples -p test_examples.py -v
python -X utf8 -m unittest discover -s tools -p test_transformer_materials.py -v
python -X utf8 tools/prepare_pages.py --target pages
```

一般讀者的環境與操作見[範例README](transformer/examples/README.md)，執行界線見[驗證紀錄](transformer/examples/VERIFICATION.md)。tools/test-transformer-reader.mjs檢查十個實驗及閱讀器，並接入全站獨立worker回歸。此次僅準備本機教材與發布檔，沒有推送或部署。


## LLM微調與模型適應

新增[完整課程](finetuning/index.html)：12章、72單元、24張原創中文SVG、24份離線Python入口、8個互動實驗與91術語。從方法選擇、資料權利與切分、chat template、位移與mask，走到完整SFT、LoRA、QLoRA、訓練工程、DPO、持續預訓練、蒸餾、遺忘、評估與模型交付。圖解、題目、解析與公式均保存在可編輯原稿。

2026-11-25查核：Python3.15.2、PyTorch2.15.0、Transformers5.24.1、PEFT0.22.0、TRL1.18.2、Accelerate1.16.0、Datasets5.2.0。CPU主線使用本地初始化小模型與原創合成資料，實測真實PEFT及TRL；不下載權重。另提供接受本地預訓練模型與JSONL的 `train_local.py`，支援完整微調、LoRA與具條件的QLoRA路線。GPU量化、分散式及付費託管工作未冒稱實測，其他課程保留原版本基準。

[程式包](finetuning/examples.zip)包含核心、24個入口、實際模型遷移工具、測試與完整鎖版；[圖解學習包](finetuning/study-pack.zip)包含72份題目與解析、91術語、24圖及來源。數學內容已加入全站逐主題覆蓋與靜態KaTeX驗收，新增閱讀器及下載包回歸，CI使用獨立Python環境驗證。


## Django完整網站實作

新增[Django課程](django/index.html)：14章84單元、28張原創中文SVG、24個離線Python實驗、8個互動算例及104術語。以StudyHub學習任務網站貫穿HTTP、設定、路由、模板、ORM、migration、自訂User、表單、登入與物件授權、Admin、私人附件、郵件、DRF API、測試、快取、Tasks、async與部署。

2026-11-26查核及Windows CPU實測：Python3.15.2、Django6.1.3、DRF3.18.3、WhiteNoise6.12.0與Waitress3.0.2。完整網站使用本地SQLite；獨立實驗與測試採記憶體資料及本地替身，不連外部API。Django6.1的fetch modes與內建Tasks均有實際執行；ImmediateBackend不是背景worker。外部PostgreSQL、SMTP、共享快取與worker另需驗收。

[完整專案](django/examples.zip)包含Model、初始migration、專案層帳號模板、app模板與CSS、API、管理命令及43項測試；[學習包](django/study-pack.zip)含84題與解析、104術語及28張圖。教材可在GitHub Pages閱讀，動態Django專案需另外的Python服務。正式設定保留HSTS子網域與preload的條件，不將部署檢查警告隱藏或冒稱已公開部署。


## SQL與資料工程

新增[完整課程](sql/index.html)：18章108單元、36張原創中文圖解、36個可執行入口、12個網頁互動實驗與90餘個術語。從SQL、JOIN、視窗與交易，走到資料模型、效能、CSV／Parquet、ETL／ELT、增量、CDC、DAG、品質、分析倉儲、安全與資料治理。

以DataHarbor訂單專案貫穿來源契約、序號、晚到更正、刪除、冪等、checkpoint、outbox與版本發布。[完整範例](sql/examples.zip)包含固定資料、SQL、Python、操作手冊與52項測試；[學習包](sql/study-pack.zip)包含108題與解析、術語、官方來源及36張圖。首頁簡易版與詳細版皆可進入，分類於軟體與資料工程，支援SQL／資料工程標籤。

2026-11-27實際驗證Python3.15.2、DuckDB2.0.1與選用Psycopg3.3.9。私人PostgreSQL19.0測試通過隔離快照、SKIP LOCKED、序列化衝突、RLS、IGNORE NULLS與DO SELECT RETURNING。主線套件安裝後可離線執行；網頁互動為概念模擬，Airflow、dbt、Debezium與雲端服務未部署。詳見[驗證紀錄](sql/examples/VERIFICATION.md)。


## 多模態與文件AI

新增[完整課程](multimodal/index.html)：16章96單元、32張原創中文圖解、32個實作入口、12個互動實驗、96題與解析及115術語。從影像座標、PDF、真實OCR、版面、表格、表單與schema，走到CLIP／VLM、三家服務契約、DocVQA、跨模態檢索、評估、安全、音訊／影片時間概念和DocWeave專題。

2026-11-27核對並Windows CPU實測PyMuPDF2.2、pypdf7.2.0、RapidOCR3.10.0、ONNX Runtime1.32.0與Pydantic2.14.4。因ONNX Runtime沒有Python3.15 wheel，採相容分支最新修補版Python3.14.10。58項測試涵蓋真正PP-OCRv6、PDF與表格、AcroForm、redaction、區域引用、WAV／動畫GIF和版本發布恢復。

[範例包](multimodal/examples.zip)包含完整來源、合成資料、操作手冊與測試；[學習包](multimodal/study-pack.zip)包含圖解、學習單、答案、術語和版本。API預設dry-run，OpenAI Responses、Gemini穩定Interactions v1與Claude Messages只做離線契約驗證。手工向量不是語意模型，逐字稿為人工fixture；大型VLM、ASR、MP4與雲端未代跑。首頁簡易版與詳細版、文件AI標籤和跨課路線均已納入。

## FastAPI 與 AI 後端工程

[閱讀課程](fastapi/index.html)：16章、96單元、32張中文SVG、32個實作入口、12個互動實驗、107術語。2026-11-27查核FastAPI0.165.0、Python3.15.2、SQLAlchemy2.1.9與31個鎖版套件。RelayDesk實作文件CRUD、ETag、租戶權限、持久化工作、租約fencing、取消與SSE回放；52項測試包含真實Uvicorn TCP與獨立worker。[完整程式包](fastapi/examples.zip)、[圖解學習包](fastapi/study-pack.zip)。付費API、容器、OIDC服務、代理TLS、GPU與正式負載另列驗收，詳見[驗證紀錄](fastapi/examples/VERIFICATION.md)。
