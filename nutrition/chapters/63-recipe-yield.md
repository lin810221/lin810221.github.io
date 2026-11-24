# 食譜、生熟重量與烹調保留率

把重量變化和營養素保留分開，避免把濃縮或吸水誤認為生成營養。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/32-recipe-yield.svg" target="_blank" rel="noopener" aria-label="放大：生熟重量、產率與採買"><img src="assets/figures/32-recipe-yield.svg" alt="原料進鍋後水分及重量可改變，產率與營養保留率不同，規劃還需成本及可取得條件；示意碗量不是實測比例。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 32｜生熟重量、產率與採買</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿原料、烹調和成品三段列各自重量，說明水分變化為何不等於營養憑空增加，並把產率與保留率分開。</div>

<p class="health-figure-sources">圖解依據：<a href="https://fdc.nal.usda.gov/data-documentation/">USDA FoodData Central資料說明</a> · <a href="https://www.who.int/publications/i/item/9789241594639">WHO：食品安全五要點手冊</a> · <a href="https://www.mohw.gov.tw/cp-2704-41108-1.html">衛福部：我的餐盤</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 兩個比例

產率Y是熟重除生重；保留率R是烹調後保留的某營養素比例。吸水可能讓每100g濃度降低，但總量未必降低；失水也可能使每100g濃度提高，不代表創造了營養素。

$$
N_{100g,cooked}=N_{100g,raw}\times\frac{R}{Y}
$$

## 手算示範

100g原料含某營養素10g，煮後250g，假設$R=0.9$，總量9g、每100g熟品3.6g。0.9是明示假設，不是各食材通用實測保留率；若還加入油、鹽與其他食物，需另外納入。

## 一鍋分成多份

先算全鍋可食成品與營養總量，再按實際食用比例分配；湯汁未喝完、殘留鍋底或食材不可食部都可能改變估計。不能只將生重和熟重混放到同一表加總。

## 失敗排查

算出異常高濃度時，檢查克與毫升、可食部、原料或成品基準、產率是否倒置，及保留率是否誤用百分數90當0.9。這個模型不評估加熱殺菌或食物安全。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 32_recipe_yield.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:32_recipe_yield.py -->

## 練習與解答

**請先判斷：** 100g含10g，熟重250g且保留90%，每100g熟品是多少？

<details><summary>展開計算與理由</summary>

全鍋保留9g，除250g乘100為3.6g。重量產率2.5與保留率0.9應分開；安全性不能由此式推論。

</details>

## 官方參考與跨課閱讀

- [USDA FoodData Central資料說明](https://fdc.nal.usda.gov/data-documentation/)
- [WHO：食品安全五要點手冊](https://www.who.int/publications/i/item/9789241594639)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
