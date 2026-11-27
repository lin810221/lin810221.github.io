# 以DPOTrainer跑一個真實步驟

用當前API驗證資料、policy與reference。

## 三份輸入的契約

TRL 1.18.2使用 `DPOConfig` 與 `DPOTrainer`，透過 `processing_class` 傳tokenizer。資料包含同提示的 `prompt`、`chosen`、`rejected`。本課使用本地小模型，policy加LoRA，reference為相同初始權重的普通因果模型。

當前文件對顯式 `ref_model` 的型別有限制，不能把任意PeftModel直接當作reference。若使用套件的adapter reference模式，需理解停用或切換adapter的實際行為；課程採明確的普通模型，便於檢查與教學。

## 訓練前後的檢查

固定reference、確認其參數不更新，再檢查配對是否共用同一prompt、回答是否有有效token，以及截斷政策。先跑一個CPU步驟驗證API與資料，不宣稱這已完成偏好品質改善。

`precompute_ref_log_probs` 可以讓reference分數預算與訓練分開，但資料與模板變更後必須重新計算。記錄beta、loss type、reference身分、adapter設定及生成評估，才能重建偏好實驗。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener"><img src="assets/figures/16.svg" alt="以DPOTrainer跑一個真實步驟：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「以DPOTrainer跑一個真實步驟」讀圖：指出固定reference與可更新policy，檢查相同配對如何進入兩者。再回答：更改聊天模板後，舊的reference預計分數還能直接沿用嗎？</p></div>

## 自我檢查與解析

**題目：**更改聊天模板後，舊的reference預計分數還能直接沿用嗎？

<details><summary>展開解析</summary><p>不能假設可以。token序列與回答邊界可能已改變，需要重新計分並更新版本身分。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def trl_dpo(folder):
    from datasets import Dataset
    from trl import DPOConfig,DPOTrainer
    seed();base=tiny_model();ref=copy.deepcopy(base);ref.requires_grad_(False);ref.eval();model=lora(base)
    ref_hash=state_hash(ref.state_dict())
    dataset=Dataset.from_list([{'prompt':'<user> classify red <eos> <assistant> ',
          'chosen':'warm <eos>','rejected':'cool <eos>'} for _ in range(3)])
    args=DPOConfig(output_dir=str(folder),max_steps=1,per_device_train_batch_size=3,
        learning_rate=.001,report_to='none',save_strategy='no',logging_strategy='no',
        use_cpu=True,bf16=False,fp16=False,activation_checkpointing=False,
        dataloader_pin_memory=False,max_length=64,beta=.1,seed=SEED)
    trainer=DPOTrainer(model=model,ref_model=ref,args=args,train_dataset=dataset,processing_class=tokenizer())
    result=trainer.train()
    return {'steps':trainer.state.global_step,'training_loss':result.training_loss,
            'reference_requires_grad':any(p.requires_grad for p in trainer.ref_model.parameters()),
            'reference_unchanged':ref_hash==state_hash(trainer.ref_model.state_dict())}
```

## 離線實作

在 `examples` 目錄執行 `python 18_trl_dpo.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:18_trl_dpo.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/dpo_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
