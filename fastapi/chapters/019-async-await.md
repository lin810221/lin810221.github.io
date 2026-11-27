# async def 與 def 的選擇

先辨識等待型與阻塞型操作，再決定函式放在哪裡執行。

## 非同步是合作式交錯

async函式遇到可等待I/O時讓出事件迴圈，其他請求才有機會執行。單純把函式改成async，不會把同步HTTP、檔案讀寫或CPU計算變成非阻塞。`time.sleep`與同步資料庫操作若直接放進async路由，可能拖住整個事件迴圈。

## FastAPI的路由執行方式

同步def路由與同步依賴通常由執行緒池執行；async路由直接在事件迴圈執行。RelayDesk同步SQLAlchemy操作由同步路由使用，非同步上傳或SSE需要呼叫store時，用明確的to_thread邊界。

## CPU工作另行評估

大量token處理、影像推論或模型載入可能需要程序、專用模型服務或GPU排程。執行緒不保證Python CPU工作加速，也不提供資料競爭的自動保護。先用可觀察的等待和峰值實驗建立直覺，再量測真實工作。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `limited_work`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.get('/limited')
    async def limited_work(value: Annotated[None, limited]):
        await asyncio.sleep(.01)
        return {'ok': True}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大async def 與 def 的選擇圖解"><img src="assets/figures/07.svg" alt="非同步等待能交錯，直接sleep會延後其他請求。" loading="lazy"></a><figcaption>等待 I/O 與阻塞事件迴圈。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「async def 與 def 的選擇」讀圖：在等待區間插入第二個請求，再比較阻塞版本。再用本節的條件回答：async路由裡呼叫同步requests.get會自動進執行緒池嗎？</p></div>

## 自我檢查與解析

**問題：**async路由裡呼叫同步requests.get會自動進執行緒池嗎？

<details><summary>展開解析</summary><p>不會。普通函式呼叫照原方式執行；需要使用非同步client，或明確放到適當執行緒邊界。</p></details>

## 執行與驗收

執行 `python lab07.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab07.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/async/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
