# 按群組、時間與來源切分資料

防止模型在測試時看見同一事件的另一種寫法。

## 切分單位是什麼

一個客戶、病人、文件、專案或事件常產生多列資料。逐列隨機切分會把同一群組拆到訓練與測試，讓模型記住來源特徵。先定義獨立單位，再將整個群組分配給同一切分；若目標是預測未來，通常還要建立時間順序的測試。

開發集供挑參數，最終測試集保留給最後比較。切分規則、隨機種子與ID清單都要保存，不能每次訓練重新洗牌切一次，再挑最好看的結果。

## 群組不相交仍可能洩漏

相同範本文字可能被不同群組複製。課程的合成資料特意有重複內容：案例ID不相交，但不能據此聲稱語意泛化。更完整的流程先找重複與近似重複群，再決定合併切分、刪除或單獨報告。

例如把同一產品說明改寫成十個問題，整組應一起保留。如果只有某類別集中在一個群組，切分後可能無法同時得到類別完整與群組隔離；應誠實記錄限制，補資料或改研究問題，而非偷偷把列搬回去。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener"><img src="assets/figures/03.svg" alt="按群組、時間與來源切分資料：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「按群組、時間與來源切分資料」讀圖：沿群組箭頭核對切分，說明來源權利與內容重複還需在哪裡檢查。再回答：測試與訓練沒有相同ID，是否足夠？</p></div>

## 自我檢查與解析

**題目：**測試與訓練沒有相同ID，是否足夠？

<details><summary>展開解析</summary><p>不夠。檢查群組、時間、來源與內容重複；ID只是一個識別欄位，不代表獨立的資訊來源。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def split_groups(rows,heldout_groups):
    validate_rows(rows)
    train=[r for r in rows if r['group'] not in heldout_groups]
    valid=[r for r in rows if r['group'] in heldout_groups]
    if not train or not valid:raise ValueError('empty split')
    assert not ({r['group'] for r in train}&{r['group'] for r in valid})
    return train,valid

def duplicates(rows):
    groups={}
    for r in rows:groups.setdefault(content_hash(r),[]).append(r['id'])
    return [ids for ids in groups.values() if len(ids)>1]
```

## 離線實作

在 `examples` 目錄執行 `python 02_group_split.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:02_group_split.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/trl/v1.18.2/sft_trainer)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
