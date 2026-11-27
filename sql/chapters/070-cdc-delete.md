# CDC事件、刪除與墓碑

變更捕捉的價值不只有新增資料，也包括更正與刪除。

## 來源日誌與教學事件

真正CDC可從來源日誌取得提交位置、操作與前後資料，並與快照協調。連接器、複寫槽、保留與重新同步各有責任；本課用合成JSON事件測試這些語意，不冒充已啟用Debezium或Kafka。

本課來源範圍是單一分區、稠密整數seq。真實PostgreSQL LSN是日誌位置，不能逐一加一當作事件編號；多分區來源也通常需要各自的checkpoint，不能只取全部事件的一個最大值。

## 為什麼不直接刪掉狀態列

刪除事件在order_state中保留來源序列與deleted旗標，live_orders再排除它。若物理移除唯一的最新版本證據，較舊更新晚到時可能被當作新列插入，讓資料復活。

DataHarbor的刪除事件仍保留完整教學payload，這是本課契約，不代表所有CDC系統的刪除格式相同。某些來源只有鍵、某些有before值，必須按連接器配置處理。

## 版本與部署差異

PostgreSQL 19對logical replication初始化增加新機制，不能沿用所有舊版本都必須用相同重啟步驟的說法。若要真正啟用來源CDC，按19版文件檢查effective WAL設定、slot保存與清理；本課核心管線不建立持久複寫槽。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大CDC事件、刪除與墓碑圖解"><img src="assets/figures/24.svg" alt="CDC事件、刪除與墓碑：追蹤八個合成來源事件，核對第二批不是只有新增，並指出墓碑為何要留下刪除版本證據。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「CDC事件、刪除與墓碑」讀圖：追蹤八個合成來源事件，核對第二批不是只有新增，並指出墓碑為何要留下刪除版本證據。請用圖回答：本課的seq能否直接換成PostgreSQL LSN，並用加一檢查來源沒有缺事件？</p></div>

## 自我檢查與解析

**題目：**本課的seq能否直接換成PostgreSQL LSN，並用加一檢查來源沒有缺事件？

<details><summary>展開解析</summary><p>不能。本課稠密整數是合成來源契約，LSN不是逐事件連號；真實來源完整性必須由連接器與日誌協議處理。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab24.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab24.py -->

## 官方來源

[本單元對應文件](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
