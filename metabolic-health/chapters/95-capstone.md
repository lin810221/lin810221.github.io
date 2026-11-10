# 整合專題：從虛構資料到可審核摘要

完成一次資料、程式、圖表與證據的連結。

## 任務與交付物

用本課合成資料輸出observations.csv、bp_observations.svg和report.json。附短說明：資料如何取得、可計算什麼、缺漏在哪、哪些推論不能做。不要加入真實姓名或把個人病歷放進公開GitHub。

## 按步驟完成

先看metadata和來源表，再跑單位與缺漏範例，執行測試，最後用48_complete_project.py指定新輸出資料夾。驗證五個資料雜湊、27次有效血壓與缺漏non-HDL；對照原始檔，確保沒有隱藏補值。

## 加入自己的研究問題

可以問「排除首日會如何改變可用平均與排定分母」「盛行率改變如何影響PPV」。這些問題由明確算術回答，不需個人醫療判斷。若改輸入或公式，更新說明與相應驗證，不只換圖色。

## 評分的依據

看單位、資料完整性、來源版本、可重跑與結論是否超出證據，而不是圖是否朝理想方向走。沒有診斷反而是符合範圍；缺漏如實保留，比補成漂亮完整數字更有學習價值。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 48_complete_project.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:48_complete_project.py -->

## 練習與解答

**先自己判斷：** 專題要如何證明自己沒有悄悄補值？

<details><summary>展開驗算與理由</summary>

保留原始資料與雜湊，列缺漏規則與衍生公式，檢查27/28及第三筆non-HDL未知，讓他人用同版程式重跑，而不是只交一張圖。

</details>

## 官方來源與研究

- [Python3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [KDIGO2024正式完整指南](https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
