# DataHarbor：解析、驗證與事件入庫

先拒絕不成立的來源，再把可重播證據寫入交易。

## 執行第一批

```powershell
python dataharbor.py --workspace .runtime/harbor --batch data/batch-001.json --show
```

工作區由你明確提供，首次建立資料庫與版本目錄。若輸入缺必要欄位、金額是布林或負數、時間沒有offset，會在寫入前拒絕。這些錯誤不是「沒有資料可處理」，不能以成功空結果回報。

## 來源範圍驗證

本課合成批次要求前後位置之間的事件序列完整，重複事件先依事件識別驗證完全相同再折疊。若不同事件占用同一序列，或少掉一個必要位置，會拒絕而不前進。這個稠密整數條件只適用本課source adapter。

## 目前狀態與原始事件

raw_events保存正規化payload與指紋，order_state按order_id保存最新來源版本。這兩層各自有唯一條件：事件鍵與來源序列不得衝突，訂單狀態則每訂單一列。不要為了「去重」而丟掉合法的多次更新。

## 驗收

讀回來源位置、原始事件數、目前訂單數與公開manifest。第一批完成後，位置4與付款12000應同時可解釋。若manifest尚未存在，需辨認是否在資料庫提交後、發布前中斷，而不是重新手工改checkpoint。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/33.svg" target="_blank" rel="noopener" aria-label="放大DataHarbor：解析、驗證與事件入庫圖解"><img src="assets/figures/33.svg" alt="DataHarbor：解析、驗證與事件入庫：核對第一批12000與第二批11500的不同來源狀態，指出更正、刪除及重播各自影響哪些層。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DataHarbor：解析、驗證與事件入庫」讀圖：核對第一批12000與第二批11500的不同來源狀態，指出更正、刪除及重播各自影響哪些層。請用圖回答：兩個不同事件使用同一seq，為何不能只保留最後讀到的一個？</p></div>

## 自我檢查與解析

**題目：**兩個不同事件使用同一seq，為何不能只保留最後讀到的一個？

<details><summary>展開解析</summary><p>本課來源契約要求序列位置唯一且範圍完整，衝突表示來源不成立。任意挑選會破壞游標的意義，應拒絕並修復來源。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab33.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab33.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/ddl-constraints.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
