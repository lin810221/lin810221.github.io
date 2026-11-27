# 用 lifespan 管理共享連線與啟動

建立一次、使用多次、在finally中可靠關閉。

## 不在匯入時做昂貴工作

匯入模組時下載模型、連外或開資料庫，會使測試、reload與worker啟動都承受不可預期成本。本課create_app只描述應用，lifespan啟動時才建立Store、執行migration和建立HTTP客戶端；完成後才提供服務。

## 共享的是可共用資源

HTTP AsyncClient保存連線池；SQLAlchemy engine管理資料庫連線。每個Uvicorn程序各有一份，並不會因app.state就跨程序共享。模型若也在這裡載入，增加worker通常會複製模型記憶體，GPU情境尤其需要另做配置。

## 啟動失敗與關閉順序

先建立資源，再標示ready；任何階段失敗都透過finally清理已取得的資源。TestClient必須放在context manager中才會執行lifespan。本課測試同時核對client在使用期間開啟、離開後關閉，以及資料庫engine可被釋放。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `lifespan`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @asynccontextmanager
    async def lifespan(app):
        store = Store(settings.database_path)
        try:
            await anyio.to_thread.run_sync(store.migrate)
            async with httpx.AsyncClient(timeout=httpx.Timeout(5, connect=2), limits=httpx.Limits(max_connections=8, max_keepalive_connections=4), follow_redirects=False, trust_env=False) as client:
                app.state.store, app.state.http, app.state.ready = store, client, True
                app.state.audit_count = 0
                yield
        finally:
            app.state.ready = False
            await anyio.to_thread.run_sync(store.engine.dispose)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大用 lifespan 管理共享連線與啟動圖解"><img src="assets/figures/05.svg" alt="Bearer與store是共享子依賴，principal判定身分再傳入editor。" loading="lazy"></a><figcaption>依賴圖與單次請求快取。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「用 lifespan 管理共享連線與啟動」讀圖：追蹤兩條路徑為何能重用同一依賴結果。再用本節的條件回答：把AsyncClient建在每次請求裡有什麼成本？</p></div>

## 自我檢查與解析

**問題：**把AsyncClient建在每次請求裡有什麼成本？

<details><summary>展開解析</summary><p>失去跨請求連線重用，每次重新建立與關閉；應在適當的程序生命週期共享client，同時限制連線數與逾時。</p></details>

## 執行與驗收

執行 `python lab05.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab05.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/advanced/events/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
