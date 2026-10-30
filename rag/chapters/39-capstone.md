## 專案要交付什麼

做一個星河工作室的虛構手冊助理：一般讀者能查休假、差旅、遠端與 IT；已失效文件、人資專用資料和別的租戶不能混進證據。找到來源時擷取原句並引用，沒有足夠依據就回報不足。這些規則都是教材資料，不是現實公司政策。

專案採標準函式庫與 CLI，讓你先掌握核心邏輯。完整預設流程不需要 API 或模型下載；可在隔離環境驗收，後續再以 adapter 換掉檢索或生成器。

## 專案資料夾

```text
examples/
  rag_core.py           資料型別、切塊、BM25、授權、context、指標
  provider_http.py      選配 Embeddings 與 Responses adapter
  01_...16_*.py         分階段實作入口
  test_examples.py     邊界與資料流驗收
  data/documents.json  虛構文件與權限反例
  data/qrels.json      小型開發題集
```

核心 `ask()` 依序建立片段、授權檢索、詞元覆蓋重排、字元預算封裝與原句回答。回應保存 `mode`，避免把擷取結果誤標為模型生成。對每個來源保存原句與版本，讓你能從輸出反查。

## 執行完整入口

<!-- example:16_capstone.py -->

```powershell
python 16_capstone.py "國內出差住宿費上限"
python 16_capstone.py "特休申請提前"
python 16_capstone.py "火星基地氧氣費率"
python 11_evaluation.py
python -m unittest discover -s . -p test_examples.py -v
```

從網站原始碼根目錄執行時，加上 `rag/examples/`。這些程式全部根據自身檔案位置讀取資料，測試也會在另一個臨時工作目錄執行所有入口，並阻擋網路連線。

## 怎樣才算完成

查特休應引用 leave 並保留三個工作日；查國內住宿應用現行 travel 的 2400，而非過期 1800；一般讀者不應在 context 得到薪資資料；不存在的租戶沒有候選；沒有知識的題目回不足。結果格式、內容與資料流都應檢查。

這些確定性驗收只證明教材基線的行為。原句擷取對否定、歧義與多步推論仍有限制，不應直接把此 CLI 包成公開問答服務後宣稱已具備生產等級語意理解。

## 下一階段的替換位置

將 `retrieve()` 換成持久化向量與 BM25 融合；將 `lexical_rerank()` 換成已評估 cross-encoder；將 `extractive_answer()` 換成生成 adapter。保留同樣 evidence map、授權與狀態契約，再用同一題集比較。

SQLite 範例說明資料與交易，不代替大型索引服務；正式部署再加身分驗證、資料儲存與可觀測性。[Python sqlite3](https://docs.python.org/3/library/sqlite3.html)

## 練習與參考答案

**題目：**把自己的文件換進去，第一步是直接加 `--live` 嗎？

**參考答案：**先確認文件可使用與可外傳的範圍，完成解析、版本、授權與離線檢索驗收，再選擇模型處理方式。先用已知問題檢查來源是否正確；在上游仍錯誤時送到更強模型，會增加成本而難以定位。
