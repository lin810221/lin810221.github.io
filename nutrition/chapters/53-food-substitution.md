# 食物替代：先決定要保留哪個功能

比較不同組合的營養與資料完整性，不輸出單一健康排行榜。

## 替代的目標

替代可能為過敏、宗教、價格、便利、營養或口味。先寫要保留的是蛋白質、鈣、能量、料理功能還是某種限制；很少有替代品在所有維度完全相同。

## 比較兩個虛構組合

範例把穀物、豆腐、蔬菜等依實際克數相加，再與另一組合並列。每種營養素各自追蹤未知，不能因能量完整就宣稱維生素D也完整。類別數不同不直接轉成好壞名次。

## 強化植物飲與乳品

必須讀實際蛋白質、糖、鈣、D等資料與食用份量；未強化產品不因外觀相似就有相同含量，已強化產品也不代表全部營養相同。食物過敏與乳糖不耐又是不同限制，替代理由要清楚。

## 報告替代的代價

列出得到什麼、可能少什麼、未知與可補資料；同時看預算、保存和可行性。這種格式支持討論，而不是假裝幾個數字足以替所有人決定最佳菜單。真正個人治療飲食需要更完整背景。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 27_pattern_comparison.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:27_pattern_comparison.py -->

## 練習與解答

**請先判斷：** 以植物飲替乳品，只確認鈣相同就夠嗎？

<details><summary>展開計算與理由</summary>

不夠。還有蛋白質、糖、D、B12等實際資料和過敏或生命階段背景；同鈣不代表整體等值。

</details>

## 官方參考與跨課閱讀

- [衛福部：我的餐盤](https://www.mohw.gov.tw/cp-2704-41108-1.html)
- [TFDA：素食與植物肉標示](https://www.fda.gov.tw/TC/siteListContent.aspx?id=51208&sid=13694)
- [NIH ODS：鈣](https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/)
- [NIH ODS：維生素B12](https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
