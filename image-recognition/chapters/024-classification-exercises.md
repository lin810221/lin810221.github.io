# 分類實作練習與完整解析

<figure class="cv-figure"><a href="assets/figures/07-convolution.svg" target="_blank" rel="noopener"><img src="assets/figures/07-convolution.svg" alt="左側三乘三輸入與邊緣kernel逐項相乘得到負二，右側三乘三視窗在五乘五影像上滑動得到三乘三輸出。" loading="lazy"></a><figcaption>卷積層：局部運算與參數共享。用手算核對一個位置，才能區分stride、padding、通道數與模型參數。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>說出模型在此階段收到什麼、輸出什麼；用本單元算例核對shape、狀態或評估分母。 本頁主題：分類實作練習與完整解析。</p></div>

本章練習把shape、訓練與評估連成一個完整決策，先自行計算，再核對解答。

## 題目：追蹤張量與參數

輸入[4,3,32,32]， `Conv2d(3,16,3,stride=2,padding=1)` ，接ReLU及AdaptiveAvgPool2d(1)，最後Linear(16,5)。寫出每步shape與卷積參數量，說明為何不需要在每次換batch大小時重建Linear。

解析：卷積為[4,16,16,16]；ReLU不改shape；池化為[4,16,1,1]，flatten(1)後[4,16]；輸出[4,5]。卷積參數 $16\times (3\times 3\times 3+1)=448$ 。batch軸不是Linear輸入特徵軸，因此最後一批只剩1張仍可推論，但訓練時其他層如BatchNorm可能有額外限制。

## 題目：損失函數契約

五類單標籤問題，輸出[8,5]，標籤寫成[8,1]的float，能直接送入CrossEntropyLoss嗎？

解析：本課整數類別模式要用[8]、long且值為0到4；不把標籤除255，也不必手動one-hot。另一種機率目標模式是不同用途，不能用形狀湊合來替代。損失輸入維度合法，也仍需檢查標籤語意。

## 題目：比較兩個模型

模型A accuracy95%，少數類recall20%；模型B accuracy92%，少數類recall80%。應選哪個？

解析：不能只憑這兩個數字決定。需要各類樣本量、誤報率、漏檢成本與作業容量。若少數類是高代價瑕疵，B可能較適合，但仍需看每小時誤報件數是否可處理。門檻要用驗證資料調整，不在測試集反覆搜尋。

## 實作任務：保留可以回看的證據

執行09_train_classifier.py及10_classification_metrics.py，保存環境版號、資料seed、loss與每類指標。再用20_shift_slices.py檢查反轉亮度後的表現。三份輸出應分別標明訓練驗證、手算示例及刻意分布改變，不能混成一個平均分數。

驗收至少包含：程式能從乾淨環境啟動；輸出沒有NaN；不同split沒有重複ID；分類頭輸出順序與標籤表一致；錯例可回到原圖。若有失敗，寫出復現命令及最小輸入，而不是只寫「模型效果不好」。

## 進一步推理

為什麼小batch過擬合成功後，還需要保留集？因為擬合能力和泛化是不同問題。為什麼換另一個seed還有用？它能觀察部分初始化與抽樣變動，但不能替代來自其他工件、日期或設備的獨立資料。

完成本章後，應能解釋一個logit從影像、卷積、池化到分類頭的路徑，以及它如何轉成評估表上的一個TP或FP。下一章才加入預訓練與遷移，而不是跳過資料契約。

## 官方與原始資料

[PyTorch分類入門](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)；[分類報告定義](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。
