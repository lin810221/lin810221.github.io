# 多模態與文件AI：可執行範例

本課以合成文件學習來源、OCR、表格、欄位、引用與可靠交付，不含真實客戶資料或API金鑰。主線會真正執行PDF解析、PP-OCRv6 CPU推論、表格、AcroForm、PDF指定文字遮蔽、WAV／動畫GIF與DocWeave。圖文向量是代數教學；逐字稿是人工fixture，沒有冒充CLIP、ASR或大型VLM推論。

## 環境與安裝

查核：2026-11-27。最新PyMuPDF2.2的ONNX Runtime依賴目前沒有Python3.15 wheel；本課採支援分支最新修補版Python3.14.10，保留最新穩定文件套件。使用一般CPython，先解壓後進入`examples`目錄：

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe run_lab.py --list
.venv\Scripts\python.exe lab01.py
.venv\Scripts\python.exe lab07.py
.venv\Scripts\python.exe -m unittest test_examples -v
```

不必先啟用PowerShell腳本。macOS/Linux先用`python3.14 -m venv .venv`，後續使用`.venv/bin/python`。本次實測為Windows CPU；其他平台仍需確認官方wheel並驗收。首次安裝要網路，之後核心資料與OCR使用本機檔案。RapidOCR3.10.0 wheel內已提供本課使用的三個模型；程式明確檢查本機路徑，找不到就停止，不自動下載未知替代品。

```powershell
.venv\Scripts\python.exe -c "import sys,importlib.metadata as m;print(sys.version);print(m.version('pymupdf'));print(m.version('rapidocr'))"
```

`requirements.txt`列主要依賴，`requirements-lock.txt`列本次完整33套件版本。PyMuPDF有AGPL或商業授權選擇，模型、資料、字型條款也需分開核對。本包不重複打包推論模型權重；模型透過原套件安裝。

## 32個實作入口

`lab01.py`到`lab32.py`可各自執行，完整目標用`run_lab.py --list`查看。它們共用真實處理模組；第7個入口執行真正OCR，第一次載入可能較久。實驗產物使用`.runtime`下獨立資料夾，結束時只清理自己的暫存目錄。不要只複製一個入口而漏掉其他模組與`data`。

## 完整DocWeave專題

```powershell
.venv\Scripts\python.exe pipeline.py --input data/invoice.pdf --workspace .runtime/my-docweave
.venv\Scripts\python.exe pipeline.py --input data/invoice.pdf --workspace .runtime/my-docweave
```

在workspace的`current.json`查看目前版本，對應`versions/<version>/review.html`可離線開啟，包含原頁疊框、欄位JSON與來源PDF。重跑會驗證既有不可變產物，不新增另一份相同版本。預期小計4500、稅額225、總額4725，單位都是USD cents。這是固定數位發票的規則式抽取，不是通用VLM產品。

掃描可透過`ocr_local.py data/scan.png`取得真實OCR；主線遇到掃描或不支援結構時拒絕自動發布，因為還沒有完成同樣的表格、引用與欄位契約。擴充時應保留這些驗收。

## 故障注入與恢復

另開一個新的workspace，加入`--fault after_artifacts`。例外退出是刻意中斷，此時產物已完成但沒有新current。移除旗標重跑，程式重新驗證來源、配方和產物，再切換指標。完整步驟與邊界在[操作手冊](RUNBOOK.md)。

## 模型API：預設不讀金鑰、不上傳

```powershell
.venv\Scripts\python.exe providers.py --provider openai --model YOUR_SUPPORTED_MODEL --pdf data/invoice.pdf
.venv\Scripts\python.exe providers.py --provider gemini --model YOUR_SUPPORTED_MODEL --pdf data/invoice.pdf
.venv\Scripts\python.exe providers.py --provider claude --model YOUR_SUPPORTED_MODEL --pdf data/invoice.pdf
```

以上只檢查請求，模型ID需依當日官方目錄與帳號支援明確指定。OpenAI採Responses、Gemini採穩定Interactions v1、Claude採Messages及`output_config.format`。要實際執行，先設定對應`OPENAI_API_KEY`、`GEMINI_API_KEY`或`ANTHROPIC_API_KEY`，再加`--live`；這會把指定PDF送到所選服務並可能產生費用。程式沒有自動換供應商、瀏覽、付款或工具執行。

正式API沒有在本次代跑，離線測試只檢查請求與回應契約。schema通過不等於值正確，回傳資料仍要檢查來源、單位與業務規則。不要把金鑰寫進程式或提交到repo。

## 選用音訊與影片路線

`transcribe.py --audio data/tones.wav --model YOUR_SUPPORTED_MODEL`預設只檢查WAV與檔案轉錄請求；換成已授權的語音樣本、設定金鑰並加`--live`才會上傳。純音不是ASR測試資料，模型文字與時間戳也要重新驗收。`ffmpeg_frame.py --input data/timeline.gif --timestamp 0.5 --output .runtime/frame.png`預設只列命令，明確安裝FFmpeg並加`--run`才啟動外部程序，不覆寫既有檔。這兩支路線已測本機契約與明確執行開關，沒有代跑付費轉錄或FFmpeg解碼。

## 檔案導覽

- [資料字典](DATA_DICTIONARY.md)：來源、座標、表格、時間與預期結果。
- [操作手冊](RUNBOOK.md)：指標、鎖、損壞、重建與恢復。
- [驗證紀錄](VERIFICATION.md)：實測環境與未執行項目。
- `test_examples.py`：58個測試，包含全部32個入口，執行期間封鎖Python HTTP請求。
- `data`：自製PDF、PNG、表單、純音WAV、動畫GIF與人工時間片段。

不要將真實文件或`.runtime`產物放進公開教材repo；GitHub Pages只能提供靜態教材，實際私有上傳與多人覆核需要另外的服務。
