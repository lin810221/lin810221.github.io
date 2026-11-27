# 合併、重新量化與多adapter服務

部署形式改變後，數值與品質都要重新確認。

## 合併的定義與條件

對支援合併的標準LoRA線性層，可將更新寫入基底：

$$
W_{merge}=W_0+\frac{\alpha}{r}BA.
$$

這裡 $A,B$ 是已訓練矩陣，$W_0$ 與更新形狀一致。若 $W_0=1$、更新為 $0.2$，合併權重為 $1.2$；但低精度捨入、量化表示與方法變體會影響實作，不能保證任意環境bitwise相同。

## 先比數值，再比任務

使用 `merge_and_unload` 後比較相同輸入logits最大絕對差，並記錄dtype與容許誤差。合併可能改變adapter切換能力；保留原基底與adapter，方便回復。量化基底的直接合併支援依工具而異，不應任意將壓縮整數相加。

若合併後重新量化，這又是新成品，需重新評估與量測。多adapter服務則要驗證請求路由、基底共用、版本隔離與記憶體；服務框架支援載入LoRA，不等於支援所有PEFT方法與額外層。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener"><img src="assets/figures/21.svg" alt="合併、重新量化與多adapter服務：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「合併、重新量化與多adapter服務」讀圖：沿基底、模板與adapter追到manifest，列出回讀必須核對的身分。再回答：合併前後文字剛好相同，是否足夠？</p></div>

## 自我檢查與解析

**題目：**合併前後文字剛好相同，是否足夠？

<details><summary>展開解析</summary><p>不夠。先比較logits與數值容許誤差，再做較完整的任務回歸；少量相同文字可能隱藏其他差異。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
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

在 `examples` 目錄執行 `python 22_adapter_artifacts.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:22_adapter_artifacts.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/peft/v0.22.0/developer_guides/checkpoint)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
