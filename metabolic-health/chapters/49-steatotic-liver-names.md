# SLD、MASLD與MASH：名稱背後的問題

從脂肪沉積走到病因、發炎與纖維化。

## 為何有新名稱

脂肪性肝病以SLD作為上位概念，MASLD強調肝脂肪沉積與心代謝條件的連結；MASH指相應的脂肪性肝炎脈絡。這些名詞不是單純把所有舊NAFLD資料改字，研究納入標準和病因仍需核對。

## 酒精與其他病因

酒精暴露、病毒、藥物或其他原因可以同時存在。MetALD等分類需依正式定義評估，不可只憑一句「偶爾喝」判定；酒精量、期間與其他原因都要具體詢問。本課不提供自行分類的飲酒配額。

## 脂肪、發炎與纖維化不同

影像見到脂肪，不能直接宣稱MASH或知道纖維化程度。肝臟指數不高也不能保證沒有重要疾病。臨床問題包括有無其他病因、是否有進展性纖維化，以及心血管與代謝共病。

## 使用2026路徑

AGA2026更新風險分層照護路徑，結合初步評估與後續非侵入檢查；EASL2024也提供正式指南。程式整理來源、年份和用途，不用來源國家相似縮寫混認學會；例如2026 TASL並不是台灣學會指南。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 25_liver_source_context.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:25_liver_source_context.py -->

## 練習與解答

**先自己判斷：** 超音波寫脂肪肝，是否已證實MASH及纖維化分期？

<details><summary>展開驗算與理由</summary>

沒有。脂肪沉積、發炎和纖維化是不同問題，需依臨床背景與適當評估確認，並考慮其他病因。

</details>

## 官方來源與研究

- [AGA2026 MASLD正式路徑原文](https://pubmed.ncbi.nlm.nih.gov/41812830/)
- [EASL2024 MASLD正式指南](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299976/)
- [AASLD：MASLD／MASH更新總入口](https://www.aasld.org/practice-guidelines/clinical-assessment-and-management-metabolic-dysfunction-associated-steatotic)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
