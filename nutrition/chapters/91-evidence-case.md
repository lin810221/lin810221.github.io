# 整合案例：審核一則營養新聞

從標題回到問題、原始計數與適用性，完成一頁查核紀錄。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/46-news-label-case.svg" target="_blank" rel="noopener" aria-label="放大：營養新聞與產品標示互相核對"><img src="assets/figures/46-news-label-case.svg" alt="新聞或廣告的主張和實際產品標示並列，追分母、對象、時間與來源，不因產品名字相同就外推原料或研究效果。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 46｜營養新聞與產品標示互相核對</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>將新聞的主要主張寫在左頁，找比較對象和結果期限，再說明缺少研究設計或分母時，不能只摘錄醒目百分比。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cochrane.org/evidence">Cochrane：健康證據與白話摘要</a> · <a href="https://ods.od.nih.gov/factsheets/WYNTK-Consumer/">NIH ODS：補充品須知</a> · <a href="https://www.mohw.gov.tw/cp-5269-70142-1.html">衛福部：現行包裝食品營養標示修正</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 案例資料

虛構新聞宣稱「某飲品讓不良事件少20%」。底稿是對照1000人100件、介入1000人80件、追蹤一年；沒有提供信賴區間，也尚未確認隨機與依從性。這些數字只用於學習，不代表真實產品研究。

## 先重建效果

事件風險10%與8%，RR0.8，絕對差2個百分點，點估計NNT50。標題若省去一年、基準風險和結果定義，就讓讀者無法評估實際意義；若是替代指標，又不能直接稱疾病事件。

## 再審核設計

確認分組、失訪、共介入、配方與劑量、比較飲品及不良事件。觀察研究還需處理混雜與反向因果；虛構計數本身不回答這些問題，不能由算術顯著感覺填補證據。

## 寫結論

可以描述點估計與缺漏，提出查原文、完整結果與研究設計的下一步；不能推薦讀者購買或宣稱人人風險降低20%。將目前支持與尚不確定分開，保留來源與查核日期。

## 可執行資料實驗

在[完整範例說明](examples/README.md)準備Python3.15.2後，於examples目錄執行 `python 46_evidence_case.py`。僅用標準函式庫，預設不連網。食物與紀錄是明示虛構資料；輸出用於檢查單位、來源與算術，不作個人需要量或診斷。

<!-- example:46_evidence_case.py -->

## 練習與解答

**請先判斷：** 此案例已能推薦每人每天喝一瓶嗎？

<details><summary>展開計算與理由</summary>

不能。劑量、配方、研究設計、不確定性與適用性等尚未確認；計數只能重建示範效果，沒有建立購買或使用建議。

</details>

## 官方參考與跨課閱讀

- [Cochrane：健康證據與白話摘要](https://www.cochrane.org/evidence)
- [NIH ODS：補充品須知](https://ods.od.nih.gov/factsheets/WYNTK-Consumer/)

[回課程總覽](#overview) · [下載程式、資料與測試](examples.zip)
