# 排錯：單位、定義、來源與解讀

依層次查找問題，不因程式成功就停止思考。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/47-report-trace.svg" target="_blank" rel="noopener" aria-label="放大：從原始紀錄追到可用摘要"><img src="assets/figures/47-report-trace.svg" alt="三欄將資料、摘要與解讀範圍分開，箭頭代表可追溯來源而非生理因果；沒有以未知當零。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 47｜從原始紀錄追到可用摘要</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>遇到合理卻可疑的數字，依次查原始單位、定義、來源和算術；圖中的流程沒有讓錯誤資料自動變真，也不能用漂亮圖表補完未知。</div>

<p class="health-figure-sources">圖解依據：<a href="https://acsm.org/resistance-training-guidelines-update-2026/">ACSM：2026健康成人阻力訓練更新</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 單位層

kg不是N，kg-reps不是J，W不是kcal；L/min與mL/kg/min需質量與1000倍轉換，配速與速度互為不同表示。先驗分母、時間和距離，再追小數誤差；負值、NaN與零分母應拒絕。

## 語意層

單組RIR-based RPE、Borg6–20與session CR10不混用；%HRR不是%HRmax； $VO_{2}peak$ 不無聲改max；計畫不是完成，休息0不是漏記。即使每行公式都對，欄位對錯仍會改結論。

## 來源層

WHO2020正式指南、2026更新說明頁、ACSM2026立場與研究搜尋截止分開。一般健康成人結果不自動涵蓋病人、兒少或菁英；新版某個特定族群回顧也不直接取代所有舊基礎知識。

## 解讀與技術層

比值不等於傷害風險，平滑不等於恢復，估1RM不等於實測或訓練指令。若import失敗，解壓完整ZIP並從examples執行；修改課文後重跑build，不直接改生成JS；輸出目錄已存在就換新路徑。

## 練習與解答

**先自己判斷：** 程式輸出正常且圖表漂亮，能否證明分析已適用真人？

<details><summary>展開理由與驗算</summary>

不能。還需單位、語意、來源、族群和解讀正確；計算成功不等於個人訓練或醫療適用已驗證。

</details>

## 官方來源與研究

- [Foster等：訓練負荷監測的方法與限制](https://pubmed.ncbi.nlm.nih.gov/28253038/)
- [Impellizzeri等：ACWR概念與方法陷阱](https://pubmed.ncbi.nlm.nih.gov/32502973/)
- [ACSM：2026阻力訓練立場聲明原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/)
- [Compendium：標準MET單位](https://pacompendium.com/unite-conversions/)
- [Python 3.15.2正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [完整範例、資料與測試](examples.zip)
