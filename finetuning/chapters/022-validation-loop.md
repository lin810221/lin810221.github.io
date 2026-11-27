# 保留集loss與生成品質分開看

Teacher forcing能評分，不能代替部署時的回答檢查。

## 評估模式與可比較的分母

評估使用 `model.eval()` 與無梯度模式，結束後恢復原訓練狀態。把所有有效target的損失加總，再除以總有效數，避免短批次與長批次等權。不同tokenizer或不同遮罩下的loss，不宜直接比較大小。

若平均負對數似然為 $\bar\ell$，在相同token化與監督定義下，perplexity定義為

$$
\operatorname{PPL}=\exp(\bar\ell).
$$

例如 $\bar\ell=\log 4$ 時PPL為 $4$。它反映正確前文下的平均預測不確定性，不是答對四分之一的意思。只監督assistant時，必須明寫這是assistant範圍的分數。

## 自由生成的另一張成績單

固定生成提示、停止規則與解碼設定，檢查格式、內容、拒答及長度。teacher-forced token準確率會使用正確前文，與模型自行生成後續不同，報告不可省略名稱。課程合成資料的train與valid雖有不同案例ID，仍重複範本，會明確標示泛化限制。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener"><img src="assets/figures/08.svg" alt="保留集loss與生成品質分開看：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「保留集loss與生成品質分開看」讀圖：比較訓練與開發曲線，區分可觀察現象與尚未證明的原因。再回答：兩個模型PPL不同，但tokenizer也不同，可以直接排名嗎？</p></div>

## 自我檢查與解析

**題目：**兩個模型PPL不同，但tokenizer也不同，可以直接排名嗎？

<details><summary>展開解析</summary><p>通常不行。token切分、評分範圍與資料分母都會改變數值；先建立共同可比較的任務評估。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def heldout_demo():
    train_rows,valid_rows=split_groups(records(),{'case-9','case-10','case-11'})
    train_batch=collate([encode(r) for r in train_rows]);valid_batch=collate([encode(r) for r in valid_rows])
    model=tiny_model();before=evaluate(model,valid_batch);losses=train(model,train_batch)
    return {'before':before,'after':evaluate(model,valid_batch),'losses':losses,
            'limitation':'disjoint synthetic case IDs, but repeated templates/content; not semantic generalization'}

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

在 `examples` 目錄執行 `python 20_heldout_evaluation.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:20_heldout_evaluation.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
