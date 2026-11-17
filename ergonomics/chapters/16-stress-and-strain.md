# 應力、應變與材料假設

知道形變是什麼，也知道為何不能直接推人體損傷。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/08-contact-area.svg" target="_blank" rel="noopener" aria-label="放大：接觸面積和平均壓力"><img src="assets/figures/08-contact-area.svg" alt="同力不同接觸面積的均勻模型，壓力與材料截面應力的問題不同，沒有人體損傷界線。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 08｜接觸面積和平均壓力</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>區分外部接觸面和材料截面，說出應力、應變各需什麼量測與假設；這張接觸圖不能直接替代組織材料測試。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 兩個不同量

應力描述力與截面關係，應變描述相對形變。教材工程應變為長度變化除原長，100mm變長1mm得到0.01、也就是1%；壓縮可有負號，需說方向。

## 理想彈性

在線性、單軸、特定小變形假設下，可用材料關係理解應力和應變。真實生物組織可能非線性、方向相關、隨時間改變，不能拿任意材料常數代表每條肌腱或椎間盤。

## 測量的來源

外物位移、皮膚角度和內部組織形變不同。若沒有相應測量與模型，就不應把手部移動幾公分轉成肌腱應變百分比。

## 時間與速度

相同最大力在不同速度、持續與重複下，可能有不同問題。用一個瞬間F/A忽略這些，不足以完成工作暴露與健康評估。

## 一個手算案例

100N作用於50mm²理想截面，算術為2MPa；若這個面積只是猜測，就要把結果標為假設，不能在人體圖片上寫成實測。換更精細小數也不會提高未知面積的可信度。

## 練習與解答

**先想一想：** 把皮膚表面量到的位移除以一個猜測長度，就能稱肌腱實際應變嗎？

<details><summary>展開驗算與理由</summary>

不能。需相應結構、測量與模型，表面位移和內部組織形變不同；假設算術不可冒充實測。

</details>

## 正式來源與進一步閱讀

- [NIH：肌腱、負荷與病變（2025）](https://newsinhealth.nih.gov/2025/12/tendon-trouble)
- [OpenStax：肌肉互動與槓桿](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-1-interactions-of-skeletal-muscles-their-fascicle-arrangement-and-their-lever-systems)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
