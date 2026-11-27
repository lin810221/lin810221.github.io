# DataHarbor：更正、刪除與舊批重播

以新的來源版本更新狀態，並保留刪除證據。

## 接續第二批

```powershell
python dataharbor.py --workspace .runtime/harbor --batch data/batch-002.json --show
```

第二批的after_seq必須等於已提交位置。若直接從空工作區執行第二批，會因游標不相符失敗，而不是跳過第一批。來源沒有證明完成，就不能由目標程式自行猜測缺口已處理。

## 四個變更

訂單102的金額修正為4500，101收到刪除事件，105加入1000，103從取消改成付款2000。104仍為付款4000，因此最後付款共11500。order_state仍保留101的墓碑，live_orders與Parquet不公開這筆刪除狀態。

## 舊批次不讓公開版本倒退

再傳第一批相同內容時，程式辨認已處理並返回replayed，不能將current.json指回位置4。若以同一batch id傳不同內容，則直接拒絕，不讓既有證據被覆寫。

## 檢查真正的結果

讀回checkpoint、raw事件數、存活列數、付款總額與manifest版本。只看終端機最後回報成功，無法證明金額與公開指標保持一致。下載包測試會把第一批和第二批多次重送，確認結果不改變。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/33.svg" target="_blank" rel="noopener" aria-label="放大DataHarbor：更正、刪除與舊批重播圖解"><img src="assets/figures/33.svg" alt="DataHarbor：更正、刪除與舊批重播：核對第一批12000與第二批11500的不同來源狀態，指出更正、刪除及重播各自影響哪些層。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「DataHarbor：更正、刪除與舊批重播」讀圖：核對第一批12000與第二批11500的不同來源狀態，指出更正、刪除及重播各自影響哪些層。請用圖回答：第二批完成後重新送第一批，current.json應回到第一批版本嗎？</p></div>

## 自我檢查與解析

**題目：**第二批完成後重新送第一批，current.json應回到第一批版本嗎？

<details><summary>展開解析</summary><p>不應。舊批次相同內容只是重播，最新已發布狀態應維持位置8；否則會讓讀取者看到已被更正或刪除的舊結果。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab33.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab33.py -->

## 官方來源

[本單元對應文件](https://duckdb.org/docs/2.0/sql/statements/merge_into)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
