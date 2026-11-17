# 膳食纖維：種類、功能與耐受

分清纖維的物理化學性質，不把所有纖維當同一種補充劑。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/12-fiber-context.svg" target="_blank" rel="noopener" aria-label="放大：纖維、腸道與耐受的關係"><img src="assets/figures/12-fiber-context.svg" alt="腸腔內不同纖維與菌相、含水及個體條件互動；線段不代表單一纖維化學式，也不保證固定效果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 12｜纖維、腸道與耐受的關係</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>將腸腔中的線段當不同纖維，列出溶解性、發酵性或其他特徵可回答的不同問題，不把所有纖維視為同一物。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240073593">WHO：醣類攝取指南</a> · <a href="https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works">NIDDK：消化系統如何運作</a> · <a href="https://www.who.int/news-room/fact-sheets/detail/healthy-diet">WHO健康飲食：2026更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 多個維度

可溶/不可溶、黏性與發酵性不是完全同義分類。不同纖維可影響糞便、腸道發酵、飽足與特定代謝結果，效果依種類與攝取方式；一個「纖維g」總數不足以描述全部機制。

## 食物來源

全穀、豆類、蔬菜、水果、堅果種子提供不同纖維與其他營養。WHO較強調天然存在食物中的纖維與來源品質；不能把單一粉末的克數自動當完整食物模式。產品添加纖維的證據也要看成分與研究。

## 份量和生熟

本例比較熟穀飯、熟蔬菜與完整水果，每100g基準一致後再算150g。生熟或可食部不同會改濃度，增加水不代表總纖維必定變零。未知成分保留未知，不能只因名稱相似就搬另一食物數字。

## 耐受與漸進

腸胃感受受纖維種類、速度、水分與個人狀況影響，增加越快不一定越好。一般建議和疾病治療應分開；有持續症狀時需正確評估，不把所有不適都歸因「排毒」或要求忍耐。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 12_fiber_and_state.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:12_fiber_and_state.py -->

## 練習與解答

**請先判斷：** 兩個食品都標纖維5g，可否保證對腸胃和代謝效果相同？

<details><summary>展開計算與理由</summary>

不能，種類、基質、加工、份量與個體不同。總量提供一個維度，還需來源與特定結果的證據，不能由相同克數直接推相同療效。

</details>

## 官方參考與跨課閱讀

- [WHO：醣類攝取指南](https://www.who.int/publications/i/item/9789240073593)
- [NIDDK：消化系統如何運作](https://www.niddk.nih.gov/health-information/digestive-diseases/digestive-system-how-it-works)
- [WHO健康飲食：2026更新](https://www.who.int/news-room/fact-sheets/detail/healthy-diet)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
