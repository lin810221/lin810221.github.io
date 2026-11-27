# JSON文件、JSON Lines與schema漂移

明確區分檔案外框、事件外框和欄位型別。

## 兩種常見外框

一份JSON文件可能是一個物件或陣列；JSON Lines則通常每行是一份完整JSON值。它們的讀取方式與錯誤定位不同，不能只因副檔名相似就用同一種逐行處理。資料包含內嵌換行字元時，也要由解析器理解跳脫。

## 欄位存在不等於型別正確

來源可能把amount由字串改成數字、把id改成陣列，或開始省略原本必要欄位。先保存原文與schema版本，再判定能否相容。可忽略的新增欄位與破壞性單位變更，要分開處理。

本課DataHarbor採固定JSON批次外框，事件欄位集合必須符合契約。批次含識別、前後序列邊界及事件列表；一個可以解析的JSON檔不一定有完整來源範圍，因此還需要序列檢查。

## 流式讀取與批次邊界

大型事件檔可逐段解析以降低記憶體，但處理到一半失敗時，必須知道哪些範圍已提交。不能把檔案行號當作所有來源的穩定游標；壓縮、重新排序與來源重建都可能改變位置。

## 欄位升級的測試

保留舊版、目前版、缺欄位與型別衝突的fixture。新增相容邏輯後，驗證舊資料仍得到相同語意，再允許新版本進入正式模型。不要只測最新的一筆正常事件。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大JSON文件、JSON Lines與schema漂移圖解"><img src="assets/figures/19.svg" alt="JSON文件、JSON Lines與schema漂移：將同一列CSV讀成三個合法欄位，指出引號中的逗號不是分隔，001也不是可任意轉型的整數。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「JSON文件、JSON Lines與schema漂移」讀圖：將同一列CSV讀成三個合法欄位，指出引號中的逗號不是分隔，001也不是可任意轉型的整數。請用圖回答：JSON能成功解析，是否代表事件批次完整且可安全前進checkpoint？</p></div>

## 自我檢查與解析

**題目：**JSON能成功解析，是否代表事件批次完整且可安全前進checkpoint？

<details><summary>展開解析</summary><p>不代表。還需驗證事件契約、識別、序列範圍與來源完整性；格式正確只通過最外層檢查。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab19.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab19.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/data/json/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
