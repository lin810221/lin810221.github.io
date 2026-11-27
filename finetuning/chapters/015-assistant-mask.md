# Assistant-only與completion-only監督

遮罩改變的是學習目標，不是模型能看見的文字。

## 有效target才進入分母

令 $m_t\in\{0,1\}$ 表示第 $t$ 個target是否納入損失，$N=\sum_t m_t$。在 $N>0$ 時，遮罩後的目標為

$$
\mathcal L_{\mathrm{mask}}=-\frac{\sum_t m_t\log p_\theta(x_t\mid x_{<t})}{N}.
$$

假設兩個assistant token的機率為 $0.5$ 與 $0.25$，user有十個token但不監督，分母仍是 $2$，不能除以 $12$。user內容依然在上下文，模型仍可對它做attention。

## 兩種資料格式的遮罩來源

提示與完成格式可用 `completion_only_loss`；對話格式的 `assistant_only_loss` 則依賴聊天模板提供assistant spans。多輪對話可能監督所有assistant回合，也可能只監督最後一輪，需由任務與資料設計明確決定。

在張量中，忽略位置通常設成 `-100`。必須先位移再數有效target，並確認停止token是否被監督。全零遮罩或截斷後只剩提示時應拒絕樣本，不能以零loss混入批次。觀察逐token標籤，比只檢查平均loss更容易發現錯誤。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener"><img src="assets/figures/05.svg" alt="Assistant-only與completion-only監督：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Assistant-only與completion-only監督」讀圖：從warm所在位置往前追一格，核對哪個logit負責答案與EOS。再回答：把user的labels設為忽略值，是否代表assistant看不到user？</p></div>

## 自我檢查與解析

**題目：**把user的labels設為忽略值，是否代表assistant看不到user？

<details><summary>展開解析</summary><p>不是。損失遮罩與attention遮罩不同；user仍提供條件資訊，只是不對那些target計算訓練誤差。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def tokenizer():
    backend=Tokenizer(models.WordLevel({v:i for i,v in enumerate(VOCAB)},unk_token='<unk>'))
    backend.pre_tokenizer=pre_tokenizers.WhitespaceSplit()
    tok=PreTrainedTokenizerFast(tokenizer_object=backend,unk_token='<unk>',pad_token='<pad>',
        bos_token='<bos>',eos_token='<eos>',additional_special_tokens=VOCAB[4:7])
    tok.chat_template=TEMPLATE
    return tok

def encode(row,tok=None,max_length=128):
    tok=tok or tokenizer()
    data=tok.apply_chat_template(row['messages'],tokenize=True,return_dict=True,
         return_assistant_tokens_mask=True,add_generation_prompt=False)
    ids=data['input_ids'];mask=data['assistant_masks']
    if len(ids)>max_length:raise ValueError('sequence too long: audit before truncation')
    labels=[v if m else -100 for v,m in zip(ids,mask)]
    if not any(v!=-100 for v in labels[1:]):raise ValueError('no supervised shifted targets')
    return {'input_ids':ids,'labels':labels,'attention_mask':[1]*len(ids)}
```

## 離線實作

在 `examples` 目錄執行 `python 03_chat_masks.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:03_chat_masks.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
