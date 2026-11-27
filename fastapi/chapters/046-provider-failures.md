# 上游錯誤、斷路與拒絕服務政策

把暫時不可用、永久錯誤與不符合輸出契約分開處理。

## 可分類的失敗

連線失敗、429或5xx可能暫時性；401、模型不存在或參數不支援通常要修設定；refusal與incomplete則屬模型結果狀態。不要把所有情況包成空字串成功，也不要把上游原始錯誤包含的秘密直接回傳。

## 斷路器與重試不是同一件事

重試處理一次請求內的暫時性；斷路器根據一段時間的失敗暫停新呼叫，再以有限探測恢復。正式需要定義open、half-open與close狀態、共享範圍和時間窗。本課沒有部署跨實例斷路服務，不以示意流程宣稱已有完整治理。

## 明確拒絕比無界排隊可控

連線、GPU或帳戶配額不足時，應有可說明的排隊和拒絕政策。worker失敗保存安全code，API可回工作failed讓客戶端查詢；監控另外計算錯誤類型與上游狀態，避免故障只留在背景程序stdout。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `fail`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def fail(self, claim, now):
        with Session(self.engine) as session, session.begin():
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.get(Job, claim['id'])
            if row and row.state == 'running' and row.lease_token == claim['token'] and row.lease_until > now:
                row.state = 'cancelled' if row.cancel_requested else 'failed'
                row.lease_until = 0
                session.add(Event(job_id=row.id, kind=row.state, data_json=canonical({'code': 'work_failed'})))
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大上游錯誤、斷路與拒絕服務政策圖解"><img src="assets/figures/16.svg" alt="暫時性GET錯誤有限重試，模型POST需考慮重複扣費。" loading="lazy"></a><figcaption>可重試錯誤與副作用。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「上游錯誤、斷路與拒絕服務政策」讀圖：在回應遺失而遠端已扣費的時間點，分析重試風險。再用本節的條件回答：沒有斷路器時，增加十次重試能保證上游恢復嗎？</p></div>

## 自我檢查與解析

**問題：**沒有斷路器時，增加十次重試能保證上游恢復嗎？

<details><summary>展開解析</summary><p>不能，可能放大故障與成本。應限制次數和總期限，並按服務需求另設斷路、排隊或拒絕策略。</p></details>

## 執行與驗收

執行 `python lab28.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab28.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.python-httpx.org/advanced/timeouts/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
