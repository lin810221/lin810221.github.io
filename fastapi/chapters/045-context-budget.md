# Context、輸出上限與成本預算

模型參數是服務契約的一部分，不能只暴露任意數字給客戶端。

## 上下文有共同預算

令$C$為所選模型可用context token上限，$S$為系統與任務設定，$Q$為問題，$R$為檢索內容，$O$為保留輸出。作為規劃檢查：

$$S+Q+R+O\leq C.$$

各項均以同一模型tokenizer計數的非負token數表示；不能用字元數或中文固定倍率當成精確token數。例如$C=8000$、$S=800$、$Q=200$、$R=5000$、$O=1000$時總額7000，還有1000餘量。

## 伺服器決定可接受上限

限制文件數、原文字元、總輸入bytes、輸出token與整體期限，再依實際模型tokenizer計算。temperature、reasoning相關參數與工具支援會依模型不同，不要把一份任意參數dict直接轉發到所有供應商。

## 成本應保留口徑

計畫值、供應商實際usage、重試和已計費未交付分開記錄。本課不提供即時價格表；需要估價時查當日官方價格與模型口徑，避免把示意算例當成正式報價。

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

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大Context、輸出上限與成本預算圖解"><img src="assets/figures/15.svg" alt="離線抽句和OpenAI adapter共享答案形狀，但能力與實測不同。" loading="lazy"></a><figcaption>供應商介面與輸出驗證。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Context、輸出上限與成本預算」讀圖：說明mock成功、結構成功與答案正確不能互相代替。再用本節的條件回答：中文文字長度4096是否等於4096個token？</p></div>

## 自我檢查與解析

**問題：**中文文字長度4096是否等於4096個token？

<details><summary>展開解析</summary><p>不等於。字元、UTF-8 bytes與模型token不同；容量和費用須依所選模型與官方計數口徑驗證。</p></details>

## 執行與驗收

執行 `python lab30.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab30.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://developers.openai.com/api/reference/resources/responses/methods/create)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
