# 202 Accepted 與持久化工作狀態

把長工作從HTTP連線分離，客戶端才能可靠追蹤。

## 接受不代表完成

POST jobs通過認證、輸入與文件授權後，在資料庫建立queued工作和事件，再回202與工作ID。worker未啟動時工作會保留queued；API不在回應後偷偷用記憶體task承擔核心計算。

## 定義合法狀態

queued可被claim為running，running最後提交succeeded、failed或cancelled。queued取消直接進cancelled；running取消先記錄意圖，發布時再判斷。資料庫CheckConstraint阻止任意狀態字串，服務方法另外限制合法轉移。

## 客戶端持有的是識別，不是執行權

查詢工作仍需相同租戶權限，工作ID不是公開下載憑證。前端應展示排隊、執行中與終止狀態，對timeout區分訂閱連線到期和持久化工作失敗。使用者刷新網頁後，能以工作ID重新取得狀態。

## 對照完整專案

以下節錄 `gateway/store.py` 的 `_job`。保留完整程式包的匯入、外層設定與相關類別，節錄不是可獨立執行的完整檔案。

```python
    @staticmethod
    def _job(row):
        return {'id': row.id, 'state': row.state, 'attempt': row.attempt, 'cancel_requested': bool(row.cancel_requested), 'result': json.loads(row.result_json) if row.result_json else None}
```

## 看圖追蹤責任與時間

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大202 Accepted 與持久化工作狀態圖解"><img src="assets/figures/17.svg" alt="queued經claim進入running，再提交成功、失敗或取消。" loading="lazy"></a><figcaption>持久化工作狀態。固定教學資料與簡化機制，非實際效能量測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「202 Accepted 與持久化工作狀態」讀圖：畫出queued取消與running取消的不同路徑。再用本節的條件回答：送出工作後一直queued，最先應檢查什麼？</p></div>

## 自我檢查與解析

**問題：**送出工作後一直queued，最先應檢查什麼？

<details><summary>展開解析</summary><p>先確認worker是否啟動、是否讀同一資料庫路徑、是否有權取得工作；202本身不表示worker已開始或完成。</p></details>

## 執行與驗收

執行 `python lab19.py`，先用 `python run_lab.py --list` 核對這個實驗的目標。觀察成功輸出，也保留本節要求的錯誤反例；數個閱讀單元可以從不同角度使用同一個機制實驗。完整專案與測試位於程式下載包，核心不需要API key或模型權重。

<!-- example:lab19.py -->

本課真實執行FastAPI、SQLAlchemy、SQLite、HTTPX、SSE與獨立worker；預設供應商只依固定原文抽句，沒有冒稱通用LLM理解。OpenAI介面以MockTransport驗證，實際付費呼叫、容器、OIDC服務、外部代理與正式負載須另行驗收。

## 官方與原始來源

[本單元對應文件](https://fastapi.tiangolo.com/tutorial/background-tasks/)。查核日：2026-11-27；主線FastAPI 0.165.0、Python 3.15.2，完整鎖版與實測邊界見學習包版本紀錄。
