# SQLite、DuckDB與PostgreSQL的遷移檢查

把語法可執行、結果相同和部署能力相同分開驗收。

## 從共同SQL開始

明確的SELECT、JOIN與GROUP BY較容易建立共同主線；值參數、日期函數、JSON、型別轉換、索引和併發則需逐項比較。不要因三者都接受CREATE TABLE，就推定資料型別與交易邊界完全一致。

## SQLite的型別與外鍵

SQLite的型別系統與嚴格表選項有自身規則，外鍵啟用也需確認；Python內建sqlite3的連結版本則要另外查。這次Python 3.15.2內建3.53.4，官網最新主線3.54.1，兩個數字不可混用。

## DuckDB 2.0檔案與API

DuckDB 2.0的原生儲存格式與部分Python API有升版差異，舊版程式與資料檔需要依官方遷移說明驗證。公開交換可使用有明確schema的Parquet，但它不會保存所有資料庫物件、交易或權限設定。

## 實際遷移清單

比較空值、精確金額、時間與時區、主外鍵、排序同值、窗口frame、JSON轉型與錯誤處理。再測參數、交易隔離、索引與權限。小資料的語意通過後，才進入容量與正式負載。

本課將核心DuckDB實驗與PostgreSQL專用測試分開，讓你能指出哪個結果在哪個引擎被驗證。這個區分比宣稱一份SQL在所有資料庫都一樣更有助於實務維護。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/35.svg" target="_blank" rel="noopener" aria-label="放大SQLite、DuckDB與PostgreSQL的遷移檢查圖解"><img src="assets/figures/35.svg" alt="SQLite、DuckDB與PostgreSQL的遷移檢查：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SQLite、DuckDB與PostgreSQL的遷移檢查」讀圖：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。請用圖回答：將資料匯成Parquet後，原本資料庫的RLS和交易設定會一起跟著走嗎？</p></div>

## 自我檢查與解析

**題目：**將資料匯成Parquet後，原本資料庫的RLS和交易設定會一起跟著走嗎？

<details><summary>展開解析</summary><p>不會。Parquet主要保存資料與相關schema資訊，資料庫物件、權限和交易部署能力需另外遷移與驗證。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab35.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab35.py -->

## 官方來源

[本單元對應文件](https://www.sqlite.org/lang.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
