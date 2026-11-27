# 災難性遺忘與資料混合

新任務進步時，也要量測舊能力的代價。

## 先定義需要保留什麼

遺忘是相對於某套原能力與評估而言，不是看到新任務進步就自動成立。建立一般語言、格式、拒答、舊任務與重要群組的保留切片；使用相同生成與評分方式比較基底、SFT與後續候選。

LoRA凍結基底不代表啟用adapter時行為不會退步。adapter仍改變整體計算。可以停用adapter回到基底，是管理上的優點，但使用者實際看到的啟用行為仍要評估。

## 混合目標的明確定義

若將新任務與保留資料混合，令兩者損失為 $\mathcal L_{new}$、$\mathcal L_{keep}$，權重 $\lambda\in[0,1]$，可寫成

$$
\mathcal L_{mix}=\lambda\mathcal L_{new}+(1-\lambda)\mathcal L_{keep}.
$$

例如 $\lambda=0.8$ 是此目標的權重，不必等於資料列數比例；長度、取樣與正規化都會影響。課程單一顏色過度訓練算例只展示某個合成切片的變化，不是所有LLM的遺忘定律。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener"><img src="assets/figures/18.svg" alt="災難性遺忘與資料混合：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「災難性遺忘與資料混合」讀圖：追蹤詞表新增列，說明哪些權重、模板或行為需要重新驗證。再回答：基底權重沒改，所以LoRA不會造成舊任務退步，對嗎？</p></div>

## 自我檢查與解析

**題目：**基底權重沒改，所以LoRA不會造成舊任務退步，對嗎？

<details><summary>展開解析</summary><p>不對。啟用adapter後整體輸出分布改變，仍可能退步；需實測保留能力。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def evaluate(model,b):
    was=model.training;model.eval()
    logits=model(input_ids=b['input_ids'],attention_mask=b['attention_mask']).logits
    loss=shifted_loss(logits,b['labels']).item()
    valid=b['labels'][:,1:]!=-100
    correct=(logits[:,:-1].argmax(-1)==b['labels'][:,1:])[valid].sum().item()
    model.train(was)
    return {'nll':loss,'ppl':math.exp(loss),'teacher_forced_accuracy':correct/valid.sum().item(),
            'valid_targets':valid.sum().item()}
```

## 離線實作

在 `examples` 目錄執行 `python 21_retention_slices.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:21_retention_slices.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
