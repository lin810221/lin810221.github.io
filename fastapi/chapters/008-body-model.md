# Request Body 與 Pydantic 模型

把輸入契約寫成明確型別，而不是到處使用不受限dict。

## 模型定義可接受的形狀

`DocumentIn`只接受title與text，拒絕額外欄位、空白內容與NUL；`JobIn`要求非空問題和有限文件ID。title長度以字元數衡量，HTTP body限制以位元組衡量，兩者不可互相替代。中文經UTF-8編碼後通常占多個位元組。

## 不接受呼叫者自稱的身分

body沒有tenant欄位，租戶來自驗證過的憑證。若讓使用者在body任意指定tenant，即使Pydantic驗證字串格式正確，仍可能變成跨租戶存取。型別驗證只負責形狀，無法代替資源授權。

## JSON與表單分開

JSON端點接受`application/json`；上傳端點使用`multipart/form-data`。不要在同一個HTTP body期待一方面是裸JSON物件，另一方面又是檔案表單；需要JSON metadata時可設計表單欄位內的JSON文字並再做明確驗證，本課上傳主線不開放額外文字欄位。

## 對照完整專案

以下節錄 `gateway/contracts.py` 的 `DocumentIn`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class DocumentIn(StrictModel):
    title: str = Field(min_length=1, max_length=120)
    text: str = Field(min_length=1, max_length=4096)

    @field_validator('title', 'text')
    @classmethod
    def visible(cls, value):
        if not value.strip() or '\x00' in value:
            raise ValueError('nonempty visible text required')
        return value
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大Request Body 與 Pydantic 模型圖解"><img src="assets/figures/03.svg" alt="同一份請求經過型別驗證、服務規則與輸出過濾。" loading="lazy"></a><figcaption>輸入與輸出契約。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Request Body 與 Pydantic 模型」讀圖：為型別、權限與事實三種錯誤安排不同檢查。再用本節的條件回答：title是合法字串，就能相信tenant也是使用者自己的嗎？</p></div>

## 自我檢查與解析

**問題：**title是合法字串，就能相信tenant也是使用者自己的嗎？

<details><summary>展開解析</summary><p>不能。型別和授權是兩層責任；本課根本不接受body指定tenant，而由憑證映射後加入查詢條件。</p></details>

## 執行與驗收

執行 `python lab02.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab02.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.pydantic.dev/latest/concepts/models/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
