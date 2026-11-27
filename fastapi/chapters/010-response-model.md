# Response Model 與 DTO

控制公開輸出，避免把內部資料模型當成對外契約。

## 內部資料通常比公開資料多

Document的ORM資料還有tenant與digest，公開DocumentOut只含id、title、text。JobOut不包含冪等鍵、請求指紋或租約token。這些資訊是伺服器控制狀態，不應因序列化ORM物件而外洩。

## 輸出驗證不是輸入驗證

當服務回傳不符合response model的資料，通常是程式錯誤，不應假裝成使用者輸入的422。錯誤紀錄要保留足夠診斷資訊，但公開回應不應洩漏資料列或模型供應商憑證。

## schema與事實是不同層次

Answer模型限制status、文字和引用欄位，但即使JSON形狀合法，document_id也可能指向別人，quote也可能對不上區間。後續還要核對允許文件、座標與原文。本課離線抽句版本再要求答案文字等於引用句，減少自由改寫的未證實內容。

## 對照完整專案

以下節錄 `gateway/contracts.py` 的 `JobOut`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class JobOut(StrictModel):
    id: str
    state: Literal['queued', 'running', 'succeeded', 'failed', 'cancelled']
    attempt: int
    cancel_requested: bool
    result: Answer | None
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大Response Model 與 DTO圖解"><img src="assets/figures/04.svg" alt="401、403、404、409、422與413對應不同邊界。" loading="lazy"></a><figcaption>狀態碼是回應契約。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Response Model 與 DTO」讀圖：用反例分辨認證、授權、衝突與輸入錯誤。再用本節的條件回答：response model會自動檢查引用屬於目前租戶嗎？</p></div>

## 自我檢查與解析

**問題：**response model會自動檢查引用屬於目前租戶嗎？

<details><summary>展開解析</summary><p>不會。它檢查形狀；租戶與引用內容須由服務規則另外驗證，不能把schema通過當成證據通過。</p></details>

## 執行與驗收

執行 `python lab17.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab17.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/response-model/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
