# 人體計測與適配：百分位不是一個完整的人

從伸得到與容得下，理解多尺寸聯合設計。

## 伸取和淨空方向不同

按鈕太遠，較短伸取能力者可能困難；空間太小，較大淨空需要者可能受限。設計要先知道是哪種限制，不是所有尺寸都取平均。

## 多項尺寸不一定同時極端

同一人的身高、腿部空間和手臂伸取不必有相同百分位。把不同極端拼成一個不存在的人，或各尺寸涵蓋95%就宣稱整體95%，都需要小心。

## 虛構樣本練習

本課12個合成個案有伸取與淨空需求，兩筆資料未完整。以距離60、空間62cm的兩項明示條件，已知符合3、已知不符7、未知2；已知比例3/10不是全人口涵蓋率。

## 設計仍要試用

尺寸符合不保證舒適、力量、視覺和整體任務適合。範例只算幾何條件，不用虛構資料冒充台灣人體計測常模或安全認證。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 14_sample_geometry.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:14_sample_geometry.py -->

## 練習與解答

**先想一想：** 兩個尺寸各自涵蓋多數人，就可直接說同時符合的比例也相同嗎？

<details><summary>展開驗算與理由</summary>

不能。需要聯合分布與同一人的資料；邊際百分比不能直接替代聯合適配，缺漏也要保留。

</details>

## 正式來源與進一步閱讀

- [OSHA：椅子、支撐與可調性](https://www.osha.gov/etools/computer-workstations/components/chairs)
- [OSHA：桌面與下方空間](https://www.osha.gov/etools/computer-workstations/components/desks)
- [HSE：DSE工作站專用檢核表](https://www.hse.gov.uk/pubns/ck1.pdf)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)
- [OSHA：多種工作參考姿勢與變化](https://www.osha.gov/etools/computer-workstations/positions)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
