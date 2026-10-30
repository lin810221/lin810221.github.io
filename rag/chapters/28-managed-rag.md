## 先看自己需要控制到哪裡

自建流程可選解析器、chunker、encoder、權限模型、reranker 與儲存；代價是維護整條資料管線。託管工具把部分匯入、索引與檢索交給供應商，通常上手快，但仍需驗證資料狀態、配額、版本、刪除與可觀測性。

選型應列出必須控制的欄位：來源定位、繁體中文品質、租戶隔離、資料處理地點、更新頻率、輸入格式與成本。不要只因介面提供 upload 按鈕，就認定已滿足你的知識治理。

## OpenAI File Search

OpenAI 的 Responses 可搭配 `file_search` 工具與 vector store；先準備並完成文件索引，再在請求提供 store 識別。下面是欄位示意，需把模型與 ID 換成自己帳戶可用值，課程網頁不會執行這個請求。[OpenAI File Search](https://developers.openai.com/api/docs/guides/tools-file-search)

```json
{
  "model": "YOUR_RESPONSES_MODEL",
  "input": "依文件回答特休申請期限並提供引用。",
  "tools": [{"type":"file_search", "vector_store_ids":["YOUR_STORE_ID"], "max_num_results":5}]
}
```

工具回應和輸出 annotations 需要依官方 schema 解析；不能只拿到自然語言答案就忽略引用資料。這與第 14 份範例的自建 dense retrieval 是不同整合路徑。

## Gemini File Search

Gemini 官方 File Search 提供匯入、切塊與索引等能力，並可在回答中使用檢索資訊。模型、檔案模態、操作完成狀態與 metadata filter 需按目前文件確認，不能把一般 Embedding 的能力全部推論到 File Search。[Gemini File Search](https://ai.google.dev/gemini-api/docs/file-search)

## Claude 生成器與自建檢索

也可以自行完成檢索與 context，交給 Claude Messages 生成。Anthropic 的 Contextual Retrieval 資料提供前處理與檢索設計參考；它不是所有帳戶皆自動啟用的完整知識庫產品。[Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)

生成器選擇與索引選擇可以獨立。遷移生成器時驗證 prompt、輸出格式、引用與完成狀態；遷移 encoder 則需要處理文件向量相容性，兩者不是同一種工作。

## 三條路線怎麼比較

用同一份公開或虛構文件，測相同問題，保存檢索結果、答案引用、延遲與實際 usage。託管服務如果看不到所有中間步驟，就把這項可觀測性差異記入選型，而不是假裝可以完全同樣除錯。

匯入後等待 ready，再驗證能找到指定原句；更新後確認舊版消失；刪除後檢查可見性。供應商處理底層索引，不代表應用程式可以省略使用者授權與資料生命週期管理。

## 練習與參考答案

**題目：**託管工具顯示檔案已上傳，能立刻向使用者說知識庫已更新嗎？

**參考答案：**先確認索引操作完成並成功，抽查查詢命中新版本，再發布更新狀態。上傳成功只是取得檔案，不代表解析、索引與可查詢狀態已全部完成。
