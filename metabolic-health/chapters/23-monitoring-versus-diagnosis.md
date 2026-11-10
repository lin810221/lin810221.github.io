# 家用血糖、CGM與實驗室：用途不同

理解指尖和間質液監測，不將漂亮曲線當所有疾病的檢驗。

## 三種資料來源

實驗室血漿、家用指尖和CGM間質液來源不同，設備、取樣和演算法可能影響數字。CGM還有時間反應與訊號條件，單點不同不必直接推誰錯。

## 監測和診斷

監測可支持特定照護和行為觀察，但ADA2026指出目前證據不足以用CGM篩檢或診斷糖尿病前期／糖尿病。工具有特定核准用途，也不等於所有族群都需購買或追蹤每次波動。

## 曲線的限制

餐後波動、睡眠與活動的相關線索不直接證明哪個因素造成，也不能以曲線越平判整體營養越好。若為了壓平曲線而過度限制食物，可能漏掉其他健康需要。

## 觀察資料的正確處理

記設備、版本、時間、樣本與協定；未知空腹或症狀不填否。範例只列缺少的臨床條件，不把虛構紀錄變成個人診斷或監測產品推薦。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 12_test_protocol.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:12_test_protocol.py -->

## 練習與解答

**先自己判斷：** 健康者CGM曲線平，就能證明所有代謝健康且不需任何其他評估嗎？

<details><summary>展開驗算與理由</summary>

不能。監測來源與用途有限，沒有涵蓋所有器官、風險或診斷；也不以CGM直接替代正式篩檢和診斷。

</details>

## 官方來源與研究

- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [NGSP：2026更新檢驗干擾資料](https://ngsp.org/factors.asp)
- [NIDDK：胰島素阻抗與糖尿病前期](https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
