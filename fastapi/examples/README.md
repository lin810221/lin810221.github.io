# FastAPI與AI後端工程：RelayDesk

查核：2026-11-27。Python3.15.2、FastAPI0.165.0、SQLAlchemy2.1.9。完整31個套件版本在requirements-lock.txt。核心使用合成文字、真實SQLite與框架，不需要API key或模型權重。首次安裝需網路。

## 從零安裝

解壓後進入包含app.py的examples目錄，Windows：

```powershell
py -3.15 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe run_lab.py --list
.venv\Scripts\python.exe lab01.py
.venv\Scripts\python.exe -m unittest discover -s . -p test_examples.py -v
.venv\Scripts\python.exe socket_smoke.py
```

macOS／Linux先用python3.15建立venv，後續改用.venv/bin/python。不要把作者工作目錄加進PYTHONPATH。測試與實驗只建立並清理自己的.runtime子目錄；實際服務預設資料庫另在.runtime/relay.sqlite3，不會被測試刪除。

## 三個終端機

視窗一啟動API：

```powershell
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

視窗二先產生本機租戶憑證，妥善保存這次輸出，再執行worker：

```powershell
.venv\Scripts\python.exe manage.py provision --tenant demo --role editor
.venv\Scripts\python.exe manage.py work
```

視窗三提供下載包的本機客戶端：

```powershell
.venv\Scripts\python.exe -m http.server 3000 --bind 127.0.0.1
```

開啟http://localhost:3000/client.html，貼入剛產生的token，按「建立文件」「提交工作」「查詢結果」和「讀取或回放事件」。token不寫localStorage。停止訂閱不等於取消工作；取消須按相應按鈕。預設Swagger UI在http://127.0.0.1:8000/docs，可能需要CDN；原始OpenAPI在/openapi.json。

API與worker要讀同一資料庫；換目錄或容器時，以RELAY_DATABASE_PATH明確指定。`manage.py work-once`只做一次claim，方便逐步操作。worker沒有執行時202後保持queued。

## 服務契約

- 文件文字最多4096字元；檔案限UTF-8文字，最多8192 bytes。
- 一般body限16384 bytes；上傳整體20000 bytes，含multipart overhead。
- 最新form_limits設定最多1檔、0文字欄位。max_part_size限制文字part，不是檔案大小。
- GET單筆文件回ETag；PATCH標題與DELETE需If-Match。版本衝突412、缺條件428。
- DELETE為邏輯刪除，原文仍保留；不是物理抹除。相同內容tombstone不能默默重建。
- 租戶只來自認證，不接受body指定。reader不能建立或取消工作。
- 同租戶相同冪等鍵與內容找回同工作；改內容回409。
- 工作最多3次claim；30秒租約、15秒工作期限。到期後舊token不能發布。
- SSE每批最多100事件，依Last-Event-ID續讀；預設10秒關閉訂閱，可再連線。
- 預設provider只做詞交集抽句，沒有語意模型；未命中回abstained。

## 外部模型與部署原稿

provider_cli.py預設只列計畫，不讀key、不連網。只有自行明確加上--live、model與OPENAI_API_KEY才真的呼叫，可能計費。介面以MockTransport驗證；本次未做付費模型推論。

Dockerfile、.dockerignore與compose.yaml是選讀部署原稿，本次沒有啟動Docker。GitHub Pages只提供教材，不能執行FastAPI服務。OIDC、正式代理TLS、GPU、負載、跨機器時間和外部queue需另行驗收。完整操作見RUNBOOK、資料語意見DATA_DICTIONARY、證據見VERIFICATION。
