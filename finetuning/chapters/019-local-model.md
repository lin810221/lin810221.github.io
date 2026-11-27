# 建立不下載權重的小型模型

用可控制的模型先驗證流程，再擴大到預訓練LLM。

## 架構與權重是兩件事

`LlamaConfig` 定義詞表、層數、hidden size、attention heads與位置上限；`LlamaForCausalLM(config)` 依設定初始化新權重。這不等於從網路下載Llama模型，更不代表它有相同的訓練資料或能力。

課程模型只有一層、hidden size為32，以固定種子初始化，配合本地短詞表。這樣能在CPU快速檢查標籤位移、adapter、Trainer與儲存流程。隨機模型的loss下降主要證明它能擬合這些合成模式。

## 先讓一個小批次工作

依序確認token ID未超出詞表、張量型別正確、logits最後一維等於詞表大小，且loss有限。再對單一小批次訓練，觀察能否明顯降低損失；連單批次都無法擬合時，先查標籤、梯度與最佳化器。

不要把小模型擬合結果寫成基準測試。正式LLM還涉及預訓練分布、模板與tokenizer、GPU精度及長序列。兩者共用可檢查的工程契約，但品質與資源需求要分別量測。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener"><img src="assets/figures/07.svg" alt="建立不下載權重的小型模型：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立不下載權重的小型模型」讀圖：沿labels、模型、loss與更新路徑，指出本單元要驗證的一步。再回答：從config建立模型且能生成文字，是否已完成預訓練模型微調？</p></div>

## 自我檢查與解析

**題目：**從config建立模型且能生成文字，是否已完成預訓練模型微調？

<details><summary>展開解析</summary><p>沒有。那是新初始化模型的訓練實驗；真正的微調需從已訓練權重開始，並保存其精確身分。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def tiny_model():
    seed()
    return LlamaForCausalLM(LlamaConfig(vocab_size=len(VOCAB),hidden_size=32,
        intermediate_size=64,num_hidden_layers=1,num_attention_heads=4,
        num_key_value_heads=2,max_position_embeddings=128,attention_dropout=0.,
        pad_token_id=0,bos_token_id=2,eos_token_id=3,tie_word_embeddings=False,
        use_cache=False,_attn_implementation='eager'))

def train(model,b,steps=12,lr=.01):
    model.train();opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=lr)
    losses=[]
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        loss=model(**b).loss;loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
        opt.step();losses.append(loss.item())
    return losses
```

## 離線實作

在 `examples` 目錄執行 `python 06_full_sft.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:06_full_sft.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
