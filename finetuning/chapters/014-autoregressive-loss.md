# 因果語言模型的標籤位移與損失

先知道哪個位置預測哪個token，再談loss下降。

## 下一個token的正式定義

對長度為 $T$ 的序列，$x_t$ 是第 $t$ 個token，模型參數為 $\theta$。因果模型在位置 $t$ 的輸出預測 $x_{t+1}$，只能依賴截至 $t$ 的輸入。完整序列的平均負對數似然為

$$
\mathcal L=-\frac{1}{T-1}\sum_{t=1}^{T-1}\log p_\theta(x_{t+1}\mid x_1,\ldots,x_t).
$$

使用自然對數，條件機率須大於零。若兩個正確目標的機率為 $0.5$ 與 $0.25$，平均損失是 $-\log(0.125)/2\approx1.040$。這是給定正確前文的評分，並非自由生成的成功率。

## 框架已做位移，不能再做一次

多數HF因果模型接收與 `input_ids` 同長的 `labels`，在模型內部把logits尾端與labels前端錯開。手寫損失則使用 `logits[:, :-1]` 對 `labels[:, 1:]`。先人工位移labels再傳給模型，會把監督錯到再下一個token。

請用相同logits比較手算與模型內建loss，並讓測試涵蓋第一個token、最後一個有效target及padding。loss是一個數字，算錯位置仍可能下降，因此數值曲線不能取代標籤契約檢查。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener"><img src="assets/figures/05.svg" alt="因果語言模型的標籤位移與損失：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「因果語言模型的標籤位移與損失」讀圖：從warm所在位置往前追一格，核對哪個logit負責答案與EOS。再回答：序列有六個token，未加外部起始位置時最多有幾個位移target？</p></div>

## 自我檢查與解析

**題目：**序列有六個token，未加外部起始位置時最多有幾個位移target？

<details><summary>展開解析</summary><p>五個。最後一個輸出位置沒有序列內的下一個token；若加入mask，實際有效數可能更少。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def shifted_loss(logits,labels,reduction='mean'):
    target=labels[:,1:];count=(target!=-100).sum()
    if not count:raise ValueError('no valid targets')
    total=F.cross_entropy(logits[:,:-1].reshape(-1,logits.shape[-1]),target.reshape(-1),
                          ignore_index=-100,reduction='sum')
    return total if reduction=='sum' else total/count
```

## 離線實作

在 `examples` 目錄執行 `python 04_shifted_loss.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:04_shifted_loss.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
