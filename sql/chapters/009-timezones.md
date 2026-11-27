# 日期、時間戳記與時區

同一瞬間、當地時鐘與業務日期是三個不同概念。

## 先定義欄位的時間意義

訂單建立時間、來源更新時間、事件發生時間與管線擷取時間可能各不相同。用一個叫做 `time`的欄位承擔所有責任，會讓增量與延遲分析變得模糊。請在資料字典中逐一命名並說明。

帶時區的時間可以正規化為UTC瞬間，再按需要轉成顯示時區。資料庫的 `TIMESTAMPTZ`通常保存瞬間語意，不保證保留使用者原來輸入的時區名稱；若需要原始地區，應另外保存。把沒有offset的文字直接當UTC，只有在來源契約明確規定時才成立。

## 日期邊界不是固定24小時

業務上的某一天應先指定時區，再產生半開區間。夏令時間切換可能使當地一天不是24小時。用「昨天的UTC時間減去固定秒數」冒充某地的日界線，會在這些情境出錯。

```python
from contracts import utc
assert utc('2026-11-01T08:00:00+08:00') == utc('2026-11-01T00:00:00Z')
```

本課的固定實驗一律以UTC分組。真實專案若改用台灣、紐約或其他業務時區，須同步修改區間定義、測試與指標說明，不只改畫面顯示格式。拒絕無時區輸入，是讓問題提早出現，而不是在報表階段猜測來源。

## 專案中的實作

節錄 `examples/contracts.py` 的 `utc`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def utc(value):
    moment=datetime.fromisoformat(value.replace('Z','+00:00'))
    if moment.tzinfo is None or moment.utcoffset() is None:raise ValueError('Timezone required')
    return moment.astimezone(timezone.utc)
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大日期、時間戳記與時區圖解"><img src="assets/figures/03.svg" alt="日期、時間戳記與時區：逐列比較NULL、零和空字串，辨認一般比較、空值判定和COUNT如何處理它們。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「日期、時間戳記與時區」讀圖：逐列比較NULL、零和空字串，辨認一般比較、空值判定和COUNT如何處理它們。請用圖回答：TIMESTAMPTZ能否讓你事後還原使用者最初輸入的時區名稱？</p></div>

## 自我檢查與解析

**題目：**TIMESTAMPTZ能否讓你事後還原使用者最初輸入的時區名稱？

<details><summary>展開解析</summary><p>不能直接如此推論。它主要表達瞬間，顯示受連線時區影響；若原始地區或offset有業務用途，應另外保存。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab03.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab03.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/datatype-datetime.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
