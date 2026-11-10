# 血糖單位：mg/dL與mmol/L

從葡萄糖換算開始，保留分析物、樣本與精度。

## 兩種表達

血糖常用mg/dL或mmol/L，臨床教學可用18作近似係數：126mg/dL約7.0mmol/L。這不是所有檢驗共用的換算，膽固醇與TG係數不同，胰島素單位更不能直接套。

$$
glucose_{mmol/L}\approx glucose_{mg/dL}/18
$$

## 樣本與時間

空腹、OGTT兩小時與隨機血糖回答不同問題，家用指尖、連續監測間質液和實驗室血漿也不等同。數值換單位後，原始樣本和協定不能丟掉。

## 修整與界線

報告小數位可能經修整，換算後不保證所有門檻都剛好一樣；先保留原值、單位和方法，不因小數差就判生理狀態突然改變。診斷還需適用條件與確認。

## 實驗與限制

範例來回換算並驗證單位，沒有輸出紅綠燈或個人診斷。若只提供126而沒有單位、空腹與方法，下一步是補資訊，不是直接把它叫糖尿病。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 10_glucose_units.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:10_glucose_units.py -->

## 練習與解答

**先自己判斷：** 126換成約7.0後，是否可以刪掉空腹和樣本資料？

<details><summary>展開驗算與理由</summary>

不可以。單位換算只改表達，診斷適用仍依原始協定、樣本、症狀及確認條件。

</details>

## 官方來源與研究

- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [NGSP：HbA1c的IFCC主方程式](https://ngsp.org/ifccngsp.asp)
- [國健署糖尿病資料入口](https://www.hpa.gov.tw/359/s)
- [NIDDK：胰島素阻抗與糖尿病前期](https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
