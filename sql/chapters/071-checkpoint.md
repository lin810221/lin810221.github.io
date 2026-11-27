# 資料、checkpoint與outbox的提交邊界

讓已處理範圍與資料狀態一起成立，再安排可恢復的發布。

## 一個原子資料庫狀態

本課同一交易中寫入原始事件、更新目前訂單、前進來源位置並新增待發布outbox。交易中斷時，這些動作全部回滾；提交後，至少能知道還有一份發布工作沒有完成。

## 發布是第二個邊界

Parquet與current.json位於檔案系統。專題先產生未公開的版本資料，核對雜湊、筆數與付款總額，再原子替換小型指標檔。最後才把outbox標為已發布。資料庫與檔案並不是同一個通用交易，因此需要恢復規則。

若資料庫已提交但尚未發布，下次執行先完成待發布工作，再接下一批。若指標已替換但outbox尚未更新，則驗證既有不可變產物後重新完成標記，不把舊批次重套成新的金額變更。

## 保證的範圍

實驗注入程序失敗，證明可從明確狀態恢復；不把它擴大成所有斷電、檔案系統或分散式儲存的耐久保證。將來搬到物件儲存，需要重新設計條件寫入或版本協調，不能將本機rename語意直接搬過去。

## 驗收順序

在提交前、提交後與指標替換後分別中斷，確認checkpoint、資料與公開版本各停在哪裡。成功的標準是讀回結果正確、重跑不重複，而不是只有最後一行印出done。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/24.svg" target="_blank" rel="noopener" aria-label="放大資料、checkpoint與outbox的提交邊界圖解"><img src="assets/figures/24.svg" alt="資料、checkpoint與outbox的提交邊界：追蹤八個合成來源事件，核對第二批不是只有新增，並指出墓碑為何要留下刪除版本證據。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「資料、checkpoint與outbox的提交邊界」讀圖：追蹤八個合成來源事件，核對第二批不是只有新增，並指出墓碑為何要留下刪除版本證據。請用圖回答：資料庫提交後程序停止，為何outbox能幫助恢復？</p></div>

## 自我檢查與解析

**題目：**資料庫提交後程序停止，為何outbox能幫助恢復？

<details><summary>展開解析</summary><p>它與資料和checkpoint一起提交，留下尚未完成的發布工作。下次可先驗證並完成發布，再前進到新批次，而不需猜測哪些副作用已發生。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab24.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab24.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/statements/transactions)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
