# 排錯手冊：從錯誤證據回到責任層

用症狀、最小檢查與可驗證修正整理常見故障。

## 啟動與環境

無法匯入app先查cwd與Python路徑；缺greenlet檢查是否裝完整鎖版或SQLAlchemy asyncio extra；TestClient提醒HTTPX相容時核對Starlette與HTTPX2；資料庫找不到先核對RELAY_DATABASE_PATH而不是刪檔重建。

## 工作與串流

queued不動先看worker與DB路徑；stale_lease看時間、attempt與token，不強行覆寫；SSE重複看cursor是否在成功處理後保存；原生EventSourceResponse報coroutine不可迭代，核對路由是否真正yield，避免把marker當一般return型別使用。

## 資料與效能

引用錯位先核對原文是否改過、offset單位與版本；刪除後仍有資料先確認本課邏輯刪除契約；pool滿看實際並行與連線生命週期，不只增加上限。保留最小合成案例與request ID，對每個推測標記已證實或仍待驗證。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `finish`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def finish(self, claim, result, now):
        answer = Answer.model_validate(result).model_dump()
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.get(Job, claim['id'])
            if row is None or row.state != 'running' or row.lease_token != claim['token'] or row.lease_until <= now:
                raise DomainError(409, 'stale_lease')
            if row.cancel_requested:
                row.state = 'cancelled'
            else:
                row.state, row.result_json = 'succeeded', canonical(answer)
            row.lease_until = 0
            session.add(Event(job_id=row.id, kind=row.state, data_json=canonical({'state': row.state})))
            return self._job(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大排錯手冊：從錯誤證據回到責任層圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「排錯手冊：從錯誤證據回到責任層」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：看到stale_lease就移除token檢查，能修好恢復嗎？</p></div>

## 自我檢查與解析

**問題：**看到stale_lease就移除token檢查，能修好恢復嗎？

<details><summary>展開解析</summary><p>那會移除保護舊worker覆寫的核心邊界。應檢查期限、重領與工作耗時，必要時設計續租，而不是關閉fencing。</p></details>

## 執行與驗收

執行 `python lab20.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab20.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/handling-errors/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
