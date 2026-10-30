## 閱讀和執行是兩件事

閱讀本網站不需要安裝套件。12 份 Python 範例的預設模式只使用 Python 3.11 標準函式庫，也不需要 API Key。三家 API 腳本會先印出請求預覽；只有你加上 `--live` 才送出真實請求。

請保留整個 examples 資料夾。範例共用 `provider_requests.py`、`contracts.py` 等模組，下載單一入口檔案後移到別處，可能找不到共用模組。

## Windows PowerShell 準備

從學習空間根目錄開始：

```powershell
cd llm
python --version
python -m venv .venv
.\.venv\Scripts\python.exe examples\01_openai.py
.\.venv\Scripts\python.exe examples\02_gemini.py
.\.venv\Scripts\python.exe examples\03_claude.py
```

直接使用虛擬環境的 Python，不需要調整執行原則。macOS / Linux 可用 `python3 -m venv .venv`，再以 `.venv/bin/python` 執行。

## 設定憑證和模型名稱

以下用佔位值示意，不要把真實 Key 寫進網頁或公開檔案：

```powershell
$env:OPENAI_API_KEY = "你的 OpenAI Key"
$env:OPENAI_MODEL = "你帳號可用的 Responses 模型 ID"
$env:GEMINI_API_KEY = "你的 Gemini Key"
$env:GEMINI_MODEL = "你帳號可用的 Interactions 模型 ID"
$env:ANTHROPIC_API_KEY = "你的 Claude Key"
$env:ANTHROPIC_MODEL = "你帳號可用的 Messages 模型 ID"
```

只用其中一家時，只需設定對應兩個變數。這些環境變數在目前終端機與子程序生效；`.env` 檔案不會自動被 Python 標準函式庫載入。

先檢查乾跑輸出，再自行執行，例如：

```powershell
.\.venv\Scripts\python.exe examples\01_openai.py --live
```

本課沒有替你呼叫付費模型。實際可用性、額度與費用由自己的帳號決定。

## HTTP 和 SDK 的關係

HTTP API 定義網址、認證標頭、JSON 請求與回應。SDK 是協助呼叫這個協定的程式庫，常提供型別、重試、串流解析或方便存取的 helper。

本課可執行基線使用 REST，方便你看見真正送出的欄位。各供應商章節也有官方 Python SDK 片段。若要執行它們，另外安裝：

```powershell
.\.venv\Scripts\python.exe -m pip install openai google-genai anthropic
```

請在自己的專案固定實測成功的版本。某個最新 SDK 支援的便利屬性，不代表原始 HTTP JSON 就有同名欄位。

## 常見錯誤

`ModuleNotFoundError` 先查環境及共用模組路徑；401 / 403 先查 Key、專案與權限；404 先確認 endpoint 和模型 ID；429 要區分速率或額度。不要把所有錯誤都歸類為模型品質。

避免使用 `openai.py`、`anthropic.py`、`json.py` 等會遮蔽套件或標準函式庫的檔名。本課入口有數字前綴，保持資料夾結構即可。

官方來源：[OpenAI quickstart](https://developers.openai.com/api/docs/quickstart)、[Gemini get started](https://ai.google.dev/gemini-api/docs/get-started)、[Claude SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)。
