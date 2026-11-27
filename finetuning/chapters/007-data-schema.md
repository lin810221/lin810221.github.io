# SFT資料格式與來源追蹤

用嚴格schema把資料問題擋在GPU之前。

## 訓練內容與來源欄位

SFT可用純文字、提示與完成，或具有角色的對話。這些格式的預設損失範圍可能不同，轉換前要決定哪些token是目標。課程使用每列一筆對話的JSONL，另保存 `id`、`group`、`source`，讓來源與切分不依賴檔案順序。

```json
{"id":"case-001","group":"customer-A","source":"synthetic-v1","messages":[{"role":"user","content":"classify red"},{"role":"assistant","content":"warm"}]}
```

## 驗證不是只確認JSON能解析

檢查必要欄位、型別、空內容、重複ID、合法角色、角色順序與最後是否存在可監督回答。工具訊息與多模態資料需要更完整的schema；本課CPU主線刻意只接受純文字對話，遇到其他格式明確拒絕，不靜默刪除。

原始資料、清理後資料與token化資料各有版本。保存清理原因與被移除列的ID，避免一條清理規則消掉所有長回答。來源追蹤可回答「這個錯誤是模型學來的，還是模板轉錯的」，但不會自動證明資料授權與標註正確。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener"><img src="assets/figures/03.svg" alt="SFT資料格式與來源追蹤：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SFT資料格式與來源追蹤」讀圖：沿群組箭頭核對切分，說明來源權利與內容重複還需在哪裡檢查。再回答：資料可以解析且沒有空值，還可能有什麼致命問題？</p></div>

## 自我檢查與解析

**題目：**資料可以解析且沒有空值，還可能有什麼致命問題？

<details><summary>展開解析</summary><p>例如assistant答案放進user、不同標籤版本混在一起、同一客戶跨切分，或來源未取得訓練權利。schema只是必要的一層檢查。</p></details>

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

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
