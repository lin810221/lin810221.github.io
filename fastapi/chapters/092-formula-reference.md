# 容量、期限與成本公式速查

公式用來整理假設與單位，不代替真實量測。

## 成本的明確口徑

令$I,O\geq0$為本次按相應官方口徑計價的輸入與輸出token數，$p_I,p_O\geq0$為每一百萬token的同幣別價格：

$$C=\frac{I p_I+O p_O}{10^6}.$$

示意輸入2000、輸出500、價格分別為每百萬2與8個貨幣單位，計算為0.008。這些是虛構算例，不是任何模型現行報價；快取、工具、推理token、重試或其他項目需按真實供應商口徑另外計入。

## 將公式連回責任

Little定律用同一穩定系統邊界的平均率與時間，不能當瞬間上限；token bucket以單調時間補充；nearest-rank以非空有限樣本取秩；deadline包含退避；記憶體乘數需註明共享假設。API參數名稱與可複製程式碼仍保持程式碼格式。

## 重新代入前先問

數字是否同單位、同模型、同資料範圍、同時間窗口？是否把平均誤當上限、把模擬誤當實測？先核對這些問題，再用公式決定下一個需要量測的量，而不是直接宣布容量已足夠。

## 對照完整專案

以下節錄 `gateway/resilience.py` 的 `nearest_rank`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
def nearest_rank(samples, quantile):
    if not samples or not 0 < quantile <= 1 or any(not math.isfinite(x) or x < 0 for x in samples):
        raise ValueError('nonempty finite observations required')
    values = sorted(samples)
    return values[math.ceil(quantile * len(values)) - 1]
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大容量、期限與成本公式速查圖解"><img src="assets/figures/22.svg" alt="穩定系統下，抵達速率乘平均停留時間得到平均在途數。" loading="lazy"></a><figcaption>平均並行量與工作行程。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「容量、期限與成本公式速查」讀圖：用相同平均值構造不同突發流量，說明還缺少哪些資訊。再用本節的條件回答：為何不能把示意價格0.008當成正式預算？</p></div>

## 自我檢查與解析

**問題：**為何不能把示意價格0.008當成正式預算？

<details><summary>展開解析</summary><p>它採虛構單價且未包含所有可能費用；正式估價需當日官方價格、真實usage與重試等完整口徑。</p></details>

## 執行與驗收

執行 `python lab31.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab31.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://developers.openai.com/api/reference/resources/responses/methods/create)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
