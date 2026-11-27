# 總複習、術語與版本驗證紀錄

把SQL語意、資料可靠性與實際測試範圍一起帶走。

## 完成後應能做的事

先定義每份資料粒度、鍵、單位與時間；寫出可手算的查詢；辨認NULL、JOIN與window的邊界；讀實際計畫；建立可重跑的ETL或ELT；處理更正、刪除、來源位置與品質；最後以版本化產物交付可追溯結果。

## 本次版本基準

查核日為2026-11-27。主線使用DuckDB 2.0.1與Python 3.15.2，伺服器主線PostgreSQL 19.0與Psycopg 3.3.9。SQLite官網主線3.54.1只作比較；實測Python內建版本3.53.4另列，不混稱最新版執行環境。

## 驗證與限制

下載包包含36個離線入口、真實DuckDB查詢、DataHarbor、手動DAG、歷史維度、品質與恢復測試。PostgreSQL私人叢集實測隔離、列鎖、Serializable衝突、RLS與19版新語法。大型負載、Quack、DuckLake、雲端物件儲存和外部CDC平台則沒有冒稱已部署。

## 學習資源

[版本與驗證紀錄](study/versions.json)、[來源索引](study/sources.md)、[中英術語](study/glossary.md)、[學習單](study/worksheet.md)與[解析](study/answers.md)均可離線保存。程式與圖解各有獨立下載包，公式使用本機LaTeX排版資源，不依賴CDN。

## 下一步

用自己的合成資料重做一份小型資料產品，先寫契約和反例，再選工具。若要跨課閱讀，可接Django理解網站資料存取，接搜尋與向量資料庫理解檢索服務；這些是不同主線，本課不需要先完成它們才可學習。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/36.svg" target="_blank" rel="noopener" aria-label="放大總複習、術語與版本驗證紀錄圖解"><img src="assets/figures/36.svg" alt="總複習、術語與版本驗證紀錄：沿四種不同版本追蹤變動，再說明哪一組反例與恢復測試能證明語意在升級後仍成立。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「總複習、術語與版本驗證紀錄」讀圖：沿四種不同版本追蹤變動，再說明哪一組反例與恢復測試能證明語意在升級後仍成立。請用圖回答：升級資料工程工具時，最值得保留的驗收資產是什麼？</p></div>

## 自我檢查與解析

**題目：**升級資料工程工具時，最值得保留的驗收資產是什麼？

<details><summary>展開解析</summary><p>可重現fixture、資料契約、預期結果、反例、故障恢復測試與版本紀錄。它們能跨工具維護語意，不只是保留某一份成功截圖。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab36.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab36.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/release-19.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
