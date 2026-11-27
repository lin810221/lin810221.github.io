# 初始化、凍結與第一步梯度

B從零開始時，兩個矩陣的第一步行為不同。

## 初始輸出如何保持不變

常見初始化令 $A$ 隨機、$B=0$，所以 $BA=0$，初始adapter不改變基底輸出。這個性質取決於初始化方式；使用其他初始化策略時不能照搬結論。PEFT的預設與研究變體應分開記錄。

令 $G=\partial\mathcal L/\partial W$、縮放 $s=\alpha/r$，矩陣微分給出

$$
\frac{\partial\mathcal L}{\partial A}=sB^\mathsf TG,
\qquad
\frac{\partial\mathcal L}{\partial B}=sGA^\mathsf T.
$$

第一步 $B=0$ 時，$A$ 的梯度為零，而 $B$ 一般可有非零梯度；這不表示A被錯誤凍結。若 $A$ 與 $B$ 同時為零，則兩者都無法依這個分支開始更新。

## 檢查真正被更新的權重

列出每個參數的 `requires_grad`、梯度與更新前後差值。確認基底不變、adapter會變，且最佳化器只包含預期參數。不要僅依參數名稱中含有LoRA就假設設定正確，尤其新增詞彙或 `modules_to_save` 時還有其他可訓練層。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener"><img src="assets/figures/09.svg" alt="初始化、凍結與第一步梯度：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「初始化、凍結與第一步梯度」讀圖：逐一核對A、B與基底形狀，數出哪些格子可以更新。再回答：看到A第一步梯度為零，應立即提高學習率嗎？</p></div>

## 自我檢查與解析

**題目：**看到A第一步梯度為零，應立即提高學習率嗎？

<details><summary>展開解析</summary><p>先核對初始化。若B初始為零，A第一步為零是預期結果；後續B更新後再觀察A。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def lora_matrix_demo():
    seed();a=torch.randn(2,3,requires_grad=True);b=torch.zeros(4,2,requires_grad=True)
    x=torch.randn(5,3);w=torch.randn(4,3);output=x@(w+4*b@a).T
    output.square().mean().backward()
    return {'delta_norm':(b@a).norm().item(),'A_grad':a.grad.norm().item(),'B_grad':b.grad.norm().item(),
            'adapter_parameters':a.numel()+b.numel()}
```

## 離線實作

在 `examples` 目錄執行 `python 07_lora_matrices.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:07_lora_matrices.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2106.09685)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
