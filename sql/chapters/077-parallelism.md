# 並行、單寫入者與鎖的範圍

先說明誰在協調，才談多開幾個工作能否更快。

## 工作獨立不表示輸出獨立

兩個任務可能讀不同資料，卻同時改同一個checkpoint或公開指標。沒有協調時，它們可能互相覆蓋，甚至各自認為成功。先畫出共享資源，再決定哪些部分可以並行。

## 本課採單一主機、單寫入工作區

writer.lock使用作業系統排他建立檔案，第二個工作會明確失敗。它不自動判定過期，也不是分散式lease；程序被強制中止後，操作者應先確認原工作是否仍存在，再按runbook處理鎖，不能只因等很久就刪除。

DuckDB嵌入式模式的原生資料庫寫入也有程序邊界。DuckDB 2.0的Quack或DuckLake提供其他協調模式，但不是本課開多個Python程序硬寫相同檔案的理由。PostgreSQL則可用資料庫交易與鎖，仍須控制競爭與重試。

## 平行擷取與統一發布

可讓獨立來源範圍先寫入各自未公開產物，再由單一協調者驗收與發布。若只是用目錄glob把所有檔案讀進來，就可能把未完成或不同版本產物混在一起。

從一個可靠工作區開始，量測瓶頸後再擴展。把併發數調大不是完整的資料工程策略；來源限制、記憶體、鎖與公開版本一致性都需要同時驗收。

## 專案中的實作

節錄 `examples/pipeline.py` 的 `writer_lock`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
@contextmanager
def writer_lock(workspace):
    workspace=Path(workspace).resolve();workspace.mkdir(parents=True,exist_ok=True)
    lock=workspace/'writer.lock'
    try:descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:raise RuntimeError('Workspace writer lock exists; inspect ownership before recovery') from None
    try:
        os.write(descriptor,str(os.getpid()).encode('ascii'));os.close(descriptor);descriptor=None
        yield
    finally:
        if descriptor is not None:os.close(descriptor)
        lock.unlink()
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/13.svg" target="_blank" rel="noopener" aria-label="放大並行、單寫入者與鎖的範圍圖解"><img src="assets/figures/13.svg" alt="並行、單寫入者與鎖的範圍：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「並行、單寫入者與鎖的範圍」讀圖：在交易邊界內找出四個變更，指出提交前失敗時為何資料與checkpoint都不能前進。請用圖回答：writer.lock存在很久，就能自動視為失效並刪除嗎？</p></div>

## 自我檢查與解析

**題目：**writer.lock存在很久，就能自動視為失效並刪除嗎？

<details><summary>展開解析</summary><p>不能。時間長短不能證明原寫入者已停止；本課不實作分散式lease，需確認程序與工作區狀態後按明確runbook恢復。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab35.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab35.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/connect/concurrency)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
