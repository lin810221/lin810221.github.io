# 排程時間、資料區間與時區

工作什麼時候啟動，和它應處理哪段資料，不是同一個時間。

## 區間需要明確邊界

每日工作常在資料日結束後才執行。排程器的執行時間、logical date與資料區間各有定義；不能把程序啟動的now直接當成需要查詢的日期。手動重跑上個月資料時，這個差異尤其明顯。

Airflow 3.4的裸cron排程預設使用 `CronTriggerTimetable`，資料區間起點和終點可能都是觸發時間。若需要連續的每日資料區間，應明確選擇 `CronDataIntervalTimetable`，或按官方設定啟用 `create_cron_data_intervals`；不能從排程字串自行假設一定代表前一整天。下載包的workflow是手動觸發，沒有自動啟動背景排程。要加入服務時，需另行驗收重跑、catchup、併發與認證設定。

## 半開日期區間

先依業務時區計算某日的開始與下一日開始，再換成來源使用的瞬間範圍。夏令時間會改變某些日子的實際長度，不能一律以固定24小時替代當地日界線。

## 依資料位置重跑

工作參數保存要處理的來源範圍或資料日期，讓同一次邏輯批次在不同時間重做仍有一致輸入。若每次都讀取「最近一天」，重試就可能悄悄換成另一批資料，無法驗證冪等。

最後記錄排程規則、來源完成條件、逾時與遲到政策。工作準時啟動但來源未完整，和工作本身晚啟動，是不同的問題；監控也應分開呈現。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大排程時間、資料區間與時區圖解"><img src="assets/figures/23.svg" alt="排程時間、資料區間與時區：辨認本課序列範圍不包含after而包含through，再與日期半開區間對照，避免把兩個契約混成同一條件。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「排程時間、資料區間與時區」讀圖：辨認本課序列範圍不包含after而包含through，再與日期半開區間對照，避免把兩個契約混成同一條件。請用圖回答：昨天的工作今天才重跑，能否直接以程序啟動時的now推算查詢範圍？</p></div>

## 自我檢查與解析

**題目：**昨天的工作今天才重跑，能否直接以程序啟動時的now推算查詢範圍？

<details><summary>展開解析</summary><p>不應。應使用該邏輯批次原本的資料區間，否則重跑可能讀到不同來源，破壞重現與去重契約。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab25.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab25.py -->

## 官方來源

[本單元對應文件](https://airflow.apache.org/docs/apache-airflow/3.4.0/core-concepts/dag-run.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
