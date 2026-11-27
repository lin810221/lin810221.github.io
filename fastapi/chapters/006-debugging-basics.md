# 讀懂第一個錯誤並建立排查順序

先分清連不上、路由不符、驗證失敗與服務規則拒絕。

## 由外向內定位

連線拒絕時先檢查程序、監聽位址與port；404核對實際路徑和前綴；405核對method；422閱讀欄位位置與錯誤類型；401檢查憑證是否存在或已撤銷；403表示身分已識別但沒有該操作權限。500則需用request ID對照伺服器紀錄。

## 建立可重現的最小請求

保留method、path、必要標頭、最小body和預期結果。刪除真實秘密、客戶資料和不必要文件，只用合成案例重現。不要把整段Authorization、完整問題或模型原文貼進公開issue；本課錯誤回應刻意不回傳Pydantic原始input。

## 一次只改一個條件

先用健康檢查確認服務，再用OpenAPI確認契約，接著加入認證，最後加入業務資料。request ID可讓客戶端回報與伺服器紀錄對上，但它不是授權憑證，也不能直接信任任意使用者輸入作為log結構。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `validation_error`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @app.exception_handler(RequestValidationError)
    async def validation_error(request, error):
        # Pydantic's raw errors can include rejected secrets in input/ctx.
        details = [{'location': list(x['loc']), 'type': x['type']} for x in error.errors()]
        return JSONResponse({'error': {'code': 'invalid_request', 'details': details, 'request_id': request.state.request_id}}, status_code=422)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大讀懂第一個錯誤並建立排查順序圖解"><img src="assets/figures/02.svg" alt="HTTP與WebSocket訊息分流，啟動和關閉管理共享資源。" loading="lazy"></a><figcaption>ASGI 訊息與 lifespan。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「讀懂第一個錯誤並建立排查順序」讀圖：分辨HTTP請求、WebSocket連線與伺服器生命週期。再用本節的條件回答：422和500在排錯上最大的差別是什麼？</p></div>

## 自我檢查與解析

**問題：**422和500在排錯上最大的差別是什麼？

<details><summary>展開解析</summary><p>422是可預期的輸入契約不符合；500代表未妥善處理的服務端問題，應核對紀錄與程式，而不是要求使用者不斷重送同一資料。</p></details>

## 執行與驗收

執行 `python lab04.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab04.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/handling-errors/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
