# 版本與不確定：最新頁面不一定是最新方法

把發布、更新、查核和方法改版拆開記錄。

## 四種日期

正式方法發布日期、文件修訂日期、入口網頁更新與本課查核日期不同。NIOSH入口2026更新，不能因此把RNLE公式叫2026新版；現行引用手冊仍需標Revised9/2021。

## 更正會影響實作

2021 RNLE更正短工時恢復時間由舊誤字1.2倍改為1.0倍。若直接複製舊筆記，會把30分鐘搬抬後所需分類恢復條件錯寫36分鐘。這項更正是方法分類條件，不能變成個人醫療休息處方。

## 推薦可能撤回

NICE NG59在2026年7月撤回特定心理及合併方案建議與交叉引用，引用舊段落當現行會出錯。撤回也不能擴張解讀成所有心理社會因素無關或所有相關介入均被禁止。

## 未知不是看起來合理的預設

缺頻率表格條件、病況、實際量測或完整日資料，輸出應保留未知。需要假設才能算時，明確標教學假設；沒有看完或無法開啟完整正式來源，也需說清查核範圍。

## 讓他人可以追溯

記來源連結、正式版次、查核日期、已核實內容、限制和程式版本。更新課程時先看哪些結論受影響，再重跑相應算術和測試；只把日期改新，不代表內容已查核。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 45_uncertainty_and_versions.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:45_uncertainty_and_versions.py -->

## 練習與解答

**先想一想：** 把課程更新日期改成今天，就可以宣稱所有正式方法都已升到今天版本嗎？

<details><summary>展開驗算與理由</summary>

不行。需核對正式方法與更新內容，日期不能替代證據；網頁與方法版次、軟體版次、查核日應分開。

</details>

## 正式來源與進一步閱讀

- [NIOSH：RNLE現行入口（2026頁面更新）](https://www.cdc.gov/niosh/ergonomics/about/rnle.html)
- [NIOSH：2021修訂與短工時更正](https://stacks.cdc.gov/view/cdc/110725)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NICE NG59：2026-07-29更新狀態](https://www.nice.org.uk/guidance/ng59/chapter/Update-information)
- [Faculty of Pain Medicine：2026 NG59更新聲明](https://www.fpm.ac.uk/fpm-position-statement-july-2026-update-nice-ng59)
- [職安署：人因性危害預防指引（2014初版）](https://www.osha.gov.tw/media/o51ee2km/%E4%BA%BA%E5%9B%A0%E6%80%A7%E5%8D%B1%E5%AE%B3%E9%A0%90%E9%98%B2%E8%A8%88%E7%95%AB%E6%8C%87%E5%BC%95.pdf)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
