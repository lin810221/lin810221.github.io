# 準確率之外的分類評估

<figure class="cv-figure"><a href="assets/figures/10-imbalance-threshold.svg" target="_blank" rel="noopener"><img src="assets/figures/10-imbalance-threshold.svg" alt="兩種樣本分數分布與可移動閾值，旁側指出提高閾值會減少陽性預測與Recall，Precision不保證單調。" loading="lazy"></a><figcaption>類別不平衡與決策閾值。訓練的取樣策略、分數校準與最後閾值是不同的控制位置。 點選圖像可放大；原創概念圖，非模型實測輸出。</figcaption></figure>

<div class="cv-task"><strong>讀圖任務</strong><p>說出模型在此階段收到什麼、輸出什麼；用本單元算例核對shape、狀態或評估分母。 本頁主題：準確率之外的分類評估。</p></div>

分類評估要先決定樣本是什麼、類別代表什麼，以及哪種錯誤代價較高，再計算分數。

## 混淆矩陣的方向

本課採真實類別為列、預測類別為欄。二類矩陣[[4,0],[1,1]]表示四筆真0全對；兩筆真1中漏掉一筆。accuracy為 $\frac{5}{6}$ ；類別1的precision為1、recall為 $\frac{1}{2}$ 。若把矩陣轉置，precision與recall的分母會交換，所以報告必須標軸。

$$
\mathrm{precision}=\frac{TP}{TP+FP},\quad
\mathrm{recall}=\frac{TP}{TP+FN},\quad
F_1=\frac{2TP}{2TP+FP+FN}
$$

沒有預測陽性時precision的分母為0，應明列未定義或約定的zero_division政策，不能悄悄把它當成完美。類別根本沒有真實樣本時，召回率也缺乏可評估分母。

## 平均方式改變意義

macro先算各類指標再平均，重視每類；weighted依支持樣本數加權；micro合併TP／FP／FN後計算。單標籤多類別分類的micro precision、recall及F1會等於accuracy，但macro不一定。balanced accuracy平均各類召回率，對不平衡資料較能揭露少數類別失敗。

多標籤任務則同一張影像可同時有多個標籤，應用每類sigmoid與多個二元目標，不能用只選一類的softmax解決。評估時還要區分整張完全正確率與每標籤表現。

## 跑一個小矩陣

<!-- example:10_classification_metrics.py -->

先用手算確認矩陣，再看程式輸出。若想改成瑕疵檢出，把class1定義為瑕疵，保存定義與門檻。ROC-AUC衡量排序，PR曲線在罕見陽性時常更具實務意義；兩者都不能直接告訴你部署門檻下會誤報幾件。

## 報告的最小內容

列出資料期間、獨立群組數、各類樣本量、前處理、門檻選定方式、每類precision／recall及錯例。若同一病人或工件有多張影像，信賴區間也應考慮群組，而不是把所有影格當獨立樣本重抽。

## 練習與解析

真0有90張全對，真1有10張全錯。accuracy90%，balanced accuracy50%，macro recall50%。這不是指標衝突，而是平均問題不同。若只看accuracy，會忽略所有瑕疵；若只看macro，仍不知道實際誤報量，兩者應配合支持數與成本說明。

門檻只能在開發資料上選。看了測試錯例再修改門檻，下一次就需要新的保留評估資料。

## 官方與原始資料

[scikit-learn分類評估定義](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)；[混淆矩陣](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)

來源查核：2026-11-23。範例的合成影像結果只用於驗證本單元方法，不能當作自然影像的效能基準。

## 可執行範例與驗收

下載[完整範例包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 10_classification_metrics.py`。共用實作保存在`vision_core.py`，需保留整包。預設不下載權重、不呼叫API；大型模型或外部資料的條件另在課文標示。先預測輸出形狀及數值範圍，再核對實際結果；結果的適用範圍依範例說明。

