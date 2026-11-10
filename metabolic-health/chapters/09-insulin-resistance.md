# 胰島素作用與阻抗：不是只有高血糖

理解分泌、敏感性和代償，分清研究指標與臨床判斷。

## 激素與組織反應

胰島素參與葡萄糖利用、儲存與其他代謝調節；組織對訊號反應不同時，分泌可能代償。血糖仍在某範圍不代表每個過程都相同，胰島素較高也不能脫離情境直接診斷。

## 胰島素阻抗

肝、肌肉和脂肪組織可有不同反應，並受生理、遺傳、健康與生活等影響。阻抗不是個人道德標籤，也不是只要少吃一種食物就能精確修復的單一開關。

## HOMA1的用途

$$
HOMA1\!\text{-}IR\approx\frac{insulin_{\mu U/mL}\times glucose_{mg/dL}}{405}
$$

空腹8與100得到約1.98。這是研究近似、不是HOMA2或鉗夾測量，沒有一個普遍界線可套所有族群與檢驗；非空腹資料本課不計。

## 不從一項推全部

Oxford提醒舊近似式與現行胰島素assay校準有差異，不宜將它當成現代HOMA2；HOMA2是非線性電腦模型，沒有通用正常值。臨床評估依病史、檢驗與適用方法，未必常規需要空腹胰島素。工具教單位和假設，不從研究指數替個人確診、選補充品或開治療。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 05_homa_research.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:05_homa_research.py -->

## 練習與解答

**先自己判斷：** 算出HOMA1約1.98，是否可套網路單一門檻判每個人有無阻抗？

<details><summary>展開驗算與理由</summary>

不應。族群、檢驗、方法與用途不同，指數是研究近似且不等於直接測量；需適當背景與專業判斷。

</details>

## 官方來源與研究

- [Oxford：HOMA模型歷史與近似式限制](https://www.rdm.ox.ac.uk/about/our-facilities-and-units/DTU/software/homa/history)
- [Oxford：HOMA沒有普遍正常範圍](https://www.rdm.ox.ac.uk/files/clinical-studies-and-and-trials/homa-no-normal-range/%40%40download)
- [NIDDK：胰島素阻抗與糖尿病前期](https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/prediabetes-insulin-resistance)
- [OpenStax：胰臟內分泌](https://openstax.org/books/anatomy-and-physiology-2e/pages/17-9-the-endocrine-pancreas)
- [ADA2026：診斷與分類正式原文](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
