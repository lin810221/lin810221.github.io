## 先確認兩種不同成品

目前個人網站提供課程、互動示範與範例下載，全部是靜態檔案。GitHub Pages 可服務這些 HTML、CSS 與 JavaScript；它不會直接執行本章的 Python 查詢流程。要讓訪客真正上傳私人文件並呼叫模型，需要另外的後端服務。[GitHub Pages 概述](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

瀏覽器原始碼對訪客可見，不能把 API Key 寫進 HTML 或前端 JavaScript。後端保存金鑰、驗證使用者、限制資料範圍與用量，前端透過受控 API 取得答案。

## 真正 Dense RAG 的選配範例

本程式預設仍執行離線基線。只有 `--live` 會對可見虛構文件產生 Embedding、對問題產生 Embedding、做 cosine 排名，再呼叫 Responses。此處沒有預訓練向量的假資料冒充真實語意表示。

<!-- example:14_live_rag.py -->

`OPENAI_RAG_MODEL` 請填自己帳戶可用且支援 Responses 的模型。程式進行兩次 Embeddings 請求與一次生成請求，不會自動重試；每次重新計算少量文件向量是為了展示，正式服務應事先建立索引。

## 本機設定與驗收

```powershell
$env:OPENAI_API_KEY = "自己的金鑰"
$env:OPENAI_RAG_MODEL = "自己的模型名稱"
python 14_live_rag.py "特休申請需要提前幾天？" --live
```

這會送出教材與問題並可能收費。本次課程開發只測試離線與模擬 API 回應，不會替你執行付費呼叫。若 API 回應未完成，程式回 incomplete；若引用編號檢查失敗，顯示需要人工審核，而不是直接當最終答案。

## 正式服務還需要哪些工作

先將索引與原文持久化，建立驗證身分的查詢 API、輸入大小限制、逾時與限流。前端只顯示應用允許的狀態與來源，不任意執行模型產生的 HTML。多租戶從身分範圍建 query filter，引用原文也再次授權。

模型生成回應與工具結果應依官方 schema 解析；不同供應商的完成狀態與文字區塊不可混用。[OpenAI 文字生成](https://developers.openai.com/api/docs/guides/text)

## 更新這份課程網站

修改 `rag/chapters/*.md` 或 `course.json` 後，Actions 會在 Push 時編譯全部課程、驗證連結、測試範例並發布靜態頁面。若要本機預覽生成結果，先執行 `python tools/build.py rag`；瀏覽器不會自行編譯 Markdown。

## 練習與參考答案

**題目：**把 Python 檔上傳 GitHub Pages，訪客按按鈕就能用你的 API Key 執行嗎？

**參考答案：**不會自動執行 Python；也不應把金鑰放在靜態網站。訪客下載範例後可在自己的本機執行；公開線上問答則需要另外部署受控後端，並設定身分、用量與資料存取政策。
