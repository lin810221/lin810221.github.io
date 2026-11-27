# 啟動第一個伺服器與互動文件

先跑通健康檢查，再理解開發重載和正式程序的差別。

## app是可被匯入的ASGI物件

`app.py`匯入`create_app`並建立應用。`python -m uvicorn app:app`中的前半是模組，後半是該模組中的物件名稱。必須在正確目錄執行；找不到模組時先核對工作目錄與虛擬環境，不要反覆安裝套件。

## 本機第一輪操作

開啟`http://127.0.0.1:8000/health/live`、`/health/ready`與`/docs`。前兩者是本機JSON端點；預設Swagger UI的腳本可能從CDN取得，因此課程閱讀器可離線，不代表後端預設互動文件已自架所有靜態資產。`/openapi.json`不需要CDN。

## reload只用於開發

`--reload`會監看檔案並重啟程序，記憶體狀態也會重建。正式服務應使用明確的程序管理、健康檢查和關閉期限。把服務開在`127.0.0.1`只提供本機存取；`0.0.0.0`是監聽所有介面，不能拿它當作瀏覽器目的網址。

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
# 在另一個終端機
curl.exe -i http://127.0.0.1:8000/health/live
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大啟動第一個伺服器與互動文件圖解"><img src="assets/figures/02.svg" alt="HTTP與WebSocket訊息分流，啟動和關閉管理共享資源。" loading="lazy"></a><figcaption>ASGI 訊息與 lifespan。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「啟動第一個伺服器與互動文件」讀圖：分辨HTTP請求、WebSocket連線與伺服器生命週期。再用本節的條件回答：app:app找不到時先檢查什麼？</p></div>

## 自我檢查與解析

**問題：**app:app找不到時先檢查什麼？

<details><summary>展開解析</summary><p>檢查是否位於解壓後examples目錄、目前Python是否來自該虛擬環境，以及app.py是否存在；錯誤不一定是缺少套件。</p></details>

## 執行與驗收

執行 `python lab01.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab01.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/first-steps/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
