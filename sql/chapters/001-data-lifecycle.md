# SQL、資料庫與資料工程的分工

先把查詢、儲存和可靠交付資料分開，再決定每個工具的位置。

## 一筆訂單走過哪些地方

使用者結帳後，應用程式將訂單寫進交易資料庫；分析工作再擷取訂單、檢查內容、轉成報表。SQL是描述資料操作的語言，資料庫是執行語言並管理資料的系統，資料工程則負責讓資料按契約、時間與品質條件可靠地流動。三者不是同義詞。

本課使用虛構商店：客戶、訂單、明細和退款。核心問題是「哪些訂單已付款、金額多少、每個地區的報表是否可重算」，不是先追求安裝最多平台。CSV、Parquet和資料庫檔案也有不同責任；一個檔案本身不會替你安排交易、權限和排程。

## OLTP與OLAP

OLTP常處理短交易，例如新增一筆付款；OLAP常掃描較多列做彙總，例如計算一季營收。兩者可能共用資料，但存取模式與延遲目標不同。本課用DuckDB完成本機SQL和分析管線，再以PostgreSQL實測多連線交易與權限，不把嵌入式分析資料庫直接當成網路交易服務。

## 閱讀與執行的位置

這個網站只是靜態教材，能離線閱讀，也能放GitHub Pages。SQL與Python程式在自己的電腦執行，沒有把私人資料送到網站。先跑第一個實驗，觀察回傳四筆已付款訂單，再沿課程追查每個數字的來源。範例全部使用合成資料，不需要真實公司資料或付費雲端帳號。

## 可執行查詢

以下是下載包 `queries/01.sql` 的實際內容；先由 `fixtures.seed` 建立本課合成資料。執行入口會建立獨立資料庫，不需修改既有資料。

```sql
-- Grain: one returned row per paid order, in a deterministic order.
SELECT order_id, customer_id, amount_cents
FROM orders
WHERE status = 'paid'
ORDER BY created_at, order_id;
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/01.svg" target="_blank" rel="noopener" aria-label="放大SQL、資料庫與資料工程的分工圖解"><img src="assets/figures/01.svg" alt="SQL、資料庫與資料工程的分工：追蹤來源、契約、查詢與交付四層，區分短交易和分析報表各自的責任。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「SQL、資料庫與資料工程的分工」讀圖：追蹤來源、契約、查詢與交付四層，區分短交易和分析報表各自的責任。請用圖回答：把CSV檔放進GitHub倉庫，是否就有完整資料管線？</p></div>

## 自我檢查與解析

**題目：**把CSV檔放進GitHub倉庫，是否就有完整資料管線？

<details><summary>展開解析</summary><p>沒有。還需明確的來源契約、處理步驟、品質檢查、重跑與發布機制；靜態檔案保存不能代替這些責任。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab01.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab01.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/clients/python/overview)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
