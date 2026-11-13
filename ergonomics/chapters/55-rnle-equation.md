# RNLE：RWL與LI怎麼算

完整列出公式，同時說明它不是每個人的搬重上限。

## 工作設計方法

RNLE針對符合條件的雙手人工搬抬，使用幾何、頻率、工時與耦合等因素。它不是把任何物件重量輸入就完成，也不是個人體能測試。

## 公制公式

$$
RWL=23\,\mathrm{kg}\times HM\times VM\times DM\times AM\times FM\times CM
$$

$$
LI=\frac{L}{RWL}
$$

L為實際負荷質量。23kg是公式負荷常數，不是法律規定或每個人可搬重量。

## 正式查表示例

H25、V75、D50cm、A0度，示例每分鐘1次、短工時且恢復足夠、正式判good coupling，FM0.94、CM1，得RWL約19.67kg；12kg的LI約0.61。

## 解釋的界線

NIOSH以LI／CLI不超過1作工作設計方向，但不是個人安全、零風險或傷害機率。程式只演算一個端點，完整適用、表格判定與現場仍需確認。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 28_rnle_factors.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:28_rnle_factors.py -->

## 練習與解答

**先想一想：** LC=23kg，是否表示每個成人都可安全搬23kg？

<details><summary>展開驗算與理由</summary>

不是。它是特定方法的負荷常數，需各因素及適用條件；不代表個人能力、法律限重或零風險。

</details>

## 正式來源與進一步閱讀

- [NIOSH：RNLE現行入口（2026頁面更新）](https://www.cdc.gov/niosh/ergonomics/about/rnle.html)
- [NIOSH：2021修訂與短工時更正](https://stacks.cdc.gov/view/cdc/110725)
- [NIOSH 94-110：Revised 9/2021完整手冊](https://www.cdc.gov/niosh/media/pdfs/2026/06/94-110_2021-revision.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
