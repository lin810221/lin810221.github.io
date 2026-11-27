# 取消、清理與外部副作用

取消等待和撤銷已發生的工作是不同問題。

## 取消通常在await邊界發生

asyncio合作式取消會在可等待處傳遞；finally仍應關閉資源。不要把CancelledError當作一般服務錯誤吞掉，也不要因取消協程就假設執行緒、模型服務或資料庫提交自動回滾。

## RelayDesk的取消契約

queued工作可以直接標示cancelled；running工作設定cancel_requested。worker在上游呼叫前檢查一次，發布結果時在同一交易再次檢查。呼叫已經開始後，本課不保證立即中止供應商推論或避免扣費，但保證收到取消標記時不發布正常答案。

## 連線取消不等於工作取消

SSE客戶端斷線只結束事件訂閱，持久化工作仍存在。若使用者確定不要結果，需呼叫取消端點；重連則可用游標回放。把網路連線當成工作生命週期，會讓行動網路短暫斷線變成難以恢復的資料遺失。

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

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大取消、清理與外部副作用圖解"><img src="assets/figures/08.svg" alt="連線、讀取、退避與重試共用同一總期限。" loading="lazy"></a><figcaption>一個總期限涵蓋多次嘗試。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「取消、清理與外部副作用」讀圖：把退避也算進總預算，說明重試次數上限的作用。再用本節的條件回答：關掉瀏覽器的SSE連線會自動取消持久化工作嗎？</p></div>

## 自我檢查與解析

**問題：**關掉瀏覽器的SSE連線會自動取消持久化工作嗎？

<details><summary>展開解析</summary><p>本課不會。工作與訂閱是兩個生命週期；取消工作要明確呼叫取消端點，已發生的外部成本也不一定能撤回。</p></details>

## 執行與驗收

執行 `python lab21.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab21.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.python.org/3.15/library/asyncio-task.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
