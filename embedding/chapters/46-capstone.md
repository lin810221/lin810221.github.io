## 專案目標

建立課程筆記向量工作台：可檢查表示來源、搜尋課程、比較分類和聚類、觀察訓練、評估指標與壓縮誤差。它是一組透明可重現工具，預設不依賴網路與外部模型。

資料由自行撰寫的九筆課程描述組成，不包含真實私人資料。字詞方法與手工座標都有標記，真正預訓練模型放在選配入口，不會把概念示範誤標成語意能力。

## 專案結構

```text
examples/
  embedding_core.py   數學、TF–IDF、微型訓練、任務與壓縮
  providers.py        OpenAI／Gemini 選配 adapter
  01_...20_*.py       分階段入口
  data/courses.json   自行撰寫的短課程資料
  test_examples.py    數值、邊界、版本與離線驗證
```

## 完整搜尋入口

<!-- example:20_workbench.py -->

```powershell
python 20_workbench.py "向量 相似度 cosine"
python 20_workbench.py "SQL 資料庫" --k 2
python 20_workbench.py "qwertyunseentoken"
python 13_evaluation.py
python -m unittest discover -s . -p test_examples.py -v
```

從網站原始碼根目錄使用 `python embedding/examples/20_workbench.py`。未知字詞 query 沒有有效表示時回空候選，不用任意零分文件補滿 k。

## 驗收哪些行為

向量算式符合手算；TF–IDF query 不改 vocabulary；微型訓練有真梯度且可重現；PAD mask 正確；PCA 中心化和方向一致；int8 重建誤差在界限內；不同 manifest 不混讀；全部預設入口在阻斷網路環境執行。

這些測試驗證程式邏輯，不是通用模型品質保證。真正 encoder 接入後，新增你的 query、標註與分組評估，保留同一套 ID、版本和結果格式。

## 替換成真模型

將 `Tfidf.transform()` 對應位置換成相容 encoder 的 query/document 呼叫，文件預先編碼。保存設定指紋和維度，接回相同 exact search。再考慮 ANN、Hybrid 與 RAG，不必一次換全部元件。

第 17、18 份需 `--live`，第 19 份使用已準備模型或明確下載選項。所有範例說明與完整模組一起放在 ZIP，可獨立離線研究。[Python unittest](https://docs.python.org/3/library/unittest.html)

## 按元件替換而非重寫全部

先保留 exact search 和結果格式，只換 encoder；再固定 encoder 比較 ANN；最後再加 Hybrid 或重排。每步保存前一版結果，才能知道改動造成的收益和損失。

如果同時改資料、模型、索引和門檻，即使結果變好也很難歸因。工作台的價值正是讓這些元件有明確邊界，從小型透明程式走向可維護系統。

## 練習與參考答案

**題目：**工作台換真模型後，第一個比較是什麼？

**參考答案：**固定資料和 query，確認維度、recipe 與原文映射，再用同義、代碼、無關與跨語題比較詞彙基線。不要只因輸出變成 768 維就宣布改善。
