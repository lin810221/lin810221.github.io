# 序列log機率與回答長度

DPO的基本分數是回答token的log機率加總。

## 同一提示下評分回答

令提示為 $x$，回答 $y=(y_1,\ldots,y_T)$，則

$$
\log\pi_\theta(y\mid x)=\sum_{t=1}^{T}\log\pi_\theta(y_t\mid x,y_{<t}).
$$

只計回答範圍，不把提示token算進配對分數；停止token是否納入需固定。若兩個回答token機率為 $0.5$ 與 $0.25$，序列log機率為 $\log0.125\approx-2.079$，不是兩個機率的平均。

## 加總與平均代表不同目標

直接改成每token平均會改變長度影響及訓練目標。某些偏好方法有長度修正，但必須明確標示變體；不能在標準DPO實作中偷偷替換。chosen與rejected長度不同時，更要檢查截斷是否只影響其中一邊。

實作使用位移後logits、log-softmax、目標ID的gather與completion mask。所有回答都需至少有一個有效target。請用手算小機率與實作比對，再觀察長回答的總log機率為何通常更負。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener"><img src="assets/figures/15.svg" alt="序列log機率與回答長度：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「序列log機率與回答長度」讀圖：重算差中之差與DPO logit，指出四個序列分數的角色。再回答：把prompt的log機率也加進去，為什麼不應直接接受？</p></div>

## 自我檢查與解析

**題目：**把prompt的log機率也加進去，為什麼不應直接接受？

<details><summary>展開解析</summary><p>分數定義應是給定prompt的回答條件機率；模板、截斷與遮罩若不一致，提示項未必正確抵消，應明確排除。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def sequence_logps(model,b):
    logits=model(input_ids=b['input_ids'],attention_mask=b['attention_mask']).logits[:,:-1]
    target=b['labels'][:,1:];mask=target!=-100
    if not torch.all(mask.sum(-1)>0):raise ValueError('empty completion')
    selected=F.log_softmax(logits.float(),-1).gather(-1,target.clamp_min(0).unsqueeze(-1)).squeeze(-1)
    return (selected*mask).sum(-1)
```

## 離線實作

在 `examples` 目錄執行 `python 16_sequence_scores.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:16_sequence_scores.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/dpo_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
