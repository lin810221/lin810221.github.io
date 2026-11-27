# 評估loss、格式與自由生成

一個模型需要多張成績單，不同指標不要互相冒名。

## 生成與teacher forcing不同

計算語言模型loss時，每一步常給模型正確前文；自由生成則把自己產生的token接回去。即使teacher-forced準確率提高，仍可能遇到開頭出錯後整段偏離。報告應清楚命名，不能只寫accuracy。

生成時固定提示、最大新token數、停止規則、temperature與取樣種子。格式任務可先使用確定性解碼建立比較，再評估實際部署設定。開發時調過解碼政策，也要記錄它是候選的一部分。

## 選擇與任務相符的指標

分類可以檢查各類別precision與recall；抽取需區分精確字串與可接受語意；摘要需核對來源忠實性；工具任務需檢查參數與成功軌跡。文字重疊分數不能直接證明事實正確，也不能取代人工複核。

課程入口提供NLL與teacher-forced token準確率，並明示合成範本重複的限制。真實專案應另建立自由生成測試與任務評分器；讀者不可把玩具結果當成任何公開大型模型的排名。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener"><img src="assets/figures/19.svg" alt="評估loss、格式與自由生成：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「評估loss、格式與自由生成」讀圖：由下到上讀三層驗收，指出本單元的指標能回答哪一層問題。再回答：模型teacher-forced token準確率為九成，是否代表九成使用者問題可解決？</p></div>

## 自我檢查與解析

**題目：**模型teacher-forced token準確率為九成，是否代表九成使用者問題可解決？

<details><summary>展開解析</summary><p>不代表。單位、上下文條件與成功定義不同，需以完整生成案例驗證任務成功。</p></details>

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
