# Airflow、dbt、Kafka與分散式工具的銜接

按責任選工具，保留已建立的契約與驗收。

## 工具各自接手哪一層

Airflow可管理工作與時間區間，dbt可管理SQL模型及測試，Kafka與CDC連接器可提供事件傳輸，Spark等引擎處理另一類分散式計算。它們不是同一件東西，也不是裝在一起就自然得到正確資料產品。

## 將本課成果逐步搬移

先把workflow的任務邊界對應排程節點，把命名SQL模型與品質規則對應模型工具，再讓來源adapter提供真實可重播位置。每搬一層，就重跑來源完整性、冪等、更正、刪除與失敗恢復測試。

## 服務驗收不能省略

真正部署需處理身分、秘密、網路、資源、版本、權限與操作手冊。這些平台的安裝與雲端服務不在本課已執行範圍，教材引用的是查核日正式文件中的責任概念，不提供未實測的整合成功宣稱。

## 規模不是唯一選擇條件

資料小也可能需要嚴格權限與稽核，資料大也不一定需要每個分散式工具。選擇前先量測工作負載、延遲、團隊能力與恢復要求。保留可以在本機重現的小fixture，能在複雜部署中繼續檢查基本語意。

相關獨立課程可跨課閱讀Django的資料存取與搜尋課的索引服務，但本課SQL和資料工程主線已完整保留，不因跨課連結就省略必要基礎。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/35.svg" target="_blank" rel="noopener" aria-label="放大Airflow、dbt、Kafka與分散式工具的銜接圖解"><img src="assets/figures/35.svg" alt="Airflow、dbt、Kafka與分散式工具的銜接：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Airflow、dbt、Kafka與分散式工具的銜接」讀圖：比較兩個實測引擎的參數與空值選項，再區分程序內分析和獨立伺服器責任，不能整段互貼語法。請用圖回答：將Python工作放進Airflow後，為什麼仍要測重跑和資料完整性？</p></div>

## 自我檢查與解析

**題目：**將Python工作放進Airflow後，為什麼仍要測重跑和資料完整性？

<details><summary>展開解析</summary><p>排程器管理呼叫與依賴，不會自動修復來源契約、去重與發布邊界。原有責任仍在工作和資料層，需要原樣驗收。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab35.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab35.py -->

## 官方來源

[本單元對應文件](https://airflow.apache.org/docs/apache-airflow/3.4.0/core-concepts/dag-run.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
