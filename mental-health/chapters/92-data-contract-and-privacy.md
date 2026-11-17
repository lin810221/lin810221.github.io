# 資料契約與隱私：用欄位保護解釋

讓每筆資料有狀態、單位、目的與限制。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/46-diary-privacy.svg" target="_blank" rel="noopener" aria-label="放大：日記欄位：先問用途，再決定收多少"><img src="assets/figures/46-diary-privacy.svg" alt="虛構記錄卡保留目的、時間、選擇和缺漏，身份欄不需要填入；不是要求公開日記。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 46｜日記欄位：先問用途，再決定收多少</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>把未知、錯誤和明確零分別放入資料欄位，說明契約可保護解釋與隱私；欄位通過驗證仍不代表資料真實或健康。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/questions-and-answers/item/stress">WHO：壓力問答</a> · <a href="https://www.nimh.nih.gov/health/topics/caring-for-your-mental-health">NIMH：照顧心理健康</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 日期與連續位置

資料要求14個唯一、連續、依序的排定日，不只是檔案有14列。缺漏仍保留位置，這樣圖與平均才知道少了哪天；不把未知日直接刪掉改成新時間線。

## 狀態與尺度

observed需有0–10原創評分，missing需保留空值，synthetic明示合成。程式拒絕不一致與錯尺度；它不是把具名量表改成原創後就能合法或有效使用的捷徑。

## 時間與功能分開

活動分鐘和在床窗口有各自單位，窗口不能直接當睡眠。計畫工時不是實際工時，也不等於心理容量。欄位命名若含混，後續算對公式也可能解錯問題。

## 隱私最小化

案例不含真實姓名、身分、創傷或醫療資訊。若日後處理真實資料，需另有適當目的、同意、安全與法律設計，不能直接沿用公開教學倉庫；雜湊也不能自動匿名化內容。

## 可審核原則

保留原始來源、程式版本、欄位定義和衍生公式，列未知與限制。程序成功只代表符合教材契約，不代表個人診斷、資料真實或介入效果已被驗證。

## 練習與解答

例如一個檔案有日期與罕見事件，即使沒有姓名，也可能和其他公開資料連結。教學資料使用全合成內容，省去不必要的暴露；真實研究另需合適審查與保護，不能只換檔名。

**先想一想：** 把真實日記的姓名刪掉，再加一個SHA-256就一定匿名嗎？

<details><summary>展開示範答案與理由</summary>

不能保證。內容和其他資訊可能仍識別人，雜湊不是匿名化證明；真實資料需另外的目的、同意與安全設計。

</details>

## 來源與進一步閱讀

- [全國法規資料庫：現行心理師法](https://law.moj.gov.tw/LawClass/LawAll.aspx?PCode=L0020098)
- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [NIMH：心理治療](https://www.nimh.nih.gov/health/topics/psychotherapies)
- [Python3.15.2官方正式發布](https://www.python.org/downloads/release/python-3152/)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
