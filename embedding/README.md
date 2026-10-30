# Embedding 與表示學習完整教學

從 [index.html](index.html) 開始，或從學習首頁選 Embedding。48 章、8 個單元，保留深色閱讀器、本機 LaTeX、搜尋、獨立進度與筆記。

涵蓋向量數學、token 與句表示、共現、Word2Vec、GloVe、fastText、BERT、SBERT、對比學習、模型與 API、搜尋、分類、聚類、去重、推薦、離群、評估、投影、量化、Matryoshka、多模態、微調、蒸餾、隱私與部署。

四個互動實驗室均在瀏覽器本機計算，不呼叫模型：

1. 角度、長度與 cosine／dot／L2 排名。
2. 正負樣本分數、溫度與 InfoNCE。
3. 門檻、混淆矩陣與 Precision／Recall／F1。
4. 三維距離與二維投影，觀察近鄰失真。

座標、標註分數與機率計算均明確標示為教學數據。20 個 Python 入口預設離線；OpenAI／Gemini 需 `--live`，本機模型需選擇已下載路徑，新下載須明確指定模型與 revision。詳見 [範例說明](examples/README.md)。

```powershell
python tools/build.py embedding
python tools/validate.py
python -m unittest discover -s embedding/examples -p test_examples.py -v
```

可編輯原稿在 `chapters/*.md`，順序與摘要在 `course.json`。建置產生 `assets/course-data.js` 與 `examples.zip`，推送後沿用既有 GitHub Actions 驗證與發布流程。
