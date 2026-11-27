# 取消 queued 與 running 工作

明確定義取消生效點，避免向使用者承諾做不到的即時中止。

## queued可立即終止

尚未執行的工作改成cancelled，後續claim不再選它。running則記錄cancel_requested，避免用一個HTTP呼叫假裝能強制停止所有外部計算。重複取消是可重送操作，不新增無限相同事件。

## 發布前重新核對

worker在呼叫provider前先讀取消狀態；若已取消就不開始上游。計算期間收到取消，finish交易也會看到標記，轉為cancelled而不保存正常答案。已發生的上游費用或其他副作用不保證撤回。

## 取消與租約共同作用

取消端點和finish都使用明確寫入交易，使同時操作有可定義結果。若先成功提交，再收到取消，本課保留已成功狀態；如果取消先取得並提交，finish會遵守取消。測試應檢查兩種順序，不只測單一路徑。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `cancel`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def cancel(self, tenant, identifier):
        with Session(self.engine) as session, session.begin():
            # SQLite obtains its writer lock before checking state.
            session.execute(text('BEGIN IMMEDIATE'))
            row = session.scalar(select(Job).where(Job.id == identifier, Job.tenant == tenant))
            if row is None:
                raise DomainError(404, 'job_not_found')
            if row.state in {'queued', 'running'} and not row.cancel_requested:
                row.cancel_requested = 1
                if row.state == 'queued':
                    row.state = 'cancelled'
                session.add(Event(job_id=row.id, kind='cancel_requested', data_json=canonical({'state': row.state})))
            return self._job(row)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大取消 queued 與 running 工作圖解"><img src="assets/figures/18.svg" alt="A失去租約後，B重新claim取得新token，A不能再發布。" loading="lazy"></a><figcaption>租約過期與 fencing。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「取消 queued 與 running 工作」讀圖：分別檢查到期時間與擁有者token，找出只驗時間的漏洞。再用本節的條件回答：答案已commit為succeeded後才按取消，能把已發生的扣費回滾嗎？</p></div>

## 自我檢查與解析

**問題：**答案已commit為succeeded後才按取消，能把已發生的扣費回滾嗎？

<details><summary>展開解析</summary><p>不能。本課保留已成功狀態；取消只能依明確生效點影響尚未完成工作，外部副作用須另有補償機制。</p></details>

## 執行與驗收

執行 `python lab21.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab21.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.python.org/3.15/library/asyncio-task.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
