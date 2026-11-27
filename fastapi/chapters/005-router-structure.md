# 用 APIRouter 組織版本與責任

模組化應保留清楚的依賴方向，避免所有程式塞進入口檔。

## 路由與業務規則分層

入口`app.py`負責提供可匯入物件；`gateway/api.py`處理HTTP與依賴；`contracts.py`定義輸入輸出；`store.py`維護資料交易；`providers.py`定義上游邊界；`worker.py`處理工作。HTTP handler不直接把SQLAlchemy物件或供應商原始回應原封不動傳出去。

## 統一API前綴

本課路由掛在`/api/v1`，健康檢查保留在`/health`。版本前綴只是相容策略的一部分；若欄位意義改變，即使URL不變也可能破壞客戶端。使用明確DTO與契約測試核對新增、移除與可空欄位。

## 依賴方向要能被替換

store不依賴FastAPI Request，供應商也不知道HTTP使用者介面。這使worker能在獨立程序使用相同規則，TestClient能替換認證依賴，也能在不啟動Uvicorn時測試資料層。先保持小而清楚的模組，避免只為未來猜測建立大量抽象。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `get_store`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def get_store(request: Request):
    return request.app.state.store
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大用 APIRouter 組織版本與責任圖解"><img src="assets/figures/02.svg" alt="HTTP與WebSocket訊息分流，啟動和關閉管理共享資源。" loading="lazy"></a><figcaption>ASGI 訊息與 lifespan。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「用 APIRouter 組織版本與責任」讀圖：分辨HTTP請求、WebSocket連線與伺服器生命週期。再用本節的條件回答：為何worker不應匯入某個HTTP請求的Session？</p></div>

## 自我檢查與解析

**問題：**為何worker不應匯入某個HTTP請求的Session？

<details><summary>展開解析</summary><p>請求結束後Session可能已關閉，也不能安全跨執行緒或工作共用。worker應自行開短Session並使用已保存、重新授權的工作資料。</p></details>

## 執行與驗收

執行 `python lab03.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab03.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/dependencies/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
