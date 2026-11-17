# 何時需要醫療：急性與進展訊號

辨認需要適時評估的資訊，不製作自測安全證書。

<!-- health-visual:start -->
## 圖解閱讀 {#visual-reading}

<figure class="health-figure"><a href="assets/figures/12-care-and-scope.svg" target="_blank" rel="noopener" aria-label="放大：照護訊號與來源範圍分開看"><img src="assets/figures/12-care-and-scope.svg" alt="情境需要適當評估，來源需核日期與適用範圍；不是自動風險分級或排除所有急症的清單。" width="860" height="520" loading="lazy"></a><figcaption><strong>圖 12｜照護訊號與來源範圍分開看</strong>原創概念示意，非比例；顏色輔助辨識，不代表正常異常。</figcaption></figure>

<div class="health-read-task"><strong>讀圖任務：</strong>從圖中指出及時評估不依網頁分數，回原課讀具體例子及限制；沒有列到的情況也不能自動宣告安全。</div>

<p class="health-figure-sources">圖解依據：<a href="https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/">IASP：疼痛定義</a> · <a href="https://www.cdc.gov/niosh/ergonomics/about/index.html">NIOSH：人體工學</a>。圖解查核2026-11-16；機構頁、方法與原課指南的版本分開。<a href="study/read-tasks.md">全部讀圖任務</a> · <a href="study-pack.zip">下載圖解學習包</a></p>

<!-- health-visual:end -->

## 不等網頁完成分析

背痛伴新發排尿或大小便控制異常、會陰或肛門周圍感覺改變、明顯或惡化的腿部無力等，應立即尋求醫療評估。重大事故後疼痛、急劇變化或其他嚴重身體不適也需按情境及時處理。

## 不自行確診

這些是評估訊號，不是只憑一項就宣稱馬尾症候群、骨折或感染。突然單側無力也可能屬其他急症，不能都當肌肉緊或姿勢問題。

## 沒有列到也不保證安全

清單不可能涵蓋所有病況，少一項不是安全通行證。反覆不適、麻、功能下降、發燒全身不適或快速惡化等，也值得合適評估。

## 準備描述

記何時開始、位置與分布、外傷、變化、功能、相關症狀及原用藥。程式只列哪些仍未知，不決定急迫等級或用分數排除需要。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 12_help_context.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:12_help_context.py -->

## 練習與解答

**先想一想：** 沒有符合清單上的全部項目，是否就可確定不需看醫療？

<details><summary>展開驗算與理由</summary>

不能。清單不是排除工具，需依當下症狀和背景處理；立即或進展問題不應因未全部符合而延誤。

</details>

## 正式來源與進一步閱讀

- [NHS：背痛與需立即評估的訊號](https://www.nhs.uk/conditions/back-pain/)
- [NICE NG127：成人神經症狀的評估與轉介](https://www.nice.org.uk/guidance/ng127/chapter/recommendations-for-adults-aged-over-16)
- [NICE NG59：2026-07-29更新狀態](https://www.nice.org.uk/guidance/ng59/chapter/Update-information)
- [IASP：2020修訂疼痛定義與說明](https://www.iasp-pain.org/publications/iasp-news/iasp-announces-revised-definition-of-pain/)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
