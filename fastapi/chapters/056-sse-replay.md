# 持久化事件與 Last-Event-ID 回放

游標只代表讀到哪裡；事件本身要先被可靠保存。

## 發布前先保存

工作狀態與對應Event在同一資料庫交易寫入，串流只是讀取已提交事件。連線中斷後，客戶端提供Last-Event-ID；伺服器先核對租戶與job，再讀取後續事件，不重新計算工作。

## 游標的定義

令$j$為已授權工作，$c\geq0$為最後已處理的事件ID。下一批事件集合為：

$$E_{j,c}=\{e\mid e.\mathrm{job\_id}=j\ \land\ e.\mathrm{id}>c\}.$$

按id升序、每批最多100筆。本課id全表遞增，單一工作的事件可能是3、6、8，不保證連號。cursor為6時只回8，不能用「上次ID加一等於下一筆」的假設找資料。

## 客戶端去重與保留政策

保存最後成功處理的ID，重連後按ID去重。若正式系統會刪除歷史事件，需定義過期cursor的錯誤或快照恢復，本課尚未實作事件保留清除，不能宣稱任意舊游標永久可恢復。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `events`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def events(self, tenant, identifier, after=0):
        self.job(tenant, identifier)
        with Session(self.engine) as session:
            rows = session.scalars(select(Event).where(Event.job_id == identifier, Event.id > after).order_by(Event.id).limit(100))
            return [{'id': row.id, 'event': row.kind, 'data': json.loads(row.data_json)} for row in rows]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大持久化事件與 Last-Event-ID 回放圖解"><img src="assets/figures/19.svg" alt="id、event、data及空白行形成一個事件，切包位置不固定。" loading="lazy"></a><figcaption>SSE 事件不是 TCP 封包。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「持久化事件與 Last-Event-ID 回放」讀圖：在事件中間切開網路chunk，說明為何必須保留解析緩衝。再用本節的條件回答：同一工作事件ID是3、6、8，游標為6要回哪些？</p></div>

## 自我檢查與解析

**問題：**同一工作事件ID是3、6、8，游標為6要回哪些？

<details><summary>展開解析</summary><p>只回已授權工作中id大於6的事件，此例為8；不要求ID連續，也不能讀其他工作的事件。</p></details>

## 執行與驗收

執行 `python lab22.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab22.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/server-sent-events/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
