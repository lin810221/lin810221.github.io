# 建立有假設的記憶體預算

權重、梯度、最佳化器與activation要分項列出。

## 純張量的預算式

令基底參數數為 $P_b$、儲存位元為 $b$，adapter可訓練參數為 $P_a$。假設adapter、梯度與Adam兩份狀態皆為FP32，且沒有額外master copy，則

$$
M_{\mathrm{tensor}}\approx P_b\frac{b}{8}+16P_a+M_{\mathrm{act}}+M_{\mathrm{temp}}+M_{\mathrm{meta}}.
$$

單位是bytes。七十億個四位元基底參數的純權重為 $3.5\times10^9$ bytes；八百萬adapter參數的上述四份狀態為 $128\times10^6$ bytes。尚未包含量化metadata、activation、暫存與allocator，不能把相加結果當作所需顯示記憶體。

## 量測與估算互相校正

序列長度、microbatch、attention實作、checkpoint與精度會改變峰值。分開記錄allocated、reserved與裝置總使用量，說明量測點與是否同步GPU。OOM可能發生在載入、第一步最佳化器初始化或評估生成，不只訓練前向。

先量測小批次再逐步增加，保存每次設定。梯度累積可以降低單次microbatch，卻不會自動縮小基底權重；QLoRA縮小基底，也不會消除長序列的activation問題。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener"><img src="assets/figures/12.svg" alt="建立有假設的記憶體預算：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立有假設的記憶體預算」讀圖：逐項指認記憶體成本，說明本單元設定會改變哪一項。再回答：四位元基底檔案3.5GB，能否保證4GB顯示卡可訓練？</p></div>

## 自我檢查與解析

**題目：**四位元基底檔案3.5GB，能否保證4GB顯示卡可訓練？

<details><summary>展開解析</summary><p>不能。檔案大小與訓練峰值不同，還有metadata、adapter狀態、activation、暫存及框架配置。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def memory_bytes(base_parameters,trainable_parameters,base_bits=4,activation_bytes=0):
    if min(base_parameters,trainable_parameters,activation_bytes)<0 or base_bits not in [4,8,16,32]:
        raise ValueError('invalid memory input')
    # Explicit model: base storage + FP32 adapters/grad/m/v. No master copy.
    return {'base':math.ceil(base_parameters*base_bits/8),
            'trainable_weights_grad_adam':trainable_parameters*4*4,
            'activations':activation_bytes}
```

## 離線實作

在 `examples` 目錄執行 `python 13_memory_budget.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:13_memory_budget.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2305.14314)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
