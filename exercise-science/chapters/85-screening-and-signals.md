# 運動前篩檢與警訊：資料不足不給綠燈

了解篩檢流程的目的，知道何時需要停止與尋求專業協助。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/43-screen-pain.svg" target="_blank" rel="noopener" aria-label="放大：資料、感受與專業評估的界線"><img src="assets/figures/43-screen-pain.svg" alt="四張資訊卡把資料不足、個人感受、功能和必要評估分開，不以紅綠燈或單一疼痛分數發運動許可。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 43｜資料、感受與專業評估的界線</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>先逐卡列目前已知與未知，說明為何缺少警訊資料不能當作沒有警訊；這張圖不能取代正式運動前評估或替讀者發綠燈。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/publications/i/item/9789240015128">WHO：2020身體活動與久坐正式指南</a> · <a href="https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/">IASP：疼痛定義及個人經驗</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 篩檢處理的是適用性

目前活動、已知健康狀況、症狀與想做的強度，是重要資訊。篩檢不等於完整檢查，也不保證零風險；Exercise is Medicine表有其2019版和較早演算法背景，不能只看下載頁日期當全新指南。

## 不自動填否

沒有問過的症狀、疾病或用藥是未知，不是已確認沒有。範例只列待查欄位，不由缺值輸出可做最大測試，也不將所有年齡的人一律要求相同流程。

## 異常反應

活動中胸部不適、暈厥或異常嚴重呼吸困難等，應停止並尋求適當醫療協助，緊急時立即啟動當地救援。即使手錶區域正常，也不能用分數否定症狀；不要以完成課表優先。

## 不同分工

一般活動教育、動作教學、臨床測試與傷病評估有不同能力範圍。教材支持理解與紀錄，合格專業依實際背景決定適用安排；單一網頁條件不能涵蓋所有疾病和環境。

## 可執行實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 43_screening_information.py`。不需要API、模型或第三方套件。資料與參數為明示虛構情境，輸出是可檢查的算術與觀察，不是個人課表、醫療許可或傷害預測。

<!-- example:43_screening_information.py -->

## 練習與解答

**先自己判斷：** 問卷沒填症狀，程式應把它視為沒有症狀以便繼續嗎？

<details><summary>展開理由與驗算</summary>

不應。未評估與已確認沒有不同；保留未知並補資訊，不能從缺值核發運動或最大測試許可。

</details>

## 官方來源與研究

- [Exercise is Medicine：運動前篩檢表與背景](https://www.exerciseismedicine.org/wp-content/uploads/2021/04/EIM-exercise-preparticipation-screening.pdf)
- [WHO：2020身體活動與久坐正式指南](https://www.who.int/publications/i/item/9789240015128)
- [CDC：慢性健康狀況與身心障礙活動](https://www.cdc.gov/physical-activity-basics/guidelines/chronic-health-conditions-and-disabilities.html)
- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
