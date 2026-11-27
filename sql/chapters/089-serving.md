# 提供資料、授權與一致版本

把內部處理成果交給使用者前，先定義讀取契約。

## 服務方式的選擇

可提供資料庫View、固定版本檔案、API或分析工具連線。每種方式都有不同的權限、延遲與相容性責任。將Parquet放到公開網站，不會自動具備逐使用者授權；私人資料應由適當服務與存取政策保護。

## 一次讀取固定版本

DataHarbor讀取current.json後，依其中的不可變版本檔案讀資料並驗證雜湊。不要在同一個報表中每次查欄位都重新讀current，否則可能混用兩個合法版本。讀取者也需按策略處理版本被保留或回收的時點。

## 欄位相容與資訊最小化

只提供使用者需要的欄位，標示單位、日期口徑和更新位置。移除敏感欄位、限制資料範圍與避免不必要的明細曝光，比單純替欄名換英文更重要。彙總資料也可能有重識別風險，應按情境評估。

## 授權不只在寫入端

列表、下載、View與API都要檢查讀取者能看什麼。PostgreSQL的GRANT與RLS在後章分別驗證，不能因ETL工作帳號可以讀全部資料，就把相同權限交給所有報表使用者。

最後留下資料版本、驗收狀態和新鮮度，讓使用者能判斷這份結果是否適合目前任務，而不是只看檔名叫latest就認為內容一定完整。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/34.svg" target="_blank" rel="noopener" aria-label="放大提供資料、授權與一致版本圖解"><img src="assets/figures/34.svg" alt="提供資料、授權與一致版本：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「提供資料、授權與一致版本」讀圖：以首次發布來源0到4為例，比對提交前、提交後與指標替換後的狀態，說明恢復不能再次套用業務變更。請用圖回答：報表過程中反覆讀current.json，為何可能混用資料版本？</p></div>

## 自我檢查與解析

**題目：**報表過程中反覆讀current.json，為何可能混用資料版本？

<details><summary>展開解析</summary><p>指標可能在讀取之間切到新版本。應先固定一次讀取的manifest，再從其不可變產物取得一致資料。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab36.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab36.py -->

## 官方來源

[本單元對應文件](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
