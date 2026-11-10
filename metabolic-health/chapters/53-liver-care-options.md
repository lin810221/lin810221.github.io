# MASLD照護：生活、共病與新治療

使用現行資訊，不再沿用「脂肪肝沒有藥」的過時概括。

## 先定義照護目的

減少心代謝風險、改善肝臟疾病及處理其他病因，是相連但不同的目的。適用選項取決於是否MASH、纖維化程度、共病與當地核准；影像見脂肪不能直接決定用哪項藥。

## 生活支持與共病

飲食、活動、體重管理及酒精暴露需要可行支持，並與糖尿病、血壓、脂質及腎臟照護整合。不是只等ALT下降，也不是所有體位與生命階段都用同一減重目標。細節需回到營養與運動主線及個別條件。

## 有更新的藥物證據

AASLD已提供2024 resmetirom與2025 semaglutide等特定MASH相關更新入口。因此「所有脂肪肝完全沒有藥物」不再是準確概括。但美國FDA核准、國際指南、台灣許可與給付不同，不可由外國新聞推定台灣可用於任何人。

## 不自行開立路徑

程式列出選項需查核的資料，沒有劑量、個人資格或自動處方。療效要看相應臨床終點、病理與長期不確定性，並權衡副作用和負擔。已在接受治療者，變動需透過照護團隊。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 27_liver_followup.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:27_liver_followup.py -->

## 練習與解答

**先自己判斷：** 知道美國核准某MASH用途，是否就能說台灣所有脂肪肝患者都適用？

<details><summary>展開驗算與理由</summary>

不能。疾病範圍、纖維化、個人條件、台灣許可與給付需分別核對；不能從一則核准訊息推論全部適用。

</details>

## 官方來源與研究

- [AASLD：MASLD／MASH更新總入口](https://www.aasld.org/practice-guidelines/clinical-assessment-and-management-metabolic-dysfunction-associated-steatotic)
- [AGA2026 MASLD正式路徑原文](https://pubmed.ncbi.nlm.nih.gov/41812830/)
- [EASL2024 MASLD正式指南](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299976/)
- [2026 AHA／ACC CKM正式指南](https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
