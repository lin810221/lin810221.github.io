# 最大肌力：負荷特異性與估計公式

讀懂高負荷證據，分清研究最佳化和初學者當下需要。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/22-strength-power.svg" target="_blank" rel="noopener" aria-label="放大：最大肌力與快速施力的任務差異"><img src="assets/figures/22-strength-power.svg" alt="任意曲線提示力、速度與功率有不同問題定義，沒有固定通用最佳負荷或個人1RM推定值。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 22｜最大肌力與快速施力的任務差異</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分別說出最大肌力測試與快速完成指定任務要觀察什麼，再指出圖沒有個人能力、技巧與方法；不能由曲線位置自動估出1RM。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 最大力量的任務性

動作、ROM、器材和技術共同定義測試；練習較接近測試需求可能提高相應表現。ACSM2026對健康成人最大力量的最佳化支持較高負荷等條件，但不是要求所有初學者第一天就測最大或直接上高負荷。

## 相對強度的前提

以%1RM安排需有可靠且相符的參考；公式估計、舊測值或另一器材的值都可能不適用。相對負荷不包含所有努力與疲勞，仍要看實際完成與技術。

## 兩個估計

$$
\widehat{1RM}_{Epley}=L(1+r/30),\qquad
\widehat{1RM}_{Brzycki}=36L/(37-r)
$$

60kg做5次分別70與67.5kg。本課只用1–10次作教育比較，單次直接保留重量；公式不是保證個人真正最大值，也不推薦拿估值立即試舉。

## 訓練決策

先建立可控制動作、持續紀錄與合適監督；再依目標逐步安排阻力。把估計、實測與訓練重量分欄，可避免一個推估數字變成自動指令。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 22_estimated_one_rm.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:22_estimated_one_rm.py -->

## 練習與解答

**先自己判斷：** 估1RM70kg，是否表示下一堂應直接舉70kg？

<details><summary>展開理由與驗算</summary>

不是。估值有條件和誤差，訓練與測試目的不同，還需技術、準備、健康與保護條件。

</details>

## 官方來源與研究

- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
