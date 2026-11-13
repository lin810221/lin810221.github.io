# 字體、距離與視角：把可讀性說清楚

算的是幾何，不是字級或視力處方。

## 高度和距離的關係

同樣實體文字高度，距離較遠時視角較小。教材以高度h、距離d算：

$$
\alpha=2\arctan\left(\frac{h}{2d}\right)
$$

兩者需同單位；範例h用mm、d用cm，先換算。

## 像素與字級不同

畫面字級、像素、實體毫米會受縮放與裝置影響，不能把同樣12pt當每台螢幕同一視角。內容對比、清晰和個人視覺也影響閱讀。

## 調整可讀性

可配合縮放、距離、反光與眼鏡需要討論。不是只叫人坐遠，也不是把字放大到任何程度都不影響其他任務；需試做和回顧。

## 程式的範圍

它不量視力、眼睛傷害或最佳字級。角度改變可教幾何，不能單獨預測疲勞、頸部負荷或疾病。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 20_visual_angle.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:20_visual_angle.py -->

## 練習與解答

**先想一想：** 同一軟體設12pt，是否代表不同裝置上眼睛看到的角度完全相同？

<details><summary>展開驗算與理由</summary>

不一定。實體大小、縮放和距離不同，視角也不同；字級不是完整可讀性或視力評估。

</details>

## 正式來源與進一步閱讀

- [OSHA：螢幕配置與視覺需求](https://www.osha.gov/etools/computer-workstations/components/monitors)
- [HSE：DSE工作站專用檢核表](https://www.hse.gov.uk/pubns/ck1.pdf)
- [OSHA：多種工作參考姿勢與變化](https://www.osha.gov/etools/computer-workstations/positions)
- [OSHA：桌面與下方空間](https://www.osha.gov/etools/computer-workstations/components/desks)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
