# 速查、名詞與版本：回來查找你的下一步

整理本課資料契約、演算法與驗證範圍，讓教材可以持續使用。

## 版本與實測基準

2026-10-30查核最新穩定框架scikit-learn1.9.1；Python3.11.6、NumPy2.4.6、SciPy1.17.1及鎖定依賴實測。數值依賴是Python3.11相容組合；較新的NumPy／SciPy需要Python3.12以上，未冒稱本環境使用所有套件的全球最新版。每次更新重新查官方release與套件索引，再安裝測試。

本課60章、30個真實sklearn離線入口、45項數值與整合測試。測試包含不同cwd、阻擋socket連線、前處理隔離、group/time邊界、校準、threshold CV、PCA／分群／異常與保存後一致性。資料全部合成或自寫短句，分數不代表真實任務性能。

## API與資料契約速查

| 名詞 | 本課含義 |
| --- | --- |
| fit | 只在允許的train資料學狀態 |
| transform | 用已學規則轉換，不重新fit |
| predict | 類別／數值／指定模型的輸出 |
| predict_proba | 依classes_排列機率欄 |
| decision_function | 分數，不普遍等於機率 |
| Pipeline | 前處理與模型一起clone／fit／保存 |
| CV test_score | 該折驗證分數，不自動是final test |
| threshold | 分數到決策的規則，也需選擇邊界 |
| calibration | 機率與觀察頻率的一致性 |
| leakage | 未見資訊滲入訓練／選擇 |

## 演算法參數方向

Ridge／Lasso alpha大通常限制強；Logistic／SVM C大通常限制弱；kNN k大更平滑；tree depth大更有容量、leaf最小樣本大更受限；forest樹數增加降低某些集成波動；boost learning_rate與步數共同決定預算；KMeans群數不能只靠inertia最小化選。

## 已執行與延伸

30個編號入口與測試在CPU執行，另外16個內嵌Python片段也已離線執行，包括t-SNE、增量與回歸／分群專題。額外模型／runtime仍需各自驗證。未安裝外部Boosting、UMAP、SHAP、ONNX服務；沒有聲稱GPU或大規模分散式性能。網頁互動是JavaScript數值演示，Python才使用scikit-learn。

## 每次開新專案先問

答案如何定義與何時可得？部署時能取得哪些特徵？樣本是否獨立？哪個split符合未來？baseline與成本是什麼？所有fit是否在train內？選模／校準／threshold看過哪些資料？模型產物與schema能否重現？分數不確定性與未驗證分布有哪些？

## 練習與下一步

不看原稿，向自己解釋fit與transform、AP與accuracy、校準與threshold、模型預測與因果的差異。再以一個小專題實作全部資料邊界並保存產物。數學、統計、深度學習與工程各有獨立課程；以你下一個問題選擇深化方向，保留這裡的驗證習慣。

## 官方來源與延伸閱讀

- [1.9正式文件](https://scikit-learn.org/1.9/user_guide.html)
- [1.9.1正式發布](https://github.com/scikit-learn/scikit-learn/releases/tag/1.9.1)
- [完整API](https://scikit-learn.org/1.9/api/index.html)
- [更新規範背景](https://scikit-learn.org/1.9/whats_new/v1.9.html)
