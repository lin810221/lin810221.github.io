# GRANT、角色與Row-Level Security

表級權限、資料列政策與應用程式身分，要分別驗證。

## 權限不只分讀與寫

PostgreSQL角色可獲得schema、表、欄位與其他物件的權限。能連線不表示能讀表，能讀表也不表示業務上能看全部資料。先列出工作與讀取者的責任，再授予必要權限。

## RLS的作用

啟用資料列安全後，政策限制可見或可修改的列；沒有適用政策時通常預設拒絕。但superuser、BYPASSRLS與表擁有者的行為不同，不能用管理者查詢看見全部資料，就斷定政策沒有作用或已正確保護一般角色。

本課建立私人測試角色，賦予必要的schema使用與SELECT，再用只允許tenant 1的政策。以該角色讀取應只得到一筆租戶資料。測試後清除只屬本次實驗的schema和角色。

## 身分來源必須可信

若政策只依賴一個使用者可以任意SET的租戶變數，攻擊者可能改值後讀到其他租戶。應由可信服務與角色設計建立身分及資料範圍，並處理連線池的狀態重設；不要把方便傳值的方式直接當成可信認證。

RLS也不能取代所有欄位、下載和外部檔案授權。將資料匯出Parquet後，原資料庫政策不會自動跟著檔案繼續執行，必須另外管理產物存取。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/31.svg" target="_blank" rel="noopener" aria-label="放大GRANT、角色與Row-Level Security圖解"><img src="assets/figures/31.svg" alt="GRANT、角色與Row-Level Security：以受限角色追蹤租戶資料列，指出表級SELECT權限不等於可以讀取所有租戶，也不能用superuser代替驗收。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「GRANT、角色與Row-Level Security」讀圖：以受限角色追蹤租戶資料列，指出表級SELECT權限不等於可以讀取所有租戶，也不能用superuser代替驗收。請用圖回答：使用superuser測到可以讀全部資料，為何不能拿來驗證一般角色的RLS效果？</p></div>

## 自我檢查與解析

**題目：**使用superuser測到可以讀全部資料，為何不能拿來驗證一般角色的RLS效果？

<details><summary>展開解析</summary><p>superuser可繞過一般資料列安全規則；應以真正受限制的角色測試可見與不可見列，並另外確認角色與政策設定。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab31.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab31.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-rowsecurity.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
