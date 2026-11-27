# 快取鍵、租戶與版本失效

快取會保存過去的決策，也可能保存過去的錯誤。

## 先決定快取哪一層

文件解析、檢索結果、模型答案與HTTP回應有不同失效條件。包含私人資料時，鍵至少要涵蓋租戶或等價權限範圍、文件版本、任務設定及模型相關版本；只用問題文字容易讓不同租戶共享答案。

## 錯誤結果不能因快取變成真相

模型、ACL或資料已變更時，舊結果要失效。先前錯誤若被快取，重複測試可能一直回同一錯誤，容易被誤認為新程式仍失效。除錯要能辨認命中、資料來源與版本，並可安全停用特定快取。

## 本課刻意分開

冪等工作找回的是同一次已定義意圖，不是任意相同問題的語意答案快取。RelayDesk沒有部署Redis或prompt cache；正式擴充需另定TTL、刪除、權限撤銷和可觀察命中率，不以一個dict包裝成完整分散式快取。

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

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大快取鍵、租戶與版本失效圖解"><img src="assets/figures/11.svg" alt="憑證映射租戶與角色，每次查詢加入租戶條件。" loading="lazy"></a><figcaption>認證與資源授權分開。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「快取鍵、租戶與版本失效」讀圖：找出角色檢查與資源歸屬檢查各自的位置。再用本節的條件回答：冪等鍵和答案快取鍵可以直接共用嗎？</p></div>

## 自我檢查與解析

**問題：**冪等鍵和答案快取鍵可以直接共用嗎？

<details><summary>展開解析</summary><p>不能直接等同。前者識別同一次意圖與回應找回，後者重用計算結果，需要獨立的資料、模型和權限失效政策。</p></details>

## 執行與驗收

執行 `python lab15.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab15.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/security/first-steps/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
