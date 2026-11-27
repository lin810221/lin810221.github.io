# 工作 claim 的資料庫交易

同一工作只能由當下有效持有者提交，競爭要在資料庫內解決。

## 先取得寫入交易

SQLite主線用BEGIN IMMEDIATE先取得writer位置，再挑queued或到期running工作，更新state、attempt、lease token與截止時間。這是特定資料庫的教學策略，SQLite同時只有有限寫入能力，不是高吞吐分散式排程器。

## 不把計算放進交易裡

claim交易只做短狀態更新與事件，commit後才呼叫provider。若在資料庫交易內等待模型十幾秒，其他寫入可能被阻塞；工作計算和結果發布使用不同短交易，以租約資訊連結。

## 遷移資料庫時重新設計

PostgreSQL可採條件更新或鎖定與skip locked等方案，但鎖行為、隔離、時間來源和公平性不同。不能把SQLite SQL直接改driver就宣稱並行語意相同。本課挑選順序不保證嚴格FIFO，正式需求若重視公平需另建排序政策。

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

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大工作 claim 的資料庫交易圖解"><img src="assets/figures/18.svg" alt="A失去租約後，B重新claim取得新token，A不能再發布。" loading="lazy"></a><figcaption>租約過期與 fencing。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「工作 claim 的資料庫交易」讀圖：分別檢查到期時間與擁有者token，找出只驗時間的漏洞。再用本節的條件回答：為何不在BEGIN後直接等待整個模型呼叫完成？</p></div>

## 自我檢查與解析

**問題：**為何不在BEGIN後直接等待整個模型呼叫完成？

<details><summary>展開解析</summary><p>長時間持有交易和鎖會阻塞其他工作；應短交易claim、交易外計算、再以租約核對後短交易提交。</p></details>

## 執行與驗收

執行 `python lab20.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab20.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
