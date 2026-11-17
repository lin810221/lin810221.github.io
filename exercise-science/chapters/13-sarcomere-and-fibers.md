# 肌肉如何收縮：肌節、鈣與ATP

把分子層級接回動作，理解收縮不必然等於整條肌肉縮短。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/07-sarcomere.svg" target="_blank" rel="noopener" aria-label="放大：肌節、滑動與收縮情境"><img src="assets/figures/07-sarcomere.svg" alt="Z線之間是肌節，細肌絲連向Z線、粗肌絲居中；滑動改變重疊，不是肌絲消失或自身縮短。" width="860" height="510" loading="lazy"></a><figcaption><strong>圖 07｜肌節、滑動與收縮情境</strong>本學習空間原創解剖圖再用，非比例；按本單元任務閱讀。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先指認兩條Z線、粗肌絲與細肌絲，再說出鈣與ATP在原課文的角色；注意滑動改變重疊，不代表肌絲本身縮短或消失。</div>

<p class="health-figure-sources">圖解依據：<a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a> · <a href="https://training.seer.cancer.gov/anatomy/nervous/tissue.html">NCI：神經組織</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 從肌肉到肌節

肌肉由多層組織與肌纖維構成，纖維內有肌原纖維和重複肌節。肌動蛋白與肌凝蛋白互動形成張力；滑動模型不是兩種絲本身變短，而是相對滑動。

## 訊號與能量

神經訊號引發膜電位和鈣調節，鈣使作用位置可用，ATP參與橫橋循環及相關運輸。不能把肌肉用力簡化為ATP瞬間全部耗完；實際疲勞有神經與周邊等多種因素。

## 肌纖維的不同特徵

I與II型等分類涉及收縮與代謝特性，肌肉含多種類型及個別差異。長時間低力與短時高力任務的需求不同，但不能由喜歡跑步或一次表現反推個人精確纖維比例。

## 從基礎到訓練

阻力和耐力訓練可改變功能與組織特徵，適應需看任務和時間。範例刻意把纖維百分比留未知：任務標籤提供背景，沒有活檢等資料就不假裝量到構成。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 07_fiber_context.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:07_fiber_context.py -->

## 練習與解答

**先自己判斷：** 肌節滑動是否表示肌動蛋白和肌凝蛋白本身都縮短？

<details><summary>展開理由與驗算</summary>

不是。主要是絲的相對滑動；另外，產生張力與整個關節是否移動也不同，等長任務仍可有張力。

</details>

## 官方來源與研究

- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [OpenStax：肌纖維類型](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-5-types-of-muscle-fibers)
- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
