# 梯度累積與有效token加權

不同回答長度時，平均的平均會改變目標。

## 一次更新的正確權重

假設第 $j$ 個microbatch有 $n_j$ 個有效target，平均loss為 $\bar\ell_j$。同一次更新希望等同合併批次時，目標為

$$
\mathcal L=\frac{\sum_j n_j\bar\ell_j}{\sum_j n_j}.
$$

若兩批有效數為 $2$、$8$，平均loss為 $1$、$3$，合併結果是 $2.6$，不是 $2$。實作可以先取得整個累積群的分母，再對每批的損失總和按該分母反向。

## 等效需要說明條件

單一程序中，沒有dropout等隨機差異、沒有依批次統計的層，且在同一參數點累積時，梯度應在浮點誤差內相近。先累積完成再裁剪梯度與更新，不能每批先更新後聲稱等效大批次。

分散式情況還涉及各rank的有效token數及梯度平均方式，不能只套本機分母。Accelerate與Trainer會處理部分縮放，但需核對版本設定。課程以不等長批次的數值測試驗證概念，不把單機測試冒稱多卡驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener"><img src="assets/figures/13.svg" alt="梯度累積與有效token加權：顯示資料、模型與檢查點之間的關係，箭頭和圖例在圖中逐一標示。" loading="lazy"></a><figcaption>原創教學示意；數值為可重算的小型案例，不是大型模型效能報告。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「梯度累積與有效token加權」讀圖：數出microbatch與更新的邊界，說明有效target不同時如何加權。再回答：四個microbatch並不等長，直接各自loss除以4有什麼問題？</p></div>

## 自我檢查與解析

**題目：**四個microbatch並不等長，直接各自loss除以4有什麼問題？

<details><summary>展開解析</summary><p>它讓每批等權，未必讓每個有效target等權；若要全token平均，需按有效數加權並核對框架縮放。</p></details>

## 實作核心

以下節錄完整程式包中的核心函式。相關匯入與共用工具保存在 `finetune_core.py`；先讀懂資料流，再使用完整入口執行，不將節錄誤當獨立檔案。

```python
def accumulation_error():
    seed();a=torch.nn.Linear(3,2,bias=False);b=copy.deepcopy(a)
    xs=[torch.randn(1,3),torch.randn(4,3)];ys=[torch.tensor([0]),torch.tensor([1,0,1,1])]
    F.cross_entropy(a(torch.cat(xs)),torch.cat(ys)).backward()
    total=sum(len(y) for y in ys)
    for x,y in zip(xs,ys): (F.cross_entropy(b(x),y,reduction='sum')/total).backward()
    return (a.weight.grad-b.weight.grad).abs().max().item()
```

## 離線實作

在 `examples` 目錄執行 `python 12_token_accumulation.py`。入口使用同資料夾的 `finetune_core.py`，請下載完整程式包；預設不連線下載模型。未指定 `--output` 時，產物放在目前目錄的 `finetuning-output`。

<!-- example:12_token_accumulation.py -->

## 來源與跨課閱讀

[官方文件或原始研究](https://huggingface.co/docs/accelerate/usage_guides/gradient_accumulation)（查核：2026-11-25；研究出版年以來源為準）。本課採原創資料與算例；大型模型的結果需自行重做評估。
