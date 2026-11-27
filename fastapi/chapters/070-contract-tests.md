# 回應、OpenAPI 與下載包契約測試

驗證讀者真正拿到的成品，不只驗作者工作目錄。

## 公開介面要能讀回

測試實際GET OpenAPI，核對Bearer、SSE媒體型別與狀態碼；讀取原生JSONL逐行解析；錯誤回應檢查不含原始秘密。自訂response class、schema或框架升級時，這些契約很容易受到影響。

## 程式包內容完整

ZIP要包含gateway、migrations、32個實驗入口、requirements、client、Dockerfile與dockerignore。模板或無副檔名檔案若被建置器漏掉，作者目錄能執行不表示讀者解壓後能用。本課以明列的檔名和副檔名納入必要資源。

## 乾淨解壓驗收

核對ZIP每個來源檔案，解壓到新目錄，再跑測試及真實TCP。排除.runtime、.venv、私人資料庫與秘密。學習包內的相對圖解連結也要在沒有原網站目錄時可用，才能算真正可攜。

## 對照完整專案

以下節錄 `gateway/api.py` 的 `PrivateEventSourceResponse`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class PrivateEventSourceResponse(EventSourceResponse):
    def __init__(self, content, status_code: int = 200, headers=None, media_type=None, background=None):
        headers = dict(headers or {}) | {'Cache-Control': 'no-store', 'X-Accel-Buffering': 'no'}
        super().__init__(content, status_code=status_code, headers=headers, media_type=media_type, background=background)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大回應、OpenAPI 與下載包契約測試圖解"><img src="assets/figures/24.svg" alt="故障點相對commit的位置會決定重試應讀舊結果或重新計算。" loading="lazy"></a><figcaption>故障注入與恢復驗收。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「回應、OpenAPI 與下載包契約測試」讀圖：判斷四個斷點中哪些可能重算，哪些只能重送回應。再用本節的條件回答：原始目錄可以跑，為何仍要解壓ZIP再測？</p></div>

## 自我檢查與解析

**問題：**原始目錄可以跑，為何仍要解壓ZIP再測？

<details><summary>展開解析</summary><p>下載包可能漏檔、混入執行產物或相對路徑依賴；只有乾淨解壓才能驗證讀者實際取得的成品。</p></details>

## 執行與驗收

執行 `python lab01.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab01.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/testing/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
