# 資料庫連線池、查詢與鎖等待

讓連線數配合資料庫能力，避免把排隊轉移到更昂貴的位置。

## 連線不是免費資源

每個API和worker程序可能各自建立engine與pool，總連線數需要加總。SQLite的檔案寫入語意與伺服器資料庫不同；增加pool不會讓多個writer無限制同時提交。

## 檢查實際SQL

核對tenant條件、排序、LIMIT與索引，避免先載入全部資料再過濾。資料量擴大時，用實際查詢計畫、掃描筆數與鎖等待評估。ORM讓程式好寫，但不會自動讓所有關聯與迴圈查詢有效率。

## 交易時間要短

模型與網路等待放在交易外，SSE每批開短Session；發生衝突時明確回滾再重試必要步驟。正式PostgreSQL可使用資料庫專屬功能，但要重新驗證隔離、死鎖、連線回收與故障恢復，不直接沿用SQLite的保證。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `claim`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def claim(self, now, lease_seconds=30):
        if type(now) is not int or now < 0 or type(lease_seconds) is not int or lease_seconds <= 0:
            raise ValueError('invalid clock or lease')
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.scalar(select(Job).where((Job.state == 'queued') | ((Job.state == 'running') & (Job.lease_until <= now))).order_by(Job.id).limit(1))
            if row is None:
                return None
            if row.attempt >= 3:
                row.state = 'cancelled' if row.cancel_requested else 'failed'
                row.lease_until = 0
                session.add(Event(job_id=row.id, kind=row.state, data_json=canonical({'code': 'attempt_limit'})))
                return None
            row.state = 'running'
            row.attempt += 1
            row.lease_token = uuid4().hex
            row.lease_until = now + lease_seconds
            session.add(Event(job_id=row.id, kind='running', data_json=canonical({'attempt': row.attempt})))
            return {'id': row.id, 'tenant': row.tenant, 'token': row.lease_token, 'request': json.loads(row.request_json), 'attempt': row.attempt}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/29.svg" target="_blank" rel="noopener" aria-label="放大資料庫連線池、查詢與鎖等待圖解"><img src="assets/figures/29.svg" alt="排隊、檢索、上游與發布各自量測，header時間不是串流完成時間。" loading="lazy"></a><figcaption>量測延遲的正確區間。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「資料庫連線池、查詢與鎖等待」讀圖：避免把提早送headers的串流誤判成整個工作很快完成。再用本節的條件回答：資料庫只容許有限writer，將HTTP並行擴大十倍會怎樣？</p></div>

## 自我檢查與解析

**問題：**資料庫只容許有限writer，將HTTP並行擴大十倍會怎樣？

<details><summary>展開解析</summary><p>可能增加鎖等待、timeout和重試，吞吐不一定改善。需縮短交易並核對資料庫實際容量。</p></details>

## 執行與驗收

執行 `python lab16.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab16.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.sqlalchemy.org/en/21/orm/session_basics.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
