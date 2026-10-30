# 完整分類專題：混合欄位、CV、門檻與最終測試

沿著一條真實執行的離線流程，核對每個資料角色與產物。

## 專題驗收條件

400筆合成資料，3個數值欄與1個類別欄，含missing。固定240train、80val、80test。所有前處理只fit train；train內3折搜尋C；用獨立val分數選5FN+FP成本門檻；模型與門檻固定後才評估test。最後實際保存、載入，對raw records推論。

## 如何執行

```powershell
python machine-learning/examples/30_capstone.py
python machine-learning/examples/30_capstone.py --output runs/ml-001/model.joblib
```

未指定output使用temporary directory並清除；指定新檔名才永久保存。已有檔案會拒絕覆蓋。此課程沒有連外服務、模型下載或真實客戶資料，不需API Key。

## 從入口追進核心

Config.validate→make_mixed_data→split_indices→mixed_pipeline→GridSearchCV；接著probability查classes→select_threshold→binary_metrics；之後save_artifact／load_artifact→predict_records。共用模組完整附在下載包，不藏在外部API。讀者可追到每個fit究竟看哪些索引。

## 輸出怎麼讀

training_selection含train CV AP與C，以及validation成本／threshold；final_test是固定方案一次評估。這兩份score來自不同資料與用途，不要求小數相同。data明確標示synthetic；即使test較高，也不能外推到真實事件。程式沒有在test挑threshold。

## 轉成自己的資料

替換資料載入，先定raw schema、label時間、group／time切分與缺失政策；保留原數值測試作對照。C搜尋空間與成本依任務重設，在開test前固定。若重fit train+val，原validation已參與模型weights，threshold與校準也需重新設計，不直接沿用舊分數而宣稱同樣保證。

## 練習與解答

改變FN成本，應只在val重新選決策並記錄；不要拿同一test反覆評比後挑最好。把record欄位順序反轉應不變，數值改Inf應拒絕，new_plan應依unknown政策可推論。解答：這些是可測工程契約，讓「跑出模型」進一步成為可重現流程。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/30_capstone.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:30_capstone.py -->

## 官方來源與延伸閱讀

- [Pipeline](https://scikit-learn.org/1.9/modules/compose.html)
- [Threshold tuning](https://scikit-learn.org/1.9/modules/classification_threshold.html)
- [Model persistence](https://scikit-learn.org/1.9/model_persistence.html)
