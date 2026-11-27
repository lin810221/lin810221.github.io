# 新鮮度、量測、SLO與告警

工作成功、資料新鮮和來源完整，不能合成一個綠燈。

## 分開監控三種狀態

程序是否成功結束、資料是否完整、產物是否足夠新鮮，是三個不同問題。排程準時且程式回傳零，仍可能讀到空來源或舊快照。監控應能指出是哪一層失敗。

## 新鮮度的定義

令 $t_{now}$ 是觀察時刻，$t_{event}$ 是這個指標採用的最後來源事件時間，定義：

$$F=t_{now}-t_{event}.$$

若觀察在01:00而最後來源時間為00:00，新鮮度落後為3600秒。先說明使用的是事件時間、提交時間還是資料發布時間；它們可能導出不同結果。本課拒絕負值，以提示未來時間或時鐘偏差，而不是將它默默當成零延遲。

## 來源靜止與工作落後

來源本來沒有新事件，與管線沒有處理新事件，是不同原因。可同時觀察來源高水位、已提交位置、待發布工作、失敗數與資料量，避免只看最後事件時間就發出錯誤告警。

## 可行動的告警

告警應附資料範圍、影響、負責人與runbook。重複發出沒有可操作資訊的訊息，只會讓真正問題更容易被忽略。SLO與閾值要按使用情境制定，本課的示意數字不是所有團隊通用標準。

## 專案中的實作

節錄 `examples/contracts.py` 的 `freshness`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def freshness(now,last_event):
    delta=(utc(now)-utc(last_event)).total_seconds()
    if delta<0:raise ValueError('Future event or clock skew')
    return delta
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大新鮮度、量測、SLO與告警圖解"><img src="assets/figures/32.svg" alt="新鮮度、量測、SLO與告警：沿來源到manifest再回讀，並在獨立恢復時間算例中區分資料落後和服務恢復時間。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「新鮮度、量測、SLO與告警」讀圖：沿來源到manifest再回讀，並在獨立恢復時間算例中區分資料落後和服務恢復時間。請用圖回答：新鮮度顯示負值時，為什麼不能直接改成0並視為表現很好？</p></div>

## 自我檢查與解析

**題目：**新鮮度顯示負值時，為什麼不能直接改成0並視為表現很好？

<details><summary>展開解析</summary><p>負值可能代表未來時間或時鐘偏差，應揭露與診斷。改成0會掩蓋時間契約問題，讓指標失去意義。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab32.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab32.py -->

## 官方來源

[本單元對應文件](https://openlineage.io/docs/spec/object-model/)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
