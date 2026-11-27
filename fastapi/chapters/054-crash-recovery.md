# 當機恢復、嘗試上限與毒性工作

重領需要有終點，故障測試要對準提交邊界。

## 故障注入的位置

run_once可以在provider已計算、尚未finish時模擬程序中止；它不會寫failed，讓租約保留running。另一個Store實例在到期後重領，重新計算並提交，測試attempt增加且只有有效token能發布。

## 有限嘗試避免永遠卡住

本課最多claim三次。第三次之後仍到期未完成，下一次檢查會標failed或cancelled並記錄attempt_limit，不讓同一工作無限重算。一次work-once可能只處理這個終止動作，其他工作由後續輪詢繼續。

## 不誇大故障證據

此測試驗證選定程式斷點與持久化恢復，不等於斷電、檔案系統損壞、跨區域故障或完整exactly-once證明。正式服務應再測資源耗盡、DB失聯、備份還原、重複投遞與人工重開工作的政策。

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

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大當機恢復、嘗試上限與毒性工作圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「當機恢復、嘗試上限與毒性工作」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：為何模擬當機不能先寫failed再拋例外？</p></div>

## 自我檢查與解析

**問題：**為何模擬當機不能先寫failed再拋例外？

<details><summary>展開解析</summary><p>真實程序可能沒有機會清理；若先寫failed就沒有測到到期重領。故障注入須保留與實際中止相近的持久化狀態。</p></details>

## 執行與驗收

執行 `python lab29.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab29.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
