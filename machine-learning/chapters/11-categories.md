# 類別編碼：One-Hot、未知值與高基數

區分類別代碼與數值大小，處理訓練沒見過的新類別。

## 名稱沒有天然距離

basic、plus、team是名目類別，若編成0、1、2再讓線性或距離模型使用，等於引入大小與等距假設。One-Hot每類一個欄位，將這個假設拿掉。真正有序的等級可以考慮OrdinalEncoder，但需明確定義順序與未知值政策。

## fit詞表，再transform新資料

只在train fit encoder。範例看過basic與team，輸出兩欄；new_plan透過handle_unknown='ignore'得到全0，不擴張欄位，也不假裝與新模型相同。這個政策讓流程可執行，但模型對未知類別沒有學到專屬效果，需要監控出現率。

## sparse與欄位數

OneHotEncoder使用sparse_output參數；本課小例設False便於觀察。高基數ID可能產生巨大特徵空間，先判斷是否應排除、合併稀有類別、用hash或其他表示。min_frequency／max_categories可限制類別細分，仍需在train fit並檢查輸出名稱。

## 參照類別與線性模型

全部one-hot加intercept會有線性依賴；特定無正則回歸推論可能選擇drop一欄。正則化模型及預測任務也要看完整設計，不把drop='first'當所有問題的固定答案。若unknown與被drop的參照類別都映成全0，解讀時需格外清楚。

## Target encoding的邊界

以類別的平均target當特徵時，最容易直接洩漏答案。應使用訓練內cross-fitting與平滑，外層CV也要保持邊界。即使某套件有TargetEncoder，也要讀fit_transform與transform的差異，不自行對全部y求均值後做CV。

## 練習與解答

train看到A、B，test新增C，應否在test重新fit三欄？解答：否，維度與含義會不同；沿用encoder並執行預先定義unknown政策。若一欄幾乎每筆唯一，one-hot高train分數可能只是記憶ID，先查它在部署的新樣本是否有可泛化意義。

## 完整可執行範例

從專案根目錄執行 `python machine-learning/examples/04_categories.py`。保留完整範例包，內含共用實作、固定資料、需求檔與測試。

<!-- example:04_categories.py -->

## 官方來源與延伸閱讀

- [Categorical preprocessing](https://scikit-learn.org/1.9/modules/preprocessing.html#encoding-categorical-features)
- [ColumnTransformer](https://scikit-learn.org/1.9/modules/compose.html)
