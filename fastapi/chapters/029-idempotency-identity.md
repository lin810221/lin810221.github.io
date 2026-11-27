# 冪等鍵、請求指紋與衝突

同一次意圖重送找回原工作，不同意圖共用鍵則拒絕。

## 兩個不同的識別

令$T$為經認證租戶，$K$為呼叫者提供的冪等鍵，$B$為已驗證且完成業務正規化的body。資料庫唯一識別和內容指紋分別為：

$$U=(T,K),\qquad F=\operatorname{SHA256}(\operatorname{canonicalJSON}(B)).$$

canonical JSON固定鍵排序、分隔符和Unicode處理；本課文件ID視為集合，所以先排序。相同$U$與$F$找回原工作，相同$U$但不同$F$回409。不同租戶可以使用相同鍵，不會合併工作。

## 用資料庫解決競爭

先嘗試插入，由唯一約束決定勝者；輸家開新Session讀回工作，再比較指紋。不能只靠應用記憶體dict，否則多worker、重啟和同時請求會失效。

## 明確的範圍限制

這個策略只控制本地工作建立。租約恢復可能再次呼叫遠端模型，不能因此宣稱遠端exactly-once。正式服務還需決定鍵保留時間、租戶配額、過期後重送語意及用量對帳。

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

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大冪等鍵、請求指紋與衝突圖解"><img src="assets/figures/10.svg" alt="資料列按id排列，以大於上次id取得下一頁。" loading="lazy"></a><figcaption>keyset 依穩定鍵續讀。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「冪等鍵、請求指紋與衝突」讀圖：比較先篩租戶與取頁後才過濾的不同結果。再用本節的條件回答：同一鍵但問題從warranty改成delivery，應回原答案嗎？</p></div>

## 自我檢查與解析

**問題：**同一鍵但問題從warranty改成delivery，應回原答案嗎？

<details><summary>展開解析</summary><p>不應默默回原答案。本課比對請求指紋，回409讓客戶端改用新的意圖識別。</p></details>

## 執行與驗收

執行 `python lab15.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab15.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
