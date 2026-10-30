## 教學使用的環境

本課選用 **Python 3.11**，核心範例固定 `langgraph==1.1.9` 與 `langchain-core==1.3.0`。這是實測基準，不代表它們永遠是最新版本。讀新版文件時，先確認新增功能的最低版本。

閱讀網站不需要安裝 Python，直接開啟 `index.html` 即可。以下步驟是為了**執行教學中的 Python 程式**。先在學習空間根目錄開啟終端機，再進入領域資料夾。

## Windows PowerShell 安裝流程

```powershell
cd langgraph
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r examples\requirements.txt
.\.venv\Scripts\python.exe examples\01_hello.py
```

這裡直接使用虛擬環境中的 Python，因此不需要先執行啟用腳本，也不需要調整 PowerShell 執行原則。若 `python` 沒有指向正確版本，可用 `py -3.11 -m venv .venv`。

每個專案建立獨立虛擬環境，避免為了這份教材改動其他專案的依賴。`python -m pip` 能確保套件安裝到正在使用的那個 Python。

## macOS / Linux

```bash
cd langgraph
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r examples/requirements.txt
.venv/bin/python examples/01_hello.py
```

後續指令中若寫 `python examples/...`，代表你已經啟用環境，或自行替換為上述虛擬環境的完整 Python 路徑。

## 先確認安裝成功

```powershell
.\.venv\Scripts\python.exe -c "import importlib.metadata as m; print(m.version('langgraph'))"
```

預期印出 `1.1.9`。不要用 `langgraph.__version__` 當通用版本檢查；套件是否提供該屬性不一致。

範例只使用程式記憶體與固定文件。模型章節的連線範例是選用功能，需要另外安裝對應供應商套件、設定 API Key，而且可能產生費用；網站本身不會呼叫模型。

## 需要模型時才加入設定

本課連線片段以 Anthropic 整合為例，模型名稱由環境變數提供，不把會變動的模型可用性寫死在程式裡。

```powershell
.\.venv\Scripts\python.exe -m pip install langchain-anthropic
$env:ANTHROPIC_API_KEY = "你的 API Key"
$env:ANTHROPIC_MODEL = "你帳號可用、支援工具呼叫的模型名稱"
```

PowerShell 的 `$env:` 設定只對該終端機及其子程序有效。關閉後需要重新設定。如果使用 `.env` 檔案，Python 不會自動讀取它；需要自行載入，例如安裝 `python-dotenv` 後呼叫 `load_dotenv()`。請不要把真實 Key 放進教材、網頁或版本控制。

## 常見卡關點

| 現象 | 檢查方式 |
| --- | --- |
| `ModuleNotFoundError` | 安裝套件的 Python 和執行範例的 Python 是否相同？ |
| 網頁看不到章節 | 確認整個資料夾都在，尤其 `assets/course-data.js`；不要只搬走 HTML |
| import 指向自己的檔案 | 不要把腳本命名成 `langgraph.py`、`typing.py` 或 `operator.py` |
| 想改教學文字 | 編輯 `chapters/*.md`，再執行根目錄 `tools/build.py` |
| 套件下載失敗 | 檢查組織代理與套件來源，不要反覆改動全域 Python |

官方來源：[LangGraph install](https://docs.langchain.com/oss/python/langgraph/install)、[Python venv](https://docs.python.org/3/library/venv.html)。
