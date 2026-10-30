# 機器學習完整教學：可執行範例

依 **2026-10-30 查核的官方最新穩定版 scikit-learn 1.9.1** 製作。[正式發布](https://github.com/scikit-learn/scikit-learn/releases/tag/1.9.1)、[版本紀錄](https://scikit-learn.org/1.9/whats_new/v1.9.html)。30 個編號入口均使用真正 scikit-learn，已在 Python 3.11.6、NumPy 2.4.6、SciPy 1.17.1 執行 45 項測試。

數值依賴是 Python 3.11 的相容鎖版組合；查核時更高版本 NumPy 2.5.4／SciPy 1.18.1 要求 Python >=3.12，沒有宣稱本環境的每個依賴都是全球最新。主框架仍採最新版 1.9.1。更新時重新查核並驗證，不讓安裝環境無條件升到未測組合。

## 安裝與執行

Windows，從網站專案根目錄：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r machine-learning/examples/requirements.txt
.\.venv\Scripts\python.exe machine-learning/examples/30_capstone.py
.\.venv\Scripts\python.exe -m unittest discover -s machine-learning/examples -p test_examples.py -v
```

macOS／Linux 解譯器路徑改 `.venv/bin/python`。若已進入 ZIP 解壓的 `examples` 資料夾，需求檔用 `requirements.txt`、入口用 `30_capstone.py`、測試用 `python -m unittest discover -s . -p test_examples.py -v`。

保留整個資料夾，包含 `course_core.py` 與 `data/prediction_records.json`。資料路徑依程式位置解析，可從其他 cwd 啟動。預設 CPU、合成數值與原創短文，沒有外部下載、API、帳號或 GPU 需求。

## 30 個入口

| 檔案 | 實作與觀察 |
| --- | --- |
| 01_first_pipeline.py | Dummy 與縮放+Logistic 完整固定模型流程 |
| 02_split.py | 分層、GroupKFold、TimeSeriesSplit 與 gap |
| 03_preprocessing.py | train-only median／scale，val 不改統計 |
| 04_categories.py | 固定 One-Hot 詞表與新類別 |
| 05_linear_regression.py | 學 y=3x+0.5；可知答案 sanity check |
| 06_regularization.py | Ridge／Lasso 係數與固定設定比較 |
| 07_logistic.py | 現行 C／l1_ratio、classes 與 predict_proba |
| 08_knn.py | 縮放距離、鄰居索引與分類 |
| 09_naive_bayes.py | 自寫英文短句 TF-IDF+MultinomialNB |
| 10_svm.py | RBF SVM、support vectors、decision score AUC |
| 11_tree.py | 決策樹實際第一分裂與複雜度 |
| 12_random_forest.py | 固定森林與 impurity importance 的含義 |
| 13_boosting.py | 真實 HistGradientBoosting 與 missing |
| 14_compare.py | 共用 train CV folds 比較三個候選 |
| 15_classification_metrics.py | 四筆手工分數的混淆矩陣與門檻 |
| 16_regression_metrics.py | 手算 MAE／RMSE 與負 R² |
| 17_cross_validation.py | 每折獨立 scaler 與多指標 CV |
| 18_search.py | train 內 GridSearchCV，不碰 final test |
| 19_nested_cv.py | 真正外三折、內三折選模評估 |
| 20_imbalance.py | class weight 與事先指定門檻示範 |
| 21_calibration.py | 真正 CalibratedClassifierCV 與 LinearSVC |
| 22_threshold.py | 真正 TunedThresholdClassifierCV |
| 23_learning_curve.py | train 內樣本量與 score 曲線數值 |
| 24_kmeans.py | inertia、中心、silhouette 與合成真值 ARI |
| 25_density.py | DBSCAN 與孤立點 -1 |
| 26_pca.py | 投影、explained variance 與重建 |
| 27_anomaly.py | IsolationForest 與不同查詢點 |
| 28_inspection.py | heldout permutation importance |
| 29_persistence.py | 完整產物真正保存／載入與預測比對 |
| 30_capstone.py | 混合欄位 → train CV → val 成本門檻 → test → 交付 |

範例的 holdout 分數是教學示範，不要依它們反覆調參。第 14、18、23 例明確只使用 train；第 19 例評估整套選模程序。原創短句沒有足夠資料報文字準確率；所有合成分數沒有真實任務性能含義。

## 完整專題

400 筆合成混合資料，固定 240 train／80 validation／80 test。三個 numeric 欄 median+missing indicator+scale，category 補 MISSING+One-Hot。整條 Pipeline 在 train 三折搜尋 Logistic C，以 average precision 選擇；在獨立 validation 以 `5×FN + 1×FP` 選 threshold；方案固定後才計算 final test。

推論輸入有明確 schema：`tenure_months`、`weekly_usage`、`support_tickets`、`plan`。按名稱取值，不依 dict 插入順序；數值僅接受有限 number／null；新 plan 沿用 unknown 政策。這是型態契約，真實專案還需自己的域值、單位、標籤時間與資料權限規則。

預設產物存在 temporary directory 並清除。需要保留時指定新的檔名：

```powershell
python machine-learning/examples/30_capstone.py --output runs/ml-001/model.joblib
```

已有檔案拒絕覆蓋。產物包含完整前處理、模型、classes／positive class、threshold、schema、選參資訊與版本。Joblib 載入可執行程式，只讀可信來源；載入後的版本檢查是相容性檢查，不是安全沙盒。

## 測試與實際範圍

45 項測試驗證手算指標、資料隔離、group／time、每折 scaler、unknown、schema、Logistic 現行介面、校準、門檻 CV、KMeans 標籤置換、PCA、異常、重要性與產物往返。全部 30 入口在不同 cwd 執行，測試攔截 socket 連線，確保預設離線。

網站的五個互動實驗用 JavaScript 計算，沒有在瀏覽器執行 scikit-learn。章節的 16 個內嵌 Python 片段也已離線執行，包括 t-SNE、增量與回歸／分群專題；不把它們計入 30 入口或額外套件性能承諾。外部 Boosting、UMAP、SHAP、ONNX runtime、GPU 與分散式未安裝／驗證。
