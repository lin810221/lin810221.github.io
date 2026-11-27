# function 與 request scope 的串流差異

清理時機會改變串流是否還能使用依賴資源。

## 兩種範圍的承諾

`scope='function'`在path operation結束、回應送出前執行清理；`scope='request'`涵蓋回應傳送。本課trace實驗記錄open、route、chunk與close，用真正StreamingResponse檢查次序，不靠閱讀函式縮排猜測。

## 串流不應無限持有交易

request scope可以讓資源活到串流結束，但若因此把資料庫交易和連線占用幾分鐘，慢客戶端就會耗盡pool。RelayDesk的SSE每輪只做短查詢，拿到純資料後即關閉Session，不讓網路背壓占住資料庫交易。

## 根據用途選擇

短驗證、轉換或已完全讀出的資料可提早清理；串流實際仍會用到的檔案或client則要延長到最後使用。選擇scope不是越長越安全，要把佔用成本、取消與失敗路徑一起列入。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `function_scope`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.get('/function')
    async def function_scope(value: Annotated[str, Depends(resource, scope='function')]):
        app.state.trace.append('route')
        return StreamingResponse(chunks(), media_type='text/plain')
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener" aria-label="放大function 與 request scope 的串流差異圖解"><img src="assets/figures/06.svg" alt="function scope在串流前關閉，request scope在回應後關閉。" loading="lazy"></a><figcaption>yield 依賴的清理時機。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「function 與 request scope 的串流差異」讀圖：指出在第一個chunk前關閉資源時，哪些後續操作會失效。再用本節的條件回答：request scope能解決慢SSE占住資料庫連線嗎？</p></div>

## 自我檢查與解析

**問題：**request scope能解決慢SSE占住資料庫連線嗎？

<details><summary>展開解析</summary><p>它只改變清理時間，反而可能延長佔用。較好的設計是短交易讀出事件、關閉Session，再向客戶端送資料。</p></details>

## 執行與驗收

執行 `python lab06.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab06.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
