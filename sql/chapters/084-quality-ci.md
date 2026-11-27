# 把資料驗收放入CI與每批流程

程式測試和批次資料檢查互補，不以其中之一取代另一個。

## CI測程式與固定契約

在乾淨環境安裝鎖版套件、建立fixture、執行查詢及失敗恢復測試。這能攔住程式或依賴升版造成的改變；但昨天通過CI，不代表今天來源沒有新增非法狀態或缺少整批資料。

## 每批仍要驗收實際資料

對實際來源執行schema、完整性、鍵、來源範圍與指標對帳。必要規則失敗時，停止提交或發布，再依契約修復。檢查結果與來源版本應一起保存，才能重現當時的判斷。

## 小資料與正式負載

固定fixture適合語意與反例，不代表大型資料庫的鎖、效能和容量。伺服器特性由PostgreSQL實驗另外驗證，正式規模仍需負載與備份演練。測試報告要清楚列出哪一層真正執行過。

## 本課驗收路線

先跑test_examples核對DuckDB與完整管線，再在私人PostgreSQL 19環境執行postgres_lab，最後將下載包解壓到乾淨目錄重跑。不要只在作者目錄成功，卻漏掉SQL或fixture檔案。

將測試放進持續流程後，每次新增模型或修復資料都要維護相關反例。測試是一份可以重新執行的契約，不是只用來湊成功數字的清單。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/36.svg" target="_blank" rel="noopener" aria-label="放大把資料驗收放入CI與每批流程圖解"><img src="assets/figures/36.svg" alt="把資料驗收放入CI與每批流程：沿四種不同版本追蹤變動，再說明哪一組反例與恢復測試能證明語意在升級後仍成立。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「把資料驗收放入CI與每批流程」讀圖：沿四種不同版本追蹤變動，再說明哪一組反例與恢復測試能證明語意在升級後仍成立。請用圖回答：CI全部通過，今天的來源批次為何仍要做品質檢查？</p></div>

## 自我檢查與解析

**題目：**CI全部通過，今天的來源批次為何仍要做品質檢查？

<details><summary>展開解析</summary><p>CI通常驗證程式和固定fixture，無法證明新來源資料的實際內容與完整性。每批資料仍需按契約驗收。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab36.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab36.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
