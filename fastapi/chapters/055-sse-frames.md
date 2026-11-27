# SSE 的 id、event、data 與事件邊界

使用原生ServerSentEvent，理解線上格式再寫客戶端。

## SSE是一串文字事件

每個事件由欄位行和空白行終止，常見id、event、data與retry。FastAPI原生EventSourceResponse搭配真正的yield路由，將ServerSentEvent轉成線上格式；data會做JSON序列化，raw_data則是明確不包JSON的文字，兩者互斥。

## 不要把marker當成一般手動串流編碼器

目前原生SSE編碼由FastAPI routing層完成，response class是標記。應依官方模式以generator yield事件；若要自行產生已編碼bytes，可用一般StreamingResponse並自行負責協定，不能混用兩種假設。

## 欄位也要防注入

id與event不能包含換行，id不能有NUL，否則可能插入額外欄位。原生模型會檢查。本課data只包含狀態與嘗試等安全資料，不把完整問題或秘密塞進可被多處記錄的事件流。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `stream`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @router.get('/jobs/{job_id}/events', response_class=PrivateEventSourceResponse)
    async def stream(job_id: str, request: Request, user: Annotated[dict, Depends(job_access)], store: Database, last_event_id: Annotated[int, Header(ge=0)] = 0) -> AsyncIterable[ServerSentEvent]:
        # Dependency authorization runs before HTTP 200; sessions close per poll.
        cursor, deadline = last_event_id, asyncio.get_running_loop().time() + settings.stream_seconds
        while True:
            rows = await anyio.to_thread.run_sync(store.events, user['tenant'], job_id, cursor)
            for row in rows:
                cursor = row['id']
                yield ServerSentEvent(id=str(cursor), event=row['event'], data=row['data'])
            state = await anyio.to_thread.run_sync(store.job, user['tenant'], job_id)
            if (state['state'] in {'succeeded', 'failed', 'cancelled'} and len(rows) < 100) or asyncio.get_running_loop().time() >= deadline or await request.is_disconnected():
                break
            await asyncio.sleep(.05)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大SSE 的 id、event、data 與事件邊界圖解"><img src="assets/figures/19.svg" alt="id、event、data及空白行形成一個事件，切包位置不固定。" loading="lazy"></a><figcaption>SSE 事件不是 TCP 封包。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SSE 的 id、event、data 與事件邊界」讀圖：在事件中間切開網路chunk，說明為何必須保留解析緩衝。再用本節的條件回答：yield字串hello透過data欄位後一定原樣是data: hello嗎？</p></div>

## 自我檢查與解析

**問題：**yield字串hello透過data欄位後一定原樣是data: hello嗎？

<details><summary>展開解析</summary><p>不是。data會JSON序列化，字串通常帶JSON引號；需要原始文字時明確使用raw_data並遵守協定。</p></details>

## 執行與驗收

執行 `python lab22.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab22.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/server-sent-events/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
