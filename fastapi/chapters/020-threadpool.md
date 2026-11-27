# 同步程式、執行緒池與競爭

把阻塞移出事件迴圈後，仍要管理共享狀態與有限容量。

## 執行緒池也會滿

FastAPI與Starlette共用底層非同步工具的執行緒資源，檔案、同步路由和部分依賴可能競爭同一容量。大量阻塞工作即使不再堵住事件迴圈，也可能因等待執行緒或資料庫連線而增加延遲。

## Session不能跟著任意搬動

engine可以管理多個連線，但Session代表一組可變交易狀態。把同一Session放到多個執行緒使用會造成競爭。RelayDesk每個store方法建立自己的Session；對共享寫入規則則使用資料庫交易和唯一約束，而不是只靠Python的先查再寫。

## 取消不一定能停止執行緒工作

取消等待中的協程不等於強制殺掉底層同步函式。耗時工作應有自己的timeout、可檢查停止點或程序隔離；不能以為to_thread加上一層asyncio timeout就能撤回已發生的資料庫或網路副作用。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `documents`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    def documents(self, tenant, after=0, limit=20):
        with Session(self.engine) as session:
            rows = session.scalars(select(Document).where(Document.tenant == tenant, Document.id > after, Document.deleted == 0).order_by(Document.id).limit(limit))
            return [self._document(row) for row in rows]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大同步程式、執行緒池與競爭圖解"><img src="assets/figures/07.svg" alt="非同步等待能交錯，直接sleep會延後其他請求。" loading="lazy"></a><figcaption>等待 I/O 與阻塞事件迴圈。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「同步程式、執行緒池與競爭」讀圖：在等待區間插入第二個請求，再比較阻塞版本。再用本節的條件回答：把同一Session包在to_thread中呼叫兩次可以並行嗎？</p></div>

## 自我檢查與解析

**問題：**把同一Session包在to_thread中呼叫兩次可以並行嗎？

<details><summary>展開解析</summary><p>不應共用同一可變Session。每個獨立工作建立自己的Session，交易衝突由資料庫約束和鎖處理。</p></details>

## 執行與驗收

執行 `python lab16.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab16.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://www.starlette.dev/threadpool/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
