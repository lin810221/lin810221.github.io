# 風險、覆蓋率與信心校準

自動接受多少和接受後錯多少，必須一起看。

## 定義接受集合

共有 $N>0$ 筆評估，門檻 $\tau$ 保留集合 $A_\tau$，其中錯誤筆數為 $E_\tau$。覆蓋率與保留風險為：

$$
C(\tau)=\frac{|A_\tau|}{N},\qquad R(\tau)=\frac{E_\tau}{|A_\tau|}.
$$

沒有保留資料時，風險未定義；不能用零讓圖看起來完美。四筆fixture在0.9門檻保留兩筆，其中一筆錯，覆蓋率與風險皆為 $1/2$。

## 門檻不是校準

提高門檻會改變保留集合，但小樣本風險不保證單調下降；最高分也可能錯。校準要把預測分數和獨立資料的實際正確頻率比較，按領域偏移重新檢查，不能只把softmax或OCR內部分數改名confidence。

## 連到人工容量

低覆蓋意味更多人工工作；高覆蓋可能增加錯誤成本。依欄位重要性、文件種類和實際人力制定政策，並觀測來源缺漏、拒答與覆核原因。不能只用一個門檻替代所有硬性業務規則。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `risk_coverage`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def risk_coverage(scores,correct,threshold):
    if len(scores)!=len(correct) or any(not 0<=s<=1 for s in scores) or not 0<=threshold<=1:raise ValueError('Invalid confidence fixture')
    selected=[ok for s,ok in zip(scores,correct) if s>=threshold]
    return {'coverage':len(selected)/len(scores) if scores else None,'risk':sum(not x for x in selected)/len(selected) if selected else None}
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大風險、覆蓋率與信心校準示意圖"><img src="assets/figures/24.svg" alt="在門檻0.9下數保留筆數與錯誤筆數，再說明提高門檻不保證每個小樣本的風險單調下降。" loading="lazy"></a><figcaption>這四筆是教學fixture，不是模型準確度報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「風險、覆蓋率與信心校準」讀圖：在門檻0.9下數保留筆數與錯誤筆數，再說明提高門檻不保證每個小樣本的風險單調下降。本單元請再回答：沒有任何資料通過門檻時，為什麼不把保留風險記成0？</p></div>

## 自我檢查與解析

**問題：**沒有任何資料通過門檻時，為什麼不把保留風險記成0？

<details><summary>展開解析</summary><p>因為分母為零，沒有觀測到可評估的保留結果。應標未定義並同時顯示零覆蓋，避免誤導成完美系統。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab24.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab24.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/1706.04599)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
