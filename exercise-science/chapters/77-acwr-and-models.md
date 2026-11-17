# ACWR與fitness-fatigue模型：描述不等於預測

親手計算比值，理解為何不提供傷害安全區或自動準備分數。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/39-monitor-model.svg" target="_blank" rel="noopener" aria-label="放大：描述模型、觀察與下一步"><img src="assets/figures/39-monitor-model.svg" alt="三條未校準曲線採同一任意基準，綠線為藍線減黃線的示例；不是實測疲勞、適應或傷害機率，決策需先核對資料。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 39｜描述模型、觀察與下一步</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>逐條說出曲線由假設產生，不是模型直接量到了身體狀態；ACWR或fitness-fatigue摘要不自動提供個人傷害機率和安全區間。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 比值的定義先清楚

本課用當週負荷除以前四個完整週平均，當週不混入分母，稱uncoupled示例。另一些文獻使用不同視窗、加權或包含當週，數字不能不加說明就比較。

## 手算

當週1100AU、前四週900、1000、1100、1000，平均1000，比值1.1。若前週有未知或平均為0，結果無定義或未知；不能補理想基線把比值算出來。

## 為何不畫安全區

原始方法批評指出比值、混雜與因果解讀等問題。某負荷比和傷害相關，並未證明操控比值能降低個人風險；本課不使用0.8–1.3之類區間核發安全許可，也不估受傷機率。

## 任意雙指數模型

fitness-fatigue示意以任意時間常數和係數累積兩種成分，解釋某種概念形狀；沒有用真人校準，不是恢復、進步或最佳比賽日預測。改參數看曲線，只是在探索假設。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 39_acwr_limit.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:39_acwr_limit.py -->

## 練習與解答

**先自己判斷：** 比值1.1落在網路稱安全的區，是否保證不會受傷？

<details><summary>展開理由與驗算</summary>

不保證。比值是指定定義下的描述，未建立個人因果風險模型；還有任務、能力、健康與多種因素，不能當安全許可。

</details>

## 官方來源與研究

- [Impellizzeri等：ACWR概念與方法陷阱](https://pubmed.ncbi.nlm.nih.gov/32502973/)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Foster等：session-RPE原始研究](https://pubmed.ncbi.nlm.nih.gov/11708692/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
