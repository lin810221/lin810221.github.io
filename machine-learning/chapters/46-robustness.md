# 資料品質與穩健性：離群值、雜訊與敏感性實驗

用可控制擾動檢查模型，而不是只靠一份乾淨test。

## 品質檢查與模型韌性

格式正確不代表內容合理：單位錯1000倍、時間錯位、欄位互換、缺失飆升都可能仍是finite數字。邊界驗證先保護schema與明確域值；穩健性實驗再看合理擾動下輸出是否可接受。兩者不能互相取代。

## 離群值不一定要刪

可能是輸入錯誤，也可能真實稀有案例。對所有高誤差點一律刪除，會讓報告偏好容易樣本。可比較RobustScaler、穩健回歸或clip政策，但每項規則需由train／validation決定並保存。依test錯誤特別刪資料會污染評估。

## 擾動矩陣

設幾種事先定義情境：缺失率5%→20%、特徵增加小量測noise、新category、某欄改單位、某來源比例改變。前三者可能是真實可接受輸入，單位／schema錯誤應直接拒絕。記錄效能、警示率、confidence與失敗模式，而不只看程式有沒有crash。

```text
情境               期望行為
少量數值null       沿用train imputer並回報缺失監控
新plan字串         走unknown政策，記錄比例
數值為Inf／字串    在邊界明確拒絕
欄位名稱錯誤       拒絕，避免silent feature swap
```

## 標籤雜訊與分布偏差

少量錯標可讓某些高容量模型追逐noise。修標需要一致規則與獨立審查，不能只改模型錯的樣本。蒐集偏差與未來分布不同則不一定能靠更多同源資料解決，需要更符合部署的樣本及評估設計。

## 練習與解答

將同一個raw record的dict鍵順序反轉，預測應相同，因為按schema取值；把數值改字串'5'，本課拒絕，避免含糊型態轉換。解答：明確介面比自動猜測更容易維護。加入一個額外key也拒絕，是否寬鬆接受應由服務契約決定，而不是任意忽略。

## 官方來源與延伸閱讀

- [Preprocessing](https://scikit-learn.org/1.9/modules/preprocessing.html)
- [Outlier detection](https://scikit-learn.org/1.9/modules/outlier_detection.html)
- [常見資料問題](https://scikit-learn.org/1.9/common_pitfalls.html)
