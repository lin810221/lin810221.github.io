# 數值型別與金額的精確表示

用整數最小單位或固定小數，避免把二進位近似當作財務規則。

## 整數、小數與浮點

整數適合數量與最小計價單位，`DECIMAL`保存指定精度的小數，浮點則適合容許近似的測量與科學計算。它們不是依數字有沒有小數點來隨意選擇。`DECIMAL(12,2)`的總位數為12，小數位數為2；整數部分的可用位數不是12。

本課訂單使用整數USD cents。顯示成美元時才換算，寫入前先檢查來源是否超出兩位小數。若來源是 `12.505`，不能默默截成1250或讓資料庫替你猜四捨五入政策；應拒絕或依已定義的規則處理。匯率、稅額和跨幣別必須另外設計，不能將不同幣別直接加總。

## 換算的定義與條件

對本課已驗證且不多於兩位小數的非負美元金額，令 $d$ 為美元金額，$c$ 為整數美分：

$$c=100d.$$

例如 $d=12.50$ 時，$c=1250$。這個式子沒有定義超過兩位小數時的取整；取整方式與發生時點是額外的業務規則。使用 `Decimal`從字串建立數字，不先經過二進位 `float`再轉回來。

## 轉型仍然要查結果

來源文字可能含空格、千分位、非法字元或超出範圍。失敗資料應進入明確錯誤或隔離路徑，而不是變成零。零代表已知金額為零，空值或失敗則代表資訊尚未成立，兩者對分析的意義不同。

## 專案中的實作

節錄 `examples/contracts.py` 的 `cents`。請以完整下載包執行，共用匯入與資料契約不可省略。

```python
def cents(value):
    number=Decimal(value)
    if not number.is_finite() or number<0 or number.as_tuple().exponent < -2:raise ValueError('Finite nonnegative amount with at most two decimals required')
    return int(number*100)
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/03.svg" target="_blank" rel="noopener" aria-label="放大數值型別與金額的精確表示圖解"><img src="assets/figures/03.svg" alt="數值型別與金額的精確表示：逐列比較NULL、零和空字串，辨認一般比較、空值判定和COUNT如何處理它們。" loading="lazy"></a><figcaption>原創中文圖解；資料皆為教學合成，箭頭與尺度依圖例解讀。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「數值型別與金額的精確表示」讀圖：逐列比較NULL、零和空字串，辨認一般比較、空值判定和COUNT如何處理它們。請用圖回答：把無法解析的金額改成0，可以讓後續SUM更穩定嗎？</p></div>

## 自我檢查與解析

**題目：**把無法解析的金額改成0，可以讓後續SUM更穩定嗎？

<details><summary>展開解析</summary><p>會掩蓋資料品質問題。零是合法金額，解析失敗應保留錯誤或隔離，不可用零冒充已知數值。</p></details>

## 離線實作

在完整程式包的 `examples` 目錄執行 `python lab03.py`，或用 `python run_lab.py --list` 對照實驗目標。程式使用真實DuckDB與合成資料；首次安裝套件後不連網路。SQL、資料契約與輸出都可從原檔核對。

<!-- example:lab03.py -->

## 官方來源

[本單元對應文件](https://www.postgresql.org/docs/19/datatype-numeric.html)（查核：2026-11-27）。DuckDB主線為2.0.1，PostgreSQL伺服器主線為19.0；兩者的能力與語法分別標示，不把概念模擬稱為服務實測。
