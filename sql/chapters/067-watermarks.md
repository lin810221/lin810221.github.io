# Watermark、固定上界與遺漏風險

增量不只是把WHERE改成更新時間大於上次。

## 先說清楚watermark代表什麼

它可能是來源更新時間、已處理事件時間，或來源日誌位置。這些資訊有不同的排序和完整性能力。只保存最大event time，不能證明所有較早事件都已到齊；只讀目前表，也可能完全看不到刪除。

## 一批有明確的上下界

常見做法在批次開始時固定來源上界，讀取上次成功位置到該上界之間的變更，完成驗收後再前進。若來源資料在擷取期間改變，仍需來源快照或日誌協議來支撐完整性，不能只憑WHERE條件作保證。

時間精度、時鐘誤差和同值更新都要納入。來源若可更正過去時間、或相同時間還有未讀資料，嚴格大於一個時間值會漏列。這是契約問題，不是單純把資料型別改成更細的時間精度就一定解決。

## 失敗時的游標

資料與checkpoint應在同一個適用交易中提交，或透過明確的恢復協議協調。若先保存游標，後續寫入失敗，重跑可能跳過尚未完成資料；若只保存資料而不保存去重證據，又可能重複套用副作用。

本課在合成來源中使用單一、閉合、稠密整數序列，後續會說明這是教學契約，不能拿來對真實PostgreSQL LSN做加一運算。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/23.svg" target="_blank" rel="noopener" aria-label="放大Watermark、固定上界與遺漏風險圖解"><img src="assets/figures/23.svg" alt="Watermark、固定上界與遺漏風險：辨認本課序列範圍不包含after而包含through，再與日期半開區間對照，避免把兩個契約混成同一條件。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Watermark、固定上界與遺漏風險」讀圖：辨認本課序列範圍不包含after而包含through，再與日期半開區間對照，避免把兩個契約混成同一條件。請用圖回答：保存目前看過最大的事件時間，能否證明更早事件全部到齊？</p></div>

## 自我檢查與解析

**題目：**保存目前看過最大的事件時間，能否證明更早事件全部到齊？

<details><summary>展開解析</summary><p>不能。事件可能遲到或被更正，時間最大值不等於來源完整性證據；需要來源協議、遲到政策與可重算範圍。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab23.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab23.py -->

## 官方來源

[本單元對應文件](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
