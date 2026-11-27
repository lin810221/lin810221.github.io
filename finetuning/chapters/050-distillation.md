# 蒸餾：從教師分布學習

教師需固定，token與詞表也必須對齊。

## 溫度與KL目標

以相同詞表與位置的教師logits $z^T$、學生logits $z^S$，溫度 $\tau>0$，可定義

$$
p^T_\tau=\operatorname{softmax}(z^T/\tau),\quad
p^S_\tau=\operatorname{softmax}(z^S/\tau),\quad
\mathcal L_{KD}=\tau^2\sum_v p^T_\tau(v)\log\frac{p^T_\tau(v)}{p^S_\tau(v)}.
$$

求和遍歷詞表，教師分布停止梯度。若兩者分布相同，KL為零；例如學生與教師都給兩類各 $0.5$，此位置沒有蒸餾誤差。係數與硬標籤損失混合時需另行記錄。

## 不同tokenizer不能逐格硬比

逐token logits蒸餾需要詞表與位置對齊；教師與學生tokenizer不同時，相同字串不一定有相同token數與ID。可以研究序列級蒸餾，以教師產生文字再做SFT，但那是不同訊號，仍需篩選品質與權利。

課程入口用小張量檢查KL方向、溫度平方與教師無梯度，不下載教師模型。真實專案還需考慮教師成本、生成偏差、資料污染與學生能力上限；教師回答本身也不是事實保證。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener"><img src="assets/figures/17.svg" alt="蒸餾：從教師分布學習：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「蒸餾：從教師分布學習」讀圖：從資料型態走到目標，指出本單元能與哪種方法比較。再回答：KL參數順序反過來，仍是同一個loss嗎？</p></div>

## 自我檢查與解析

**題目：**KL參數順序反過來，仍是同一個loss嗎？

<details><summary>展開解析</summary><p>不是。KL不對稱；需依定義核對框架的log機率與目標分布參數，並測試教師是否detach。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def distillation(student_logits,teacher_logits,temperature=2.):
    if temperature<=0 or student_logits.shape!=teacher_logits.shape:raise ValueError('temperature or vocab mismatch')
    t=temperature
    return F.kl_div(F.log_softmax(student_logits/t,-1),F.softmax(teacher_logits.detach()/t,-1),
                    reduction='batchmean')*t*t
```

## 離線實作

在 `examples` 目錄執行 `python 19_distillation.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:19_distillation.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/1503.02531)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
