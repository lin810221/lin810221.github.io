# 手寫完整參數SFT迴圈

明確看見歸零、前向、反向與更新的先後。

## 一個訓練步驟的責任

先將模型切到訓練模式，清除上一輪梯度，前向計算loss，呼叫 `backward()`，必要時裁剪梯度，再呼叫最佳化器更新。若使用排程器，依其定義在正確的更新步驟呼叫；不要把每個microbatch都當成一次參數更新。

完整微調讓所有指定的基底參數可訓練。建立最佳化器後，再檢查參數群是否涵蓋預期權重；凍結策略若稍後改變，最佳化器也要重新核對。`model.train()` 本身不會打開被凍結參數的梯度。

## 梯度更新的基本式

以最簡單的梯度下降說明，學習率 $\eta>0$、參數向量 $\theta$ 與損失 $\mathcal L$ 的關係為

$$
\theta_{k+1}=\theta_k-\eta\nabla_\theta\mathcal L(\theta_k).
$$

若某個參數的梯度是 $2$、學習率為 $0.01$，這一步減少 $0.02$。實作使用AdamW，另有動量、平方梯度估計與weight decay，不能把此算例當作AdamW的完整公式。每輪保留loss、有效target數及更新步數，才知道比較是否公平。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener"><img src="assets/figures/07.svg" alt="手寫完整參數SFT迴圈：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「手寫完整參數SFT迴圈」讀圖：沿labels、模型、loss與更新路徑，指出本單元要驗證的一步。再回答：忘了zero_grad時，為什麼仍可能看到loss下降？</p></div>

## 自我檢查與解析

**題目：**忘了zero_grad時，為什麼仍可能看到loss下降？

<details><summary>展開解析</summary><p>梯度會跨步累加，仍可能朝某個有利方向移動；但已不是原定的更新規則，步長與實驗比較都失去控制。</p></details>

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

[官方文件或原始研究](https://docs.pytorch.org/docs/stable/notes/amp_examples.html)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
