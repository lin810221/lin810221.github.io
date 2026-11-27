# 並行競爭、過期租約與取消測試

先列出可能交錯順序，再驗證不變條件。

## 同時建立同一意圖

測試以多個執行緒同時提交相同租戶和冪等鍵，確認只有一個job ID與一份queued事件。若測試只依序呼叫兩次，可能永遠碰不到先查再寫的競爭漏洞。

## 舊worker與新worker交錯

A先claim，時間推到到期後B重領，再讓A嘗試finish，必須拒絕；B在自己的有效期限內提交才成功。測試使用可注入時鐘，避免真的等30秒，也讓邊界t等於截止時的行為可重現。

## 保留不變條件

同一鍵不同內容不能共用結果，取消先提交時不能保存正常答案，failed事件不能洩漏供應商秘密。先寫出這些不變條件，再選測試交錯；不要只斷言某個內部函式剛好呼叫幾次。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `submit`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def submit(self, tenant, key, request: JobIn):
        if not re.fullmatch(r'[A-Za-z0-9_-]{8,64}', key):
            raise DomainError(422, 'invalid_idempotency_key')
        self.selected(tenant, request.document_ids)
        payload = canonical(request.model_dump())
        fingerprint = digest(payload)
        try:
            with Session(self.engine) as session, session.begin():
                row = Job(id=uuid4().hex, tenant=tenant, key=key, fingerprint=fingerprint, request_json=payload, state='queued', attempt=0, lease_until=0, lease_token='', cancel_requested=0)
                session.add(row)
                session.flush()
                session.add(Event(job_id=row.id, kind='queued', data_json=canonical({'state': 'queued'})))
                result = self._job(row)
            return result
        except IntegrityError:
            with Session(self.engine) as session:
                row = session.scalar(select(Job).where(Job.tenant == tenant, Job.key == key))
                if row is None:
                    raise
                if row.fingerprint != fingerprint:
                    raise DomainError(409, 'idempotency_conflict')
                return self._job(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大並行競爭、過期租約與取消測試圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「並行競爭、過期租約與取消測試」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：依序重送兩次成功，是否足以證明並行冪等安全？</p></div>

## 自我檢查與解析

**問題：**依序重送兩次成功，是否足以證明並行冪等安全？

<details><summary>展開解析</summary><p>不足。需同時競爭資料庫唯一鍵，並核對工作和事件只有一份，才能覆蓋核心競爭路徑。</p></details>

## 執行與驗收

執行 `python lab16.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab16.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
