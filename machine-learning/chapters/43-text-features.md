# 文字特徵工程：TF-IDF、n-gram與分類管線

將文字向量化與模型包在同一訓練邊界，處理中英文差異。

## 先把文字變成可運算表示

CountVectorizer以詞／字n-gram建立詞表與計數；TfidfVectorizer另依文件頻率調整。詞表與IDF是fit學到的狀態，必須只看train。預測新詞可能被忽略，維度沿用原詞表，不重新fit test語料。

## 中文與英文的基本差異

英文預設token規則常依空白／字元模式切詞；中文未斷詞時可能形成不合預期長片段。可以明確使用斷詞器並版本化，或char n-gram作離線基準。選擇n範圍、min_df、max_df與max_features影響成本與訊號，需驗證。

```python
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
model=make_pipeline(TfidfVectorizer(analyzer='char',ngram_range=(2,4)),
                    LogisticRegression(l1_ratio=0,max_iter=1000))
texts=['程式資料分析','模型程式工具','球隊比賽進球','足球球員比賽']
model.fit(texts,[0,0,1,1])
print(model.predict(['資料程式工具','足球比賽進球']))
```

這是四句自製示例，不是中文分類成績；第19章另有完整英文NB入口。

## 稀疏矩陣與線性基準

詞表很大但每句只少數詞，sparse保存非零元素。不要隨手toarray把幾十萬欄展開；也避免會中心化的scaler。線性Logistic、LinearSVC、NB常是強且便宜的起點；kernel或森林未必適合這種高維稀疏表示。

## 文字資料的洩漏

同一文件切塊、轉貼、模板與重複文章跨split，會讓val過高；以來源／文件group或時間切分。主題label若出現在檔名或頁尾，也可能被模型當捷徑。文字清理規則先用train設計，不看到test錯例就一直增加特定詞規則。

## 練習與解答

語意相近但用詞不同，TF-IDF可能失敗；解答：比較更適當字／詞特徵或Embedding，仍保持同樣切分與指標。使用預訓練Embedding時保存模型與前處理版本，不能因為向量維度相同就混用。RAG則還要處理檢索、引用與生成，與這裡的分類不同。

## 官方來源與延伸閱讀

- [Text feature extraction](https://scikit-learn.org/1.9/modules/feature_extraction.html#text-feature-extraction)
- [文字分類官方範例](https://scikit-learn.org/1.9/auto_examples/text/plot_document_classification_20newsgroups.html)
