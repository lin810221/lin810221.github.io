# 工作失敗、依賴阻擋與恢復紀錄

把成功定義成成果已驗證，而不是某段程式回傳零。

## 工作狀態與資料狀態

工作可能已寫入資料卻在回報成功前失敗，也可能程式結束成功但輸出資料不完整。因此要區分執行嘗試、資料提交與對外發布。這也是outbox與讀回驗證的重要性。

## 失敗必須阻止不成立的下游

本課run_dag在永久錯誤或重試預算耗盡後拋出TaskFailed，後續依賴不再執行。它保存工作名、嘗試次數、狀態與錯誤類型，不把完整來源payload與憑證塞進紀錄。

這個執行器不持久保存排程歷史；程序重啟時會再走一次DAG。工作之所以可安全重做，是因DataHarbor的批次識別與交易契約，而不是記憶體中的results字典永久存在。

## 驗收一條完整路徑

先讓第一個工作暫時失敗兩次、第三次成功，確認等待預算與下游順序。再改成輸入契約錯誤，確認不重試且不執行依賴工作。最後將整個workflow重做，確認公開快照不變。

要部署成服務時，再加入持久狀態、排程權限、併發限制、告警與操作手冊。不要將課程的手動執行器直接宣稱成已完成正式Airflow部署。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/25.svg" target="_blank" rel="noopener" aria-label="放大工作失敗、依賴阻擋與恢復紀錄圖解"><img src="assets/figures/25.svg" alt="工作失敗、依賴阻擋與恢復紀錄：由兩個來源追蹤到staging及品質發布，辨認紅色回邊會構成循環，圖的合法性不等於資料正確。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「工作失敗、依賴阻擋與恢復紀錄」讀圖：由兩個來源追蹤到staging及品質發布，辨認紅色回邊會構成循環，圖的合法性不等於資料正確。請用圖回答：本課run_dag程序重啟後沒有持久results，為何仍可重跑DataHarbor workflow？</p></div>

## 自我檢查與解析

**題目：**本課run_dag程序重啟後沒有持久results，為何仍可重跑DataHarbor workflow？

<details><summary>展開解析</summary><p>每個資料工作本身按批次內容與checkpoint辨識已處理狀態，重播可安全返回。冪等由工作和資料層保護，不依賴記憶體結果永遠存在。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab25.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab25.py -->

## 官方來源

[本單元對應文件](https://airflow.apache.org/docs/apache-airflow/3.4.0/core-concepts/dag-run.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
