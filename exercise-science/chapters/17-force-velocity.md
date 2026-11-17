# 力量、速度與功率：任務優先順序

分清用力意圖、實際速度與機械功率，避免一律慢做或一律快做。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/09-force-velocity.svg" target="_blank" rel="noopener" aria-label="放大：力量、速度與輸出的關係"><img src="assets/figures/09-force-velocity.svg" alt="兩條任意形狀曲線區分力與功率概念，不具實測刻度或個人適用參數，也不把疲勞簡化為單一曲線。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 09｜力量、速度與輸出的關係</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>分別找到力與功率兩條線，說明任務若優先快速動作，和只比最高外部負荷問的問題不同；此示意沒有可直接取用的個人數字。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a> · <a href="https://training.seer.cancer.gov/anatomy/muscular/structure.html">NCI：骨骼肌構造</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 向心力量與速度

在控制的肌肉實驗中，向心速度與可產力有關；真實舉重還有加速、負荷、技術和器材。不能以簡單曲線精算個人每種動作的最佳負荷，也不將離心、等長直接當同一支曲線。

## 快的意圖與真的快

高外在負荷下，即使有快速施力意圖，實際速度仍可能較慢。功率任務需看可控制的動作、合適阻力與速度；把每次都故意拖很慢或讓每個動作盡可能加速，都不是通用原則。

## 外功率驗算

同20kg外物升0.5m，約98.07J；1秒與0.5秒平均外功率約98.07與196.13W。這只是外物的簡化正功，不含完整人體，也沒有證明任何個人的技術或關節可承受較快條件。

## 目標與測試對齊

若關注快速產力，還需看衝量、時間與專項；若關注最大力量，測試又不同。訓練安排先定結果，不能只用總噸數宣稱功率已提高。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 09_concentric_speed.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:09_concentric_speed.py -->

## 練習與解答

**先自己判斷：** 負荷很重所以移動慢，是否證明受試者沒有快速用力？

<details><summary>展開理由與驗算</summary>

不能。意圖與實際速度不同，還受負荷和任務限制；需正確測量和上下文，不能只由影片速度推意圖。

</details>

## 官方來源與研究

- [OpenStax：神經控制與肌肉張力](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-4-nervous-system-control-of-muscle-tension)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [ACSM：2026正式更新與適用範圍](https://acsm.org/resistance-training-guidelines-update-2026/)
- [OpenStax：肌纖維收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
