# 推論介面：欄位名稱、機率與決策的一致性

把raw資料轉成固定契約，讓相同模型在不同入口有相同行為。

## 先定義輸入

完整專題接受records list，每筆恰含tenure_months、weekly_usage、support_tickets、plan。numeric允許有限數字或null，category允許非空字串或null；不接受Inf、數字字串與bool混作數值。這是教學的明確型態契約，真實服務可另定轉換政策並測試。

## 欄位順序與shape

dict送入的鍵順序可能不同，records_to_array依SCHEMA固定取值，因此反轉鍵插入順序仍相同。若直接list(record.values())，就可能silent feature swap。即使shape都是[N,4]，模型也不知道第一欄其實換成usage。保存名稱並在邊界驗證，才可避免。

## 缺失與新類別

null→NaN後，沿用train imputer與encoder；new_plan走handle_unknown政策。能產生預測不代表此群已有良好評估，需要監控未知比例與score。若欄位本身有域值限制，例如年資非負，真實schema還應補驗證，本課基本函式沒有聲稱涵蓋所有業務規則。

## 輸出包含什麼

scores是positive_class=1對應欄的機率，labels由保存threshold決定。回傳threshold便於追蹤，正式服務另附model_version、schema_version、錯誤狀態與label名稱。不能假設predict_proba[:,1]永遠是你想要的正例；先看classes_。

```python
from course_core import experiment,predict_records,sample_records
artifact=experiment()['artifact']
print(predict_records(artifact,sample_records()))
```

在examples資料夾執行。它是本機推論，不是公開API服務；HTTP認證、流量、觀測與發布屬交付層，要在之後工程課整合。

## 練習與解答

給同樣值但不同dict鍵順序，預測應相同；新增未知key，本課拒絕。若想允許extra metadata，需明確分欄並測試，不能直接把它塞進features。空list的政策也要明確，本課拒絕以避免含糊空推論。介面品質不只是程式沒有Exception，也包括輸出含義一致。

## 官方來源與延伸閱讀

- [Pipeline推論](https://scikit-learn.org/1.9/modules/compose.html)
- [分類機率與classes](https://scikit-learn.org/1.9/modules/generated/sklearn.linear_model.LogisticRegression.html)
