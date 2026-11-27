# 租約、重領與 fencing token

到期時間解決卡住，持有者token解決舊worker回來覆寫。

## 為何只記running不夠

worker可能中止卻沒有機會標記失敗。租約讓另一worker在截止後重新claim；每次claim產生新token並增加attempt。舊worker即使稍後恢復，也不能再用原token提交。

## 提交條件

令$s$為目前工作狀態，$k_w$為worker持有token，$k_d$為資料庫token，$t$為提交時間，$e$為租約截止。只有：

$$s=\text{running}\ \land\ k_w=k_d\ \land\ t<e$$

才允許提交。本課整數秒時鐘在$t=e$已到期，不能再發布。例子A在100領到截止130，B在130重領，A在131返回時會被拒絕，不論它的答案是否看似正確。

## 時鐘與續租邊界

教學用同一機器時間和30秒租約，worker呼叫期限15秒；沒有實作跨機器時鐘治理或長工作續租。正式分散式部署需選可信時間來源、續租政策與故障測試，不可直接放大這個教學實作的保證。

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

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大租約、重領與 fencing token圖解"><img src="assets/figures/18.svg" alt="A失去租約後，B重新claim取得新token，A不能再發布。" loading="lazy"></a><figcaption>租約過期與 fencing。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「租約、重領與 fencing token」讀圖：分別檢查到期時間與擁有者token，找出只驗時間的漏洞。再用本節的條件回答：只確認工作仍running，為何不能防止舊worker提交？</p></div>

## 自我檢查與解析

**問題：**只確認工作仍running，為何不能防止舊worker提交？

<details><summary>展開解析</summary><p>B重領後狀態仍是running。還要比較每次claim的新token與未過期條件，才能拒絕A的舊結果。</p></details>

## 執行與驗收

執行 `python lab20.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab20.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
