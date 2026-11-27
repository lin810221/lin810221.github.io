# Adapter成品、manifest與基底身分

一個小檔案需要一整套明確依賴才能正確運作。

## 交付哪些檔案

PEFT的 `save_pretrained` 保存adapter設定與權重，通常不包含完整基底。交付時另附精確基底revision或可驗證雜湊、tokenizer與template、可訓練額外層、版本及評估報告。模型卡也要交代資料來源與已知限制。

安全張量格式保存權重，不等於自動確認來源身分；manifest用來連接檔案與實驗。課程基底為本地初始化，因此以固定config、種子與權重內容雜湊驗證。真正預訓練模型應使用不可變revision並保存取得方式。

## 回讀驗收不可省略

在新模型物件上載入相同基底與adapter，以eval模式、相同dtype、固定輸入比較logits。再回讀tokenizer並確認模板身分，最後做任務回歸。若只在原本記憶體中的模型生成，無法發現漏存成品的問題。

基底同名但revision不同、tokenizer被修改或新增embedding未保存，都可能讓結果變化。遇到身分不一致時明確拒絕載入或要求重新評估，不用「應該差不多」代替可追溯的交付契約。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener"><img src="assets/figures/21.svg" alt="Adapter成品、manifest與基底身分：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Adapter成品、manifest與基底身分」讀圖：沿基底、模板與adapter追到manifest，列出回讀必須核對的身分。再回答：adapter能載入另一個同架構模型，是否表示兩者可以互換？</p></div>

## 自我檢查與解析

**題目：**adapter能載入另一個同架構模型，是否表示兩者可以互換？

<details><summary>展開解析</summary><p>不表示。形狀相容與權重身分相同是兩件事；必須核對基底、tokenizer與回歸結果。</p></details>

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
