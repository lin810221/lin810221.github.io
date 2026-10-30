## 這個 API 回傳什麼

Embedding 請求把一段或多段文字轉成向量，不會直接產生自然語言答案。範例以 `text-embedding-3-small` 作明確示範，輸入兩句自行撰寫教材。實際可用模型與限制需依帳戶和官方文件確認。

請求包含 `model`、`input`，並明確指定 `encoding_format="float"`。支援的模型可用 `dimensions` 請求較小輸出；不能假定所有舊模型或任意新名稱都接受同一選項。[OpenAI Embeddings API](https://developers.openai.com/api/reference/resources/embeddings/methods/create)

## 先看請求，不先付費

<!-- example:17_openai.py -->

預設只列出 payload。加 `--live` 才呼叫外部 API，金鑰從 `OPENAI_API_KEY` 讀取。程式不把金鑰寫進教材或瀏覽器，也不自動重試。

```powershell
python 17_openai.py
python 17_openai.py --dimensions 256
# 下列才送出真正請求，可能產生費用
python 17_openai.py --live
```

## 回應怎麼配對

回應 `data` 各列有 index 與 embedding。應按 index 對回輸入，確認沒有缺漏、重複或越界，再檢查維度和有限數值。不能只假設網路回傳列順序永遠是原順序。

保存原始文件 ID 與輸入索引的映射，避免向量 A 接上原文 B。這類錯誤不一定讓距離計算報錯，卻會產生難以解釋的錯來源。

## 輸入與限制

空字串、超長輸入、批次限制與速率限制都應明確處理。token 上限不等於中文字元數，正式流程需用相應計數和文件上限分批。不要用默默截斷讓請求成功，卻遺失問題所需內容。

範例只送兩句短文字，目的是學介面，不是完整大量匯入工具。批次、有限退避和工作進度在第 23 章說明。

## 維度變更就是設定變更

文件使用 1536 維、query 改用 256 維，不能直接相乘。即使使用模型支援的降維，兩側維度和 recipe 仍需一致；資料庫、cache key、模型 manifest 和評估結果都要同步更新。

## 練習與參考答案

**題目：**API 成功回 200，但有兩筆 index 都是 0，可以繼續建索引嗎？

**參考答案：**應拒絕這個批次並保留錯誤狀態。HTTP 成功不代表資料契約正確。教材測試會用模擬回應驗證重複與缺失 index，不執行付費呼叫。
