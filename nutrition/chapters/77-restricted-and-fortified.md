# 植物飲食、過敏與強化食品的生命階段應用

交叉檢查多重限制，避免一項替代解決一個問題卻製造未知。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/39-restrictions-support.svg" target="_blank" rel="noopener" aria-label="放大：飲食限制、替代與專業合作"><img src="assets/figures/39-restrictions-support.svg" alt="同一餐可能有過敏、強化、質地及臨床限制，需求不等於單純刪除某類；示意不要求所有人採相同限制。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 39｜飲食限制、替代與專業合作</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分開植物飲食、過敏與強化三種資訊，說明替代來源要保留哪些成分功能，不能只因名稱相近就認為缺口自動補上。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.fda.gov.tw/TC/siteListContent.aspx?id=51208&amp;sid=13694">TFDA：素食與植物肉標示</a> · <a href="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/">NIH ODS：維生素B12</a> · <a href="https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/">NIH ODS：維生素D</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 限制可能同時存在

植物飲食、奶過敏、咀嚼問題、宗教與預算可交疊；只用一個標籤分類不足以規劃。先列不能使用的來源、需要保留的營養功能與可取得選項，再看生命階段。

## 強化必須看產品

假設兩款植物飲，一款鈣與D有明示強化值，另一款未提供D，不能把兩者因名稱相近而記相同。成分、蛋白質、每份量、糖、過敏原和搖勻等使用說明也可能重要。

## 食物資料中的未知

範例比較虛構豆飲與乳品等資料，但不宣布所有品牌等值。未知D不是0，已知鈣也不保證其他營養完整；對兒童、孕哺與臨床情境尤其不能用成人示例直接產生替代處方。

## 可查核的下一步

拍下或抄錄完整標示、份量、使用頻率與限制，對照適用來源後與專業人員討論。若某重要營養缺乏可靠來源，重點是確認與規劃，不是用未證實的天然食品宣稱填空。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 39_fortified_foods.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:39_fortified_foods.py -->

## 練習與解答

**請先判斷：** 植物飲未提供D，能否複製另一品牌數值讓報表完整？

<details><summary>展開計算與理由</summary>

不能。品牌、強化及配方不同；保留未知並查產品資料。完整欄位外觀不等於資料品質。

</details>

## 官方參考與跨課閱讀

- [TFDA：素食與植物肉標示](https://www.fda.gov.tw/TC/siteListContent.aspx?id=51208&sid=13694)
- [NIH ODS：維生素B12](https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/)
- [NIH ODS：維生素D](https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/)
- [衛福部：台灣過敏原標示](https://www.mohw.gov.tw/cp-16-43376-1.html)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
