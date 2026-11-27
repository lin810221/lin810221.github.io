# 使用目前版本的SFTTrainer

把框架設定接到已經驗證的資料與模板。

## SFTConfig與processing_class

TRL 1.18.2以 `SFTConfig` 設定訓練，以 `processing_class` 傳入tokenizer。本課使用對話資料、`assistant_only_loss=True`、明確關閉packing與梯度checkpoint，CPU上執行少量步驟。這條主線先追求可檢查，再討論吞吐。

舊文章常將許多參數直接放進Trainer，或使用舊的 `tokenizer` 參數。閱讀舊程式時應對照當前signature與文件，不能將相似名稱原樣貼進新版本。預設值也可能隨版本變動，因此重要設定要明寫並保存。

## Trainer不會替你定義任務

確認Trainer實際看到的資料格式、長度上限、collator與labels。若提供預token化的 `input_ids` 與labels，需確認版本處理方式，避免遮罩被轉換或再套模板。本課另外提供手寫loss比對，讓框架抽象不會掩蓋錯誤。

先跑兩步smoke test，再擴大完整訓練。成功輸出訓練loss只表示流程可跑；需接上保留評估、固定生成及成品回讀。下載包包含完整相依與真實TRL入口，沒有用手寫模擬器冒充Trainer執行。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener"><img src="assets/figures/07.svg" alt="使用目前版本的SFTTrainer：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「使用目前版本的SFTTrainer」讀圖：沿labels、模型、loss與更新路徑，指出本單元要驗證的一步。再回答：範例跑完兩步，能否把training_loss當成最終模型品質？</p></div>

## 自我檢查與解析

**題目：**範例跑完兩步，能否把training_loss當成最終模型品質？

<details><summary>展開解析</summary><p>不能。兩步是相容性與流程檢查，品質需比較保留資料與自由生成的任務表現。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def trl_sft(folder):
    from datasets import Dataset
    from trl import SFTConfig,SFTTrainer
    tok=tokenizer();dataset=Dataset.from_list([{'messages':r['messages']} for r in records()[:3]])
    args=SFTConfig(output_dir=str(folder),max_steps=2,per_device_train_batch_size=3,
        learning_rate=.003,report_to='none',save_strategy='no',logging_strategy='no',
        use_cpu=True,bf16=False,fp16=False,activation_checkpointing=False,
        dataloader_pin_memory=False,max_length=64,assistant_only_loss=True,seed=SEED)
    trainer=SFTTrainer(model=tiny_model(),args=args,train_dataset=dataset,processing_class=tok)
    result=trainer.train()
    return {'steps':trainer.state.global_step,'training_loss':result.training_loss}
```

## 離線實作

在 `examples` 目錄執行 `python 15_trl_sft.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:15_trl_sft.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
