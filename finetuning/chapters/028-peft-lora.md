# 用PEFT訓練第一個LoRA

在真實套件上核對參數、訓練與成品。

## 建立設定後檢查模型

使用 `LoraConfig` 定義 `r`、`lora_alpha`、`lora_dropout`、`target_modules` 與 `task_type='CAUSAL_LM'`，再以 `get_peft_model` 包裝模型。本課rank為4、alpha為8、dropout為零，便於重現CPU數值比較。

包裝後先列可訓練參數，確認基底凍結；保留基底狀態雜湊，再訓練少量步驟。梯度必須從loss流到adapter，不能用無梯度上下文包住整個模型前向。凍結權重與切斷計算圖是不同操作。

## 與完整微調公平比較

使用相同資料、模板、監督規則與評估設定。可分別調整兩種方法適合的學習率，但必須報告搜尋預算；不能讓一方用精調設定、另一方只跑一次預設值。

LoRA的優勢常包含可訓練狀態較小及多任務adapter管理，品質則需任務評估。本課入口會輸出參數數量與前後loss，後續成品章再驗證重新載入與合併。不要把少量參數當成必然較快或必然不會遺忘的保證。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/10.svg" target="_blank" rel="noopener"><img src="assets/figures/10.svg" alt="用PEFT訓練第一個LoRA：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「用PEFT訓練第一個LoRA」讀圖：從B為零推回初始輸出，說明第一步A與B的梯度差異。再回答：只需訓練adapter，能否把base前向整段放在no_grad內？</p></div>

## 自我檢查與解析

**題目：**只需訓練adapter，能否把base前向整段放在no_grad內？

<details><summary>展開解析</summary><p>不能這樣一概處理。反向仍需穿過相關運算到adapter；凍結base參數即可，不能無條件切斷所需計算圖。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def lora(model=None,rank=4,rs=False):
    from peft import LoraConfig,get_peft_model
    return get_peft_model(model or tiny_model(),LoraConfig(task_type='CAUSAL_LM',r=rank,
        lora_alpha=8,lora_dropout=0.,target_modules=['q_proj','v_proj'],bias='none',use_rslora=rs))

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

在 `examples` 目錄執行 `python 08_peft_lora.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:08_peft_lora.py -->


## 換成自己的本地模型

完整程式包另有 `train_local.py`，接受已下載且有權使用的HF模型資料夾，以及具有來源與群組欄位的訓練、驗證JSONL。它拒絕跨切分的ID、群組與精確內容重複，並先檢查模板監督與長度，不靜默截斷。

```powershell
python train_local.py --model models/local-base --train data/train.jsonl --valid data/valid.jsonl --output outputs/local-lora --method lora --targets q_proj v_proj --rank 8 --alpha 16 --steps 20 --cpu
```

`--method full` 更新完整參數；`--method qlora` 需要另建相容CUDA環境並移除 `--cpu`。target名稱依架構核對，學習率與步數是探索設定，不能當通用建議。工具只使用本地檔案，不自動下載或上傳；輸出保存模型、tokenizer、資料與基底雜湊及前後評估。此路線已用課程小模型完成整合測試，真實預訓練權重與GPU量化需另行實測。

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/package_reference/lora)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
