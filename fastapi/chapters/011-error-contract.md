# 設計可追蹤又不洩漏秘密的錯誤

狀態碼、錯誤代碼與request ID一起構成可操作的失敗介面。

## 可預期的領域錯誤

DomainError包含HTTP狀態和穩定代碼，例如`idempotency_conflict`、`document_not_found`和`stale_lease`。HTTP層統一轉成JSON；store不直接依賴FastAPI例外，使獨立worker也能使用相同規則。

## 驗證錯誤也可能包含秘密

Pydantic原始errors可能有input與ctx，直接回傳時可能把遭拒的秘密內容送回客戶端或寫進log。本課只公開錯誤位置與類型；不要以為只有成功回應才需要資料最小化。401保留Bearer challenge，幫助客戶端判斷認證方式。

## 對外穩定，對內可查

request ID在入口核對長度與字元，非法輸入則產生新ID。代碼應保持穩定，文字訊息可調整；對外不要回傳完整traceback。營運監控則須區分使用者錯誤、暫時性上游錯誤與程式缺陷，避免把所有失敗算成同一類。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `domain_error`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.exception_handler(DomainError)
    async def domain_error(request, error):
        headers = {'WWW-Authenticate': 'Bearer'} if error.status == 401 else None
        return JSONResponse({'error': {'code': error.code, 'request_id': request.state.request_id}}, status_code=error.status, headers=headers)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大設計可追蹤又不洩漏秘密的錯誤圖解"><img src="assets/figures/04.svg" alt="401、403、404、409、422與413對應不同邊界。" loading="lazy"></a><figcaption>狀態碼是回應契約。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「設計可追蹤又不洩漏秘密的錯誤」讀圖：用反例分辨認證、授權、衝突與輸入錯誤。再用本節的條件回答：為何不能直接把error.errors()回傳？</p></div>

## 自我檢查與解析

**問題：**為何不能直接把error.errors()回傳？

<details><summary>展開解析</summary><p>它可能包含原始input或驗證context；若輸入是秘密或私人文件，就會擴大洩漏範圍。只回傳必要位置、類型與追蹤識別。</p></details>

## 執行與驗收

執行 `python lab02.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab02.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/handling-errors/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
