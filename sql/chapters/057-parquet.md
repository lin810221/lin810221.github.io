# Parquet的列組、欄位chunk與型別

用檔案內部結構解釋為什麼部分分析可以少讀資料。

## 列式格式的基本構造

Parquet將資料分成row group，各組再依欄位形成column chunk，內部包含頁與metadata。這讓分析引擎有機會只讀需要的欄位，並按統計排除部分列組；它不是每列都隨機讀取的交易資料庫。

型別、壓縮與列組大小會影響讀取成本。檔案可保存精確數值與時間型別，但來源轉型若已錯誤，換成Parquet不會自動修好。也不能因為檔案小，就推論所有查詢一定更快。

## 本課的真實往返實驗

先把五筆訂單按鍵寫入壓縮Parquet，再重新讀回筆數與總額，應得到五筆與15000美分。這個對帳包含取消訂單，與付款總額13000不同。回讀時仍明確選擇欄位與條件，不能依寫入順序推定輸出順序。

## 原生檔案和開放交換格式

DuckDB資料庫檔方便保存多張表與交易狀態，Parquet則適合資料交換與分析快照。版本升級時，資料庫檔案相容性與Parquet欄位契約是不同問題；本課會分開保存執行器版本、模型版本和產物雜湊。

圖解中的矩形表示欄位與列組，不表示實際壓縮比例。真正裁剪效果應觀察引擎計畫與讀取量，不只看格式名稱。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大Parquet的列組、欄位chunk與型別圖解"><img src="assets/figures/20.svg" alt="Parquet的列組、欄位chunk與型別：找出只需要金額且日期相交的候選區塊，理解投影和列組裁剪是不同維度，並非保證所有查詢只讀一格。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Parquet的列組、欄位chunk與型別」讀圖：找出只需要金額且日期相交的候選區塊，理解投影和列組裁剪是不同維度，並非保證所有查詢只讀一格。請用圖回答：五筆訂單寫入Parquet後總額15000，為何不同於付款總額13000？</p></div>

## 自我檢查與解析

**題目：**五筆訂單寫入Parquet後總額15000，為何不同於付款總額13000？

<details><summary>展開解析</summary><p>檔案保存所有五筆訂單，包含取消訂單103的2000。兩個數字的輸入集合不同，對帳前必須先確認狀態口徑。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab20.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab20.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/data/parquet/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
