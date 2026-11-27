# Rank、rsLoRA、DoRA與soft prompt

比較不同的適應位置與縮放，而非只記方法名稱。

## rank與縮放的獨立角色

標準LoRA與rsLoRA的縮放分別為

$$
s_{\mathrm{LoRA}}=\frac{\alpha}{r},\qquad
s_{\mathrm{rsLoRA}}=\frac{\alpha}{\sqrt r}.
$$

在 $\alpha=8,r=16$ 時，兩者為 $0.5$ 與 $2$。這是分支的縮放係數，不是實際輸出一定相差四倍，因為訓練所得矩陣也會不同。比較時記錄初始化、alpha與學習率。

## DoRA與提示調整的位置

DoRA將權重的幅度與方向分開適應。以每個輸出列為正規化方向、$V=W_0+BA$ 為例，可寫成

$$
W_i=m_i\frac{V_i}{\lVert V_i\rVert_2},\quad \lVert V_i\rVert_2>0.
$$

其中 $m_i$ 為可學幅度；若方向列範數為2、幅度為3，輸出列範數為3。實際實作的軸與參數化需核對套件。Soft prompt則學習輸入端的虛擬token向量，例如 $k$ 個、維度 $d$ 時有 $kd$ 個參數；prefix tuning還可在層內注入前綴狀態，兩者不完全相同。方法選擇需考慮推論長度、支援架構與品質，不能只比參數數量。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener"><img src="assets/figures/10.svg" alt="Rank、rsLoRA、DoRA與soft prompt：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Rank、rsLoRA、DoRA與soft prompt」讀圖：從B為零推回初始輸出，說明第一步A與B的梯度差異。再回答：rank提高但alpha固定，標準LoRA縮放會如何變化？</p></div>

## 自我檢查與解析

**題目：**rank提高但alpha固定，標準LoRA縮放會如何變化？

<details><summary>展開解析</summary><p>縮放alpha除以rank會降低；因此rank消融要交代縮放政策，不能假設只改了容量。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def lora(model=None,rank=4,rs=False):
    from peft import LoraConfig,get_peft_model
    return get_peft_model(model or tiny_model(),LoraConfig(task_type='CAUSAL_LM',r=rank,
        lora_alpha=8,lora_dropout=0.,target_modules=['q_proj','v_proj'],bias='none',use_rslora=rs))

def count_parameters(model):
    return {'all':sum(p.numel() for p in model.parameters()),
            'trainable':sum(p.numel() for p in model.parameters() if p.requires_grad)}
```

## 離線實作

在 `examples` 目錄執行 `python 09_rank_scaling.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:09_rank_scaling.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://arxiv.org/abs/2312.03732)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
