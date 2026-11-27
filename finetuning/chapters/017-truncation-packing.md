# 截斷與packing的資訊邊界

長度上限會改變資料；EOS不會隔離attention。

## 先量測，再決定截斷規則

記錄提示、回答與總序列長度分布，再設定 `max_length`。從右端截斷可能刪掉答案與EOS；從左端截斷可能刪掉問題條件。不能只看有多少列成功token化，還要看各類別保留多少監督token。

本課入口遇到過長序列會明確拒絕，讓你先檢查資料。正式流程可以分段、摘要或設計任務專用截斷，但必須記錄規則與被影響ID，並用截斷後資料重做品質檢查。

## packing有多種語意

把短樣本接到同一序列能減少padding，但簡單加EOS後串接，後段仍可能注意前段。要聲稱跨文件隔離，必須確認模型與訓練kernel支援對應的區塊遮罩或序列邊界，不能只靠分隔token。

TRL有不同packing策略與版本預設，`packing=False` 是本課CPU主線的明確設定。開啟packing前比較有效token數、邊界與loss；同時控制樣本順序，避免把吞吐改善誤當模型品質提升。特殊attention實作也需核對支援的格式與硬體。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/06.svg" target="_blank" rel="noopener"><img src="assets/figures/06.svg" alt="截斷與packing的資訊邊界：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「截斷與packing的資訊邊界」讀圖：沿文件邊界檢查可見前文與有效labels，說明截斷會刪去哪部分。再回答：把每份文件之間放EOS，能否保證它們互相看不到？</p></div>

## 自我檢查與解析

**題目：**把每份文件之間放EOS，能否保證它們互相看不到？

<details><summary>展開解析</summary><p>不能。因果遮罩通常仍允許後面的token看前文；真正隔離需要實際支援並驗證區塊邊界。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def encode(row,tok=None,max_length=128):
    tok=tok or tokenizer()
    data=tok.apply_chat_template(row['messages'],tokenize=True,return_dict=True,
         return_assistant_tokens_mask=True,add_generation_prompt=False)
    ids=data['input_ids'];mask=data['assistant_masks']
    if len(ids)>max_length:raise ValueError('sequence too long: audit before truncation')
    labels=[v if m else -100 for v,m in zip(ids,mask)]
    if not any(v!=-100 for v in labels[1:]):raise ValueError('no supervised shifted targets')
    return {'input_ids':ids,'labels':labels,'attention_mask':[1]*len(ids)}

def collate(rows):
    length=max(len(r['input_ids']) for r in rows)
    return {k:torch.tensor([r[k]+[(-100 if k=='labels' else 0)]*(length-len(r[k])) for r in rows])
            for k in ['input_ids','labels','attention_mask']}
```

## 離線實作

在 `examples` 目錄執行 `python 05_sequence_audit.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:05_sequence_audit.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
