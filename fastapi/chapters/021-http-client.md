# HTTPX 連線池與共享客戶端

持久化client、連線上限和明確信任設定一起管理上游請求。

## 重用TCP與TLS連線

每次請求重建AsyncClient會失去pool的好處。本課lifespan建立一次client，設定最大連線與keep-alive數；關閉app時一起關閉。這個client的生命週期屬於單一程序，不是跨所有worker共享。

## 明確設定外部連線行為

connect timeout處理建立連線，read timeout處理讀取等待，pool timeout處理取得連線。`follow_redirects=False`避免把請求帶到非預期目的地；`trust_env=False`不隱式採用本機代理設定。本課模型adapter使用固定官方URL，不允許文件內容指定內網網址。

## 使用MockTransport隔離外部服務

測試用MockTransport檢查endpoint、payload與失敗處理，不連網、不扣費。ASGITransport則把HTTP客戶端接到本機ASGI應用；兩者都是測試邊界，不能當成真實遠端服務品質或網路延遲的證據。

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

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大HTTPX 連線池與共享客戶端圖解"><img src="assets/figures/07.svg" alt="非同步等待能交錯，直接sleep會延後其他請求。" loading="lazy"></a><figcaption>等待 I/O 與阻塞事件迴圈。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「HTTPX 連線池與共享客戶端」讀圖：在等待區間插入第二個請求，再比較阻塞版本。再用本節的條件回答：每個連線池上限八條且有三個worker，遠端最多一定八條連線嗎？</p></div>

## 自我檢查與解析

**問題：**每個連線池上限八條且有三個worker，遠端最多一定八條連線嗎？

<details><summary>展開解析</summary><p>不是。每個程序各有client與pool，上限可能合計24；還需計入其他服務或客戶端。</p></details>

## 執行與驗收

執行 `python lab27.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab27.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.python-httpx.org/advanced/clients/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
