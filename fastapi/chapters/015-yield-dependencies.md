# yield 依賴與資源所有權

取得資源與歸還資源必須屬於同一個清楚的範圍。

## 前半取得，後半清理

yield前建立資源，yield交給使用者，finally確保正常、例外或取消都能清理。不是所有資源都需要依賴yield：本課engine由lifespan管理，短Session由store方法的context manager管理；實驗另外用簡單resource觀察框架行為。

## 所有權比語法重要

誰建立資源，誰負責在正確時間關閉。不要把請求Session傳給BackgroundTasks，或把在路由內with已關閉的client交給串流generator。即使Python仍持有物件參照，底層連線也可能已被回收。

## 取消時也要做清理

使用try/finally保護釋放流程，不任意吞掉CancelledError。非同步取消是合作式的，不會讓所有外部副作用回滾；已送出的模型請求或已提交資料仍需要明確恢復策略。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `resource`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    async def resource():
        app.state.trace.append('open')
        try:
            yield 'resource'
        finally:
            app.state.trace.append('close')
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大yield 依賴與資源所有權圖解"><img src="assets/figures/05.svg" alt="Bearer與store是共享子依賴，principal判定身分再傳入editor。" loading="lazy"></a><figcaption>依賴圖與單次請求快取。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「yield 依賴與資源所有權」讀圖：追蹤兩條路徑為何能重用同一依賴結果。再用本節的條件回答：路由回傳generator後，為何with資源可能已關閉？</p></div>

## 自我檢查與解析

**問題：**路由回傳generator後，為何with資源可能已關閉？

<details><summary>展開解析</summary><p>路由函式可能已結束，而generator是在之後傳送body時才迭代。資源生命週期必須涵蓋實際使用時點。</p></details>

## 執行與驗收

執行 `python lab06.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab06.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
