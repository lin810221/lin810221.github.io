# 建立最新穩定版的隔離環境

以查核日鎖版，區分CPU教學與GPU模型訓練。

## 本課版本與安裝順序

2026-11-25查核基準為Python 3.15.2、PyTorch 2.15.0、Transformers 5.24.1、PEFT 0.22.0與TRL 1.18.2。完整相依見程式包的 `requirements-lock.txt`。先安裝適用平台的PyTorch，再安裝其餘鎖定套件；不要把先前其他課程的環境原地升級。

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install torch==2.15.0 --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple
python -m pip install -r requirements-lock.txt
python 01_schema.py
python -m unittest -v test_examples.py
```

## CPU主線與GPU支線

本機小模型與TRL範例採CPU、單一程序及少量合成資料，不需金鑰。Windows的啟動檔與Linux shell指令不同，但Python入口相同。第一次安裝相依需要網路，完成後教材與預設程式可離線運行。

QLoRA另需相容的GPU、驅動、CUDA版PyTorch及bitsandbytes；CPU鎖版環境不代表GPU組合已驗收。先讀官方相容性並建立另一個環境，再記錄實際硬體與版本。更新版本時重跑測試，不能只改網頁上的版本標籤。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener"><img src="assets/figures/02.svg" alt="建立最新穩定版的隔離環境：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立最新穩定版的隔離環境」讀圖：沿版本身分走到成品，指出本單元需要保存的檢查紀錄。再回答：為何不把安裝指令一律改成不指定版本？</p></div>

## 自我檢查與解析

**題目：**為何不把安裝指令一律改成不指定版本？

<details><summary>展開解析</summary><p>最新穩定版應先查核與實測，再鎖定以供重現。無條件追隨更新會使資料處理、Trainer預設與成品格式在不知情下改變。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def validate_rows(rows):
    ids=set()
    for row in rows:
        if not all(isinstance(row.get(k),str) and row[k].strip() for k in ['id','group','source']):
            raise ValueError('id, group and source are required')
        if row['id'] in ids:raise ValueError('duplicate id')
        ids.add(row['id']);messages=row.get('messages')
        if not isinstance(messages,list) or not messages:raise ValueError('empty messages')
        for i,m in enumerate(messages):
            if set(m)!={'role','content'} or m['role'] not in {'system','user','assistant'}:
                raise ValueError('unsupported message schema')
            if not isinstance(m['content'],str) or not m['content'].strip():raise ValueError('empty content')
            if m['role']=='system' and i!=0:raise ValueError('system must be first')
            if i and m['role']==messages[i-1]['role']:raise ValueError('repeated role')
        if messages[-1]['role']!='assistant':raise ValueError('missing assistant target')
    return len(ids)
```

## 離線實作

在 `examples` 目錄執行 `python 01_schema.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:01_schema.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/transformers/main_classes/trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
