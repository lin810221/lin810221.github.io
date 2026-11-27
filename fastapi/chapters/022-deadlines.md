# 局部逾時與整體 deadline

每段等待有限，整次工作也必須有總預算。

## 逾時涵蓋不同等待

連線、讀取、寫入與pool等待各有不同timeout。若每次重試都重新取得完整逾時，整次請求可能遠超使用者可接受時間。本課fetch_json用asyncio.timeout包住全部嘗試與退避，worker另外限制一次供應商工作的期限。

## 總預算的定義

令$D>0$為整體期限秒數，$t_i\geq0$為第$i$次嘗試耗時，$b_i\geq0$為嘗試間退避；最多$N$次嘗試時，需要：

$$\sum_{i=1}^{N}t_i+\sum_{i=1}^{N-1}b_i\leq D.$$

例如兩次各0.7秒、一次0.1秒退避，共1.5秒，仍在2秒內；若第二次一直等待，整體期限會取消它。這是預算條件，不是網路完成時間保證。

## 剩餘預算不足就停止

timeout不是失敗後補填的欄位；要在等待發生之前生效。取消後確保client與response釋放，並判斷遠端是否可能已產生副作用。將本地超時誤認為遠端一定沒有執行，會造成重試風險。

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

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大局部逾時與整體 deadline圖解"><img src="assets/figures/08.svg" alt="連線、讀取、退避與重試共用同一總期限。" loading="lazy"></a><figcaption>一個總期限涵蓋多次嘗試。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「局部逾時與整體 deadline」讀圖：把退避也算進總預算，說明重試次數上限的作用。再用本節的條件回答：兩次各5秒timeout，整次一定不超過5秒嗎？</p></div>

## 自我檢查與解析

**問題：**兩次各5秒timeout，整次一定不超過5秒嗎？

<details><summary>展開解析</summary><p>不一定，還有多次嘗試、退避和其他等待。必須另設整體deadline，並納入所有階段。</p></details>

## 執行與驗收

執行 `python lab28.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab28.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.python-httpx.org/advanced/timeouts/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
