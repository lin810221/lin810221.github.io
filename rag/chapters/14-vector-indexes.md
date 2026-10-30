## 先建立 exact baseline

對每個可見文件向量計算 cosine，再排序取前 k，稱為精確搜尋。它容易理解與驗證，但計算量隨片段數與維度增加。小資料集可以先使用這個方法，之後才用它當近似索引的參考答案。

近似最近鄰搜尋 ANN 用索引結構換取速度，可能漏掉精確結果。衡量 ANN recall 時，要比較同一份向量、相同權限與距離設定下的 exact top-k；這與「是否找到回答所需證據」的任務 recall 是兩種指標。

## HNSW 的直覺

HNSW 建立多層鄰接圖，從較稀疏的上層導航，再到下層探索候選。它不是把所有距離都算完。原論文提出這種階層圖式近鄰搜尋設計。[HNSW 論文](https://arxiv.org/abs/1603.09320)

常見設定包含鄰接程度、建置候選與搜尋候選。提高搜尋探索通常能改善召回但增加延遲；提高建置品質也可能增加匯入時間與記憶體。參數名稱依產品不同，應從實測曲線選擇，而不是只抄一組數值。

## 資料庫負責的事

向量運算函式庫主要解決最近鄰；資料庫還需要存原文、metadata、版本、更新、併發、備份與存取控制。選擇時列出這些需求，不要只比較一個延遲數字。原文也可以放在另一個受控文件儲存，索引只保存識別與表示。

以下是 PostgreSQL 搭配 pgvector 的概念 SQL，需自行準備 extension 和連線；教材離線範例不會建立 PostgreSQL 服務：

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE knowledge_chunks (
  tenant text NOT NULL,
  chunk_id text NOT NULL,
  body text NOT NULL,
  embedding vector(1536),
  PRIMARY KEY (tenant, chunk_id)
);
-- $1、$2、$3 由資料庫 driver 綁定，不是字串插值。
SELECT chunk_id, body
FROM knowledge_chunks
WHERE tenant = $1
ORDER BY embedding <=> $2::vector
LIMIT $3;
```

pgvector 使用不同運算子處理不同距離；索引 operator class 需要匹配查詢運算。上例示意 cosine 距離，維度必須跟實際模型一致。[pgvector 官方說明](https://github.com/pgvector/pgvector)

## 篩選與近似搜尋的交互作用

如果 ANN 先探索有限候選，再套 metadata filter，結果可能不足 k 筆，即使可見資料中實際有足夠相關片段。要查明產品的 filter、探索與迭代掃描語意，並用高選擇性篩選做測試。

## 練習與參考答案

**題目：**資料庫搜尋只回兩筆，`LIMIT 10`，可否斷言只有兩份相關文件？

**參考答案：**不一定。可能受篩選、索引探索、分數閾值或資料狀態影響。先用相同可見範圍的精確搜尋比較，再檢查 ANN 設定與實際候選數。查詢回傳數與知識庫中相關資料數並不相同。
