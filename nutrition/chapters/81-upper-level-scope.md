# 上限的來源範圍：不是把所有數字直接相加

以folic acid示例做來源篩選，保留形式、單位與地區。

## 上限需要完整名稱

UL的適用年齡、化學形式、來源和地區不可省略。某些值針對總攝取，某些只針對補充、藥物或強化來源；同樣標μg也不保證可直接加總。

## 葉酸來源實驗

假設天然食物葉酸400μg、強化folic acid200μg、補充folic acid400μg。以美國19歲以上folic acid UL範圍，相關已知分子是600μg folic acid，不是把天然量或DFE全部塞進同一分子。

## 缺值的傳播

若某一相關補充品folic acid量未知，完整相關總量也未知；天然食物不在此限定範圍，該欄未知不一定污染這個特定小計。程式依source_type篩選，但呼叫者仍需保證形式與單位相同。

## 不輸出安全判決

算出相對某UL的比例，只表示算術與範圍；不涵蓋藥物、疾病、其他不良影響及資料誤差。不能把低於100%當所有人安全，也不能把UL當希望達到的攝取目標。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 41_ul_source_scope.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:41_ul_source_scope.py -->

## 練習與解答

**請先判斷：** 天然食物葉酸未知，是否一定使上述限定folic acid小計未知？

<details><summary>展開計算與理由</summary>

不一定。天然來源不屬該UL範圍；但相關強化或補充來源未知就需標完整限定總量未知。前提是形式、單位和來源分類正確。

</details>

## 官方參考與跨課閱讀

- [NIH ODS：葉酸與DFE](https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/)
- [NIH ODS：營養參考值的不同用途](https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx)
- [NIH ODS：補充品須知](https://ods.od.nih.gov/factsheets/WYNTK-Consumer/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
