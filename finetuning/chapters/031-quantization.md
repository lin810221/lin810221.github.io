# 量化的儲存、計算與誤差

位元數省下的是哪一部分，必須說清楚。

## 均勻量化的教學定義

以對稱均勻量化為例，正尺度 $s$、整數上限 $q_{max}$ 與權重 $w$ 的關係為

$$
q=\operatorname{clip}\!\left(\operatorname{round}(w/s),-q_{max},q_{max}\right),\qquad \hat w=sq.
$$

若 $s=0.1,w=0.26$ 且未觸發裁切，重建值為 $0.3$。這是均勻量化算例，不是NF4。誤差取決於分布、分組、尺度、離群值與量化方案，不能只由位元數推論品質。

## 儲存精度不等於所有運算精度

量化權重通常附帶尺度與其他metadata，實際記憶體不等於參數數量直接乘位元。運算時可能解量化到另一種dtype，activation、梯度與最佳化器也可能使用不同精度。

量化已微調模型與在量化基底上訓練adapter，是不同流程。量化後需重新量測品質、峰值記憶體與吞吐；模型檔比較小不代表一定推論較快，也不代表原本的合併與服務工具都支援。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener"><img src="assets/figures/11.svg" alt="量化的儲存、計算與誤差：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「量化的儲存、計算與誤差」讀圖：比較兩排碼本間距，說明本單元涉及哪種量化與哪些假設。再回答：四位元模型的所有張量都是四位元嗎？</p></div>

## 自我檢查與解析

**題目：**四位元模型的所有張量都是四位元嗎？

<details><summary>展開解析</summary><p>不是。權重壓縮、尺度、activation、計算dtype、adapter與最佳化器狀態需要分開記錄。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def quantize_toy(values,bits=4):
    """Uniform symmetric quantizer, intentionally NOT the NF4 algorithm."""
    if bits<2 or bits>8:raise ValueError('bits must be 2..8')
    x=torch.tensor(values,dtype=torch.float32);qmax=2**(bits-1)-1
    scale=max(x.abs().max().item()/qmax,1e-12)
    q=(x/scale).round().clamp(-qmax,qmax).to(torch.int8)
    y=q.float()*scale
    return {'codes':q.tolist(),'scale':scale,'reconstructed':y.tolist(),'mse':(x-y).square().mean().item()}
```

## 離線實作

在 `examples` 目錄執行 `python 10_toy_quantization.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:10_toy_quantization.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/developer_guides/quantization)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
