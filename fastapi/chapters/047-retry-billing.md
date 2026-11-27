# 模型重試、冪等與用量對帳

本地只建立一份工作，不代表遠端只執行或計費一次。

## 結果遺失的模糊區間

請求送出後遠端可能已完成推論，但本地在讀取回應前中斷。重新呼叫可能再次計費；若只看本地沒有結果就判斷沒執行，會低估風險。供應商是否支援冪等、查詢或usage對帳，要依該API正式契約確認。

## 至少一次與一次可見提交

RelayDesk租約到期後允許新worker重新計算，因此計算可能多次。fencing拒絕舊worker發布，結果與事件在一個資料庫交易內提交，保護本地可見狀態。這仍不是跨供應商、資料庫與客戶端的exactly-once保證。

## 記錄要能重建成本

保存工作ID、attempt、provider、model、使用量、開始結束與可見交付狀態，避免把所有attempt合併成一筆成功。若要自動重試付費呼叫，先定義費用上限、人工覆核與不可確定執行結果的處理。

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

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大模型重試、冪等與用量對帳圖解"><img src="assets/figures/16.svg" alt="暫時性GET錯誤有限重試，模型POST需考慮重複扣費。" loading="lazy"></a><figcaption>可重試錯誤與副作用。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「模型重試、冪等與用量對帳」讀圖：在回應遺失而遠端已扣費的時間點，分析重試風險。再用本節的條件回答：fencing成功是否表示兩個worker沒有重複呼叫模型？</p></div>

## 自我檢查與解析

**問題：**fencing成功是否表示兩個worker沒有重複呼叫模型？

<details><summary>展開解析</summary><p>不是。它控制誰能提交本地結果，不能取消已執行的遠端呼叫；重算與重複費用仍可能發生。</p></details>

## 執行與驗收

執行 `python lab20.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab20.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.sqlite.org/lang_transaction.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
