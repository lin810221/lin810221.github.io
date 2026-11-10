# 共同決策：把效益、負擔與偏好放在一起

從「分數多少」走向「這個選擇解決什麼問題」。

## 先確認決策問題

是需要補足量測、進一步評估，還是比較預防選項？有無既往事件與器官疾病，會改變問題。若基線風險、期限或結果不清楚，先補資訊，不要急著用單一百分比決定全部照護。

## 三種資訊並列

可能效益包含降低特定事件；可能傷害包含副作用與檢查負擔；生活條件包含成本、時間和偏好。程式以結構化紀錄檢查這些資訊是否已知，不替它們加權成一個「應該治療」總分。

## 說清不確定性

可詢問證據來自哪些人、多久、效果多大、結果是否重要，以及我的情況有哪些不同。未知時說未知；不把缺少副作用資訊當成沒有副作用，也不把沒有填偏好當成已同意。

## 留下可回顧的計畫

決策可以包含下一步收集什麼、如何監測不適、什麼情況聯繫和何時由團隊回顧。網站整理資料有幫助，但不能以輸入欄位取代完整病史與診察。原治療的改變需透過照護團隊。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 24_shared_decision.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:24_shared_decision.py -->

## 練習與解答

**先自己判斷：** 選項A效果較大，是否無須再問負擔與偏好？

<details><summary>展開驗算與理由</summary>

仍需問。效果的絕對大小、傷害、不確定性、成本與個人價值共同影響決策；資訊缺漏不能自動視為已接受。

</details>

## 官方來源與研究

- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [2026血脂指南官方摘要](https://professional.heart.org/en/science-news/2026-guideline-on-the-management-of-dyslipidemia/top-things-to-know)
- [2026台灣高齡高血壓正式指南](https://pubmed.ncbi.nlm.nih.gov/42926177/)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
