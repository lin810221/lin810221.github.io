# 血壓波動：重測能回答什麼

分辨自然變異、程序差異與值得處理的訊號。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/18-repeat-bp.svg" target="_blank" rel="noopener" aria-label="放大：波動、重測與照護回顧"><img src="assets/figures/18-repeat-bp.svg" alt="相對高度為虛構觀察，無正常異常線；重測提供資訊，但不能單由走向選擇個人處方。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 18｜波動、重測與照護回顧</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>沿四個時點先說觀察，再列可能的量測條件與生物變動，解釋第二次改變為何不一定證明某措施造成效果。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hpa.gov.tw/5020/20223/n">國健署：居家722與量測條件</a> · <a href="https://professional.heart.org/en/science-news/2026-guideline-for-the-prevention-detection-evaluation-and-management-of-ckm-syndrome">AHA：2026 CKM正式指南入口</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 讀值本來會變

血壓受活動、情緒、睡眠、疼痛、藥物和時段影響。連續兩次不同，不代表一定一筆錯誤，也不能立刻歸因為血管變差。先檢查休息、姿勢、袖帶、間隔與記錄，再看多日模式。

## 重複不是一直追低

同一時段依程序量測可估計觀察變化；若量十次只保留最低兩次，會產生選擇偏差。課程示範一組虛構重複值的平均和標準差，僅描述分散，不用標準差自動做疾病或器材診斷。

## 症狀與數字並看

新發胸痛、明顯呼吸困難、單側無力或語言困難等，應立即尋求緊急醫療評估，不能留在網頁反覆計算平均。無急症時，也需按臨床建議處理反覆異常、頭暈或量測困難。

## 報告保留背景

以「使用同一設備、三次讀值、休息與時段如附」描述，比用最低值取代當天紀錄更可追溯。缺漏和疑慮明示後，照護者才能決定是否需補測、評估設備或換用其他監測方式。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 18_repeat_variation.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:18_repeat_variation.py -->

## 練習與解答

**先自己判斷：** 連續測五次後只記最低一次，算不算提高準確？

<details><summary>展開驗算與理由</summary>

不算。這改變採樣規則並偏向較低值；應依預定程序保留讀值及背景。重複測量的目的在減少不確定，不是挑出想看到的數字。

</details>

## 官方來源與研究

- [2022台灣一般高血壓指南全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9121756/)
- [國健署2026居家722說明](https://www.hpa.gov.tw/5020/20223/n)
- [2026台灣高齡高血壓正式指南](https://pubmed.ncbi.nlm.nih.gov/42926177/)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
