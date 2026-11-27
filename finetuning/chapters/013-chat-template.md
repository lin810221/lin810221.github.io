# 聊天模板是模型輸入協定

角色標記、生成起點與訓練用模板必須一致。

## messages不是模型直接讀取的格式

`messages`只是資料表示。tokenizer的 `apply_chat_template` 會把角色與內容轉成模型認得的序列；不同模型可能使用不同的起始符、回合結束符及assistant標頭。自行拼上通用的「User:」不一定符合基底模型的訓練分布。

推論常需 `add_generation_prompt=True`，讓序列停在assistant即將回答的位置。訓練已有完整答案時通常不再加入另一個空assistant標頭。先印出模板文字、token ID與特殊token，再檢查是否重複加入起始或結束符號。

## 從模板追到監督位置

課程模板用Jinja的 `generation` 區塊包住assistant內容及其結束符號，供assistant mask追蹤。不是每個現成模板都提供這種區塊；啟用 `assistant_only_loss` 前，要實際確認遮罩不是全零，也沒有包含user內容。

本課的本地WordLevel tokenizer只處理少量合成單詞，用於逐token檢查；它不適合中文LLM訓練。換用真正模型時，應保存原tokenizer與模板，並以多輪、空白、工具及特殊符號案例重跑檢查，而非直接沿用這個玩具詞表。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/05.svg" target="_blank" rel="noopener"><img src="assets/figures/05.svg" alt="聊天模板是模型輸入協定：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「聊天模板是模型輸入協定」讀圖：從warm所在位置往前追一格，核對哪個logit負責答案與EOS。再回答：把模型原模板改成自己喜歡的角色符號，為什麼可能退步？</p></div>

## 自我檢查與解析

**題目：**把模型原模板改成自己喜歡的角色符號，為什麼可能退步？

<details><summary>展開解析</summary><p>角色符號與token邊界是輸入協定的一部分，模型可能沒學過新格式；需核對是否新增token、監督是否正確及推論是否一致。</p></details>

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

[官方文件或原始研究](https://huggingface.co/docs/transformers/chat_templating)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
