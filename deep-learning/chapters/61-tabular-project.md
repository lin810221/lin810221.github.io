# 專題一：非線性表格分類的完整實驗

從已知生成規則到模型選擇，讀懂資料、指標與每次權重更新的責任。

## 任務不是一張模糊的表格

本專題生成480筆、每筆4個常態特徵，標籤依x1x2+.25x3−.1x4>0。交乘讓它含非線性交互，MLP可學這種表示。因為規則公開，直接計算規則有完美答案；這是教學用oracle，現實未知標籤通常沒有可直接查詢的規則。

## 切分與前處理

固定生成器及打散，分成288筆train、96筆validation、96筆test。均值及母體標準差只用train估，再轉換其他集合。保留原始schema與統計，避免交付時用三筆新資料重算scaler，使相同輸入的結果依同批其他資料而變。

## 模型與訓練協定

4→24→24→2的ReLU MLP共有770個參數。batch24、AdamW lr=.02、weight_decay=.001，訓練24epochs。每epoch以validation loss挑最佳快照，再載回最佳state；保存快照使用detach／clone，避免被後續更新覆寫。accuracy為輔助指標，主選擇標準在訓練前就寫好。

$$
\hat e=\arg\min_{e\in\{1,\ldots,24\}}L_{\rm val}(\theta_e),
\qquad m_{\rm test}=m(\theta_{\hat e};D_{\rm test})
$$

## 看懂執行結果

第41例真的訓練、評估並回報起始與最佳validation，以及最後test。不要逐epoch查看test或用test選寬度。若改loss為sum，或最後batch大小不同，樣本加權的epoch平均也需一起檢查；現有train與evaluate都依實際樣本數統計。

## 可獨立完成的延伸

先建不含交互項的linear baseline，再加入已知x1x2人工特徵，與MLP比較。這可以辨認收益來自函數表示還是其他訓練條件。保持split與評估一致；若你看過test後又調整，換新的保留集作最終驗收。第42例再把整套前處理與模型包成推論artifact。

## 練習與解答

validation最佳在第17epoch，但第24epoch train loss最低，交付哪一份？依本協定交付第17epoch快照。為何不把test最高的epoch交付？因為這會讓test參與選擇，原本的最終估計就失去保留意義。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/41_tabular_project.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:41_tabular_project.py -->

## 原始論文與官方來源

- [Dataset與DataLoader](https://docs.pytorch.org/docs/2.15/data.html)
- [模組狀態保存](https://docs.pytorch.org/docs/2.15/notes/modules.html)
- [AdamW參數](https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html)
