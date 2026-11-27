# 有限重試、退避與重試放大

只在明確的暫時性錯誤上重試，並保留次數與時間上限。

## 先判斷可重試性

401與403通常要修正憑證或權限，不應盲目重送；429、502、503或504可能是暫時性，但也需要總期限。示範fetch_json只處理GET，最多三次，採短指數退避，沒有把同樣策略直接套在付費模型POST上。

## 指數退避與上限

令初始退避$b>0$，第$i$次重試前的等待為$b_i=b2^{i-1}$。若最多三次嘗試，就只有兩次等待；例如$b=0.01$秒，等待為0.01與0.02秒。正式環境可加入有界jitter與尊重Retry-After，但仍須受總deadline約束。

$$b_i=b\,2^{i-1},\qquad i=1,\ldots,N-1.$$

## 多層重試會相乘

三層服務若各最多三次嘗試，一個入口最壞可能觸發$3^3=27$次下游嘗試。這個算例假設每層每次都觸發下一層並耗盡重試；它說明為何要指定由哪一層負責重試，而不是每層都加上看似保險的迴圈。

## 對照完整專案

以下節錄 `gateway/resilience.py` 的 `fetch_json`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
async def fetch_json(client, path, *, attempts=2, deadline=2, sleep=asyncio.sleep):
    if not path.startswith('/') or path.startswith('//') or '://' in path or not 1 <= attempts <= 3 or not math.isfinite(deadline) or deadline <= 0:
        raise ValueError('relative path and finite bounded policy required')
    async with asyncio.timeout(deadline):
        for attempt in range(attempts):
            try:
                response = await client.get(path)
                if response.status_code not in {429, 502, 503, 504}:
                    response.raise_for_status()
                    return response.json()
                response.raise_for_status()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as error:
                transient = not isinstance(error, httpx.HTTPStatusError) or error.response.status_code in {429, 502, 503, 504}
                if not transient or attempt + 1 == attempts:
                    raise
                await sleep(.01 * 2 ** attempt)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大有限重試、退避與重試放大圖解"><img src="assets/figures/08.svg" alt="連線、讀取、退避與重試共用同一總期限。" loading="lazy"></a><figcaption>一個總期限涵蓋多次嘗試。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「有限重試、退避與重試放大」讀圖：把退避也算進總預算，說明重試次數上限的作用。再用本節的條件回答：模型POST在本機timeout後，可以直接當成沒扣費再重試嗎？</p></div>

## 自我檢查與解析

**問題：**模型POST在本機timeout後，可以直接當成沒扣費再重試嗎？

<details><summary>展開解析</summary><p>不能。供應商可能已執行而回應遺失；本地冪等鍵不保證遠端只計費一次，需供應商支援與用量對帳。</p></details>

## 執行與驗收

執行 `python lab27.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab27.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.python-httpx.org/advanced/timeouts/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
