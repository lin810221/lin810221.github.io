# 對稱對比損失與溫度

用小矩陣看懂正配對如何和其他候選競爭。

## 以圖找文

batch有 $N$ 組正配對，$s_{ij}$ 為圖片 $i$ 和文字 $j$ 的相似度，$	au>0$ 為溫度。單一圖片方向的損失為：

$$
\ell_i=-\log\frac{\exp(s_{ii}/\tau)}{\sum_{j=1}^{N}\exp(s_{ij}/\tau)}.
$$

對角線代表正配對；分母包含該圖片在batch內的所有候選。較小溫度讓相對差異更集中，但不會產生新的來源資訊，也不等於越小越好。

## 兩個方向

交換圖文角色再計算一次，本課取兩方向平均：

$$
L=\tfrac12\left(L_{I\to T}+L_{T\to I}\right).
$$

二乘二矩陣對角線為1、其他為0時，比把正配對交換的矩陣有較低損失。程式用穩定的log-sum-exp計算，避免極小溫度造成數值溢位。

## 本課算例的界線

這是手工相似度矩陣的損失演算，沒有訓練影像或文字編碼器，不把它稱為已學到語意。若要真正訓練，還需要資料、模型、梯度、最佳化與獨立測試，可接深度學習與PyTorch課程。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `contrastive_loss`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def contrastive_loss(similarities,temperature=.1):
    n=len(similarities)
    if not n or any(len(r)!=n for r in similarities) or not math.isfinite(temperature) or temperature<=0:raise ValueError('Square paired matrix and positive temperature required')
    def direction(matrix):
        losses=[]
        for i,row in enumerate(matrix):
            if any(not math.isfinite(v) for v in row):raise ValueError('Nonfinite similarity')
            logits=[x/temperature for x in row];m=max(logits)
            losses.append(m+math.log(sum(math.exp(x-m) for x in logits))-logits[i])
        return sum(losses)/n
    return (direction(similarities)+direction(list(zip(*similarities))))/2
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大對稱對比損失與溫度示意圖"><img src="assets/figures/15.svg" alt="找出兩個方向的正例與負例，說明batch內重複語意為何可能形成假負例。" loading="lazy"></a><figcaption>範例用手工矩陣演算損失，不冒稱訓練出CLIP。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「對稱對比損失與溫度」讀圖：找出兩個方向的正例與負例，說明batch內重複語意為何可能形成假負例。本單元請再回答：把手工矩陣的對比損失算得很小，能否宣稱訓練出可用的圖文embedding？</p></div>

## 自我檢查與解析

**問題：**把手工矩陣的對比損失算得很小，能否宣稱訓練出可用的圖文embedding？

<details><summary>展開解析</summary><p>不能。這只驗證目標函數演算；真正embedding需由編碼器和資料學習，並在未見的目標任務驗收。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab15.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab15.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2103.00020)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
