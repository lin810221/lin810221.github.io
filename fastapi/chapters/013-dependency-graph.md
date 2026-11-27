# Depends：把依賴關係寫成可檢查的圖

從Bearer到principal再到editor，重用的是責任清楚的可呼叫物件。

## 依賴不是一般函式呼叫

`Depends(principal)`交給框架在每次請求解析；不要寫成`Depends(principal())`。principal依賴Bearer解析結果和store；editor再使用principal結果判斷角色。路由只宣告自己需要Editor或Identity，不重複貼認證程式。

## 單次請求的依賴快取

相同依賴在一個請求中通常重用結果，可避免重複驗證或開多個相同資源。這不表示跨請求共用使用者資料，也不是LLM prompt cache。若使用`use_cache=False`，應有可說明的理由與測試，不應用來修補不清楚的全域狀態。

## 讓資料層保持獨立

get_store取回共享engine的包裝，但每個store操作自行建立短Session。engine可跨請求使用，Session不能任意跨執行緒或並行工作共享。依賴圖讓這個生命週期差異更容易被檢查。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `principal`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def principal(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], store: Annotated[Store, Depends(get_store)]):
    if credentials is None or credentials.scheme.lower() != 'bearer' or len(credentials.credentials) > 512:
        raise DomainError(401, 'unauthorized')
    return store.identity(credentials.credentials)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener" aria-label="放大Depends：把依賴關係寫成可檢查的圖圖解"><img src="assets/figures/05.svg" alt="Bearer與store是共享子依賴，principal判定身分再傳入editor。" loading="lazy"></a><figcaption>依賴圖與單次請求快取。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Depends：把依賴關係寫成可檢查的圖」讀圖：追蹤兩條路徑為何能重用同一依賴結果。再用本節的條件回答：Depends快取可以存放上一次使用者的權限嗎？</p></div>

## 自我檢查與解析

**問題：**Depends快取可以存放上一次使用者的權限嗎？

<details><summary>展開解析</summary><p>不能。依賴快取是單一請求的求值重用；跨請求權限快取需要租戶、身分、失效與撤銷政策，不能混為一談。</p></details>

## 執行與驗收

執行 `python lab03.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab03.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/dependencies/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
