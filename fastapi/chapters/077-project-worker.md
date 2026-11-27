# 獨立 worker 與已驗證答案

工作計算、引用驗證與結果提交分成可觀察階段。

## 執行順序

worker以短交易claim，查詢授權文件，在總期限內呼叫provider，驗證Answer與引用，再以租約token和期限提交。結果與終止事件同交易，不會先向串流顯示成功才發現資料庫沒有保存。

## 操作兩種模式

work-once最多執行一次claim流程，適合逐步學習；work持續輪詢，直到`Ctrl+C`。兩者都要與API使用同一RELAY_DATABASE_PATH；不同工作目錄可能導致相對路徑指向不同資料庫，所以正式部署建議明確絕對路徑與volume。

## 驗證而非只看終端機

GET job取得結果，核對status、引用document_id、字元區間和quote。再問文件未提供的資訊，應得到abstained。終端機顯示執行完成不能代替資料庫可讀結果；程序log和業務交付是兩份證據。

## 對照完整專案

以下節錄 `gateway/worker.py` 的 `run_once`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
async def run_once(store, provider=None, *, clock=None, crash_before_publish=False):
    now = clock or (lambda: int(time.time()))
    claim = await asyncio.to_thread(store.claim, now())
    if claim is None:
        return None
    provider = provider or ExtractiveProvider()
    try:
        if (await asyncio.to_thread(store.job, claim['tenant'], claim['id']))['cancel_requested']:
            return await asyncio.to_thread(store.finish, claim, {'status': 'abstained', 'text': 'Cancelled before provider invocation.', 'citations': []}, now())
        documents = await asyncio.to_thread(store.selected, claim['tenant'], claim['request']['document_ids'])
        async with asyncio.timeout(15):
            value = await provider.answer(claim['request']['question'], documents)
        result = validate_answer(value, documents, extractive=isinstance(provider, ExtractiveProvider))
        if crash_before_publish:
            raise InjectedCrash('simulated process death before publication')
        return await asyncio.to_thread(store.finish, claim, result, now())
    except InjectedCrash:
        raise  # Leave the lease for an independently restarted worker.
    except DomainError as exc:
        if exc.code == 'stale_lease':
            return {'id': claim['id'], 'state': 'stale'}
        await asyncio.to_thread(store.fail, claim, now())
        raise
    except Exception:
        await asyncio.to_thread(store.fail, claim, now())
        raise
```

## 實際操作

在解壓後的 `examples` 目錄執行；Windows使用虛擬環境的Python路徑，macOS／Linux改為 `.venv/bin/python`。

```powershell
python manage.py work-once
# 持續處理模式
python manage.py work
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大獨立 worker 與已驗證答案圖解"><img src="assets/figures/26.svg" alt="API伺服器、worker與客戶端分開執行，共用持久化資料庫。" loading="lazy"></a><figcaption>三個操作視窗。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「獨立 worker 與已驗證答案」讀圖：停止worker後提交工作，再啟動worker觀察狀態演進。再用本節的條件回答：worker顯示執行過，API卻仍queued，可能是哪個設定差異？</p></div>

## 自我檢查與解析

**問題：**worker顯示執行過，API卻仍queued，可能是哪個設定差異？

<details><summary>展開解析</summary><p>最先核對API和worker的資料庫絕對路徑；不同cwd或環境設定可能讓兩者操作不同檔案。</p></details>

## 執行與驗收

執行 `python lab17.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab17.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/background-tasks/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
