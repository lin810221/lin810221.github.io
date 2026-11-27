# AsyncSession 與非同步驅動

非同步資料庫需要對應驅動，不能只替換函式名稱。

## engine、Session與driver成套使用

`create_async_engine`、`async_sessionmaker`和非同步資料庫driver一起運作。教學實驗使用`sqlite+aiosqlite`實際執行SQL；SQLAlchemy的asyncio extra需要greenlet，本課完整鎖版已納入，避免只安裝基礎SQLAlchemy後才在執行時失敗。

## 一個task一個Session

AsyncSession仍是可變交易狀態，不適合在gather裡讓多個task共享。每個獨立task建立自己的Session，再以資料庫交易協調。若業務必須原子化多個修改，就應在同一明確交易依序完成，而不是任意拆成並行task。

## 選擇應依實際瓶頸

同步資料庫搭配def路由也能形成清楚的小型服務。改成async不保證查詢變快，更不會消除鎖衝突或慢SQL。先量測等待比例、連線池與資料庫容量，再決定是否遷移；本課主專案保留同步Session，另用實驗驗證async行為。

## 對照完整專案

以下節錄 `gateway/mechanics.py` 的 `async_database_example`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
async def async_database_example():
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    factory = async_sessionmaker(engine)
    try:
        async with factory() as session, session.begin():
            value = await session.scalar(text('SELECT 6 * 7'))
        return value
    finally:
        await engine.dispose()
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener" aria-label="放大AsyncSession 與非同步驅動圖解"><img src="assets/figures/10.svg" alt="資料列按id排列，以大於上次id取得下一頁。" loading="lazy"></a><figcaption>keyset 依穩定鍵續讀。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「AsyncSession 與非同步驅動」讀圖：比較先篩租戶與取頁後才過濾的不同結果。再用本節的條件回答：gather十個查詢時可以共用一個AsyncSession嗎？</p></div>

## 自我檢查與解析

**問題：**gather十個查詢時可以共用一個AsyncSession嗎？

<details><summary>展開解析</summary><p>不應如此。每個並行task應有自己的Session；若要同一原子交易，改成清楚的交易流程而非共用可變Session並行操作。</p></details>

## 執行與驗收

執行 `python lab08.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab08.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
