# 接觸、面積與壓力：同樣的力如何分布

分開外部均勻接觸模型與真實局部組織。

## 平均接觸壓力

$$
P=\frac{F}{A}
$$

N除以m²為Pa；100cm²=0.01m²，所以200N在均勻100cm²上為20kPa。若把cm²直接當m²，會差一萬倍。

## 截面應力不同

工程材料的單軸應力可用F/A描述，若面積用mm²，N/mm²等於MPa。它與椅緣、握柄或支撐面的接觸幾何不是同一測量，不能混用面積。

## 真實分布不均勻

邊緣、材料、形狀、姿勢與時間都會影響局部接觸。平均較低不保證每個局部都較低，也不直接表示血流、神經或皮膚沒有負擔。

## 任務應用

可觀察硬邊、腕部接觸、扶手與握柄，討論調整或分散接觸。但本課不建立壓力傷害門檻、不選配醫療鞋墊，也不以計算取代症狀評估。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 08_pressure_and_area.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:08_pressure_and_area.py -->

## 練習與解答

**先想一想：** 同樣的力分在較大面積，平均壓力降低，是否已保證任何人都更舒適？

<details><summary>展開驗算與理由</summary>

沒有。這只在均勻模型下成立，局部分布、時間、材料和個人需要仍影響實際感受與風險。

</details>

## 正式來源與進一步閱讀

- [OSHA：椅子、支撐與可調性](https://www.osha.gov/etools/computer-workstations/components/chairs)
- [OSHA：鍵盤與工作配置](https://www.osha.gov/etools/computer-workstations/components/keyboards)
- [OSHA：滑鼠與指向裝置](https://www.osha.gov/etools/computer-workstations/components/pointer-mouse)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
