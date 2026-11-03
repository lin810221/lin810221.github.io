# MCP 與 RAG：搜尋、讀取、引用與權限

用工具與資源建立可追溯知識流程，同時保留檢索品質的獨立責任。

## 把流程拆成可驗證步驟

知識助理可以先呼叫 search_docs，回傳短摘要、穩定文件 ID 與來源，再依需要讀取 Resource 全文，最後生成帶引用的回答。這樣能控制資料量，也讓 Host 追蹤「哪個工具取得哪份資料」。

MCP 是把這些能力接到 Host 的介面，並不取代 RAG 中的 chunking、embedding、召回、重排、引用與評估。檢索品質很差的系統包成 MCP 之後，仍然可能給出沒有證據的答案。

## 搜尋與讀取都做 ACL

若搜尋已過濾權限，讀取也不能省略驗證。文件可能在兩次呼叫之間被撤權，或者 URI 被其他使用者取得。反過來，只有讀取時驗證也不夠，搜尋摘要與文件標題本身就可能是敏感資料。

快取鍵要反映主體與權限修訂；向量索引也應保存可正確套用的 tenant 和資料可見性。不要先全庫搜尋，把跨租戶結果送入模型，再讓模型自行挑出可用內容。

## 引用要能回到穩定來源

搜尋結果可以回 doc_id、revision、uri、title 和摘要。Host 生成回答時，保留這些來源與引用對應，避免只剩一段無法查驗的自然語言。ResourceLink 代表可讀位置，並不證明內容已被讀取或支持某個論點。

若結果不足以支持答案，應明確說明。用不同文件中的單字湊出回答，不等於證據成立；工具有成功回傳資料，也不代表資料和使用者問題相關。

## 專題中的簡化檢索

本課 notes 使用字串比對，目的是驗證 tenant filtering、資料路徑與工具契約，不宣稱具有向量語意檢索品質。你可以將 search_notes 的領域實作換成已完成的 [RAG](../rag/index.html) 或 [Embedding](../embedding/index.html) 管線，保持相同輸入與結果契約。

這種 adapter 設計可以讓模型與 Host 不必因後端換了檢索器而全部重寫，但檢索行為變更仍需更新結果語意、品質評估與資料版本。

## 練習與解答

設計一個結果物件，至少含摘要、穩定來源和是否截斷，再列三種必測反例。參考答案：其他租戶不能命中；已撤權 URI 不能再讀；沒有相關資料時不能編造引用。最後把「協定成功率」與「答案支持率」分開量測，兩者不是同一指標。

## 官方閱讀

- [Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)
- [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Client best practices](https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices)
