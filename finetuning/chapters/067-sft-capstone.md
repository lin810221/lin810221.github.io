# 專題：完成一份SFT實驗報告

串起契約、資料、基準、訓練、評估與成品。

## 先完成離線合成專題

下載完整程式包，先跑schema與模板入口，再跑手寫SFT與TRL版本，最後執行capstone。它會輸出保留評分、adapter回讀與合併比較、續訓對照及manifest。所有資料由本地程式建立，不下載外部權重。

```powershell
python 01_schema.py
python 03_chat_masks.py
python 06_full_sft.py
python 15_trl_sft.py
python 24_capstone.py --output outputs/first-project
python -m unittest -v test_examples.py
```

## 報告要包含限制

合成資料具有重複範本，保留ID不同仍不能證明語意泛化。請在報告寫明這是流程與數值驗證，展示有效target、loss分母、可訓練參數與成品身分。程式輸出的teacher-forced準確率也不等於自由生成成功率。

移植到真實專案時，替換為已授權資料與明確revision的預訓練模型，重新做群組與時間切分、去重、模板檢查和合理提示基準。再建立任務生成評估，而非沿用合成資料的數值門檻。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener"><img src="assets/figures/23.svg" alt="專題：完成一份SFT實驗報告：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「專題：完成一份SFT實驗報告」讀圖：沿完整交付鏈指出每個步驟產出的證據，再找出尚未測試的能力。再回答：capstone報告中最容易被誤讀的是什麼？</p></div>

## 自我檢查與解析

**題目：**capstone報告中最容易被誤讀的是什麼？

<details><summary>展開解析</summary><p>合成保留集的改善容易被誤當真實泛化；應明寫重複範本、teacher forcing與小模型限制。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def heldout_demo():
    train_rows,valid_rows=split_groups(records(),{'case-9','case-10','case-11'})
    train_batch=collate([encode(r) for r in train_rows]);valid_batch=collate([encode(r) for r in valid_rows])
    model=tiny_model();before=evaluate(model,valid_batch);losses=train(model,train_batch)
    return {'before':before,'after':evaluate(model,valid_batch),'losses':losses,
            'limitation':'disjoint synthetic case IDs, but repeated templates/content; not semantic generalization'}

def load_verified_adapter(base,folder,tok):
    from peft import PeftModel
    folder=Path(folder)
    manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    if state_hash(base.state_dict())!=manifest['base_sha256']:raise ValueError('base identity mismatch')
    if tokenizer_hash(tok)!=manifest['tokenizer_sha256']:raise ValueError('tokenizer or chat template mismatch')
    return PeftModel.from_pretrained(base,folder/'adapter')

def artifact_demo(folder):
    from peft import PeftModel
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    base=tiny_model();original=copy.deepcopy(base.state_dict());base_hash=state_hash(original)
    tok=tokenizer();model=lora(base);b=batch();train(model,b,steps=4)
    model.eval();before=model(**b).logits.detach()
    adapter=folder/'adapter';model.save_pretrained(adapter,safe_serialization=True);tok.save_pretrained(folder/'tokenizer')
    manifest={'schema':1,'base_sha256':base_hash,'tokenizer_sha256':tokenizer_hash(tok),
              'seed':SEED,'base':'locally initialized tiny Llama; not a pretrained checkpoint'}
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    restored=tiny_model();restored.load_state_dict(original)
    loaded=load_verified_adapter(restored,folder,tok);loaded.eval()
    reloaded=loaded(**b).logits.detach();merged=loaded.merge_and_unload();merged.eval()
    after=merged(**b).logits.detach()
    return {'reload_max_abs':(before-reloaded).abs().max().item(),
            'merge_max_abs':(before-after).abs().max().item(),'manifest':manifest}
```

## 離線實作

在 `examples` 目錄執行 `python 24_capstone.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:24_capstone.py -->


## 換成自己的本地模型

完整程式包另有 `train_local.py`，接受已下載且有權使用的HF模型資料夾，以及具有來源與群組欄位的訓練、驗證JSONL。它拒絕跨切分的ID、群組與精確內容重複，並先檢查模板監督與長度，不靜默截斷。

```powershell
python train_local.py --model models/local-base --train data/train.jsonl --valid data/valid.jsonl --output outputs/local-lora --method lora --targets q_proj v_proj --rank 8 --alpha 16 --steps 20 --cpu
```

`--method full` 更新完整參數；`--method qlora` 需要另建相容CUDA環境並移除 `--cpu`。target名稱依架構核對，學習率與步數是探索設定，不能當通用建議。工具只使用本地檔案，不自動下載或上傳；輸出保存模型、tokenizer、資料與基底雜湊及前後評估。此路線已用課程小模型完成整合測試，真實預訓練權重與GPU量化需另行實測。

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
