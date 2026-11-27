# Path 與 Query：把參數放在正確位置

資源識別、篩選與分頁各有自己的契約。

## path識別資源

`/jobs/{job_id}`使用path找一個工作；工作ID存在也不代表呼叫者能讀取。query適合`after`、`limit`等查詢選項。`limit`在本課只接受1到50，`after`不能為負值，資料層仍必須套用已識別租戶。

## 字串輸入與驗證規則

HTTP query本來是文字。FastAPI依參數宣告將合法文字轉成整數，再檢查界線；JSON body的strict模型則刻意拒絕字串整數與布林冒充ID。兩種入口的轉換政策不同，文件與測試要寫清楚。

## 避免隱藏的無界查詢

將所有可回傳多筆資料的端點設上限，排序使用穩定且唯一的鍵。分頁游標表示續讀位置，不表示全資料庫的永久快照；同時新增資料時，需要先定義讀者可接受的可見性和一致性。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `documents`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @router.get('/documents', response_model=list[DocumentOut])
    def documents(user: Identity, store: Database, after: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=1, le=50)] = 20):
        return store.documents(user['tenant'], after, limit)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大Path 與 Query：把參數放在正確位置圖解"><img src="assets/figures/03.svg" alt="同一份請求經過型別驗證、服務規則與輸出過濾。" loading="lazy"></a><figcaption>輸入與輸出契約。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Path 與 Query：把參數放在正確位置」讀圖：為型別、權限與事實三種錯誤安排不同檢查。再用本節的條件回答：要求十萬筆資料後，能等資料庫查完再裁成50筆嗎？</p></div>

## 自我檢查與解析

**問題：**要求十萬筆資料後，能等資料庫查完再裁成50筆嗎？

<details><summary>展開解析</summary><p>不應如此。入口先拒絕或限制，SQL本身也要有LIMIT；否則網路回傳少量資料仍可能造成大量資料庫和記憶體消耗。</p></details>

## 執行與驗收

執行 `python lab12.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab12.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/query-params/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
