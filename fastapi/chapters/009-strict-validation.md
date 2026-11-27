# Strict、欄位驗證與正規化

明確決定哪些轉換能做，哪些應直接拒絕。

## 嚴格模式的目的

Python中bool是int的子類別，寬鬆轉換也可能讓文字數字變成ID。JobIn使用strict避免`true`被當作文件1。`extra='forbid'`讓拼錯欄位直接報錯，而不是默默忽略後造成錯誤預設值。

## 正規化要符合業務意義

文件ID清單不允許重複且必須為正整數；通過檢查後按ID排序，表示本課把指定文件視為集合。這個決定也讓同一組文件的不同排列產生相同請求指紋。若任務需要文件順序，排序就會改變意義，必須移除並調整冪等策略。

## 不要無聲修補

問題只有空白時直接拒絕，原文quote則保持原字串，不自動改標點或空白。正規化過的檢索文字與需要精確引用的原文可以分開保存，不能在取得字元座標後又修改原文而不更新座標。

## 對照完整專案

以下節錄 `gateway/contracts.py` 的 `JobIn`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
class JobIn(StrictModel):
    question: str = Field(min_length=1, max_length=300)
    document_ids: list[int] = Field(min_length=1, max_length=8)

    @field_validator('question')
    @classmethod
    def question_visible(cls, value):
        if not value.strip():
            raise ValueError('question required')
        return value

    @field_validator('document_ids')
    @classmethod
    def unique_ids(cls, value):
        if any(x <= 0 for x in value) or len(value) != len(set(value)):
            raise ValueError('positive unique IDs required')
        return sorted(value)
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大Strict、欄位驗證與正規化圖解"><img src="assets/figures/03.svg" alt="同一份請求經過型別驗證、服務規則與輸出過濾。" loading="lazy"></a><figcaption>輸入與輸出契約。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Strict、欄位驗證與正規化」讀圖：為型別、權限與事實三種錯誤安排不同檢查。再用本節的條件回答：把文件ID排序永遠正確嗎？</p></div>

## 自我檢查與解析

**問題：**把文件ID排序永遠正確嗎？

<details><summary>展開解析</summary><p>不是。只有當業務把文件集合視為無序時才正確；需要順序的任務應保留原順序並把順序納入指紋。</p></details>

## 執行與驗收

執行 `python lab02.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab02.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://docs.pydantic.dev/latest/concepts/strict_mode/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
