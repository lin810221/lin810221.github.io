# 精確續訓：保存的不只是權重

在optimizer更新邊界恢復，是最容易驗證的起點。

## 需要保存的完整狀態

包含模型、最佳化器、排程器、更新步數、隨機狀態、資料順序與讀取位置，以及精度scaler等實際使用的狀態。分散式時還需每個rank的相關狀態。只載入adapter並重新建立AdamW，雖可繼續學習，卻不是原訓練軌跡的恢復。

若在梯度累積中途保存，還涉及未更新梯度與累積分母。初學主線先在完整optimizer step後保存，降低恢復契約的複雜度。資料loader有預取或隨機轉換時，還要確認位置與RNG如何對應。

## 用對照實驗驗證續訓

一路連續跑兩步，與跑一步、保存、恢復再跑一步比較。課程採固定CPU批次、零dropout與可控制RNG，檢查每個參數最大差異。這證明限定環境的恢復邏輯，不保證任意GPU kernel與多卡都完全相同。

部署權重優先使用安全的張量格式；完整Python訓練checkpoint可能包含可執行的序列化物件，僅載入可信的本地產物。課程測試只回讀自身剛寫出的檔案，不把未知來源checkpoint當作一般資料。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener"><img src="assets/figures/14.svg" alt="精確續訓：保存的不只是權重：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「精確續訓：保存的不只是權重」讀圖：比較兩種保存內容，指出續訓與推論各自依賴的狀態。再回答：恢復了模型卻沒有Adam動量，能否說exact resume？</p></div>

## 自我檢查與解析

**題目：**恢復了模型卻沒有Adam動量，能否說exact resume？

<details><summary>展開解析</summary><p>不能。更新規則依賴動量等狀態；可稱從該權重重新開始訓練，但需與完整續訓區分。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def resume_demo(folder):
    """Exact CPU comparison at optimizer boundary, deterministic one-batch order."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);seed()
    b=batch();model=tiny_model();opt=torch.optim.AdamW(model.parameters(),lr=.003)
    scheduler=torch.optim.lr_scheduler.LambdaLR(opt,lambda step:1-step/20)
    def step(m,o,s):
        m.train();o.zero_grad(set_to_none=True);loss=m(**b).loss;loss.backward();o.step();s.step()
    step(model,opt,scheduler)
    checkpoint={'model':model.state_dict(),'optimizer':opt.state_dict(),'scheduler':scheduler.state_dict(),
                'torch_rng':torch.get_rng_state(),'python_rng':random.getstate(),'optimizer_step':1,'data_offset':0}
    path=folder/'resume.pt';torch.save(checkpoint,path)
    step(model,opt,scheduler);target=copy.deepcopy(model.state_dict())
    # Only load a trusted checkpoint produced locally by this very experiment.
    state=torch.load(path,weights_only=False,map_location='cpu')
    restored=tiny_model();restored.load_state_dict(state['model'])
    ropt=torch.optim.AdamW(restored.parameters(),lr=.003)
    rs=torch.optim.lr_scheduler.LambdaLR(ropt,lambda step:1-step/20)
    # Scheduler construction initializes LR; restore optimizer AFTER construction.
    ropt.load_state_dict(state['optimizer']);rs.load_state_dict(state['scheduler'])
    torch.set_rng_state(state['torch_rng']);random.setstate(state['python_rng'])
    step(restored,ropt,rs)
    return max((target[k]-restored.state_dict()[k]).abs().max().item() for k in target)
```

## 離線實作

在 `examples` 目錄執行 `python 14_checkpoint_resume.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:14_checkpoint_resume.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
