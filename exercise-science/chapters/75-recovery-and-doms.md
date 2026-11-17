# 疲勞、DOMS與恢復觀察

分清一般訓練反應、警訊與長期問題，不用痠痛判進步。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/38-recovery-context.svg" target="_blank" rel="noopener" aria-label="放大：恢復受到任務與生活共同影響"><img src="assets/figures/38-recovery-context.svg" alt="睡眠、工作壓力、任務及支持與恢復討論相連，不把線條長短當影響量，也不由酸痛推療效。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 38｜恢復受到任務與生活共同影響</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先分DOMS感覺、當下表現與組織適應三個問題，再沿圖列生活條件；沒有酸痛不代表沒有訓練效果，有酸痛也不證明有效增長。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://training.seer.cancer.gov/anatomy/nervous/tissue.html">NCI：神經組織</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## DOMS的基本概念

不熟悉或新奇負荷後可能出現延遲痠痛，和活動中急性疼痛不同。它不是乳酸留在肌肉幾天造成，也不等於越痠增肌越多；舊ACSM宣導的概念可參考，但其中舊活動量數字不作本課最新基線。

## 恢復的多個面向

主觀感受、表現、睡眠、食慾與生活壓力可提供不同線索。固定48小時或一個穿戴分數不能保證所有系統都恢復；不同任務與組織時間不同，也沒有一個症狀可單獨診斷過度訓練。

## 平滑觀察

範例用三筆視窗計平均：視窗不足或有未知回None，不補0。平滑讓某些變動較容易看，但會延遲和掩蓋細節，不是將資料變成更真實的恢復指標。

## 需要處理的情況

持續或異常嚴重疼痛、明顯腫脹、功能受限或其他異常症狀，需適當評估；不能用痠痛正常當所有情況的通用解釋。教材不開傷後復健或從痠痛分數自動給訓練許可。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 38_rolling_missing.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:38_rolling_missing.py -->

## 練習與解答

**先自己判斷：** 三天平均下降，是否可以直接判已完全恢復並加量？

<details><summary>展開理由與驗算</summary>

不能。平滑值只是描述，還需任務、其他反應與資料品質；缺值和多系統恢復未被一個平均處理。

</details>

## 官方來源與研究

- [ACSM：DOMS概念說明；舊活動量段落不作本課基線](https://www.acsm.org/docs/default-source/files-for-resource-library/delayed-onset-muscle-soreness-%28doms%29.pdf)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
