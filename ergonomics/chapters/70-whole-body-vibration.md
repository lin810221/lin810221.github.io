# 全身振動與乘坐設備：方法不同，不能混算

把座椅、地面、車輛與暴露類型分清。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/35-vibration-types.svg" target="_blank" rel="noopener" aria-label="放大：HAV與WBV：同單位也不是同方法"><img src="assets/figures/35-vibration-types.svg" alt="左側手工具接觸，右側乘坐設備接觸；輸入、軸向權重與時間方法不同，不能直接混算。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 35｜HAV與WBV：同單位也不是同方法</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>比較乘坐設備與手工具的不同暴露，說明相同m/s²不代表方法和法規界線相同；本課HAV算術不等於完整WBV評估。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.hse.gov.uk/vibration/hav/index.htm">HSE：手臂振動</a> · <a href="https://www.hse.gov.uk/vibration/wbv/regulations.htm">HSE：WBV</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 接觸與來源

車輛、設備與地面可透過座位、腳或其他接觸傳遞振動；路況、速度、懸吊、座椅調整與維護都可能影響。不能只憑車型或座椅品牌判定實際暴露。

## WBV不是HAV換名稱

全身振動有不同各軸權重和評估方法，不能拿手－手臂三軸合成直接套用。姿勢、時間、衝擊與其他條件也需按正式方法處理。

## 地區法規

HSE說明英國WBV行動值0.5、限值 $\frac{1.15m}{s^{2}}$  A(8)，和HAV不同。這些不是台灣統一通行線，也不是低於就完全沒有健康需求的保證。

## 改善的來源

路面、設備維護、操作安排、速度與合適座椅等可成為評估方向。單靠更厚墊子不一定改善所有頻率，還需實際方法與新風險確認。

## 本課的界線

瀏覽器和Python只實作HAV已加權輸入的算術，WBV作概念及來源介紹，不冒稱已建完整評估器。需要現場時由適當受訓人員與工具處理，不能用手機曲線生成安全認證。

## 練習與解答

**先想一想：** HAV和WBV都用m/s²，所以可直接共用同一算法與界線嗎？

<details><summary>展開驗算與理由</summary>

不能。暴露來源、軸向權重、方法與法規背景不同，單位相同不等於評估等效。

</details>

## 正式來源與進一步閱讀

- [HSE：英國全身振動的不同方法](https://www.hse.gov.uk/vibration/wbv/regulations.htm)
- [HSE L140：手－手臂振動正式方法](https://www.hse.gov.uk/pubns/priced/l140.pdf)
- [HSE：英國HAV行動值與限值](https://www.hse.gov.uk/vibration/HAV/responsibilities.htm)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [台灣職安法：現行第6條](https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=N0060001&flno=6)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
