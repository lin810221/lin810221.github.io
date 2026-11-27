# 原生 JSON Lines 與一般 JSON 陣列

逐筆交付資料時，客戶端要使用符合媒體型別的解析方式。

## JSONL是一行一個值

一般JSON陣列要等到完整陣列結束才能正常解析；JSON Lines每行是一個獨立JSON值，可逐行消費。FastAPI對宣告AsyncIterable模型並使用yield的路由，提供原生JSONL序列化與媒體型別，本課實測為`application/jsonl`。

## 型別與真正generator

路由必須實際yield資料，不是async函式回傳一個未await的coroutine。本課documents.ndjson取出有限文件清單，再yield DocumentOut，輸出仍受公開DTO控制，不含tenant或摘要等內部欄位。

## 串流仍要有限

逐筆序列化不代表來源查詢可以無界載入。此端點一次最多50筆，定位為簡單示範；正式大型匯出應用游標批次、工作快照與可中止策略。傳輸chunk可能切在JSON行或UTF-8字元中間，解析器需要累積緩衝。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `ndjson`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @router.get('/documents.ndjson')
    async def ndjson(user: Identity, store: Database) -> AsyncIterable[DocumentOut]:
        rows = await anyio.to_thread.run_sync(store.documents, user['tenant'], 0, 50)
        for row in rows:
            yield DocumentOut.model_validate(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大原生 JSON Lines 與一般 JSON 陣列圖解"><img src="assets/figures/19.svg" alt="id、event、data及空白行形成一個事件，切包位置不固定。" loading="lazy"></a><figcaption>SSE 事件不是 TCP 封包。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「原生 JSON Lines 與一般 JSON 陣列」讀圖：在事件中間切開網路chunk，說明為何必須保留解析緩衝。再用本節的條件回答：能把整個JSONL回應直接response.json()嗎？</p></div>

## 自我檢查與解析

**問題：**能把整個JSONL回應直接response.json()嗎？

<details><summary>展開解析</summary><p>多行各自是獨立JSON值，通常不是單一合法JSON文件；應依行解析，並保留跨chunk的未完整內容。</p></details>

## 執行與驗收

執行 `python lab23.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab23.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/stream-json-lines/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
