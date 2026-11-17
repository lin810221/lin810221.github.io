# GI、GL與實際血糖：別把指標當預測器

分清固定測試、食用份量和個人反應，正確使用血糖指標。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/11-grain-matrix.svg" target="_blank" rel="noopener" aria-label="放大：穀粒結構與加工：GI之外的資訊"><img src="assets/figures/11-grain-matrix.svg" alt="穀粒的麩皮胚乳胚芽概念剖面，配合加工與餐食條件理解，不把全穀或某個GI值直接換成個人血糖曲線。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 11｜穀粒結構與加工：GI之外的資訊</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指出食物結構可影響處理的哪些條件，再將GI、實際份量和餐食搭配分開，說明圖不能直接預測個人血糖。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240073593">WHO：醣類攝取指南</a> · <a href="https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works">NIDDK：消化系統如何運作</a> · <a href="https://www.mohw.gov.tw/cp-2704-41108-1.html">衛福部：我的餐盤</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## GI在測什麼

GI比較特定測試條件下，含指定可利用碳水量食品與參照物的血糖反應。它不是糖含量，也不是完整營養評分；食物品種、加工、熟度與研究方法會影響。未知GI不能從營養標示計算出來。

## GL加入份量

常用GL=GI×該份可利用碳水g/100。示例GI55、碳水30g，GL16.5；份量加倍會使這個算式加倍。它只把兩個輸入相乘，沒有模擬個人的血糖峰值或長期風險。

$$
GL=\frac{GI\times C_{available,portion}}{100}
$$

## 混合餐和個人差異

同餐脂肪、蛋白質、纖維、胃排空、活動、藥物與生理狀況會改變反應。不能把單一食物GI直接當整餐實測，也不能由一次穿戴/連續血糖曲線自行診斷疾病。個人治療目標需另有評估。

## 如何使用而不過度使用

先看食物類別、纖維、份量與整體模式，再把GI/GL當特定問題的輔助資訊。低GI食物仍可能含很多能量、鈉或其他成分；高GI也不自動代表整份食物不可吃。保存來源和定義，不追求單一最小數字。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 11_gi_gl.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:11_gi_gl.py -->

## 練習與解答

**請先判斷：** GI已知，是否只需輸入份量就能準確畫個人餐後血糖曲線？

<details><summary>展開計算與理由</summary>

不能，GL算式只給粗略指標，缺少消化、混合餐、個人代謝與用藥等資訊。範例不提供血糖預測或診斷，未知GI也不硬填。

</details>

## 官方參考與跨課閱讀

- [WHO：醣類攝取指南](https://www.who.int/publications/i/item/9789240073593)
- [NIDDK：消化系統如何運作](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
