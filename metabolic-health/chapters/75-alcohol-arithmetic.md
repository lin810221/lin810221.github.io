# 酒精量怎麼算：容量、濃度與純酒精

用明確單位記錄，不把算式變成安全飲酒額度。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/38-alcohol-volume.svg" target="_blank" rel="noopener" aria-label="放大：酒精：容量、濃度與時間型態"><img src="assets/figures/38-alcohol-volume.svg" alt="瓶子示意提醒容量不是酒精克數；計算暴露不等於有安全配額，圖不鼓勵開始飲酒。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 38｜酒精：容量、濃度與時間型態</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>指出容量、ABV比例和密度三項，說明百分比為何需先轉成比例，並辨識瓶子大小不是純酒精量。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.who.int/news-room/fact-sheets/detail/alcohol">WHO：酒精與健康</a> · <a href="https://www.niddk.nih.gov/health-information/liver-disease/nafld-nash">NIDDK：脂肪肝機制背景（原頁沿用舊名）</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 容量不是酒精量

一杯大小和酒精濃度不同，不能只寫「一杯」。ABV是酒精體積百分比；5%需用0.05，並非5。酒款、容器與倒入量不明時，應保留估計範圍或未知。

## 純酒精近似式

教材用乙醇密度約0.789 g/mL：

$$
\mathrm{alcohol\;(g)}=\mathrm{volume\;(mL)}\times\mathrm{ABV}\times0.789
$$

330mL、5%約13.0g。這是化學近似，不是個人風險估計；各國「標準杯」定義也不同，不能直接將杯數跨國比較。

## 紀錄要有時間

相同總量集中在一次與分散多日，暴露型態不同。肝病、用藥、懷孕、駕駛與依賴等背景都重要；不能只從平均每日克數判斷全部風險。

## 不為預防建議開始喝

WHO資料指出酒精具有多種健康傷害，不能以可能升高HDL或觀察研究的表面相關，建議未飲酒者開始。這份算式沒有安全飲酒配額、也不從FIB-4判定可喝多少。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 38_alcohol_units.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:38_alcohol_units.py -->

## 練習與解答

**先自己判斷：** 330mL、5%啤酒的純酒精是否為330×5×0.789？

<details><summary>展開驗算與理由</summary>

應先把5%換成0.05，因此約13.0g。直接乘5會大100倍；計算結果不是建議攝取量。

</details>

## 官方來源與研究

- [WHO：酒精與健康風險](https://www.who.int/news-room/fact-sheets/detail/alcohol)
- [EASL2024 MASLD正式指南](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299976/)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
