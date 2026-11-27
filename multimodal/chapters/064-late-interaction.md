# Late interaction與MaxSim

讓問題的不同token各自尋找頁面的局部匹配。

## 不先壓成一個向量

單向量把整頁聚合成一個表示；late interaction保留多個token表示，讓問題的各部分各自對頁面token比較。它能保留較細資訊，也增加儲存、計算與索引設計成本。token在視覺頁面中的語意和文字字詞不一定一對一。

## 正式定義

令 $q_i$ 為問題token向量，$p_j$ 為頁面token向量，使用非零向量的餘弦相似度：

$$
S(Q,P)=\sum_{i=1}^{m}\max_{1\le j\le n}s(q_i,p_j).
$$

每個問題token選一個最佳頁面匹配，再加總。兩個正交query向量和同樣的兩個page向量，分數為 $2$。同一個頁面token可以被多個query token選中；這不是一對一匹配。

## 比較的限制

分數受query長度和表示分布影響，不能當成固定機率或跨問題任意比較。本課函式只驗證代數與邊界；真實ColPali類模型還需要訓練表示、特定預處理和索引路線，不能以手工陣列的成功代替檢索品質。

## 完整專案中的實作

以下節錄 `examples/metrics.py` 的 `maxsim`；請使用完整程式包，保留匯入、依賴與fixture。

```python
def maxsim(query_tokens,page_tokens):
    if not query_tokens or not page_tokens:raise ValueError('Nonempty token sets required')
    return sum(max(cosine(q,p) for p in page_tokens) for q in query_tokens)
```

## 看圖追蹤機制

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大Late interaction與MaxSim示意圖"><img src="assets/figures/22.svg" alt="逐列找query token的最佳頁面token，說明此總分不是機率，也會受query長度影響。" loading="lazy"></a><figcaption>範例向量是手工數值；真實頁面embedding需另載入模型。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Late interaction與MaxSim」讀圖：逐列找query token的最佳頁面token，說明此總分不是機率，也會受query長度影響。本單元請再回答：MaxSim為2，是否代表這頁有百分之兩百的相關性？</p></div>

## 自我檢查與解析

**問題：**MaxSim為2，是否代表這頁有百分之兩百的相關性？

<details><summary>展開解析</summary><p>不是。它是各query token最佳相似度的加總，尺度和query長度有關，不是機率。</p></details>

## 實作與驗收

在下載包的 `examples` 目錄執行 `python lab22.py`。先用 `python run_lab.py --list` 核對這個入口的實際目標，再將輸出和本單元的條件對照；相關單元可以共用一個機制實驗，不代表每次執行會重做整章。

核心程式使用合成PDF、影像、WAV與動畫GIF。OCR使用鎖版RapidOCR隨套件提供的模型；API範例預設不連線，也不讀取金鑰。手工向量、人工逐字稿與固定題意規則均有明確標示，不冒稱通用語意模型、ASR或VLM推論。

<!-- example:lab22.py -->

## 官方與原始來源

[本單元對應來源](https://arxiv.org/abs/2407.01449)（查核：2026-11-27）。主線為PyMuPDF 2.2、pypdf 7.2.0、RapidOCR 3.10.0與Pydantic 2.14.4；相容環境採Python 3.14.10，安裝差異與外部服務驗證邊界另見版本紀錄。
