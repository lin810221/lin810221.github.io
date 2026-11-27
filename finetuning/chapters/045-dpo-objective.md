# DPO目標、beta與固定reference

比較的是偏好變化，不能漏掉reference項。

## 從四個序列分數得到一個loss

令 $y^+$ 為chosen、$y^-$ 為rejected，$\pi_\theta$ 是policy，$\pi_{ref}$ 是固定reference，$\beta>0$。標準sigmoid DPO為

$$
z=\beta\left[\log\frac{\pi_\theta(y^+\mid x)}{\pi_\theta(y^-\mid x)}-\log\frac{\pi_{ref}(y^+\mid x)}{\pi_{ref}(y^-\mid x)}\right],\qquad
\mathcal L_{DPO}=-\log\sigma(z).
$$

其中 $\sigma(z)=1/(1+e^{-z})$。policy偏好差為 $3$、reference為 $1$、$\beta=0.2$ 時，$z=0.4$，loss約 $0.513$。兩者偏好差相同時loss為 $\log2$。

## beta不是學習率

beta控制目標中相對分數的尺度，學習率則控制最佳化更新。reference必須固定並停止梯度；若使用預先計算分數，需保存來源模型、模板與資料版本。配對標註相反時，最佳化器會忠實學到錯誤方向。

標準公式使用序列log機率加總；不同loss變體可能更改定義。檢查chosen與rejected對調、policy等於reference及極端margin三個情況，能抓出符號錯誤與不穩定計算。用穩定的 `logsigmoid`，避免直接計算極端指數。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener"><img src="assets/figures/15.svg" alt="DPO目標、beta與固定reference：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DPO目標、beta與固定reference」讀圖：重算差中之差與DPO logit，指出四個序列分數的角色。再回答：policy等於reference時loss為log2，是不是表示訓練失敗？</p></div>

## 自我檢查與解析

**題目：**policy等於reference時loss為log2，是不是表示訓練失敗？

<details><summary>展開解析</summary><p>不是。這是相對偏好差為零的基準值；下一步梯度仍可能推動policy偏向chosen。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def dpo_loss(policy_chosen,policy_rejected,ref_chosen,ref_rejected,beta=.1):
    if beta<=0:raise ValueError('beta must be positive')
    margin=(policy_chosen-policy_rejected)-(ref_chosen.detach()-ref_rejected.detach())
    return -F.logsigmoid(beta*margin).mean()
```

## 離線實作

在 `examples` 目錄執行 `python 17_dpo_loss.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:17_dpo_loss.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2305.18290)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
