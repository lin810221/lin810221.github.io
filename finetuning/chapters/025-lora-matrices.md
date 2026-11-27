# LoRA矩陣、形狀與參數量

凍結基底，以低秩更新表示任務需要的改變。

## 低秩更新的正式定義

令基底線性層 $W_0\in\mathbb R^{d_{out}\times d_{in}}$，LoRA學習 $A\in\mathbb R^{r\times d_{in}}$ 與 $B\in\mathbb R^{d_{out}\times r}$，其中 $r$ 是正整數rank。標準縮放下

$$
W=W_0+\frac{\alpha}{r}BA,\qquad P_{\mathrm{adapter}}=r(d_{in}+d_{out}).
$$

例如輸入與輸出維度皆為 $4096$、$r=8$ 時，一個adapter有 $65536$ 個參數；原矩陣有 $16777216$ 個。這只計該線性層的兩個矩陣，不含bias、額外儲存層與其他目標模組。

## 少量參數不表示沒有成本

基底權重保持凍結，但前向與梯度傳遞仍需要穿過模型。LoRA可減少可訓練權重與最佳化器狀態，activation卻仍可能佔大量記憶體。rank限制的是單個更新矩陣的秩，不是整個模型只能學幾種知識。

推論可保留基底與adapter分支，或在支援的精度與模型上合併。合併前後需比較logits，而非只看檔案能否開啟。更改rank與alpha是不同的實驗因素，不能任意同時改動後把結果都歸因於rank。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener"><img src="assets/figures/09.svg" alt="LoRA矩陣、形狀與參數量：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「LoRA矩陣、形狀與參數量」讀圖：逐一核對A、B與基底形狀，數出哪些格子可以更新。再回答：輸入維度100、輸出維度200、rank為4，一層LoRA有多少可訓練矩陣參數？</p></div>

## 自我檢查與解析

**題目：**輸入維度100、輸出維度200、rank為4，一層LoRA有多少可訓練矩陣參數？

<details><summary>展開解析</summary><p>1200個，不含bias及其他層。完整原矩陣有20000個參數；比較時還要合計所有目標模組。</p></details>

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
