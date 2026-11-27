# 血緣、資料字典與執行證據

讓讀者能從指標回到來源與轉換版本。

## 設計血緣與執行血緣

設計血緣說明哪些模型依賴哪些資料集，執行血緣則記錄某次工作實際讀寫了哪些版本。DAG依賴、資料字典與執行紀錄互補；只畫一張漂亮流程圖，不足以證明某次產物使用了哪批資料。

OpenLineage把Job、Run與Dataset等概念分開，提供正式事件規格。本課參考其責任分工，但manifest是本課的精簡格式，沒有冒稱已實作完整OpenLineage相容事件或後端。

## 最小可追溯資訊

來源識別與範圍、原始內容指紋、模型版本、執行器版本、產物位置、雜湊與品質結果。這些資料要能互相連起來，才能從「某日總額不對」定位受影響批次。

## 資料字典補上語意

欄位名稱與型別之外，還要記錄單位、日期角色、空值、唯一性與歷史政策。兩個都叫amount的欄位，若一個是美分、一個是美元，單靠血緣連線並無法解決解讀問題。

本課current.json指到不可變版本，版本manifest再記錄來源處理位置與模型版本；raw_events保留事件與payload指紋。它提供可以從成果回查來源的實作起點，正式系統仍需更完整的來源catalog與治理整合。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/32.svg" target="_blank" rel="noopener" aria-label="放大血緣、資料字典與執行證據圖解"><img src="assets/figures/32.svg" alt="血緣、資料字典與執行證據：沿來源到manifest再回讀，並在獨立恢復時間算例中區分資料落後和服務恢復時間。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「血緣、資料字典與執行證據」讀圖：沿來源到manifest再回讀，並在獨立恢復時間算例中區分資料落後和服務恢復時間。請用圖回答：manifest裡有來源位置與雜湊，是否就等於已完成OpenLineage協定整合？</p></div>

## 自我檢查與解析

**題目：**manifest裡有來源位置與雜湊，是否就等於已完成OpenLineage協定整合？

<details><summary>展開解析</summary><p>不是。本課是精簡的可追溯格式，OpenLineage有正式的Job、Run、Dataset與事件規格；相容整合需要另外實作及驗證。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab32.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab32.py -->

## 官方來源

[本單元對應文件](https://openlineage.io/docs/spec/object-model/)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
