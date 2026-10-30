# RAG 檢索增強生成完整教學

從 [index.html](index.html) 開始；也可以從學習網站首頁進入 RAG。42 章、8 個單元，沿用深色閱讀器、離線 LaTeX、全文搜尋、獨立進度與筆記。

課程涵蓋文件解析、切塊、BM25、Embedding、向量索引、Metadata Filter、Hybrid/RRF、重排、MMR、Query Transformation、Context、引用與拒答、對話、結構化資料、多模態、Agentic RAG、GraphRAG/RAPTOR、評估與正式服務。

首頁的三個離線實驗室：

1. 實際 BM25、同義擴展/RRF、可見範圍切換與原句引用。
2. 可修改文件、大小及重疊的 Unicode 字元切塊。
3. 可調排名的 Precision、Recall、MRR 和 nDCG。

所有示範組織與規章均為虛構。網頁不呼叫模型，也不需要 API Key。16 份 Python 入口預設離線，真正模型接法需明確指定 `--live`；詳見 [範例說明](examples/README.md)。離線擷取與手工向量不代表執行了神經模型。

從網站原始碼根目錄編譯及檢查：

```powershell
python tools/build.py rag
python tools/validate.py
python -m unittest discover -s rag/examples -p test_examples.py -v
```

內容原稿位於 `chapters/*.md`，分組與摘要在 `course.json`。`assets/course-data.js` 和 `examples.zip` 由建置工具產生；ZIP 包含共用模組、測試與巢狀資料檔。推送到 `main` 後，既有 GitHub Actions 會驗證並發布全部課程。
