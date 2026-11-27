# 重試、退避與有限預算

先辨認錯誤是否可能暫時恢復，再限制成本與等待。

## 先分錯誤，再決定重試

連線暫時中斷、明確的序列化衝突，和schema不相容、非法金額，是不同問題。重試不會修好錯誤的輸入；無限重試還可能放大來源負載、延誤其他批次並掩蓋真正原因。

## 有上限的指數退避

令第 $i$ 次等待從 $i=0$ 開始，基礎等待 $b>0$、上限 $c>0$，教學模型為：

$$d_i=\min(c,b2^i).$$

若最多嘗試5次，兩次嘗試之間最多有4次等待。設定 $b=1$ 秒、$c=4$ 秒，等待為1、2、4、4秒，總等待11秒；這不含工作本身與連線超時的時間。正式系統可能再加jitter，應同樣定義其範圍與總預算。

## 實作的邊界

contracts實驗只計算等待，不真的睡眠；orchestrator則會對明確的TransientError套用有限等待，其他錯誤直接停止，阻止下游工作。測試注入等待函數記錄預期秒數，驗證控制邏輯而不拖長離線驗收。

可重試並不代表只重送最後一個SQL敘述。Serializable衝突應重新執行整個交易；外部副作用則先確定是否可重複。把錯誤全部改包成TransientError，會破壞這份分類責任。

## 專案中的實作

節錄 `examples/orchestrator.py` 的 `run_dag`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def run_dag(dependencies,tasks,max_attempts=3,sleeper=time.sleep):
    order=topological_sort(dependencies)
    if set(tasks)!=set(dependencies):raise ValueError('Every task needs exactly one callable')
    delays=retry_delays(max_attempts);events=[];results={}
    for name in order:
        for attempt in range(1,max_attempts+1):
            try:
                results[name]=tasks[name]();events.append({'task':name,'attempt':attempt,'status':'success'});break
            except Exception as exc:
                events.append({'task':name,'attempt':attempt,'status':'failed','error_type':type(exc).__name__})
                if not isinstance(exc,TransientError) or attempt==max_attempts:raise TaskFailed(name,events) from exc
                sleeper(delays[attempt-1])
    return {'order':order,'results':results,'events':events}
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/26.svg" target="_blank" rel="noopener" aria-label="放大重試、退避與有限預算圖解"><img src="assets/figures/26.svg" alt="重試、退避與有限預算：從五次嘗試數出只有四個間隔，核對上限退避的等待時間，並把等待與工作耗時分開。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「重試、退避與有限預算」讀圖：從五次嘗試數出只有四個間隔，核對上限退避的等待時間，並把等待與工作耗時分開。請用圖回答：最多嘗試5次、等待1、2、4、4秒時，為何不能說總耗時一定11秒？</p></div>

## 自我檢查與解析

**題目：**最多嘗試5次、等待1、2、4、4秒時，為何不能說總耗時一定11秒？

<details><summary>展開解析</summary><p>11秒只是重試間等待，尚未包含每次工作執行、連線超時與其他固定成本。總預算必須把這些項目一起計入。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab26.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab26.py -->

## 官方來源

[本單元對應文件](https://airflow.apache.org/docs/apache-airflow/3.4.0/core-concepts/dag-run.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
