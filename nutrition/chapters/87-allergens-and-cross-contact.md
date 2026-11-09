# 食物過敏原、乳糖不耐與交叉接觸

區分免疫反應和消化不耐，讀懂地區清單與標示的限制。

## 過敏與不耐不同

食物過敏涉及免疫系統，乳糖不耐涉及乳糖消化等問題；無乳糖不等於沒有乳蛋白，也不自動適合乳品過敏者。不能因某食物讓人不舒服就自行歸為同一機制。

## 台灣11類的範圍

台灣主要標示類別包括甲殼類、芒果、花生、牛羊奶、蛋、堅果、芝麻、含麩質穀物、大豆、魚，以及符合殘留條件的亞硫酸鹽等；規範另有例外與細節。美國9類不能直接取代台灣清單。

## 成分與交叉接觸

配方未加某原料不代表製程與器具完全沒有接觸；沒有「可能含有」警語也不足以證明不含。嚴重過敏者需確認具體產品與管理資訊，依醫療團隊的個別計畫處理。

## 程式輸出的邊界

範例把ingredient_present、cross_contact與not_checked分開；未知不得自動轉false。教材不提供自我激發試驗或依微量數字判個人可安全食用，因個別反應與處理需要專業評估。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 44_cross_contact.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:44_cross_contact.py -->

## 練習與解答

**請先判斷：** 無乳糖牛奶是否必然適合牛奶蛋白過敏者？

<details><summary>展開計算與理由</summary>

不一定，通常仍含乳蛋白。乳糖不耐與蛋白過敏不同，需查成分與個別過敏管理計畫。

</details>

## 官方參考與跨課閱讀

- [衛福部：台灣過敏原標示](https://www.mohw.gov.tw/cp-16-43376-1.html)
- [FDA：食物過敏](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies)
- [NIDDK：消化系統如何運作](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
